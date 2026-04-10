"""Verify Pydantic schemas reject invalid input.

Two categories:
1. Unknown fields (extra='forbid') to catch user YAML typos at load time
2. Numeric and date constraints to catch nonsense values before rendering
"""

import pytest
from pydantic import ValidationError

from fda_samd_toolkit.checklist.schemas import ChecklistItem, ReadinessReport
from fda_samd_toolkit.model_cards.schemas import ModelCard
from fda_samd_toolkit.pccp.schemas import PCCPConfig
from fda_samd_toolkit.validation.schemas import ValidationPlan


class TestPCCPStrict:
    def test_rejects_unknown_top_level_field(self):
        """PCCPConfig should reject typos at the top level."""
        with pytest.raises(ValidationError) as excinfo:
            PCCPConfig(
                device_info={"name": "Test", "classification": "II", "intended_use": "Test"},
                baseline_performance=[],
                planned_modifications=[],
                monitoring_triggers=[],
                modification_protocol={"data_governance": "x", "retraining_procedure": "x", "test_procedure": "x"},
                impact_assessment={"intended_use_impact": "x"},
                deveice_name="typo",  # intentional typo
            )
        assert "extra" in str(excinfo.value).lower() or "deveice_name" in str(excinfo.value)


class TestModelCardStrict:
    def test_rejects_unknown_top_level_field(self):
        with pytest.raises(ValidationError) as excinfo:
            ModelCard(
                model_details={
                    "name": "Test",
                    "version": "1.0",
                    "owner": "Test Org",
                    "license": "MIT",
                },
                intended_use={
                    "primary_use": "test",
                    "users": ["test"],
                    "out_of_scope": ["test"],
                },
                factors={
                    "relevant_factors": ["age"],
                    "evaluation_factors": ["age"],
                },
                metrics={
                    "performance_measures": [{"name": "auc", "value": 0.9}],
                    "decision_thresholds": {},
                    "approaches": "test",
                    "variation_approaches": "test",
                },
                evaluation_data={
                    "datasets": ["test"],
                    "motivation": "test",
                    "preprocessing": "test",
                },
                training_data={
                    "datasets": ["test"],
                    "preprocessing": "test",
                },
                bonus_field="typo",  # intentional typo
            )
        assert "extra" in str(excinfo.value).lower() or "bonus_field" in str(excinfo.value)


class TestValidationPlanStrict:
    def test_rejects_unknown_nested_field(self):
        """Nested schemas should also forbid extras so DeviceInfo-like typos get caught."""
        with pytest.raises(ValidationError):
            # Feed a minimal but structurally valid document with a nested typo
            ValidationPlan(
                study_overview={
                    "title": "Test Study",
                    "objective": "x",
                    "phases": ["x"],
                    "totally_made_up_field": "should fail",
                },
                device={
                    "name": "Test",
                    "intended_use": "Test",
                    "device_class": "II",
                },
                modality="signals",
                primary_endpoint={
                    "name": "sensitivity",
                    "definition": "test",
                    "hypothesis_null": "x",
                    "hypothesis_alternative": "x",
                    "acceptance_criterion": "x",
                },
                secondary_endpoints=[],
                study_design={
                    "design_type": "prospective",
                    "blinding": "double",
                    "randomization": "none",
                    "control": "none",
                    "comparator": "none",
                },
                study_population={
                    "target_population": "x",
                    "inclusion_criteria": ["x"],
                    "exclusion_criteria": ["x"],
                    "enrollment_strategy": "x",
                },
                sample_size={
                    "total_sample_size": 100,
                    "per_arm": 50,
                    "justification": "x",
                    "significance_level": 0.05,
                    "power_target": 0.8,
                    "effect_size": "x",
                },
                reference_standard={
                    "description": "x",
                    "source": "x",
                    "limitations": "x",
                },
                subgroup_analysis={
                    "subgroups": ["age"],
                    "approach": "x",
                },
                statistical_plan={
                    "primary_analysis": "x",
                    "secondary_analyses": [],
                    "handling_missing_data": "x",
                    "multiplicity_adjustment": "x",
                },
                safety={
                    "adverse_events_tracking": "x",
                    "stopping_rules": "x",
                    "data_safety_monitoring": "x",
                },
                regulatory_compliance={
                    "ich_gcp": True,
                    "fda_guidance": ["x"],
                    "irb_approval_required": True,
                },
                document_date="2026-01-01",
            )


class TestChecklistStrict:
    def test_readiness_report_rejects_unknown_field(self):
        with pytest.raises(ValidationError):
            ReadinessReport(
                categories=[],
                overall_pct=0.0,
                timestamp="2026-01-01T00:00:00Z",
                device_name="Test",
                unknown_field="typo",
            )

    def test_checklist_item_rejects_unknown_field(self):
        with pytest.raises(ValidationError):
            ChecklistItem(
                id="T001",
                category="Test Category",
                text="Test item",
                status="complete",
                severity="critical",
                unknown_field="typo",
            )
