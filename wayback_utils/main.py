"""Utilities for submitting URLs to the Internet Archive's Wayback Machine."""

import typing

import typer
from rich import print

import markdown
import medium_utils
import omnifocus
import pocket_utils
import raindrop
import urls_utils
import wayback_utils

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
app.add_typer(markdown.app, name="markdown")
app.add_typer(medium_utils.app, name="medium")
app.add_typer(omnifocus.app, name="omnifocus")
app.add_typer(pocket_utils.app, name="pocket")
app.add_typer(raindrop.app, name="raindrop")
app.add_typer(urls_utils.app, name="urls")


def version_callback(value: bool) -> None:
    if value:
        print(
            f"{wayback_utils.__name__} version: {wayback_utils.__version__}",
        )
        raise typer.Exit()


@app.callback()
def main(
    *,
    version: typing.Optional[bool] = typer.Option(
        False,
        "--version",
        "-v",
        help=f"print the version of {wayback_utils.__name__}",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Utilities to submit URLs to the Internet Archive's Wayback Machine."""
    pass


if __name__ == "__main__":
    app()
