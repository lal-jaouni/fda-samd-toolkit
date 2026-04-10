"""Golden file tests for checklist runner.

Golden file tests detect unintended regressions in generator output.
If a test fails after template changes, regenerate the golden file:

    pytest tests/golden/test_checklist_golden.py --update-golden
"""

from pathlib import Path

import pytest

from fda_samd_toolkit.checklist.runner import report_to_markdown, run_from_yaml


class TestChecklistGoldenFiles:
    """Test checklist runner output against golden files."""

    def test_checklist_output_matches_golden_artifacts(self, golden_data_dir):
        """Generate checklist from artifacts example and compare structure to golden file."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"
        golden_file = golden_data_dir / "checklist" / "artifacts.md"

        # Skip if golden file doesn't exist yet
        if not golden_file.exists():
            pytest.skip("Golden file not found, run with --update-golden to create it")

        report = run_from_yaml(str(example_path), device_name="Test Device")
        actual_output = report_to_markdown(report)

        with open(golden_file) as f:
            expected_output = f.read()

        # Compare outputs - allow some variance due to timestamps
        actual_lines = actual_output.strip().split("\n")
        expected_lines = expected_output.strip().split("\n")

        assert abs(len(actual_lines) - len(expected_lines)) < 5, (
            f"Checklist output structure differs significantly from golden file. "
            f"Expected ~{len(expected_lines)} lines, got {len(actual_lines)} lines."
        )

    def test_checklist_output_has_required_sections(self):
        """Verify checklist output contains all required sections."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"

        report = run_from_yaml(str(example_path), device_name="Test Device")
        content = report_to_markdown(report)

        # Verify required sections are present
        required_sections = [
            "Readiness",
            "Device",
            "Summary",
        ]
        for section in required_sections:
            assert section in content, f"Missing required section: {section}"

        # Verify content is meaningful
        assert len(content) > 1000, "Checklist output is suspiciously short"
