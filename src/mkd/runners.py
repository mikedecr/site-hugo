import os
from subprocess import run, CompletedProcess
from typing import List, Optional

from .logging import log


def uv_run(
    cmd: List[str],
    capture_output = True
) -> CompletedProcess:
    cmd = ["uv", "run", *cmd]
    log.info("uv_run: " + " ".join(map(str, cmd)))
    ret = run(cmd, capture_output = capture_output)
    return ret


# for now we still assume there is a (micro)mamba executable
mamba_exe = os.environ["MAMBA_EXE"]


def micromamba_run(
    cmd: List[str],
    prefix: Optional[str] = None,
    capture_output = True
) -> CompletedProcess:
    _umrun_cmd = [mamba_exe, "run"]
    if prefix is not None:
        _umrun_cmd.extend(["-p", prefix])
    cmd = [*_umrun_cmd, *cmd]
    log.info("micromamba run: " + " ".join(map(str, cmd)))
    ret = run(cmd, capture_output = capture_output)
    return ret


