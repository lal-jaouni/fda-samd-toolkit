# CardioGuard ECG-AI: Clinician Labeling and Instructions for Use

**Document Version:** 1.0  
**Document Date:** 2026-10-15  
**Device:** CardioGuard ECG-AI  
**Manufacturer:** CardioGuard Medical, Inc.

---

## CARDIOGUARD ECG-AI - INSTRUCTIONS FOR CLINICIANS

### INDICATIONS FOR USE

CardioGuard ECG-AI is indicated to assist primary care and urgent care clinicians in the detection and characterization of atrial fibrillation, ventricular tachycardia, and 1st degree atrioventricular block from 12-lead electrocardiogram (ECG) recordings in ambulatory adult patients (age 18 years and older) presenting with signs or symptoms of cardiac arrhythmia.

### CONTRAINDICATIONS

CardioGuard ECG-AI is NOT appropriate for:
- Pediatric patients (age < 18 years)
- Patients with implanted pacemakers or defibrillators (paced rhythms)
- Intubated or critically ill ICU patients
- Real-time continuous rhythm monitoring systems
- Non-ECG diagnostic modalities

### DESCRIPTION

CardioGuard ECG-AI is a machine learning-enabled software system deployed as a cloud-based service. The device analyzes 12-lead ECG signals (10 seconds, 500 Hz sampling rate) and generates probability scores for four cardiac rhythm classes: atrial fibrillation, ventricular tachycardia, 1st degree AV block, and normal sinus rhythm.

The device uses a transformer-based deep learning neural network trained on 250,000 ECG recordings from five major U.S. health systems (2019-2023). The model was clinically validated in a prospective, multi-site study of 1,500 patients with board-certified cardiologist adjudication as reference standard.

### HOW TO USE

**Step 1: Obtain ECG**
Acquire a standard 12-lead ECG using your institution's ECG machine (GE MUSE, Philips PageWriter, Mortara ELI, Schiller, or similar). Ensure all 12 leads are captured at 500 Hz sampling rate for 10 seconds.

**Step 2: Transmit to CardioGuard**
- **Automatic:** If your EHR is integrated with CardioGuard API, the ECG is automatically transmitted for analysis
- **Manual:** Upload ECG to the CardioGuard web portal (www.cardiogaurd.com/upload) using your hospital credentials

**Step 3: Review Results**
CardioGuard returns a JSON response within 1 second containing:
- Probability score (0-1) for each rhythm class
- 95% confidence intervals
- Clinical interpretation flag ("FLAGGED" if any probability > 0.70)

**Step 4: Clinical Decision-Making**
Interpret CardioGuard output in context of patient presentation:
- Correlate with patient symptoms (palpitations, syncope, fatigue, dyspnea)
- Review patient medical history and prior ECGs
- Integrate with physical examination findings
- Consider other clinical tests if diagnosis uncertain

### UNDERSTANDING YOUR RESULTS

**Interpretation Guide:**

| Probability | Clinical Interpretation | Recommended Action |
|---|---|---|
| 0.80-1.00 | High confidence arrhythmia detected | Strong evidence for arrhythmia; act accordingly (treat, refer, monitor) |
| 0.65-0.80 | Moderate confidence arrhythmia detected | Reasonable evidence; recommend cardiology consultation if uncertain |
| 0.50-0.65 | Equivocal result | Uncertain; recommend clinical correlation, additional testing, or specialist review |
| < 0.50 | Low confidence; arrhythmia not detected | Device does not detect target arrhythmia; if clinical suspicion high, consider further workup |

**Example 1: High Confidence Atrial Fibrillation**
```
Patient: 68-year-old with palpitations
CardioGuard Output: Atrial Fibrillation probability 0.92 (95% CI: 0.88-0.95) - FLAGGED
Clinical Correlation: Patient reports irregular palpitations, no syncope
Decision: Initiate anticoagulation workup (CHA2DS2-VASc score) and rate control medication
```

**Example 2: Equivocal Result**
```
Patient: 35-year-old with dyspnea
CardioGuard Output: Ventricular Tachycardia probability 0.62 (95% CI: 0.55-0.70)
Clinical Correlation: Patient hemodynamically stable, no syncope history
Decision: Obtain repeat ECG, consider event monitor, refer to cardiology for expert review
```

**Example 3: Negative Result with High Clinical Suspicion**
```
Patient: 52-year-old with syncope history
CardioGuard Output: All arrhythmias probability < 0.50 (NSR probability 0.98)
Clinical Correlation: Patient has high syncope risk, structural heart disease
Decision: Despite negative CardioGuard output, pursue cardiology evaluation (ECG quality issue, exercise testing, device interrogation if ICD patient)
```

### CLINICAL PERFORMANCE

