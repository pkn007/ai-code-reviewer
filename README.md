# AI Code Reviewer (Bitbucket PR Webhook + Claude)

This repo contains a small FastAPI service that listens to Bitbucket pull request webhooks, fetches the PR diff (full or incremental), optionally generates **extra Java context** from a local clone of the repo, asks **Claude** to produce **Bitbucket inline review comments** in a strict JSON format, and then posts those comments back to the PR.

It’s designed to run as a long-lived service (e.g. on an Ubuntu VM) and to be triggered by Bitbucket Cloud webhooks.

## What it does (end-to-end)

- **Bitbucket webhook hits** `POST /prupdate` when a PR is created/updated.
- Service checks the PR targets `master`/`main` (see `server.py`).
- Service **syncs a local clone** of the repo under `/home/ubuntu/repo/<repo>` and generates:
  - **incremental diff** between last processed commit and the new commit, or
  - **full PR diff** on first run.
- Service extracts changed files from the diff and filters down to “code-like” files (extensions allowlist + skiplist).
- If there are **Java files with meaningful changes**, it generates a **context bundle** (imports + reverse deps + configs) and includes it in the LLM prompt.
- Service calls **Anthropic Claude** and expects **one-or-more standalone JSON objects** (not an array) describing inline comments.
- Service posts those JSON objects to Bitbucket PR comments API.
- When the PR is merged, `POST /prmerge` re-clones the repo (clean local state).

## Requirements

- Python 3.11+ recommended
- A Bitbucket Cloud OAuth app (client id/secret + refresh token) **or** equivalent tokens as used here
- Bitbucket Git username + app password (used for cloning repos over HTTPS)
- Anthropic API key

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

`server.py` will **raise on startup** if any of these are missing:

- **`BITBUCKET_CLIENT_ID`**: Bitbucket OAuth client id
- **`BITBUCKET_CLIENT_SECRET`**: Bitbucket OAuth client secret
- **`BITBUCKET_REFRESH_TOKEN`**: refresh token used to obtain access tokens
- **`BITBUCKET_GIT_USERNAME`**: Bitbucket username for cloning via HTTPS
- **`BITBUCKET_GIT_APP_PASSWORD`**: Bitbucket app password for cloning via HTTPS
- **`CLAUDE_API_KEY`**: Anthropic API key

Typically you’ll provide them via a `.env` file (loaded by `python-dotenv`).

## Run locally

`server.py` includes an `__main__` that runs uvicorn on port 8080:

```bash
python server.py
```

Health check:

```bash
curl http://localhost:8080/health
```

## Webhook endpoints

- **`POST /prupdate`**: Handles PR create/update/reopen events and posts review comments.
- **`POST /prmerge`**: Handles PR merged events and re-clones the repo.
- **`GET /health`**: Liveness check.

### Event filtering behavior

In `server.py`:

- Only handles `pullrequest:created`, `pullrequest:updated`, `pullrequest:reopened`.
- Skips PRs not targeting `master` or `main`.

## File-by-file explanation

### `server.py`

Main FastAPI service and orchestrator.

- **Startup**: loads `.env`, validates required env vars, configures logging to `webhook.log`.
- **Bitbucket OAuth**: `get_bitbucket_access_token()` refreshes tokens when expired.
- **Local repo sync**: `update_local_repo()` clones or fetch+resets a local mirror at `/home/ubuntu/repo/<repo>`.
- **Diff strategy**:
  - If a PR was processed before, uses `git diff <old>..<new>` from the local clone (incremental).
  - Otherwise fetches the full PR diff via Bitbucket API.
  - Stores/loads last processed commit via `pr_history.py`.
- **Changed-file filtering**:
  - Extracts changed paths using `diff.extract_changed_files_from_diff()`.
  - Keeps only files matching `CODE_EXTENSIONS` and not matching `SKIP_EXTENSIONS`.
  - Applies a minimum-change threshold:
    - Java uses comment-aware counting (`extract_java_files_with_min_changes`)
    - Other languages use simple add/delete non-empty line counting (`extract_files_with_min_changes`)
- **Context generation (Java only)**:
  - Calls `context.generate_java_context()` for Java files that pass the threshold.
  - Includes the generated context text in the LLM prompt.
- **LLM prompt**:
  - Loads additional formatting constraints from `prompt_rules.txt`.
  - Writes the full prompt to `/home/ubuntu/raw_prompt.txt` and the trimmed prompt to `/home/ubuntu/trimmed_prompt.txt`.
  - Uses `trim_prompt_to_token_limit()` to keep the prompt under a token cap.
- **Claude call + parsing**:
  - Calls Anthropic and expects output containing one or more JSON objects.
  - Parses JSON objects out of the raw text via `parse_json_objects()`.
- **Posting comments**:
  - Posts each parsed object to Bitbucket’s PR comments API.
- **Merge webhook**:
  - Deletes the local clone directory and re-clones the repo on PR merge (`/prmerge`).

### `context.py`

Java context generator used to give Claude more surrounding code (beyond the diff).

Key features:

