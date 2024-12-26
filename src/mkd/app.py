from pathlib import Path
import tomllib
from typing import Dict, Union

from typer import Typer, Context, Option

# from .main import init, render_quarto, serve, build


def read_toml(file: Union[str, Path]) -> Dict:
    io = open(file, "rb")
    return tomllib.load(io)


app = Typer(name = "Hugo Site Builder")


@app.callback()
def _callback(context: Context,
              config_file: str = Option("pyproject.toml", "-f", "--file")):
    toml_data: Dict = read_toml(config_file)
    context.obj = toml_data
    return context

