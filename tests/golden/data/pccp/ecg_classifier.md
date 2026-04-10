# Predetermined Change Control Plan (PCCP)
## Machine Learning-Enabled Medical Device

**Document Version:** 1.0
**Effective Date:** 2025-04-01
---

## Executive Summary

This Predetermined Change Control Plan (PCCP) describes the modifications that may be made to CardioDetect ECG Arrhythmia Classifier without requiring a new 510(k) submission to the U.S. Food and Drug Administration (FDA). The plan is established under the FDA's PCCP guidance for Machine Learning (ML)-enabled Medical Devices[^1] and specifies pre-approved modification types, implementation protocols, and performance monitoring requirements.

This PCCP enables faster iteration and improvement of CardioDetect ECG Arrhythmia Classifier while maintaining regulatory compliance and patient safety. All modifications implemented under this plan must strictly adhere to the protocols, thresholds, and monitoring requirements outlined herein.

---

## Section 1: Description of Modifications

### 1.1 Device Identification

**Device Name:** CardioDetect ECG Arrhythmia Classifier
**Manufacturer:** CardioAI Systems, Inc.
**Intended Use:** The CardioDetect ECG Arrhythmia Classifier is a software-as-a-medical-device (SaMD) intended to assist healthcare professionals in identifying supraventricular, ventricular, and normal rhythm patterns in 12-lead electrocardiogram (ECG) recordings. The device provides probability scores for each rhythm category to support clinical decision-making.
**Indications for Use:** The CardioDetect ECG Arrhythmia Classifier is indicated for use in hospital settings to analyze 12-lead ECG recordings from adult patients (age 18+) presenting with suspected arrhythmias. The device is intended for use by trained healthcare professionals and is not a replacement for clinical judgment or standard diagnostic procedures.
**FDA Classification:** Class II
**Predicate Device(s):** Philips ECG Analysis Software (K123456)**FDA Device ID:** 3004521089
### 1.2 Overview of Planned Modifications

The following types of modifications are pre-approved under this PCCP. All modifications must be implemented in accordance with the protocols specified in Section 2.

| Modification Type | Frequency | Affected Metrics | Rationale |
|---|---|---|---|
| Model Retraining | Every 6 months or when drift threshold exceeded | AUROC (Supraventricular), AUROC (Ventricular), Sensitivity (Ventricular), Specificity (Ventricular), PPV (Positive Predictive Value) | New ECG data from diverse patient populations may contain previously unrepresented rhythm... |
| Data Expansion | Every 12 months, subject to data availability | AUROC (Supraventricular), AUROC (Ventricular), Demographic parity metrics, PPV variance across age groups | Expanding data sources improves demographic balance and reduces algorithmic bias. Wider... |
| Hyperparameter Optimization | Every 6 months during retraining cycles | AUROC (Supraventricular), AUROC (Ventricular), Validation loss | Hyperparameter tuning can improve convergence and prevent overfitting on updated datasets... |

### 1.3 Detailed Modification Descriptions

#### 1.3.1 Model Retraining

**Description:** Periodic retraining of the deep learning classifier on newly collected ECG data to maintain or improve sensitivity and specificity for arrhythmia detection. The model architecture (ResNet-50 with bidirectional LSTM) remains fixed; only weights are updated. Retraining occurs every 6 months or when performance drift exceeds specified thresholds.

**Rationale:** New ECG data from diverse patient populations may contain previously unrepresented rhythm patterns or demographic characteristics. Periodic retraining with balanced datasets improves model robustness and ensures sustained clinical performance across changing populations.

**Affected Performance Metrics:**
- AUROC (Supraventricular)
- AUROC (Ventricular)
- Sensitivity (Ventricular)
- Specificity (Ventricular)
- PPV (Positive Predictive Value)

**Frequency:** Every 6 months or when drift threshold exceeded

#### 1.3.2 Data Expansion

**Description:** Incorporation of ECG signals from additional hospital systems and patient demographics into the training dataset. This includes representation from different ECG machines (GE Healthcare, Schiller, Mortara) and patient populations across age groups, sex, and comorbidity profiles.

**Rationale:** Expanding data sources improves demographic balance and reduces algorithmic bias. Wider representation enables the model to generalize better to diverse clinical settings.

