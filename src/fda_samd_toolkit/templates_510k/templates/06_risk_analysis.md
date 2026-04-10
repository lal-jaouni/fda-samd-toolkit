# AI/ML-Specific Risk Analysis for Medical Devices

## Overview
Traditional risk analysis (FMEA, FTA) applies to all devices. AI/ML devices have unique failure modes
that traditional analysis often misses:
- Model uncertainty and confidence calibration
- Performance degradation when deployed on data different from training distribution
- Failure modes that emerge from model architecture (e.g., adversarial examples)
- Automation bias (physicians over-relying on AI output, skipping manual review)
- Lack of interpretability making it hard to catch errors

**FDA Guidance:** Explicitly analyze AI-specific failure modes. Generic risk analysis is insufficient.

---

## Template

## 1. Standard FMEA (Adapted for AI)

### 1.1 AI Component Failure Modes and Effects

Apply failure mode and effects analysis (FMEA) to the AI model itself.

[INSERT: AI-specific FMEA]

Example: "**FMEA for AI Model (Atrial Fibrillation Detector)**

| Failure Mode | Potential Cause | Effects | Severity (1-5) | Probability (1-5) | Risk Priority | Mitigation |
|---|---|---|---|---|---|---|
| **High False Negative Rate (missed AF)** | | | | | | |
| Model underfits training data | Insufficient model capacity, early stopping too aggressive | Sensitivity <85%; AF cases missed; delayed diagnosis | 5 (critical) | 1 (rare, validated in testing) | 5 | Pre-deployment sensitivity testing; minimum sensitivity >90% required |
| Distribution shift in deployment | New hospital with different ECG equipment, patient population skew | Model performance degrades; unknown sensitivity in new data | 5 | 2 (possible) | 10 | Input validation checks; confidence scoring flags low-reliability cases; post-market surveillance |
| Data preprocessing error | Bug in filter implementation, normalization fails | Model receives malformed input; undefined behavior | 4 | 1 (rare) | 4 | Unit tests for preprocessing; continuous data quality monitoring |
| **High False Positive Rate (unnecessary alerts)** | | | | | | |
| Model overfits to training data | Training dataset has idiosyncratic patterns absent in real deployment | Specificity <85%; alert fatigue; physician override of true positives | 3 (moderate) | 2 (possible) | 6 | External validation (Section 4); random forest feature importance analysis; prospective monitoring |
| Threshold selection too sensitive | Threshold optimized on training set but calibration drifts in deployment | Positive predictive value drops; alerts on non-AF patterns | 3 | 2 | 6 | Confidence interval thresholding; alert is probabilistic (not binary); physician review required |
| **Model Uncertainty Not Quantified** | | | | | | |
| Confidence score unreliable | Monte Carlo dropout dropout rate poorly chosen; uncertainty underestimated | Physician relies on confident but incorrect prediction; missed error | 4 | 2 | 8 | Confidence calibration testing (Hosmer-Lemeshow p>0.05); comparison to known difficult cases |
| Confidence score overestimated | Model is overconfident; CI too narrow | Physician falsely believes prediction is reliable; rare dangerous errors go undetected | 4 | 1 | 4 | Calibration plots; external validation; prospective error monitoring |
| **Systematic Bias (Subgroup Performance Disparities)** | | | | | | |
| Lower sensitivity in underrepresented populations | Training data skewed: 82% Caucasian, 3% Asian | Model misses AF in Asian patients; diagnostic delay | 4 (missed diagnosis in vulnerable population) | 2 (Asian subgroup 4% of population) | 8 | Stratified performance testing (Section 5.3 of Performance); labeling warning; future retraining; monitoring in post-market surveillance |
| Systematic false positives in specific demographics | Model biased against certain race, age, sex | Over-alerts in one subgroup; alert fatigue + treatment burden | 2 | 2 | 4 | Fairness testing; disaggregated metrics by subgroup; labeling of limitations |
| **Software/Integration Failure** | | | | | | |
| Model inference fails/crashes | Out-of-memory, floating-point error, library version mismatch | Device unavailable; clinician has no AI support | 3 (degraded to manual review) | 1 (rare, tested in integration) | 3 | Comprehensive unit/integration testing; graceful failure mode (device outputs 'unable to analyze' not random garbage) |
| Incorrect model version deployed | Version control error; old model pushed to production | Unknown performance; possible regression vs. prior version | 4 | 1 | 4 | Version control (Git tags); automated deployment verification; model signature/hash verification |
| Data pipeline bug | Preprocessing not applied; model receives raw ECG | Model expects normalized input; garbage output | 4 | 1 | 4 | End-to-end integration testing; data quality checks pre-inference |
| **Automation Bias and Clinical Workflow Failure** | | | | | | |
| Physician blind trust in AI | Over-reliance on AI output; physician skips manual ECG review | Dangerous errors not caught; especially risky if model is wrong in unusual ways | 4 | 2 | 8 | UI design: probabilistic output (not binary); confidence score displayed; mandatory decision support disclaimer; alerts for low-confidence cases requiring review |
| Alert fatigue | False positive rate 6.2%; physicians become desensitized to alerts | True positives ignored; AF cases missed | 4 | 2 | 8 | Optimized threshold to minimize false positives; confidence scoring filters unimportant alerts; quarterly alert effectiveness audits |
| Workflow disruption | Device too slow (>500 ms per ECG) or requires unnatural workflow integration | Clinicians bypass device; no use of AI support | 2 (degraded benefit) | 1 (validated latency <200ms) | 2 | Performance testing; workflow integration testing with target clinical sites |

