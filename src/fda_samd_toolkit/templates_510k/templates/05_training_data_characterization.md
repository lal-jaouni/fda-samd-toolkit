# Training Data Characterization for AI/ML Medical Devices

## Overview
FDA's AI/ML guidance (Dec 2024) makes training data characterization a major submission requirement.
Reviewers care about:
1. Is the training data representative of the intended clinical population?
2. Are there systematic biases (e.g., predominantly male, Caucasian, younger)?
3. How was ground truth established? How reliable is it?
4. What quality control was applied to training data?
5. What data shifts or distribution changes might cause performance degradation?

**FDA Guidance:** Transparent data characterization builds confidence that the model will work
in diverse real-world settings. Hiding limitations (e.g., homogeneous training population) is
a major red flag.

---

## Template

## 1. Training Data Overview

### 1.1 Training Dataset Summary

Provide basic facts about your training data.

[INSERT: Dataset overview]

Example: "The neural network was trained on **200,000 ECG recordings** from three academic medical
centers acquired between 2015-2020:

| Institution | Records | AF Cases | Percentage |
|---|---|---|---|
| Mayo Clinic Rochester, MN | 80,000 | 20,000 | 25% |
| Cleveland Clinic, OH | 72,000 | 17,280 | 24% |
| Johns Hopkins, MD | 48,000 | 12,000 | 25% |
| **Total** | **200,000** | **49,280** | **24.6%** |

**Data Collection Period:** 2015-2020 (de-identified retroactively; HIPAA compliant)
**Ground Truth Method:** Cardiologist consensus + clinical diagnosis confirmation
**Data Format:** HL7 v2.5 ECG messages extracted from hospital ECG management systems
**Labeling:** 98.5% automated (ICD-10 code 'I48' for AF); 1.5% manual chart review for ambiguous cases
**Quality Control:** Three-stage QC process (Section 3)"

---

### 1.2 Dataset Composition and Class Balance

What is the ratio of positive (AF) to negative (non-AF) cases?

[INSERT: Class balance analysis]

Example: "**Class Distribution:**

| Outcome | Cases | Percentage | Comments |
|---|---|---|---|
| AF (Atrial Fibrillation) | 49,280 | 24.6% | 35% paroxysmal, 50% persistent, 15% permanent |
| Non-AF (Normal/Other) | 150,720 | 75.4% | 89% normal sinus rhythm, 11% other rhythms (PVCs, AV block) |
| **Total** | **200,000** | **100%** | — |

**Class Imbalance Analysis:**
The dataset is naturally imbalanced (25% AF, 75% non-AF), reflecting real-world ECG populations
in hospital settings. This imbalance was addressed during training:
- **Class weights:** Non-AF = 0.35, AF = 2.80 (computed as total_samples / (2 * class_samples))
  This upweights AF cases during backpropagation to balance learning
- **Focal loss:** Alternative to cross-entropy that down-weights easy negatives and focuses on hard examples
- **Threshold optimization:** Youden's index used instead of default 0.5 probability threshold

**Justification:** Imbalanced training data reflects real clinical practice. Addressing imbalance
during training (class weights, focal loss) is standard deep learning practice and prevents the
model from being biased toward the majority class (over-predicting non-AF)."

---

## 2. Training Data Demographics

### 2.1 Demographic Breakdown

How representative is your training data of the intended population?

[INSERT: Demographics]

Example: "**Demographics of Training Dataset (n=200,000):**

