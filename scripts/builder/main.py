import os
from pathlib import Path
from subprocess import run, CompletedProcess
from typing import List, Optional

from typer import Typer, Option

from ._links import create_links
app = Typer(name = "Hugo Site Builder")


def umrun(cmd: List[str], prefix: Optional = None) -> CompletedProcess:
    assert type(cmd) is list, f"{cmd=} must be a list"
    mamba = os.environ["MAMBA_EXE"]
    if prefix is None:
        prefix = os.environ['CONDA_PREFIX']
    cmd = [mamba, "run", "-p", prefix, *cmd]
    print(cmd)
    return run(cmd)


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
    if prefix_path.exists():
        print("found prefix", prefix_path, "for", path)
    else:
        prefix_path = None
        print("rendering", path, "in default environment")
    umrun(["quarto", "render", path], prefix = prefix_path)


@app.command()
def serve():
    cmd = [
        "hugo",
        "serve",
        "--source", "hugo",
        "--disableFastRender",
        "--buildDrafts",
    ]
    umrun(cmd)


DOC_SOURCE_DIR = "Directory where quarto source files are located"


@app.command()
def render_quarto(
    source_dir: str = Option("src", "--source-dir", "-s",
                             help=DOC_SOURCE_DIR),
):
    source_path: Path = Path(source_dir).resolve()
    # find quarto files
    try:
        render_files: List[Path] = find_quarto_render_sources(source_path)
        from pprint import pprint
        pprint(list(map(str, render_files)))
    except FileNotFoundError:
        raise FileNotFoundError(f"{source_path=} does not exist")
    # no files found
    if len(render_files) == 0:
        raise ValueError(f"Found no files to render in {source_path=}")
    # render each file
    for file in render_files:
        _ = quarto_render_file(file, source_path)


@app.command()
def build(
        quarto: bool = Option(True, "--quarto", "-q",
                              help = "Render quarto files in source directory"),
        source_dir: str = Option("src", "--source-dir", "-s",
                                 help = DOC_SOURCE_DIR)
):
    """
    - render all qmds
    - serve site
    """
    render_quarto(source_dir)
    serve()


@app.command()
def init():
    blog_src = "submodules/blog-monorepo"
    blog_dest = "src/blog"
    create_links(blog_src, blog_dest)


if __name__ == "__main__":
    app()
