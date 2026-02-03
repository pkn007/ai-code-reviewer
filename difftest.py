#!/usr/bin/env python3
import asyncio
import httpx
import os
import re
from dotenv import load_dotenv

load_dotenv()

BITBUCKET_TOKEN = None

async def get_access_token():
    """Fetch OAuth access token using refresh token."""
    global BITBUCKET_TOKEN

    if BITBUCKET_TOKEN:
        return BITBUCKET_TOKEN

    url = "https://bitbucket.org/site/oauth2/access_token"
    refresh = os.getenv("BITBUCKET_REFRESH_TOKEN")
    cid = os.getenv("BITBUCKET_CLIENT_ID")
    secret = os.getenv("BITBUCKET_CLIENT_SECRET")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data={"grant_type": "refresh_token", "refresh_token": refresh},
            auth=(cid, secret),
        )
        resp.raise_for_status()
        data = resp.json()

    BITBUCKET_TOKEN = data["access_token"]
    return BITBUCKET_TOKEN


async def fetch_incremental_or_full_diff(
    workspace: str,
    repo: str,
    pr_id: int,
    old_head: str | None,
    new_head: str,
    token: str
) -> tuple[str, bool]:

    base = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream",
        "Cache-Control": "no-cache",
    }

    # FIRST RUN → full diff
    if old_head is None:
        url = f"{base}/pullrequests/{pr_id}/diff?topic=true"
        print(f"[TEST] Fetching FULL DIFF → {url}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
        return (resp.text or ""), False

    # INCREMENTAL
    incr_url = f"{base}/diff/{old_head}..{new_head}"

    print(f"[TEST] Fetching INCREMENTAL DIFF → {incr_url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(incr_url, headers=headers)

    # CASE: Incremental fails or empty
    if resp.status_code != 200 or not resp.text.strip():
        print(f"[WARN] Incremental diff empty or failed → status={resp.status_code}")

        fallback = f"{base}/pullrequests/{pr_id}/diff?topic=true"
        print(f"[TEST] Falling back to FULL DIFF → {fallback}")

        async with httpx.AsyncClient() as client:
            resp2 = await client.get(fallback, headers=headers)

        return (resp2.text or ""), False

    return resp.text, True


def extract_changed_files(diff_text: str):
    pattern = re.compile(r"^diff --git a/(.+?) b/", re.MULTILINE)
    files = {match.group(1) for match in pattern.finditer(diff_text)}
    return sorted(files)


async def main():
    # ---- CONFIGURE THIS ----
    workspace = "hackathon-test"       # << UPDATE
    repo = "user-service-hackathon"    # << UPDATE
    pr_id = 1                           # << UPDATE

    # Test commits
    old_head = "da9d7b6ec6869996690d40ec95d2d972cb73e439"
    new_head = "240183e69b3713e6dc865c84719121892bb45348"

    token = await get_access_token()

    diff_text, is_incremental = await fetch_incremental_or_full_diff(
        workspace=workspace,
        repo=repo,
        pr_id=pr_id,
        old_head=old_head,
        new_head=new_head,
        token=token
    )

    print("\n================ DIFF RESULT ================")
    print("Incremental?" , is_incremental)
    print("Diff length:", len(diff_text))

    print("\n---- FIRST 400 chars ----")
    print(diff_text[:400])

    changed_files = extract_changed_files(diff_text)

    print("\n================ CHANGED FILES ================")
    print(changed_files)

    print("==============================================")


if __name__ == "__main__":
    asyncio.run(main())

