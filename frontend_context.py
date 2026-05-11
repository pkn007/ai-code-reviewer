#!/usr/bin/env python3
"""
Frontend context generator for AI code review.
Supports: React, React Native, Next.js, Android (Kotlin), iOS (Swift)
"""
import os
import re
import logging
from typing import Dict, List, Optional, Set

logger = logging.getLogger("frontend_context")

# ============================================================
# Extension sets
# ============================================================

ANDROID_EXTS = {'.kt', '.gradle', '.kts'}
IOS_EXTS = {'.swift', '.m', '.h', '.xib', '.storyboard'}
JS_TS_EXTS = {'.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs', '.vue'}
STYLE_EXTS = {'.css', '.scss', '.sass', '.less'}

ALL_FRONTEND_EXTS = ANDROID_EXTS | IOS_EXTS | JS_TS_EXTS | STYLE_EXTS


# ============================================================
# Platform detection
# ============================================================

def detect_platform(file_list: List[str]) -> str:
    """
    Detect the primary frontend platform from a list of changed files.
    Returns one of: 'android', 'ios', 'react_native', 'nextjs', 'react', 'backend'
    """
    has_kotlin = any(f.endswith(('.kt', '.kts')) for f in file_list)
    has_swift = any(f.endswith('.swift') for f in file_list)
    has_js_ts = any(os.path.splitext(f)[1] in JS_TS_EXTS for f in file_list)

    if has_kotlin and not has_swift and not has_js_ts:
        return 'android'
    if has_swift and not has_kotlin and not has_js_ts:
        return 'ios'
    if has_js_ts:
        # Next.js: pages/ or app/ directory pattern
        if any(
            '/pages/' in f or f.startswith('pages/')
            or '/app/' in f or f.startswith('app/')
            for f in file_list
        ):
            return 'nextjs'
        # React Native: android/ or ios/ subdirectory, or .native. files
        if any(
            '/android/' in f.lower() or '/ios/' in f.lower() or '.native.' in f
            for f in file_list
        ):
            return 'react_native'
        return 'react'
    return 'backend'