**Overall Performance (Clinical Validation Study, n=1500):**
- AUROC: 0.92 (95% CI: 0.89-0.94)
- Sensitivity: 0.88 (detects 88 of 100 true arrhythmias)
- Specificity: 0.92 (correctly identifies 92 of 100 normal rhythms)
- PPV: 0.90 (when flagged, 90% probability of true arrhythmia)

**Performance by Rhythm:**
- Atrial Fibrillation: AUROC 0.95, Sensitivity 0.92, Specificity 0.96
- Ventricular Tachycardia: AUROC 0.93, Sensitivity 0.88, Specificity 0.94
- 1st Degree AV Block: AUROC 0.90, Sensitivity 0.85, Specificity 0.92

**Performance Variation by Patient Age:**
- Age 18-40: AUROC 0.91, Sensitivity 0.85 (lower; recommend closer review in this age group)
- Age 41-65: AUROC 0.95, Sensitivity 0.90 (best performance)
- Age 66+: AUROC 0.94, Sensitivity 0.89 (excellent)

**Known Performance Gap:** Black patients show 0.03 lower AUROC (0.91 vs. 0.94 White patients) in internal development data. This gap does not mean the device is contraindicated in Black patients; it indicates potential for improved performance in future versions. Mitigation is underway (additional diverse training data, v1.1 retraining planned Q4 2026).

### WARNINGS

**Critical: Device is Decision Support, Not Replacement for Clinical Judgment**

CardioGuard ECG-AI is a tool to assist your clinical assessment. It does NOT:
- Diagnose arrhythmias; only you, the clinician, can diagnose
- Replace your clinical judgment or cardiology consultation when indicated
- Guarantee absence of arrhythmia if output is negative
- Account for real-time hemodynamic changes or patient symptoms

**Equivocal Results Require Expert Review**

If CardioGuard probability is 0.50-0.70 (equivocal range), do NOT make treatment decisions based on the device output alone. Recommend cardiology consultation or additional diagnostic testing.

**Missed Arrhythmias Are Possible**

Like all diagnostic tests, CardioGuard sensitivity is not 100% (0.88). If patient presentation conflicts with device output (e.g., patient has classic AFib symptoms but CardioGuard shows low probability), prioritize patient presentation and seek expert evaluation.

**Emergency Situations**

For hemodynamically unstable patients (hemodynamic VT, syncope, chest pain with ECG changes), do NOT wait for device output. Pursue emergent cardiology and emergency medicine evaluation immediately.

### PRECAUTIONS

**Age-Related Performance Variation**

Model performance is lower in younger adults (18-40 years, AUROC 0.91 vs. 0.95 in 41-65). Exercise greater caution and consider lower probability thresholds for clinical action in young patients with equivocal results.

**Demographic Disparities**

Device performance is 0.03 lower in Black/African American populations compared to White populations (internal development data). This known gap does NOT mean device should not be used in Black patients; rather, clinicians should be aware of potential performance variation and consider this context when interpreting results.

**Signal Quality Matters**

Device performs optimally on high-quality ECG signals. If ECG shows:
- Excessive baseline wander
- Electrode noise or artifact
- Powerline interference
...consider obtaining a repeat ECG. Marginal quality signals may produce unreliable results.

**Equipment Variation**

Device trained on GE MUSE, Philips PageWriter, Mortara ELI, and Schiller equipment. Use with caution on ECG machines from manufacturers not represented in training data.

**Medications and Electrolytes**

Device performance has not been specifically analyzed for:
- QT-prolonging medications (antipsychotics, antiemetics, antibiotics)
- Electrolyte abnormalities (hypokalemia, hypocalcemia)
- Anti-arrhythmic drugs
Consider these factors when interpreting results in patients taking relevant medications or with known electrolyte disorders.

### LABELING LEGEND

**FLAGGED:** CardioGuard detected probability >= 0.70 for target arrhythmia. Clinician review and action recommended.

**NOT FLAGGED:** All target arrhythmia probabilities < 0.70. Normal sinus rhythm or other non-target rhythm detected.

**AUROC:** Area Under the Receiver Operating Characteristic Curve. Higher AUROC (closer to 1.0) indicates better discrimination between presence and absence of disease.

**Sensitivity:** Probability that device detects arrhythmia when it is truly present. (True Positives / All Disease-Positive)

**Specificity:** Probability that device correctly identifies absence of arrhythmia when it is truly absent. (True Negatives / All Disease-Negative)

**PPV (Positive Predictive Value):** When device flags an arrhythmia, probability that patient truly has the arrhythmia. (True Positives / All Positive Flags)

**NPV (Negative Predictive Value):** When device does not flag an arrhythmia, probability that patient is truly free of arrhythmia. (True Negatives / All Negative Flags)

### SYSTEM REQUIREMENTS

**ECG Machine Compatibility:**
- GE MUSE (supported)
- Philips PageWriter (supported)
- Mortara ELI (supported)
- Schiller (supported)
- Other manufacturers: contact CardioGuard Medical for compatibility verification

