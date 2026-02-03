def should_process_pr(payload):
    print(payload)
    """
    Returns (True, reason) if the PR should be processed,
    or (False, reason) if it should be skipped.
    """

    pr = payload.get("pullrequest", {})
    pr_id = pr.get("id")
    title = pr.get("title", "").lower()
    author = pr.get("author", {}).get("nickname", "")
    source_branch = pr.get("source", {}).get("branch", {}).get("name", "")
    destination_branch = pr.get("destination", {}).get("branch", {}).get("name", "")

    # ---------------------------------------
    # 1. Skip PRs with certain keywords
    # ---------------------------------------
    skip_keywords = ["wip", "draft", "auto-merge", "no-review"]
    if any(k in title for k in skip_keywords):
        return False, "title contains skip keyword"

    # ---------------------------------------
    # 2. Skip PRs created by bots
    # ---------------------------------------
    bot_authors = ["bitbucket-pipelines", "automation-bot", "dependabot"]
    if author.lower() in bot_authors:
        return False, "authored by bot"

    # ---------------------------------------
    # 3. Skip if source == destination (should never happen)
    # ---------------------------------------
    if source_branch == destination_branch:
        return False, "same branch PR"

    # ---------------------------------------
    # 4. Only review PRs targeting certain branches
    # ---------------------------------------
    allowed_targets = ["develop", "master", "main", "release"]
    if destination_branch.lower() not in allowed_targets:
        return False, f"destination branch '{destination_branch}' not in allowed list"

    # ---------------------------------------
    # 5. Only process PRs touching code (not docs, YAML, markdown etc.)
    # ---------------------------------------
    try:
        changed = pr["links"]["diffstat"]["href"]
    except:
        pass  # fallback will check diff in background

    # OPTIONAL: If you want to skip small PRs:
    if "skip-review" in title:
        return False, "manual skip flag"

    # ---------------------------------------
    # Accept PR for automatic review
    # ---------------------------------------
    return False, "eligible for processing"

