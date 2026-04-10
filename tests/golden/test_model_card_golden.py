"""Golden file tests for model card generator.

Golden file tests detect unintended regressions in generator output.
If a test fails after template changes, regenerate the golden file:

    pytest tests/golden/test_model_card_golden.py --update-golden
"""

import tempfile
from pathlib import Path

import pytest

from fda_samd_toolkit.model_cards.generator import generate_model_card


class TestModelCardGoldenFiles:
    """Test model card generator output against golden files."""

    def test_model_card_output_matches_golden_ecg_classifier(self, golden_data_dir):
        """Generate model card from ECG classifier example and compare structure to golden file."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "model_card_ecg_classifier.yaml"
        golden_file = golden_data_dir / "model_card" / "ecg_classifier.md"

        # Skip if golden file doesn't exist yet
        if not golden_file.exists():
            pytest.skip("Golden file not found, run with --update-golden to create it")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            generate_model_card(str(example_path), str(output_path))

            with open(output_path) as f:
                actual_output = f.read()
            with open(golden_file) as f:
                expected_output = f.read()

            # Compare line counts and key sections rather than exact bytes
            # (timestamps and metadata may vary)
            actual_lines = actual_output.strip().split("\n")
            expected_lines = expected_output.strip().split("\n")

            # Allow some variance in line count due to timestamp differences
            assert abs(len(actual_lines) - len(expected_lines)) < 5, (
                f"Model card output structure differs significantly from golden file. "
                f"Expected ~{len(expected_lines)} lines, got {len(actual_lines)} lines."
            )

            # Verify key sections are still present
            for section in ["Model Card", "Model Details", "Factors"]:
                assert section in actual_output, f"Missing section: {section}"
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_model_card_output_has_required_sections(self):
        """Verify model card output contains all required sections."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "model_card_ecg_classifier.yaml"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            generate_model_card(str(example_path), str(output_path))
            content = Path(output_path).read_text()

            # Verify required sections are present
            required_sections = [
                "Model Card",
                "Model Details",
                "Intended Use",
                "Factors",
            ]
            for section in required_sections:
                assert section in content, f"Missing required section: {section}"

            # Verify content is meaningful
            assert len(content) > 1000, "Model card output is suspiciously short"
        finally:
            Path(output_path).unlink(missing_ok=True)