| Characteristic | Count | Percentage | Mean (SD) | Range |
|---|---|---|---|---|
| **Age** | | | | |
| Mean age (years) | | | 66.8 (13.2) | 18-85 |
| <45 years | 14,200 | 7.1% | | |
| 45-65 years | 76,800 | 38.4% | | |
| 65-75 years | 76,520 | 38.3% | | |
| >75 years | 32,480 | 16.2% | | |
| **Sex** | | | | |
| Female | 84,200 | 42.1% | | |
| Male | 115,800 | 57.9% | | |
| **Race/Ethnicity** | | | | |
| Caucasian | 164,420 | 82.2% | | |
| African-American | 23,600 | 11.8% | | |
| Asian | 6,800 | 3.4% | | |
| Hispanic | 3,800 | 1.9% | | |
| Other | 1,380 | 0.7% | | |
| **Comorbidities** | | | | |
| Hypertension | 143,600 | 71.8% | | |
| Heart failure | 35,200 | 17.6% | | |
| Diabetes | 49,800 | 24.9% | | |
| Prior MI | 17,200 | 8.6% | | |
| COPD | 29,600 | 14.8% | | |

**Demographic Assessment Against Intended Population:**

IFU specifies intended population: Adults (18-85) with known/suspected arrhythmias in hospital settings.
- Age distribution: 18-85 (IFU compliant); well-distributed across age groups with appropriate
  representation in target age range (>65 years: 54.5% of training data)
- Sex distribution: 58% male, 42% female (reflects hospital population; slight male predominance
  is clinically expected for AF)
- Race/Ethnicity: 82% Caucasian, 12% African-American, 3% Asian, 2% other
  - Limitation: Caucasian over-representation (US population ~60% Caucasian)
  - Mitigation: Stratified performance analysis (Section 5.3 of Performance Testing);
    planned rebalancing in future versions
- Comorbidities: High prevalence of hypertension (72%), heart failure (18%), diabetes (25%)
  consistent with AF risk factors and target population

**Diversity Assessment:** Training data reflects major U.S. demographic groups but with limitations
in Asian and Hispanic representation. Sub-group performance analysis in main validation study
addresses this limitation."

---

### 2.2 Data Stratification by Subgroup

Provide demographic breakdown by outcome (AF vs. non-AF).

[INSERT: Stratified demographics]

Example: "**Demographics by Atrial Fibrillation Status:**

| Characteristic | AF Cases (n=49,280) | Non-AF (n=150,720) | p-value |
|---|---|---|---|
| Mean age | 71.2 (11.3) | 65.4 (13.8) | <0.001 |
| **Age groups** | | | |
| <45 years | 2.1% | 8.9% | |
| 45-65 years | 28.3% | 41.2% | |
| >65 years | 69.6% | 49.9% | |
| **Sex (Male)** | 64.2% | 55.1% | <0.001 |
| **Race (Caucasian)** | 85.4% | 81.0% | <0.001 |
| **Race (African-American)** | 10.8% | 12.3% | — |
| **Race (Asian)** | 2.1% | 4.0% | — |
| **Hypertension** | 81.2% | 68.4% | <0.001 |
| **Heart Failure** | 28.7% | 13.5% | <0.001 |
| **Diabetes** | 32.1% | 21.8% | <0.001 |

**Analysis:** AF population is older (mean 71 vs. 65 years), more male (64% vs. 55%), with
higher burden of comorbidities. These differences are clinically expected (age and comorbidity
are AF risk factors). The stratified demographics ensure the training data reflects the disease
process, not just the clinical setting."

---

## 3. Data Quality Control

### 3.1 Quality Control Process

Describe the multi-stage process used to validate training data.

[INSERT: QC methodology]

Example: "**Three-Stage Quality Control Process:**

**Stage 1: Automated Data Validation (100% of records)**
- Check 1: ECG waveform completeness (all 12 leads present)
- Check 2: Sampling rate validation (500 Hz +/- 5%)
- Check 3: Duration validation (8-12 seconds)
- Check 4: Voltage range (within -5 to +5 mV on all leads)
- Check 5: Digital artifact detection (entropy-based signal quality score)
- Result: 204,000 records submitted; 4,000 (1.96%) rejected for data quality issues

