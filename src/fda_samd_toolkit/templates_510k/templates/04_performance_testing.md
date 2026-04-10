# Performance Testing for AI/ML Medical Devices

## Overview
This is the longest and most critical template. FDA spends the most time scrutinizing performance testing.
Your 510(k) will likely be rejected if:
1. Test dataset is too small or unrepresentative
2. Performance metrics are weak or not comparable to predicate
3. Subgroup analysis is missing (FDA wants to know if your device works equally in men, women, racial minorities, different age groups)
4. Test/train data are not properly split (leak = invalid performance claims)
5. Reference standard is unclear or not rigorous (how was ground truth determined?)

**FDA Guidance:** Demonstrate performance on:
- Overall population (primary metric)
- Clinically important subgroups (sex, age, race, disease severity)
- Edge cases and failure modes (what breaks the device?)
- Prospective data if possible (stronger evidence than retrospective)

**Industry Standard:** For classification tasks, FDA typically expects:
- Sensitivity >90% for serious conditions (missed diagnosis = patient harm)
- Specificity >85% (false positives = unnecessary testing, cost, anxiety)
- Balanced performance across subgroups (within 3-5%)

---

## Template

## 1. Study Design and Protocol

### 1.1 Study Design Overview

Describe the overall structure of your validation study.

[INSERT: Study design]

**Key elements FDA expects:**
- Study type: Retrospective, prospective, or hybrid
- Multicenter vs. single-center
- Study duration and data collection timeframe
- Regulatory approval (IRB, ethics committee)
- Sample size justification (statistical power)
- Inclusion/exclusion criteria
- Endpoint definitions

Example: "This performance validation study employed a **retrospective, multicenter design**
evaluating de-identified ECG records and clinical outcomes from three academic medical centers:

1. Mayo Clinic Rochester (MN): 15,000 ECG records (2015-2019)
2. Cleveland Clinic (OH): 18,000 ECG records (2016-2020)
3. Johns Hopkins (MD): 17,000 ECG records (2017-2020)

**Total Sample:** 50,000 ECG records with corresponding clinical outcomes.

**Study Duration:** Data collection: 2015-2020. Analysis: 2023-2024.

**Regulatory Approval:** Study was determined to be exempt from IRB review under FDA regulations
(45 CFR 46.102(c)) because it used de-identified data from an existing clinical database.
All patient identifiers were removed prior to analysis.

**Study Population:** Adult patients (18-85 years) with ECG recordings from hospital or clinic
settings. Inclusion criteria: (1) Valid 12-lead ECG recording; (2) Clinical outcome documented
within 30 days of ECG (diagnosis of AF or confirmation of normal sinus rhythm).

**Sample Size Justification:** For detecting AF sensitivity >90% with 95% confidence interval
width of +/- 2%, we required n>2,000 AF-positive cases (calculated using binomial distribution).
Our AF-positive sample of 12,500 (25% of total 50,000) provides >99% power for this analysis.
Specificity analysis required n>3,000 non-AF cases, met by 37,500 non-AF records."

---

### 1.2 Study Protocol and IRB Approval

[INSERT: Protocol details]

Example: "**Study Protocol:** A written study protocol was developed and followed for all
analyses. The protocol specified:
- Inclusion/exclusion criteria (below)
- Data collection and quality control procedures
- Endpoint definitions and reference standard methodology
- Statistical analysis plan (pre-specified before data analysis)
- Subgroup analyses of interest

**IRB Approval/Exemption:** Study was submitted to the Johns Hopkins Institutional Review Board
(IRB00021970) and determined to be **exempt** from full review under 45 CFR 46.101(b)(4)
because it involved analysis of de-identified, existing data and posed no more than minimal
risk to subjects. Exemption letter dated [DATE] is included in Appendix A.

Note: Although exempted, the study was conducted according to Good Clinical Practice (GCP)
principles and FDA regulations (21 CFR Part 11, electronic records). All analyses were
pre-specified before unblinded data review (analysis plan locked 2023-10-15)."

---

## 2. Study Population and Dataset Characterization

### 2.1 Inclusion and Exclusion Criteria

Define exactly who was included in the study.

[INSERT: Inclusion/exclusion]

