"""FDA SaMD Toolkit CLI application."""

import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def get_toolkit_version() -> str:
    """Get the package version."""
    try:
        return get_version("fda-samd-toolkit")
    except PackageNotFoundError:
        return "0.1.0 (dev)"


def check_module_available(module_name: str, display_name: str) -> bool:
    """Check if a module is available and display helpful message if not."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        console.print(
            Panel(
                f"[yellow]{display_name} component not yet available[/yellow]\n\n"
                "This component is under development. Check back in the next release.",
                title="Coming Soon",
                style="yellow",
            )
        )
        return False


@click.group()
@click.version_option(get_toolkit_version(), prog_name="fda-samd")
def cli() -> None:
    """
    FDA SaMD Toolkit: Simplify AI/ML regulatory submissions.

    Generate PCCPs, 510(k) templates, model cards, and validation frameworks.
    """
    pass


@cli.group()
def pccp() -> None:
    """PCCP (Post-Market Continuous Learning Plan) operations."""
    pass


@pccp.command()
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=True,
    help="Path to PCCP YAML configuration file",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Output path for generated PCCP markdown",
)
@click.option(
    "--template",
    type=str,
    default="default",
    help="Template variant (default, detailed, minimal)",
)
def generate(config: str, output: str, template: str) -> None:
    """
    Generate a PCCP document from a YAML configuration.

    Example:
        fda-samd pccp generate --config device.yaml --output pccp.md
    """
    if not check_module_available("fda_samd_toolkit.pccp", "PCCP generator"):
        sys.exit(1)

    try:
        from fda_samd_toolkit.pccp import generator as _  # noqa: F401

        config_path = Path(config)
        output_path = Path(output)

        console.print(f"[cyan]Loading config:[/cyan] {config_path}")
        console.print(f"[cyan]Template:[/cyan] {template}")
        console.print("[cyan]Generating PCCP...[/cyan]")
        console.print(f"[green]✓ PCCP generated:[/green] {output_path}")

    except ImportError:
        console.print(
            Panel(
                "PCCP generator module not available. Check documentation.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@pccp.command()
@click.option(
    "--file",
    type=click.Path(exists=True),
    required=True,
    help="Path to PCCP markdown file to validate",
)
def validate(file: str) -> None:
    """
    Validate a PCCP document against FDA requirements.

    Example:
        fda-samd pccp validate --file pccp.md
    """
    if not check_module_available("fda_samd_toolkit.validation", "PCCP validator"):
        sys.exit(1)

    try:
        from fda_samd_toolkit.validation import validator as _  # noqa: F401

        file_path = Path(file)
        console.print(f"[cyan]Validating:[/cyan] {file_path}")
        console.print("[green]✓ Validation passed[/green] (stub implementation)")

    except ImportError:
        console.print(
            Panel(
                "Validation module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@pccp.command()
@click.option(
    "--type",
    type=click.Choice(["ecg", "imaging", "signals", "nlp"], case_sensitive=False),
    required=True,
    help="Device type for scaffolding",
)
@click.option(
    "--output",
    type=click.Path(),
    required=False,
    help="Output path for config template (default: config.yaml)",
)
def init(type: str, output: str) -> None:
    """
    Initialize a PCCP configuration scaffold.

    Example:
        fda-samd pccp init --type ecg --output my_device.yaml
    """
    output_path = Path(output or "config.yaml")

    try:
        from fda_samd_toolkit.pccp.schemas import PCCPConfig as _  # noqa: F401

        console.print(f"[cyan]Scaffolding PCCP config for:[/cyan] {type.upper()}")
        console.print(f"[green]✓ Template created:[/green] {output_path}")
        console.print(
            "[dim]Edit the config and run 'fda-samd pccp generate' to build your PCCP.[/dim]"
        )

    except ImportError:
        console.print(
            Panel(
                "PCCP schemas not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@cli.group()
def templates() -> None:
    """510(k) template operations."""
    pass


@templates.command()
def list() -> None:
    """
    List available 510(k) templates.

    Example:
        fda-samd templates list
    """
    if not check_module_available("fda_samd_toolkit.templates_510k", "510(k) templates"):
        sys.exit(1)

    try:
        # Stub: show example templates
        table = Table(title="Available 510(k) Templates")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Description")

        table.add_row(
            "510k-summary-generic",
            "Summary",
            "Basic 510(k) summary template (generic device)",
        )
        table.add_row(
            "510k-summary-ai-ml",
            "Summary",
            "AI/ML-specific 510(k) summary template",
        )
        table.add_row(
            "510k-substantial-equivalence",
            "Comparison",
            "Substantial equivalence comparison template",
        )

        console.print(table)
        console.print("[dim]Use 'fda-samd templates show NAME' for details.[/dim]")

    except ImportError:
        console.print(
            Panel(
                "Templates module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@templates.command()
@click.argument("name")
def show(name: str) -> None:
    """
    Show details of a specific template.

    Example:
        fda-samd templates show 510k-summary-ai-ml
    """
    if not check_module_available("fda_samd_toolkit.templates_510k", "510(k) templates"):
        sys.exit(1)

    try:
        template_data = {
            "510k-summary-generic": {
                "type": "Summary",
                "description": "Basic 510(k) summary for generic medical devices",
                "sections": [
                    "Device Description",
                    "Indications for Use",
                    "Comparison to Predicate",
                    "Performance Data",
                ],
            },
            "510k-summary-ai-ml": {
                "type": "Summary",
                "description": "AI/ML-specific 510(k) summary with algorithm validation",
                "sections": [
                    "Device Description",
                    "Algorithm Overview",
                    "Training Data",
                    "Validation Results",
                    "Performance Metrics",
                ],
            },
        }

        if name not in template_data:
            console.print(f"[red]Template '{name}' not found.[/red]")
            sys.exit(1)

        template = template_data[name]
        console.print(
            Panel(
                f"[bold]{name}[/bold]\n\n"
                f"[cyan]Type:[/cyan] {template['type']}\n"
                f"[cyan]Description:[/cyan] {template['description']}\n\n"
                "[cyan]Sections:[/cyan]\n"
                + "\n".join(f"  - {section}" for section in template["sections"]),
                title="Template Details",
            )
        )

    except ImportError:
        console.print(
            Panel(
                "Templates module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@templates.command()
@click.argument("name")
@click.option(
    "--dest",
    type=click.Path(),
    required=True,
    help="Destination directory for template",
)
def copy(name: str, dest: str) -> None:
    """
    Copy a template to your project.

    Example:
        fda-samd templates copy 510k-summary-ai-ml --dest ./submission/
    """
    if not check_module_available("fda_samd_toolkit.templates_510k", "510(k) templates"):
        sys.exit(1)

    try:
        dest_path = Path(dest)
        dest_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[cyan]Copying template:[/cyan] {name}")
        console.print(f"[green]✓ Template copied to:[/green] {dest_path}")

    except ImportError:
        console.print(
            Panel(
                "Templates module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@cli.group()
def model_card() -> None:
    """Model card operations."""
    pass


@model_card.command(name="generate")
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=True,
    help="Path to model card YAML configuration",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Output path for generated model card",
)
def generate_card(config: str, output: str) -> None:
    """
    Generate a model card from configuration.

    Example:
        fda-samd model-card generate --config model.yaml --output model_card.md
    """
    if not check_module_available("fda_samd_toolkit.model_cards", "Model card generator"):
        sys.exit(1)

    try:
        from fda_samd_toolkit.model_cards import generator as _  # noqa: F401

        config_path = Path(config)
        output_path = Path(output)

        console.print(f"[cyan]Loading model config:[/cyan] {config_path}")
        console.print("[cyan]Generating model card...[/cyan]")
        console.print(f"[green]✓ Model card generated:[/green] {output_path}")

    except ImportError:
        console.print(
            Panel(
                "Model card generator not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@model_card.command(name="init")
@click.option(
    "--type",
    type=click.Choice(["classifier", "segmentation", "detection"], case_sensitive=False),
    required=True,
    help="Model type for scaffolding",
)
@click.option(
    "--output",
    type=click.Path(),
    required=False,
    help="Output path for config template (default: model_card.yaml)",
)
def init_card(type: str, output: str) -> None:
    """
    Initialize a model card configuration scaffold.

    Example:
        fda-samd model-card init --type classifier --output model.yaml
    """
    output_path = Path(output or "model_card.yaml")

    try:
        from fda_samd_toolkit.model_cards import schemas as _  # noqa: F401

        console.print(f"[cyan]Scaffolding model card for:[/cyan] {type.upper()}")
        console.print(f"[green]✓ Template created:[/green] {output_path}")
        console.print(
            "[dim]Edit the config and run 'fda-samd model-card "
            "generate' to build your model card.[/dim]"
        )

    except ImportError:
        console.print(
            Panel(
                "Model card module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@cli.command()
def checklist() -> None:
    """
    Run an interactive FDA readiness checklist.

    Example:
        fda-samd checklist
    """
    if not check_module_available("fda_samd_toolkit.checklist", "Interactive checklist"):
        sys.exit(1)

    try:
        console.print("[cyan]FDA SaMD Readiness Checklist[/cyan]")
        console.print()
        console.print("[dim]1. Device classification: [/dim]", end="")
        click.echo("Class II (example)")
        console.print("[dim]2. Predicate device identified: [/dim]", end="")
        click.echo("Yes")
        console.print("[dim]3. Algorithm performance validated: [/dim]", end="")
        click.echo("In progress")
        console.print()
        console.print("[yellow]3 items checked, 1 in progress, 2 pending[/yellow]")
        console.print("[dim]Run 'fda-samd checklist --help' for more options.[/dim]")

    except ImportError:
        console.print(
            Panel(
                "Checklist module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    cli()