**Stage 2: Ground Truth Validation (100% of remaining 200,000 records)**
- Method: Automated matching of ECG ID to clinical outcome in EHR
- Outcome: AF diagnosis confirmed by:
  (a) Cardiologist interpretation of same ECG, OR
  (b) Clinical diagnosis of AF in chart within 30 days, OR
  (c) AF detected on monitoring device (Holter, event monitor, pacemaker)
- Non-AF confirmed by: Sinus rhythm documentation or 12+ months without AF diagnosis
- Result: 98.5% of records matched automatically; 1.5% (3,000 records) required manual chart review
- Manual review inter-rater agreement: kappa=0.89 (blind second review of 10% of manual cases)

**Stage 3: Expert Review (5% sample audit)**
- Method: Random sample of 10,000 records (5% of total) reviewed by independent cardiologist
- Auditor: Cardiologist not involved in original data collection or labeling
- Check: Verify ground truth accuracy, ECG quality, appropriateness of inclusion
- Result: 99.2% agreement with original labeling (8 discrepancies out of 10,000 audited)
- Outcome: 8 records with incorrect labels were corrected; no systematic issues identified

**Stage 4: Longitudinal Data Consistency (post-hoc, 1% sample)**
- Method: For non-AF cases, verify 12+ months follow-up without AF diagnosis
- Sample: 1,500 non-AF records; traced in EHR for minimum 12 months post-ECG
- Result: 1,498 of 1,500 (99.9%) remained non-AF at follow-up; 2 (0.1%) developed AF
  within 1 year and were reclassified
- Outcome: Minimal reclassification needed; validates reference standard

**Summary:** Multi-stage QC achieved high data quality:
- 98% of submitted data passed automated validation
- 99.2% of audited records confirmed accurate ground truth
- <0.1% reclassification rate for longitudinal consistency
- Rejected records (n=4,000) were analyzed for patterns (Section 3.3)"

---

### 3.2 Handling of Data Artifacts and Anomalies

What problems were found in the data, and how were they handled?

[INSERT: Artifact analysis]

Example: "**Common Data Artifacts and Handling:**

| Artifact Type | Prevalence | Cause | Handling |
|---|---|---|---|
| Pacemaker artifact | 2.1% of all records | 1,900 patient records with implanted pacemakers | Excluded from training (IFU excludes pacemaker patients) |
| Electrical noise (50/60 Hz) | 8.4% | Inadequate shielding during ECG acquisition | Trained preprocessing filter includes notch filter; retained with artifact flag |
| Baseline wander | 12.3% | Loose electrodes, patient movement | Butterworth high-pass filter (0.5 Hz) handles this; retained |
| Signal saturation (flat ECG) | 0.6% | ECG machine malfunction | Excluded; indicative of equipment failure |
| Duplicate or near-duplicate records | 3.2% | Same patient multiple recordings on same day | Kept all (represent natural temporal variation within single day) |
| Missing segments (<5 seconds) | 0.4% | Data transmission error | Excluded (insufficient duration) |
| Electrode swap (wrong lead order) | 0.1% | Manual data entry error | Identified via QA heuristics and corrected |

**Outlier Analysis:**
- Identified 127 outlier records with extreme ECG features (very high/low heart rate, unusual morphology)
- Manual review: 118 were valid clinical findings (extreme tachycardia, severe bradycardia);
  9 were data quality issues
- Decision: Retained valid outliers; rejected 9 with data quality issues
- Justification: Outliers represent real clinical presentations; model must learn these cases

**Missing Data:**
- No missing data by design: dataset excluded any records with incomplete ground truth labels
- Systematic absence: Pediatric records (<18 years) and patients >85 were intentionally excluded
  (outside IFU); not missing data, but exclusion criteria"

---

### 3.3 Data Retention Policies

Were any records intentionally excluded from training? If so, why?

[INSERT: Exclusion criteria for training data]

Example: "**Training Data Exclusion Criteria:**

Applied to 204,000 submitted records; 4,000 (1.96%) excluded for the following reasons:

