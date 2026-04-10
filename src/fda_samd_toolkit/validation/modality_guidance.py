"""Modality-specific validation guidance for different AI/ML data types."""

IMAGING_GUIDANCE = {
    "modality_name": "Medical Imaging",
    "description": "AI/ML applied to radiological images (X-ray, CT, MRI, ultrasound, etc.)",
    "key_considerations": [
        "DICOM standard compliance and image archiving practices",
        "Image acquisition protocols (scanner type, parameters, field of view)",
        "Image quality criteria and preprocessing steps (anonymization, standardization)",
        "Reader study design for reference standard (number of radiologists, experience level)",
        "Pixel-level versus region-of-interest labeling accuracy",
        "Handling of equivocal or borderline cases in adjudication",
    ],
    "data_source_guidance": (
        "Data should be obtained from clinical PACS systems with documented acquisition parameters. "
        "Ensure image quality metadata is captured (manufacturer, model, acquisition settings). "
        "Include multiple scanner types/vendors to assess generalization. "
        "Document any image preprocessing or filtering applied before AI inference."
    ),
    "reference_standard_guidance": (
        "Reference standard should be established by certified radiologists (ACR or equivalent certification). "
        "Use structured reporting templates (e.g., BIRADS for breast imaging). "
        "Employ 3-reader consensus or independent adjudication for equivocal cases. "
        "Target Cohen's kappa >= 0.75 for inter-rater reliability. "
        "Consider blinded re-review of borderline cases."
    ),
    "endpoint_guidance": (
        "Primary endpoint typically: sensitivity >= 0.90 and specificity >= 0.85 with 95% CI. "
        "Report performance stratified by disease severity, imaging type, and patient factors. "
        "Include ROC curves with comparison to radiologist performance where applicable."
    ),
    "statistical_guidance": (
        "Use DeLong test for comparing AUROC between AI and radiologists. "
        "Sample size calculation: n = (1.96 + 1.28)^2 * 2 * (0.5 - AUC_0) * (1 + AUC_0) / delta^2. "
        "Adjust for clustering if multiple images per patient. "
        "Stratify analysis by scanner type to assess device-independence."
    ),
    "subgroup_guidance": (
        "Stratify by sex, age group (e.g., <50, 50-65, >65), and ethnicity. "
        "Analyze performance by disease severity category (benign, malignant, indeterminate). "
        "Report metrics separately for single-image and multi-image studies if applicable."
    ),
    "safety_guidance": (
        "False positive: unnecessary additional imaging, biopsies, or patient anxiety. "
        "False negative: delayed diagnosis or missed pathology. "
        "Include plan for radiologist alert/override of AI predictions. "
        "Define workflow integration and clinician decision support messaging."
    ),
    "external_validation_guidance": (
        "Conduct external validation at geographically distinct site with different scanner vendors/models. "
        "Assess temporal generalization on images acquired >6 months after training data. "
        "Evaluate performance across different imaging protocols and post-processing parameters."
    ),
}

SIGNALS_GUIDANCE = {
    "modality_name": "Physiological Signals",
    "description": "AI/ML applied to time-series signals (ECG, EEG, PPG, respiration, etc.)",
    "key_considerations": [
        "Signal sampling rate and duration requirements",
        "Lead configuration (ECG: 12-lead vs 1-lead, EEG: number and placement of electrodes)",
        "Signal quality criteria (noise thresholds, artifact handling, baseline wander)",
        "QC procedures for signal preprocessing (filtering, normalization, artifact removal)",
        "Handling of signals with motion artifacts, noise, or missing segments",
        "Temporal aspect: windowing strategy and overlap for inference",
    ],
    "data_source_guidance": (
        "Data should be obtained from clinical monitoring systems (Holter, ICU monitors, wearables) with "
        "documented equipment type, firmware version, and sampling specifications. "
        "Include multiple device manufacturers to assess hardware independence. "
        "Capture full signal metadata: lead configuration, sampling rate, filter settings, gain. "
        "Document time-of-day and patient state during recording (resting, exercise, sleep, etc.)."
    ),
    "reference_standard_guidance": (
        "Reference standard established by board-certified cardiologists/neurologists with subspecialty training. "
        "For ECG: use serial tracings, clinical correlation, and when needed, EP study or imaging confirmation. "
        "For EEG: use structured scoring systems (e.g., IFSECN classification). "
        "Use 3-reader consensus for equivocal arrhythmias/abnormalities. "
        "Target inter-rater reliability (Cohen's kappa or ICC2,k) >= 0.80."
    ),
    "endpoint_guidance": (
        "Primary endpoint: sensitivity >= 0.90 and specificity >= 0.95 for target arrhythmia/abnormality. "
        "Report both on per-beat and per-episode level (for continuous monitoring). "
        "Include positive/negative predictive value for typical patient prevalence. "
        "For multi-class arrhythmias: report macro and weighted averages."
    ),
    "statistical_guidance": (
        "Account for within-subject correlation (multiple signals per patient). "
        "Use mixed-effects models or GEE for clustered analysis if applicable. "
        "Sample size: n = [z_alpha + z_beta]^2 * (Se * (1-Se) + Sp * (1-Sp)) / (Se + Sp - 1)^2. "
        "Stratify by device type, lead configuration, and signal quality metrics. "
        "Assess performance across different sampling rates if device-agnostic."
    ),
    "subgroup_guidance": (
        "Stratify by sex, age (<40, 40-65, >65), and heart rate/baseline rhythm. "
        "Analyze performance by signal quality (noise level, artifact percentage). "
        "Report metrics separately for different device manufacturers if multi-device study. "
        "Include stratification by comorbidities (structural heart disease, electrolyte abnormalities, medications)."
    ),
    "safety_guidance": (
        "False positive: unnecessary interventions (medication changes, device implant), patient anxiety. "
        "False negative: missed life-threatening arrhythmia (syncope, sudden cardiac death risk). "
        "Plan for human review of borderline predictions; define confidence thresholds for alert escalation. "
        "Include panic value thresholds for immediately actionable findings."
    ),
    "external_validation_guidance": (
        "External validation with different device manufacturer (different signal conditioning). "
        "Test on different lead configurations if applicable (12-lead trained, evaluate on 3-lead). "
        "Temporal validation: assess performance drift over >1 year post-market. "
        "Include subjects with known arrhythmias and asymptomatic individuals."
    ),
}