**Risk Evaluation Summary:**
- Top 5 risks: False negatives (missed AF), distribution shift, uncertainty miscalibration, demographic disparities, automation bias
- Residual risk after mitigation: All ranked <10 (acceptable per ISO 14971)
- No unacceptable risks remaining"

---

## 2. Model-Specific Failure Modes

### 2.1 Failure Modes Unique to Neural Networks

[INSERT: NN-specific failure analysis]

Example: "**Failure Modes Inherent to Deep Learning Architectures:**

1. **Adversarial Examples**
   - Definition: Tiny perturbations to input (imperceptible to humans) that cause misclassification
   - Clinical relevance: Real ECGs don't have adversarial perturbations, so attack surface is theoretical
   - Risk level: LOW (adversarial examples require intentional crafting; unlikely in accidental deployment)
   - Mitigation: (a) Adversarial robustness testing not required for 510(k); (b) If concerning, can be addressed in future versions

2. **Gradient-Based Failure Modes**
   - Definition: Exploding/vanishing gradients during training cause training failure
   - Symptom: Model doesn't learn; loss stays flat
   - Risk level: LOW (detected during development; model released only if training converges)
   - Mitigation: Batch normalization + careful hyperparameter selection prevent this

3. **Class Imbalance Exploitation**
   - Definition: Model learns to predict majority class (non-AF) for everything
   - Symptom: High overall accuracy but 0% sensitivity (catches no AF cases)
   - Risk level: MEDIUM (possible if class weights not applied during training)
   - Mitigation: Class weights (AF=2.80, non-AF=0.35) applied during training;
     validated sensitivity >90% before release

4. **Overfitting to Training Set**
   - Definition: Model learns training data specifics (noise, site-specific artifacts) instead of generalizable patterns
   - Symptom: High performance on test set, low on new real-world data
   - Risk level: MEDIUM (possible with small training set or high model capacity)
   - Mitigation: (a) Large training set (200K ECGs >> model parameters 847K); (b) validation set prevents overfitting;
     (c) external validation shows 1% performance drop (minor overfitting); (d) regularization (dropout p=0.5)

5. **Representation Collapse**
   - Definition: Hidden layers learn redundant or meaningless representations
   - Symptom: Model accuracy doesn't improve with deeper networks
   - Risk level: LOW (detected during architecture search; models with collapsed representations discarded)
   - Mitigation: Cross-validation of multiple architectures; choice of simplest adequate model

**Conclusion:** Neural network failure modes are well-understood and addressed through standard
deep learning best practices (regularization, validation, external testing). No unique high-risk
failure modes remain unmitigated."

---

### 2.2 Uncertainty Quantification Failure

[INSERT: Confidence/uncertainty analysis]

Example: "**Risk: Model Confidence Score is Unreliable**

When would a physician make a dangerous error based on model confidence?

Scenario 1: Model is highly confident (confidence=0.95) but wrong
- Physician sees high confidence and skips manual review
- Model predicts 'AF likely (0.95 confidence)' but true rhythm is normal sinus
- Result: Unnecessary anticoagulation, bleeding risk

Scenario 2: Model is uncertain (confidence=0.55) but physician overrides
- Model outputs 'uncertain, manual review recommended'
- Physician still makes clinical decision based on confidence level
- If model's uncertain predictions are biased toward false positives, physician is misled

**Mitigation Strategy:**

Confidence calibration testing (Hosmer-Lemeshow test):
- Binned predictions into deciles: [0-0.1), [0.1-0.2), ... [0.9-1.0)
- Compared predicted probability to observed accuracy in each bin
- Result: Slope = 1.02 (95% CI: 0.98-1.06), intercept = -0.02
- Interpretation: Model is well-calibrated; predicted probabilities match observed frequencies
- Conclusion: Physician can trust confidence scores

