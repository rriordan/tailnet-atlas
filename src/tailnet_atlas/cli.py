"""Initial CLI entry point for the Tailnet Atlas implementation handoff."""

import typer

from tailnet_atlas import __version__

app = typer.Typer(
    name="tailnet-atlas",
    help="Private launcher and health dashboard for services on a Tailscale tailnet.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Display the current package version."""
    typer.echo(__version__)


@app.command()
def specification() -> None:
    """Show where implementation requirements are documented."""
    typer.echo("Read HERMES_TASK.md and docs/implementation-spec.md before implementation.")


if __name__ == "__main__":
    app()
