"""Pydantic v2 schemas for clinical validation plans."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudyDesign(BaseModel):
    """Study design and methodology."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    type: str = Field(
        ...,
        description="Study design type: retrospective, prospective, or hybrid",
    )
    blinding: str = Field(
        ...,
        description="Blinding strategy: open, single-blinded, or double-blinded",
    )
    multi_site: bool = Field(
        default=False,
        description="Whether this is a multi-site study",
    )
    sites_count: int | None = Field(
        None,
        description="Number of participating sites (if multi-site)",
    )
    site_locations: list[str] | None = Field(
        None,
        description="Geographic locations or names of sites",
    )
    study_duration_months: int | None = Field(
        None,
        description="Planned study duration in months",
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Ensure study type is valid."""
        valid_types = {"retrospective", "prospective", "hybrid"}
        if v.lower() not in valid_types:
            raise ValueError(f"type must be one of {valid_types}, got '{v}'")
        return v.lower()

    @field_validator("blinding")
    @classmethod
    def validate_blinding(cls, v: str) -> str:
        """Ensure blinding is valid."""
        valid_blinding = {"open", "single-blinded", "double-blinded"}
        if v.lower() not in valid_blinding:
            raise ValueError(f"blinding must be one of {valid_blinding}, got '{v}'")
        return v.lower()


class DataSource(BaseModel):
    """Data source and eligibility criteria."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    sites: list[str] = Field(
        ...,
        description="List of data collection sites or databases",
    )
    time_period_start: str = Field(
        ...,
        description="Data collection start date (ISO 8601 format: YYYY-MM-DD)",
    )
    time_period_end: str = Field(
        ...,
        description="Data collection end date (ISO 8601 format: YYYY-MM-DD)",
    )
    inclusion_criteria: list[str] = Field(
        ...,
        description="List of inclusion criteria for subjects",
    )
    exclusion_criteria: list[str] = Field(
        ...,
        description="List of exclusion criteria for subjects",
    )
    sample_size: int = Field(
        ...,
        description="Total planned sample size",
    )
    sample_size_justification: str = Field(
        ...,
        description="Statistical justification for sample size (power analysis, precision, etc.)",
    )
    population_diversity: str | None = Field(
        None,
        description="Description of population diversity goals (e.g., sex, race, age distribution)",
    )


class ReferenceStandard(BaseModel):
    """Gold standard and adjudication process."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    gold_standard: str = Field(
        ...,
        description="Description of the gold standard or reference diagnosis",
    )
    reference_source: str = Field(
        ...,
        description="Source of reference standard (clinical diagnosis, biopsy, other gold standard)",
    )
    adjudication_process: str = Field(
        ...,
        description="Process for adjudication if initial assessment is unclear",
    )
    adjudicator_qualifications: str = Field(
        ...,
        description="Required qualifications of adjudicators (e.g., board certification, years of experience)",
    )
    number_of_adjudicators: int = Field(
        ...,
        description="Number of adjudicators for reference standard assessment",
    )
    inter_rater_reliability_target: float = Field(
        ...,
        description="Target inter-rater reliability (Cohen's kappa or ICC)",
    )
    inter_rater_reliability_method: str = Field(
        ...,
        description="Method for assessing inter-rater reliability (Cohen's kappa, Fleiss kappa, ICC, etc.)",
    )


class Endpoints(BaseModel):
    """Primary and secondary endpoints."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    primary_endpoint: str = Field(
        ...,
        description="Primary efficacy endpoint definition and measurement",
    )
    primary_endpoint_target: str = Field(
        ...,
        description="Target performance for primary endpoint (e.g., AUROC > 0.90)",
    )
    secondary_endpoints: list[str] = Field(
        default_factory=list,
        description="List of secondary endpoints",
    )
    sensitivity_target: float | None = Field(
        None,
        description="Target sensitivity (true positive rate) if applicable",
    )
    specificity_target: float | None = Field(
        None,
        description="Target specificity (true negative rate) if applicable",
    )
    sensitivity_lower_ci: float | None = Field(
        None,
        description="Required lower bound of confidence interval for sensitivity",
    )
    specificity_lower_ci: float | None = Field(
        None,
        description="Required lower bound of confidence interval for specificity",
    )
    positive_predictive_value_target: float | None = Field(
        None,
        description="Target positive predictive value if applicable",
    )
    negative_predictive_value_target: float | None = Field(
        None,
        description="Target negative predictive value if applicable",
    )