Calibration assessment for high-risk confidence ranges:
- When confidence >0.90: Model is correct 91-92% of the time (calibrated)
- When confidence <0.60: Model is correct 55-65% of the time (appropriately uncertain)
- When confidence in 0.70-0.80: Model is correct 72-80% of the time (calibrated)

Monitoring for confidence degradation:
- Post-market surveillance tracks: observed accuracy vs. predicted confidence
- If degradation detected (e.g., predicted 0.90 but only 85% correct), triggers model retraining
- Quarterly calibration check on deployment data (HL7 result logging captures all predictions)

Physician workflow accommodation:
- Confidence <0.60: ALERT - 'Manual review required; model uncertain'
- Confidence 0.60-0.75: CAUTION - 'Recommend clinical correlation'
- Confidence >0.75: REPORT - Standard interpretation displayed
- At all levels: Physician retains override capability (can discard AI recommendation)

**Residual Risk:** LOW. Confidence scores are well-calibrated and monitored."

---

## 3. Data-Related Risks

### 3.1 Training Data Biases and Their Clinical Impact

[INSERT: Data bias analysis]

Example: "**Identified Biases in Training Data and Clinical Implications:**

1. **Demographic Bias: Underrepresentation of Asian Patients**
   - Training data: 82% Caucasian, 3% Asian
   - Performance impact: Sensitivity in Asian population 88.5% (vs. 92.7% Caucasian) = 4.2% gap
   - Clinical risk: AF cases missed in Asian patients; delayed diagnosis
   - Severity: MODERATE (4% miss rate is still substantial)
   - Sample size: 410 AF cases in validation; CI wide but point estimate is concerning
   - Mitigation:
     a) Labeling explicitly warns about limited Asian representation
     b) Stratified sub-group analysis conducted and published (Section 5.3)
     c) Future retraining planned with targeted Asian patient enrollment (goal: 8-10%)
     d) Post-market surveillance includes explicit monitoring of Asian subgroup performance
     e) If real-world performance in Asian patients drops <85%, triggers alert and retraining

2. **Sex Bias: Male Predominance in Training Data**
   - Training data: 58% male, 42% female
   - Performance impact: No significant sex difference in validation (Female 92.4% vs. Male 91.8%)
   - Clinical risk: LOW (no evidence of sex-based performance difference)
   - Mitigation: None needed; equal performance across sexes

3. **Age Bias: Limited Pediatric Data**
   - Training data: <1% pediatric (outside IFU; intentionally excluded)
   - Performance impact: Device is not intended for pediatric use (IFU: 18+ years)
   - Clinical risk: NONE (pediatrics excluded from indication)
   - Mitigation: IFU clearly states age restriction; no pediatric claims made

4. **Site Bias: Academic Medical Center Data Only**
   - Training data: 100% from large academic hospitals (Mayo, Cleveland, Johns Hopkins)
   - Potential bias: These are high-quality settings with excellent ECG technique
   - Risk: Model may underperform in community hospitals with lower ECG quality
   - Severity: MODERATE (unknown real-world performance in non-academic settings)
   - Mitigation:
     a) External validation planned at community hospitals (prospective study, ongoing)
     b) Post-market surveillance includes community hospital sites
     c) Input validation flagged low-quality ECGs as 'manual review recommended'
     d) If community hospital performance degrades >5%, triggers retraining with community data

5. **Temporal Bias: Training Data 2015-2020**
   - Risk: ECG equipment, acquisition standards, and patient demographics have changed
   - Severity: LOW-MODERATE (AF physiology unchanged; but population characteristics may have shifted)
   - Mitigation:
     a) Prospective validation on 2023-2024 data (planned)
     b) Post-market surveillance monitors for performance drift over time
     c) Annual revalidation on recent data (last 12 months of deployment data)

**Summary of Bias Mitigation:**
- Identified biases are documented and acknowledged (not hidden)
- Performance disparities are quantified with confidence intervals
- Clinical impact is assessed (which biases are clinically important?)
- Labeling reflects limitations (Asian representation warning)
- Monitoring and retraining plans address persistent biases
- Future improvements are committed to and tracked"

---

### 3.2 Data Distribution Shift

[INSERT: Deployment distribution monitoring]

Example: "**Data Shift Scenarios and Detection Strategy:**

**Monitored Covariates (will trigger alerts if shift detected):**