NLP_GUIDANCE = {
    "modality_name": "Natural Language Processing",
    "description": "AI/ML applied to clinical text (notes, reports, literature, etc.)",
    "key_considerations": [
        "Corpus composition and representativeness (note type, specialty, time period)",
        "Annotation protocol and inter-annotator agreement methodology",
        "Handling of ambiguous, contradictory, or incomplete clinical narratives",
        "De-identification quality assurance to protect patient privacy",
        "Bias evaluation for demographic characteristics (age, sex, race, language, comorbidities)",
        "Evaluation of performance on edge cases (rare conditions, complex cases, multiple languages)",
    ],
    "data_source_guidance": (
        "Clinical text should come from EHR systems with documented note types and specialties. "
        "Ensure diversity of providers (different hospitals, vendors, specialties, geographic regions). "
        "Include text from different time periods (>2 years span) to assess temporal generalization. "
        "Document any preprocessing: tokenization, stemming, removal of structured fields (patient identifiers). "
        "Preserve demographic information for bias analysis (race, ethnicity, language, age, sex)."
    ),
    "reference_standard_guidance": (
        "Reference standard established by clinical experts with demonstrated expertise in target domain "
        "(e.g., infectious disease specialists for sepsis detection in clinical notes). "
        "Use detailed annotation guidelines with clear examples and decision rules. "
        "Require annotator training and certification with >95% agreement on reference cases before annotation. "
        "Use inter-annotator agreement metrics: Fleiss kappa >= 0.80 or ICC >= 0.80. "
        "Employ adjudication process for disagreements; do not use majority vote."
    ),
    "endpoint_guidance": (
        "Primary endpoint: F1-score >= 0.85 (for token/span classification), "
        "or AUROC >= 0.90 (for document-level classification like sepsis prediction). "
        "Report per-class metrics, especially for imbalanced classes (rare conditions). "
        "Include error analysis: false positive and false negative examples with qualitative assessment. "
        "Report performance on both common and rare conditions proportional to clinical prevalence."
    ),
    "statistical_guidance": (
        "Macro-average metrics for multi-class tasks (equal weight to rare classes). "
        "Weighted-average metrics reflecting clinical prevalence. "
        "Sample size depends on task complexity and class imbalance; "
        "aim for >=100 examples per class per data partition. "
        "Stratify by note type, specialty, time period, and patient characteristics. "
        "Use stratified k-fold cross-validation (k=5 or higher) for smaller datasets."
    ),
    "subgroup_guidance": (
        "Stratify by demographics: age, sex, race/ethnicity, language, and comorbidity burden. "
        "Analyze performance by note type (progress notes vs. consultation vs. discharge summary). "
        "Report metrics by provider specialty and experience level if available. "
        "Assess performance on cases with high semantic complexity, ambiguity, or negation. "
        "Include fairness assessment: evaluate whether performance disparities exist for protected attributes."
    ),
    "safety_guidance": (
        "False positive: triggering unnecessary clinical action, alert fatigue, unnecessary treatment. "
        "False negative: missed diagnosis or delayed intervention for serious conditions. "
        "Evaluate risk of systematic bias (e.g., model more sensitive for certain demographic groups). "
        "Plan for clinician review workflow; define when human override is necessary. "
        "Consider downstream impact: how will errors in NLP affect clinical decision-making?"
    ),
    "external_validation_guidance": (
        "External validation with data from different EHR vendor (different note structures, vocabularies). "
        "Evaluate on text from non-English speakers if multilingual capability intended. "
        "Temporal validation: assess on notes written >1 year after training data cutoff. "
        "Include data from different healthcare systems (academic, community, pediatric if applicable). "
        "Test on complex, unusual, or borderline cases that may reveal model failure modes."
    ),
}

