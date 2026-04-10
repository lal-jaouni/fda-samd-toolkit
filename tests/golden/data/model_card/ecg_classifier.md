# FDA-Extended Model Card: CardioDetect AI-ECG Classifier

**Version:** 1.2.1
**Date:** 2024-03-15
**Owner:** CardioHealth AI, Inc.
**Contact:** regulatory@cardiohealth.com

---

## 1. Model Details

**Model Name:** CardioDetect AI-ECG Classifier

**Version:** 1.2.1

**License:** MIT

**Owner/Developer:** CardioHealth AI, Inc.

**Citation:**
```
@inproceedings{cardiohealth2024,
  title={CardioDetect: Real-time AI-assisted Atrial Fibrillation Detection},
  author={Smith, J. and Johnson, M.},
  booktitle={American College of Cardiology Conference},
  year={2024}
}

```
---

## 2. Intended Use

**Primary Purpose:** Atrial fibrillation detection from 12-lead electrocardiograms in hospital and clinical settings

**Intended Users:**
- Cardiologists
- Emergency medicine physicians
- Cardiac nurses
- Cardiac technicians


**Clinical Settings:**
- Hospital cardiology departments
- Emergency departments
- Outpatient cardiology clinics
- Intensive care units


**Contraindications:**
- Patients with implanted pacemakers or ICDs (device artifact interferes with analysis)
- Pediatric patients (age <18 years; performance not evaluated)
- Acute myocardial infarction within 48 hours (ST changes confound AF detection)

**Out of Scope Uses (Explicitly Prohibited):**
- Unsupervised patient self-diagnosis (home use without clinical supervision)
- Automated treatment decisions without physician review
- Diagnosis of other cardiac arrhythmias (paroxysmal SVT, atrial flutter, ventricular arrhythmias)
- Use as sole diagnostic basis for anticoagulation initiation

---

## 3. Factors Affecting Model Performance

**Instrumentation:**
- GE MAC 5500 ECG acquisition system
- Philips PageWriter Touch ECG machine
- NVIDIA T4 GPU for inference (or compatible CPU fallback)

**Environmental Factors:**
- temperature_celsius: 15-25
- humidity_percent: <80
- altitude_feet: <8000

**Demographic Groups Evaluated:**
- sex (male/female)
- age_group (18-45, 45-65, 65-75, >75)
- race_ethnicity (Caucasian, African-American, Asian, Hispanic)
- af_type (paroxysmal, persistent, permanent)

**Datasets Used for Evaluation:**
- Mayo Clinic Rochester
- Cleveland Clinic Ohio
- Johns Hopkins Baltimore

---

## 4. Metrics

### 4.1 Overall Performance

| Metric | Value |
|--------|-------|
| sensitivity | 0.9210 |
| specificity | 0.9380 |
| accuracy | 0.9320 |
| auc_roc | 0.9407 |
| ppv | 0.8730 |
| npv | 0.9650 |
| f1_score | 0.8960 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.9080 | 0.9320 |
| specificity | 0.9250 | 0.9490 |
| auc_roc | 0.9368 | 0.9446 |

**Decision Threshold:** 0.5
**Notes:** Metrics computed on 5000-case held-out test set. Confidence intervals calculated
using Wilson score method (recommended for proportions). Subgroup analyses show
performance disparities in Asian population; planned future retraining with targeted
Asian patient enrollment.

### 4.2 Subgroup Analysis

#### Female

**Definition:** Patients with documented biological sex female

**Sample Size:** 10670

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.9240 |
| specificity | 0.9410 |
| auc_roc | 0.9412 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.9090 | 0.9370 |
| specificity | 0.9270 | 0.9530 |

#### Male

**Definition:** Patients with documented biological sex male

**Sample Size:** 14330

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.9180 |
| specificity | 0.9360 |
| auc_roc | 0.9401 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.9020 | 0.9320 |
| specificity | 0.9220 | 0.9480 |

#### Age 45-65

**Definition:** Patients aged 45-65 years at ECG acquisition

**Sample Size:** 9451

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.9210 |
| specificity | 0.9420 |
| auc_roc | 0.9389 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.9020 | 0.9380 |
| specificity | 0.9280 | 0.9540 |

