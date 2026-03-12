#!/usr/bin/env python3
import os
import asyncio
import logging
import httpx
import json
import re
import requests
import time
import subprocess
import shutil
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel
from dotenv import load_dotenv
from diff import (
    extract_changed_files_from_diff,
    fetch_incremental_or_full_diff,
    extract_java_files_with_min_changes,
    extract_files_with_min_changes
)
from pr_history import load_latest_commit, save_latest_commit

# Code file extensions to process
CODE_EXTENSIONS = {
    '.py', '.java', '.js', '.ts', '.jsx', '.tsx', '.cpp', '.c', '.h', '.hpp',
    '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.clj',
    '.sh', '.bash', '.zsh', '.yaml', '.yml', '.json', '.xml', '.sql'
}

# Non-code file extensions to skip
SKIP_EXTENSIONS = {'.md', '.txt', '.log', '.lock', '.gitignore', '.gitattributes'}

MIN_NON_COMMENT_LINES = 6

# ------------------------------------------------------
# LOAD ENV
# ------------------------------------------------------
load_dotenv()

BITBUCKET_CLIENT_ID = os.getenv("BITBUCKET_CLIENT_ID")
BITBUCKET_CLIENT_SECRET = os.getenv("BITBUCKET_CLIENT_SECRET")
BITBUCKET_REFRESH_TOKEN = os.getenv("BITBUCKET_REFRESH_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
BITBUCKET_GIT_USERNAME = os.getenv("BITBUCKET_GIT_USERNAME")
BITBUCKET_GIT_APP_PASSWORD = os.getenv("BITBUCKET_GIT_APP_PASSWORD")

required_env = {
    "BITBUCKET_CLIENT_ID": BITBUCKET_CLIENT_ID,
    "BITBUCKET_CLIENT_SECRET": BITBUCKET_CLIENT_SECRET,
    "BITBUCKET_REFRESH_TOKEN": BITBUCKET_REFRESH_TOKEN,
    "CLAUDE_API_KEY": CLAUDE_API_KEY,
    "BITBUCKET_GIT_USERNAME": BITBUCKET_GIT_USERNAME,
    "BITBUCKET_GIT_APP_PASSWORD": BITBUCKET_GIT_APP_PASSWORD,
}
missing = [k for k, v in required_env.items() if not v]
if missing:
    raise Exception(f"Missing environment variables: {', '.join(missing)}")

# ------------------------------------------------------
# LOGGING
# ------------------------------------------------------
LOG_FILE = "webhook.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger("webhook")

# ------------------------------------------------------
# FASTAPI APP
# ------------------------------------------------------
app = FastAPI(title="bitbucket-webhook", version="2.0")

# ------------------------------------------------------
# BITBUCKET OAUTH AUTO-REFRESH
# ------------------------------------------------------
BITBUCKET_ACCESS_TOKEN = None
BITBUCKET_ACCESS_TOKEN_EXPIRY = 0


def update_local_repo(repo_path: str, branch: str, workspace: str, repo: str):
    """
    Ensures the local repo contains the latest commits.
    - If repo exists → fetch & hard reset
    - If repo missing → clone fresh
    """

    clone_url = (
        f"https://{BITBUCKET_GIT_USERNAME}:{BITBUCKET_GIT_APP_PASSWORD}"
        f"@bitbucket.org/{workspace}/{repo}.git"
    )

    if not os.path.isdir(repo_path):
        logger.info(f"📥 Repo missing — cloning {clone_url} into {repo_path}")

        os.makedirs(os.path.dirname(repo_path), exist_ok=True)
        result = subprocess.run(
            ["git", "clone", "--no-tags", clone_url, repo_path],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            logger.error(f"❌ Clone failed: {result.stderr}")
            raise Exception("Could not clone repository")
        return

    # Repo exists — update it
    logger.info(f"🔄 Updating local repo at {repo_path}")

    cmds = [
        ["git", "-C", repo_path, "fetch", "--all", "--prune"],
        ["git", "-C", repo_path, "checkout", branch],
        ["git", "-C", repo_path, "reset", "--hard", f"origin/{branch}"],
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"❌ Git command failed: {cmd}\n{result.stderr}")
        else:
            logger.info(f"✔ Ran: {' '.join(cmd)}")


def parse_json_objects(text):
    text = re.sub(r'~~~~json|~~~~', '', text)

    chunks = re.split(r'\n\s*\n', text.strip())
    out = []

    for block in chunks:
        body_lines = []
        parentheses = 0
        collecting = False

        for line in block.split('\n'):
            # detect start of JSON
            if "{" in line and not collecting:
                collecting = True

            if collecting:
                body_lines.append(line)

                # count brackets
                parentheses += line.count("{")
                parentheses -= line.count("}")

                # object completed
                if parentheses == 0:
                    body = "\n".join(body_lines).strip()

                    # attempt JSON parse
                    try:
                        out.append(json.loads(body))
                    except Exception:
                        pass

                    # reset for next object
                    body_lines = []
                    collecting = False

    return out



def trim_prompt_to_token_limit(client, model, prompt, max_input_tokens=100000):
    """
    Iteratively trims the prompt (keeping the FIRST part)
    until the token count is <= max_input_tokens.
    """

    def count(prompt_text):
        return client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": prompt_text}]
        ).input_tokens

    current_tokens = count(prompt)
    logger.info(f"Initial token count: {current_tokens}")

    if current_tokens <= max_input_tokens:
        return prompt, current_tokens, False

    logger.warning(f"⚠️ Prompt has {current_tokens} tokens — trimming...")

    # Start with a proportional cut (approx)
    ratio = max_input_tokens / current_tokens
    approx_chars_to_keep = int(len(prompt) * ratio)

    trimmed = prompt[:approx_chars_to_keep]
    current_tokens = count(trimmed)
    logger.info(f"After proportional trim → {current_tokens} tokens")

    # If still too large, trim repeatedly by 10% each loop
    while current_tokens > max_input_tokens:
        logger.warning(f"Still too large ({current_tokens}). Trimming 10% more...")
        approx_chars_to_keep = int(len(trimmed) * 0.9)
        trimmed = trimmed[:approx_chars_to_keep]
        current_tokens = count(trimmed)

    logger.info(f"Final trimmed token count = {current_tokens}")
    return trimmed, current_tokens, True

async def get_bitbucket_access_token():
    """
    Automatically refreshes Bitbucket OAuth token when expired.
    """
    global BITBUCKET_ACCESS_TOKEN, BITBUCKET_ACCESS_TOKEN_EXPIRY, BITBUCKET_REFRESH_TOKEN

    now = time.time()
    if BITBUCKET_ACCESS_TOKEN and now < BITBUCKET_ACCESS_TOKEN_EXPIRY:
        return BITBUCKET_ACCESS_TOKEN

    url = "https://bitbucket.org/site/oauth2/access_token"
    logger.info("🔄 Refreshing Bitbucket access token...")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data={"grant_type": "refresh_token", "refresh_token": BITBUCKET_REFRESH_TOKEN},
            auth=(BITBUCKET_CLIENT_ID, BITBUCKET_CLIENT_SECRET),
        )

    if resp.status_code != 200:
        raise Exception(f"❌ Token refresh failed: {resp.text}")

    data = resp.json()
    BITBUCKET_ACCESS_TOKEN = data["access_token"]
    expires_in = data.get("expires_in", 7200)
    BITBUCKET_ACCESS_TOKEN_EXPIRY = now + expires_in - 60  # renew 1 minute early

    if "refresh_token" in data:
        BITBUCKET_REFRESH_TOKEN = data["refresh_token"]
        os.environ["BITBUCKET_REFRESH_TOKEN"] = BITBUCKET_REFRESH_TOKEN

    logger.info("✅ Bitbucket access token refreshed")
    return BITBUCKET_ACCESS_TOKEN