1. **Input ECG Quality**
   - Metric: % of ECGs flagged with artifact >15%
   - Baseline (training): 8.4%
   - Alert threshold: >15% (>80% increase from baseline)
   - Action: Investigate cause; may indicate equipment malfunction or technique change

2. **Patient Age Distribution**
   - Metric: Mean age of patients studied
   - Baseline (training): 66.8 years
   - Alert threshold: Mean age shifts >10 years from baseline
   - Action: Stratified re-analysis by age; validate performance in new age distribution

3. **AF Prevalence**
   - Metric: % of studied ECGs with AF diagnosis
   - Baseline (training): 24.6%
   - Alert threshold: AF prevalence <10% or >40%
   - Action: Validate that model performance holds across prevalence range (performance should not depend on prevalence)

4. **Heart Rate Distribution**
   - Metric: Mean heart rate of studied population
   - Baseline (training): 72 BPM
   - Alert threshold: Shift >15 BPM from baseline
   - Action: Validate performance at extreme heart rates (known failure mode at >120 BPM)

5. **Model Confidence Score Distribution**
   - Metric: Mean confidence of model predictions
   - Baseline (test set): mean=0.85, std=0.12
   - Alert threshold: Mean confidence drops <0.80 (suggests model is less certain in deployment)
   - Action: May indicate harder cases or distribution shift; investigate root cause

**Monitoring Infrastructure:**
- All ECG submissions logged with covariates (age, HR, artifact level, model output, confidence)
- Monthly automated report: Distribution of monitored covariates vs. baseline
- Quarterly manual review: Identify trends, investigate root causes
- Annual formal re-validation: Run model on last 12 months of deployment data; confirm performance

**Response Protocol if Shift Detected:**
- Level 1 (Minor shift): Alert hospital IT department; investigate equipment/workflow changes
- Level 2 (Moderate shift): Run interim performance analysis on new data; communicate findings to FDA (within 6 months)
- Level 3 (Severe shift): Trigger retraining with recent data; full validation study conducted
- Level 4 (Outside IFU population): Consider withdrawing indication or issuing Dear Healthcare Provider letter

**Risk Assessment:** Comprehensive monitoring enables early detection of shifts before safety impact;
residual risk is LOW due to proactive surveillance"

---

## 4. Clinical Integration Risks

### 4.1 Automation Bias and Over-Reliance

[INSERT: Automation bias mitigation]

Example: "**Risk: Physician Over-Relies on AI, Misses Manual Review**

Why it matters: AI makes mistakes that humans would catch if they were thinking critically.
Over-reliance is dangerous.

Example scenario:
- Device outputs: 'AF likely (confidence: 92%)'
- Physician sees high confidence and signs off without reviewing ECG
- Device was wrong; rhythm is actually normal sinus with artifact
- Unnecessary anticoagulation initiated; patient later bleeds

**Mitigation Strategy:**

1. **UI/UX Design to Prevent Blind Trust**
   - Output format: Probabilistic, not binary
     WRONG: 'AF DETECTED'
     RIGHT: 'Probability of AF: 92% (95% CI: 88-96%)'
   - Confidence score always displayed and color-coded:
     - Green (>80% confidence): Device is fairly confident
     - Yellow (60-80%): Device is somewhat uncertain
     - Red (<60%): Device recommends manual review
   - Explicit disclaimer on every report:
     'This is a clinical decision support tool. Physician interpretation required. Do not rely
     solely on this output for clinical decision-making.'

2. **Mandatory Manual Review for Low-Confidence Cases**
   - If confidence <60%: System prevents sign-off without physician explanation
   - Physician must select one of: 'Agree with AI', 'Disagree with AI', 'Uncertain, will monitor'
   - Selection is logged for downstream analysis

3. **Escalation Pathways for Disagreement**
   - If physician overrides AI (e.g., device says AF, physician says normal):
     - Logged as discrepancy event
     - Cardiologist QA review triggered for random sample (10% of overrides)
     - Pattern analysis: Are certain types of cases frequently overridden? (Suggests model weakness)
   - If pattern detected: May trigger retraining or UI redesign

4. **Alert Fatigue Mitigation**
   - Current false positive rate: 6.2% (generates ~62 alerts per 1,000 non-AF ECGs)
   - Industry standard: <10% false positive rate acceptable
   - Monitoring: Quarterly alert effectiveness audit
     - Are true positive AF cases getting appropriate clinical response?
     - Are false positive alerts being appropriately disregarded?
   - If override rate >70% (indicates alert fatigue), threshold adjusted to reduce false positives

