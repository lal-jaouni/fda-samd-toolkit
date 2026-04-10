"""Tests for the clinical validation plan generator."""

import pytest
from pathlib import Path
import tempfile
import yaml

from fda_samd_toolkit.validation.schemas import (
    ValidationPlan,
    StudyDesign,
    DataSource,
    ReferenceStandard,
    Endpoints,
    StatisticalAnalysisPlan,
)
from fda_samd_toolkit.validation.generator import generate_validation_plan
from fda_samd_toolkit.validation.modality_guidance import get_modality_guidance


class TestValidationSchemas:
    """Test Pydantic validation schemas."""

    def test_study_design_valid(self):
        """Test valid study design creation."""
        design = StudyDesign(
            type="retrospective",
            blinding="double-blinded",
            multi_site=True,
            sites_count=3,
        )
        assert design.type == "retrospective"
        assert design.blinding == "double-blinded"
        assert design.multi_site is True
        assert design.sites_count == 3

    def test_study_design_invalid_type(self):
        """Test invalid study type raises error."""
        with pytest.raises(ValueError):
            StudyDesign(
                type="invalid_type",
                blinding="double-blinded",
            )

    def test_study_design_invalid_blinding(self):
        """Test invalid blinding raises error."""
        with pytest.raises(ValueError):
            StudyDesign(
                type="retrospective",
                blinding="triple-blinded",
            )

    def test_study_design_type_case_insensitive(self):
        """Test that study type is case-insensitive."""
        design = StudyDesign(
            type="PROSPECTIVE",
            blinding="SINGLE-BLINDED",
        )
        assert design.type == "prospective"
        assert design.blinding == "single-blinded"

    def test_data_source_valid(self):
        """Test valid data source creation."""
        source = DataSource(
            sites=["Hospital A", "Hospital B"],
            time_period_start="2020-01-01",
            time_period_end="2023-12-31",
            inclusion_criteria=["Age >= 18", "ECG available"],
            exclusion_criteria=["Pacemaker", "Atrial fibrillation"],
            sample_size=1500,
            sample_size_justification="Power analysis with 90% power",
        )
        assert source.sample_size == 1500
        assert len(source.sites) == 2
        assert len(source.inclusion_criteria) == 2

    def test_reference_standard_valid(self):
        """Test valid reference standard creation."""
        ref = ReferenceStandard(
            gold_standard="Clinical diagnosis",
            reference_source="Cardiologist assessment",
            adjudication_process="3-reader consensus",
            adjudicator_qualifications="Board-certified cardiologists",
            number_of_adjudicators=3,
            inter_rater_reliability_target=0.80,
            inter_rater_reliability_method="Cohen's kappa",
        )
        assert ref.number_of_adjudicators == 3
        assert ref.inter_rater_reliability_target == 0.80

    def test_endpoints_valid(self):
        """Test valid endpoints creation."""
        endpoints = Endpoints(
            primary_endpoint="Sensitivity for AF detection",
            primary_endpoint_target="Sensitivity >= 90%",
            sensitivity_target=0.90,
            specificity_target=0.95,
            sensitivity_lower_ci=0.85,
            specificity_lower_ci=0.90,
        )
        assert endpoints.sensitivity_target == 0.90
        assert endpoints.specificity_target == 0.95

    def test_validation_plan_valid(self):
        """Test creating a complete valid validation plan."""
        plan = ValidationPlan(
            device_name="Test Device",
            intended_use="Test intended use",
            modality="signals",
            document_date="2026-04-10",
            study_design=StudyDesign(
                type="retrospective",
                blinding="double-blinded",
            ),
            data_source=DataSource(
                sites=["Hospital A"],
                time_period_start="2020-01-01",
                time_period_end="2023-12-31",
                inclusion_criteria=["Age >= 18"],
                exclusion_criteria=["None"],
                sample_size=1000,
                sample_size_justification="Power analysis",
            ),
            reference_standard=ReferenceStandard(
                gold_standard="Clinical diagnosis",
                reference_source="Physician assessment",
                adjudication_process="Consensus review",
                adjudicator_qualifications="Board certification",
                number_of_adjudicators=3,
                inter_rater_reliability_target=0.80,
                inter_rater_reliability_method="Kappa",
            ),
            endpoints=Endpoints(
                primary_endpoint="Test endpoint",
                primary_endpoint_target="Target >= 90%",
            ),
            statistical_analysis_plan=StatisticalAnalysisPlan(
                primary_hypothesis="Test hypothesis",
                statistical_test="Binomial test",
                power_calculation_description="Test calculation",
                multiplicity_correction="None",
                missing_data_strategy="Complete case",
            ),
        )
        assert plan.device_name == "Test Device"
        assert plan.modality == "signals"

    def test_validation_plan_invalid_modality(self):
        """Test that invalid modality raises error."""
        with pytest.raises(ValueError):
            ValidationPlan(
                device_name="Test Device",
                intended_use="Test",
                modality="invalid_modality",
                document_date="2026-04-10",
                study_design=StudyDesign(
                    type="retrospective",
                    blinding="double-blinded",
                ),
                data_source=DataSource(
                    sites=["Hospital"],
                    time_period_start="2020-01-01",
                    time_period_end="2023-12-31",
                    inclusion_criteria=["Age >= 18"],
                    exclusion_criteria=["None"],
                    sample_size=1000,
                    sample_size_justification="Test",
                ),
                reference_standard=ReferenceStandard(
                    gold_standard="Test",
                    reference_source="Test",
                    adjudication_process="Test",
                    adjudicator_qualifications="Test",
                    number_of_adjudicators=2,
                    inter_rater_reliability_target=0.75,
                    inter_rater_reliability_method="Test",
                ),
                endpoints=Endpoints(
                    primary_endpoint="Test",
                    primary_endpoint_target="Test",
                ),
                statistical_analysis_plan=StatisticalAnalysisPlan(
                    primary_hypothesis="Test",
                    statistical_test="Test",
                    power_calculation_description="Test",
                    multiplicity_correction="Test",
                    missing_data_strategy="Test",
                ),
            )

    def test_validation_plan_modality_case_insensitive(self):
        """Test that modality is case-insensitive."""
        plan = ValidationPlan(
            device_name="Test Device",
            intended_use="Test",
            modality="IMAGING",
            document_date="2026-04-10",
            study_design=StudyDesign(
                type="retrospective",
                blinding="double-blinded",
            ),
            data_source=DataSource(
                sites=["Hospital"],
                time_period_start="2020-01-01",
                time_period_end="2023-12-31",
                inclusion_criteria=["Age >= 18"],
                exclusion_criteria=["None"],
                sample_size=1000,
                sample_size_justification="Test",
            ),
            reference_standard=ReferenceStandard(
                gold_standard="Test",
                reference_source="Test",
                adjudication_process="Test",
                adjudicator_qualifications="Test",
                number_of_adjudicators=2,
                inter_rater_reliability_target=0.75,
                inter_rater_reliability_method="Test",
            ),
            endpoints=Endpoints(
                primary_endpoint="Test",
                primary_endpoint_target="Test",
            ),
            statistical_analysis_plan=StatisticalAnalysisPlan(
                primary_hypothesis="Test",
                statistical_test="Test",
                power_calculation_description="Test",
                multiplicity_correction="Test",
                missing_data_strategy="Test",
            ),
        )
        assert plan.modality == "imaging"


