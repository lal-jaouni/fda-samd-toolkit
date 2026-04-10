"""
Model card generator for FDA-extended model cards.

Generates markdown model cards from YAML configuration files
using Pydantic schemas and Jinja2 templates.
"""

from pathlib import Path
from typing import Any, Dict

import yaml
from jinja2 import Environment, FileSystemLoader

from .schemas import ModelCard


class ModelCardGenerator:
    """Generate model cards from YAML configuration."""

    def __init__(self):
        """Initialize Jinja2 environment with template loader."""
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self.env.globals["now"] = self._jinja_now

    @staticmethod
    def _jinja_now(format_string="iso"):
        """Jinja2 filter for current datetime."""
        from datetime import datetime

        now = datetime.utcnow()
        if format_string == "iso":
            return now.isoformat() + "Z"
        return now.strftime(format_string)

    def load_config(self, config_path: Path) -> Dict[str, Any]:
        """
        Load and parse YAML configuration file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            Parsed YAML configuration as dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if config is None:
            raise ValueError(f"Empty or invalid YAML: {config_path}")

        return config

    def validate_config(self, config: Dict[str, Any]) -> ModelCard:
        """
        Validate configuration against Pydantic schema.

        Args:
            config: Configuration dictionary

        Returns:
            Validated ModelCard object

        Raises:
            ValueError: If configuration doesn't match schema
        """
        try:
            model_card = ModelCard(**config)
            return model_card
        except ValueError as e:
            raise ValueError(f"Configuration validation failed: {e}")

    def generate_model_card(
        self, config_path: Path, output_path: Path, template_name: str = "model_card.md.j2"
    ) -> Path:
        """
        Generate a model card from YAML configuration.

        Args:
            config_path: Path to YAML configuration file
            output_path: Path where generated model card will be saved
            template_name: Jinja2 template filename (default: model_card.md.j2)

        Returns:
            Path to generated model card file

        Raises:
            FileNotFoundError: If config or template file not found
            ValueError: If configuration invalid
        """
        # Load and validate configuration
        config = self.load_config(config_path)
        model_card = self.validate_config(config)

        # Load template
        try:
            template = self.env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError(f"Template not found: {template_name}") from e

        # Render template with model card data
        context = {
            "model_details": model_card.model_details,
            "intended_use": model_card.intended_use,
            "factors": model_card.factors,
            "metrics": model_card.metrics,
            "evaluation_data": model_card.evaluation_data,
            "training_data": model_card.training_data,
            "quantitative_analyses": model_card.quantitative_analyses,
            "ethical_considerations": model_card.ethical_considerations,
            "caveats_recommendations": model_card.caveats_recommendations,
            "fda_specific": model_card.fda_specific,
        }

        markdown = template.render(**context)

        # Write output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        return output_path


def generate_model_card(config_path: Path, output_path: Path) -> Path:
    """
    Convenience function to generate a model card.

    Args:
        config_path: Path to YAML configuration
        output_path: Path where model card will be saved

    Returns:
        Path to generated model card

    Raises:
        FileNotFoundError: If config or template not found
        ValueError: If configuration invalid
    """
    generator = ModelCardGenerator()
    return generator.generate_model_card(config_path, output_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python generator.py <config.yaml> <output.md>")
        sys.exit(1)

    config_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    try:
        result = generate_model_card(config_path, output_path)
        print(f"Model card generated successfully: {result}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