**Affected Performance Metrics:**
- AUROC (Supraventricular)
- AUROC (Ventricular)
- Demographic parity metrics
- PPV variance across age groups

**Frequency:** Every 12 months, subject to data availability

#### 1.3.3 Hyperparameter Optimization

**Description:** Adjustment of learning rate, batch size, dropout rates, and regularization parameters within pre-defined ranges. Optimization is performed using validation set performance. Architecture and algorithm remain unchanged.

**Rationale:** Hyperparameter tuning can improve convergence and prevent overfitting on updated datasets without changing the fundamental model structure.

**Affected Performance Metrics:**
- AUROC (Supraventricular)
- AUROC (Ventricular)
- Validation loss

**Frequency:** Every 6 months during retraining cycles


---

## Section 2: Modification Protocol

This section details the procedural requirements for implementing any modification covered by this PCCP. Adherence to these protocols is mandatory for regulatory compliance.

### 2.1 Data Management

ECG data is collected from hospital electronic health record (EHR) systems via HL7 FHIR API endpoints and stored in a HIPAA-compliant, access-controlled database. All patient identifiers are removed and replaced with de-identified tokens. Each dataset is versioned with a unique identifier including date and source. Data is validated for completeness (all 12 leads present, signal quality >95%) before inclusion in training sets. Records of all data versions, sources, and inclusion/exclusion criteria are maintained for audit trails.

### 2.2 Data Quality Assurance

The following data quality checks must be performed before any retraining:

Before any retraining, the following quality checks are mandatory: (1) Signal integrity: verify all 12 leads present with sampling rate 500 Hz; (2) Artifact detection: exclude records with baseline wander or electrode noise exceeding 5mV; (3) Label validity: confirm manual rhythm annotations from board-certified cardiologists; (4) Class balance: verify training set contains at least 25% each of supraventricular, ventricular, and normal rhythm classes; (5) Patient diversity: ensure representation across age (18-85), sex (male/female), and presence of known comorbidities; (6) Temporal distribution: confirm data collected across at least 12 months to capture seasonal variation.

### 2.3 Retraining Methodology

The model retraining process follows these specifications:

The model is retrained using a ResNet-50 backbone pre-trained on ImageNet, followed by a bidirectional LSTM layer (256 hidden units) for temporal sequence modeling. Input: 12-lead ECG signals at 500 Hz, normalized to zero mean and unit variance. The architecture processes each heartbeat window (2.5 seconds, 1,250 samples) independently. Loss function: weighted cross-entropy to account for class imbalance. Optimizer: Adam with learning rate 1e-4, weight decay 1e-5. Batch size: 32. Training for maximum 50 epochs with early stopping (patience=5 on validation AUROC). Hardware: NVIDIA GPU (A100 or equivalent). Training reproducibility ensured via fixed random seeds (numpy, torch, tf).

### 2.4 Model Validation Strategy

Retrained models must be validated using the following approach:

Retrained models are evaluated using stratified 5-fold cross-validation on a held-out test set (20% of data, temporally after training data). Test set must include at least 200 samples per rhythm class from at least 3 distinct hospital systems not represented in training data. Performance is evaluated separately for each rhythm class and for sub-populations (age groups: <50, 50-65, >65). Validation must be performed by the Quality team independently of the model development team.

### 2.5 Validation Acceptance Criteria

The retrained model must satisfy ALL of the following criteria before deployment:

- AUROC for supraventricular detection must be >= 0.90 (baseline 0.925)
- AUROC for ventricular detection must be >= 0.92 (baseline 0.937)
- Sensitivity for ventricular detection must be >= 0.89 (baseline 0.91)
- Specificity for ventricular detection must be >= 0.93 (baseline 0.95)
- PPV must not decline by more than 3% from baseline across all classes
- Performance must be maintained (within 2%) for age subgroups: <50, 50-65, >65
- No regression in demographic fairness: max PPV difference across sex/age <= 5%
- Agreement with cardiologist annotations on difficult cases must be >= 85%

### 2.6 Performance Thresholds and Monitoring

Performance is monitored against the following metrics. Models must maintain or exceed baseline performance as specified in the warning and action thresholds below.