#### Age >65

**Definition:** Patients aged >65 years at ECG acquisition

**Sample Size:** 13449

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.9310 |
| specificity | 0.9410 |
| auc_roc | 0.9476 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.9180 | 0.9420 |
| specificity | 0.9280 | 0.9520 |

#### Caucasian

**Definition:** Self-identified Caucasian race/ethnicity

**Sample Size:** 17210

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.9270 |
| specificity | 0.9430 |
| auc_roc | 0.9463 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.9140 | 0.9390 |
| specificity | 0.9300 | 0.9550 |

#### African-American

**Definition:** Self-identified African-American race/ethnicity

**Sample Size:** 2362

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.9040 |
| specificity | 0.9210 |
| auc_roc | 0.9240 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.8800 | 0.9250 |
| specificity | 0.8970 | 0.9410 |

#### Asian

**Definition:** Self-identified Asian race/ethnicity

**Sample Size:** 730

**Metrics:**

| Metric | Value |
|--------|-------|
| sensitivity | 0.8850 |
| specificity | 0.9180 |
| auc_roc | 0.8965 |


**95% Confidence Intervals:**

| Metric | Lower | Upper |
|--------|-------|-------|
| sensitivity | 0.8430 | 0.9270 |
| specificity | 0.8760 | 0.9600 |

---

## 5. Evaluation Data

**Datasets Used:**
- Mayo Clinic external validation cohort (n=2500, 2021-2023)
- Cleveland Clinic external validation cohort (n=1500, 2022-2023)
- Johns Hopkins prospective cohort (n=1000, 2024 ongoing)


**Motivation:** External validation datasets selected to assess real-world generalization beyond
training institutions. Prospective cohort (Johns Hopkins) provides evidence of
prospective performance without retrospective bias.

**Preprocessing:**
- Butterworth IIR filter 0.5-100 Hz (zero-phase, order 4)
- Resampling to 500 Hz if input differs (linear interpolation)
- Z-score normalization per lead (mean=0, std=1)
- Automated artifact detection and quality flagging

**Data Split:**
- training: 80.0%
- validation: 10.0%
- testing: 10.0%

**Stratification:** Stratified by diagnosis (AF positive/negative); Stratified by clinical site (balanced across 3 institutions)
---

## 6. Training Data

**Datasets:**
- Mayo Clinic Rochester ECG database
- Cleveland Clinic Ohio ECG database
- Johns Hopkins Baltimore ECG database


**Sample Size:** 200,000 examples
**Demographics:**
- mean_age_years: 66.8
- std_age_years: 13.2
- female_percent: 42.1
- male_percent: 57.9
- caucasian_percent: 82.2
- african_american_percent: 11.8
- asian_percent: 3.4
- hispanic_percent: 1.9
- other_percent: 0.7
- af_cases_percent: 24.6
- hypertension_percent: 71.8
- heart_failure_percent: 17.6
- diabetes_percent: 24.9

**Data Sources:**
- HL7 v2.5 ECG messages from hospital ECG management systems
- Clinical outcomes from electronic health records
- Monitoring device logs (Holter, pacemaker/ICD interrogations)

**Inclusion Criteria:**
- Age 18-85 years at time of ECG
- Standard 12-lead ECG from hospital equipment
- Complete 12-lead waveform with all leads interpretable
- Sampling rate 500 Hz (tolerance 480-520 Hz)
- Clinical outcome documented within 30 days
- Ground truth established via cardiologist review or clinical confirmation

**Exclusion Criteria:**
- Pacemaker or ICD implant (device artifact)
- Pediatric patients (<18 years)
- Elderly patients (>85 years, outside IFU)
- Signal quality <60% (excessive artifact)
- Non-standard ECG format (single-lead, wireless)
- Conflicting clinical documentation (indeterminate diagnosis)

**Quality Control:**
- Automated data validation (all 12 leads present, proper sampling rate and duration)
- Three-stage QC process with 99.2% accuracy on audited sample
- Inter-rater agreement verification (kappa=0.89 for manual labeling)
- Longitudinal consistency check (12+ month follow-up confirms non-AF status)

