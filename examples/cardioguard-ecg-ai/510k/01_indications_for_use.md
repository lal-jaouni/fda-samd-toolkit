# CardioGuard ECG-AI: Indications for Use

**Device Name:** CardioGuard ECG-AI  
**Manufacturer:** CardioGuard Medical, Inc.  
**Device Classification:** Class II Software-as-a-Medical-Device  
**Regulatory Submission:** 510(k) Traditional  
**Document Version:** 1.0  
**Document Date:** 2026-10-15

---

## Indications for Use Statement

CardioGuard ECG-AI is a software-as-a-medical-device (SaMD) intended to assist primary care and urgent care clinicians in the detection and characterization of atrial fibrillation, ventricular tachycardia, and 1st degree atrioventricular block from 12-lead electrocardiogram (ECG) recordings in ambulatory adult patients (age 18 years and older) presenting with signs or symptoms of cardiac arrhythmia. The device provides probability scores for each detected cardiac rhythm and is intended to be used as a decision support tool to guide clinical assessment and management decisions.

---

## Intended Use

### Primary Purpose
CardioGuard ECG-AI is intended for use as a clinical decision support tool to assist healthcare professionals in interpreting 12-lead ECG recordings and detecting the presence of specific cardiac arrhythmias (atrial fibrillation, ventricular tachycardia, 1st degree AV block) in adult patients presenting with signs or symptoms suggestive of arrhythmia.

### Intended Users
- Primary care physicians
- Nurse practitioners
- Physician assistants
- Urgent care clinicians
- Telehealth providers with access to 12-lead ECG acquisition and interpretation capability

### Intended Use Environments
- Primary care clinics and medical offices
- Urgent care centers
- Ambulatory care settings
- Telehealth/remote care platforms
- Community health centers

### Patient Population
- Adults age 18 years and older
- Patients presenting with symptoms suggestive of arrhythmia (palpitations, syncope, presyncope, dyspnea, fatigue, chest discomfort)
- Patients undergoing routine cardiac screening in primary care
- Patients with known risk factors for arrhythmia (hypertension, diabetes, structural heart disease)

---

## Specific Clinical Indications

CardioGuard ECG-AI is indicated for the following clinical applications:

### 1. Detection of Atrial Fibrillation (AFib)
- **Indication:** Screening and detection of atrial fibrillation in ambulatory adult patients with signs or symptoms of arrhythmia
- **Clinical Context:** AFib affects 2-3% of US adults and is associated with increased risk of stroke (5-fold), heart failure (2-fold), and mortality. Early detection enables initiation of anticoagulation or rate control therapy
- **Diagnostic Role:** Device assists clinician in determining whether AFib is present on the index ECG. Device output (probability score) supports clinical decision-making regarding need for further evaluation, cardiology referral, or initiation of treatment

### 2. Detection of Ventricular Tachycardia (VT)
- **Indication:** Detection of ventricular tachycardia in ambulatory adult patients
- **Clinical Context:** VT is a life-threatening arrhythmia associated with syncope, cardiac arrest, and sudden cardiac death. Rapid detection and appropriate management (antiarrhythmic drugs, cardioversion, ICD placement) is critical
- **Diagnostic Role:** Device flags presence of VT to alert clinician to urgent arrhythmia. Clinician should prioritize appropriate management including emergency care if patient is hemodynamically unstable

### 3. Detection of 1st Degree Atrioventricular (AV) Block
- **Indication:** Detection of 1st degree AV block (PR interval > 200 ms) in ambulatory adult patients
- **Clinical Context:** 1st degree AV block is common (prevalence ~1-2% in primary care) and usually benign in the absence of symptoms. However, may indicate need for monitoring or underlying conduction system disease
- **Diagnostic Role:** Device identifies presence of prolonged PR interval to support rhythm characterization and risk stratification

---

## Specific Instructions for Use

### When to Use CardioGuard ECG-AI
1. **Primary care patient with palpitations:** ECG obtained; CardioGuard output reviewed to assess for arrhythmia
2. **Urgent care patient with syncope:** 12-lead ECG acquired immediately; CardioGuard output helps triage severity and need for emergency department referral
3. **Telehealth patient with symptoms:** ECG obtained via portable device; CardioGuard provides remote decision support
4. **Routine screening:** Patient in primary care for annual exam; ECG ordered; CardioGuard provides rapid arrhythmia screening