| Reason | Count | Percentage | Justification |
|---|---|---|---|
| **Quality Issues** | | | |
| Signal quality <60% (automated QC) | 1,840 | 46.0% | Insufficient data to train model; uninterpretable ground truth |
| Missing/corrupted data segments | 650 | 16.3% | Incomplete records; violate input specifications |
| Non-standard ECG format | 280 | 7.0% | Single-lead or non-standard sampling; outside IFU |
| **Population Exclusions** | | | |
| Age <18 or >85 years | 620 | 15.5% | Outside IFU; would require separate sub-group analysis |
| Pacemaker/ICD in situ | 380 | 9.5% | Contraindicated in IFU; introduces device artifact |
| **Ground Truth Issues** | | | |
| Conflicting clinical documentation (cannot establish AF status) | 150 | 3.8% | Ambiguous outcome; violates reference standard requirement |
| **Total Excluded** | **3,920** | **98.0%** | — |
| **Total Retained** | **200,080** | **100.0%** | — |

*Note: Small rounding discrepancies due to some records meeting multiple exclusion criteria.*

**Justification:** Exclusions were applied systematically and documented. Excluded records
(n~4,000) represent <2% of submission and were excluded for valid reasons (data quality,
safety contraindications, population boundaries). Retention of 200,000 records is large
enough to train robust model without concern that exclusions biased the result."

---

## 4. Ground Truth and Annotation Methods

### 4.1 Ground Truth Establishment

How was AF diagnosis confirmed in training data?

[INSERT: Ground truth methodology]

Example: "**Three-Tier Hierarchy for Ground Truth (AF cases):**

**Tier 1: Objective Electrographic Confirmation (78.2% of AF cases, n=38,574)**
Highest confidence ground truth. Requires documented AF on:
- Same-day 12-lead ECG interpreted by board-certified cardiologist as AF, OR
- Continuous monitoring (Holter, telemetry, event monitor) within 7 days showing irregular RR intervals + absent P waves, OR
- Device interrogation (pacemaker/ICD log) documenting AF episodes

Process:
1. Extract ECG and any associated monitoring records from EHR
2. Automated detection: Search for AF diagnosis codes (ICD-10 I48, I48.0-I48.9)
3. Manual verification: Cardiologist confirms diagnosis on electrogram
4. Annotation: Labeled AF=1 with evidence code E1 (electrographic)

Example records:
- ECG dated 2019-03-15 interpreted as 'Atrial fibrillation' with irregular RR intervals visible
- Holter monitor dated 2019-03-16 showing 2-hour AF episode
- Both confirm same-patient AF diagnosis within 24 hours

**Tier 2: Clinical Documentation (19.2% of cases, n=9,475)**
Secondary confirmation when objective data unavailable. Requires documented AF in clinical note + treatment evidence.

Process:
1. Search clinical notes for AF diagnosis (within 30 days of index ECG)
2. Cross-check with treatment: anticoagulation order, rate/rhythm control medication, ablation referral
3. Exclude if conflicting documentation (e.g., 'rule out AFib' without confirmation)
4. Annotation: Labeled AF=1 with evidence code E2 (clinical)

Example records:
- ED note 2019-03-15: 'Patient presenting with palpitations, irregular pulse. EKG shows atrial fibrillation.
  Cardiology called. Started on metoprolol.'
- Discharge summary lists AF as active diagnosis
- Anticoagulation (apixaban) prescribed
- Record confirmed as AF despite not having objective monitoring

**Tier 3: Longitudinal Confirmation (2.6% of cases, n=1,231)**
For records lacking immediate objective/clinical documentation. Requires either:
- Retrospective diagnosis: AF diagnosed in follow-up clinical notes (30-90 days post-ECG)
  AND clinical intervention (anticoagulation, ablation referral)
- Prospective diagnosis: Documented AF diagnosed within 1 year of index ECG on any modality

