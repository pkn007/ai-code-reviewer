#!/usr/bin/env python3
import os
import subprocess
import requests
from dotenv import load_dotenv

# --------------------------------------------------------
# CONFIGURATION (EDIT THESE VALUES ONLY)
# --------------------------------------------------------

SOURCE_WORKSPACE = "merabolabs"
SOURCE_REPO = "cart-service-coderabbit"

DEST_WORKSPACE = "hackathon-test"
DEST_REPO = "cart-service-hackathon"

# --------------------------------------------------------
# LOAD CREDS FROM .env
# --------------------------------------------------------
load_dotenv()

BB_USER = os.getenv("BITBUCKET_GIT_USERNAME")
BB_APP_PASS = os.getenv("BITBUCKET_GIT_APP_PASSWORD")

if not BB_USER or not BB_APP_PASS:
    print("❌ Missing Bitbucket credentials in .env")
    exit(1)

API_BASE = "https://api.bitbucket.org/2.0/repositories"


# --------------------------------------------------------
# UTILS
# --------------------------------------------------------
def run(cmd, cwd=None):
    """Run shell command and stream output live."""
    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    for line in process.stdout:
        print(line, end="")  # stream live output to console

    process.wait()
    if process.returncode != 0:
        print(f"❌ Command failed: {' '.join(cmd)}")
        exit(1)


def repo_exists(workspace, repo_slug):
    url = f"{API_BASE}/{workspace}/{repo_slug}"
    resp = requests.get(url, auth=(BB_USER, BB_APP_PASS))
    return resp.status_code == 200


def create_repo(workspace, repo_slug):
    print(f"📦 Creating repository → {workspace}/{repo_slug}")
    url = f"{API_BASE}/{workspace}/{repo_slug}"
    payload = {
        "scm": "git",
        "is_private": True,
        "name":  "cart-service-hackathon",
        "project":{"key": "HAC"}
    }
    resp = requests.post(url, json=payload, auth=(BB_USER, BB_APP_PASS))

    if resp.status_code not in (200, 201):
        print("❌ Failed to create repo:", resp.text)
        exit(1)

    print("✅ Repository created")


def clone_repo(source_ws, source_repo):
    clone_url = f"https://{BB_USER}:{BB_APP_PASS}@bitbucket.org/{source_ws}/{source_repo}.git"
    local_path = f"/tmp/{source_repo}"

    # Clean old clone if exists
    run(["rm", "-rf", local_path])

    print(f"📥 Cloning {source_ws}/{source_repo} ...")
    run(["git", "clone", "--mirror", clone_url, local_path])

    print("✅ Clone completed")
    return local_path


def push_repo(local_repo_path, dest_ws, dest_repo):
    push_url = f"https://{BB_USER}:{BB_APP_PASS}@bitbucket.org/{dest_ws}/{dest_repo}.git"

    print(f"🚀 Pushing to {dest_ws}/{dest_repo} ...")
    run(["git", "push", "--mirror", push_url], cwd=local_repo_path)
    print("🎉 Migration completed successfully!")


# --------------------------------------------------------
# MAIN LOGIC (NO ARGS, JUST VARIABLES ABOVE)
# --------------------------------------------------------
def main():
    print("===============================================")
    print(f"🔁 Migrating\n  {SOURCE_WORKSPACE}/{SOURCE_REPO}\n   → {DEST_WORKSPACE}/{DEST_REPO}")
    print("===============================================")

    # 1. Clone source repository
    local_repo = clone_repo(SOURCE_WORKSPACE, SOURCE_REPO)

    # 2. Create destination repo if missing
    if repo_exists(DEST_WORKSPACE, DEST_REPO):
        print("⚠️ Destination repo already exists — skipping creation")
    else:
        create_repo(DEST_WORKSPACE, DEST_REPO)

    # 3. Mirror push repo to destination
    push_repo(local_repo, DEST_WORKSPACE, DEST_REPO)


if __name__ == "__main__":
    main()

