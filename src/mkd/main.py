import os
from pathlib import Path
# from subprocess import run, CompletedProcess
import shutil
from typing import Any, Dict, List

from typer import Option, Context

from .links import create_links
from .logging import log
from .runners import uv_run, micromamba_run, mamba_exe, pixi_run

from .app import app


QUARTO_SOURCE_SUFFIXES = [
    ".md",
    ".qmd"
]

QUARTO_EXCLUDE_FILENAMES = [
    "README.md"
]


def find_quarto_render_sources(
        path: Path,
        extensions = QUARTO_SOURCE_SUFFIXES,
        exclude_patterns = QUARTO_EXCLUDE_FILENAMES
) -> List[Path]:
    """
    List of all filepaths to render with quarto
    """
    # ugh just in case
    path = Path(path).absolute()
    if not path.exists():
        raise FileNotFoundError(f"cannot find {path=}")
    if not path.is_dir():
        if path.suffix in extensions and all(p.lower() not in str(path).lower() for p in exclude_patterns):
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
    # render the qmd and place it in _quarto.yml: project.output_dir
    path = Path(path).absolute()
    if (pixi_toml := resolve_pixi_manifest_path(path)):
        out = _pixi_render(qmd_path=path, pixi_manifest_path=pixi_toml)
    elif (conda_prefix := resolve_conda_prefix(path)):
        out = _micromamba_render(path, conda_prefix)
    else:
        out = _uvx_render(path)
    # currently hugo-md does not copy the index_files to output-dir
    # so we need to make an inference about where in output-dir that should have gone
    index_files_dir: Path = path.parent / (path.stem + "_files")
    if not index_files_dir.exists():
        return
    log.info(f"detected {index_files_dir}, must copy these to output")
    quarto_yml_path: Path = _find_quarto_yml(path)
    quarto_output_dir: Path = _quarto_output_dir(quarto_yml_path)
    src_branch_below_quarto: Path = path.relative_to(quarto_yml_path.parent).parent
    dest_page_dir = quarto_output_dir / src_branch_below_quarto
    dest_index_files_dir = dest_page_dir / index_files_dir.stem
    assert dest_index_files_dir.parent.exists()
    log.info(f"copying {index_files_dir} to {dest_index_files_dir}")
    return shutil.copytree(index_files_dir, dest_index_files_dir, dirs_exist_ok=True)


def _quarto_output_dir(quarto_yml_path: Path):
    """
    fully qualified path of the quarto output dir, relative to location of _quarto.yml
    """
    yaml_data = read_yaml(quarto_yml_path)
    flattened_yaml = flatten_nested_dict(yaml_data, sep = "/")
    output_branch = flattened_yaml["project/output-dir"]
    yaml_dir = quarto_yml_path.parent
    return (yaml_dir / output_branch).absolute()



def _find_quarto_yml(path: Path):
    try:
        iterdir = path.iterdir()
        for f in iterdir:
            name = f.name
            if name.startswith("_quarto") and name.endswith(".yml"):
                return f
        # can't find it
        return _find_quarto_yml(path.parent)
    except NotADirectoryError:
        parent = path.parent
        if parent == Path("/"):
            return None
        else:
            return _find_quarto_yml(parent)


def read_yaml(path: Path):
    from yaml import load, CLoader
    return load(open(path, "r"), Loader = CLoader)


def _micromamba_render(path: str, prefix_path: str):
    log.info(" ".join(map(str, ["rendering", path, "in", prefix_path])))
    which_quarto = micromamba_run(["which", "quarto"], prefix=prefix_path, capture_output=True).stdout
    log.info(f"which quarto: {which_quarto}")
    return micromamba_run(["quarto", "render", path], prefix = prefix_path, capture_output=False)


def _uvx_render(path: str):
    return uv_run(["quarto", "render", path], capture_output = False)


def _pixi_render(qmd_path: Path, pixi_manifest_path: Path = Path("./pixi.toml")):
    return pixi_run(
        cmd = ["quarto", "render", qmd_path],
        manifest_path=pixi_manifest_path,
        capture_output=False
    )


def resolve_pixi_manifest_path(path: Path):
    """
    return path to pixi.toml else None
    """
    maybe_pixi_toml: Path = Path(path).parent / "pixi.toml"
    if maybe_pixi_toml.exists():
        return maybe_pixi_toml


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
    return micromamba_run(
        cmd = [mamba_exe, "env", "create", "-f", env_yml, "-p", prefix_path, "-y"],
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


# pin these here for now
WEB_SOURCE = "qmd"
WEB_DEST = "hugo/content"
IGNORE_PATTERNS = [".html", ".qmd", "_freeze", "_cache", "conda", ".R", "_quarto.yml"]


def _move_ignore_fn(src: str, names: List[str]):
    kept_names = []
    for name in names:
        for pattern in IGNORE_PATTERNS:
            if pattern.lower() in name.lower():
                kept_names.append(name)
    return kept_names


def move_to_content(
    context: Context,
):
    src_dir = WEB_SOURCE
    dest_dir = WEB_DEST
    Path(dest_dir).mkdir(exist_ok=True, parents=True)
    _out = shutil.copytree(src=src_dir, dst=dest_dir, ignore=_move_ignore_fn, dirs_exist_ok = True)
    log.info(list(Path(_out).iterdir()))
    return _out


@app.command()
def clear(
    context: Context,
):
    link_toml: Dict = get_nested_path(context.obj, "mkd", "links")
    kv_pairs: Dict[str, str] = flatten_nested_dict(link_toml, sep = "/")
    qmd_paths = [k for k in kv_pairs if str(k).startswith("qmd")]
    log.info(f"Unlinking {qmd_paths=}")
    _ = [Path(p).unlink for p in qmd_paths]





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
    link(context, hard=True)
    link(context, hard=False)


def link(context: Context, hard=False):
    if hard:
        print("HARD")
        links_leaf = "hard_links"
    else:
        links_leaf = "links"
    link_toml: Dict = get_nested_path(context.obj, "mkd", links_leaf)
    link_to_target: Dict = flatten_nested_dict(link_toml, sep = "/")
    log.info("symlink recipe:\n" + str(link_to_target))
    for link_dir, target_dir in link_to_target.items():
        create_links(
            Path(target_dir).resolve(),
            Path(link_dir).resolve(),
            hard=hard
        )


if __name__ == "__main__":
    app()