Process:
1. Conduct chart review for minimum 1-year follow-up post-ECG
2. Identify any documentation of AF diagnosis or treatment initiation
3. Annotation: Labeled AF=1 with evidence code E3 (longitudinal)
4. Note: These cases increase annotation latency but minimize false negatives

Example records:
- ECG dated 2019-03-15 documented as 'sinus rhythm' at time
- Holter monitor ordered 6 weeks later (2019-05-01) shows AF episodes
- Cardiologist documents 'newly diagnosed paroxysmal AF' and starts anticoagulation
- Record reclassified AF=1 based on longitudinal confirmation

**Ground Truth Confidence Scores:**
- Tier 1 (electrographic): Confidence 0.98 (99.5% inter-rater agreement in sample audit)
- Tier 2 (clinical): Confidence 0.92 (89.2% inter-rater agreement)
- Tier 3 (longitudinal): Confidence 0.88 (85.1% inter-rater agreement)

Overall weighted ground truth confidence: (0.78 x 0.98) + (0.19 x 0.92) + (0.026 x 0.88) = 0.96
This exceeds FDA guidance minimum (>0.90) for acceptable reference standard."

---

### 4.2 Ground Truth for Non-AF Cases

How was non-AF confirmed in training data?

[INSERT: Non-AF ground truth]

Example: "**Confirmation of Non-AF Cases (n=150,720):**

**Tier 1: Documented Sinus Rhythm (89.1% of non-AF cases, n=134,168)**
- Same-day 12-lead ECG interpreted by cardiologist as 'normal sinus rhythm' or 'no AF'
- Automated detection: Search for absence of AF codes + presence of 'NSR' or 'normal' codes
- Manual spot-check: Random sample of 5% (n=6,708) reviewed by independent cardiologist
  to verify absence of AF
- Confidence: 99.1% agreement (only 60 records had evidence of missed AF on independent review)
- Outcome: 60 records with missed AF were reclassified to AF group

**Tier 2: No AF on Longitudinal Follow-up (10.9% of non-AF cases, n=16,440)**
- Definition: Records without immediate AF documentation but no AF diagnosis after minimum
  12 months clinical follow-up
- Method:
  1. Identify records without AF diagnosis at index ECG
  2. Trace in EHR for minimum 12 months
  3. Verify no AF-related diagnoses, treatments, or hospitalizations
  4. Verify no anticoagulation initiated (would suggest undiagnosed AF)
- Confidence: 99.7% remain non-AF at follow-up (only 5 of 16,440 developed AF during follow-up;
  reclassified to AF group)
- Justification: 12+ month follow-up with no AF diagnosis strongly suggests true non-AF status
  (paroxysmal AF would likely manifest)

**Tier 3: Other Rhythms Confirmed (0.02% of non-AF, n=112)**
- Records with non-AF, non-sinus diagnoses (PVCs, AV block, etc.)
- Included for completeness; allows model to distinguish AF from other abnormalities
- Confidence: >98% based on documented rhythm diagnosis

**Overall Non-AF Confidence:** (0.891 x 0.991) + (0.109 x 0.997) = 0.992
Excellent reference standard for non-AF cases."

---

## 5. Annotation Quality and Inter-Rater Reliability

### 5.1 Annotation Process

Who labeled the training data? What training did they have?

[INSERT: Annotation methodology]

Example: "**Annotation Workflow:**

**Stage 1: Automated Labeling (98.5% of records)**
- Method: Deterministic algorithm matching ECG ID to EHR diagnosis codes
- Diagnosis codes: ICD-10 I48.x (Atrial fibrillation) = AF; all others = non-AF
- Confidence: High for objective cases (electrographic confirmation)
- Outcome: 197,000 of 200,000 records labeled automatically

**Stage 2: Manual Verification (1.5% of records)**
- Method: Cardiologist expert review of ambiguous or borderline cases
- Cases requiring manual review:
  - Missing or unclear diagnosis codes
  - Conflicting documentation (e.g., 'rule out AFib' vs. confirmed AF)
  - Tier 2 or Tier 3 ground truth (clinical or longitudinal confirmation)