class TestModalityGuidance:
    """Test modality-specific guidance retrieval."""

    def test_imaging_guidance(self):
        """Test retrieving imaging guidance."""
        guidance = get_modality_guidance("imaging")
        assert guidance["modality_name"] == "Medical Imaging"
        assert "DICOM" in guidance["key_considerations"][0]
        assert "radiologists" in guidance["reference_standard_guidance"].lower()

    def test_signals_guidance(self):
        """Test retrieving signals guidance."""
        guidance = get_modality_guidance("signals")
        assert guidance["modality_name"] == "Physiological Signals"
        assert "sampling rate" in guidance["key_considerations"][0].lower()
        assert "ECG" in guidance["reference_standard_guidance"]

    def test_nlp_guidance(self):
        """Test retrieving NLP guidance."""
        guidance = get_modality_guidance("nlp")
        assert guidance["modality_name"] == "Natural Language Processing"
        assert "Corpus" in guidance["key_considerations"][0]
        assert "clinical experts" in guidance["reference_standard_guidance"].lower()

    def test_multimodal_guidance(self):
        """Test retrieving multimodal guidance."""
        guidance = get_modality_guidance("multimodal")
        assert guidance["modality_name"] == "Multimodal"
        assert "Alignment" in guidance["key_considerations"][0]

    def test_invalid_modality_guidance(self):
        """Test invalid modality raises error."""
        with pytest.raises(ValueError):
            get_modality_guidance("invalid_modality")

    def test_guidance_case_insensitive(self):
        """Test that modality lookup is case-insensitive."""
        guidance1 = get_modality_guidance("IMAGING")
        guidance2 = get_modality_guidance("imaging")
        assert guidance1 == guidance2