5. **Physician Training on Automation Bias**
   - Mandatory training module: 'Automation Bias in AI-Assisted Diagnosis' (15 minutes)
   - Training covers:
     a) Common ways physicians unconsciously over-rely on AI
     b) Types of cases where AI commonly fails (paroxysmal AF, artifact)
     c) How to maintain critical thinking while using AI tools
   - Completion tracked; credential required before device use

6. **Continuous Monitoring for Bias in Practice**
   - Post-market surveillance includes:
     a) Audit of 10 random AI-flagged AF cases per site monthly (did physician follow up appropriately?)
     b) Audit of 10 random AI-negative cases per site monthly (were any missed AF cases later diagnosed?)
   - Feedback loop: Findings shared with clinical teams to reinforce appropriate use

**Residual Risk:** LOW with above mitigations. Probabilistic output, low-confidence alerts, and
training reduce unconscious over-reliance. Logging + QA auditing catch problematic patterns early."

---

## 5. Post-Market Surveillance and Monitoring

### 5.1 Surveillance Plan for AI-Specific Risks

[INSERT: Monitoring and surveillance plan]

Example: "**Post-Market Surveillance Plan:**

**Objective:** Detect performance degradation, demographic disparities, or unexpected failure modes in real deployment

**Duration:** Minimum 1 year post-market; may extend based on findings

**Data Collection:**
- Passive logging: Every ECG submitted to device is logged (HL7 event, age, sex, diagnosis, model output, confidence)
- Active audits: Monthly manual review of 50 random cases by cardiologist
- Quarterly performance analysis: Sensitivity/specificity on accumulated deployment data
- Annual re-validation: Full performance study on last 12 months of data

**KPIs Monitored:**
1. **Performance Metrics (quarterly):**
   - Sensitivity: Alert if <85% (baseline 92%)
   - Specificity: Alert if <88% (baseline 94%)
   - False positive rate: Alert if >10% (baseline 6.2%)
   - AUC-ROC: Alert if <0.90 (baseline 0.94)

2. **Subgroup Metrics (quarterly):**
   - Sensitivity stratified by race: Alert if disparity increases >2%
   - Sensitivity stratified by sex: Alert if disparity increases >2%
   - Sensitivity stratified by age: Alert if elderly/young subgroups degrade >3%

3. **Confidence Calibration (quarterly):**
   - Hosmer-Lemeshow test: Alert if p<0.05 (model becomes miscalibrated)
   - Observed vs. predicted accuracy by confidence decile: Alert if slope drifts from 1.0 >0.1

4. **Operational Metrics (monthly):**
   - False alarm rate (alerts on clearly normal ECGs): Alert if >8%
   - Processing latency: Alert if >500 ms (workflow disruption risk)
   - System uptime: Alert if <99% (availability concern)
   - Device rejection rate: Alert if >2% (may indicate equipment change)

**Alert Response Protocol:**

If quarterly analysis shows KPI exceedance:
1. Investigate root cause: Is it real performance change or measurement artifact?
   - If artifact (e.g., new hospital added with different patient population): Analyze separately
   - If real: Determine cause (data shift, equipment change, patient population change?)
2. If performance degradation confirmed: Escalate to FDA within 30 days per 21 CFR 803.12
3. Interim mitigation: May recommend heightened manual review or temporary use restriction while investigating
4. Permanent mitigation: Retrain model with recent data if indicated

**Annual Comprehensive Re-Validation:**
- Formal study: Test model on full year of deployment data
- Full metrics: Sensitivity, specificity, AUC, stratified by all subgroups
- External validation: Compare findings to new external sites if available
- Labeling update: If limitations identified, update to reflect real-world performance
- Publication: Share findings with FDA and cardiology community (transparency)"

---

## Checklist Before Finalizing

- [ ] Standard FMEA completed with AI-specific failure modes included
- [ ] Top 5 risks identified and ranked by risk priority number
- [ ] Each risk has documented mitigation strategy with residual risk <10 (or acceptably justified)
- [ ] Model-specific failure modes addressed (overfitting, adversarial examples, class imbalance, uncertainty calibration)
- [ ] Data biases identified and quantified (demographic disparities with confidence intervals)
- [ ] Clinical impact of biases assessed (which are clinically meaningful?)
- [ ] Data distribution shift scenarios anticipated with monitoring plan
- [ ] Automation bias mitigation includes UI/UX design, training, audit, escalation pathways
- [ ] Post-market surveillance plan is specific (KPIs, thresholds, alert protocols, response times)
- [ ] All risks have clear residual risk assessment (low, medium, acceptable)
- [ ] No "unknown unknowns" (unforeseen failure modes discussed as limitation to monitor)