- Annotators: 3 board-certified cardiologists (Mayo, Cleveland, Johns Hopkins)
  - All have minimum 5 years AF experience
  - All completed 2-hour training on labeling protocol (Section 5.1.1)
- Inter-rater reliability: Random sample of 500 records reviewed by all 3 annotators
  - Fleiss' kappa = 0.87 [95% CI: 0.83-0.91] (substantial agreement)
  - Discrepancies resolved by consensus review

**Stage 3: QA Audit (5% of all records)**
- Method: Independent cardiologist (not involved in labeling) reviewed random sample
- Sample: Stratified random sample of 10,000 records (5% of 200,000)
  - Stratified by: institution (balanced across Mayo, Cleveland, Johns Hopkins)
  - Stratified by: outcome (balanced AF:non-AF per original labeling)
- Results:
  - Agreement with original labels: 99.2% (9,920 of 10,000)
  - Discrepancies: 80 (0.8% mislabeled)
  - Pattern analysis: Mislabeling not systematic (spread across all institutions and outcomes)
  - Resolution: Mislabeled records corrected in final dataset
- Conclusion: Annotation quality is excellent (>99% accuracy)"

---

### 5.2 Annotation Guidelines and Conflict Resolution

[INSERT: Annotation protocol]

Example: "**Annotation Protocol for Ambiguous Cases:**

**Protocol for 'Rule Out AFib' Documentation:**
- Rule: If chart documents 'rule out AFib' but then rules it OUT (confirms non-AF), label as non-AF
- Rule: If chart documents 'rule out AFib' but then confirms AF (clinical or electrographic),
  label as AF
- Example 1 (non-AF): 'EKG concerning for AFib, but 12-lead confirms sinus rhythm.
  Symptoms likely anxiety.' -> Label: non-AF
- Example 2 (AF): 'Initial concern for AFib on telemetry; subsequent Holter shows
  documented AF episodes.' -> Label: AF

**Protocol for Multiple Conflicting Diagnoses:**
- Rule: Use most recent reliable diagnosis (within 30 days of index ECG)
- Rule: Prioritize objective (electrographic) > clinical (documented) > presumed (longitudinal)
- Example: Patient with 'AFib' documented in 2018 discharge but 'NSR' on index ECG 2019.
  Recent echo (2019) shows normal LV function. -> Label: non-AF (based on index ECG and recent documentation)

**Conflict Resolution Protocol:**
- If two cardiologists disagree on labeling: Third cardiologist provided input (by consensus)
- If all three disagree: Case reviewed in group discussion; consensus reached
- If no consensus possible: Case excluded from training (n<20 cases across entire dataset)

**Training on Protocol:**
- 2-hour training session led by study PI (cardiologist)
- Training included: 20 representative cases (10 clear AF, 10 clear non-AF)
- Training included: 10 ambiguous cases requiring protocol interpretation
- All annotators demonstrated 100% accuracy on training cases before independent annotation
- Protocol document (2 pages) provided as reference guide; available in appendix"

---

## 6. Data Preprocessing and Feature Engineering

### 6.1 Preprocessing Applied to Training Data

What transformations were applied to raw ECG signals?

[INSERT: Preprocessing pipeline]

Example: "**Standard Preprocessing Pipeline (applied to all 200,000 training ECGs):**

**Step 1: Signal Filtering (Linear Time-Invariant, non-causal)**
- Goal: Remove electrical noise and baseline wander without distorting ECG morphology
- Method: Butterworth IIR filter (zero-phase, applied forwards-backwards to avoid phase lag)
- Specifications:
  - High-pass filter: 0.5 Hz cutoff (removes DC offset and very slow baseline drift)
  - Low-pass filter: 100 Hz cutoff (removes 50/60 Hz electrical noise and high-frequency artifact)
  - Filter order: 4 (steep enough for artifact removal but stable)
