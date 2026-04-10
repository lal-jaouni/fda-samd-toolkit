# Clinical Validation Plan: CardioDetect ECG Arrhythmia Classifier

**Document Version:** 1.0
**Date:** 2026-04-10
**Modality:** Signals

---

## 1. Executive Summary

This clinical validation plan describes the prospective clinical testing protocol for CardioDetect ECG Arrhythmia Classifier, an AI/ML-enabled medical device intended for Detection and classification of cardiac arrhythmias from 12-lead ECG signals as decision support for cardiologists during clinical assessment of patients with suspected arrhythmias or cardiac conduction abnormalities..

The validation study will establish clinical performance, safety, and generalizability of the algorithm across diverse patient populations and clinical settings. This plan adheres to FDA guidance on clinical performance assessment for AI/ML devices (FDA 2024) and clinical performance assessment for computer-assisted detection devices (FDA 2020).

**Key Study Parameters:**
- Study Design: Retrospective
- Planned Sample Size: 1500 subjects
- Primary Endpoint: Sensitivity >= 90% (95% CI lower bound >= 85%) AND Specificity >= 95% (95% CI lower bound >= 90%)
- Data Modality: Signals

---

## 2. Device and Intended Use

### 2.1 Device Name and Classification
**Device Name:** CardioDetect ECG Arrhythmia Classifier

**Intended Use:**
Detection and classification of cardiac arrhythmias from 12-lead ECG signals as decision support for cardiologists during clinical assessment of patients with suspected arrhythmias or cardiac conduction abnormalities.

This device processes Signals data and provides decision support for clinical interpretation and diagnosis.

### 2.2 Indications for Use
- **Patient Population:** [Specify age range, disease state, clinical setting]
- **Clinical Setting:** [Hospital, outpatient, home, etc.]
- **Provider Type:** [Cardiologists, radiologists, etc.]

---

## 3. Study Design

### 3.1 Overview
**Study Type:** Retrospective
**Blinding:** Double-Blinded
**Multi-Site:** Yes (3 sites)**Duration:** 18 months
**Rationale for Study Design:**
The retrospective design with double-blinded blinding was selected to:
- [Rationale 1: Reduces bias in reference standard assessment]
- [Rationale 2: Reflects real-world deployment scenario]
- [Rationale 3: Enables assessment of algorithm on consecutive patients]

**Participating Sites:**
- Johns Hopkins Medical Center, Baltimore, MD
- Stanford Health, Palo Alto, CA
- Mayo Clinic, Rochester, MN

Multi-site enrollment ensures:
- Geographic diversity and generalization potential
- Different clinical practices and workflows
- Diverse patient populations by race, ethnicity, and socioeconomic status

### 3.2 Regulatory References
FDA guidance documents informing this validation plan:
- FDA "Clinical Performance Assessment: Considerations for Computer-Assisted Detection Devices" (2020)
- FDA "Predetermined Change Control Plans for AI/ML-Enabled Medical Devices" (December 2024)
- STARD 2015 (Standards for Reporting Diagnostic Accuracy Studies)
- TRIPOD-AI (Transparent Reporting of Evaluations with Nonlinear Machine Learning Models)
- IMDRF SaMD Framework

---

## 4. Study Population and Data

### 4.1 Data Sources

**Primary Data Sources:**
- Johns Hopkins Hospital ECG Repository
- Stanford Health ECG Database
- Mayo Clinic Cardiovascular Biobank

**Data Collection Period:** 2020-01-01 to 2023-12-31

**Total Sample Size:** 1500 subjects

### 4.2 Inclusion Criteria
Subjects will be eligible for the study if they meet all of the following criteria:

- Age 18 years or older at time of ECG
- Complete 12-lead ECG recording with sampling rate 250 Hz or higher
- Confirmed clinical diagnosis or outcome within 6 months of ECG (for reference standard)
- Available cardiology assessment or device diagnosis for adjudication
- Clinical note documentation of arrhythmia status or cardiac rhythm

### 4.3 Exclusion Criteria
Subjects will be excluded from the study if they meet any of the following criteria:

- Incomplete or corrupted ECG signal
- ECG signal quality score <80% (excessive noise, artifact, baseline wander)
- Paced rhythms (due to complexity in rhythm classification)
- Subjects with no clinical follow-up data for reference standard establishment
- Insufficient documentation for adjudicator reference standard determination

### 4.4 Sample Size Justification

**Planned Sample Size:** 1500 subjects

**Statistical Justification:**
Sample size calculation assumes atrial fibrillation (AF) prevalence of 15% (225 AF subjects, 1275 non-AF). Using binomial test with alpha=0.05, power=0.90, and target sensitivity=90% with null hypothesis of 80%, n=225 AF subjects provides adequate power. For specificity with target 95% (null=90%), n=1275 non-AF subjects provides power>0.99. Additional 20% buffer accounts for protocol deviations. Formula: n = [z_alpha + z_beta]^2 * p0 * (1-p0) / (p1 - p0)^2.

**Sample Size Calculation Details:**
[Provide alpha level, power target (typically 80-90%), effect size, assumed performance rates, and dropout rate assumptions used in calculation]

### 4.5 Population Diversity and Representation
**Diversity Goals:**
The study aims to enroll a demographically diverse population including: Age: 18-40 (25%), 41-60 (35%), 61-75 (25%), >75 (15%); Sex: 48% Female, 52% Male; Race/Ethnicity: 60% White, 20% Black/African American, 12% Hispanic/Latino, 8% Asian. Comorbidity distribution should reflect typical cardiology clinic prevalence (hypertension 50%, diabetes 25%, structural heart disease 15%).

**Rationale:** FDA guidance and clinical standards emphasize evaluation of AI algorithms across demographic subgroups to identify and mitigate performance disparities. Underrepresentation of any demographic group limits evidence of safety and effectiveness in that population.

---

## 5. Reference Standard (Gold Standard)

### 5.1 Reference Standard Definition
**Gold Standard:** Clinical diagnosis of cardiac arrhythmia confirmed by board-certified cardiologists based on 12-lead ECG interpretation, device interrogation (for patients with pacemakers/ICDs), electrophysiology testing, or cardiac imaging.

**Source of Reference Standard:** Board-certified cardiologist clinical assessment

**Clinical Justification:**
This reference standard is the accepted diagnostic or prognostic standard for the condition of interest. [Provide rationale for why this standard is appropriate and clinically meaningful.]

### 5.2 Adjudication Process
**Adjudication Protocol:** Two independent board-certified cardiologists will review each ECG and classify the cardiac rhythm using standardized classification system (Brugada classification for arrhythmias). For cases of disagreement, a third cardiologist specialist in electrophysiology will adjudicate. Final reference standard assignment requires consensus of at least 2 of 3 adjudicators.

**Adjudicator Qualifications:**
Board certification in Cardiology from American Board of Internal Medicine with minimum 5 years post-board certification experience. Cardiologists must have demonstrated expertise in arrhythmia interpretation (publications, clinical role, or fellowship training in electrophysiology).

**Number of Adjudicators:** 3

**Process for Disagreement:**
[Specify decision rule when adjudicators disagree. Examples:
- Majority vote (use if >=3 adjudicators)
- Consensus discussion among all adjudicators
- Escalation to third-party senior expert for tiebreaker
- Do NOT use majority vote if only 2 adjudicators; escalate instead]

### 5.3 Inter-Rater Reliability
**Target Inter-Rater Reliability:** 0.85 (Fleiss kappa for multi-rater reliability)

**Methodology for Assessing Reliability:**
- All adjudicators will independently review reference data
- At minimum, 10% of subjects will be reviewed by all adjudicators for reliability assessment
- Reliability will be calculated before subject enrollment completes
- If target reliability not met, adjudicators will undergo retraining and process revised

---

## 6. Primary and Secondary Endpoints

### 6.1 Primary Endpoint
**Endpoint:** Sensitivity and specificity for detection of atrial fibrillation (AF) on 12-lead ECG compared to clinical reference standard diagnosis.

**Primary Success Criterion:** Sensitivity >= 90% (95% CI lower bound >= 85%) AND Specificity >= 95% (95% CI lower bound >= 90%)

**Definition of Success:** [Specify what performance is considered clinically and statistically significant]