Example: "**Inclusion Criteria (ALL must be met):**
1. Age 18-85 years at time of ECG recording
2. Clinically indicated 12-lead ECG acquired using standard hospital equipment (GE, Philips, Schiller, Mortara)
3. Complete 12-lead ECG (all 12 leads present and interpretable)
4. ECG recording duration between 8-12 seconds at 500 Hz sampling rate
5. Clinical outcome documented within 30 days of ECG:
   - AF diagnosis confirmed by: (a) clinical documentation of AF; OR (b) Holter/event monitor
     showing AF episode; OR (c) permanent pacemaker/ICD log showing AF detection
   - Non-AF diagnosis confirmed by: (a) clinical documentation of sinus rhythm; OR (b)
     longitudinal follow-up (minimum 1 year) with no AF diagnosis or treatment
6. High-quality ground truth: For AF cases, independent consensus review by >=2 cardiologists;
   for non-AF cases, clinical consensus

**Exclusion Criteria (ANY reason for exclusion):**
1. Pacemaker or ICD implant at time of ECG (artifact precludes analysis)
2. Implantable electrical cardiac devices (ventricular assist device, etc.)
3. Poor signal quality: >30% baseline artifact, >50% missing data on any lead
4. Non-standard ECG format (single-lead, wireless devices, non-standard sampling rates)
5. Insufficient clinical follow-up (outcome unknown)
6. Conflicting clinical documentation (charting errors preventing gold standard establishment)
7. Acute myocardial infarction within 48 hours (confounding ST changes)
8. Ventricular fibrillation, ventricular tachycardia, or other life-threatening rhythm at time of ECG
9. Pediatric patients (<18 years) or elderly >85 years (outside IFU)
10. Duplicate ECGs from same patient within 30 days (only first ECG included to avoid dependence)

**Justification for Exclusions:**
- Pacemaker/ICD exclusion: Device artifact makes AF detection unreliable; not clinically relevant
- Signal quality exclusion: Poor data leads to uninterpretable ground truth; violates data quality assumptions
- Acute MI exclusion: ST-segment changes can mimic AF patterns; confounds model learning
- Duplicate ECGs: Repeated measurements from same patient violate statistical independence assumption
- Age exclusion: Outside labeled intended use population; would require separate sub-group analysis"

---

### 2.2 Dataset Characterization

Provide detailed statistics on the study population.

[INSERT: Demographics and clinical characteristics]

Example: "**Overall Dataset Characteristics (n = 50,000 ECG records):**

| Characteristic | Count | Percentage | Mean (SD) | Range |
|---|---|---|---|---|
| **Demographics** | | | | |
| Age (years) | | | 67.2 (13.4) | 18-85 |
| <45 years | 4,230 | 8.5% | | |
| 45-65 years | 18,902 | 37.8% | | |
| >65 years | 26,868 | 53.7% | | |
| Sex | | | | |
| Female | 21,340 | 42.7% | | |
| Male | 28,660 | 57.3% | | |
| Race/Ethnicity | | | | |
| Caucasian | 40,870 | 81.7% | | |
| African-American | 5,895 | 11.8% | | |
| Asian | 1,832 | 3.7% | | |
| Hispanic | 985 | 2.0% | | |
| Other | 418 | 0.8% | | |
| **Clinical Status** | | | | |
| AF at time of ECG | 12,500 | 25.0% | | |
| Paroxysmal AF | 4,375 | 8.8% of total | | |
| Persistent/permanent AF | 8,125 | 16.2% of total | | |
| Non-AF (normal/other rhythm) | 37,500 | 75.0% | | |
| Normal sinus rhythm | 33,420 | 66.8% of total | | |
| Other (PVC, AV block, etc.) | 4,080 | 8.2% of total | | |
| **Clinical Context** | | | | |
| Inpatient/Hospital | 28,500 | 57.0% | | |
| Outpatient/Clinic | 21,500 | 43.0% | | |
| **Comorbidities** | | | | |
| Known hypertension | 35,800 | 71.6% | | |
| Known heart failure | 8,750 | 17.5% | | |
| Prior MI | 4,230 | 8.5% | | |
| Diabetes mellitus | 12,430 | 24.9% | | |

**Subgroup Sample Sizes (important for stratified analysis):**

| Subgroup | Total N | AF Cases | Sensitivity 95% CI Width | Specificity 95% CI Width |
|---|---|---|---|---|
| Female | 21,340 | 5,080 | ~+/- 1.9% | +/- 1.2% |
| Male | 28,660 | 7,420 | ~+/- 1.6% | +/- 1.0% |
| Age <45 | 4,230 | 425 | ~+/- 4.8% | +/- 2.1% |
| Age 45-65 | 18,902 | 3,850 | ~+/- 2.5% | +/- 1.4% |
| Age >65 | 26,868 | 8,225 | ~+/- 1.8% | +/- 1.1% |
| Caucasian | 40,870 | 10,500 | ~+/- 1.4% | +/- 0.9% |
| African-American | 5,895 | 1,400 | ~+/- 3.4% | +/- 2.1% |
| Asian | 1,832 | 410 | ~+/- 6.2% | +/- 3.8% |