- **Import resolution**: parses Java `import ...;` lines and tries to map them to files under `src/main/java`.
- **Type extraction**: extracts a whole `class/interface/enum/record` definition (balances braces) to avoid dumping entire files.
- **Reverse dependency search**: finds Java files that reference a target type via patterns (imports, `implements`, `extends`, construction, field usage, etc.).
- **Spring-ish config search**: scans for `@Configuration`, `@Bean`, and `@Qualifier` patterns referencing the target class name.
- **Public entrypoint**: `generate_java_context(...)` can work from a local repo path (`repo=...`) or clone a remote repo URL (`repo_url=...`).
- **Output**: returns a single context string (default) or writes `context_full.txt`-style output.

### `diff.py`

Bitbucket diff fetching helpers + diff parsing utilities.

- **`fetch_incremental_or_full_diff(...)`**: fetches either full PR diff or incremental diff, falling back to full diff if incremental fails.
- **`extract_changed_files_from_diff(diff_text)`**: extracts file paths from `diff --git a/... b/...` headers.
- **Per-file diff splitting**: `split_diff_by_file()` groups diff lines by destination path.
- **Change counting**:
  - Java-only: `count_non_comment_java_changes()` ignores `//`, `/* */`, and Javadoc-style `*` lines.
  - Generic: `count_changes_for_file()` counts non-empty added/removed lines.
- **Threshold filters**:
  - `extract_java_files_with_min_changes(...)`
  - `extract_files_with_min_changes(...)`

### `pr_history.py`

Stores the “last processed” commit hash for each PR so `server.py` can compute incremental diffs.

- Writes to `HISTORY_DIR = "/home/ubuntu/pr_history"`.
- **`load_latest_commit(workspace, repo, pr_id)`** returns the stored hash (or `None`).
- **`save_latest_commit(workspace, repo, pr_id, payload)`** overwrites the file with the latest source commit hash from the webhook payload.

### `webhooks.py`

One-off CLI helper to **create Bitbucket webhooks** for a given repository URL.

- Reads `BITBUCKET_CLIENT_ID`, `BITBUCKET_CLIENT_SECRET`, `BITBUCKET_REFRESH_TOKEN` from `.env`.
- Creates (if missing) two webhooks pointing at:
  - `/prupdate` for PR create/update
  - `/prmerge` for PR merged

Usage (as written in the file):

```bash
python webhooks.py https://bitbucket.org/<workspace>/<repo-slug>
```

### `clone_repos.py`

Utility script to “mirror migrate” a Bitbucket repository from one workspace/repo to another.

- Clones the source repo with `git clone --mirror`
- Optionally creates the destination repo via Bitbucket REST API if it doesn’t exist
- Pushes all refs with `git push --mirror`

This is not used by the webhook server at runtime; it’s an admin/helper script.

### `difftest.py`

Standalone script used to manually test Bitbucket diff fetching logic.

- Refreshes OAuth token
- Fetches full or incremental diff
- Prints diff stats and extracted changed files

Not used by `server.py` in production flow.

### `filter.py`

Contains `should_process_pr(payload)` intended to decide whether a PR should be processed.

Notes:

- Implements keyword/bot/branch filters.
- As currently written, it returns `False, "eligible for processing"` at the end, which effectively **skips everything** if used as-is.
- This function is not currently wired into `server.py`.

### `prompt_rules.txt`

Additional prompt constraints injected into the Claude prompt, mainly enforcing output format:

- output must be **only** standalone JSON objects
- no markdown/prose outside JSON objects
- no arrays, no extra fields, no trailing commas
- only emit comments when useful, etc.

### `raw_prompt.txt` and `trimmed_prompt.txt`

Sample prompt artifacts committed to the repo (and also paths that `server.py` writes to under `/home/ubuntu/` at runtime).

- `server.py` builds a large prompt containing:
  - a role/instruction header
  - `prompt_rules.txt`
  - the PR diff
  - optionally the generated Java context text
- `trim_prompt_to_token_limit()` ensures the prompt stays under an input token cap by truncating from the end.

### `requirements.txt`

Pinned Python dependencies used by the service:

- FastAPI + uvicorn runtime
- httpx / requests for Bitbucket API calls
- anthropic SDK for Claude
- python-dotenv for `.env` loading

## Logs and runtime files

The service writes/uses several runtime paths (configured directly in code):

- **`webhook.log`**: service logs (in current working directory)
- **`/home/ubuntu/repo/<repo>`**: local clones used to compute diffs and context
- **`/home/ubuntu/diff/diff_PR_<id>.patch`**: stored diffs
- **`/home/ubuntu/context/context_PR_<id>.txt`**: stored Java context (when generated)
- **`/home/ubuntu/claude/claude_PR_<id>.txt`**: stored Claude output
- **`/home/ubuntu/pr_history/...`**: last processed commit per PR

If you run locally on macOS, you’ll likely want to adjust these absolute paths to something writable (or mount them if running in a container).

## Quick “smoke test” checklist

- `GET /health` returns `{"status":"ok"}`.
- You can receive a Bitbucket webhook event payload at `POST /prupdate` (from Bitbucket webhook tester).
- Service can refresh OAuth token and fetch diffs.
- Claude output parses into JSON objects and posts to Bitbucket comments API.

