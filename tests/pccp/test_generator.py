"""Tests for PCCP generator functionality."""

import tempfile
from pathlib import Path

import pytest

from fda_samd_toolkit.pccp.generator import generate_pccp, load_config
from fda_samd_toolkit.pccp.schemas import PCCPConfig


class TestLoadConfig:
    """Tests for loading and validating YAML configuration."""

    def test_load_config_valid_minimal(self):
        """Load a minimal valid configuration."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        config = load_config(str(config_path))
        assert isinstance(config, PCCPConfig)
        assert config.device_info.name == "CardioDetect ECG Arrhythmia Classifier"
        assert config.device_info.classification == "Class II"

    def test_load_config_missing_file(self):
        """Raise FileNotFoundError for missing config."""
        with pytest.raises(FileNotFoundError):
            load_config("/nonexistent/path/config.yaml")

    def test_load_config_empty_file(self):
        """Raise ValueError for empty config file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="empty"):
                load_config(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_load_config_invalid_schema(self):
        """Raise ValidationError for invalid schema."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("device_info:\n  name: Test\n")  # Missing required fields
            temp_path = f.name

        try:
            with pytest.raises(Exception):  # ValidationError
                load_config(temp_path)
        finally:
            Path(temp_path).unlink()


class TestGeneratePCCP:
    """Tests for PCCP document generation."""

    def test_generate_pccp_end_to_end_ecg(self):
        """Generate a complete PCCP document from ECG example config."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP_ECG.md"
            generate_pccp(str(config_path), str(output_path))

            assert output_path.exists()
            content = output_path.read_text()

            # Check required section headers
            assert "Predetermined Change Control Plan" in content
            assert "Section 1: Description of Modifications" in content
            assert "Section 2: Modification Protocol" in content
            assert "Section 3: Impact Assessment" in content

            # Check device info is populated
            assert "CardioDetect ECG Arrhythmia Classifier" in content
            assert "CardioAI Systems, Inc." in content

            # Check sections have substantive content (not stubs)
            assert len(content) > 3000  # Should be 3+ pages

    def test_generate_pccp_end_to_end_imaging(self):
        """Generate a complete PCCP document from imaging example config."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_imaging_segmentation.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP_Imaging.md"
            generate_pccp(str(config_path), str(output_path))

            assert output_path.exists()
            content = output_path.read_text()

            assert "PneumoDetect Chest X-Ray Pneumonia Classifier" in content
            assert "RespirAI Medical, Inc." in content
            assert "Section 1: Description of Modifications" in content
            assert len(content) > 3000

    def test_generate_pccp_creates_output_directory(self):
        """Create output directory if it doesn't exist."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "dir" / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            assert output_path.exists()
            assert output_path.parent.exists()

    def test_generate_pccp_missing_config(self):
        """Raise FileNotFoundError for missing config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            with pytest.raises(FileNotFoundError):
                generate_pccp("/nonexistent/config.yaml", str(output_path))

    def test_generate_pccp_invalid_config(self):
        """Raise ValidationError for invalid config."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("device_info:\n  name: Test\n")  # Missing required fields
            config_path = f.name

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            try:
                with pytest.raises(Exception):  # ValidationError wrapped
                    generate_pccp(config_path, str(output_path))
            finally:
                Path(config_path).unlink()


class TestGeneratedContent:
    """Tests validating the content of generated PCCP documents."""

    def test_generated_content_includes_tables(self):
        """Generated PCCP includes performance metric tables."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            # Should have performance threshold table
            assert "| Metric |" in content or "| Baseline |" in content

    def test_generated_content_includes_device_info(self):
        """Generated PCCP includes all device information."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            assert "Intended Use:" in content or "intended use" in content.lower()
            assert "Indications for Use:" in content or "indications" in content.lower()
            assert "Classification:" in content or "Class II" in content

    def test_generated_content_includes_modification_details(self):
        """Generated PCCP includes all planned modifications."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            # Check that modification types are included
            assert "Model Retraining" in content

    def test_generated_content_includes_protocols(self):
        """Generated PCCP includes modification protocol details."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            assert "Data Management" in content
            assert "Validation" in content or "validation" in content.lower()

    def test_generated_content_includes_impact_assessment(self):
        """Generated PCCP includes impact assessment section."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            assert "Benefits" in content or "benefits" in content.lower()
            assert "Risks" in content or "risks" in content.lower()
            assert "Sub-Population" in content or "sub.population" in content.lower()

    def test_generated_content_includes_fda_references(self):
        """Generated PCCP includes FDA citations."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            assert "FDA" in content or "[^1]" in content
            assert "Predetermined Change Control" in content or "PCCP" in content

    def test_generated_content_no_em_dashes(self):
        """Generated PCCP does not contain em dashes."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            # Check for em dash character (U+2014)
            assert "\u2014" not in content, "Em dashes found in generated content"

    def test_generated_content_is_valid_markdown(self):
        """Generated PCCP is valid markdown."""
        config_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
        if not config_path.exists():
            pytest.skip("Example config not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "PCCP.md"
            generate_pccp(str(config_path), str(output_path))

            content = output_path.read_text()
            # Basic markdown validation
            assert content.startswith("#")  # Starts with heading
            # Check balanced parentheses (rough check)
            assert content.count("(") == content.count(")")
            # Check balanced brackets (rough check)
            assert content.count("[") == content.count("]")
