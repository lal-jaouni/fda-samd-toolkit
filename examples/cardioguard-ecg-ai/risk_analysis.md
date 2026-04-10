# CardioGuard ECG-AI: Risk Analysis (ISO 14971)

**Document Version:** 1.0  
**Document Date:** 2026-10-15  
**Standard:** ISO 14971:2019 (Risk management for medical devices)  
**Device:** CardioGuard ECG-AI, Class II SaMD

---

## 1. Executive Summary

CardioGuard ECG-AI risk analysis follows ISO 14971:2019 risk management methodology. Hazards identified include model errors (false negatives/positives), software/infrastructure failures, cybersecurity vulnerabilities, and automation bias. All identified risks are mitigated to acceptable levels through design controls, validation, labeling, and post-market surveillance.

---

## 2. Risk Analysis Process

**Risk Management Team:**
- Clinical Affairs VP (risk lead)
- Software Engineering Lead
- Regulatory Affairs Manager
- Clinical Cardiologist (external)

**Risk Assessment Method:** Risk Priority Number (RPN) = Severity x Probability x Detection
- Severity: 1-5 scale (1=minor, 5=catastrophic)
- Probability: 1-5 scale (1=remote, 5=frequent)
- Detection: 1-5 scale (1=certain to detect, 5=cannot detect)

**Risk Acceptance Criteria:**
- RPN < 50: Acceptable with standard controls
- RPN 50-100: Acceptable with enhanced controls
- RPN > 100: Not acceptable; risk mitigation required

---

## 3. Hazard Analysis and Risk Assessment

### HAZARD 1: False Negative Arrhythmia Detection

**Definition:** Device fails to detect true arrhythmia; patient presented with symptoms of AFib/VT/AV block but CardioGuard outputs probability < 0.50.

**Potential Harm:**
- Delayed diagnosis of life-threatening arrhythmia (VT)
- Missed AFib detection, leading to stroke (thromboembolic event)
- Inappropriate reassurance of symptomatic patient
- Patient harm: stroke, syncope, cardiac arrest

**Hazard Cause:**
1. Model underfitting or poor generalization to new population
2. ECG signal quality degradation (noise, artifact)
3. Atypical ECG morphology not well-represented in training data
4. Input/output software error
5. Model trained on biased dataset

**Risk Assessment:**
- **Severity:** 4 (high - potential for serious patient harm including stroke)
- **Probability:** 2 (low - model sensitivity 0.88 in clinical validation)
- **Detection:** 3 (moderate - may be detected through clinical correlation or follow-up ECG)
- **RPN:** 4 x 2 x 3 = **24 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Clinical Validation** | Prospective multi-site study (n=1500) with cardiologist adjudication demonstrated sensitivity 0.88 overall, 0.92 for AFib | Clinical validation report; 04_performance_summary.md |
| **Sub-population Monitoring** | Performance stratified by age, sex, race/ethnicity; lower sensitivity (0.85) in 18-40 age group flagged in labeling | Model card; labeling precautions |
| **Confidence Intervals** | Output includes 95% CI; wide intervals flag uncertain results requiring clinical correlation | API output specification; 02_device_description.md |
| **Labeling** | Indications describe device as "decision support"; warnings emphasize clinical judgment priority; precautions re: younger patients | 05_labeling.md; 01_indications_for_use.md |
| **Training Requirements** | All clinicians must complete 30-min training on interpretation and limitations before use | Training program requirement |
| **Clinical Workflow** | Device integrated into EHR as decision support; final diagnosis remains clinician responsibility | Implementation guidance |
| **Post-Market Surveillance** | Quarterly AUROC monitoring; annual FDA reports documenting any missed cases or adverse events | PCCP commitment; 04_performance_summary.md |

**Residual Risk:** LOW. Sensitivity of 0.88 for target arrhythmias is acceptable for clinical decision support. Labeling clearly emphasizes that device does not replace clinical judgment. Sub-population gaps identified and transparent.

**Acceptance:** ACCEPTED with documented mitigations.

---