- Rationale: Standard in clinical ECG signal processing (matches hospital ECG machine filtering)

**Step 2: Resampling (if needed)**
- Goal: Standardize all ECGs to exactly 500 Hz sampling rate
- Method: Linear interpolation
- Tolerance: If input sampling rate within 480-520 Hz, resample; otherwise reject
- Rationale: 500 Hz is standard for ECG acquisition (Nyquist rate for frequencies <250 Hz)

**Step 3: Amplitude Normalization**
- Goal: Make model robust to differences in ECG amplification across machines/clinics
- Method: Z-score normalization per lead
  - For each lead: x_norm = (x - mean) / std_dev
  - Computed across the entire 10-second window
- Rationale: Removes dependence on ECG machine gain settings and patient electrode contact quality
- Verification: All normalized leads have approximately mean=0, std_dev=1

**Step 4: Duration Standardization**
- Goal: Ensure all ECGs are exactly 10 seconds (5,000 samples at 500 Hz)
- Method:
  - If <10 seconds: Exclude (insufficient data)
  - If >10 seconds: Trim to first 10 seconds (consistent methodology)
- Rationale: Neural network requires fixed input size; 10 seconds captures ~2-3 cardiac cycles (sufficient for AF detection)

**Step 5: Data Augmentation (during training only)**
- Goal: Artificially increase dataset size and robustness to noise
- Methods:
  - Jitter: Random shift +/- 1% of signal amplitude (mimics sensor noise)
  - Temporal shift: Random 10-50 ms time shift (shift position within cardiac cycle)
  - Frequency jitter: Random +/- 2 BPM rate variation
- Frequency: 50% of training batches included augmented data
- Rationale: Improves model generalization and robustness to real-world signal variations

**Step 6: Outlier Clipping (optional, minimal impact)**
- Goal: Prevent rare extreme values from dominating training loss
- Method: Clip values >3 standard deviations from mean (per lead)
- Frequency: Applied to <0.01% of samples
- Rationale: Extreme values usually represent data artifacts rather than real physiology

**Preprocessing Validation:**
- Verified that preprocessing does NOT distort clinically important ECG features
- QA check: Compared preprocessed vs. original ECG for random sample of 100 records
  - Clinical morphology (P wave, QRS, ST segment) unchanged
  - Artifacts removed without removing true AF findings
- Conclusion: Preprocessing is appropriate and clinically validated"

---

## 7. Data Distribution and Potential Shifts

### 7.1 Source-Wise Distribution

Where did the training data come from? Are there systematic differences between sources?

[INSERT: Data source analysis]

Example: "**Training Data Distribution by Source:**

| Institution | Records | AF % | Demographics | Potential Bias |
|---|---|---|---|---|
| **Mayo Clinic (Rochester, MN)** | 80,000 (40%) | 25.0% | 85% Caucasian, 68% male, mean age 68 | Affluent Midwestern US population |
| **Cleveland Clinic (Cleveland, OH)** | 72,000 (36%) | 24.0% | 82% Caucasian, 58% male, mean age 67 | Rust Belt, slightly higher African-American representation |
| **Johns Hopkins (Baltimore, MD)** | 48,000 (24%) | 25.0% | 76% Caucasian, 51% male, mean age 65 | Urban population, greater diversity |

**Bias Assessment:**
- Geographic: 60% Midwest (Mayo + Cleveland); 24% Mid-Atlantic (Johns Hopkins); 16% other
  - Limitation: Limited West Coast, South, or international representation
  - Implication: Model may underperform in non-represented regions
  - Mitigation: Future data collection in underrepresented regions

- Demographic: 82% Caucasian overall; underrepresentation of Asian (3%) and Hispanic (2%)
  - Limitation: Known performance disparities in underrepresented groups
  - Mitigation: Stratified performance testing; explicit labeling of limitations

