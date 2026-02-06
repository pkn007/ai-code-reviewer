#!/usr/bin/env python3
import httpx
import re
from typing import Dict, List

async def fetch_incremental_or_full_diff(
    workspace: str,
    repo: str,
    pr_id: int,
    old_head: str | None,
    new_head: str,
    token: str
) -> tuple[str, bool]:
    """
    Returns (diff_text, is_incremental).

    - If old_head is None → full PR diff
    - If old_head exists   → incremental diff old_head..new_head
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream",
        "Cache-Control": "no-cache",
    }

    base = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}"

    # CASE 1 — First-time processing → fetch FULL DIFF
    if old_head is None:
        url = f"{base}/pullrequests/{pr_id}/diff"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            return resp.text, False  # not incremental

    # CASE 2 — Incremental diff between commits
    diff_path = f"diff/{old_head}..{new_head}"
    url = f"{base}/{diff_path}?from_pullrequest_id={pr_id}&topic=true"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)

    # If incremental is unsupported or fails → fallback to full diff
    if resp.status_code != 200:
        fallback = f"{base}/pullrequests/{pr_id}/diff"
        async with httpx.AsyncClient() as client:
            resp2 = await client.get(fallback, headers=headers)
        return resp2.text, False

    return resp.text, True


def extract_changed_files_from_diff(diff_text: str) -> List[str]:
    """
    Parse raw unified diff text and extract list of changed file paths.
    Works for incremental diffs as well as full diffs.
    """
    files = set()

    # Example line:
    # diff --git a/src/Main.java b/src/Main.java
    pattern = re.compile(r'^diff --git a/(.+?) b/', re.MULTILINE)

    for match in pattern.finditer(diff_text):
        files.add(match.group(1))

    return sorted(files)


# ---------- Regex ----------
FILE_HEADER_RE = re.compile(r'^diff --git a/(.+?) b/(.+)$')
HUNK_HEADER_RE = re.compile(r'^@@')
JAVA_EXT = ".java"

# Single-line comment
SL_COMMENT = re.compile(r'^\s*//')

# Block comment start / end
BLOCK_COMMENT_START = re.compile(r'/\*')
BLOCK_COMMENT_END = re.compile(r'\*/')

# Javadoc continuation
JAVADOC_LINE = re.compile(r'^\s*\*')

def split_diff_by_file(diff_text: str) -> Dict[str, List[str]]:
    files = {}
    current = None

    for line in diff_text.splitlines():
        m = FILE_HEADER_RE.match(line)
        if m:
            current = m.group(2)
            files[current] = []
            continue

        if current:
            files[current].append(line)

    return files


def count_non_comment_java_changes(diff_lines: List[str]) -> int:
    """
    Counts only non-comment, non-empty Java code changes.
    """
    count = 0
    inside_block_comment = False

    for line in diff_lines:
        # Only consider actual additions / deletions
        if not (line.startswith("+") or line.startswith("-")):
            continue

        # Skip diff headers
        if line.startswith("+++ ") or line.startswith("--- "):
            continue

        code = line[1:].strip()

        # Empty line
        if not code:
            continue

        # Handle block comments
        if inside_block_comment:
            if BLOCK_COMMENT_END.search(code):
                inside_block_comment = False
            continue

        if BLOCK_COMMENT_START.search(code):
            if not BLOCK_COMMENT_END.search(code):
                inside_block_comment = True
            continue

        # Skip single-line & javadoc comments
        if SL_COMMENT.match(code) or JAVADOC_LINE.match(code):
            continue

        # Count only real code
        count += 1

    return count


def extract_java_files_with_min_changes(
    diff_text: str,
    min_lines: int,
) -> List[str]:
    """
    Returns Java files having >= min_lines of non-comment code change.
    Works for full + incremental diffs.
    """
    result = []
    files = split_diff_by_file(diff_text)

    for file, lines in files.items():
        if not file.endswith(JAVA_EXT):
            continue

        changed = count_non_comment_java_changes(lines)
        if changed >= min_lines:
            result.append(file)

    return sorted(result)


