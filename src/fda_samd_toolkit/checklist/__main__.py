"""CLI entry point for FDA checklist module."""

import sys
from pathlib import Path

import click
from rich.console import Console

from fda_samd_toolkit.checklist.runner import (
    print_report,
    report_to_markdown,
    run_from_yaml,
    run_interactive,
)

console = Console()


@click.command()
@click.option(
    "--yaml",
    type=click.Path(exists=True),
    default=None,
    help="Path to YAML artifact inventory file (optional - use interactive mode if not provided)",
)
@click.option(
    "--output",
    type=click.Path(),
    default=None,
    help="Save report to markdown file (optional)",
)
@click.option(
    "--device-name",
    type=str,
    default=None,
    help="Device name (optional - defaults to prompt or YAML value)",
)
def main(yaml: str, output: str, device_name: str) -> None:
    """
    FDA SaMD Submission Readiness Checklist.

    Run interactively (no args) or load from YAML artifact inventory:

    Example:
        fda-samd-checklist
        fda-samd-checklist --yaml artifacts.yaml --output report.md
    """
    try:
        if yaml:
            # Load from YAML
            console.print(f"[cyan]Loading checklist from:[/cyan] {yaml}")
            report = run_from_yaml(yaml, device_name=device_name)
        else:
            # Run interactive
            report = run_interactive(device_name=device_name)

        # Print to console
        print_report(report)

        # Save to file if requested
        if output:
            output_path = Path(output)
            markdown = report_to_markdown(report)
            output_path.write_text(markdown)
            console.print(f"\n[green]✓ Report saved to:[/green] {output_path}")

    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Checklist cancelled by user[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