**Data Shifts Addressed:**
- Class imbalance (25% AF, 75% non-AF) addressed via class weights
- Missing data handling (excluded records with insufficient ground truth)
- Demographic underrepresentation (Asian patients: 3% of training data; flagged in caveats)

---

## 7. Ethical Considerations

**Impact Summary:** Positive: Faster AF detection assists clinicians in acute settings; can reduce diagnostic
delay and improve patient outcomes through timely intervention. Negative: False positives
may lead to unnecessary anticoagulation and bleeding risk; false negatives may delay AF
diagnosis, increasing stroke risk. Automation bias risk if physicians over-rely without
manual review. Demographic disparities in performance may disproportionately affect Asian
populations if model is deployed without explicit caveats.

**Potential Harms:**
- False negatives (missed AF) lead to delayed diagnosis and increased stroke risk
- False positives (normal rhythm flagged as AF) lead to unnecessary anticoagulation and bleeding risk
- Automation bias if physician relies solely on AI without reviewing original ECG
- Demographic disparities in performance (4.2% lower sensitivity in Asian populations) may disadvantage underrepresented groups
- Over-reliance on device in emergency settings where time pressure encourages shortcuts

**Demographic Disparities:** Sensitivity is 4.2 percentage points lower in Asian patients (88.5% vs 92.7% in Caucasian
population). Specificity is 2.5 points lower. These disparities are attributable to
underrepresentation of Asian patients in training data (3% vs 18% US population estimate).
Labeled as limitation in clinical labeling; mitigation includes explicit physician training
on disparities and planned future retraining with targeted Asian enrollment.

**Bias Mitigation Strategies:**
- Stratified performance analysis by sex, age, race; disparities quantified and documented
- Class weighting to address AF prevalence imbalance (AF weight 2.80 vs non-AF 0.35)
- Transparency in output (probabilistic scores, confidence levels, saliency maps) reduce blind trust
- Training module emphasizing known limitations and failure modes
- Labeling and disclaimers highlighting disparities and need for manual review
- Future retraining planned with expanded Asian and Hispanic representation

**Fairness Considerations:** Model exhibits measurable fairness disparity in Asian populations. Recommend heightened
clinical vigilance when deploying in Asian-serving hospitals. Current approach: transparency
+ labeling + training. Ideal future approach: equitable performance across all demographic
groups via balanced training data and continued retraining.

---

## 8. Caveats and Recommendations

**Caveats:**
- Performance not validated in pediatric patients; device contraindicated in <18 years
- Sensitivity drops to 87.3% for paroxysmal AF (not present at time of ECG); clinical workflow must include repeat monitoring
- Limited validation in Asian populations (3% of training data); recommend manual review for Asian patients
- Device performance may degrade with extreme heart rates (<45 or >120 BPM)
- Designed for standard 12-lead ECG; not compatible with single-lead or wireless devices

**Known Limitations and Failure Modes:**
- Paroxysmal AF not electrically evident on single 10-second ECG; device cannot detect if not present at acquisition time
- Model uncertainty underestimated in extreme population (confidence calibration limited to 5-95 percentile of training data)
- Fails in presence of >30% baseline artifact; flagged as manual review but may miss AF if clinician doesn't notice
- Training data skewed toward Caucasian population; model may underperform in diverse populations
- Temporal drift: training data 2015-2020; performance on recent 2024 data not yet validated

**Recommendations for Use:**
- Always review original ECG alongside AI output; never rely on device output alone
- For low-confidence results (confidence <60%), escalate to senior cardiologist for independent review
- Mandatory 15-minute training for all users covering device limitations and failure modes
- Monthly alert effectiveness audit; escalate if override rate >70% (suggests alert fatigue)
- Annual revalidation on recent deployment data; retrain if sensitivity drops >5%

**Future Improvements:** Planned improvements for v2.0: (1) Expand training data with 50% Asian representation;
(2) Add sub-second paroxysmal AF detection via longer input window; (3) Implement
domain adaptation for different ECG equipment; (4) Develop real-time monitoring module
for continuous AF detection. Timeline: annual updates; major improvements evaluated in
prospective validation before release.

