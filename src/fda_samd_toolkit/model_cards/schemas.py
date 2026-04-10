"""
Pydantic v2 schemas for FDA-extended model cards.

Extends Mitchell et al. 2019 model cards (https://arxiv.org/abs/1810.03993)
with FDA-specific fields for medical device submissions.

All schemas use Pydantic v2 with strict validation.
"""

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ModelDetails(BaseModel):
    """Basic metadata about the model."""

    name: str = Field(..., description="Name of the model")
    version: str = Field(..., description="Semantic version (e.g., 1.2.3)")
    owner: str = Field(..., description="Organization or individual responsible for the model")
    license: str = Field("MIT", description="License governing model use and distribution")
    citation: str | None = Field(None, description="BibTeX citation if model is published")
    contact: str | None = Field(None, description="Email or contact information for questions")
    release_date: date | None = Field(None, description="Date model was released")


class IntendedUse(BaseModel):
    """Describes the intended clinical use."""

    primary_use: str = Field(
        ...,
        description="Primary clinical purpose (e.g., 'Atrial fibrillation detection from 12-lead ECG')",
    )
    intended_users: list[str] = Field(
        ...,
        description="Types of users (e.g., ['Cardiologists', 'Emergency medicine physicians'])",
    )
    clinical_setting: list[str] = Field(
        ...,
        description="Approved clinical settings (e.g., ['Hospital cardiology', 'Emergency department'])",
    )
    contraindications: list[str] = Field(
        default=[],
        description="Populations or conditions where device should NOT be used",
    )
    out_of_scope_uses: list[str] = Field(
        default=[],
        description="Explicitly prohibited uses (e.g., 'Unsupervised home use', 'Pediatric patients')",
    )


class Factors(BaseModel):
    """Factors affecting model performance."""

    instrumentation: list[str] = Field(
        default=[],
        description="Equipment/hardware used (e.g., 'GE MAC 5500 ECG machine', 'NVIDIA T4 GPU')",
    )
    environment: dict[str, Any] = Field(
        default={},
        description="Environmental factors (e.g., {'temperature': '15-25C', 'humidity': '<80%'})",
    )
    demographic_groups_evaluated: list[str] = Field(
        default=[],
        description="Demographic categories analyzed (e.g., ['sex', 'age', 'race', 'disease_severity'])",
    )
    datasets_used: list[str] = Field(default=[], description="Datasets used for evaluation (names/identifiers)")


class MetricSubgroup(BaseModel):
    """Performance metrics for a specific subgroup."""

    subgroup_name: str = Field(..., description="Name of subgroup (e.g., 'Female, age 45-65')")
    subgroup_definition: str = Field(..., description="Definition of subgroup membership criteria")
    n_cases: int = Field(..., description="Number of cases in this subgroup")
    metrics: dict[str, float] = Field(
        ...,
        description="Performance metrics for this subgroup (e.g., {'sensitivity': 0.92, 'specificity': 0.94})",
    )
    confidence_intervals: dict[str, tuple] | None = Field(
        None,
        description="95% confidence intervals for metrics (e.g., {'sensitivity': [0.90, 0.94]})",
    )


class Metrics(BaseModel):
    """Performance metrics overall and by subgroup."""

    overall: dict[str, float] = Field(
        ...,
        description="Overall performance metrics (e.g., {'sensitivity': 0.92, 'specificity': 0.94, 'auc_roc': 0.941})",
    )
    overall_confidence_intervals: dict[str, tuple] | None = Field(None, description="95% CIs for overall metrics")
    subgroups: list[MetricSubgroup] = Field(default=[], description="Metrics broken down by demographic subgroups")
    threshold_used: float | None = Field(
        None, description="Decision threshold for binary classification (e.g., 0.5 probability)"
    )
    notes: str | None = Field(None, description="Additional notes on metrics calculation")


