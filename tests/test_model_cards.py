"""
Tests for model card generator and schemas.
"""

import tempfile
from pathlib import Path

import pytest

from fda_samd_toolkit.model_cards.generator import ModelCardGenerator, generate_model_card
from fda_samd_toolkit.model_cards.schemas import (
    CaveatsRecommendations,
    EthicalConsiderations,
    EvaluationData,
    Factors,
    FDASpecific,
    IntendedUse,
    MetricSubgroup,
    Metrics,
    ModelCard,
    ModelDetails,
    TrainingData,
)


class TestModelCardSchemas:
    """Test Pydantic schemas for model cards."""

    def test_model_details_creation(self):
        """Test ModelDetails schema validation."""
        details = ModelDetails(
            name="Test Model",
            version="1.0.0",
            owner="Test Organization",
        )
        assert details.name == "Test Model"
        assert details.version == "1.0.0"
        assert details.owner == "Test Organization"

    def test_intended_use_creation(self):
        """Test IntendedUse schema validation."""
        intended = IntendedUse(
            primary_use="AF detection from ECG",
            intended_users=["Cardiologists", "ED physicians"],
            clinical_setting=["Hospital", "ED"],
            contraindications=["Pacemaker patients"],
        )
        assert intended.primary_use == "AF detection from ECG"
        assert len(intended.intended_users) == 2
        assert len(intended.contraindications) == 1

    def test_metrics_with_subgroups(self):
        """Test Metrics schema with subgroup analysis."""
        subgroup = MetricSubgroup(
            subgroup_name="Female",
            subgroup_definition="Biological sex female",
            n_cases=100,
            metrics={"sensitivity": 0.92, "specificity": 0.94},
        )

        metrics = Metrics(
            overall={"sensitivity": 0.92, "specificity": 0.94},
            subgroups=[subgroup],
        )

        assert metrics.overall["sensitivity"] == 0.92
        assert len(metrics.subgroups) == 1
        assert metrics.subgroups[0].subgroup_name == "Female"

    def test_training_data_creation(self):
        """Test TrainingData schema."""
        training = TrainingData(
            datasets=["Dataset A", "Dataset B"],
            sample_size=100000,
            demographics={"mean_age": 67, "female_percent": 42},
        )
        assert training.sample_size == 100000
        assert training.demographics["mean_age"] == 67

    def test_evaluation_data_creation(self):
        """Test EvaluationData schema."""
        eval_data = EvaluationData(
            datasets=["External validation cohort"],
            preprocessing=["Butterworth filter", "z-score normalization"],
            test_train_split={"train": 0.8, "test": 0.2},
        )
        assert len(eval_data.datasets) == 1
        assert len(eval_data.preprocessing) == 2
        assert eval_data.test_train_split["train"] == 0.8

    def test_fda_specific_creation(self):
        """Test FDASpecific schema."""
        fda = FDASpecific(
            intended_use_statement="AF detection from ECG",
            classification="Class II; 510(k)",
            predicate_devices=["K232488"],
            drift_monitoring_plan="Monthly KPI checks",
        )
        assert fda.classification == "Class II; 510(k)"
        assert len(fda.predicate_devices) == 1

    def test_full_model_card_creation(self):
        """Test creating a complete ModelCard."""
        card = ModelCard(
            model_details=ModelDetails(
                name="Test AF Detector",
                version="1.0.0",
                owner="Test Org",
            ),
            intended_use=IntendedUse(
                primary_use="AF detection",
                intended_users=["Cardiologists"],
                clinical_setting=["Hospital"],
            ),
            factors=Factors(),
            metrics=Metrics(overall={"sensitivity": 0.92}),
            evaluation_data=EvaluationData(datasets=["Test cohort"]),
            training_data=TrainingData(datasets=["Training cohort"]),
        )
        assert card.model_details.name == "Test AF Detector"
        assert card.metrics.overall["sensitivity"] == 0.92

    def test_optional_fields_in_schema(self):
        """Test that optional fields work correctly."""
        # Create model card with only required fields
        card = ModelCard(
            model_details=ModelDetails(
                name="Minimal Model",
                version="1.0.0",
                owner="Test",
            ),
            intended_use=IntendedUse(
                primary_use="Test",
                intended_users=["Users"],
                clinical_setting=["Setting"],
            ),
            factors=Factors(),
            metrics=Metrics(overall={"accuracy": 0.95}),
            evaluation_data=EvaluationData(datasets=["Test"]),
            training_data=TrainingData(datasets=["Train"]),
            # Optional sections
            ethical_considerations=None,
            fda_specific=None,
        )
        assert card.ethical_considerations is None
        assert card.fda_specific is None


class TestModelCardGenerator:
    """Test ModelCardGenerator class."""

    def test_generator_initialization(self):
        """Test generator initialization."""
        gen = ModelCardGenerator()
        assert gen.env is not None

    def test_load_valid_yaml_config(self):
        """Test loading valid YAML configuration."""
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
model_details:
  name: Test Model
  version: 1.0.0
  owner: Test Org
intended_use:
  primary_use: Test purpose
  intended_users:
    - Doctors
  clinical_setting:
    - Hospital
factors: {}
metrics:
  overall:
    accuracy: 0.95
evaluation_data:
  datasets:
    - Test dataset
training_data:
  datasets:
    - Training dataset
