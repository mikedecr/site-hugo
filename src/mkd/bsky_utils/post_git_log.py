from rich import print as rprint
from bsky_bridge import post_text as bsky_post_text

from .bsky_session import session as bsky_session
from .git_log import GitLog

from logging import getLogger
logger = getLogger(__name__)


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
        f"- {commit['message']}" for commit in log_data
    ]
    return '\n'.join([header, *commits])


def post_git_log(repo_name: str, gitlog: GitLog, dry_run=True):
    text: str = date_post_text(repo_name=repo_name, gitlog=gitlog)
    if dry_run:
        logger.info("as dry run:\n---\n%s", text)
        return
    else:
        logger.info("Posting for real:\n%s", text)
        return bsky_post_text(session=bsky_session, text=text)
