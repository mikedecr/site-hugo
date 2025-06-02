from typer import Option
from ..app import app
from .post_git_log import post_git_log
from .git_log import GitLog

from datetime import date as Date, timedelta


yesterday = Date.today() - timedelta(days=1)


@app.command()
def post_daily_update(dry_run: bool = Option(True), n: int = Option(None)):
    gl = GitLog(date = yesterday , n = n)
    post_git_log(repo_name="mikedecr.computer", gitlog=gl, dry_run=dry_run)
