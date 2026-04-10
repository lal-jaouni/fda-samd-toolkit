"""PCCP generator: load YAML config, validate, and render markdown document."""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from pydantic import ValidationError

from .schemas import PCCPConfig


def generate_pccp(config_path: str, output_path: str) -> None:
    """
    Generate a PCCP markdown document from a YAML configuration.

    Args:
        config_path: Path to YAML configuration file
        output_path: Path where the PCCP markdown document will be written

    Raises:
        FileNotFoundError: If config file does not exist
        ValidationError: If configuration does not match PCCPConfig schema
        RuntimeError: If template rendering fails

    Example:
        >>> generate_pccp('examples/pccp_ecg.yaml', 'output/PCCP_ECG.md')
    """
    config_path = Path(config_path)
    output_path = Path(output_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        config_data = yaml.safe_load(f)

    if not config_data:
        raise ValueError(f"Configuration file is empty: {config_path}")

    try:
        config = PCCPConfig(**config_data)
    except ValidationError as e:
        raise ValidationError(f"Configuration validation failed:\n{e.json()}") from e

    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("pccp_main.md.j2")
    rendered = template.render(config=config)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(rendered)


def load_config(config_path: str) -> PCCPConfig:
    """
    Load and validate a PCCP configuration from YAML.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Validated PCCPConfig object

    Raises:
        FileNotFoundError: If config file does not exist
        ValidationError: If configuration is invalid
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        config_data = yaml.safe_load(f)

    if not config_data:
        raise ValueError(f"Configuration file is empty: {config_path}")

    return PCCPConfig(**config_data)