---

## 9. FDA-Specific Information

**Intended Use Statement (IFU):**
The CardioDetect AI-ECG Classifier is a software-based clinical decision support system
intended to assist healthcare professionals in detecting atrial fibrillation from standard
12-lead electrocardiogram recordings. The device provides a probabilistic score for AF
presence and is intended for use by licensed cardiologists, emergency medicine physicians,
and trained cardiac professionals. The device is not intended as a standalone diagnostic
tool and does not replace clinical judgment. Physician interpretation and verification of
device output is required before any clinical action.


**FDA Classification:** Class II; 510(k) premarket submission
**Predicate Devices (510k):**
- K232488 (Anumana ECG-AI, atrial fibrillation detection)
- K233429 (Eko AI, cardiac abnormality screening)

**Substantial Equivalence Summary:** Subject device demonstrates substantial equivalence to K232488 based on: (1) identical
intended use (AF detection from 12-lead ECG); (2) identical input modality (12-lead ECG
at 500 Hz); (3) similar output (probabilistic classification); (4) non-significant
technological differences (different neural network architecture but superior performance).
Differences in model architecture (CNN vs. LSTM) are implementation details that do not
affect clinical safety or effectiveness. Performance exceeds predicate on all metrics
(sensitivity 92.1% vs 88%, specificity 93.8% vs 92%, AUC 0.9407 vs 0.91).

**Failure Modes and Mitigations:**
- Paroxysmal AF not present at time of ECG: Sensitivity 87.3% (vs 92.1% overall); mitigated by clinical workflow including repeat monitoring
- Extreme heart rate (>120 BPM): Sensitivity 84.2%; device flags as 'manual review' with warning
- Asian race/ethnicity: Sensitivity 88.5% (vs 92.7% Caucasian); mitigated by labeling and physician training
- Baseline artifact >30%: Model confidence drops <0.60; flagged as requiring manual review
- Automation bias (physician over-reliance): Mitigated by probabilistic output, confidence scoring, explainability features, training, and audit

**Drift Monitoring Plan:** Monthly: Automated KPI monitoring of sensitivity, specificity, PPV, NPV, AUC on deployment data.
Alert thresholds: sensitivity <85%, specificity <88%, false positive rate >10%.
Quarterly: Manual review of 50 random cases by independent cardiologist to assess for systematic failures.
Annual: Full revalidation study on 12 months of deployment data; compare to baseline performance.
If drift detected: Investigate root cause (data shift, equipment change, patient population change);
interim mitigation (heightened manual review) implemented; retraining triggered if sustained degradation.

**Model Update Cadence:** Minor updates (bug fixes, UI improvements): As needed, released via secure container registry.
Model retraining: If performance degrades >5% on deployment data OR new diversity goals require
retrain (planned annual diversity expansion). Major releases require abbreviated validation on
held-out test set; full validation if substantial changes to architecture or preprocessing.

**Post-Market Surveillance Plan:** Adverse event reporting: All serious adverse events (missed AF leading to stroke, false positive
leading to bleeding) reported to FDA MedWatch within 30 days. Device includes feedback mechanism
(in-app "Report Issue" button) for non-serious issues and suggestions. Monthly analysis of feedback;
trends triggering investigation. Annual summary report to FDA.

**Human Factors Summary:** Usability testing conducted with 16 clinical users (cardiologists, nurses, technicians);
95% demonstrated competency post-training. Mandatory 15-minute online training covering:
output interpretation, confidence levels, common failure modes, override procedures. Training
includes 3 realistic case studies + hands-on demo in actual EHR. Competency assessed via 5-question
quiz (pass >80%) + practical demonstration. Reassessment required annually. UI designed for
minimal cognitive load; probabilistic output with color-coded confidence reduces automation bias.

---

## 10. References and Appendices

[Add references, citations, and links to supporting documentation here]

- Mitchell et al. (2019): Model Cards for Model Reporting (https://arxiv.org/abs/1810.03993)
- FDA AI/ML Action Plan (2021)
- FDA PCCP Guidance (2024)

---

**Document Generated:** 2026-04-10T15:45:36.753047Z
**Model Card Version:** 1.0