### 6.2 Secondary Endpoints
- Classification accuracy for 5-class arrhythmia categories (Normal, AF, Atrial Flutter, SVT, VT)
- Area Under Receiver Operating Characteristic Curve (AUROC) for AF detection: >= 0.92
- Positive Predictive Value >= 85% at typical AF prevalence of 5%
- Negative Predictive Value >= 98%
- Performance consistency across device brands (GE, Philips, Nihon Kohden, Schiller)

### 6.3 Performance Targets
**Sensitivity:** 0.9(95% CI lower bound: 0.85)
**Specificity:** 0.95(95% CI lower bound: 0.9)


**Rationale for Performance Targets:**
[Explain how targets were determined. Consider:
- Clinical literature on acceptable performance for this indication
- FDA predicate device performance if 510(k) pathway
- Expert consultation on clinically meaningful performance
- Trade-off analysis between sensitivity (avoiding missed diagnoses) and specificity (avoiding false alarms)]

---

## 7. Statistical Analysis Plan

### 7.1 Primary Hypothesis
**Hypothesis:** The CardioDetect algorithm will achieve sensitivity >= 90% and specificity >= 95% for atrial fibrillation detection compared to clinical reference standard in a diverse population of 1500 subjects.

### 7.2 Statistical Test and Analysis
**Test:** Binomial test for sensitivity and specificity, with DeLong test for comparing AUROC between algorithm and clinical cardiologist performance.

**Significance Level (alpha):** 0.05

**Target Power:** 0.9

### 7.3 Power Calculation
**Sample Size Justification:**
Sample size calculation assumes AF prevalence of 15% (225 AF subjects, 1275 non-AF). Using binomial test with alpha=0.05, power=0.90, and target sensitivity=90% with null hypothesis of 80%, n=225 AF subjects provides adequate power. For specificity with target 95% (null=90%), n=1275 non-AF subjects provides power>0.99. Additional 20% buffer (n=1800 total enrollment, 1500 analyzable) accounts for potential protocol deviations and missing reference standards. Formula: n = [z_alpha + z_beta]^2 * p0 * (1-p0) / (p1 - p0)^2.

[Include detailed calculation showing:
- Formula used
- Assumed performance parameters from pilot data or literature
- Assumptions about dropout/missing data
- Any adjustments for multiple comparisons or clustering]

### 7.4 Handling Multiple Comparisons
**Multiplicity Correction:** No correction for primary AF sensitivity/specificity tests (pre-specified co-primary). Bonferroni correction (alpha/5 = 0.01) applied to 5 secondary arrhythmia class tests.

[If multiple primary endpoints or subgroup tests are planned, specify correction method:
- Bonferroni (most conservative)
- Holm step-down procedure
- False discovery rate (FDR) control
- Pre-specified subgroup hierarchy with no correction for primary analysis]

### 7.5 Missing Data Strategy
**Approach:** Primary analysis: intention-to-analyze with complete case analysis for subjects with valid ECG and reference standard. Sensitivity analysis will use multiple imputation (MICE) for subjects with missing reference standard adjudication. Subjects with technical ECG failures will be excluded (recorded separately).

[Specify:
- Handling of subjects with missing reference standard assessment
- Handling of subjects with missing algorithm prediction
- Handling of partially completed studies (early dropout)
- Primary analysis (complete case, per-protocol, or intention-to-analyze)]

### 7.6 Sensitivity Analyses
Sensitivity analyses will be conducted to assess robustness of primary findings:
- Stratified analysis by AF paroxysmal vs. persistent/permanent
- Performance on high-quality ECGs (SNR >40dB) vs. routine clinical recordings
- Sensitivity analysis excluding subjects with structural heart disease
- Sub-group analysis by device manufacturer (GE vs. Philips vs. others)
- Analysis removing outlier subjects with extreme signal characteristics

---

## 8. Subgroup Analysis


### 8.1 Planned Subgroup Stratifications
The following subgroups will be analyzed to assess whether algorithm performance differs across populations:

**Subgroups:**
- Sex: Male vs. Female
- Age: <50, 50-65, >65 years
- Race/Ethnicity: White, Black/African American, Hispanic/Latino, Asian, Other
- Comorbidity: None vs. Hypertension vs. Diabetes vs. Structural Heart Disease
- Arrhythmia Type: Paroxysmal AF vs. Persistent AF
- Device Manufacturer: GE, Philips, Nihon Kohden, Schiller, Other

