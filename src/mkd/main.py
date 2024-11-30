import os
from pathlib import Path
from subprocess import run, CompletedProcess
import tomllib
from typing import Any, Dict, List, Optional, Union

from typer import Typer, Option, Context

from ._links import create_links
from ._logging import log

app = Typer(name = "Hugo Site Builder")


@app.callback()
def _callback(context: Context,
              config_file: str = Option("pyproject.toml", "-f", "--file")):
    toml_data: Dict = read_toml(config_file)
    context.obj = toml_data
    return context


def read_toml(file: Union[str, Path]) -> Dict:
    with open(file, "rb") as f:
        data: Dict = tomllib.load(f)
        return data



# for now we still assume there is a (micro)mamba executable
_um = os.environ["MAMBA_EXE"]


def umrun(cmd: List[str], prefix: Optional = None, capture_output = True) -> CompletedProcess:
    assert type(cmd) is list, f"{cmd=} must be a list"
    _umrun_cmd = [_um, "run"]
    if prefix is not None:
        _umrun_cmd.extend(["-p", prefix])
    cmd = [*_umrun_cmd, *cmd]
    log.info("umrun: " + " ".join(map(str, cmd)))
    ret = run(cmd, capture_output = capture_output)
    return ret


def uv_run(cmd: List[str], capture_output = True) -> CompletedProcess:
    cmd = ["uv", "run", *cmd]
    log.info("uv_run: " + " ".join(map(str, cmd)))
    ret = run(cmd, capture_output = capture_output)
    return ret


def find_quarto_render_sources(
        path: Path,
        extensions = [".md", ".qmd"],
        exclude_patterns = ["README.md"]
) -> List[Path]:
    """
    List of all filepaths to render with quarto
    """
    # ugh just in case
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"cannot find {path=}")
    if not path.is_dir():
        if path.suffix in extensions and all(p not in str(path) for p in exclude_patterns):
            return [path]
    else:
        targets = []
        for it in path.iterdir():
            v = find_quarto_render_sources(it, extensions)
            if v is not None:
                targets += v
        return targets


def quarto_render_file(path: Path):
    """
    activate environment if it exists
    - else build it and re-call
    - if no env file, continue
    """
    path = Path(path).resolve()
    if (conda_prefix := resolve_conda_prefix(path)):
        return _micromamba_render(path, conda_prefix)
    else:
        return _uvx_render(path)


def _micromamba_render(path: str, prefix_path: str):
    log.info(" ".join(map(str, ["rendering", path, "in", prefix_path])))
    which_quarto = umrun(["which", "quarto"], prefix=prefix_path, capture_output=True).stdout
    log.info(f"which quarto: {which_quarto}")
    return umrun(["quarto", "render", path], prefix = prefix_path, capture_output=False)


def _uvx_render(path: str):
    return uv_run(["quarto", "render", path], capture_output = False)


def resolve_conda_prefix(path):
    parent = path.parent
    # if env exists, return its path
    root: Path = Path(os.getcwd())
    subpath: Path = parent.relative_to(root)
    prefix_path: Path = root / "build/conda_envs" / subpath
    if prefix_path.exists():
        return prefix_path
    log.warning(f"did not find environment at {prefix_path}")
    # find an env yml, return None if not
    conda_yaml_dir: Path = parent / "conda"
    log.info(f"searching for conda ymls in {conda_yaml_dir}")
    if not conda_yaml_dir.exists():
        log.warning(f"{conda_yaml_dir} doesn't exist")
        return None
    # identify ymls, return None if there aren't any
    conda_yamls: List[Path] = [
        file for file in conda_yaml_dir.iterdir()
        if file.suffix in (".yml", ".yaml")
    ]
    if len(conda_yamls) == 0:
        log.warning(f"No yamls in {conda_yaml_dir}")
        return None
    yml = conda_yamls[0]
    # build first first / only yml
    if len(conda_yamls) > 1:
        log.warning(f"Multiple yamls found: {conda_yamls}. Picking the first one: {yml}.")
        return prefix_path
    log.info(f"found {yml}")
    create_micromamba_env(yml, prefix_path)
    return prefix_path


def create_micromamba_env(env_yml: Path, prefix_path: Path):
    return umrun(
        cmd = [_um, "env", "create", "-f", env_yml, "-p", prefix_path, "-y"],
        capture_output = False
    )


@app.command()
def serve():
    cmd = [
        "hugo",
        "serve",
        "--source", "hugo",
        "--disableFastRender",
        "--buildDrafts",
    ]
    uv_run(cmd, capture_output = False)


DOC_SOURCE_DIR = "Directory where quarto source files are located"


@app.command()
def render_quarto(
    source_dir: str = Option("qmd", "--source-dir", "-s", help=DOC_SOURCE_DIR),
):
    source_path: Path = Path(source_dir).resolve()
    try:
        render_files: List[Path] = find_quarto_render_sources(source_path)
        log.info("Found qmd source files:" +
                 "\n - ".join(map(str, render_files)))
    except FileNotFoundError:
        raise FileNotFoundError(f"{source_path=} does not exist")
    if len(render_files) == 0:
        raise ValueError(f"Found no files to render in {source_path=}")
    return [quarto_render_file(file) for file in render_files]


@app.command()
def build(
        context: Context,
        quarto: bool = Option(True, "--quarto", "-q",
                              help = "Render quarto files in source directory"),
        source_dir: str = Option("qmd", "--source-dir", "-s",
                                 help = DOC_SOURCE_DIR)
):
    """
    - render all qmds
    - serve site
    """
    init(context)
    render_quarto(source_dir)
    serve()


def get_nested_path(data: Dict, *args) -> Any:
    for rg in args:
        data = data[rg]
    return data


def flatten_nested_dict(nested, sep = "_"):
    """
    credit: Matias Thayer, <https://stackoverflow.com/a/64717285>
    """
    stack = list(nested.items())
    ans = {}
    while stack:
        key, val = stack.pop()
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                stack.append((f"{key}{sep}{sub_key}", sub_val))
        else:
            ans[key] = val
    return ans


@app.command()
def init(context: Context):
    # currently just a "symlinks" step
    link(context)


def link(context: Context):
    link_toml: Dict = get_nested_path(context.obj, "mkd", "links")
    link_to_target: Dict = flatten_nested_dict(link_toml, sep = "/")
    log.info("symlink recipe:\n" + str(link_to_target))
    for link_dir, target_dir in link_to_target.items():
        create_links(Path(target_dir), Path(link_dir))


if __name__ == "__main__":
    app()
