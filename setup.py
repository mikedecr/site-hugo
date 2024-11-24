from setuptools import setup

setup(
    name="mkd-website",
    version="0.1.0",
    py_modules=["scripts.builder"],
    install_requires=[
        "typer",
    ],
    entry_points={
        "console_scripts": [
            "mkd = scripts.builder.main:app",  # This binds the 'yeet' command to your Typer app
        ],
    },
)
