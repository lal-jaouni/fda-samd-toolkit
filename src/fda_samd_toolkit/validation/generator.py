"""Generator for clinical validation plans from YAML configuration."""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from fda_samd_toolkit.validation.modality_guidance import get_modality_guidance
from fda_samd_toolkit.validation.schemas import ValidationPlan


def generate_validation_plan(
    config_path: str,
    output_path: str,
    modality: str = None,
) -> None:
    """
    Generate a clinical validation plan from a YAML configuration.

    Args:
        config_path: Path to YAML configuration file
        output_path: Path to output markdown file
        modality: Data modality (imaging, signals, nlp, multimodal).
                 If not specified, will use modality from config.

    Raises:
        FileNotFoundError: If config file does not exist
        ValueError: If config is invalid or modality is unknown
        IOError: If output file cannot be written
    """
    config_path = Path(config_path)
    output_path = Path(output_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config_data = yaml.safe_load(f)

    if not config_data:
        raise ValueError(f"Config file is empty: {config_path}")

    plan = ValidationPlan(**config_data)

    if modality is None:
        modality = plan.modality
    else:
        modality = modality.lower()
        plan.modality = modality

    try:
        modality_guidance = get_modality_guidance(modality)
    except ValueError as e:
        raise ValueError(f"Invalid modality: {e}") from e

    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["md", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("validation_plan.md.j2")

    rendered = template.render(
        validation_plan=plan,
        modality_guidance=modality_guidance,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(rendered)
