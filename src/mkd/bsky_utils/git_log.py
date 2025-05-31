import subprocess

from pydantic import BaseModel
from typing import Optional
from datetime import date as Date, timedelta


class GitLog(BaseModel):
    """
    Job of this class it construct a git log command and return a representation of the data
    """

    n: Optional[int]
    date: Optional[Date]

    def command(self, collapse = False):
        cmd: list[str] = ["git", "log", "--oneline"]
        if self.date:
            start: Date = self.date - timedelta(days=1)
            until: Date = self.date
            cmd += [f"--since='{start}'",
                    f"--until='{until}'"]
        if self.n:
            cmd.append(f"-n {self.n}")
        return ' '.join(cmd) if collapse else cmd

    def messages(self) -> list[dict[str, str]]:
        """
        Intermediate representation of git log data.
        List of records with schema {hash: str, message: str}
        """
        if self.n == 0:
            return []
        cmd = self.command()
        if not cmd:
            return []
        # is there a better way?
        bstr: bytes = subprocess.check_output(cmd)
        if not bstr:
            return []
        msgs: list[str] = bstr.decode("utf-8").strip().split("\n")
        print(msgs)
        # combine results
        res: list[dict] = []
        if not msgs:
            return res
        for line in msgs:
            hash, *words = line.split(" ")
            msg: str = ' '.join(words)
            parsed: dict[str, str] = dict(hash=hash, message=msg)
            res.append(parsed)
        return res


gl = GitLog(date=Date(2025, 5, 29), n = None)