def is_frontend_file(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    return ext in ALL_FRONTEND_EXTS


# ============================================================
# JS / TS context
# ============================================================

# Matches: import X from './path', import { X } from '../path', import type { X } from './x'
JS_IMPORT_RE = re.compile(
    r'(?:import\s+(?:type\s+)?(?:\{[^}]+\}|[\w*]+(?:\s+as\s+\w+)?)\s+from\s+|'
    r'import\s+[\'"])([./][^\'"]+)[\'"]',
    re.MULTILINE,
)

# require() calls
JS_REQUIRE_RE = re.compile(r'require\s*\(\s*[\'"]([./][^\'"]+)[\'"]\s*\)')


def resolve_js_import(import_path: str, current_file: str, repo_path: str) -> Optional[str]:
    """Resolve a relative JS/TS import path to an absolute filesystem path."""
    if not import_path.startswith('.'):
        return None  # Skip node_modules / absolute imports

    current_dir = os.path.dirname(os.path.join(repo_path, current_file))
    resolved_base = os.path.normpath(os.path.join(current_dir, import_path))

    if os.path.isfile(resolved_base):
        return resolved_base

    for ext in ('.ts', '.tsx', '.js', '.jsx', '.mjs', '.d.ts'):
        candidate = resolved_base + ext
        if os.path.isfile(candidate):
            return candidate

    for ext in ('.ts', '.tsx', '.js', '.jsx'):
        candidate = os.path.join(resolved_base, 'index' + ext)
        if os.path.isfile(candidate):
            return candidate

    return None


def find_js_imports(abs_path: str, repo_path: str) -> List[str]:
    """Extract all relative imports from a JS/TS file and resolve them."""
    resolved = []
    try:
        code = open(abs_path, 'r', encoding='utf-8', errors='ignore').read()
        rel = os.path.relpath(abs_path, repo_path)
        for match in JS_IMPORT_RE.finditer(code):
            path = resolve_js_import(match.group(1), rel, repo_path)
            if path:
                resolved.append(path)
        for match in JS_REQUIRE_RE.finditer(code):
            path = resolve_js_import(match.group(1), rel, repo_path)
            if path:
                resolved.append(path)
    except Exception as e:
        logger.warning(f"Could not read {abs_path}: {e}")
    return list(set(resolved))


def find_js_reverse_deps(
    repo_path: str, target_file: str, include_tests: bool = False, limit: int = 5
) -> List[str]:
    """Find JS/TS files that import the given target file."""
    results = []
    skip_dirs = {'node_modules', '.git', 'dist', 'build', '.next', '.expo', '__pycache__'}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fname in files:
            if os.path.splitext(fname)[1] not in JS_TS_EXTS:
                continue
            if not include_tests and re.search(r'\.(test|spec)\.(ts|tsx|js|jsx)$', fname):
                continue
            fpath = os.path.join(root, fname)
            if fpath == target_file:
                continue
            try:
                code = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                rel = os.path.relpath(fpath, repo_path)
                for match in JS_IMPORT_RE.finditer(code):
                    resolved = resolve_js_import(match.group(1), rel, repo_path)
                    if resolved and os.path.abspath(resolved) == os.path.abspath(target_file):
                        results.append(fpath)
                        break
            except Exception:
                pass
            if len(results) >= limit:
                return results
    return results


def extract_ts_exported_types(file_path: str) -> str:
    """Extract exported type/interface/enum definitions from a TS file."""
    try:
        code = open(file_path, 'r', encoding='utf-8', errors='ignore').read()
        blocks = []
        for match in re.finditer(
            r'export\s+(?:type\s+\w+\s*[=<{]|interface\s+\w+[\s{<]|enum\s+\w+\s*{)', code
        ):
            start = match.start()
            depth, i, found_brace = 0, match.end(), False
            while i < len(code):
                if code[i] == '{':
                    depth += 1
                    found_brace = True
                elif code[i] == '}':
                    depth -= 1
                    if found_brace and depth == 0:
                        blocks.append(code[start:i + 1])
                        break
                elif code[i] == ';' and not found_brace:
                    blocks.append(code[start:i + 1])
                    break
                i += 1
        return "\n\n".join(blocks)
    except Exception:
        return ""


def build_js_ts_context(
    repo_path: str, target_files: List[str], seen: Set[str], output_chunks: List[str]
):
    """Build context for React / React Native / Next.js files."""
    for rel_path in target_files:
        abs_path = os.path.join(repo_path, rel_path)
        if not os.path.exists(abs_path):
            logger.warning(f"⚠️ Skipping missing file: {rel_path}")
            continue

        logger.info(f"🔍 Analyzing JS/TS: {rel_path}")

        # Direct imports
        for imp_path in find_js_imports(abs_path, repo_path):
            if imp_path in seen:
                continue
            seen.add(imp_path)
            rel = os.path.relpath(imp_path, repo_path)
            try:
                full = open(imp_path, 'r', encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            # For large TS files prefer types-only to save tokens
            if imp_path.endswith(('.ts', '.tsx')) and len(full) > 3000:
                types_only = extract_ts_exported_types(imp_path)
                content = types_only if types_only else full[:3000] + "\n... (truncated)"
            elif len(full.splitlines()) > 120:
                content = "\n".join(full.splitlines()[:120]) + "\n... (truncated)"
            else:
                content = full
            output_chunks.append(f"=== IMPORT ===\n# {rel}\n\n{content}\n\n")

        # Reverse dependencies (who uses this component/hook)
        for rdep in find_js_reverse_deps(repo_path, abs_path, limit=5):
            if rdep in seen:
                continue
            seen.add(rdep)
            rel = os.path.relpath(rdep, repo_path)
            try:
                lines = open(rdep, 'r', encoding='utf-8', errors='ignore').readlines()
                content = "".join(lines[:100]) + ("... (truncated)" if len(lines) > 100 else "")
                output_chunks.append(f"=== USED BY ===\n# {rel}\n\n{content}\n\n")
            except Exception:
                pass


# ============================================================
# Kotlin / Android context
# ============================================================

KOTLIN_IMPORT_RE = re.compile(r'^\s*import\s+([\w.]+(?:\.\*)?)\s*$', re.MULTILINE)
KOTLIN_CLASS_RE = re.compile(
    r'(?:data\s+class|sealed\s+class|abstract\s+class|open\s+class|class|object|interface)\s+'
    r'([A-Za-z_][A-Za-z0-9_]*)'
)
ANDROID_SYSTEM_PREFIXES = (
    'android.', 'androidx.', 'kotlin.', 'java.', 'javax.', 'com.google.',
    'kotlinx.', 'org.jetbrains.',
)


def find_kotlin_file_for_class(class_name: str, repo_path: str) -> Optional[str]:
    skip_dirs = {'.git', 'build', '.gradle', 'test', 'androidTest'}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f == f"{class_name}.kt":
                return os.path.join(root, f)
    return None


def find_android_xml_layout(repo_path: str, class_name: str) -> Optional[str]:
    """Find the XML layout file for an Activity or Fragment."""
    # CamelCase → snake_case, strip suffix
    snake = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
    for suffix in ('_activity', '_fragment', 'activity', 'fragment'):
        snake = snake.replace(suffix, '')
    snake = snake.strip('_')

    candidates = [f"activity_{snake}.xml", f"fragment_{snake}.xml", f"{snake}.xml"]
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', 'build'}]
        if os.path.basename(root) == 'layout':
            for f in files:
                if f in candidates:
                    return os.path.join(root, f)
    return None


def find_kotlin_reverse_deps(repo_path: str, class_name: str, limit: int = 8) -> List[str]:
    skip_dirs = {'.git', 'build', '.gradle'}
    results = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if not f.endswith('.kt'):
                continue
            fpath = os.path.join(root, f)
            try:
                if re.search(rf'\b{re.escape(class_name)}\b',
                             open(fpath, 'r', encoding='utf-8', errors='ignore').read()):
                    results.append(fpath)
            except Exception:
                pass
            if len(results) >= limit:
                return results
    return results


def build_android_kotlin_context(
    repo_path: str, target_files: List[str], seen: Set[str], output_chunks: List[str]
):
    """Build context for Android/Kotlin files."""
    for rel_path in target_files:
        if not rel_path.endswith('.kt'):
            continue
        abs_path = os.path.join(repo_path, rel_path)
        if not os.path.exists(abs_path):
            continue

        logger.info(f"🤖 Analyzing Kotlin: {rel_path}")
        try:
            code = open(abs_path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue

        cls_match = KOTLIN_CLASS_RE.search(code)
        class_name = cls_match.group(1) if cls_match else None

        # Resolve project-internal imports
        for imp in KOTLIN_IMPORT_RE.findall(code):
            if any(imp.startswith(p) for p in ANDROID_SYSTEM_PREFIXES):
                continue
            leaf = imp.split('.')[-1]
            if leaf == '*':
                continue
            kf = find_kotlin_file_for_class(leaf, repo_path)
            if kf and kf not in seen:
                seen.add(kf)
                try:
                    src = open(kf, 'r', encoding='utf-8', errors='ignore').read()
                    lines = src.splitlines()
                    content = "\n".join(lines[:100]) + ("\n... (truncated)" if len(lines) > 100 else "")
                    output_chunks.append(
                        f"=== KOTLIN IMPORT {imp} ===\n# {os.path.relpath(kf, repo_path)}\n\n{content}\n\n"
                    )
                except Exception:
                    pass

        # XML layout for Activity / Fragment
        if class_name and ('Activity' in class_name or 'Fragment' in class_name):
            layout = find_android_xml_layout(repo_path, class_name)
            if layout and layout not in seen:
                seen.add(layout)
                try:
                    xml = open(layout, 'r', encoding='utf-8', errors='ignore').read()
                    output_chunks.append(
                        f"=== XML LAYOUT ===\n# {os.path.relpath(layout, repo_path)}\n\n{xml}\n\n"
                    )
                except Exception:
                    pass

        # Reverse dependencies
        if class_name:
            for rdep in find_kotlin_reverse_deps(repo_path, class_name):
                if rdep not in seen and rdep != abs_path:
                    seen.add(rdep)
                    try:
                        src = open(rdep, 'r', encoding='utf-8', errors='ignore').read()
                        lines = src.splitlines()
                        content = "\n".join(lines[:80]) + ("\n... (truncated)" if len(lines) > 80 else "")
                        output_chunks.append(
                            f"=== USED BY ===\n# {os.path.relpath(rdep, repo_path)}\n\n{content}\n\n"
                        )
                    except Exception:
                        pass


# ============================================================
# Swift / iOS context
# ============================================================

SWIFT_CLASS_RE = re.compile(
    r'(?:class|struct|protocol|enum|actor)\s+([A-Za-z_][A-Za-z0-9_]*)'
)
SWIFT_CONFORMANCE_RE = re.compile(
    r'(?:class|struct|actor)\s+\w+\s*(?:<[^>]*>)?\s*:\s*([A-Za-z_][A-Za-z0-9_,\s<>]*?)\s*\{'
)
SWIFT_SYSTEM_TYPES = {
    'NSObject', 'UIViewController', 'UIView', 'UITableViewController',
    'UICollectionViewController', 'Equatable', 'Hashable', 'Codable', 'Encodable',
    'Decodable', 'Identifiable', 'ObservableObject', 'View', 'AnyObject',
    'CustomStringConvertible', 'Error', 'RawRepresentable',
}


def find_swift_file_for_type(type_name: str, repo_path: str) -> Optional[str]:
    skip_dirs = {'.git', 'build', 'Pods', 'Carthage', 'DerivedData', '.build'}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f == f"{type_name}.swift":
                return os.path.join(root, f)
    return None


def find_swift_protocol_files(repo_path: str, protocol_names: List[str]) -> Dict[str, str]:
    skip_dirs = {'.git', 'build', 'Pods', 'Carthage', 'DerivedData', '.build'}
    found: Dict[str, str] = {}
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if not f.endswith('.swift'):
                continue
            fpath = os.path.join(root, f)
            try:
                code = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
                for pname in protocol_names:
                    if pname not in found and re.search(rf'\bprotocol\s+{re.escape(pname)}\b', code):
                        found[pname] = fpath
            except Exception:
                pass
    return found


def find_swift_reverse_deps(repo_path: str, type_name: str, limit: int = 8) -> List[str]:
    skip_dirs = {'.git', 'build', 'Pods', 'Carthage', 'DerivedData', '.build'}
    results = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if not f.endswith('.swift'):
                continue
            fpath = os.path.join(root, f)
            try:
                if re.search(rf'\b{re.escape(type_name)}\b',
                             open(fpath, 'r', encoding='utf-8', errors='ignore').read()):
                    results.append(fpath)
            except Exception:
                pass
            if len(results) >= limit:
                return results
    return results


def build_ios_swift_context(
    repo_path: str, target_files: List[str], seen: Set[str], output_chunks: List[str]
):
    """Build context for iOS/Swift files."""
    for rel_path in target_files:
        if not rel_path.endswith('.swift'):
            continue
        abs_path = os.path.join(repo_path, rel_path)
        if not os.path.exists(abs_path):
            continue

        logger.info(f"🍎 Analyzing Swift: {rel_path}")
        try:
            code = open(abs_path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue

        cls_match = SWIFT_CLASS_RE.search(code)
        type_name = cls_match.group(1) if cls_match else None

        # Protocol conformances — find definitions
        conformance_match = SWIFT_CONFORMANCE_RE.search(code)
        if conformance_match:
            raw = conformance_match.group(1)
            protocols = [p.strip() for p in re.split(r'[,\s]+', raw) if p.strip()]
            user_protocols = [
                p for p in protocols
                if p and p not in SWIFT_SYSTEM_TYPES and re.match(r'^[A-Z]', p)
            ]
            proto_files = find_swift_protocol_files(repo_path, user_protocols)
            for pname, pfile in proto_files.items():
                if pfile not in seen:
                    seen.add(pfile)
                    try:
                        src = open(pfile, 'r', encoding='utf-8', errors='ignore').read()
                        output_chunks.append(
                            f"=== PROTOCOL {pname} ===\n# {os.path.relpath(pfile, repo_path)}\n\n{src}\n\n"
                        )
                    except Exception:
                        pass

        # Reverse dependencies
        if type_name:
            for rdep in find_swift_reverse_deps(repo_path, type_name):
                if rdep not in seen and rdep != abs_path:
                    seen.add(rdep)
                    try:
                        src = open(rdep, 'r', encoding='utf-8', errors='ignore').read()
                        lines = src.splitlines()
                        content = "\n".join(lines[:80]) + ("\n... (truncated)" if len(lines) > 80 else "")
                        output_chunks.append(
                            f"=== USED BY ===\n# {os.path.relpath(rdep, repo_path)}\n\n{content}\n\n"
                        )
                    except Exception:
                        pass


# ============================================================
# Public API
# ============================================================

def generate_frontend_context(
    repo: str,
    files: List[str],
    platform: str,
    output: str = "/tmp/frontend_context.txt",
    return_string: bool = True,
) -> str:
    """
    Generate context for a frontend PR.

    Args:
        repo:          Local repository path
        files:         Changed file paths relative to repo root
        platform:      One of 'android', 'ios', 'react', 'react_native', 'nextjs'
        output:        Path to write context file (used when return_string=False)
        return_string: If True, return context as string instead of writing to file
    """
    seen: Set[str] = set()
    output_chunks: List[str] = []

    if platform == 'android':
        build_android_kotlin_context(repo, files, seen, output_chunks)
    elif platform == 'ios':
        build_ios_swift_context(repo, files, seen, output_chunks)
    else:  # react, react_native, nextjs
        build_js_ts_context(repo, files, seen, output_chunks)

    context_text = (
        f"# Frontend Context — Platform: {platform}\n"
        f"# Repo: {repo}\n"
        f"# Files: {', '.join(files)}\n\n"
        + "".join(output_chunks)
    )

    if not return_string:
        os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write(context_text)
        logger.info(f"✅ Frontend context saved to {output} ({len(seen)} unique files)")

    logger.info(f"✅ Generated frontend context in memory ({len(seen)} unique files, platform: {platform})")
    return context_text
