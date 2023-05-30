"""Utilities for submitting URLs to the Internet Archive's Wayback Machine."""

import typing

import rich.pretty
import typer

import markdown
import medium
import omnifocus
import pocket
import raindrop
import wayback_utils

app = typer.Typer()
app.add_typer(markdown.app, name="markdown")
app.add_typer(medium.app, name="medium")
app.add_typer(omnifocus.app, name="omnifocus")
app.add_typer(pocket.app, name="pocket")
app.add_typer(raindrop.app, name="raindrop")

rich.pretty.install()


def version_callback(value: bool, ) -> None:
    if value:
        typer.echo(
            f"{wayback_utils.__name__} version: {wayback_utils.__version__}")
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