### HAZARD 2: False Positive Arrhythmia Flagging

**Definition:** Device incorrectly flags normal rhythm as arrhythmia; patient without arrhythmia receives probability >= 0.70.

**Potential Harm:**
- Unnecessary cardiology referral and healthcare cost
- Patient anxiety/stress from false diagnosis
- Unnecessary medication initiation (anticoagulation, rate control)
- Unnecessary procedures (Holter monitoring, electrophysiology testing)
- Medication side effects from unnecessary drugs

**Hazard Cause:**
1. Model overfitting to training data
2. ECG variants (e.g., persistent juvenile T wave inversion) misclassified as VT
3. Atrial ectopy misclassified as AFib
4. Data preprocessing error
5. Model drift from retraining

**Risk Assessment:**
- **Severity:** 2 (low-moderate - primarily economic and psychological harm, not direct physical harm)
- **Probability:** 2 (low - model specificity 0.92; false positive rate 8%)
- **Detection:** 2 (good - cardiologist can confirm diagnosis)
- **RPN:** 2 x 2 x 2 = **8 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Clinical Validation** | Study demonstrates specificity 0.92; only 8% false positive rate at 0.70 threshold | 04_performance_summary.md |
| **Decision Threshold** | Threshold of 0.70 probability set to balance sensitivity/specificity | Device description; labeling |
| **Confidence Intervals** | Narrow CI flags high-confidence results; wide CI indicates uncertainty | API output specification |
| **Clinical Correlation** | Labeling emphasizes integration with symptoms, physical exam, prior ECGs | 05_labeling.md |
| **Equivocal Guidance** | Labeling recommends cardiology consultation for equivocal results (0.50-0.70 probability) | 05_labeling.md |
| **ECG Review by Cardiologist** | False positives will be caught on cardiologist review; low actual harm expected | Standard clinical practice |
| **Drift Monitoring** | Quarterly AUROC monitoring; 2% specificity drop triggers retraining | PCCP; 02_device_description.md |

**Residual Risk:** LOW. False positive rate is acceptable for decision support tool. Additional cardiologist review will catch false positives. Primarily economic/psychological harm, not physical harm.

**Acceptance:** ACCEPTED with documented mitigations.

---

### HAZARD 3: Automation Bias

**Definition:** Clinician over-relies on CardioGuard output and fails to apply clinical judgment; dismisses true positive arrhythmia as false alarm based on unconscious bias toward device output.

**Potential Harm:**
- Missed true arrhythmia despite device output (paradoxically, clinician ignores correct device result due to bias toward automation)
- Inappropriate treatment decisions
- Patient harm: stroke, sudden cardiac death

**Hazard Cause:**
1. Clinician fatigue or time pressure leading to mindless acceptance of device output
2. Cognitive bias toward automation (assumption that computers are always right)
3. Lack of training on appropriate device use
4. System design that makes device output too prominent in EHR

**Risk Assessment:**
- **Severity:** 3 (moderate - potential for missed diagnosis)
- **Probability:** 2 (low to moderate - depends on implementation and training)
- **Detection:** 3 (moderate - detected through adverse event reporting or patient outcome)
- **RPN:** 3 x 2 x 3 = **18 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Labeling** | Prominent warning that device is "decision support, NOT replacement for clinical judgment" | 05_labeling.md; 01_indications_for_use.md |
| **Clinical Training** | All clinicians complete 30-minute training including automation bias discussion | Training program |
| **EHR Integration Design** | Device output displayed as "supporting information," not as a diagnosis. Clinician must confirm diagnosis. | Implementation specification |
| **Equivocal Result Protocol** | When probability 0.50-0.70, system prompts clinician to "confirm result with clinical assessment" | EHR workflow rules |
| **Confidence Intervals** | Wide CI visually indicates uncertainty; prompts clinician skepticism of overconfident device | UI design |
| **Conflict Protocol** | If patient presentation conflicts with device output (e.g., symptomatic but negative), system prompts "Consider clinical correlation or additional testing" | EHR workflow |
| **Adverse Event Reporting** | Post-market surveillance monitors for missed diagnoses; cases where clinician ignored correct device output | PCCP; post-market monitoring |

