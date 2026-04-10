# CardioGuard ECG-AI: Device Overview

## 1. Clinical Problem and Intended Use

### Unmet Clinical Need

Atrial fibrillation (AFib), ventricular tachycardia (VT), and 1st degree atrioventricular (AV) block are common cardiac arrhythmias in primary care and urgent care settings. Current clinical practice relies on:

1. Manual ECG interpretation by healthcare providers of varying expertise
2. Computer-assisted interpretation from ECG machines (typically rule-based, with high false positive rates in primary care)
3. Cardiology referral for suspected cases (creating scheduling bottlenecks)

Manual interpretation has recognized limitations:
- Sensitivity for AFib in primary care ranges from 85-92% (depends on clinician expertise)
- False positive rate from automated ECG machines is 10-15% in primary care populations
- Cardiac referral delays increase risk of thromboembolic events in AFib patients

### Intended Use Statement

CardioGuard ECG-AI is a software-as-a-medical-device (SaMD) intended to assist primary care and urgent care clinicians in the detection and characterization of:

1. Atrial fibrillation
2. Ventricular tachycardia  
3. 1st degree atrioventricular block

from 12-lead electrocardiogram (ECG) recordings in ambulatory adult patients (age 18 and older) presenting with signs or symptoms of cardiac arrhythmia. The device provides probability scores and confidence intervals for each detected arrhythmia to support clinical decision-making. The device is not intended to replace clinical judgment, direct patient treatment decisions, or cardiology consultation when indicated.

### Indications for Use (IFU)

CardioGuard ECG-AI is indicated for:

- Ambulatory adult patients (age >= 18 years)
- Patients with signs or symptoms suggestive of arrhythmia (palpitations, syncope, fatigue, dyspnea)
- Patients undergoing routine ECG screening in primary care or urgent care settings
- Integration with existing clinical workflows in primary care clinics, urgent care centers, and telehealth platforms

The device is NOT indicated for:

- Pediatric patients (age < 18)
- Paced rhythms (pacemaker or ICD patients)
- Intubated ICU patients
- Real-time monitoring systems (designed for single-beat or short-term recordings, not continuous monitoring)

### Target Population

**Demographics:** Adult patients (18-85 years old)
**Prevalence:** AFib affects 2-3% of adults in US primary care; VT and AV block each affect < 1%
**Risk factors:** Hypertension (50%), diabetes (25%), structural heart disease (15%)
**Sex distribution:** Study enrolled 48% female, 52% male
**Race/ethnicity distribution:** 60% White, 20% Black/African American, 12% Hispanic/Latino, 8% Asian American

## 2. Technology Overview

### Algorithm Architecture

**Model Type:** Transformer-based deep learning neural network  
**Input:** 12-lead ECG signal (10 seconds, 500 Hz sampling rate = 5,000 samples per lead, 60,000 samples total)  
**Output:** Probability scores for each target class:
- Atrial fibrillation (0-1, where 1 = high confidence AFib)
- Ventricular tachycardia (0-1)
- 1st degree AV block (0-1)
- Normal sinus rhythm (0-1, residual)

**Architecture Details:**

1. **Input Layer:** 12-lead ECG signals (5,000 samples x 12 leads), zero-mean normalized
2. **Feature Extraction:** 1D convolutional layers (kernel sizes: 16, 32, 64 filters) to extract local morphological features
3. **Temporal Modeling:** Multi-head self-attention transformer encoder (8 attention heads, 256 hidden dimensions) to capture long-range dependencies and rhythm patterns
4. **Classification Head:** Global average pooling + 2 fully connected layers (256 -> 128 -> 4 output neurons)
5. **Output:** Softmax to produce probability distribution across 4 classes

**Key Design Rationale:**
- Transformer architecture captures complex temporal patterns in ECG morphology and rhythm regularity
- Self-attention mechanism naturally learns to focus on diagnostically relevant portions of the 10-second recording
- 12-lead input (vs. single-lead) captures atrial and ventricular electrical activity simultaneously

### Training Dataset

**Data Collection:**
- Sources: 5 major US health systems (anonymized, HIPAA-compliant)
- Time period: 2019-2023
- Total ECGs collected: 250,000 (includes all rhythms, not just target arrhythmias)
- Total unique patients: 180,000

**Data Characteristics:**