**Stratification Variables:**
- age_group
- sex
- race_ethnicity
- comorbidity_status

### 8.2 Performance Targets by Subgroup
- **Female:** Sensitivity >= 88%, Specificity >= 94%
- **Male:** Sensitivity >= 90%, Specificity >= 95%
- **<50 years:** Sensitivity >= 92%, Specificity >= 96%
- **50-65 years:** Sensitivity >= 90%, Specificity >= 95%
- **>65 years:** Sensitivity >= 88%, Specificity >= 94%

### 8.3 Minority Representation
**Strategy:**
The study will actively recruit from diverse healthcare systems serving African American, Hispanic/Latino, and Asian communities. Target enrollment: Black/African American 20% (300 subjects), Hispanic/Latino 12% (180 subjects), Asian 8% (120 subjects). Recruitment incentives and multi-language materials will be provided.

### 8.4 Differential Performance Analysis
**Plan:**
Chi-square tests will assess whether sensitivity/specificity differs significantly across demographic subgroups. If disparity detected (>5% difference), we will investigate potential drivers (signal quality, arrhythmia phenotype, comorbidities) and plan mitigation (retraining data weighting, confidence adjustments).


---

## 9. External Validation and Generalization Testing


### 9.1 External Validation Sites
**Sites:**
- Cleveland Clinic, Cleveland, OH
- UCSF Medical Center, San Francisco, CA

**Sample Size:** 400 subjects

**Timeline:** External validation will be conducted post-primary analysis, pre-FDA submission. Timeline: 6 months for enrollment and analysis.
**Site Selection Rationale:**
External validation sites should be geographically and organizationally distinct from primary study sites to ensure generalization. Sites should differ in:
- Electronic health record system and vendor
- Clinical workflows and provider expertise levels
- Patient population demographics and disease burden
- For imaging: equipment manufacturer and acquisition protocols
- For signals: device manufacturer and signal processing parameters


### 9.2 Temporal Validation
**Plan:**
Temporal validation will assess algorithm performance on ECGs collected in 2024 (>12 months after primary study data). Comparison metrics: sensitivity/specificity should not degrade >3%. Investigation of any drift with updated prevalence estimates or signal distribution shifts.

### 9.3 Data Drift Monitoring
**Plan:**
Post-market surveillance: Monthly analysis of algorithm predictions and confidence distributions. Drift detection using Kolmogorov-Smirnov test (p<0.05 triggers investigation). Performance metrics tracked monthly; if monthly sensitivity drops >5% or specificity drops >3%, trigger retraining protocol.

### 9.4 Geographic Generalization
**Plan:**
The multi-site primary study (3 geographic regions) will assess regional performance variation. External validation adds 2 additional regions for 5-region US coverage. Analysis will assess whether site-specific performance differences relate to demographic factors, clinical practice patterns, or equipment differences.


---

## 10. Safety Monitoring


### 10.1 Adverse Event Definitions
**Adverse Event:** Any clinical consequence of false algorithm prediction that results in unintended patient harm, unnecessary intervention, or diagnostic delay. Includes: false positive AF detection triggering inappropriate anticoagulation, false negative missing clinically significant arrhythmia.

**Serious Adverse Event:** False negative result leading to missed AF diagnosis with subsequent stroke, thromboembolic event, or other serious morbidity. False positive leading to major bleeding from inappropriate anticoagulation.

### 10.2 Prospective Safety Monitoring
**Monitoring Plan:**
During retrospective study: structured chart review of false predictions and clinical outcomes. For all subjects with disagreement between algorithm and reference standard, senior cardiologist will assess clinical consequences.

[Specify:
- How adverse events will be detected and reported
- Frequency of safety reviews
- Criteria for escalation]

### 10.3 Safety Stopping Rules
**Rules:**
Study will be paused if: (1) False negative rate in AF detection >15%, (2) >3 subjects identified with serious adverse outcome attributable to false negative, or (3) Sensitivity <85% with lower 95% CI <80%.

