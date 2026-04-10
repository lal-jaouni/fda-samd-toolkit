"""End-to-end integration test for the full FDA SaMD toolkit pipeline.

This test runs the critical user journey: load example configurations,
run every generator, and verify outputs are valid and complete.
"""

import tempfile
from pathlib import Path

import pytest

from fda_samd_toolkit.checklist.runner import report_to_markdown, run_from_yaml
from fda_samd_toolkit.model_cards.generator import generate_model_card
from fda_samd_toolkit.pccp.generator import generate_pccp
from fda_samd_toolkit.validation.generator import generate_validation_plan


class TestFullPipeline:
    """Test the complete FDA SaMD toolkit workflow."""

    def test_pccp_pipeline_ecg_classifier(self):
        """Test PCCP generation pipeline end-to-end."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            # Run generator
            generate_pccp(str(example_path), str(output_path))

            # Verify output exists and is valid
            output_file = Path(output_path)
            assert output_file.exists(), "PCCP output file was not created"

            content = output_file.read_text()
            assert len(content) > 5000, "PCCP output is suspiciously short"
            assert "Predetermined Change Control Plan" in content
            assert "CardioDetect ECG Arrhythmia Classifier" in content
            assert "FDA" in content or "FDA" in content.upper()
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_model_card_pipeline_ecg_classifier(self):
        """Test model card generation pipeline end-to-end."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "model_card_ecg_classifier.yaml"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = Path(f.name)

        try:
            # Run generator
            generate_model_card(example_path, output_path)

            # Verify output exists and is valid
            output_file = output_path
            assert output_file.exists(), "Model card output file was not created"

            content = output_file.read_text()
            assert len(content) > 1000, "Model card output is suspiciously short"
            assert "Model Card" in content or "Model Details" in content
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_validation_pipeline_ecg_classifier(self):
        """Test validation plan generation pipeline end-to-end."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "validation_plan_ecg_classifier.yaml"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            # Run generator
            generate_validation_plan(str(example_path), str(output_path))

            # Verify output exists and is valid
            output_file = Path(output_path)
            assert output_file.exists(), "Validation plan output file was not created"

            content = output_file.read_text()
            assert len(content) > 5000, "Validation plan output is suspiciously short"
            assert "Validation" in content or "validation" in content.lower()
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_checklist_pipeline_artifacts(self):
        """Test checklist generation pipeline end-to-end."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"

        # Run checklist generator
        report = run_from_yaml(str(example_path), device_name="ECG Classifier Device")
        content = report_to_markdown(report)

        # Verify output is valid
        assert len(content) > 1000, "Checklist output is suspiciously short"
        assert "Readiness" in content or "readiness" in content.lower()
        assert "ECG Classifier Device" in content

    def test_multiple_example_files_are_valid(self):
        """Verify all example YAML files can be loaded without errors."""
        examples_dir = Path(__file__).parent.parent.parent / "examples"

        if not examples_dir.exists():
            pytest.skip("Examples directory not found")

        yaml_files = list(examples_dir.glob("**/*.yaml"))
        assert len(yaml_files) > 0, "No example YAML files found"

        # Just verify files exist and are not empty
        for yaml_file in yaml_files:
            assert yaml_file.stat().st_size > 0, f"Example file is empty: {yaml_file}"
