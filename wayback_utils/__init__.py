"""Utilities for submitting URLs to the Internet Archive's Wayback Machine."""

# Keep these in sync with CHANGELOG.md and pyproject.toml.
__name__ = "wayback-utils"
__pkg_name__ = "wayback_utils"
__version__ = "0.1.0"


def version_callback(value: bool) -> None:
    import typer

    if value:
        typer.echo(
            f"{__name__} version: {__version__}",
        )
        raise typer.Exit()
