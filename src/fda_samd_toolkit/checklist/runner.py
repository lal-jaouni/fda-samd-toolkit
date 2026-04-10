"""Interactive runner for FDA submission readiness checklist."""

from datetime import datetime
from pathlib import Path

import yaml
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from fda_samd_toolkit.checklist.items import get_all_categories, get_items_by_category
from fda_samd_toolkit.checklist.schemas import (
    CategoryResult,
    ChecklistItem,
    ItemSeverity,
    ItemStatus,
    ReadinessReport,
)

console = Console()


def _prompt_item_status(item: ChecklistItem) -> ItemStatus:
    """Prompt user for status of a single item with context."""
    console.print(f"\n[bold cyan]{item.requirement}[/bold cyan]")
    console.print(f"[dim]ID: {item.id}[/dim]")
    console.print(f"[dim]Reference: {item.standard_reference}[/dim]")
    console.print(f"[dim]Evidence needed: {item.evidence_required}[/dim]")
    if item.notes:
        console.print(f"[yellow]Note: {item.notes}[/yellow]")

    choice = Prompt.ask(
        "Status",
        choices=["complete", "partial", "missing"],
        default="missing",
    )

    status_map = {
        "complete": ItemStatus.COMPLETE,
        "partial": ItemStatus.PARTIAL,
        "missing": ItemStatus.MISSING,
    }
    return status_map[choice]


def run_interactive(
    device_name: str | None = None, skip_complete: bool = False
) -> ReadinessReport:
    """
    Run interactive checklist walking through each item.

    Args:
        device_name: Optional name of device being assessed
        skip_complete: If True, don't ask about items marked complete in previous run

    Returns:
        ReadinessReport with complete assessment
    """
    console.print(
        "\n[bold]FDA SaMD Submission Readiness Checklist[/bold]\n"
        "Answer 'complete', 'partial', or 'missing' for each requirement.\n"
    )

    if not device_name:
        device_name = Prompt.ask(
            "Device name (optional)", default="Unnamed Device"
        )

    categories = get_all_categories()
    all_results = []

    for category in categories:
        console.print(f"\n[bold cyan]--- {category} ---[/bold cyan]\n")

        items = get_items_by_category(category)
        category_items = []

        for item in items:
            status = _prompt_item_status(item)
            item_copy = item.model_copy()
            item_copy.status = status
            category_items.append(item_copy)

        # Calculate category stats
        complete_count = sum(1 for i in category_items if i.status == ItemStatus.COMPLETE)
        partial_count = sum(1 for i in category_items if i.status == ItemStatus.PARTIAL)
        missing_count = sum(1 for i in category_items if i.status == ItemStatus.MISSING)

        cat_result = CategoryResult(
            category=category,
            items=category_items,
            total=len(category_items),
            complete=complete_count,
            partial=partial_count,
            missing=missing_count,
        )
        all_results.append(cat_result)

    # Generate report
    total_items = sum(r.total for r in all_results)
    total_complete = sum(r.complete for r in all_results)
    overall_pct = round((total_complete / total_items) * 100, 1) if total_items > 0 else 0.0

    report = ReadinessReport(
        categories=all_results,
        overall_pct=overall_pct,
        timestamp=datetime.now().isoformat(),
        device_name=device_name,
    )

    return report


def run_from_yaml(
    yaml_path: str | Path, device_name: str | None = None
) -> ReadinessReport:
    """
    Load checklist status from YAML file instead of interactive prompts.

    YAML format:
      device_name: Device Name
      items:
        - id: dc-001
          status: complete
        - id: dc-002
          status: partial

    Args:
        yaml_path: Path to YAML artifact inventory file
        device_name: Override device name from YAML

    Returns:
        ReadinessReport with status loaded from file

    Raises:
        FileNotFoundError: If YAML file not found
        ValueError: If YAML format invalid
    """
    yaml_path = Path(yaml_path)

    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("YAML file must contain a dictionary at root level")

    file_device_name = data.get("device_name", "Unnamed Device")
    if device_name:
        file_device_name = device_name

    # Build status map from YAML
    item_statuses = {}
    for item_entry in data.get("items", []):
        if "id" not in item_entry or "status" not in item_entry:
            raise ValueError("Each item in YAML must have 'id' and 'status'")

        item_id = item_entry["id"]
        status_str = item_entry["status"].lower()

        status_map = {
            "complete": ItemStatus.COMPLETE,
            "partial": ItemStatus.PARTIAL,
            "missing": ItemStatus.MISSING,
        }
        if status_str not in status_map:
            raise ValueError(
                f"Invalid status '{status_str}' for item {item_id}. "
                "Must be 'complete', 'partial', or 'missing'"
            )

        item_statuses[item_id] = status_map[status_str]

    # Apply statuses to items
    all_results = []

    for category in get_all_categories():
        items = get_items_by_category(category)
        category_items = []

        for item in items:
            if item.id in item_statuses:
                item_copy = item.model_copy()
                item_copy.status = item_statuses[item.id]
                category_items.append(item_copy)
            else:
                # Not in YAML, default to missing
                item_copy = item.model_copy()
                item_copy.status = ItemStatus.MISSING
                category_items.append(item_copy)

        # Calculate category stats
        complete_count = sum(1 for i in category_items if i.status == ItemStatus.COMPLETE)
        partial_count = sum(1 for i in category_items if i.status == ItemStatus.PARTIAL)
        missing_count = sum(1 for i in category_items if i.status == ItemStatus.MISSING)

        cat_result = CategoryResult(
            category=category,
            items=category_items,
            total=len(category_items),
            complete=complete_count,
            partial=partial_count,
            missing=missing_count,
        )
        all_results.append(cat_result)

    # Generate report
    total_items = sum(r.total for r in all_results)
    total_complete = sum(r.complete for r in all_results)
    overall_pct = round((total_complete / total_items) * 100, 1) if total_items > 0 else 0.0

    report = ReadinessReport(
        categories=all_results,
        overall_pct=overall_pct,
        timestamp=datetime.now().isoformat(),
        device_name=file_device_name,
    )

    return report


