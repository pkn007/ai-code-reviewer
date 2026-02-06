#!/usr/bin/env python3
import os
import sys
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# ------------------------------------------------------
# LOAD ENV VARIABLES
# ------------------------------------------------------
load_dotenv()

CLIENT_ID = os.getenv("BITBUCKET_CLIENT_ID")
CLIENT_SECRET = os.getenv("BITBUCKET_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("BITBUCKET_REFRESH_TOKEN")

if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
    print("❌ Missing Bitbucket OAuth variables in .env")
    sys.exit(1)

# ------------------------------------------------------
# READ INPUT ARGUMENTS
# ------------------------------------------------------
if len(sys.argv) < 2:
    print("❌ Usage: python setup_hooks.py <repo_url>")
    print("Example:")
    print("  python setup_hooks.py https://bitbucket.org/ws/cart-service")
    sys.exit(1)

REPO_URL = sys.argv[1]
WEBHOOK_BASE = "https://codereviewer.dealshare.in"
# ------------------------------------------------------
# PARSE REPO URL → workspace + repo_slug
# ------------------------------------------------------
def parse_repo_url(url):
    """
    Example URL:
    https://bitbucket.org/workspace/repo-slug
    """
    try:
        path = urlparse(url).path.strip("/")  # "workspace/repo"
        workspace, repo = path.split("/")
        return workspace, repo
    except Exception:
        print(f"❌ Invalid repository URL: {url}")
        sys.exit(1)

WORKSPACE, REPO = parse_repo_url(REPO_URL)
print(f"📦 Parsed workspace={WORKSPACE}, repo={REPO}")

# ------------------------------------------------------
# WEBHOOK DEFINITIONS
# ------------------------------------------------------
WEBHOOKS = [
    {
        "description": "AI Code Reviewer/ALB: Created and Updated",
        "url": f"{WEBHOOK_BASE}/prupdate",
        "events": ["pullrequest:created", "pullrequest:updated"]
    },
    {
        "description": "AI Code Reviewer/ALB: Merged",
        "url": f"{WEBHOOK_BASE}/prmerge",
        "events": ["pullrequest:fulfilled"]
    }
]

# ------------------------------------------------------
# STEP 1 → Refresh Access Token
# ------------------------------------------------------
def get_access_token():
    print("🔄 Requesting Access Token...")

    resp = requests.post(
        "https://bitbucket.org/site/oauth2/access_token",
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN},
    )

    if resp.status_code != 200:
        raise Exception(f"❌ Failed to refresh token: {resp.text}")

    print("✅ Access Token Received")
    return resp.json()["access_token"]

# ------------------------------------------------------
# STEP 2 → List Existing Webhooks
# ------------------------------------------------------
def list_webhooks(token):
    url = f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}/{REPO}/hooks"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    if resp.status_code != 200:
        raise Exception(f"❌ Cannot fetch webhooks: {resp.text}")

    return resp.json().get("values", [])

# ------------------------------------------------------
# STEP 3 → Create a Webhook Only If Missing
# ------------------------------------------------------
def ensure_webhook(token, hook_def):
    existing = list_webhooks(token)

    # Check if the same URL already exists
    for hook in existing:
        if hook["url"] == hook_def["url"]:
            print(f"⚠️ Webhook already exists → {hook_def['url']}")
            print("UUID:", hook["uuid"])
            return hook["uuid"]

    print(f"🛠 Creating webhook → {hook_def['url']}")

    payload = {
        "description": hook_def["description"],
        "url": hook_def["url"],
        "events": hook_def["events"],
        "active": True,
    }

    url = f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}/{REPO}/hooks"

    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
    )

    if resp.status_code not in (200, 201):
        raise Exception(f"❌ Failed to create hook: {resp.text}")

    print("✅ Webhook created!")
    print("UUID:", resp.json()["uuid"])
    return resp.json()["uuid"]

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
if __name__ == "__main__":
    token = get_access_token()

    for hook in WEBHOOKS:
        ensure_webhook(token, hook)

    print("\n🎉 All webhooks verified or created successfully!")