**Data Provenance:** ECG recordings were extracted from institutional EHR systems using
standardized HL7 interfaces. Clinical outcomes (AF diagnosis, non-AF confirmation) were
extracted from physician notes, discharge summaries, and structured EHR data elements.
Data quality checks ensured internal consistency (age at ECG <= age at outcome, etc.)."

---

## 3. Reference Standard (Ground Truth)

### 3.1 Reference Standard Definition

How was the clinical "gold standard" determined?

[INSERT: Reference standard methodology]

**FDA expects:**
- Rigorous definition of disease presence/absence
- Independent determination (not influenced by device output, which would bias results)
- High inter-rater agreement (kappa >0.80 for subjective standards)
- Validation of reference standard itself (how do you know it's accurate?)

Example: "**Reference Standard for Atrial Fibrillation:**

AF diagnosis was established using a hierarchical algorithm prioritizing objective over subjective data:

1. **Objective confirmation (preferred):** Electrographic evidence of AF on:
   - Continuous cardiac monitoring (Holter, telemetry, event monitor) within 7 days of index ECG
   - Permanent pacemaker or ICD device interrogation log showing AF episodes
   - Electrocardiographic documentation by cardiologist-reviewed ECG or monitoring strip
   showing characteristic AF findings: irregular RR intervals (defined as coefficient of variation
   of RR intervals >15%), lack of distinct P waves, irregular baseline 'f' waves
   
2. **Clinical documentation (secondary):** When objective confirmation unavailable:
   - Physician progress note explicitly documenting 'Atrial Fibrillation' diagnosis within 30 days
   - Clinical decision to initiate AF-specific treatment (anticoagulation, rate/rhythm control)
     documented in medication orders or discharge summary
   - Supported by complementary findings (elevated BNP, clinical symptoms of palpitations/SOB
     consistent with AF presentation)

3. **Longitudinal confirmation for presumed non-AF:** For ECG records without immediate AF
   documentation, clinical diagnosis of 'sinus rhythm' was confirmed by:
   - Minimum 12 months clinical follow-up with no AF diagnosis or treatment initiation
   - Absence of AF-related diagnoses or procedures in longitudinal record
   - Absence of anticoagulation initiated post-ECG (would suggest previously undiagnosed AF)

**Reference Standard Validation:**

For all AF-positive cases (n=12,500), the reference standard was independently verified by
a second cardiologist blind to the index ECG findings. Inter-rater agreement (Cohen's kappa)
was calculated:
- Objective confirmation cases (n=11,200): kappa = 0.92 [95% CI: 0.90-0.94] (almost perfect agreement)
- Clinical documentation only (n=1,300): kappa = 0.73 [95% CI: 0.68-0.78] (substantial agreement)
- Overall AF diagnosis: kappa = 0.89 [95% CI: 0.87-0.91]

These kappas exceed FDA guidance threshold (>0.80) and demonstrate rigorous reference standard.

For non-AF cases (n=37,500), ground truth was considered 'confirmed' when either:
(a) Objective evidence of sinus/other non-AF rhythm (n=33,420), or
(b) 12+ months follow-up without AF (n=4,080)
No independent re-verification was performed for non-AF cases (standard practice; would be
resource-prohibitive), but secondary validation was performed via random audit (see below).

**Reference Standard Audit:** A random sample of 500 cases (10% of each outcome) was re-reviewed
by a third cardiologist to validate the reference standard itself. Agreement with primary
reference standard was kappa = 0.91 for AF cases, kappa = 0.87 for non-AF cases, supporting
the validity of the reference standard."

---

### 3.2 Blinding and Bias Prevention

Was the reference standard determination blinded to device output?

[INSERT: Blinding description]

Example: "**Blinding Protocol:**

This was a **fully blinded, retrospective analysis:**
- Reference standard (clinical AF diagnosis) was established before device testing
- Device (CardioDetect model) did not exist at the time reference standard was established
  (historical ECGs pre-date algorithm development)
- Analysts performing ground truth assessment were cardiologists with no involvement in
  algorithm development (independent medical center personnel)
- Device performance analysis was performed by separate analysts blinded to clinical outcome
  (statisticians at independent contract research organization)

**No possibility of bias:** Because reference standard was established independent of and
prior to device development, there is zero possibility of circular reasoning or outcome
expectation bias. This is the gold-standard study design for device validation.

Note: Going forward (prospective validation), blinding will be maintained by:
- Recording reference standard independently during standard clinical care
- Computing device output on independently-recorded ECG waveform
- Statistical analysis comparing these independent streams without unblinding"

---

## 4. Performance Metrics and Analysis

### 4.1 Primary Endpoints

What is the device supposed to do? Measure that.

[INSERT: Primary endpoint definition and results]

**For AI diagnostic devices, common primary endpoints:**
- Sensitivity (true positive rate): % of disease cases correctly identified
- Specificity (true negative rate): % of non-disease cases correctly excluded
- Overall accuracy: % of all cases correctly classified
- AUC-ROC: Area under receiver operating characteristic curve (summary of sensitivity/specificity trade-off)
- Negative predictive value (NPV): % of negative predictions that are correct
- Positive predictive value (PPV): % of positive predictions that are correct

Example: "**Primary Endpoint: Detection of Atrial Fibrillation**

The primary outcome was the device's ability to correctly classify 12-lead ECG recordings as
AF-present or AF-absent compared to the reference standard.

**Primary Efficacy Results (n=50,000 total):**

| Metric | Value | 95% Confidence Interval | Interpretation |
|---|---|---|---|
| **Sensitivity** | 92.1% | 90.8% - 93.2% | Of 12,500 AF cases, device correctly identified 11,513 |
| **Specificity** | 93.8% | 92.5% - 94.9% | Of 37,500 non-AF cases, device correctly excluded 35,175 |
| **Overall Accuracy** | 93.2% | 92.6% - 93.8% | Device correctly classified 46,688 of 50,000 cases |
| **Positive Predictive Value (PPV)** | 87.3% | 85.9% - 88.6% | Of cases device flagged as AF, 87.3% truly had AF |
| **Negative Predictive Value (NPV)** | 96.5% | 95.8% - 97.1% | Of cases device flagged as non-AF, 96.5% truly were non-AF |
| **AUC-ROC** | 0.9407 | 0.9368 - 0.9446 | Excellent discrimination across all decision thresholds |
| **Youden's Index** | 0.8590 | | Threshold of P(AF)=0.50 is optimal for this population |

**Clinical Interpretation:**
- Sensitivity 92.1% means device catches 92 of every 100 AF cases. The 7.9% miss rate is
  acceptable given: (1) ECG captures single moment in time; paroxysmal AF may not be present
  at recording; (2) clinical workflow includes repeat ECGs for high-risk patients; (3) other
  diagnostic modalities (Holter, event monitor) confirm AF in missed cases.
  
- Specificity 93.8% means device correctly excludes 94 of every 100 non-AF cases. The 6.2%
  false positive rate is acceptable because: (1) it is lower than the predicate (K232488) at ~8%;
  (2) false positives lead to cardiology review but not unnecessary treatment (physicians provide
  override); (3) PPV 87.3% means most positive results are true positives.

- NPV 96.5% is clinically important: if device says 'no AF', you can be quite confident (96.5%)
  it's truly negative.

**Comparison to Predicate:**
- Subject device sensitivity 92.1% vs. K232488 ~88%: Equivalent or superior
- Subject device specificity 93.8% vs. K232488 ~92%: Equivalent or superior
- Subject device AUC 0.9407 vs. K232488 ~0.91: Superior discrimination"

---

### 4.2 Secondary Endpoints

Are there any additional performance goals?

[INSERT: Secondary endpoints]

Example: "**Secondary Endpoints:**

1. **Device Processing Quality:**
   - Failure rate (input rejected): 0.8% of submitted ECGs (n=400) rejected due to quality issues
   - Most common rejection reasons: >30% artifact (45%), pacemaker detected (35%), insufficient duration (20%)
   - Interpretation: Acceptable failure rate; device appropriately refuses to analyze uninterpretable data

2. **Confidence Score Calibration:**
   - Does the model's confidence score match actual accuracy?
   - Evaluated using calibration plots (predicted probability vs. observed frequency)
   - Result: Calibration slope = 1.02 (95% CI: 0.98-1.06), intercept = -0.02 (ideal = slope 1, intercept 0)
   - Interpretation: Model is well-calibrated; confidence scores are reliable indicators of accuracy

3. **Processing Speed:**
   - Inference latency: 145 ms per ECG (median; 95% CI: 120-180 ms)
   - Meets operational requirement of <500 ms per ECG for real-time clinical workflow
   - Interpretation: Device is fast enough for clinical integration

4. **Alert Burden (False Positive Analysis):**
   - Of 2,325 false positive cases (non-AF flagged as AF):
     - 1,847 (79%) had minor ECG abnormalities (PVCs, AV block, artifact)
     - 478 (21%) had completely normal ECGs (model incorrectly classified as AF)
   - When presented to cardiologists, 63% of false positives were immediately disregarded (model override)
   - Interpretation: False positive burden is manageable; physician override reduces clinical impact"

---

## 5. Subgroup Analysis (CRITICAL FOR FDA)

### 5.1 Analysis by Sex

FDA expects equal performance in males and females. Report stratified analysis.

[INSERT: Sex stratification]

Example: "**Performance by Sex:**

| Metric | Female (n=21,340) | Male (n=28,660) | Difference | Clinical Significance |
|---|---|---|---|---|
| Sensitivity | 92.4% | 91.8% | 0.6% | No meaningful difference |
| Specificity | 94.1% | 93.6% | 0.5% | No meaningful difference |
| AUC-ROC | 0.9412 | 0.9401 | 0.0011 | Essentially identical |
| PPV | 87.6% | 87.1% | 0.5% | No meaningful difference |
| NPV | 96.8% | 96.2% | 0.6% | No meaningful difference |

**Analysis:** Performance is balanced across sexes. No evidence of sex-based performance differences.
The 0.6% sensitivity difference favors females and is not statistically significant
(p=0.15, Fisher's exact test). No sex-specific sub-groups or recommendations needed."

---

### 5.2 Analysis by Age

FDA wants to know if device works in young vs. old patients.

[INSERT: Age stratification]

Example: "**Performance by Age Group:**

| Metric | <45 yrs (n=4,230) | 45-65 yrs (n=18,902) | >65 yrs (n=26,868) | p-value |
|---|---|---|---|---|
| Sensitivity | 89.2% | 92.1% | 93.1% | 0.003 |
| Specificity | 91.8% | 94.2% | 94.1% | 0.021 |
| AUC-ROC | 0.9048 | 0.9389 | 0.9476 | <0.001 |
| AF Prevalence in Group | 10.0% | 20.4% | 30.6% | (expected) |

**Analysis:** Device performance improves with age (sensitivity 89.2% -> 93.1%, AUC 0.9048 -> 0.9476).
This trend is clinically expected:
- AF prevalence increases with age (10% in <45 to 31% in >65)
- Model trains more effectively with higher disease prevalence
- Older population is also the target use case (IFU specifies 18-85, with primary indication in older adults)

Younger patients (<45 years) represent 8.5% of dataset with 425 AF cases. Sensitivity 89.2%
is slightly lower than overall but still adequate (>88% threshold). The 95% CI is wider
(89.2% +/- 4.8%) due to smaller subgroup. No safety concern. Will monitor in post-market
surveillance with plan to re-evaluate with larger pediatric cohort if needed."

---

### 5.3 Analysis by Race/Ethnicity

This is where FDA often finds disparities. Be thorough and honest.

[INSERT: Race/ethnicity stratification]

Example: "**Performance by Race/Ethnicity:**

| Metric | Caucasian (n=40,870) | African-American (n=5,895) | Asian (n=1,832) | Hispanic (n=985) |
|---|---|---|---|---|
| Sensitivity | 92.7% | 90.4% | 88.5% | 90.1% |
| 95% CI | 91.4-93.9% | 88.8-92.0% | 84.3-92.7% | 85.2-94.6% |
| Specificity | 94.3% | 92.1% | 91.8% | 92.7% |
| 95% CI | 93.0-95.5% | 89.9-94.3% | 87.6-96.0% | 88.1-97.3% |
| AUC-ROC | 0.9463 | 0.9240 | 0.8965 | 0.9140 |
| N cases with AF | 10,500 (81.7% of total AF) | 1,400 (11.2%) | 410 (3.3%) | 190 (1.5%) |

**Disparity Analysis:**
- African-American sensitivity 90.4% vs. Caucasian 92.7%: 2.3% difference (95% CI of difference: -0.5% to 4.8%)
- Asian sensitivity 88.5% vs. Caucasian 92.7%: 4.2% difference (95% CI: -0.8% to 9.2%)
- Specificity differences are small (<2%) across all groups

**Statistical Significance:**
- Sensitivity difference by race is not statistically significant at p=0.05 for African-American
  (p=0.11, Fisher's exact test) but approaches significance for Asian (p=0.08)
- Likely due to smaller sample sizes in Asian and Hispanic groups (n=410 and n=190 AF cases)

**Clinical Significance and Action Plan:**

1. **African-American patients (n=5,895):**
   - Sensitivity 90.4% is adequate but 2.3 percentage points lower than Caucasian population
   - Performance is still comparable to predicate K232488 (~88%)
   - Larger sample size (1,400 AF cases) provides confidence in estimate
   - Action: Monitor performance in post-market use; no labeling restriction recommended
   - Future: Planned re-training with increased representation (currently 12% African-American
     in training set; target 20%)

2. **Asian patients (n=1,832):**
   - Sensitivity 88.5% is adequate but 4.2% lower than Caucasian population
   - Smaller sample size (410 AF cases) results in wider CI (84.3-92.7%); true population sensitivity
     may be higher or lower
   - Action: Include cautionary statement in labeling: 'Limited validation in Asian populations;
     recommend clinical correlation'
   - Future: Expand training data to increase Asian representation (currently 3%; target 8-10%)

3. **Hispanic patients (n=985):**
   - Limited sample (190 AF cases) with wide CI (85.2-94.6%)
   - Sensitivity 90.1% appears adequate
   - Action: Continue monitoring in post-market surveillance
   - Future: Deliberate enrollment of Hispanic patients in prospective validation

**Comparison to Predicate:**
Predicate K232488 does not report stratified performance by race/ethnicity, making direct
comparison impossible. Subject device's explicit reporting of racial disparities exceeds
predicate in transparency and meets FDA guidance on equity in AI (2023 AI Action Plan).

**Labeling Impact:**
The results above are reflected in the 'Limitations' section of labeling:
'Performance in Asian populations is limited by smaller sample sizes in validation study.
Use of device in Asian populations should be accompanied by heightened clinical vigilance.
The manufacturer is conducting additional validation with expanded Asian representation.'
"

---

### 5.4 Analysis by Disease Severity and Clinical Subgroups

[INSERT: Clinical subgroup analysis]

Example: "**Performance by AF Type:**

| AF Type | Sensitivity | Specificity | N Cases | Clinical Significance |
|---|---|---|---|---|
| **Paroxysmal AF** | 87.3% | 94.2% | 4,375 (35% of AF) | Lower sensitivity; AF may not be present on single ECG |
| **Persistent AF** | 95.2% | 93.8% | 5,125 (41% of AF) | High sensitivity; AF present on ECG |
| **Permanent AF** | 98.1% | 93.1% | 3,000 (24% of AF) | Very high sensitivity; AF continuously present |
| **Non-AF (all)** | — | 93.8% | 37,500 | — |

**Analysis:** Paroxysmal AF (AF not present at time of ECG) has lower sensitivity 87.3%,
which is expected and clinically reasonable. By definition, paroxysmal AF is not always present;
device can only detect AF if it is electrically evident on the recorded ECG. Persistent/permanent
AF has very high sensitivity (95-98%) because AF is continuously present.

Clinical interpretation: Device performance is appropriate for the clinical manifestation of AF.
A negative test does not rule out paroxysmal AF (patient may require Holter or event monitor),
but this is a limitation of ECG modality, not the device.

**Performance by Clinical Setting:**

| Setting | Sensitivity | Specificity | N | Notes |
|---|---|---|---|---|
| Inpatient/Hospital (n=28,500) | 93.2% | 93.1% | — | Sicker population; higher AF prevalence |
| Outpatient/Clinic (n=21,500) | 90.8% | 94.6% | — | Healthier population; lower AF prevalence |

Performance is adequate in both settings. Slightly lower sensitivity in outpatient setting is
due to lower disease prevalence (lower positive predictive value) and is not clinically concerning."

---

## 6. Generalization and External Validation

### 6.1 Internal Validation Strategy

How were training and test data separated? (Critical: data leakage is a common FDA concern)

[INSERT: Train/test split methodology]

Example: "**Data Splitting Methodology:**

The 50,000 ECG dataset was split into three independent, non-overlapping subsets:

1. **Training set (40,000 ECGs; 80%):**
   - Used to fit model weights (backpropagation)
   - Stratified by AF case/control and institution
   - AF prevalence: 25.0% (10,000 AF; 30,000 non-AF)
   - Institutions: Mayo 12,000 / Cleveland 14,400 / Johns Hopkins 13,600

2. **Validation set (5,000 ECGs; 10%):**
   - Used for hyperparameter tuning and early stopping (not to fit weights)
   - Stratified by AF case/control and institution
   - AF prevalence: 25.0% (1,250 AF; 3,750 non-AF)
   - Institutions: Mayo 1,500 / Cleveland 1,800 / Johns Hopkins 1,700

3. **Test set (5,000 ECGs; 10%):**
   - Held out and never used during training or hyperparameter tuning
   - Unlocked only after final model submission (no post-hoc tuning)
   - Stratified by AF case/control and institution
   - AF prevalence: 25.0% (1,250 AF; 3,750 non-AF)
   - Institutions: Mayo 1,500 / Cleveland 1,800 / Johns Hopkins 1,700

**Prevention of Data Leakage:**
- Splitting was done at ECG-level (not patient-level), but analysis verified no patient
  had multiple ECGs in both train and test sets
- Data split was performed before any exploratory data analysis on test set
- Test set was never accessed during model development
- Statistical analysis plan was pre-registered before test set unlock
- Test set results are reported in a locked, submitted report (no revision post-analysis)

**Justification for 80/10/10 split:**
- 80% training set is adequate for deep learning with 40,000 ECGs (>2,000 AF examples per epoch)
- 10% validation set provides stable estimates for early stopping
- 10% test set (5,000 ECGs) is large enough for narrow 95% CIs (<2% for sensitivity/specificity)

**Statistical Independence Verification:**
- Checked for repeated measures: 3 patients had >1 ECG in dataset; their additional ECGs were
  removed (rare; didn't materially affect analysis)
- Cross-validated that no single institution dominates train/validation/test (balanced 30% each)
- Verified AF prevalence is balanced across splits (25% +/- 0.1%)"

---

### 6.2 External Validation

Did you test on completely independent data from other institutions?

[INSERT: External validation results]

Example: "**External Validation Cohort:**

After completing internal development and testing, the finalized model was evaluated on
independent data from a fourth institution not included in training:

- Institution: Vanderbilt University Medical Center (Nashville, TN)
- Sample: 3,000 ECG records acquired 2021-2023
- AF cases: 680 (22.7% prevalence)
- Collection: De-identified, prospective collection from routine clinical care
- Ground truth: Cardiologist interpretation + 90-day clinical outcomes

**External Validation Results (n=3,000):**

| Metric | Subject Device | Internal Test Set | Difference |
|---|---|---|---|
| Sensitivity | 91.0% | 92.1% | 1.1% |
| Specificity | 92.8% | 93.8% | 1.0% |
| AUC-ROC | 0.9318 | 0.9407 | 0.0089 |
| PPV | 85.7% | 87.3% | 1.6% |
| NPV | 95.8% | 96.5% | 0.7% |

**Analysis:** External validation performance is consistent with internal test set, with
differences <1.1% on all metrics. This demonstrates the model generalizes well to new data
from a different institution, suggesting low overfitting risk and good real-world performance.

The slight decrease in sensitivity (92.1% -> 91.0%) is expected with external data and is
not clinically meaningful. Performance exceeds the predicate K232488 (~88%) in external validation."

---

## 7. Failure Mode Analysis

### 7.1 Conditions Where Device Underperforms

Be honest about limitations. Where does the device fail?

[INSERT: Failure mode analysis]

Example: "**Identified Failure Modes:**

1. **High Heart Rate (>120 BPM):**
   - Sensitivity drops to 84.2% (vs. overall 92.1%)
   - Reason: Model trained primarily on rates <110 BPM; high rate causes compressed ECG intervals
   - Cases affected: ~8% of test set
   - Mitigation: Labeling includes warning; recommend manual review of tachycardic ECGs

2. **Extensive Artifact (15-30%):**
   - Sensitivity drops to 79.5%; specificity drops to 88.1%
   - Reason: Neural network cannot distinguish AF waves from electrical noise
   - Cases affected: ~2% of test set (most >30% artifact are rejected by QC filter)
   - Mitigation: Automated artifact detection triggers manual review flag

3. **Severe Bradycardia (<45 BPM):**
   - Sensitivity drops to 81.3%
   - Reason: Model less trained on extreme bradycardia; AV blocks and junctional rhythms are rare
   - Cases affected: <1% of test set
   - Mitigation: None needed; population is rare; clinical indication is AF detection (not bradycardia management)

4. **Asian Race/Ethnicity:**
   - Sensitivity 88.5% (vs. overall 92.7%)
   - Reason: Training data underrepresentation (only 3% Asian vs. 82% Caucasian)
   - Cases affected: ~4% of test set
   - Mitigation: Labeling includes recommendation for heightened clinical vigilance in Asian populations;
     future retraining planned

5. **Paroxysmal AF Not Present at Time of ECG:**
   - Sensitivity 87.3% (vs. overall 92.1%)
   - Reason: Cannot detect AF if not electrically present on single ECG
   - Cases affected: ~35% of AF cases in population (expected and inherent to modality)
   - Mitigation: Clinical workflow includes repeat ECGs and other monitoring modalities for high-risk patients

**Summary of Failure Modes:**
The device has been explicitly characterized for conditions where it underperforms. The most
concerning failure modes (artifact, extreme heart rates) are rare (<2% of cases) and/or handled
by automated detection. The most clinically important limitation (paroxysmal AF) is a modality
limitation (ECG), not a device limitation, and is addressed in clinical workflow. Labeling
includes all identified failure modes and recommended mitigations."

---

## 8. Statistical Methods

### 8.1 Analysis Plan and Methods

[INSERT: Statistical methods]

Example: "**Primary Analysis (Intent-to-Analyze):**
- Population: All ECGs in test set (n=5,000), regardless of image quality or other factors
  (all passed input validation criteria)
- Test set: 5,000 independent ECGs; 1,250 AF, 3,750 non-AF
- Primary metrics: Sensitivity and specificity calculated as:
  - Sensitivity = True Positives / (True Positives + False Negatives) = TP / P
  - Specificity = True Negatives / (True Negatives + False Positives) = TN / N
- Confidence intervals: Wilson score method (recommended by FDA for proportions), 95% CI
- Statistical significance: All p-values are two-sided; alpha=0.05

**Subgroup Analyses:**
- Stratified by sex, age, race, AF type, clinical setting
- Separate sensitivity/specificity calculations for each stratum
- Comparison: Fisher's exact test (comparing two proportions across strata)
- Multiple comparisons: Bonferroni correction applied (alpha=0.05 / number of tests)

**Model Calibration Assessment:**
- Calibration plot: Plot predicted probability vs. observed frequency
- Hosmer-Lemeshow test: Chi-square test of calibration (p>0.05 = well-calibrated)
- Calibration slope and intercept: Logistic regression of outcome on predicted probability

**Secondary Analyses:**
- ROC curve: Plot sensitivity vs. (1-specificity) across all possible thresholds
- Threshold optimization: Find threshold that maximizes Youden's index (sensitivity + specificity - 1)
- Confidence interval for AUC: Non-parametric (DeLong method)

**Missing Data:**
- No missing data in test set (all 5,000 ECGs had complete ground truth labels)
- Analyses were intent-to-analyze (no post-hoc exclusions)

**Computational Methods:**
- All analyses conducted in Python 3.11 using scikit-learn 1.3.2 and scipy 1.11.0
- Numerical precision: 64-bit floating point (IEEE 754); no precision loss
- Results reproducible with fixed random seed (seed=42) and locked code repository
- Code is available at [GitHub repo] for transparency and FDA verification"

---

## Checklist Before Finalizing

- [ ] Study design is prospective or retrospective with clear inclusion/exclusion criteria
- [ ] Dataset is large enough (>1,000 AF cases for sensitivity CI <2%) and from multiple centers if possible
- [ ] Reference standard is rigorous (inter-rater agreement >0.80) and established independently
- [ ] Primary endpoints clearly show sensitivity, specificity, AUC-ROC with 95% CIs
- [ ] Subgroup analyses (sex, age, race) show balanced performance or document disparities with mitigation plans
- [ ] External validation on independent data shows consistency
- [ ] Failure modes are identified and honest (where does device underperform?)
- [ ] Train/test split prevents data leakage (test set never used during development)
- [ ] Statistical methods are pre-specified (analysis plan locked before test set unlock)
- [ ] Comparison to predicate shows equivalent or superior performance
- [ ] All metrics and CIs are reported to 1 decimal place (precision appropriate to sample size)
- [ ] Any performance disparities in underrepresented populations are acknowledged and have mitigation plans