[Pre-specified stopping criteria:
- If serious adverse event rate exceeds X%
- If false negative rate leads to [specify adverse clinical outcome] in >X subjects
- If false positive rate triggers unnecessary interventions in >X% of subjects]

### 10.4 Clinical Impact of False Positives and Negatives
**False Positive Impact:**
False positive AF detection may trigger: (a) Initiation of anticoagulation therapy with bleeding risk, (b) Unnecessary cardiology referral and additional testing, (c) Patient anxiety and lifestyle modifications. Impact mitigated by: integration of algorithm output as decision support (not standalone diagnostic), requirement for clinician confirmation before treatment decisions, high specificity target (95%).

**False Negative Impact:**
False negative AF detection may result in: (a) Missed opportunity for anticoagulation in patient at stroke risk, (b) Delayed referral for rate control or other management, (c) Patient experiencing stroke or other thromboembolic event. Impact mitigated by: high sensitivity target (90%), integration in standard ECG interpretation workflow, clinician override capability.

**Mitigation Strategies:**
- [Clinician review and override capability for borderline predictions]
- [High-confidence threshold for automated alerts versus lower-confidence decision support]
- [Alerts integrated into existing clinical workflow with clear documentation of algorithm prediction and confidence]
- [Training for clinicians on algorithm capabilities and limitations]


---

## 11. Modality-Specific Considerations

### 11.1 Signals-Specific Guidance
This validation plan incorporates modality-specific best practices for signals AI/ML validation.

**Key Considerations:**
- Signal sampling rate and duration requirements
- Lead configuration (ECG: 12-lead vs 1-lead, EEG: number and placement of electrodes)
- Signal quality criteria (noise thresholds, artifact handling, baseline wander)
- QC procedures for signal preprocessing (filtering, normalization, artifact removal)
- Handling of signals with motion artifacts, noise, or missing segments
- Temporal aspect: windowing strategy and overlap for inference

**Data Source Requirements:**
Data should be obtained from clinical monitoring systems (Holter, ICU monitors, wearables) with documented equipment type, firmware version, and sampling specifications. Include multiple device manufacturers to assess hardware independence. Capture full signal metadata: lead configuration, sampling rate, filter settings, gain. Document time-of-day and patient state during recording (resting, exercise, sleep, etc.).