**Residual Risk:** LOW-MODERATE. Mitigation depends on proper implementation and clinician adherence to training. Design of EHR integration and workflow is critical.

**Acceptance:** ACCEPTED with implementation-dependent controls. Pre-deployment EHR integration review required.

---

### HAZARD 4: Model Degradation / Data Drift

**Definition:** Model performance degrades over time as patient population or ECG signal characteristics change; AUROC drops below acceptable threshold.

**Potential Harm:**
- Progressive increase in false negatives (missed arrhythmias)
- Progressive increase in false positives (unnecessary referrals)
- Loss of clinical utility
- Patient harm from accumulated missed diagnoses

**Hazard Cause:**
1. Deployment ECG machines have different signal characteristics than training data
2. New patient population differs from training cohort (age, comorbidities, medications)
3. Healthcare system changes (equipment upgrades, workflow changes)
4. Data distribution shift not captured in initial validation
5. Subpopulation emerging with poor model performance

**Risk Assessment:**
- **Severity:** 3 (moderate - progressive performance degradation)
- **Probability:** 3 (moderate - data drift is common in ML models)
- **Detection:** 2 (good - detected through performance monitoring)
- **RPN:** 3 x 3 x 2 = **18 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Drift Monitoring Framework** | Monthly AUROC calculation on internal validation set; drift triggers defined (5% AUROC drop, 3% sensitivity drop) | PCCP; 02_device_description.md |
| **Predetermined Change Control Plan** | FDA-approved PCCP allows quarterly retraining without new 510(k) when drift triggers exceeded | PCCP.yaml |
| **Retraining Protocol** | Systematic retraining procedure with data QA, class balance verification, hyperparameter optimization | PCCP section 4 |
| **Version Control** | All model versions tagged with training date, dataset composition, performance metrics | Device description section 10 |
| **Real-World Performance Tracking** | Logged predictions and clinical outcomes from deployed sites enable early drift detection | Post-market surveillance |
| **Data Quality Assurance** | All new training data undergoes signal integrity checks, artifact detection, label validation | PCCP section 3 |
| **Diversity Monitoring** | Training data composition tracked by age, sex, race/ethnicity; diversity targets maintained | PCCP section 3 |
| **Annual FDA Notification** | FDA receives annual retraining summary with performance before/after, any drift events, demographic analysis | PCCP section 5 |

**Residual Risk:** LOW. Systematic drift monitoring and PCCP framework allow timely detection and mitigation. Model not frozen; continuous improvement framework in place.

**Acceptance:** ACCEPTED with PCCP framework and quarterly monitoring commitment.

---

### HAZARD 5: Out-of-Distribution Input

**Definition:** Device receives ECG recording outside design specifications or distribution of training data; model performance unknown.

**Examples:**
1. ECG from equipment manufacturer not in training data (e.g., Mindray, other non-major brands)
2. Extremely high or low heart rate (< 40 or > 150 bpm)
3. ECG from pediatric patient (though contraindicated)
4. ICU patient with critical illness artifacts
5. Non-standard lead arrangement or ordering

**Potential Harm:**
- Unpredictable model output on out-of-distribution input
- False negatives or false positives on equipment not validated
- Patient harm from unreliable device output

**Hazard Cause:**
1. Broader deployment than intended use scope
2. Clinician error (inputs pediatric ECG despite contraindication)
3. Equipment vendor diversity in healthcare systems
4. Integration errors in EHR (incorrect lead ordering)