def report_to_markdown(report: ReadinessReport) -> str:
    """
    Convert ReadinessReport to markdown format.

    Args:
        report: ReadinessReport instance

    Returns:
        Markdown string suitable for documentation
    """
    lines = [
        "# FDA SaMD Submission Readiness Report\n",
        f"**Device:** {report.device_name}\n",
        f"**Report Generated:** {report.timestamp}\n",
        (
            f"**Overall Completion:** {report.overall_pct}% "
            f"({report.total_complete}/{report.total_items} items)\n"
        ),
    ]

    # Blockers section
    if report.blockers:
        lines.append("\n## BLOCKERS (Critical Missing Items)\n")
        lines.append(
            f"{report.total_blockers_missing} blocker items require immediate "
            "attention:\n"
        )
        for category, item in report.blockers:
            lines.append(
                f"- [{item.id}] **{category}**: {item.requirement}\n"
                f"  - Evidence: {item.evidence_required}\n"
                f"  - Reference: {item.standard_reference}\n"
            )

    # Category breakdown
    lines.append("\n## Category Breakdown\n")

    for cat_result in report.categories:
        lines.append(
            f"\n### {cat_result.category}\n"
            f"**Completion: {cat_result.completion_pct}% "
            f"({cat_result.complete}/{cat_result.total})**\n"
        )

        # Status distribution
        lines.append(
            f"- Complete: {cat_result.complete}\n"
            f"- Partial: {cat_result.partial}\n"
            f"- Missing: {cat_result.missing}\n"
        )

        # List missing and partial items
        incomplete_items = [
            i
            for i in cat_result.items
            if i.status in (ItemStatus.MISSING, ItemStatus.PARTIAL)
        ]

        if incomplete_items:
            lines.append("\n**Incomplete Items:**\n")
            for item in incomplete_items:
                severity_str = (
                    f"[{item.severity.upper()}]"
                    if item.severity.value != ItemSeverity.MINOR.value
                    else ""
                )
                status_str = f"({item.status.upper()})"
                lines.append(
                    f"- {severity_str} [{item.id}] {item.requirement} {status_str}\n"
                    f"  - Evidence: {item.evidence_required}\n"
                    f"  - Reference: {item.standard_reference}\n"
                )

    lines.append("\n## Summary\n")
    lines.append(f"- **Total Items:** {report.total_items}\n")
    lines.append(f"- **Complete:** {report.total_complete}\n")
    lines.append(f"- **Partial:** {sum(c.partial for c in report.categories)}\n")
    lines.append(f"- **Missing:** {sum(c.missing for c in report.categories)}\n")
    lines.append(f"- **Blocker Items:** {report.total_blockers_missing}\n")

    return "".join(lines)


def print_report(report: ReadinessReport) -> None:
    """Print report to console using rich formatting."""
    console.print("\n[bold]FDA SaMD Submission Readiness Report[/bold]")
    console.print(f"Device: [cyan]{report.device_name}[/cyan]")
    console.print(f"Generated: [dim]{report.timestamp}[/dim]\n")

    # Overall progress
    overall_bar_pct = int(report.overall_pct / 5)
    bar = "[green]" + "=" * overall_bar_pct + "[/green]"
    bar += "[dim]" + "-" * (20 - overall_bar_pct) + "[/dim]"
    console.print(f"Overall: {bar} {report.overall_pct}%\n")

    # Blockers alert
    if report.blockers:
        console.print(
            f"[red bold]WARNING: {report.total_blockers_missing} BLOCKER ITEMS MISSING[/red bold]\n"
        )

    # Category summary table
    table = Table(title="Category Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Complete", justify="right", style="green")
    table.add_column("Partial", justify="right", style="yellow")
    table.add_column("Missing", justify="right", style="red")
    table.add_column("Progress", justify="right")

    for cat in report.categories:
        bar_pct = int(cat.completion_pct / 5)
        bar = "[green]" + "=" * bar_pct + "[/green]"
        bar += "[dim]" + "-" * (20 - bar_pct) + "[/dim]"
        table.add_row(
            cat.category,
            str(cat.complete),
            str(cat.partial),
            str(cat.missing),
            f"{bar} {cat.completion_pct}%",
        )

    console.print(table)