class StatisticalAnalysisPlan(BaseModel):
    """Statistical analysis approach."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    primary_hypothesis: str = Field(
        ...,
        description="Primary statistical hypothesis to be tested",
    )
    statistical_test: str = Field(
        ...,
        description="Statistical test to be used (e.g., DeLong test for AUC comparison)",
    )
    significance_level: float = Field(
        default=0.05,
        gt=0.0,
        lt=1.0,
        description="Significance level (alpha) for hypothesis tests (0 < alpha < 1)",
    )
    power_target: float = Field(
        default=0.90,
        gt=0.0,
        lt=1.0,
        description="Target statistical power for primary endpoint (0 < power < 1)",
    )
    power_calculation_description: str = Field(
        ...,
        description="Description of power calculation methodology and assumptions",
    )
    multiplicity_correction: str = Field(
        ...,
        description="Method for correcting for multiple comparisons if applicable (Bonferroni, Holm, none, etc.)",
    )
    missing_data_strategy: str = Field(
        ...,
        description="Strategy for handling missing data (complete case, imputation method, etc.)",
    )
    sensitivity_analyses: list[str] | None = Field(
        None,
        description="Planned sensitivity analyses to assess robustness of findings",
    )


class SubgroupAnalysis(BaseModel):
    """Sub-population analysis plan."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    subgroups: list[str] = Field(
        ...,
        description="List of sub-populations to analyze (e.g., 'Sex: Male/Female', 'Age: <65 vs >=65')",
    )
    stratification_variables: list[str] = Field(
        ...,
        description="Variables used for stratification in randomization if applicable",
    )
    performance_target_by_subgroup: dict | None = Field(
        None,
        description="Performance targets for each subgroup (key: subgroup name, value: target metric)",
    )
    minority_representation: str | None = Field(
        None,
        description="Strategy for ensuring adequate representation of historically underrepresented groups",
    )
    differential_performance_analysis: str | None = Field(
        None,
        description="Plan for analyzing differences in model performance across subgroups",
    )


class GeneralizationTesting(BaseModel):
    """External validation and temporal generalization."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    external_validation_sites: list[str] | None = Field(
        None,
        description="External sites for holdout validation (geographically or organizationally distinct)",
    )
    external_validation_sample_size: int | None = Field(
        None,
        description="Sample size for external validation",
    )
    external_validation_timeline: str | None = Field(
        None,
        description="When external validation will be performed (during pilot, pre-submission, post-approval, etc.)",
    )
    temporal_validation_plan: str | None = Field(
        None,
        description="Plan for assessing model performance on data from different time periods",
    )
    data_drift_monitoring: str | None = Field(
        None,
        description="Strategy for detecting and responding to data drift post-market",
    )
    geographic_generalization_plan: str | None = Field(
        None,
        description="Plan for assessing generalization across geographic regions and healthcare systems",
    )


class SafetyMonitoring(BaseModel):
    """Safety and adverse event monitoring."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    adverse_event_definition: str = Field(
        ...,
        description="Definition of adverse events relevant to this AI/ML device",
    )
    serious_adverse_event_definition: str = Field(
        ...,
        description="Definition of serious adverse events",
    )
    adverse_event_monitoring_plan: str = Field(
        ...,
        description="Plan for prospective monitoring of adverse events during study",
    )
    safety_stopping_rules: str | None = Field(
        None,
        description="Pre-specified stopping rules based on safety (e.g., if SAE rate exceeds X%)",
    )
    false_positive_impact_assessment: str | None = Field(
        None,
        description="Assessment of clinical impact of false positives (unnecessary follow-up, harm, cost)",
    )
    false_negative_impact_assessment: str | None = Field(
        None,
        description="Assessment of clinical impact of false negatives (missed diagnosis, delay in treatment)",
    )


class ValidationPlan(BaseModel):
    """Top-level clinical validation plan."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    device_name: str = Field(
        ...,
        description="Name of the AI/ML device being validated",
    )
    intended_use: str = Field(
        ...,
        description="Intended use statement for the device",
    )
    modality: str = Field(
        ...,
        description="Data modality: imaging, signals, nlp, or multimodal",
    )
    document_version: str = Field(
        default="1.0",
        description="Document version",
    )
    document_date: str = Field(
        ...,
        description="Date of validation plan (ISO 8601 format: YYYY-MM-DD)",
    )
    study_design: StudyDesign = Field(
        ...,
        description="Study design and methodology",
    )
    data_source: DataSource = Field(
        ...,
        description="Data source and eligibility criteria",
    )
    reference_standard: ReferenceStandard = Field(
        ...,
        description="Gold standard and adjudication process",
    )
    endpoints: Endpoints = Field(
        ...,
        description="Primary and secondary endpoints",
    )
    statistical_analysis_plan: StatisticalAnalysisPlan = Field(
        ...,
        description="Statistical analysis approach",
    )
    subgroup_analysis: SubgroupAnalysis | None = Field(
        None,
        description="Sub-population analysis plan",
    )
    generalization_testing: GeneralizationTesting | None = Field(
        None,
        description="External validation and temporal generalization",
    )
    safety_monitoring: SafetyMonitoring | None = Field(
        None,
        description="Safety and adverse event monitoring",
    )
    regulatory_references: list[str] | None = Field(
        None,
        description="List of FDA guidance documents and regulatory references",
    )

    @field_validator("modality")
    @classmethod
    def validate_modality(cls, v: str) -> str:
        """Ensure modality is valid."""
        valid_modalities = {"imaging", "signals", "nlp", "multimodal"}
        if v.lower() not in valid_modalities:
            raise ValueError(f"modality must be one of {valid_modalities}, got '{v}'")
        return v.lower()

    @field_validator("document_date")
    @classmethod
    def validate_document_date(cls, v: str) -> str:
        """Validate that document_date is a well-formed ISO 8601 date."""
        from datetime import datetime

        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"document_date must be ISO 8601 format YYYY-MM-DD, got {v!r}") from e
        return v