class EvaluationData(BaseModel):
    """Data used for evaluation/testing."""

    datasets: list[str] = Field(
        ...,
        description="Evaluation dataset names and sources (e.g., 'Mayo Clinic external validation cohort, 2023')",
    )
    motivation: str | None = Field(
        None,
        description="Why these specific datasets were chosen for evaluation",
    )
    preprocessing: list[str] | None = Field(
        None,
        description="Preprocessing applied to evaluation data (e.g., 'Butterworth 0.5-100 Hz filter', 'z-score normalization')",
    )
    test_train_split: dict[str, float] | None = Field(
        None, description="Data split ratios (e.g., {'train': 0.8, 'val': 0.1, 'test': 0.1})"
    )
    stratification: list[str] | None = Field(
        None,
        description="How data was stratified (e.g., 'stratified by diagnosis and site')",
    )


class TrainingData(BaseModel):
    """Data used for training the model."""

    datasets: list[str] = Field(
        ...,
        description="Training dataset names and sources (e.g., 'Mayo, Cleveland, Johns Hopkins ECG databases')",
    )
    sample_size: int | None = Field(None, description="Total number of training examples")
    demographics: dict[str, Any] | None = Field(
        None,
        description="Demographic breakdown of training data (e.g., {'mean_age': 67, 'female_pct': 42, 'caucasian_pct': 82})",
    )
    data_sources: list[str] | None = Field(
        None, description="Specific data sources (e.g., ['EHR database', 'Hospital ECG system'])"
    )
    inclusion_criteria: list[str] | None = Field(None, description="Inclusion criteria for training data")
    exclusion_criteria: list[str] | None = Field(None, description="Exclusion criteria for training data")
    quality_control: list[str] | None = Field(
        None,
        description="QC processes applied (e.g., 'Inter-rater agreement verification (kappa=0.89)', 'Automated artifact detection')",
    )
    data_shifts_addressed: list[str] | None = Field(
        None,
        description="Known data distribution shifts and how they were handled (e.g., 'Class imbalance addressed via class weights')",
    )


class QuantitativeAnalyses(BaseModel):
    """Unitary and intersectional results."""

    unitary_results: dict[str, Any] | None = Field(
        None,
        description="Results across single factors (e.g., {'sensitivity_by_age': {...}})",
    )
    intersectional_results: dict[str, Any] | None = Field(
        None,
        description="Results across intersecting factors (e.g., {'sensitivity_female_over_65': 0.94})",
    )


class EthicalConsiderations(BaseModel):
    """Ethical considerations and potential harms."""

    impact_summary: str | None = Field(
        None,
        description="Summary of potential positive and negative impacts",
    )
    potential_harms: list[str] = Field(
        default=[],
        description="Potential harms if model fails or is misused (e.g., 'Missed AF diagnosis leading to stroke')",
    )
    demographic_disparities: str | None = Field(
        None,
        description="Known or suspected performance disparities across demographics and mitigation plans",
    )
    bias_mitigation_strategies: list[str] = Field(
        default=[],
        description="Strategies to mitigate identified biases (e.g., 'Stratified performance analysis', 'Planned data augmentation for underrepresented populations')",
    )
    fairness_considerations: str | None = Field(None, description="Discussion of model fairness and equity")


class CaveatsRecommendations(BaseModel):
    """Caveats, recommendations, and limitations."""

    caveats: list[str] = Field(
        default=[],
        description="Important limitations and caveats (e.g., 'Performance not validated in pediatric populations')",
    )
    recommendations: list[str] = Field(
        default=[],
        description="Recommendations for use (e.g., 'Manual review recommended for confidence <0.60')",
    )
    known_limitations: list[str] = Field(
        default=[],
        description="Known failure modes (e.g., 'Sensitivity drops to 87% with extreme heart rates >120 BPM')",
    )
    future_improvements: str | None = Field(
        None,
        description="Planned improvements and retraining schedule",
    )