**Risk Assessment:**
- **Severity:** 3 (moderate - model behavior unknown)
- **Probability:** 2 (low-moderate - primarily depends on implementation scope)
- **Detection:** 3 (moderate - detected through clinical correlation or performance monitoring)
- **RPN:** 3 x 2 x 3 = **18 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Input Validation** | Software validates that input meets specifications (12 leads present, 500 Hz, 10 sec, 12-lead format) | Device description section 3 |
| **Signal Quality Checks** | Automated checks reject ECGs with baseline wander > 5 mV, noise > 2 mV, or data gaps | Device description preprocessing |
| **Equipment Screening** | Pre-deployment inventory of all ECG equipment at site; only supported manufacturers approved for integration | Implementation checklist |
| **Contraindication Screening** | User interface includes contraindication warnings: "Not for pediatric patients" | EHR UI design |
| **Device Labeling** | Labeling explicitly lists supported equipment (GE MUSE, Philips, Mortara, Schiller); others use with caution | 05_labeling.md; 02_device_description.md |
| **Error Return** | If input validation fails, system returns error message rather than attempting inference on invalid data | API specification |
| **Validation Studies** | Performance validated on major manufacturers; performance on other brands documented as "not validated" | Clinical validation study design |
| **Post-Market Surveillance** | Errors and out-of-spec inputs logged and analyzed for patterns | Post-market monitoring |

**Residual Risk:** LOW. Input validation framework and labeling minimize risk. Some residual uncertainty for equipment not validated, but appropriately labeled.

**Acceptance:** ACCEPTED with input validation framework and labeling precautions.

---

### HAZARD 6: Cybersecurity Vulnerability / Data Breach

**Definition:** Unauthorized access to CardioGuard systems or patient data; malicious actor gains access to ECG data, model weights, or patient records.

**Potential Harm:**
- HIPAA breach; unauthorized access to protected health information
- Privacy violation; patient information exposed
- Model theft or reverse-engineering
- Reputational harm to manufacturer
- Loss of patient trust

**Hazard Cause:**
1. API vulnerability (injection attack, authentication bypass)
2. Cloud infrastructure misconfiguration (public S3 bucket, open database port)
3. Insider threat (disgruntled employee access)
4. Supply chain vulnerability (compromised dependency library)
5. DDoS attack causing service unavailability

**Risk Assessment:**
- **Severity:** 4 (high - HIPAA breach, privacy violation)
- **Probability:** 2 (low - medical devices typically well-protected; AWS security strong)
- **Detection:** 2 (good - intrusion detection systems; audit logs)
- **RPN:** 4 x 2 x 2 = **16 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Encryption** | TLS 1.3 for data in transit; AES-256 for data at rest | Device description section 7 |
| **Access Control** | OAuth 2.0 authentication; role-based access control; encrypted credential management | Device description section 8 |
| **HIPAA Compliance** | Business Associate Agreement with AWS; HIPAA-compliant deployment | Device description section 8 |
| **Intrusion Detection** | AWS GuardDuty monitoring for unauthorized access; CloudTrail logging all API calls | Device description section 9 |
| **Vulnerability Scanning** | Automated scanning via AWS Inspector; penetration testing annually | Device description section 9 |
| **Dependency Management** | Software bill of materials (SBOM) maintained; dependencies scanned for known vulnerabilities | Device description section 8 |
| **Security Updates** | 30-day commitment to patch security vulnerabilities of HIGH severity or greater | PCCP commitment |
| **Incident Response** | 24-hour breach notification required if breach involves patient data | PCCP section 4 |

**Residual Risk:** LOW. Comprehensive security controls in place. Some residual risk of zero-day exploits, but mitigated by monitoring and incident response plan.

**Acceptance:** ACCEPTED with comprehensive security framework and monitoring.

---

### HAZARD 7: Sub-Population Performance Disparity

**Definition:** Device performs significantly worse in specific demographic sub-populations (e.g., Black patients, younger patients), leading to disparate care.

**Potential Harm:**
- Missed arrhythmias in lower-performing populations (worse sensitivity)
- Over-flagging in lower-performing populations (worse specificity)
- Health equity concern; unequal quality of care by race/ethnicity or age
- Perpetuation of systemic disparities in cardiovascular disease

**Hazard Cause:**
1. Training data imbalance (60% White, 20% Black)
2. Signal characteristic variation by equipment or health system demographics
3. Underlying prevalence differences (e.g., AFib prevalence lower in younger cohort, affecting training)
4. Model bias toward majority populations

