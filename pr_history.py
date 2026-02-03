import os

HISTORY_DIR = "/home/ubuntu/pr_history"
os.makedirs(HISTORY_DIR, exist_ok=True)


def history_path(workspace: str, repo: str, pr_id: int) -> str:
    return os.path.join(
        HISTORY_DIR,
        f"{workspace}_{repo}_PR_{pr_id}.txt"
    )


def load_latest_commit(workspace: str, repo: str, pr_id: int) -> str:
    """
    Returns the last stored commit hash for this PR.
    If file doesn't exist, returns None.
    """
    path = history_path(workspace, repo, pr_id)
    if not os.path.isfile(path):
        return None

    try:
        with open(path, "r") as f:
            return f.read().strip() or None
    except:
        return None


def save_latest_commit(workspace: str, repo: str, pr_id: int, payload: dict):
    """
    Stores ONLY the latest commit hash from PR payload.
    Overwrites the file each time.
    """
    latest = payload["pullrequest"]["source"]["commit"]["hash"]
    path = history_path(workspace, repo, pr_id)

    with open(path, "w") as f:
        f.write(latest)