| Metric | Baseline | Warning Threshold | Action Threshold | Direction |
|---|---|---|---|---|
| AUROC (Supraventricular) | 0.925 | 0.91 | 0.895 | Higher |
| AUROC (Ventricular) | 0.937 | 0.92 | 0.905 | Higher |
| Sensitivity (Ventricular) | 0.91 | 0.895 | 0.88 | Higher |
| Specificity (Ventricular) | 0.95 | 0.935 | 0.92 | Higher |
| PPV (Positive Predictive Value) | 0.88 | 0.85 | 0.82 | Higher |

#### 2.6.1 Metric Descriptions and Justifications

**AUROC (Supraventricular):** Area under the receiver operating characteristic curve for binary supraventricular rhythm classification. Measures overall discriminative ability.
- **Baseline Value (from development):** 0.925
- **Warning Threshold:** 0.91 (triggers investigation)
- **Action Threshold:** 0.895 (triggers retraining cycle)
- **Direction of Improvement:** Higher

**AUROC (Ventricular):** Area under the receiver operating characteristic curve for binary ventricular rhythm classification. Critical for detecting dangerous rhythms.
- **Baseline Value (from development):** 0.937
- **Warning Threshold:** 0.92 (triggers investigation)
- **Action Threshold:** 0.905 (triggers retraining cycle)
- **Direction of Improvement:** Higher

**Sensitivity (Ventricular):** True positive rate for ventricular rhythm detection. Clinically critical: missing ventricular arrhythmias poses patient safety risk.
- **Baseline Value (from development):** 0.91
- **Warning Threshold:** 0.895 (triggers investigation)
- **Action Threshold:** 0.88 (triggers retraining cycle)
- **Direction of Improvement:** Higher

**Specificity (Ventricular):** True negative rate for ventricular rhythm classification. Reduces false alarms and unnecessary interventions.
- **Baseline Value (from development):** 0.95
- **Warning Threshold:** 0.935 (triggers investigation)
- **Action Threshold:** 0.92 (triggers retraining cycle)
- **Direction of Improvement:** Higher

**PPV (Positive Predictive Value):** Precision of positive detections. Prevents overdiagnosis and unnecessary patient interventions.
- **Baseline Value (from development):** 0.88
- **Warning Threshold:** 0.85 (triggers investigation)
- **Action Threshold:** 0.82 (triggers retraining cycle)
- **Direction of Improvement:** Higher


### 2.7 Data Drift Monitoring

The following protocol is used to detect and respond to data drift:

**Drift Detection Method:** Statistical distribution shift detection using Kolmogorov-Smirnov test on ECG signal features extracted from input data (mean, variance, skewness, kurtosis of each lead). Compares monthly batches to baseline distribution from model development. Additionally monitors prediction entropy and confidence distribution as proxy for data shift.

**Monitoring Frequency:** Monthly on all ECGs processed in production

**Drift Threshold Definition:** Drift is flagged when (1) KS-test p-value < 0.05 for any lead's features, or (2) mean model confidence drops >5% from baseline, or (3) >10% of samples have prediction entropy > 0.8 (indicating high model uncertainty).

**Response Protocol When Drift Detected:** When drift is detected, (1) alert Quality/Regulatory team within 24 hours; (2) sample 50 drift-flagged ECGs for cardiologist review to assess clinical impact; (3) if cardiologist review shows >5% discordance with model output, trigger emergency retraining cycle or roll back to previous model version pending investigation; (4) document drift event, root cause, and resolution.

### 2.8 Deployment Process

Once a model passes all validation criteria, deployment proceeds as follows:

A validated, retrained model is deployed to production via the following process: (1) Quality team approves model against all validation criteria and signs off in electronic system. (2) Model is packaged with version metadata, training date, and checksums. (3) Deployment to production happens on scheduled maintenance window (Friday 2 AM UTC, low-traffic period). (4) Canary deployment: model serves 5% of inference requests for 24 hours with side-by-side prediction logging. (5) If canary metrics stable, scale to 100% over 2 hours. (6) Previous model version retained for 30 days to enable rapid rollback. (7) Production performance metrics (latency, throughput, inference accuracy on logged predictions) monitored in real-time dashboard. (8) Weekly audit of deployment logs and discordance events.

---

## Section 3: Impact Assessment

### 3.1 Benefits of Planned Modifications