class TestGenerationECGExample:
    """Test generating validation plan from ECG example config."""

    @pytest.fixture
    def ecg_config_path(self):
        """Path to ECG example config."""
        return Path(__file__).parent.parent.parent / "examples" / "validation_plan_ecg_classifier.yaml"

    def test_ecg_config_exists(self, ecg_config_path):
        """Test that ECG example config exists."""
        assert ecg_config_path.exists()

    def test_load_ecg_config(self, ecg_config_path):
        """Test loading ECG config."""
        with open(ecg_config_path) as f:
            config = yaml.safe_load(f)
        assert config["device_name"] == "CardioDetect ECG Arrhythmia Classifier"
        assert config["modality"] == "signals"
        assert config["study_design"]["type"] == "retrospective"

    def test_validate_ecg_config(self, ecg_config_path):
        """Test that ECG config validates against schema."""
        with open(ecg_config_path) as f:
            config = yaml.safe_load(f)
        plan = ValidationPlan(**config)
        assert plan.device_name == "CardioDetect ECG Arrhythmia Classifier"
        assert plan.modality == "signals"
        assert plan.study_design.multi_site is True
        assert len(plan.study_design.site_locations) == 3

    def test_generate_ecg_validation_plan(self, ecg_config_path):
        """Test generating ECG validation plan."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(
                str(ecg_config_path),
                str(output_path),
            )
            assert output_path.exists()
            content = output_path.read_text()
            assert "CardioDetect ECG Arrhythmia Classifier" in content
            assert "Clinical Validation Plan" in content
            assert "Johns Hopkins Medical Center" in content
            assert "signals" in content.lower()

    def test_ecg_output_length(self, ecg_config_path):
        """Test that generated output is substantial (5+ pages equivalent)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(
                str(ecg_config_path),
                str(output_path),
            )
            content = output_path.read_text()
            lines = content.split("\n")
            assert len(lines) > 300  # 5+ pages at ~60 lines/page


class TestGenerationImagingExample:
    """Test generating validation plan from imaging example config."""

    @pytest.fixture
    def imaging_config_path(self):
        """Path to imaging example config."""
        return Path(__file__).parent.parent.parent / "examples" / "validation_plan_imaging_segmentation.yaml"

    def test_imaging_config_exists(self, imaging_config_path):
        """Test that imaging example config exists."""
        assert imaging_config_path.exists()

    def test_load_imaging_config(self, imaging_config_path):
        """Test loading imaging config."""
        with open(imaging_config_path) as f:
            config = yaml.safe_load(f)
        assert "PneumoDetect" in config["device_name"]
        assert config["modality"] == "imaging"
        assert config["study_design"]["type"] == "prospective"

    def test_validate_imaging_config(self, imaging_config_path):
        """Test that imaging config validates against schema."""
        with open(imaging_config_path) as f:
            config = yaml.safe_load(f)
        plan = ValidationPlan(**config)
        assert "PneumoDetect" in plan.device_name
        assert plan.modality == "imaging"
        assert plan.study_design.multi_site is True

    def test_generate_imaging_validation_plan(self, imaging_config_path):
        """Test generating imaging validation plan."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(
                str(imaging_config_path),
                str(output_path),
            )
            assert output_path.exists()
            content = output_path.read_text()
            assert "PneumoDetect" in content
            assert "Clinical Validation Plan" in content
            assert "DICOM" in content or "chest radiograph" in content.lower()

    def test_imaging_output_includes_modality_guidance(self, imaging_config_path):
        """Test that generated output includes imaging-specific guidance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(
                str(imaging_config_path),
                str(output_path),
            )
            content = output_path.read_text()
            assert "Medical Imaging" in content or "Modality" in content
            assert "radiologists" in content.lower()