- Healthcare System: All three are large academic medical centers
  - Limitation: Model trained exclusively on 'ideal' settings; may underperform in community hospitals
  - Imitation: External validation should include community hospitals (ongoing prospective study)

- Temporal: All data collected 2015-2020; pre-COVID-19
  - Limitation: May not generalize to post-pandemic ECG acquisition changes (telemedicine, different populations)
  - Implication: Monitor performance on 2020+ data in post-market surveillance"

---

### 7.2 Data Shift Analysis

What distribution changes might cause the model to fail?

[INSERT: Data shift scenarios]

Example: "**Potential Data Shift Scenarios and Mitigation:**

| Shift Type | Definition | Example | Expected Impact | Monitoring |
|---|---|---|---|---|
| **Covariate Shift** | P(X) changes, P(Y\|X) stays same | More elderly patients in new populations (mean age shifts from 67 to 72) | Minimal; AF prevalence increases but model detects AF regardless of age | Monitor input age distribution |
| **Label Shift** | P(Y) changes, P(X\|Y) stays same | AF prevalence drops from 25% to 10% (due to population selection) | Minimal; doesn't affect model performance (threshold remains optimal) | Monitor AF prevalence in deployment |
| **Concept Drift** | P(Y\|X) changes | ECG acquisition standards change (different sampling rate, different equipment); patient population demographics shift | Moderate; if ECG quality differs fundamentally, model performance may degrade | Monthly performance audits on deployment data |
| **Domain Shift** | Fundamental change in X distribution | Model deployed in telehealth with single-lead ECG instead of 12-lead | Severe; outside IFU, likely to fail | Device has input validation; rejects non-12-lead |
| **Temporal Drift** | Changes over time (aging data) | Model trained on 2015-2020 data; deployed 2024 (4 years later) | Low risk; AF physiology unchanged; deployment data monitored | Annual revalidation on recent data |

**Mitigation Strategies:**
1. **Input validation:** Device rejects inputs outside specifications (non-12-lead, non-500 Hz)
2. **Output uncertainty:** Model outputs confidence scores; low confidence (<0.6) triggers manual review
3. **Prospective monitoring:** Deployment includes logging of all cases + periodic physician review
4. **Periodic revalidation:** Quarterly performance review on new deployment data; annual formal revalidation
5. **Retraining protocol:** If performance degrades >5% on deployment data, trigger retraining with recent data

**Early Warning System:**
- KPI monitoring: Alert if sensitivity drops <85% or specificity drops <90% (2-week rolling average)
- Distribution monitoring: Alert if input age distribution shifts >10% from training data
- Failure mode monitoring: Alert if false-positive rate increases >50% (suggests new artifact type)

These mitigations are detailed in Section 6 (Risk Analysis) of main submission."

---

## Checklist Before Finalizing

- [ ] Training dataset size is >30,000 cases with >1,000 positive examples (adequate for deep learning)
- [ ] Multi-center data from >=2 institutions (reduces site-specific bias)
- [ ] Demographics closely match intended population (or explicitly documented limitations)
- [ ] Ground truth is rigorous (kappa >0.80 inter-rater agreement or objective confirmation)
- [ ] Ground truth is independent of device input (no circular reasoning)
- [ ] QC process is multi-stage with explicit rejection criteria and audit results
- [ ] Data exclusions are documented and justified (not arbitrary)
- [ ] Annotation agreement is measured and acceptable (>85% agreement, ideally >90%)
- [ ] Preprocessing is clinically reasonable and doesn't distort important features
- [ ] Data shift scenarios are anticipated and mitigation strategies documented
- [ ] Training/test split is clearly described with no data leakage
- [ ] Imbalanced class distribution is addressed (class weights, focal loss, threshold optimization)
- [ ] Disparities in underrepresented populations are documented with future plans
- [ ] Temporal coverage is clear (2015-2020 in example; specify your dates)