Periodic model retraining and data expansion enable continuous improvement in arrhythmia detection performance, allowing CardioDetect to maintain clinical efficacy as patient populations and ECG equipment evolve. Data expansion to diverse institutions reduces algorithmic bias and improves model generalization. Planned modifications allow faster iteration cycles compared to traditional 510(k) amendments, accelerating patient access to improved diagnostics. The documented modification protocol provides transparency and auditability for regulatory oversight and clinical governance.

### 3.2 Potential Risks and Mitigations

Model retraining on new data may introduce unexpected behavior if training data contains systematic biases or unrepresentative samples. Hyperparameter changes could degrade performance on previously well-handled edge cases. Rapid deployment cycles may reduce time for thorough testing. Data expansion from new sources introduces potential for unmeasured confounders or systematic labeling differences across institutions. Changes in ECG equipment or patient populations could cause distribution shift not captured by drift monitoring.

The following mitigations are in place to manage identified risks:

| Risk | Mitigation |
|---|---|
| Performance degradation in new demographic groups | Stratified validation on subpopulation data before deployment. Each new data source is labeled by certified cardiologists and validated on at least 200 samples before inclusion in training set. Fairness metrics (PPV variance, equalized odds) are monitored for each age/sex group. |
| Training data distribution contamination | Automated data quality checks reject records with artifact, missing leads, or invalid labels. Manual review of 5% of training data by independent cardiologist. Training set composition tracked in change control log with justifications for any significant shifts. |
| Rapid deployment introduces untested model behavior | Canary deployment with 24-hour observation period before full rollout. Automated alerting on key performance metrics and cardiologist-in-the-loop review for high-uncertainty predictions. Rapid rollback capability to previous model. |
| Data drift undetected, model performance silently degrades | Continuous monthly drift monitoring with statistical tests and entropy-based alerts. Weekly manual review of 50 high-entropy predictions by cardiologists to catch performance issues early. Post-market surveillance protocol includes quarterly 30-day audit samples. |
| Cross-site ECG equipment differences cause systematic bias | Training data explicitly stratified by equipment manufacturer (GE, Schiller, Mortara) with minimum 100 samples per device before inclusion. Performance validated separately for each equipment type. |

#### 3.2.1 Detailed Risk Mitigation Strategies

**Risk:** Performance degradation in new demographic groups

**Mitigation:** Stratified validation on subpopulation data before deployment. Each new data source is labeled by certified cardiologists and validated on at least 200 samples before inclusion in training set. Fairness metrics (PPV variance, equalized odds) are monitored for each age/sex group.

**Risk:** Training data distribution contamination

**Mitigation:** Automated data quality checks reject records with artifact, missing leads, or invalid labels. Manual review of 5% of training data by independent cardiologist. Training set composition tracked in change control log with justifications for any significant shifts.

**Risk:** Rapid deployment introduces untested model behavior

**Mitigation:** Canary deployment with 24-hour observation period before full rollout. Automated alerting on key performance metrics and cardiologist-in-the-loop review for high-uncertainty predictions. Rapid rollback capability to previous model.

**Risk:** Data drift undetected, model performance silently degrades

**Mitigation:** Continuous monthly drift monitoring with statistical tests and entropy-based alerts. Weekly manual review of 50 high-entropy predictions by cardiologists to catch performance issues early. Post-market surveillance protocol includes quarterly 30-day audit samples.

**Risk:** Cross-site ECG equipment differences cause systematic bias

**Mitigation:** Training data explicitly stratified by equipment manufacturer (GE, Schiller, Mortara) with minimum 100 samples per device before inclusion. Performance validated separately for each equipment type.


### 3.3 Sub-Population Analysis

Performance of the ML model must be maintained across the following clinically relevant sub-populations:

#### 3.3.1 Age Group: <50 years

**Sub-Population Definition:** Patients under 50 years old. Typically have lower baseline arrhythmia prevalence and different ECG morphology than older patients.

**Performance Expectations:** AUROC targets: Supraventricular 0.93, Ventricular 0.94 (higher specificity due to lower disease prevalence). Sensitivity for ventricular >= 0.90.

**Monitoring Plan:** Separate tracking of this cohort in monthly performance reports. Flagged if AUROC differs by >3% from overall model.

#### 3.3.2 Age Group: 50-65 years

**Sub-Population Definition:** Patients between 50 and 65 years old. Moderate prevalence of arrhythmias with age-related ECG changes.