**Reference Standard Requirements:**
Reference standard established by board-certified cardiologists/neurologists with subspecialty training. For ECG: use serial tracings, clinical correlation, and when needed, EP study or imaging confirmation. For EEG: use structured scoring systems (e.g., IFSECN classification). Use 3-reader consensus for equivocal arrhythmias/abnormalities. Target inter-rater reliability (Cohen's kappa or ICC2,k) >= 0.80.

**Endpoint Specifications:**
Primary endpoint: sensitivity >= 0.90 and specificity >= 0.95 for target arrhythmia/abnormality. Report both on per-beat and per-episode level (for continuous monitoring). Include positive/negative predictive value for typical patient prevalence. For multi-class arrhythmias: report macro and weighted averages.

**Statistical Analysis:**
Account for within-subject correlation (multiple signals per patient). Use mixed-effects models or GEE for clustered analysis if applicable. Sample size: n = [z_alpha + z_beta]^2 * (Se * (1-Se) + Sp * (1-Sp)) / (Se + Sp - 1)^2. Stratify by device type, lead configuration, and signal quality metrics. Assess performance across different sampling rates if device-agnostic.

**Subgroup Analysis Recommendations:**
Stratify by sex, age (<40, 40-65, >65), and heart rate/baseline rhythm. Analyze performance by signal quality (noise level, artifact percentage). Report metrics separately for different device manufacturers if multi-device study. Include stratification by comorbidities (structural heart disease, electrolyte abnormalities, medications).

**Safety Considerations:**
False positive: unnecessary interventions (medication changes, device implant), patient anxiety. False negative: missed life-threatening arrhythmia (syncope, sudden cardiac death risk). Plan for human review of borderline predictions; define confidence thresholds for alert escalation. Include panic value thresholds for immediately actionable findings.

**External Validation Strategy:**
External validation with different device manufacturer (different signal conditioning). Test on different lead configurations if applicable (12-lead trained, evaluate on 3-lead). Temporal validation: assess performance drift over >1 year post-market. Include subjects with known arrhythmias and asymptomatic individuals.

---

## 12. Data Management and Quality Assurance

### 12.1 Data Collection and Security
- All subject data will be de-identified per HIPAA standards before analysis
- Electronic data capture will be used with audit trails and validation rules
- Data quality checks will be performed at study sites before data transfer
- All data transfers will be encrypted and logged

### 12.2 Algorithm Implementation
**Input Specifications:**
[Specify: data format, required fields, sampling rate/resolution, preprocessing requirements]

**Inference Pipeline:**
[Specify: preprocessing steps, model version, confidence threshold, output format]

**Version Control:**
- Algorithm version will be documented and fixed before study enrollment begins
- Any modifications or retraining during study will be tracked and reported
- Final algorithm version used for analysis will be specified in final report

---

## 13. Success Criteria and Analysis

### 13.1 Primary Success Criterion
The study will be considered successful if:
- Sensitivity >= 90% (95% CI lower bound >= 85%) AND Specificity >= 95% (95% CI lower bound >= 90%)

### 13.2 Secondary Success Criteria
Secondary success will be demonstrated if:
- Classification accuracy for 5-class arrhythmia categories (Normal, AF, Atrial Flutter, SVT, VT)
- Area Under Receiver Operating Characteristic Curve (AUROC) for AF detection: >= 0.92
- Positive Predictive Value >= 85% at typical AF prevalence of 5%
- Negative Predictive Value >= 98%
- Performance consistency across device brands (GE, Philips, Nihon Kohden, Schiller)

### 13.3 Analysis Population
- **Primary Analysis:** [Specify: Intention-to-treat (all enrolled), Per-protocol (protocol-adherent), or others]
- **Sensitivity Analyses:** [Specify alternative populations to test robustness]

---

## 14. Study Timeline

| Milestone | Timeline |
|-----------|----------|
| Institutional Review Board (IRB) Review | [Date] |
| Site Initiation | [Date] |
| Subject Enrollment Complete | [Date] |
| Final Data Lock | [Date] |
| Interim Analysis (if planned) | [Date] |
| Final Analysis | [Date] |
| Report Completion | [Date] |

---

## 15. Quality and Regulatory Compliance

### 15.1 Regulatory Oversight
- Study will comply with FDA regulations (21 CFR Part 11, Part 56, Part 312 if applicable)
- Institutional Review Board (IRB) review and approval required before enrollment
- Informed consent obtained from all subjects or legally authorized representatives

### 15.2 Quality Assurance
- Protocol deviations tracked and reported
- Regular quality reviews of data collection and algorithm performance
- Monitoring for loss to follow-up and missing data
- Audit trail maintained for all algorithm predictions and reference standard assignments

### 15.3 Regulatory References
- FDA 'Clinical Performance Assessment: Considerations for Computer-Assisted Detection Devices' (2020)
- FDA 'Predetermined Change Control Plans for Machine Learning-Enabled Medical Devices' (December 2024)
- STARD 2015 (Standards for Reporting Diagnostic Accuracy Studies)
- TRIPOD-AI (Transparent Reporting of Evaluations with Nonlinear Machine Learning Models in Diagnostic and Prognostic Applications)
- ACC/AHA Guidelines for Atrial Fibrillation (2019)
- IEC 62304: Medical Device Software Lifecycle Processes

---

## 16. Appendices

### Appendix A: Algorithm Architecture Summary
[Provide high-level description of:
- Input data types and preprocessing
- Model architecture (if appropriate to disclose)
- Training data and validation approach used during development
- Known limitations and edge cases]

### Appendix B: Case Report Form Templates
[Attach templates for:
- Subject demographic and clinical data
- Reference standard assessment forms
- Algorithm prediction documentation]

### Appendix C: Statistical Formulas and Sample Size Calculations
[Attach detailed calculations showing:
- Sample size formula and parameters
- Interim analysis plan (if applicable)
- Stopping boundaries]

### Appendix D: Study Protocol
[Attach the full institutional protocol reviewed by IRB]

---

**Document Approved By:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Principal Investigator | | | |
| Sponsor Representative | | | |
| Regulatory Affairs | | | |