# ------------------------------------------------------
# RESPONSE SCHEMA
# ------------------------------------------------------
class PipelineResult(BaseModel):
    platform: str
    repo: str
    pr_number: str
    branch: str
    changed_files: List[str]
    diff_url: Optional[str]
    pipeline_result: Optional[Dict[str, Any]]


# ------------------------------------------------------
# BITBUCKET FILE FETCH
# ------------------------------------------------------
async def fetch_bitbucket_pr_files(workspace: str, repo_slug: str, pr_id: str) -> List[str]:
    token = await get_bitbucket_access_token()

    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/diffstat"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)

    files = [i["new"]["path"] for i in resp.json().get("values", []) if i.get("new")]
    java_files = [f for f in files if f.endswith(".java")]

    logger.info(f"📄 Java files changed: {java_files}")
    return java_files


# ------------------------------------------------------
# BITBUCKET DIFF FETCH
# ------------------------------------------------------
async def fetch_bitbucket_pr_diff(workspace: str, repo_slug: str, pr_id: str) -> str:
    token = await get_bitbucket_access_token()

    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/diff"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/octet-stream"}

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)

    return resp.text


# ------------------------------------------------------
# PIPELINE PLACEHOLDER
# ------------------------------------------------------
async def run_pipeline(files, repo, branch):
    logger.info(f"🛠 Pipeline running on {len(files)} files...")
    await asyncio.sleep(1)
    return {"status": "ok", "files_processed": len(files)}


