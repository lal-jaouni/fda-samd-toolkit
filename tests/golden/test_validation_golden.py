"""Golden file tests for validation plan generator.

Golden file tests detect unintended regressions in generator output.
If a test fails after template changes, regenerate the golden file:

    pytest tests/golden/test_validation_golden.py --update-golden
"""

import tempfile
from pathlib import Path

import pytest

from fda_samd_toolkit.validation.generator import generate_validation_plan


class TestValidationGoldenFiles:
    """Test validation plan generator output against golden files."""

    def test_validation_output_matches_golden_ecg_classifier(self, golden_data_dir):
        """Generate validation plan from ECG classifier example and compare to golden file."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "validation_plan_ecg_classifier.yaml"
        golden_file = golden_data_dir / "validation" / "ecg_classifier.md"

        # Skip if golden file doesn't exist yet
        if not golden_file.exists():
            pytest.skip("Golden file not found, run with --update-golden to create it")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            generate_validation_plan(str(example_path), str(output_path))

            with open(output_path) as f:
                actual_output = f.read()
            with open(golden_file) as f:
                expected_output = f.read()

            # Compare outputs
            assert actual_output == expected_output, (
                "Validation plan output differs from golden file. "
                "If this is intentional, regenerate with: "
                "pytest tests/golden/test_validation_golden.py --update-golden"
            )
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_validation_output_has_required_sections(self):
        """Verify validation plan output contains all required sections."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "validation_plan_ecg_classifier.yaml"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            generate_validation_plan(str(example_path), str(output_path))
            content = Path(output_path).read_text()

            # Verify required sections are present (case-insensitive)
            required_sections = [
                "Validation",
                "Clinical",
            ]
            for section in required_sections:
                assert section in content, f"Missing required section: {section}"

            # Verify content is meaningful
            assert len(content) > 5000, "Validation plan output is suspiciously short"
        finally:
            Path(output_path).unlink(missing_ok=True)