| Characteristic | Count | Percentage |
|---|---|---|
| Total ECG recordings | 250,000 | 100% |
| Normal sinus rhythm | 155,000 | 62% |
| Atrial fibrillation | 52,000 | 21% |
| Ventricular tachycardia | 15,000 | 6% |
| 1st degree AV block | 18,000 | 7% |
| Other rhythms (excluded) | 10,000 | 4% |

**Demographic Distribution in Training Set:**

| Age Group | Count | % |
|---|---|---|
| 18-40 years | 35,000 | 14% |
| 41-65 years | 130,000 | 52% |
| 66+ years | 85,000 | 34% |

| Sex | Count | % |
|---|---|---|
| Male | 130,000 | 52% |
| Female | 120,000 | 48% |

| Race/Ethnicity | Count | % |
|---|---|---|
| White | 150,000 | 60% |
| Black/African American | 50,000 | 20% |
| Hispanic/Latino | 30,000 | 12% |
| Asian American | 20,000 | 8% |

**Data Quality Assurance:**
- All ECGs verified for signal integrity (12 leads present, no excessive noise)
- Automated artifact detection excluded recordings with baseline wander > 5mV
- All rhythm annotations confirmed by at least one board-certified cardiologist
- Class imbalance addressed through weighted sampling during training

### Model Training

**Hyperparameters:**
- Optimizer: Adam (learning rate = 0.0001, weight decay = 1e-5)
- Batch size: 128
- Epochs: 150 (with early stopping on validation AUROC, patience = 10)
- Loss function: Weighted cross-entropy (weights: normal=1.0, AFib=2.5, VT=2.2, AV block=1.8 to account for clinical severity and class imbalance)
- Validation/Test split: 70% / 15% / 15%

**Training Duration:**
- Computational environment: GPU cluster (8x NVIDIA A100, 40GB memory)
- Training time: 18 hours per epoch, 150 epochs = 112 total GPU days
- Total development timeline: 8 months (including preprocessing, architecture search, hyperparameter tuning)

## 3. Model Performance

### Internal Validation Results

**Overall Performance (n=37,500 test set ECGs):**

| Metric | Atrial Fibrillation | Ventricular Tachycardia | 1st Degree AV Block | Overall |
|---|---|---|---|---|
| AUROC (95% CI) | 0.95 (0.93-0.96) | 0.93 (0.91-0.95) | 0.90 (0.88-0.92) | 0.94 (0.92-0.95) |
| Sensitivity @ 0.90 threshold | 0.92 | 0.88 | 0.85 | 0.91 |
| Specificity @ 0.90 threshold | 0.96 | 0.94 | 0.92 | 0.94 |
| Positive Predictive Value | 0.94 | 0.90 | 0.86 | 0.92 |
| Negative Predictive Value | 0.95 | 0.93 | 0.91 | 0.94 |

### Sub-Population Performance

**By Sex:**

| Sex | N | AUROC | Sensitivity | Specificity |
|---|---|---|---|---|
| Male | 19,500 | 0.94 (0.92-0.95) | 0.90 | 0.95 |
| Female | 18,000 | 0.93 (0.91-0.94) | 0.91 | 0.93 |
| Difference | - | 0.01 | 0.01 | 0.02 |

Interpretation: No clinically significant performance difference between sexes.

**By Age Group:**

| Age Group | N | AUROC | Sensitivity | Specificity |
|---|---|---|---|---|
| 18-40 years | 5,250 | 0.91 (0.88-0.92) | 0.88 | 0.92 |
| 41-65 years | 19,500 | 0.95 (0.93-0.96) | 0.92 | 0.95 |
| 66+ years | 12,750 | 0.94 (0.92-0.95) | 0.90 | 0.94 |

Interpretation: Slightly lower performance in 18-40 age group (AUROC 0.91 vs. 0.95), possibly due to lower prevalence of target arrhythmias and less training data in younger cohorts. Recommend closer clinical attention in younger patients with equivocal model scores.

**By Race/Ethnicity (Internal Validation):**

| Race/Ethnicity | N | AUROC | Sensitivity | Specificity |
|---|---|---|---|---|
| White | 22,500 | 0.94 (0.93-0.96) | 0.91 | 0.95 |
| Black/African American | 7,500 | 0.91 (0.89-0.93) | 0.88 | 0.92 |
| Hispanic/Latino | 4,500 | 0.92 (0.90-0.94) | 0.89 | 0.93 |
| Asian American | 3,000 | 0.93 (0.90-0.95) | 0.90 | 0.94 |
| Gap (White vs. Black) | - | 0.03 | 0.03 | 0.03 |