**Performance Expectations:** AUROC targets: Supraventricular 0.92, Ventricular 0.93. Sensitivity >= 0.90, Specificity >= 0.95.

**Monitoring Plan:** Primary performance evaluation cohort. Validated in development. Continuous monitoring in post-market surveillance.

#### 3.3.3 Age Group: >65 years

**Sub-Population Definition:** Patients over 65 years old. High prevalence of atrial fibrillation and other arrhythmias; complex ECG morphology.

**Performance Expectations:** AUROC targets: Supraventricular 0.91, Ventricular 0.92 (accounting for complex baseline conditions). Sensitivity >= 0.89.

**Monitoring Plan:** Monthly stratified analysis. If AUROC < 0.90, trigger urgent retraining focused on geriatric population. Cardiologist-in-the-loop review for all discordant cases.

#### 3.3.4 Sex: Male

**Sub-Population Definition:** Patients identifying as male. ECG morphology differs from female.

**Performance Expectations:** Performance parity: AUROC within 2% of overall model. PPV within 3%.

**Monitoring Plan:** Monthly tracking. If PPV diverges >3%, investigate for sex-related bias in training data.

#### 3.3.5 Sex: Female

**Sub-Population Definition:** Patients identifying as female. ECG QT interval and T-wave morphology differ; lower ST-elevation MI prevalence.

**Performance Expectations:** Performance parity: AUROC within 2% of overall model. PPV within 3%.

**Monitoring Plan:** Monthly tracking. Historical cardiology literature documents sex differences in arrhythmia presentation; model must maintain sensitivity across sexes.


### 3.4 Post-Market Surveillance and Reporting

Post-market surveillance for PCCP modifications includes: (1) Continuous logging of all model inferences with input ECG signals and predicted rhythm probabilities; (2) Monthly performance reports stratified by sub-population, hospital system, and ECG equipment, compared to baseline thresholds; (3) Quarterly cardiologist review of 50 discordant cases (model prediction differed from clinical diagnosis); (4) Annual analysis of demographic fairness metrics and publication of results; (5) FDA MedWatch reporting for any safety events attributable to model error; (6) Immediate notification to healthcare facility if drift detected or performance falls below action thresholds; (7) Retention of all training data, model versions, validation reports, and deployment logs for FDA inspection; (8) Annual PCCP effectiveness review and update if modifications fall outside approved scope.

---

## Section 4: Regulatory Compliance

This PCCP is executed in compliance with: (1) FDA Predetermined Change Control Plans guidance for ML-enabled medical devices (Dec 2024); (2) 21 CFR 860 Medical Device Regulations; (3) IEC 62304 medical device software lifecycle; (4) HIPAA de-identification standards (45 CFR 164.502(b)) for patient data; (5) 21 CFR 11 electronic records and signatures; (6) FDA guidance on AI/ML-based SaMD (January 2021). All modifications are implemented under the quality management system and design control procedures as documented in CardioAI's design history file (DHF) and design transfer file (DTF). No modifications falling outside the scope defined in Sections 1-2 of this PCCP may be implemented without a new 510(k) submission or equivalent FDA clearance.

---

## Approval and Implementation

This PCCP is valid upon completion of the validation and approval process specified herein. Modifications to this PCCP or implementation of modifications not explicitly described herein require prior FDA notification or approval.

**Prepared By:** [Signature/Name - Regulatory/Quality Function]

**Approved By:** [Signature/Name - Quality Assurance]

**Date of Approval:** [Date]

---

## References and Footnotes

[^1]: FDA Guidance Document: "Predetermined Change Control Plans for Machine Learning-Enabled Medical Devices." FDA Center for Devices and Radiological Health (CDRH), December 2024. Available at: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices

[^2]: 21 Code of Federal Regulations Part 860 - Medical Device Regulations

[^3]: FDA Guidance for Industry: "Proposed Regulatory Framework for Modifications to Artificial Intelligence/Machine Learning (AI/ML)-Based Software as a Medical Device (SaMD)" - Precertification Program, January 2021.

---

*This document is automatically generated from a configuration specification. While it provides regulatory scaffolding, every PCCP must be customized to the specific device, clinical context, and intended modifications. Review by qualified regulatory professionals is mandatory before submission to FDA. The generator and its users assume no liability for submissions made using generated documents.*