class TestGeneratorErrors:
    """Test error handling in generator."""

    def test_nonexistent_config_file(self):
        """Test that nonexistent config raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            generate_validation_plan(
                "/nonexistent/config.yaml",
                "/tmp/output.md",
            )

    def test_empty_config_file(self):
        """Test that empty config raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "empty.yaml"
            config_path.write_text("")
            with pytest.raises(ValueError):
                generate_validation_plan(
                    str(config_path),
                    str(Path(tmpdir) / "output.md"),
                )

    def test_invalid_yaml_config(self):
        """Test that invalid YAML raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "invalid.yaml"
            config_path.write_text("{ invalid yaml: [}")
            with pytest.raises(Exception):  # yaml.YAMLError or similar
                generate_validation_plan(
                    str(config_path),
                    str(Path(tmpdir) / "output.md"),
                )

    def test_incomplete_config_data(self):
        """Test that incomplete config raises validation error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "incomplete.yaml"
            config_path.write_text("device_name: Test Device\n")
            with pytest.raises(Exception):  # ValidationError
                generate_validation_plan(
                    str(config_path),
                    str(Path(tmpdir) / "output.md"),
                )


class TestTemplateRendering:
    """Test Jinja2 template rendering."""

    def test_template_renders_all_sections(self, ecg_config_path):
        """Test that all major sections are rendered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(str(ecg_config_path), str(output_path))
            content = output_path.read_text()

            expected_sections = [
                "Executive Summary",
                "Device and Intended Use",
                "Study Design",
                "Study Population and Data",
                "Reference Standard",
                "Primary and Secondary Endpoints",
                "Statistical Analysis Plan",
                "Subgroup Analysis",
                "External Validation",
                "Safety Monitoring",
                "Modality-Specific Considerations",
            ]

            for section in expected_sections:
                assert section in content, f"Missing section: {section}"

    def test_template_renders_device_details(self, ecg_config_path):
        """Test that device-specific details are rendered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(str(ecg_config_path), str(output_path))
            content = output_path.read_text()

            with open(ecg_config_path) as f:
                config = yaml.safe_load(f)

            assert config["device_name"] in content
            assert "1500" in content  # sample size
            assert "90%" in content or "0.90" in content  # endpoint target
            assert "double-blinded" in content.lower()

    def test_no_em_dashes_in_output(self, ecg_config_path):
        """Test that output does not contain em-dashes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "validation_plan.md"
            generate_validation_plan(str(ecg_config_path), str(output_path))
            content = output_path.read_text()

            # Check for common em-dash unicode characters
            assert "\u2014" not in content  # em-dash
            assert "\u2013" not in content  # en-dash (should use hyphen)


class TestModularityAndExtensibility:
    """Test modularity for future modality additions."""

    def test_all_modalities_have_guidance(self):
        """Test that all valid modalities have guidance."""
        valid_modalities = ["imaging", "signals", "nlp", "multimodal"]
        for modality in valid_modalities:
            guidance = get_modality_guidance(modality)
            assert "modality_name" in guidance
            assert "key_considerations" in guidance
            assert "data_source_guidance" in guidance

    def test_guidance_structure_consistent(self):
        """Test that all guidance sections have consistent structure."""
        modalities = ["imaging", "signals", "nlp"]
        required_keys = [
            "modality_name",
            "key_considerations",
            "data_source_guidance",
            "reference_standard_guidance",
            "endpoint_guidance",
            "statistical_guidance",
            "subgroup_guidance",
            "safety_guidance",
            "external_validation_guidance",
        ]

        for modality in modalities:
            guidance = get_modality_guidance(modality)
            for key in required_keys:
                assert key in guidance, f"Missing {key} in {modality} guidance"
