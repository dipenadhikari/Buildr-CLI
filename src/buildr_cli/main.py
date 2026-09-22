import os
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .ai import DEFAULT_MODEL, ask_openai, configured_model, has_api_key
from .generator import BuildrGenerationError, create_project, discover_projects


app = typer.Typer(
    name="buildr",
    help="A safe local assistant for asking coding questions and scaffolding Python projects.",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"buildr-cli {__version__}")
        raise typer.Exit()


@app.callback()
def root(
    version: Annotated[
        bool,
        typer.Option("--version", callback=version_callback, is_eager=True, help="Show version."),
    ] = False,
):
    """Buildr keeps generated work local and never executes it automatically."""


@app.command()
def hello():
    """Confirm that Buildr is installed."""
    console.print("[bold green]Buildr is working![/bold green]")


@app.command()
def ask(
    prompt: Annotated[str, typer.Argument(help="Coding or project question.")],
    model: Annotated[
        str | None,
        typer.Option(help=f"OpenAI model. Default: BUILDR_MODEL or {DEFAULT_MODEL}."),
    ] = None,
    offline: Annotated[
        bool,
        typer.Option("--offline", help="Do not call an external model."),
    ] = False,
):
    """Ask Buildr a question, with a safe offline fallback."""
    clean_prompt = prompt.strip()
    if not clean_prompt:
        console.print("[red]Prompt cannot be empty.[/red]")
        raise typer.Exit(code=2)

    if offline or not has_api_key():
        note = "Offline mode: no API request was made."
        if not offline:
            note += " Set OPENAI_API_KEY to enable AI responses."
        console.print(Panel(f"You asked: {clean_prompt}\n\n[dim]{note}[/dim]", title="Buildr"))
        return

    try:
        with console.status("Buildr is thinking..."):
            answer = ask_openai(clean_prompt, model=model or configured_model())
    except Exception as exc:
        console.print(f"[red]Buildr could not complete the request:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(Panel(answer, title=f"Buildr · {model or configured_model()}"))


@app.command("create")
def create_command(
    description: Annotated[str, typer.Argument(help="Project to create, such as 'calculator app'.")],
    name: Annotated[str | None, typer.Option(help="Optional directory name.")] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output", file_okay=False, help="Parent directory for generated projects."),
    ] = Path("projects"),
):
    """Generate a small project without executing or overwriting files."""
    try:
        project = create_project(description, name=name, output_dir=output_dir)
    except BuildrGenerationError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.print(f"[bold green]Created project:[/bold green] {project.name}")
    console.print(f"[dim]Template:[/dim] {project.template}")
    console.print(f"[dim]Path:[/dim] {project.path}")
    for filename in project.files:
        console.print(f"  • {filename}")


@app.command("list")
def list_command(
    output_dir: Annotated[
        Path,
        typer.Option("--output", file_okay=False, help="Directory containing generated projects."),
    ] = Path("projects"),
):
    """List projects created by Buildr."""
    projects = discover_projects(output_dir)
    if not projects:
        console.print("No Buildr projects found.")
        return
    table = Table("Name", "Template", "Description", "Path")
    for project in projects:
        table.add_row(
            project.get("name", "unknown"),
            project.get("template", "unknown"),
            project.get("description", ""),
            project["path"],
        )
    console.print(table)


if __name__ == "__main__":
    app()

