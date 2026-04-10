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
        from fda_samd_toolkit.pccp.generator import generate_pccp

        config_path = Path(config)
        output_path = Path(output)

        console.print(f"[cyan]Loading config:[/cyan] {config_path}")
        console.print(f"[cyan]Template:[/cyan] {template}")
        console.print("[cyan]Generating PCCP...[/cyan]")
        generate_pccp(str(config_path), str(output_path))
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
    except Exception as e:
        console.print(
            Panel(
                f"PCCP generation failed: {e}",
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
    if not check_module_available("fda_samd_toolkit.pccp", "PCCP validator"):
        sys.exit(1)

    try:
        from fda_samd_toolkit.pccp.validator import validate_pccp

        file_path = Path(file)
        console.print(f"[cyan]Validating:[/cyan] {file_path}")
        issues = validate_pccp(str(file_path))
        if not issues:
            console.print("[green]✓ No validation issues found[/green]")
            return
        errors = [i for i in issues if i.level == "error"]
        warnings = [i for i in issues if i.level == "warning"]
        info = [i for i in issues if i.level == "info"]
        if errors:
            console.print(f"[red]✗ {len(errors)} error(s)[/red]")
            for issue in errors:
                console.print(f"  [red]error[/red] {issue.section}: {issue.message}")
        if warnings:
            console.print(f"[yellow]! {len(warnings)} warning(s)[/yellow]")
            for issue in warnings:
                console.print(f"  [yellow]warn [/yellow] {issue.section}: {issue.message}")
        if info:
            console.print(f"[cyan]i {len(info)} info[/cyan]")
            for issue in info:
                console.print(f"  [cyan]info [/cyan] {issue.section}: {issue.message}")
        if errors:
            sys.exit(1)

    except ImportError:
        console.print(
            Panel(
                "Validation module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)
    except Exception as e:
        console.print(
            Panel(
                f"PCCP validation failed: {e}",
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

    # Map device type to a packaged example we can copy as a starter scaffold.
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    type_to_example = {
        "ecg": examples_dir / "pccp_ecg_classifier.yaml",
        "imaging": examples_dir / "pccp_imaging_segmentation.yaml",
        "signals": examples_dir / "pccp_ecg_classifier.yaml",
        "nlp": examples_dir / "pccp_ecg_classifier.yaml",
    }

    source = type_to_example.get(type.lower())
    if source is None or not source.exists():
        console.print(
            Panel(
                f"No starter example available for type '{type}'. See examples/ in the repo.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)

    try:
        from fda_samd_toolkit.pccp.schemas import PCCPConfig as _  # noqa: F401

        console.print(f"[cyan]Scaffolding PCCP config for:[/cyan] {type.upper()}")
        output_path.write_text(source.read_text())
        console.print(f"[green]✓ Template created:[/green] {output_path}")
        console.print("[dim]Edit the config and run 'fda-samd pccp generate' to build your PCCP.[/dim]")

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
                "[cyan]Sections:[/cyan]\n" + "\n".join(f"  - {section}" for section in template["sections"]),
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
        from fda_samd_toolkit.model_cards.generator import ModelCardGenerator

        config_path = Path(config)
        output_path = Path(output)

        console.print(f"[cyan]Loading model config:[/cyan] {config_path}")
        console.print("[cyan]Generating model card...[/cyan]")
        ModelCardGenerator().generate_model_card(config_path, output_path)
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
    except Exception as e:
        console.print(
            Panel(
                f"Model card generation failed: {e}",
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

    examples_dir = Path(__file__).parent.parent.parent / "examples"
    source = examples_dir / "model_card_ecg_classifier.yaml"

    if not source.exists():
        console.print(
            Panel(
                f"Starter example not found at {source}",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)

    try:
        from fda_samd_toolkit.model_cards import schemas as _  # noqa: F401

        console.print(f"[cyan]Scaffolding model card for:[/cyan] {type.upper()}")
        output_path.write_text(source.read_text())
        console.print(f"[green]✓ Template created:[/green] {output_path}")
        console.print("[dim]Edit the config and run 'fda-samd model-card generate' to build your model card.[/dim]")

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
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=False,
    help="YAML file with pre-recorded artifact statuses (skips interactive prompts)",
)
@click.option(
    "--device-name",
    type=str,
    required=False,
    help="Device name to include in the report",
)
@click.option(
    "--output",
    type=click.Path(),
    required=False,
    help="Optional markdown report output path",
)
def checklist(config: str | None, device_name: str | None, output: str | None) -> None:
    """
    Run the FDA readiness checklist.

    With --config, runs non-interactively from a YAML file. Without, runs
    interactively, prompting for each of the 58 items across 8 categories.

    Examples:
        fda-samd checklist
        fda-samd checklist --config examples/checklist_artifacts.yaml --output readiness.md
    """
    if not check_module_available("fda_samd_toolkit.checklist", "Readiness checklist"):
        sys.exit(1)

    try:
        from fda_samd_toolkit.checklist.runner import (
            print_report,
            report_to_markdown,
            run_from_yaml,
            run_interactive,
        )

        if config:
            console.print(f"[cyan]Loading checklist artifacts from:[/cyan] {config}")
            report = run_from_yaml(config, device_name=device_name)
        else:
            console.print("[cyan]Running interactive FDA SaMD Readiness Checklist[/cyan]")
            report = run_interactive(device_name=device_name)

        print_report(report)

        if output:
            output_path = Path(output)
            output_path.write_text(report_to_markdown(report))
            console.print(f"[green]✓ Markdown report written:[/green] {output_path}")

    except ImportError:
        console.print(
            Panel(
                "Checklist module not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)
    except Exception as e:
        console.print(
            Panel(
                f"Checklist failed: {e}",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@cli.group()
def validation() -> None:
    """Clinical validation plan operations."""
    pass


@validation.command(name="generate")
@click.option(
    "--config",
    type=click.Path(exists=True),
    required=True,
    help="Path to validation plan YAML configuration",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Output path for generated validation plan markdown",
)
@click.option(
    "--modality",
    type=click.Choice(
        ["imaging", "signals", "nlp", "multimodal"],
        case_sensitive=False,
    ),
    required=False,
    help="Override the modality declared in the config (imaging, signals, nlp, multimodal)",
)
def generate_validation(config: str, output: str, modality: str | None) -> None:
    """
    Generate a clinical validation plan from configuration.

    Example:
        fda-samd validation generate --config examples/validation_plan_ecg_classifier.yaml --output validation_plan.md
        fda-samd validation generate --config my_plan.yaml --output plan.md --modality imaging
    """
    if not check_module_available("fda_samd_toolkit.validation", "Validation plan generator"):
        sys.exit(1)

    try:
        from fda_samd_toolkit.validation.generator import generate_validation_plan

        console.print(f"[cyan]Loading validation config:[/cyan] {config}")
        if modality:
            console.print(f"[cyan]Using modality override:[/cyan] {modality}")
        console.print("[cyan]Generating clinical validation plan...[/cyan]")
        generate_validation_plan(config, output, modality=modality)
        console.print(f"[green]✓ Validation plan generated:[/green] {output}")

    except ImportError:
        console.print(
            Panel(
                "Validation plan generator not available.",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)
    except Exception as e:
        console.print(
            Panel(
                f"Validation plan generation failed: {e}",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)


@validation.command(name="init")
@click.option(
    "--modality",
    type=click.Choice(
        ["imaging", "signals", "nlp", "multimodal"],
        case_sensitive=False,
    ),
    required=True,
    help="Modality for the starter template",
)
@click.option(
    "--output",
    type=click.Path(),
    required=False,
    help="Output path for config template (default: validation_plan.yaml)",
)
def init_validation(modality: str, output: str) -> None:
    """
    Scaffold a validation plan configuration from a worked example.

    Example:
        fda-samd validation init --modality signals --output my_plan.yaml
    """
    output_path = Path(output or "validation_plan.yaml")

    examples_dir = Path(__file__).parent.parent.parent / "examples"
    starter_map = {
        "signals": "validation_plan_ecg_classifier.yaml",
        "imaging": "validation_plan_imaging_segmentation.yaml",
        "nlp": "validation_plan_ecg_classifier.yaml",
        "multimodal": "validation_plan_ecg_classifier.yaml",
    }
    source = examples_dir / starter_map[modality.lower()]

    if not source.exists():
        console.print(
            Panel(
                f"Starter example not found at {source}",
                title="Error",
                style="red",
            )
        )
        sys.exit(1)

    console.print(f"[cyan]Scaffolding validation plan for:[/cyan] {modality.upper()}")
    output_path.write_text(source.read_text())
    console.print(f"[green]✓ Template created:[/green] {output_path}")
    console.print("[dim]Edit the config and run 'fda-samd validation generate' to build your plan.[/dim]")


if __name__ == "__main__":
    cli()