class FDASpecific(BaseModel):
    """FDA-specific fields for regulatory submissions."""

    intended_use_statement: str = Field(
        ...,
        description="Official IFU statement as it will appear on device labeling",
    )
    classification: str | None = Field(
        None,
        description="FDA classification (e.g., 'Class II') and regulatory pathway (e.g., '510(k) premarket submission')",
    )
    predicate_devices: list[str] | None = Field(
        None, description="510(k) predicate device K-numbers (e.g., 'K232488', 'K233429')"
    )
    substantial_equivalence_summary: str | None = Field(
        None,
        description="Brief summary of substantial equivalence rationale and predicate comparison",
    )
    drift_monitoring_plan: str | None = Field(
        None,
        description="Plan for monitoring model performance in deployed settings (e.g., 'Quarterly performance audits; alert if sensitivity drops <85%')",
    )
    failure_modes: list[str] | None = Field(
        None,
        description="Identified failure modes and mitigations (e.g., 'Paroxysmal AF not present at time of ECG: Will miss if not electrically evident; mitigated by clinical workflow')",
    )
    update_cadence: str | None = Field(
        None,
        description="Schedule for model updates and retraining (e.g., 'Annual revalidation; retraining if sensitivity drops >5%')",
    )
    post_market_surveillance: str | None = Field(
        None,
        description="Post-market surveillance plan (e.g., 'MedWatch reporting for serious adverse events; adverse event email feedback mechanism')",
    )
    human_factors_summary: str | None = Field(
        None,
        description="Summary of human factors validation (e.g., 'Usability testing with 16 physicians; 15-minute training required')",
    )


class ModelCard(BaseModel):
    """FDA-extended model card combining Mitchell et al. 2019 with medical device specifics."""

    model_details: ModelDetails = Field(..., description="Basic model metadata")
    intended_use: IntendedUse = Field(..., description="Intended clinical use")
    factors: Factors = Field(..., description="Factors affecting model performance")
    metrics: Metrics = Field(..., description="Performance metrics overall and by subgroup")
    evaluation_data: EvaluationData = Field(..., description="Evaluation/test data characterization")
    training_data: TrainingData = Field(..., description="Training data characterization")
    quantitative_analyses: QuantitativeAnalyses | None = Field(None, description="Additional quantitative analyses")
    ethical_considerations: EthicalConsiderations | None = Field(
        None, description="Ethical considerations and potential harms"
    )
    caveats_recommendations: CaveatsRecommendations | None = Field(
        None, description="Caveats, limitations, and recommendations"
    )
    fda_specific: FDASpecific | None = Field(None, description="FDA-specific fields for regulatory submissions")

    model_config = ConfigDict(
        json_schema_extra={
            "title": "FDA-Extended Model Card",
            "description": "Model card extending Mitchell et al. 2019 with FDA medical device fields",
        }
    )


if __name__ == "__main__":
    # Example: Create a minimal model card
    card = ModelCard(
        model_details=ModelDetails(
            name="Example ECG AF Detector",
            version="1.0.0",
            owner="Example Hospital",
            license="MIT",
            citation=None,
            contact=None,
            release_date=None,
        ),
        intended_use=IntendedUse(
            primary_use="Detection of atrial fibrillation from 12-lead ECG",
            intended_users=["Cardiologists", "Emergency physicians"],
            clinical_setting=["Hospital cardiology", "Emergency department"],
        ),
        factors=Factors(
            instrumentation=["GE MAC 5500 ECG machine"],
            demographic_groups_evaluated=["sex", "age", "race"],
        ),
        metrics=Metrics(
            overall={"sensitivity": 0.92, "specificity": 0.94, "auc_roc": 0.9407},
            overall_confidence_intervals=None,
            threshold_used=None,
            notes=None,
        ),
        evaluation_data=EvaluationData(
            datasets=["Mayo Clinic validation cohort (n=5000)"],
            motivation=None,
            preprocessing=None,
            test_train_split=None,
            stratification=None,
        ),
        training_data=TrainingData(
            datasets=["Mayo, Cleveland, Johns Hopkins ECG databases"],
            sample_size=200000,
            demographics=None,
            data_sources=None,
            inclusion_criteria=None,
            exclusion_criteria=None,
            quality_control=None,
            data_shifts_addressed=None,
        ),
        quantitative_analyses=None,
        ethical_considerations=None,
        caveats_recommendations=None,
        fda_specific=None,
    )

    print("Model Card created successfully:")
    print(card.model_dump_json(indent=2)[:500] + "...")