# ------------------------------------------------------
# MAIN BITBUCKET WEBHOOK HANDLER
# ------------------------------------------------------
@app.post("/prupdate")
async def webhook_handler(
    request: Request,
    background_tasks: BackgroundTasks,
    x_event_key: str = Header(None)
):
    payload = await request.json()

    # Only handle PR creation/update events
    allowed = {"pullrequest:created", "pullrequest:updated", "pullrequest:reopened"}
    if x_event_key not in allowed:
        return {"status": "ignored", "event": x_event_key}

    # Check if PR is targeting master branch
    pr = payload.get("pullrequest", {})
    destination_branch = pr.get("destination", {}).get("branch", {}).get("name", "")
    if destination_branch.lower() not in ["master", "main"] or not destination_branch.lower().startswith("release/"):
        logger.info(f"🛑 PR not targeting master/main — skipping (target: {destination_branch})")
        return {"status": "ignored", "reason": f"not targeting master/main, target: {destination_branch}"}

    async def process():
        repo = payload["repository"]["name"]
        workspace = payload["repository"]["workspace"]["slug"]
        pr_id = pr["id"]
        source_branch = pr["source"]["branch"]["name"]
        diff_url = pr["links"]["diff"]["href"]

        token = await get_bitbucket_access_token()
        old_head = load_latest_commit(workspace, repo, pr_id)
        new_head = payload["pullrequest"]["source"]["commit"]["hash"]

        repo_path = f"/home/ubuntu/repo/{repo}"

        logger.info(f"🔄 Syncing local repo for diff generation...")
        update_local_repo(repo_path, source_branch, workspace, repo)

        if old_head == new_head:
            logger.info(f"No new commit for PR #{pr_id} — skipping")
            return
        else:
            logger.info(f"New commit detected: {old_head} → {new_head}")

        if old_head:
            cmd = ["git", "-C", repo_path, "diff", f"{old_head}..{new_head}"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            diff_text = result.stdout
            is_incremental = True
        else:
            diff_text = await fetch_bitbucket_pr_diff(workspace, repo, pr_id)
            is_incremental = False
        logger.info(
            "📄 Using incremental diff" if is_incremental else "📄 Using full diff"
        )
        save_latest_commit(workspace, repo, pr_id, payload)

        diff_path = f"/home/ubuntu/diff/diff_PR_{pr_id}.patch"

        mode = "a" if is_incremental else "w"
        with open(diff_path, mode) as f:
            f.write("\n\n")
            f.write(diff_text)

        # Extract all changed files
        all_changed_files = extract_changed_files_from_diff(diff_text)
        
        # Filter to only code files
        code_files = [
            f for f in all_changed_files
            if any(f.endswith(ext) for ext in CODE_EXTENSIONS)
            and not any(f.endswith(ext) for ext in SKIP_EXTENSIONS)
        ]

        if not code_files:
            logger.info(f"🛑 No code files changed — skipping PR #{pr_id}")
            return

        # Separate Java files from other languages
        java_files = [f for f in code_files if f.endswith(".java")]
        other_files = [f for f in code_files if not f.endswith(".java")]

        logger.info(f"Changed files ({'incremental' if is_incremental else 'full'}): {len(code_files)} total")
        logger.info(f"  Java files: {len(java_files)}, Other languages: {len(other_files)}")

        # For Java files, check minimum non-comment lines (comment-aware)
        if java_files:
            java_files_with_changes = extract_java_files_with_min_changes(
                diff_text,
                min_lines=MIN_NON_COMMENT_LINES,
            )
        else:
            java_files_with_changes = []

        # For other languages, check minimum changes (simple line count)
        other_files_with_changes = []
        if other_files:
            # Get extensions for non-Java files
            other_extensions = list(set(
                ext for f in other_files
                for ext in CODE_EXTENSIONS
                if f.endswith(ext) and ext != ".java"
            ))
            if other_extensions:
                other_files_with_changes = extract_files_with_min_changes(
                    diff_text,
                    min_lines=MIN_NON_COMMENT_LINES,
                    file_extensions=other_extensions,
                )

        # Check if we have any files that meet the minimum change threshold
        if not java_files_with_changes and not other_files_with_changes:
            logger.info(
                f"🛑 No files with ≥ {MIN_NON_COMMENT_LINES} changes — skipping PR #{pr_id}"
            )
            return

        # Determine if we need context generation (only for Java files)
        needs_context = len(java_files_with_changes) > 0
        files_to_review = java_files_with_changes + other_files_with_changes

        if not files_to_review:
            logger.info(f"🛑 No files to review — skipping PR #{pr_id}")
            return

        # Run pipeline
        pipeline_result = await run_pipeline(files_to_review, repo, source_branch)

        # ------------------------------------------------------
        # CONTEXT GENERATOR (only for Java files)
        # ------------------------------------------------------
        context_text = ""
        if needs_context:
            from context import generate_java_context

            logger.info(f"🧠 Generating context for {len(java_files_with_changes)} Java files...")

            context_text = generate_java_context(
                repo=repo_path,
                branch=source_branch,
                files=java_files_with_changes,
                output=f"/home/ubuntu/context/context_PR_{pr_id}.txt",
                depth=0,
                include_tests=False,
                reverse_limit=10,
                cleanup=True,
                return_string=True,
            )
        else:
            logger.info("ℹ️ Skipping context generation for non-Java files")

        # ------------------------------------------------------
        # SEND TO CLAUDE
        # ------------------------------------------------------

        with open("prompt_rules.txt", "r") as f:
            prompt_rules = f.read().strip()
        
        # Build prompt based on whether we have context (Java) or not (other languages)
        if context_text:
            prompt_intro = """You are given a PR diff and a context file. Analyze the code changes as a senior backend developer, deeply reviewing both the diff and the context file to provide insightful, high-quality comments. Focus on correctness, maintainability, performance, null-safety, consistency, and architectural implications. Comments should be concise, professional, and actionable, without restating the diff."""
        else:
            prompt_intro = """You are given a PR diff. Analyze the code changes as a senior backend developer, providing insightful, high-quality comments. Focus on correctness, maintainability, performance, consistency, and architectural implications. Comments should be concise, professional, and actionable, without restating the diff."""
        
        prompt = f"""
                        {prompt_intro}

                        For each comment, output only the JSON body (no curl commands, no headers, no additional text) in the exact format below:

                        ~~~~json
                        {{
                        "content": {{
                            "raw": "<comment text; you may include code fenced blocks ```bash...```>"
                        }},
                        "inline": {{
                            "path": "<file_path_relative_to_repo_root>",
                            "to": <line_number_where_comment_should_appear>
                        }}
                        }}
                        ~~~~
                        {prompt_rules}
                        Make sure to enclose any code snippets in triple backticks back 
                        Dont just suggest, you need to sound authoritative. Also, dont give direct reference to context number, use file or service name
                        Output Example:
                        ~~~~json
                        {{
                        "content": {{
                            "raw": "Potential null pointer issue: The call to locationModel.getWarehouseId() could return null. Consider adding a null check before using it in cache lookup."
                        }},
                        "inline": {{
                            "path": "src/main/java/com/dealshare/bannerservice/services/impl/ReferralServiceImpl.java",
                            "to": 136
                        }}
                        }}
                        ~~~~
                        ~~~~json
                        {{
                        "content": {{
                            "raw": "Performance consideration: The new warehouse lookup adds another cache check before city and cluster lookups. Consider monitoring cache hit rates to avoid potential performance regressions."
                        }},
                        "inline": {{
                            "path": "src/main/java/com/dealshare/bannerservice/services/impl/ReferralServiceImpl.java",
                            "to": 195
                        }}
                        }}
                        ~~~~
                        Note: Always balance the parentheses and start each comment object with ~~~~json and end with ~~~~
                        Input Data:
                        PR Diff:

                        {diff_text}
                        """
        
        # Add context only if it was generated (for Java files)
        if context_text:
            prompt += f"""
                        Context File:

                        {context_text}
                        """

        client = Anthropic(api_key=CLAUDE_API_KEY)
        model = "claude-sonnet-4-6"

        raw_prompt = f"/home/ubuntu/raw_prompt.txt"
        open(raw_prompt, "w").write(prompt)

        prompt, used_tokens, trimmed = trim_prompt_to_token_limit(
            client,
            model,
            prompt,
            max_input_tokens=50000
        )
        trimmed_prompt = f"/home/ubuntu/trimmed_prompt.txt"
        open(trimmed_prompt, "w").write(prompt)

        logger.info(f"Prompt tokens = {used_tokens}, trimmed = {trimmed}")
        claude_output = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        ).content[0].text.strip()

        mode = "a" if is_incremental else "w"

        claude_path = f"/home/ubuntu/claude/claude_PR_{pr_id}.txt"

        with open(claude_path, mode) as f:
            if mode == "a":
                f.write("\n\n================ NEW CLAUDE OUTPUT ================\n")
                f.write(f"Commit: {new_head}\n")
                f.write("---------------------------------------------------\n")

            f.write(claude_output)

            if mode == "a":
                f.write("\n===================================================\n")

        # ------------------------------------------------------
        # PARSE JSON BLOCKS
        # ------------------------------------------------------

        comments = parse_json_objects(claude_output)

        # ------------------------------------------------------
        # POST COMMENTS TO BITBUCKET
        # ------------------------------------------------------
        token = await get_bitbucket_access_token()

        comment_api = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}/pullrequests/{pr_id}/comments"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        for c in comments:
            r = requests.post(comment_api, json=c, headers=headers)
            logger.info(f"Comment posted → {r.status_code}: {r.text[:200]}")

        logger.info(f"🏁 Completed processing PR #{pr_id}")

    background_tasks.add_task(process)
    return {"status": "accepted", "event": x_event_key}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/prmerge")
