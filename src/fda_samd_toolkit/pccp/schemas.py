"""Pydantic v2 schemas for PCCP configuration and validation."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DeviceInfo(BaseModel):
    """Device identification and regulatory classification."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., description="Device name or brand name")
    manufacturer: str = Field(..., description="Manufacturer name")
    intended_use: str = Field(..., description="Intended use statement (IFU)")
    indications_for_use: str = Field(..., description="Indications for use")
    classification: str = Field(..., description="FDA classification (e.g., 'Class II', 'Class III')")
    predicate_device: str | None = Field(None, description="510(k) predicate device name (if applicable)")
    device_id: str | None = Field(None, description="FDA Device ID (if available)")


class PerformanceMetric(BaseModel):
    """A single performance metric to be monitored."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., description="Metric name (e.g., 'AUROC', 'Sensitivity')")
    description: str = Field(..., description="What this metric measures and why it matters")
    baseline_value: float = Field(..., description="Baseline value from development")
    threshold_warning: float = Field(..., description="Warning threshold (trigger for investigation)")
    threshold_action: float = Field(..., description="Action threshold (trigger for model retraining)")
    direction: str = Field(default="higher", description="'higher' or 'lower' for good performance")

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str) -> str:
        """Ensure direction is 'higher' or 'lower'."""
        if v.lower() not in ("higher", "lower"):
            raise ValueError("direction must be 'higher' or 'lower'")
        return v.lower()


class DataDriftMonitoring(BaseModel):
    """Data drift detection and response protocol."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    method: str = Field(..., description="Drift detection method (e.g., 'Statistical test', 'Distribution shift')")
    monitoring_frequency: str = Field(..., description="How often drift is checked (e.g., 'weekly', 'monthly')")
    threshold_description: str = Field(..., description="What constitutes actionable drift")
    response_protocol: str = Field(..., description="What happens when drift is detected")


class PlannedModification(BaseModel):
    """A single type of modification pre-approved under the PCCP."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    type: str = Field(
        ...,
        description="Modification type (e.g., 'Model Retraining', 'Data Expansion', 'Algorithm Change')",
    )
    description: str = Field(..., description="Detailed description of the modification")
    rationale: str = Field(..., description="Why this modification is planned")
    affected_performance_metrics: list[str] = Field(..., description="List of metric names that may be affected")
    frequency_cadence: str = Field(
        ..., description="How often this modification occurs (e.g., '6 months', 'quarterly')"
    )


class ModificationProtocol(BaseModel):
    """Protocol for implementing modifications under the PCCP."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    data_management: str = Field(
        ...,
        description="How data is collected, versioned, and managed for retraining",
    )
    data_quality_checks: str = Field(..., description="Quality assurance steps before retraining")
    retraining_methodology: str = Field(
        ..., description="Algorithm, loss function, hyperparameters, and training process"
    )
    validation_strategy: str = Field(
        ...,
        description="How the retrained model is validated (e.g., test set, cross-validation)",
    )
    validation_criteria: list[str] = Field(..., description="Specific criteria the model must meet before deployment")
    performance_thresholds: list[PerformanceMetric] = Field(
        ..., description="List of performance metrics with warning and action thresholds"
    )
    drift_monitoring: DataDriftMonitoring = Field(..., description="Data drift detection strategy")
    deployment_process: str = Field(..., description="How the validated model is deployed to production")


class RiskMitigation(BaseModel):
    """Mitigation strategy for a specific risk."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    risk: str = Field(..., description="Description of the risk")
    mitigation: str = Field(..., description="How this risk is mitigated")


class SubPopulationAnalysis(BaseModel):
    """Performance analysis for a specific sub-population."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., description="Sub-population identifier (e.g., 'Age 65+')")
    description: str = Field(..., description="Characteristics defining this sub-population")
    performance_expectations: str = Field(..., description="Expected model performance in this sub-population")
    monitoring_plan: str = Field(..., description="How performance will be monitored for this group")


class ImpactAssessment(BaseModel):
    """Assessment of planned modifications' impact on safety and efficacy."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    benefits: str = Field(
        ...,
        description="Benefits of planned modifications (improved performance, broader applicability, etc.)",
    )
    risks: str = Field(..., description="Potential risks introduced by modifications")
    risk_mitigations: list[RiskMitigation] = Field(..., description="Detailed mitigations for each identified risk")
    sub_population_analysis: list[SubPopulationAnalysis] = Field(
        ..., description="Performance analysis for relevant sub-populations"
    )
    monitoring_and_reporting: str = Field(
        ...,
        description="Post-market surveillance and reporting plan for modifications",
    )


class PCCPConfig(BaseModel):
    """Top-level PCCP configuration model."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    device_info: DeviceInfo = Field(..., description="Device identification and classification")
    planned_modifications: list[PlannedModification] = Field(..., description="List of pre-approved modifications")
    modification_protocol: ModificationProtocol = Field(
        ..., description="Detailed protocol for implementing modifications"
    )
    impact_assessment: ImpactAssessment = Field(..., description="Assessment of modification impacts")
    regulatory_compliance: str | None = Field(
        None,
        description="Statements about compliance with applicable regulations (21 CFR 11, etc.)",
    )
    version: str = Field(default="1.0", description="PCCP document version")
    effective_date: str | None = Field(None, description="Date PCCP becomes effective (ISO 8601 format: YYYY-MM-DD)")

    @field_validator("effective_date")
    @classmethod
    def validate_effective_date(cls, v: str | None) -> str | None:
        """Validate that effective_date is a well-formed ISO 8601 date."""
        if v is None:
            return v
        from datetime import datetime

        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"effective_date must be ISO 8601 format YYYY-MM-DD, got {v!r}") from e
        return v