### How to Use CardioGuard ECG-AI
1. Acquire 12-lead ECG using standard equipment (GE MUSE, Philips PageWriter, Mortara ELI, Schiller, or similar)
2. Transmit ECG to CardioGuard API (automatic via EHR integration or manual upload)
3. Device processes signal and returns probability scores within 1 second:
   - Probability of atrial fibrillation
   - Probability of ventricular tachycardia
   - Probability of 1st degree AV block
   - Confidence intervals for each probability
4. Clinician reviews probabilities in context of patient presentation
5. If probability > 0.70 for target arrhythmia, device flags result for clinician review
6. Clinician integrates device output with clinical assessment (symptoms, vital signs, prior ECGs, patient history) to make diagnosis and management decisions

### Decision Support Framework
- **High confidence arrhythmia (probability 0.80-1.00):** Strong evidence for arrhythmia presence; clinician should act accordingly (treat, refer to cardiology, initiate monitoring, etc.)
- **Moderate confidence (probability 0.65-0.80):** Reasonable evidence for arrhythmia; recommend cardiology consultation or expert review if diagnosis uncertain
- **Low confidence (probability 0.50-0.65):** Equivocal result; recommend clinical correlation and consideration of additional testing (repeat ECG, event monitor, stress test, etc.)
- **Negative result (probability < 0.50):** Device does not detect target arrhythmia; if clinical suspicion high, recommend cardiology consultation or further testing

---

## Contraindications

CardioGuard ECG-AI is NOT indicated for:

1. **Pediatric patients (age < 18 years):** Device not validated in pediatric population. Separate validation required before pediatric use
2. **Paced rhythms:** Patients with pacemakers or implantable cardioverter-defibrillators (ICDs) are excluded. Algorithm not designed to interpret paced complexes or device-generated rhythms
3. **Intubated or critically ill patients:** Device designed for ambulatory patients; performance in ICU setting unknown
4. **Real-time continuous monitoring:** Device designed for single 10-second ECG recordings, not for continuous rhythm monitoring systems
5. **Non-ECG modalities:** Device accepts only 12-lead ECG input at 500 Hz sampling rate. Single-lead, wireless, or non-standard ECG formats not supported

---

## Warnings and Precautions

### Warnings
- **Do not use as sole diagnostic tool:** CardioGuard ECG-AI is intended as a clinical decision support tool, not as a replacement for physician judgment. Clinicians must integrate device output with clinical presentation, patient history, and other diagnostic tests
- **Equivocal results require expert review:** If device probability is in the equivocal range (0.50-0.70), clinicians should not make diagnostic or treatment decisions solely on device output; cardiology consultation is recommended
- **Missed arrhythmias possible:** Like all diagnostic tests, CardioGuard has sensitivity < 100%. Clinical presentation inconsistent with device output should prompt expert review and additional diagnostic testing
- **Emergency situations:** If patient is hemodynamically unstable (hemodynamic VT, VT with syncope) or presents with chest pain/dyspnea suggestive of acute coronary syndrome, clinician should pursue emergent cardiology and emergency medicine evaluation regardless of CardioGuard output

### Precautions
- **Age-related performance variation:** Model performance is slightly lower in younger adults (18-40 years, AUROC 0.91 vs. 0.95 in 41-65). Clinicians should exercise greater caution and consider lower sensitivity threshold in younger patients with equivocal results
- **Demographic disparities:** AUROC is 0.03 lower in Black/African American populations compared to White populations in internal validation. This gap does not mean the device is contraindicated in Black patients, but clinicians should be aware of potential performance variation
- **ECG signal quality:** Device performs optimally on high-quality signals (signal quality score > 95%). Marginal-quality signals (excessive noise, baseline wander) may produce less reliable output; clinician should consider repeat ECG if signal quality is questionable
- **Equipment variations:** Device trained on ECGs from GE, Philips, Mortara, and Schiller equipment. Performance on ECG machines from other manufacturers has not been validated; use with caution
- **Medications and electrolytes:** No explicit analysis of medication effects (QT-prolonging drugs, beta-blockers, antiarrhythmic drugs) or electrolyte abnormalities on model performance. Clinicians should consider these factors when interpreting results
- **No cardiac rate information:** Device classifies rhythm but does not provide explicit heart rate calculation. Clinicians should assess rate separately if rate control is therapeutic goal

