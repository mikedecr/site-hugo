from typing import Optional
from datetime import date as Date

from .bsky_session import session as bsky_session
from bsky_bridge import post_text as bsky_post_text
from .git_log import GitLog


def date_post_text(repo_name: str, gitlog: GitLog):
    log_data: list[dict[str, str]] = gitlog.messages()
    if not log_data:
        return
    header = ''.join([
        f"Commits to {repo_name}",
        f", {gitlog.date}" if gitlog.date else '',
        ":"
    ])
    commits = [
        f"- {commit['hash']}: {commit['message']}" for commit in log_data
    ]
    return '\n'.join([header, *commits])


def post_git_log(repo_name: str, gitlog: GitLog):
    text: str = date_post_text(repo_name=repo_name, gitlog=gitlog)
    return bsky_post_text(session=bsky_session, text=text)