**Risk Assessment:**
- **Severity:** 3 (moderate - affects specific populations; not universal hazard)
- **Probability:** 4 (high - identified disparity already exists; 0.03 AUROC gap)
- **Detection:** 2 (good - sub-population analysis detected disparity)
- **RPN:** 3 x 4 x 2 = **24 (Acceptable)**

**Mitigations:**

| Mitigation | Description | Evidence |
|---|---|---|
| **Transparent Disclosure** | Clinical validation report explicitly documents 0.03 AUROC gap between White (0.94) and Black (0.91) populations | 04_performance_summary.md section 5 |
| **Root Cause Analysis** | Gap attributed to training data imbalance (60% White, 20% Black) and potential signal variations | Model card; 04_performance_summary.md |
| **Mitigation Plan** | Committed to recruit 50,000 additional ECGs from HBCU health systems; re-validate with diverse data; target gap <= 0.02 in v1.1 (Q4 2026) | PCCP modification 2 |
| **Labeling Precautions** | Labeling notes demographic gap and directs clinician attention in Black patients with equivocal results | 05_labeling.md precautions |
| **Sub-Population Monitoring** | Quarterly performance tracking by demographics; annual FDA report | PCCP section 6 |
| **Age-Related Guidance** | Lower sensitivity (0.85) in 18-40 age group documented in labeling; recommend closer clinical review | Model card; labeling |
| **Continuous Improvement** | PCCP framework allows quarterly retraining with diversity targets to continuously improve equity | PCCP section 3 data quality standards |
| **Accountability** | Annual FDA pre-notification reports progress on equity mitigation; public commitment to reducing disparity | PCCP section 5 |

**Residual Risk:** MODERATE. Known disparity exists but is transparent and actively mitigated. Residual risk that disparity persists until v1.1 retraining (Q4 2026) and that other unmeasured disparities may exist. However, disparity is smaller than general clinician variation in ECG interpretation.

**Acceptance:** ACCEPTED with transparency and active mitigation commitment. Disparity is disclosed to end-users (clinicians and health systems); health systems can make informed deployment decisions. Mitigation timeline committed in PCCP.

---

## 4. Risk Summary Table

| Hazard | Severity | Probability | Detection | RPN | Status | Residual Risk |
|---|---|---|---|---|---|---|
| False negative arrhythmia | 4 | 2 | 3 | 24 | Acceptable | Low |
| False positive arrhythmia | 2 | 2 | 2 | 8 | Acceptable | Low |
| Automation bias | 3 | 2 | 3 | 18 | Acceptable | Low-Moderate |
| Model drift | 3 | 3 | 2 | 18 | Acceptable | Low |
| Out-of-distribution input | 3 | 2 | 3 | 18 | Acceptable | Low |
| Cybersecurity breach | 4 | 2 | 2 | 16 | Acceptable | Low |
| Sub-population disparity | 3 | 4 | 2 | 24 | Acceptable | Moderate |

**Overall Risk Assessment:** All identified hazards have acceptable residual risk with implemented mitigations. No unmitigated high-risk hazards identified. Risk acceptance criteria met.

---

## 5. Post-Market Surveillance and Ongoing Risk Management

**Commitment to Ongoing Risk Monitoring:**
1. Quarterly AUROC monitoring for drift detection
2. Annual FDA reports documenting performance, adverse events, and equity metrics
3. Real-world performance database from deployed sites
4. Patient outcome tracking where available (registry participation)
5. Adverse event reporting via MedWatch for serious events
6. Systematic sub-population performance analysis

**Risk Management Review:** Annual review of risk analysis with clinical team and regulatory advisors. Updates to risk analysis if new hazards identified or if mitigation effectiveness changes.

---

## Document Certification

This risk analysis is accurate and complete per ISO 14971:2019. All identified hazards have been assessed and mitigated to acceptable risk levels.

**Risk Management Lead:** Dr. Michael Rodriguez, VP Product and Clinical Affairs  
**Date:** 2026-10-15