**Sampling Rate:** >= 250 Hz (500 Hz standard)  
**Signal Duration:** 10 seconds  
**Input Format:** HL7v2, XML, or direct API call with JSON

**Internet/Connectivity:** Requires secure HTTPS connection to CardioGuard servers (www.cardiogaurd.com)

**Latency:** Response returned within 200 milliseconds (typical: 87 milliseconds)

### STORAGE AND HANDLING

CardioGuard operates in cloud environment on HIPAA-compliant AWS infrastructure. Patient data:
- De-identified using HIPAA Safe Harbor method
- Encrypted in transit (TLS 1.3) and at rest (AES-256)
- Logged for audit trails and performance monitoring
- Retained per HIPAA record retention (minimum 3 years)

Data is NOT stored on personal computers or portable devices.

### TRAINING AND CERTIFICATION

Before deploying CardioGuard in your institution:
1. All clinicians using the system must complete 30-minute online training module
2. Training covers indications, contraindications, how to interpret results, when to seek cardiology consultation
3. Annual recertification recommended

Contact CardioGuard Medical for training materials: training@cardiogaurd-medical.com

### TECHNICAL SUPPORT

**Technical Issues (System not responding, error messages):**
- Contact: support@cardiogaurd-medical.com
- Phone: 1-888-CARDIO-1 (1-888-227-3461)
- Hours: 24/7 support for critical issues

**Clinical Questions (How to interpret a result):**
- Contact: clinicians@cardiogaurd-medical.com
- Phone: 1-617-555-0123 ext. 5 (Clinical Affairs)
- Hours: M-F 8:00 AM - 5:00 PM Eastern Time

**Adverse Events or Safety Concerns:**
- Report to: safety@cardiogaurd-medical.com
- Include: ECG ID, patient demographics (age, sex), result interpretation, clinical outcome (if known)
- CardioGuard Medical will investigate and may report to FDA via MedWatch if appropriate

### POST-MARKET SURVEILLANCE

CardioGuard Medical, Inc. commits to:
1. **Performance monitoring:** Quarterly internal validation set monitoring for drift detection
2. **Annual reports:** FDA pre-notification submitting performance data and any adverse events
3. **Registry participation:** Enrollment in cardiac device outcomes registry for 24 months post-clearance
4. **Adverse event tracking:** MedWatch reporting for any serious adverse events with probable relation to device

### MODIFICATIONS AND UPDATES

CardioGuard operates under a Predetermined Change Control Plan (PCCP) approved by FDA. Modifications that may occur without new 510(k) submission:
1. **Model retraining:** Quarterly retraining on new data with drift monitoring (5% AUROC threshold trigger)
2. **Data expansion:** Annual addition of diverse training data to improve sub-population performance
3. **Hyperparameter optimization:** Fine-tuning of learning rates and regularization within predefined ranges

Any modifications are version-controlled and performance re-validated before deployment. Health systems will be notified of any modifications that affect clinical performance or user interface.

### REFERENCES

- FDA PCCP Guidance (Dec 2024): https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices
- Anumana ECG-AI 510(k) Submission (K232488)
- IEC 62304: Medical Device Software - Software Lifecycle Processes
- ISO 13485: Medical Devices - Quality Management Systems

---

## QUICK REFERENCE CARD (For Clinician Pocket Cards)

**CardioGuard ECG-AI Quick Reference**

| When to Use | How to Use | Interpret |
|---|---|---|
| Patient with suspected arrhythmia (palpitations, syncope, dyspnea) | 1. Obtain 12-lead ECG 2. Transmit to CardioGuard 3. Review output in 1 second | Probability 0.80-1.00 = STRONG evidence, act on it |
| | 4. Correlate with clinical presentation | Probability 0.65-0.80 = MODERATE, consult cardiology if uncertain |
| | 5. Proceed with clinical decision | Probability 0.50-0.65 = EQUIVOCAL, seek expert review |
| | | Probability < 0.50 = NOT detected; if clinical suspicion high, further workup |

| WARNING |
|---|
| Device is decision support ONLY. Clinical judgment is final. |
| If hemodynamically unstable, pursue emergency evaluation immediately. |
| If result conflicts with clinical presentation, prioritize patient presentation. |

---

## MANUFACTURER CONTACT INFORMATION

**CardioGuard Medical, Inc.**  
100 Cardiology Drive  
Cambridge, MA 02139  
USA

**Phone:** 1-888-CARDIO-1 (1-888-227-3461)  
**Email:** support@cardiogaurd-medical.com  
**Website:** www.cardiogaurd-medical.com

**Regulatory Inquiries:** fda-submissions@cardiogaurd-medical.com  
**Clinical Support:** clinicians@cardiogaurd-medical.com

---

**This labeling is accurate and complete. For clarifications or updates, contact CardioGuard Medical.**

**Date:** 2026-10-15