**Gap Analysis and Mitigation:** A 0.03 AUROC gap exists between White and Black populations in internal validation. This is attributed to:
1. Imbalanced representation in training data (60% White vs. 20% Black)
2. Potential differences in ECG signal characteristics and artifact patterns across equipment manufacturers predominantly used in different health systems
3. Acknowledged disparity in cardiovascular disease representation in training data

**Mitigation Strategy (In Progress):**
- Additional 50,000 ECGs from 2 historically Black colleges and universities (HBCUs) health systems added to training pipeline
- Data stratified retraining planned for v1.1 with dedicated sub-population loss weighting
- Clinical validation study designed to detect and quantify any performance differences in validation cohort

## 4. Deployment Model

### Integration Architecture

**Deployment Option 1: Cloud API (Recommended for v1.0)**
- RESTful API hosted on AWS (HIPAA BAA in place)
- Input: 12-lead ECG in HL7 format or GE MUSE XML export
- Output: JSON payload with probabilities, confidence intervals, and interpretation flag
- Latency: < 200 milliseconds
- Availability: 99.9% uptime SLA

**Deployment Option 2: On-Premise Docker Container (Future)**
- Self-contained inference server for hospital IT integration
- No external API calls; all computation local
- Compatible with hospital EHR via HL7 FHIR interface

### Clinical Workflow

1. Clinician orders ECG in primary care setting
2. 12-lead ECG acquired (GE, Philips, Mortara ECG machines supported)
3. ECG transmitted to CardioGuard API (automatic or manual, depending on EHR integration)
4. Algorithm inference completes in < 1 second
5. Result appears in EHR as:
   - Flagged arrhythmias (if probability > 0.70 for any target class)
   - Confidence intervals
   - Clinical interpretation guidance
6. Clinician reviews result in context of patient presentation and clinical judgment
7. Cardiology referral initiated if indicated

### Security and Compliance

- All data in transit encrypted with TLS 1.3
- All data at rest encrypted with AES-256
- Access logging and audit trails per HIPAA Audit Rule
- Annual penetration testing and vulnerability assessment
- Incident response plan with 24-hour notification requirement

### Monitoring and Retraining

- Real-time performance monitoring dashboard (AUROC, sensitivity, specificity tracked daily)
- Monthly drift detection analysis (comparing validation set from different time periods)
- Quarterly retraining cycle with new data (see PCCP section)
- Automated alert if AUROC drops > 5% or sensitivity drops > 3%

## 5. Regulatory Strategy

### Submission Pathway

**Classification:** Class II  
**Regulatory Pathway:** 510(k) Traditional (not Abbreviated)  
**Predicate Device:** Anumana ECG-AI (K232488), cleared 2021  
**Substantial Equivalence Argument:** Same intended use (AFib detection from ECG), different algorithm (transformer vs. CNN), different training data (larger, more diverse), different performance characteristics (comparable or superior)

### Predetermined Change Control Plan (PCCP)

CardioGuard will be submitted with a PCCP to allow model retraining and performance updates without additional 510(k) submissions, per FDA guidance (December 2024).

**Planned Modifications:**
1. Model retraining with new ECG data (quarterly)
2. Data expansion (adding diverse training cohorts)
3. Hyperparameter optimization

**Drift Monitoring and Triggers:**
- Primary trigger: 5% relative AUROC decrease on internal validation set
- Secondary trigger: 3% relative sensitivity decrease for any target arrhythmia
- Review cadence: Monthly drift assessment, FDA pre-notification every 12 months

See pccp.yaml for detailed configuration.

### Post-Market Surveillance

- Real-world performance database to track model accuracy after deployment
- 24-month commitment to registry participation (e.g., device registry or clinical outcomes database)
- Annual safety report submission to FDA
- Commitment to issue software updates for security vulnerabilities within 30 days of discovery

## 6. Key References

- FDA PCCP Guidance: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices
- Anumana ECG-AI 510(k) Submission (K232488): Available via FDA CDRH database
- IEC 62304 Medical Device Software Lifecycle Processes
- ISO 13485 Medical Devices Quality Management Systems
