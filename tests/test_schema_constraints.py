"""Tests for numeric range and date format constraints on Pydantic schemas.

These constraints prevent nonsense values (like significance_level=2.5 or
document_date='2024-13-45') from rendering into regulatory documents.
"""

import pytest
from pydantic import ValidationError

from fda_samd_toolkit.pccp.schemas import PCCPConfig
from fda_samd_toolkit.validation.schemas import StatisticalAnalysisPlan


def _make_stat_plan(**overrides):
    """Build a StatisticalAnalysisPlan via model_validate to avoid pyright
    kwarg typing issues when exercising invalid values."""
    base: dict = {
        "primary_hypothesis": "H1: sensitivity >= 90%",
        "statistical_test": "Binomial test",
        "power_calculation_description": "Alpha 0.05, power 0.90, one-sided test",
        "multiplicity_correction": "Bonferroni",
        "missing_data_strategy": "Complete case analysis",
    }
    base.update(overrides)
    return StatisticalAnalysisPlan.model_validate(base)


class TestSignificanceLevelConstraint:
    def test_default_valid(self):
        plan = _make_stat_plan()
        assert plan.significance_level == 0.05

    def test_explicit_valid(self):
        plan = _make_stat_plan(significance_level=0.01)
        assert plan.significance_level == 0.01

    def test_rejects_zero(self):
        with pytest.raises(ValidationError) as excinfo:
            _make_stat_plan(significance_level=0.0)
        msg = str(excinfo.value).lower()
        assert "greater than" in msg or "gt" in msg

    def test_rejects_one(self):
        with pytest.raises(ValidationError):
            _make_stat_plan(significance_level=1.0)

    def test_rejects_above_one(self):
        with pytest.raises(ValidationError):
            _make_stat_plan(significance_level=2.5)

    def test_rejects_negative(self):
        with pytest.raises(ValidationError):
            _make_stat_plan(significance_level=-0.1)


class TestPowerTargetConstraint:
    def test_explicit_valid(self):
        plan = _make_stat_plan(power_target=0.80)
        assert plan.power_target == 0.80

    def test_rejects_zero(self):
        with pytest.raises(ValidationError):
            _make_stat_plan(power_target=0.0)

    def test_rejects_one(self):
        with pytest.raises(ValidationError):
            _make_stat_plan(power_target=1.0)

    def test_rejects_above_one(self):
        with pytest.raises(ValidationError):
            _make_stat_plan(power_target=1.5)


class TestPCCPEffectiveDate:
    """Verify PCCPConfig.effective_date is validated as ISO 8601 YYYY-MM-DD."""

    def test_rejects_impossible_date(self):
        """The field_validator should reject dates like 2024-13-45."""
        # Minimal kwargs that get past required-field validation, then trip the date check.
        # If the date validator is wired correctly, it fires regardless of other fields
        # being incomplete, because Pydantic validates each field independently.
        with pytest.raises(ValidationError) as excinfo:
            PCCPConfig.model_validate(
                {
                    "device_info": {
                        "name": "Test",
                        "classification": "Class II",
                        "intended_use": "Test",
                    },
                    "baseline_performance": [],
                    "planned_modifications": [],
                    "monitoring_triggers": [],
                    "modification_protocol": {
                        "data_governance": "x",
                        "retraining_procedure": "x",
                        "test_procedure": "x",
                    },
                    "impact_assessment": {"intended_use_impact": "x"},
                    "effective_date": "2024-13-45",
                }
            )
        # Find the date-specific validator message
        errors = excinfo.value.errors()
        date_errors = [e for e in errors if "effective_date" in str(e.get("loc", ""))]
        assert date_errors, f"Expected effective_date error, got: {errors}"
        # The message should mention ISO 8601 or YYYY-MM-DD
        msg = str(date_errors[0])
        assert "ISO 8601" in msg or "YYYY-MM-DD" in msg

    def test_rejects_word_format(self):
        with pytest.raises(ValidationError) as excinfo:
            PCCPConfig.model_validate(
                {
                    "device_info": {
                        "name": "Test",
                        "classification": "Class II",
                        "intended_use": "Test",
                    },
                    "baseline_performance": [],
                    "planned_modifications": [],
                    "monitoring_triggers": [],
                    "modification_protocol": {
                        "data_governance": "x",
                        "retraining_procedure": "x",
                        "test_procedure": "x",
                    },
                    "impact_assessment": {"intended_use_impact": "x"},
                    "effective_date": "January 15, 2026",
                }
            )
        errors = excinfo.value.errors()
        date_errors = [e for e in errors if "effective_date" in str(e.get("loc", ""))]
        assert date_errors


class TestValidationPlanDocumentDate:
    """Verify ValidationPlan.document_date is validated as ISO 8601 YYYY-MM-DD."""

    def test_rejects_impossible_date(self):
        from fda_samd_toolkit.validation.schemas import ValidationPlan

        with pytest.raises(ValidationError) as excinfo:
            ValidationPlan.model_validate(
                {
                    "device_name": "Test",
                    "intended_use": "Test",
                    "modality": "signals",
                    "document_date": "2024-13-45",
                }
            )
        errors = excinfo.value.errors()
        date_errors = [e for e in errors if "document_date" in str(e.get("loc", ""))]
        assert date_errors
        msg = str(date_errors[0])
        assert "ISO 8601" in msg or "YYYY-MM-DD" in msg