---

## Clinical Performance

### Primary Endpoint (Clinical Validation Study)
- **AUROC >= 0.90 with 95% CI lower bound >= 0.87:** ACHIEVED
- Result: AUROC 0.92 (95% CI: 0.89-0.94)

### Secondary Endpoints
- **Sensitivity >= 0.85:** ACHIEVED (0.88)
- **Specificity >= 0.90:** ACHIEVED (0.92)
- **PPV >= 0.88:** ACHIEVED (0.90)
- **NPV >= 0.90:** ACHIEVED (0.91)

### Sub-Population Performance
- **Age 18-40:** AUROC 0.91, Sensitivity 0.85, Specificity 0.91
- **Age 41-65:** AUROC 0.95, Sensitivity 0.90, Specificity 0.94
- **Age 66+:** AUROC 0.94, Sensitivity 0.89, Specificity 0.92
- **Male:** AUROC 0.93, Sensitivity 0.88, Specificity 0.93
- **Female:** AUROC 0.91, Sensitivity 0.88, Specificity 0.90
- **White:** AUROC 0.94, Sensitivity 0.90, Specificity 0.93
- **Black:** AUROC 0.91, Sensitivity 0.86, Specificity 0.91

---

## Deployment and Integration

### Input Specifications
- **Format:** 12-lead ECG signal (digital format)
- **Duration:** 10 seconds (5,000 samples per lead at 500 Hz)
- **Sampling rate:** >= 500 Hz (device assumes 500 Hz; 250 Hz minimum for data quality inclusion)
- **Signal source:** Standard ECG machines (GE MUSE, Philips PageWriter, Mortara ELI, Schiller, or similar)

### Output Specifications
- **Latency:** < 200 milliseconds (typical: < 100 ms)
- **Output format:** JSON payload containing:
  - Probability of atrial fibrillation (0-1)
  - Probability of ventricular tachycardia (0-1)
  - Probability of 1st degree AV block (0-1)
  - Probability of normal sinus rhythm (0-1)
  - 95% confidence intervals for each
  - Clinical interpretation flag (FLAGGED if any probability > 0.70)

### Integration with EHR
- **API:** RESTful HTTPS API (TLS 1.3)
- **Authentication:** OAuth 2.0 with encrypted credentials
- **Data transmission:** All data encrypted in transit; audit logging maintained
- **Compliance:** HIPAA BAA in place; device operates under AWS business associate agreement

---

## Post-Market Surveillance

CardioGuard Medical, Inc. commits to the following post-market activities:

1. **Real-world performance database:** Ongoing collection of model predictions and clinical outcomes from deployed sites
2. **Annual safety report:** Submission to FDA of safety data, adverse events, and performance metrics
3. **Quarterly retraining:** Model retraining on new data with drift monitoring; FDA notified annually or if drift triggers exceeded
4. **Device registry participation:** Enrollment in cardiac device registry for 24 months post-clearance
5. **Adverse event reporting:** MedWatch reporting within 30 days of any adverse event with probable relation to device
6. **Cybersecurity monitoring:** Vulnerability scanning and annual penetration testing; 30-day patch release for security vulnerabilities

---

## References

- FDA PCCP Guidance: Predetermined Change Control Plans for Machine Learning-Enabled Medical Devices (December 2024)
- FDA AI/ML Action Plan (2021)
- Anumana ECG-AI 510(k) Submission (K232488)
- IEC 62304: Medical Device Software - Software Lifecycle Processes
- ISO 13485: Medical Devices - Quality Management Systems
- IMDRF Software as a Medical Device (SaMD) Framework

---

## Document Certification

This Indications for Use statement is accurate and complete, and represents the intended clinical use of CardioGuard ECG-AI as designed and validated.

**Prepared by:**  
Dr. Michael Rodriguez, VP Product and Clinical Affairs  
CardioGuard Medical, Inc.

**Date:** 2026-10-15
