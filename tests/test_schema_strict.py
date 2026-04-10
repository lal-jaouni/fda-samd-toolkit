"""Verify Pydantic schemas reject unknown fields (extra='forbid').

This catches user YAML typos at validation time instead of silently dropping
the typoed field and producing a submission with missing data.

Note: all tests use model_validate() with dicts rather than keyword
constructors. The intent is to feed deliberately invalid input, which the
kwarg form would cause pyright to (correctly) complain about at type-check
time.
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
            PCCPConfig.model_validate(
                {
                    "device_info": {
                        "name": "Test",
                        "manufacturer": "Test Co",
                        "intended_use": "Test",
                        "indications_for_use": "Test",
                        "classification": "Class II",
                    },
                    "planned_modifications": [],
                    "modification_protocol": {
                        "data_management": "x",
                        "data_quality_checks": "x",
                        "retraining_methodology": "x",
                        "performance_testing": "x",
                        "drift_monitoring": {
                            "method": "x",
                            "monitoring_frequency": "x",
                            "threshold_description": "x",
                            "response_protocol": "x",
                        },
                        "deployment_process": "x",
                    },
                    "impact_assessment": {
                        "benefits": "x",
                        "risks": "x",
                        "risk_mitigations": [],
                        "sub_population_analysis": [],
                        "post_market_surveillance": "x",
                    },
                    "deveice_name": "typo",
                }
            )
        msg = str(excinfo.value).lower()
        assert "extra" in msg or "deveice_name" in msg


class TestModelCardStrict:
    def test_rejects_unknown_top_level_field(self):
        with pytest.raises(ValidationError) as excinfo:
            ModelCard.model_validate(
                {
                    "model_details": {
                        "name": "Test",
                        "version": "1.0",
                        "owner": "Test Org",
                        "license": "MIT",
                    },
                    "intended_use": {
                        "primary_use": "test",
                        "users": ["test"],
                        "out_of_scope": ["test"],
                    },
                    "factors": {
                        "relevant_factors": ["age"],
                        "evaluation_factors": ["age"],
                    },
                    "metrics": {
                        "performance_measures": [{"name": "auc", "value": 0.9}],
                        "decision_thresholds": {},
                        "approaches": "test",
                        "variation_approaches": "test",
                    },
                    "evaluation_data": {
                        "datasets": ["test"],
                        "motivation": "test",
                        "preprocessing": "test",
                    },
                    "training_data": {
                        "datasets": ["test"],
                        "preprocessing": "test",
                    },
                    "bonus_field": "typo",
                }
            )
        msg = str(excinfo.value).lower()
        assert "extra" in msg or "bonus_field" in msg


class TestValidationPlanStrict:
    def test_rejects_unknown_top_level_field(self):
        """Top-level ValidationPlan should reject unknown fields."""
        with pytest.raises(ValidationError) as excinfo:
            ValidationPlan.model_validate(
                {
                    "device_name": "Test",
                    "intended_use": "Test",
                    "modality": "signals",
                    "document_date": "2026-01-01",
                    "made_up_field": "should fail",
                }
            )
        msg = str(excinfo.value).lower()
        assert "extra" in msg or "made_up_field" in msg


class TestChecklistStrict:
    def test_readiness_report_rejects_unknown_field(self):
        with pytest.raises(ValidationError):
            ReadinessReport.model_validate(
                {
                    "categories": [],
                    "overall_pct": 0.0,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "device_name": "Test",
                    "unknown_field": "typo",
                }
            )

    def test_checklist_item_rejects_unknown_field(self):
        with pytest.raises(ValidationError):
            ChecklistItem.model_validate(
                {
                    "id": "T001",
                    "category": "Test Category",
                    "requirement": "Test item",
                    "evidence_required": "Test evidence",
                    "standard_reference": "Test ref",
                    "status": "complete",
                    "severity": "critical",
                    "unknown_field": "typo",
                }
            )