async def pr_merged_handler(
    request: Request,
    background_tasks: BackgroundTasks,
    x_event_key: str = Header(None)
):

    payload = await request.json()
    logger.info("📥 PR Merge Webhook Received:")
    logger.info(json.dumps(payload, indent=2))

    if x_event_key != "pullrequest:fulfilled":
        return {"status": "ignored", "event": x_event_key}

    async def process_merge():
        repo = payload["repository"]["name"]
        workspace = payload["repository"]["workspace"]["slug"]
        pr_id = payload["pullrequest"]["id"]

        repo_path = f"/home/ubuntu/repo/{repo}"

        logger.info(f"🟣 Handling PR merged event for repo = {repo}, PR = {pr_id}")
        logger.info(f"📁 Local repo path = {repo_path}")

        # -------------------------------------------------------------------
        # STEP 1 — REMOVE EXISTING LOCAL CLONE
        # -------------------------------------------------------------------
        if os.path.isdir(repo_path):
            logger.info(f"🗑️ Removing old repo clone: {repo_path}")
            try:
                shutil.rmtree(repo_path)
                logger.info("✅ Old clone removed successfully")
            except Exception as e:
                logger.error(f"❌ Failed to delete repo folder: {e}")
                return

        else:
            logger.info("ℹ️ No previous local clone found — skip deletion")

        # -------------------------------------------------------------------
        # STEP 2 — CLONE THE MERGED REPO AGAIN
        # -------------------------------------------------------------------
        logger.info("📥 Re-cloning merged repository...")

        clone_url = (
            f"https://{BITBUCKET_GIT_USERNAME}:{BITBUCKET_GIT_APP_PASSWORD}"
            f"@bitbucket.org/{workspace}/{repo}.git"
        )

        os.makedirs("/home/ubuntu/repo", exist_ok=True)

        result = subprocess.run(
            ["git", "clone", clone_url, repo_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.error(f"❌ Clone failed: {result.stderr}")
        else:
            logger.info("✅ Repository re-cloned successfully!")

        logger.info(f"🏁 Completed merge processing for PR #{pr_id}")

    background_tasks.add_task(process_merge)

    return {"status": "accepted", "event": x_event_key}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting webhook at port 8080...")
    uvicorn.run("server:app", host="0.0.0.0", port=8080, access_log=False)