MULTIMODAL_GUIDANCE = {
    "modality_name": "Multimodal",
    "description": "AI/ML integrating multiple data types (images + signals, text + images, etc.)",
    "key_considerations": [
        "Alignment and synchronization of different data modalities (temporal, spatial)",
        "Handling of missing modalities (what if image is unavailable but signal is not?)",
        "Relative weighting of different modalities and feature importance assessment",
        "Complexity of multimodal fusion strategy (early fusion vs. late fusion vs. ensemble)",
        "Cross-modality consistency checks and conflict resolution when modalities disagree",
        "Validation of each modality separately and combined to isolate contribution",
    ],
    "data_source_guidance": (
        "Ensure balanced data across all modalities (minimize missingness). "
        "Document modality-specific collection protocols (e.g., ECG + echo recorded simultaneously). "
        "Record temporal relationships between acquisitions if they are not simultaneous. "
        "Include cases where one modality is higher quality than another (real-world scenario). "
        "Maintain modality metadata separately (e.g., imaging parameters and signal characteristics)."
    ),
    "reference_standard_guidance": (
        "Reference standard should integrate information from all clinically relevant modalities "
        "(don't establish ground truth from imaging alone if signals are clinically important). "
        "Use multimodal adjudication when modalities provide conflicting information. "
        "Define hierarchy: which modality takes precedence if multimodal data disagree? "
        "Ensure all adjudicators have expertise in interpreting all included modalities. "
        "Report inter-rater reliability separately for single-modality vs. multimodal assessment."
    ),
    "endpoint_guidance": (
        "Primary endpoint: metric on combined modality (e.g., AUROC with both imaging and ECG). "
        "Report performance when each modality is present individually. "
        "Report incremental improvement: AUC(modality A) vs. AUC(modality A + B). "
        "Analyze: which modality combination is necessary/sufficient for clinical decision? "
        "Include scenario: if one modality is missing, does performance degrade acceptably?"
    ),
    "statistical_guidance": (
        "Use multivariate analysis to assess relative importance of each modality. "
        "Consider interaction effects: does benefit of modality A depend on quality of modality B? "
        "If sample sizes vary by modality (e.g., 50% missing image data), "
        "use sensitivity analysis with and without the modality. "
        "Stratify by completeness: full data vs. single modality missing."
    ),
    "subgroup_guidance": (
        "Report stratified analysis by: all demographics (age, sex, race) and disease severity. "
        "Assess whether subgroups have differential reliance on different modalities "
        "(e.g., does pediatric population need different modality weighting?). "
        "Analyze performance in subgroups with lower data quality for one modality. "
        "Evaluate whether performance disparities are driven by one modality or consistent across modalities."
    ),
    "safety_guidance": (
        "Evaluate risk of each failure mode: false positives, false negatives, and conflicting predictions. "
        "Assess clinical impact when modalities strongly disagree (algorithm gives different prediction "
        "from standard single-modality workflow). "
        "Plan for clinician review: when should multimodal AI prediction override standard workflow? "
        "Include fallback: if one modality is unreliable, can clinician revert to single-modality assessment?"
    ),
    "external_validation_guidance": (
        "External validation should include variation in modality devices/vendors (e.g., "
        "different ultrasound machines if multimodal includes echo). "
        "Assess temporal validation separately for each modality's data quality. "
        "Include sites where data collection differs (e.g., different imaging protocols). "
        "Test on real-world cases where one modality is suboptimal (patient motion, artifact, etc.)."
    ),
}


MODALITY_GUIDANCE = {
    "imaging": IMAGING_GUIDANCE,
    "signals": SIGNALS_GUIDANCE,
    "nlp": NLP_GUIDANCE,
    "multimodal": MULTIMODAL_GUIDANCE,
}


def get_modality_guidance(modality: str) -> dict:
    """Retrieve modality-specific guidance."""
    modality = modality.lower()
    if modality not in MODALITY_GUIDANCE:
        raise ValueError(
            f"Unknown modality '{modality}'. Valid options: {', '.join(MODALITY_GUIDANCE.keys())}"
        )
    return MODALITY_GUIDANCE[modality]
