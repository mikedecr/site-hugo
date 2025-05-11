import os
from pathlib import Path
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


def pixi_run(
    cmd: List[str],
    manifest_path: Path | str = Path("./pixi.toml"),
    capture_output: bool = True
):
    manifest_path = Path(manifest_path).resolve()
    cmd = [
        "pixi", "run",
        "--manifest-path", str(manifest_path),
        *cmd
    ]
    log.info("pixi_run: " + " ".join(map(str, cmd)))
    return run(cmd, capture_output=capture_output)


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


