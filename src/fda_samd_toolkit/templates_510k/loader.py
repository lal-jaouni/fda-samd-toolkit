"""
Template loader for 510(k) AI/ML section templates.

This module provides utilities to list and copy FDA 510(k) AI/ML submission templates
to a target directory. Templates are designed to be filled in by device developers
preparing a 510(k) submission for an AI/ML medical device.

Templates included:
1. 01_indications_for_use.md - IFU statement with examples
2. 02_device_description.md - System architecture and AI model specification
3. 03_substantial_equivalence.md - Predicate comparison and justification
4. 04_performance_testing.md - Comprehensive validation testing plan
5. 05_training_data_characterization.md - Training data sources and quality
6. 06_risk_analysis.md - AI-specific failure modes and mitigations
7. 07_human_factors.md - User interface, training, workflow integration
"""

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

TEMPLATE_FILES = [
    "01_indications_for_use.md",
    "02_device_description.md",
    "03_substantial_equivalence.md",
    "04_performance_testing.md",
    "05_training_data_characterization.md",
    "06_risk_analysis.md",
    "07_human_factors.md",
]

TEMPLATE_DESCRIPTIONS = {
    "01_indications_for_use.md": (
        "Indications for Use (IFU) statement. Define device purpose, intended users, "
        "clinical setting, contraindications. Includes worked examples."
    ),
    "02_device_description.md": (
        "Device description covering system architecture, AI model specification, "
        "input/output formats, SDLC practices, and interoperability standards."
    ),
    "03_substantial_equivalence.md": (
        "Substantial equivalence comparison to predicate devices. Justify technological "
        "differences, performance comparison, and 510(k) pathway selection."
    ),
    "04_performance_testing.md": (
        "Comprehensive performance testing protocol: study design, dataset characterization, "
        "reference standard, primary/secondary endpoints, subgroup analysis, generalization testing."
    ),
    "05_training_data_characterization.md": (
        "Detailed characterization of training data: sources, demographics, quality control, "
        "ground truth methodology, potential biases, and data distribution shifts."
    ),
    "06_risk_analysis.md": (
        "AI-specific risk analysis including FMEA, model-specific failure modes, "
        "data biases, distribution shifts, automation bias, and post-market surveillance."
    ),
    "07_human_factors.md": (
        "Human factors engineering: user profiles, use environment, output presentation, "
        "workflow integration, training requirements, usability testing, and feedback mechanisms."
    ),
}


def list_templates() -> list[str]:
    """
    List all available 510(k) AI/ML section templates.

    Returns:
        List of template filenames in order of submission appearance.
    """
    return TEMPLATE_FILES.copy()


def get_template_description(template_name: str) -> str:
    """
    Get a brief description of a template's contents.

    Args:
        template_name: Name of the template file (e.g., '01_indications_for_use.md')

    Returns:
        Description of the template's purpose and contents.

    Raises:
        ValueError: If template_name is not a valid template.
    """
    if template_name not in TEMPLATE_DESCRIPTIONS:
        raise ValueError(f"Unknown template: {template_name}. Valid templates: {', '.join(TEMPLATE_FILES)}")
    return TEMPLATE_DESCRIPTIONS[template_name]


def copy_template(template_name: str, destination_dir: Path | str) -> Path:
    """
    Copy a single template to a destination directory.

    Args:
        template_name: Name of the template file (e.g., '01_indications_for_use.md')
        destination_dir: Target directory where template will be copied (Path or str)

    Returns:
        Path to the copied template file.

    Raises:
        ValueError: If template_name is not a valid template.
        FileNotFoundError: If template file does not exist.
        IOError: If copy operation fails.
    """
    if template_name not in TEMPLATE_FILES:
        raise ValueError(f"Unknown template: {template_name}. Valid templates: {', '.join(TEMPLATE_FILES)}")

    source_path = TEMPLATES_DIR / template_name
    if not source_path.exists():
        raise FileNotFoundError(f"Template file not found: {source_path}")

    destination_dir = Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination_path = destination_dir / template_name
    try:
        with open(source_path, encoding="utf-8") as src:
            content = src.read()
        with open(destination_path, "w", encoding="utf-8") as dst:
            dst.write(content)
    except OSError as e:
        raise OSError(f"Failed to copy template {template_name}: {e}") from e

    return destination_path


def copy_all_templates(destination_dir: Path | str) -> list[Path]:
    """
    Copy all 510(k) templates to a destination directory.

    Args:
        destination_dir: Target directory where templates will be copied (Path or str)

    Returns:
        List of paths to copied template files in order.

    Raises:
        IOError: If any copy operation fails.
    """
    destination_dir = Path(destination_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)

    copied_paths = []
    for template_name in TEMPLATE_FILES:
        try:
            path = copy_template(template_name, destination_dir)
            copied_paths.append(path)
        except (OSError, FileNotFoundError) as e:
            # Continue with remaining templates but track error
            print(f"Warning: Failed to copy {template_name}: {e}")

    return copied_paths


def get_template_content(template_name: str) -> str:
    """
    Read and return the full content of a template.

    Args:
        template_name: Name of the template file

    Returns:
        Full template content as string.

    Raises:
        ValueError: If template_name is not a valid template.
        FileNotFoundError: If template file does not exist.
    """
    if template_name not in TEMPLATE_FILES:
        raise ValueError(f"Unknown template: {template_name}. Valid templates: {', '.join(TEMPLATE_FILES)}")

    source_path = TEMPLATES_DIR / template_name
    if not source_path.exists():
        raise FileNotFoundError(f"Template file not found: {source_path}")

    with open(source_path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    if len(sys.argv) < 2:
        print("Usage: python loader.py <command> [args]")
        print("\nCommands:")
        print("  list                     - List all available templates")
        print("  describe <template>      - Show description of a template")
        print("  copy <template> <dest>   - Copy a template to destination")
        print("  copy-all <dest>          - Copy all templates to destination")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        for template in list_templates():
            print(f"  {template}")

    elif command == "describe" and len(sys.argv) > 2:
        template_name = sys.argv[2]
        try:
            desc = get_template_description(template_name)
            print(f"{template_name}:")
            print(f"  {desc}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "copy" and len(sys.argv) > 3:
        template_name = sys.argv[2]
        dest = sys.argv[3]
        try:
            path = copy_template(template_name, Path(dest))
            print(f"Copied {template_name} to {path}")
        except (OSError, ValueError, FileNotFoundError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "copy-all" and len(sys.argv) > 2:
        dest = sys.argv[2]
        try:
            paths = copy_all_templates(Path(dest))
            print(f"Copied {len(paths)} templates to {dest}:")
            for path in paths:
                print(f"  {path}")
        except OSError as e:
            print(f"Error: {e}")
            sys.exit(1)

    else:
        print(f"Unknown command or missing arguments: {command}")
        sys.exit(1)
