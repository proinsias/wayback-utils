"""Utilities for working with URLs saved to OmniFocus."""

import typing

import rich.pretty
import typer

import wayback_utils

app = typer.Typer()
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
    """Utilities for working with URLs saved to OmniFocus."""
    pass


if __name__ == "__main__":
    app()
