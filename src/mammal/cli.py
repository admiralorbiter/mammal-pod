"""Command line interface for Project MAMMAL scientific instrument."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from mammal import __version__
from mammal.artifacts.store import ArtifactStore
from mammal.config import settings
from mammal.db import check_db, get_engine, get_session, init_db

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="mammal")
def main() -> None:
    """Project MAMMAL: Scientific instrument & provenance kernel."""
    pass


@main.command()
def doctor() -> None:
    """Run environmental diagnostics, directory validation, and database health checks."""
    console.print(Panel(f"[bold cyan]Project MAMMAL Diagnostic Doctor (v{__version__})[/bold cyan]"))

    table = Table(title="System Environment & Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status / Path", style="green")

    table.add_row("Python Version", sys.version.split()[0])
    table.add_row("Data Root (MAMMAL_DATA_ROOT)", str(settings.data_root))
    table.add_row("Database Path", str(settings.db_path))

    # Ensure directories exist
    settings.ensure_directories()
    table.add_row("Data Directories", "INITIALIZED / OK")

    # Check DB
    try:
        engine = get_engine()
        init_db(engine)
        db_status = check_db(engine)
        table.add_row("SQLite Foreign Keys", db_status["foreign_keys"])
        table.add_row("SQLite Journal Mode", db_status["journal_mode"])
        table.add_row("SQLite Integrity Check", db_status["integrity"])
    except Exception as exc:
        table.add_row("Database Status", f"[red]ERROR: {exc}[/red]")

    # Check Artifacts
    try:
        store = ArtifactStore()
        with get_session() as session:
            art_status = store.verify_all_artifacts(session)
            table.add_row(
                "Artifact Store",
                f"{art_status['verified']}/{art_status['total']} verified ({art_status['status']})"
            )
    except Exception as exc:
        table.add_row("Artifact Store", f"[red]ERROR: {exc}[/red]")

    console.print(table)


@main.group()
def db() -> None:
    """Database administration commands."""
    pass


@db.command(name="init")
def db_init() -> None:
    """Initialize database tables."""
    settings.ensure_directories()
    init_db()
    console.print(f"[bold green]✓ Database initialized successfully at {settings.db_path}[/bold green]")


@db.command(name="check")
def db_check() -> None:
    """Run database integrity checks."""
    status = check_db()
    table = Table(title="Database Health Check", show_header=True, header_style="bold blue")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green" if status["integrity"] == "ok" else "red")

    for k, v in status.items():
        table.add_row(k, v)

    console.print(table)


@main.group()
def artifacts() -> None:
    """Artifact store commands."""
    pass


@artifacts.command(name="verify")
def artifacts_verify() -> None:
    """Verify cryptographic hashes for all artifacts on disk."""
    store = ArtifactStore()
    with get_session() as session:
        result = store.verify_all_artifacts(session)

    table = Table(title="Artifact Verification Audit", show_header=True, header_style="bold yellow")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green" if result["status"] == "PASS" else "red")

    table.add_row("Total Registered", str(result["total"]))
    table.add_row("Verified Intact", str(result["verified"]))
    table.add_row("Missing Files", str(len(result["missing"])))
    table.add_row("Corrupted Files", str(len(result["corrupted"])))
    table.add_row("Audit Result", result["status"])

    console.print(table)


@main.command()
@click.option("--host", default="127.0.0.1", help="Host interface to bind.")
@click.option("--port", default=5000, type=int, help="Port to listen on.")
@click.option("--debug", is_flag=True, default=False, help="Run in Flask debug mode.")
def serve(host: str, port: int, debug: bool) -> None:
    """Start Project MAMMAL local web server and session runner."""
    from mammal.app import create_app

    app = create_app()
    console.print(Panel(f"[bold cyan]MAMMAL POD // CODEC Session Server[/bold cyan]\nListening on [bold green]http://{host}:{port}[/bold green]"))
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()

