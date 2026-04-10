"""Golden file tests for PCCP generator.

Golden file tests detect unintended regressions in generator output.
If a test fails after template changes, regenerate the golden file:

    pytest tests/golden/test_pccp_golden.py --update-golden
"""

import tempfile
from pathlib import Path

import pytest

from fda_samd_toolkit.pccp.generator import generate_pccp


class TestPCCPGoldenFiles:
    """Test PCCP generator output against golden files."""

    def test_pccp_output_matches_golden_ecg_classifier(self, golden_data_dir):
        """Generate PCCP from ECG classifier example and compare to golden file."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        golden_file = golden_data_dir / "pccp" / "ecg_classifier.md"

        # Skip if golden file doesn't exist yet
        if not golden_file.exists():
            pytest.skip("Golden file not found, run with --update-golden to create it")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            generate_pccp(str(example_path), str(output_path))

            with open(output_path) as f:
                actual_output = f.read()
            with open(golden_file) as f:
                expected_output = f.read()

            # Compare outputs
            assert actual_output == expected_output, (
                "PCCP output differs from golden file. "
                "If this is intentional, regenerate with: "
                "pytest tests/golden/test_pccp_golden.py --update-golden"
            )
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_pccp_output_has_required_sections(self):
        """Verify PCCP output contains all required FDA sections."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            output_path = f.name

        try:
            generate_pccp(str(example_path), str(output_path))
            content = Path(output_path).read_text()

            # Verify required sections are present
            required_sections = [
                "Predetermined Change Control Plan",
                "Executive Summary",
                "Section 1: Description of Modifications",
                "Section 2: Modification Protocol",
                "Section 3: Impact Assessment",
            ]
            for section in required_sections:
                assert section in content, f"Missing required section: {section}"

            # Verify device info is present
            assert "CardioDetect ECG Arrhythmia Classifier" in content
            assert "CardioAI Systems, Inc." in content
        finally:
            Path(output_path).unlink(missing_ok=True)
