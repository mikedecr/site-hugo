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



_default_prefix = os.environ['CONDA_PREFIX']


def umrun(cmd: List[str], prefix: Optional = None, capture_output = True) -> CompletedProcess:
    assert type(cmd) is list, f"{cmd=} must be a list"
    mamba = os.environ["MAMBA_EXE"]
    if prefix is None:
        prefix = _default_prefix
        log.warning("falling back to " + prefix)
    cmd = [mamba, "run", "-p", prefix, *cmd]
    ret = run(cmd, capture_output = capture_output)
    log.info("umrun: " + " ".join(map(str, ret.args)))
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


def quarto_render_file(path: Path, source_path = "src"):
    """
    activate environment if it exists
    - else build it and re-call
    - if no env file, continue
    """
    path = Path(path).resolve()
    parent = path.parent
    # find the environment
    root = Path(os.getcwd())
    subpath = parent.relative_to(root)
    prefix_path = root / "build/conda_envs" / subpath
    if not prefix_path.exists():
        prefix_path = os.environ['CONDA_PREFIX']
    log.info(" ".join(map(str, ["rendering", path, "in", prefix_path])))
    return umrun(["quarto", "render", path], prefix = prefix_path)


@app.command()
def serve():
    cmd = [
        "hugo",
        "serve",
        "--source", "hugo",
        "--disableFastRender",
        "--buildDrafts",
    ]
    umrun(cmd, capture_output = False)


DOC_SOURCE_DIR = "Directory where quarto source files are located"


@app.command()
def render_quarto(
    source_dir: str = Option("src", "--source-dir", "-s", help=DOC_SOURCE_DIR),
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
    return [quarto_render_file(file, source_path) for file in render_files]


@app.command()
def build(
        context: Context,
        quarto: bool = Option(True, "--quarto", "-q",
                              help = "Render quarto files in source directory"),
        source_dir: str = Option("src", "--source-dir", "-s",
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
    # currently just a "symlink blog posts" step
    links: Dict = get_nested_path(context.obj, "mkd", "links")
    dest_to_srcs: Dict = flatten_nested_dict(links, sep = "/")
    log.info("symlink recipe:\n" + str(dest_to_srcs))
    for dest, sources in dest_to_srcs.items():
        dest_path: Path = Path(dest)
        for source in sources:
            source_path: Path = Path(source)
            name: str = source_path.name
            dest_with_name: Path = dest_path / name
            create_links(source_path, dest_with_name)


if __name__ == "__main__":
    app()