""")
            temp_path = Path(f.name)

        try:
            gen = ModelCardGenerator()
            config = gen.load_config(temp_path)
            assert config["model_details"]["name"] == "Test Model"
            assert config["model_details"]["version"] == "1.0.0"
        finally:
            temp_path.unlink()

    def test_load_nonexistent_yaml(self):
        """Test loading non-existent file raises error."""
        gen = ModelCardGenerator()
        with pytest.raises(FileNotFoundError):
            gen.load_config(Path("/nonexistent/path/config.yaml"))

    def test_validate_config(self):
        """Test config validation."""
        gen = ModelCardGenerator()
        config = {
            "model_details": {
                "name": "Test",
                "version": "1.0.0",
                "owner": "Test",
            },
            "intended_use": {
                "primary_use": "Test",
                "intended_users": ["Users"],
                "clinical_setting": ["Setting"],
            },
            "factors": {},
            "metrics": {"overall": {"accuracy": 0.95}},
            "evaluation_data": {"datasets": ["Test"]},
            "training_data": {"datasets": ["Train"]},
        }
        model_card = gen.validate_config(config)
        assert isinstance(model_card, ModelCard)
        assert model_card.model_details.name == "Test"

    def test_validate_invalid_config(self):
        """Test invalid config raises validation error."""
        gen = ModelCardGenerator()
        invalid_config = {
            "model_details": {
                # Missing required fields
                "name": "Test",
            }
        }
        with pytest.raises(ValueError):
            gen.validate_config(invalid_config)

    def test_generate_model_card_end_to_end(self):
        """Test end-to-end model card generation."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
model_details:
  name: Test Model
  version: 1.0.0
  owner: Test Org
intended_use:
  primary_use: Atrial fibrillation detection
  intended_users:
    - Cardiologists
  clinical_setting:
    - Hospital cardiology
factors: {}
metrics:
  overall:
    sensitivity: 0.92
    specificity: 0.94
evaluation_data:
  datasets:
    - Test cohort
training_data:
  datasets:
    - Training cohort
""")
            config_path = Path(f.name)

        # Generate model card
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "model_card.md"
            try:
                result = generate_model_card(config_path, output_path)
                assert result == output_path
                assert output_path.exists()

                # Verify content
                content = output_path.read_text()
                assert "Test Model" in content
                assert "1.0.0" in content
                assert "Atrial fibrillation detection" in content
                assert "Cardiologists" in content
            finally:
                config_path.unlink()

    def test_generate_model_card_with_fda_fields(self):
        """Test model card generation with FDA-specific fields."""
        config = {
            "model_details": {
                "name": "FDA Device",
                "version": "1.2.0",
                "owner": "Medical Corp",
            },
            "intended_use": {
                "primary_use": "AF detection",
                "intended_users": ["Cardiologists"],
                "clinical_setting": ["Hospital"],
                "contraindications": ["Pacemaker patients"],
            },
            "factors": {},
            "metrics": {
                "overall": {"sensitivity": 0.921, "specificity": 0.938},
            },
            "evaluation_data": {
                "datasets": ["External cohort"],
            },
            "training_data": {
                "datasets": ["Training cohort"],
                "sample_size": 200000,
            },
            "fda_specific": {
                "intended_use_statement": "AF detection from 12-lead ECG",
                "classification": "Class II; 510(k)",
                "predicate_devices": ["K232488"],
            },
        }

        gen = ModelCardGenerator()
        model_card = gen.validate_config(config)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "model_card.md"
            template = gen.env.get_template("model_card.md.j2")

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
            output_path.write_text(markdown)

            content = output_path.read_text()
            assert "FDA-Extended Model Card" in content
            assert "Medical Corp" in content
            assert "K232488" in content
            assert "Class II" in content

    def test_generate_from_example_yaml(self):
        """Test generating model card from provided example."""
        example_path = Path(__file__).parent.parent / "examples" / "model_card_ecg_classifier.yaml"

        if not example_path.exists():
            pytest.skip(f"Example file not found: {example_path}")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "ecg_classifier_model_card.md"
            result = generate_model_card(example_path, output_path)

            assert result == output_path
            assert output_path.exists()

            # Verify content contains expected sections
            content = output_path.read_text()
            assert "CardioDetect" in content
            assert "1.2.1" in content
            assert "Atrial fibrillation" in content
            assert "FDA-Specific" in content
            assert "K232488" in content
            assert "Metrics" in content
            assert "Subgroup Analysis" in content


class TestModelCardValidation:
    """Test validation of model card data."""

    def test_metrics_confidence_intervals(self):
        """Test that confidence intervals are properly formatted."""
        subgroup = MetricSubgroup(
            subgroup_name="Test Subgroup",
            subgroup_definition="Test definition",
            n_cases=1000,
            metrics={"sensitivity": 0.92},
            confidence_intervals={"sensitivity": (0.90, 0.94)},
        )
        assert subgroup.confidence_intervals["sensitivity"] == (0.90, 0.94)

    def test_ethical_considerations_completeness(self):
        """Test that ethical considerations can be fully specified."""
        ethical = EthicalConsiderations(
            impact_summary="Positive and negative impacts",
            potential_harms=["Missed diagnosis", "False positive"],
            demographic_disparities="4.2% disparity in Asian population",
            bias_mitigation_strategies=["Stratified analysis", "Transparency"],
            fairness_considerations="Model fairness evaluated",
        )
        assert len(ethical.potential_harms) == 2
        assert len(ethical.bias_mitigation_strategies) == 2

    def test_caveats_recommendations_completeness(self):
        """Test CaveatsRecommendations schema."""
        caveats = CaveatsRecommendations(
            caveats=["Limited data in Asian populations"],
            known_limitations=["Paroxysmal AF not present at ECG"],
            recommendations=["Always review original ECG", "Manual review if confidence <0.60"],
            future_improvements="Planned retraining with diverse data",
        )
        assert len(caveats.caveats) == 1
        assert len(caveats.recommendations) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
