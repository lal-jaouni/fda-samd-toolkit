# CardioGuard ECG-AI: Device Description

**Document Version:** 1.0  
**Document Date:** 2026-10-15  
**Submission:** 510(k) Traditional

---

## 1. Overview

CardioGuard ECG-AI is a machine learning-enabled software-as-a-medical-device (SaMD) that analyzes 12-lead electrocardiogram (ECG) recordings to detect and characterize three specific cardiac arrhythmias: atrial fibrillation (AFib), ventricular tachycardia (VT), and 1st degree atrioventricular (AV) block. The device is deployed as a cloud-based API accessible to primary care and urgent care clinics.

---

## 2. Technology Overview

### Algorithm Classification
- **Type:** Deep learning, supervised neural network
- **Architecture:** Transformer-based encoder with multi-head self-attention mechanism
- **Training Method:** Supervised learning on annotated ECG data
- **Model Class:** Classification (multi-class: 4 output classes)

### Hardware Requirements
- **Deployment Environment:** Amazon Web Services (AWS) cloud infrastructure
- **Compute Resources:** GPU instances (NVIDIA A100) for inference
- **Storage:** Encrypted database for logged predictions and performance monitoring
- **Redundancy:** Multi-availability zone deployment for high availability (99.9% uptime SLA)

### Software Stack
- **Runtime:** Python 3.10+
- **Deep Learning Framework:** PyTorch 2.0
- **Serving:** FastAPI + Gunicorn (Python web application server)
- **Dependencies:** NumPy 1.24, SciPy 1.10, scikit-learn 1.3
- **Container:** Docker (image: cardiogaurd-medical/cardioguard-ecg-ai:v1.0)
- **Version Control:** Git with semantic versioning (v1.0.0 corresponds to FDA-cleared baseline model)

---

## 3. Input Specifications

### Signal Input Format

**Format Type:** 12-lead electrocardiogram signal  
**Duration:** 10 seconds of continuous recording  
**Sampling Rate:** 500 Hz (standard clinical ECG acquisition rate)  
**Total Samples:** 60,000 samples total (5,000 samples per lead x 12 leads)

### Input Leads
1. Standard bipolar limb leads: I, II, III
2. Augmented unipolar leads: aVR, aVL, aVF
3. Precordial leads: V1, V2, V3, V4, V5, V6

### Data Encoding
- **Format:** Digital signal (numeric arrays)
- **Accepted Input Formats:** HL7v2 ECG segment, GE MUSE XML, Philips PageWriter XML, Mortara ECG XML, JSON with raw samples
- **Voltage Units:** Millivolts (mV)
- **Bit Depth:** 16-bit signed integer (or floating point, range -10 to +10 mV typical)

### Signal Quality Requirements
- **Baseline Wander:** < 5 mV (excess wander may compromise rhythm classification)
- **Powerline Noise:** < 0.1 mV RMS after 50/60 Hz notch filtering
- **Electrode Noise:** < 2 mV RMS over 1-second windows
- **Data Completeness:** No missing samples or gaps; all 12 leads must be present and temporally aligned
- **Signal Duration:** Exactly 10 seconds (tolerance +/- 0.1 seconds)

### Pre-Processing Steps (Applied Before Algorithm Inference)

1. **Lead-wise normalization:** Each lead independently normalized to zero mean and unit variance
   - Formula: `normalized_signal[i] = (raw_signal[i] - mean(raw_signal)) / std(raw_signal)`

2. **Baseline wander removal:** High-pass filter (cutoff 0.5 Hz, 4th-order Butterworth)
   - Removes low-frequency DC offset and baseline drift

3. **Powerline noise removal:** Notch filter at 50 Hz and 60 Hz (Q=10, 4th-order IIR)
   - Attenuates AC interference from clinical environment

4. **Signal validation:** Automated checks for artifact and signal quality
   - Reject if baseline wander > 5 mV, electrode noise > 2 mV RMS, or data gaps present
   - Return error message to EHR if signal fails quality threshold

### Input via API

**HTTP Protocol:** POST request to `/api/v1/predict`  
**Authentication:** OAuth 2.0 bearer token (provided by CardioGuard Medical)  
**Request Format:**
```json
{
  "ecg_id": "ECG-2026-10-15-12345",
  "patient_mrn": "encrypted_mrn_token",
  "timestamp": "2026-10-15T14:30:00Z",
  "leads": {
    "I": [float, float, ...],    # 5000 samples
    "II": [float, float, ...],
    "III": [float, float, ...],
    "aVR": [float, float, ...],
    "aVL": [float, float, ...],
    "aVF": [float, float, ...],
    "V1": [float, float, ...],
    "V2": [float, float, ...],
    "V3": [float, float, ...],
    "V4": [float, float, ...],
    "V5": [float, float, ...],
    "V6": [float, float, ...]
  },
  "sampling_rate_hz": 500,
  "ecg_machine": "GE_MUSE"  # optional
}
```

---

## 4. Algorithm Architecture

### High-Level Architecture

```
Input (12-lead ECG, 500 Hz, 10 sec)
  |
  v
Preprocessing (normalization, filtering)
  |
  v
Feature Extraction (1D Convolution)
  |
  v
Transformer Encoder (Self-Attention)
  |
  v
Global Average Pooling
  |
  v
Classification Head (Dense Layers)
  |
  v
Softmax Output (4 class probabilities)
```

### Detailed Architecture Specification

#### Stage 1: Input and Preprocessing
- **Input Shape:** (12, 5000) = 12 leads x 5000 samples
- **Operations:** Normalization (zero-mean, unit variance per lead)
- **Output Shape:** (12, 5000)

#### Stage 2: Feature Extraction (Convolutional Layers)
Three 1D convolutional blocks to extract local morphological features:

**Block 1:**
- 16 filters, kernel size 3, stride 1, padding 1
- Activation: ReLU
- Output shape: (16, 5000)

**Block 2:**
- 32 filters, kernel size 3, stride 1, padding 1
- Activation: ReLU
- Output shape: (32, 5000)

**Block 3:**
- 64 filters, kernel size 3, stride 1, padding 1
- Activation: ReLU
- Output shape: (64, 5000)

#### Stage 3: Temporal Modeling (Transformer Encoder)
Multi-head self-attention transformer to capture rhythm patterns and long-range dependencies:

- **Number of layers:** 4
- **Hidden dimension:** 256
- **Number of attention heads:** 8
- **Head dimension:** 256 / 8 = 32
- **Positional encoding:** Sinusoidal positional embeddings
- **Dropout:** 0.2 (applied during training; disabled during inference)
- **Layer normalization:** Applied before each sublayer

**Computation flow per layer:**
1. Multi-head self-attention: Q, K, V projections from input; compute attention weights (softmax of Q*K^T/sqrt(d_k)); apply attention to V
2. Add + LayerNorm (residual connection)
3. Feedforward network: 2 linear layers (256 -> 1024 -> 256) with ReLU
4. Add + LayerNorm (residual connection)

**Rationale:** Transformer architecture excels at capturing ECG rhythm patterns because:
- Self-attention learns to focus on diagnostically relevant regions (irregular RR intervals in AFib, wide QRS in VT)
- Multi-head attention captures independent feature relationships simultaneously
- Positional encoding preserves temporal structure of 10-second recording
- No recurrent structures enable efficient parallel computation

#### Stage 4: Global Aggregation
- **Operation:** Global average pooling across time dimension
- **Input:** (4, 256, 5000) from transformer encoder
- **Output:** (4, 256) = reduced to single vector per attention head

#### Stage 5: Classification Head
Two fully connected (dense) layers with dropout:

**Layer 1:**
- Input: 256 (from global pooling)
- Output: 128
- Activation: ReLU
- Dropout: 0.2 (training only)

**Layer 2:**
- Input: 128
- Output: 4 (one for each class: AFib, VT, 1st deg AV block, Normal)
- Activation: None (raw logits)

#### Stage 6: Output Processing
- **Softmax:** Convert logits to probability distribution
- **Output:** 4-element probability vector (probabilities sum to 1.0)

### Total Model Parameters
- Convolutional feature extraction: ~50K parameters
- Transformer encoder: ~2.2M parameters
- Classification head: ~50K parameters
- **Total trainable parameters: 2.3M**

---

## 5. Output Specifications

### Output Format
**HTTP Response (JSON):**
```json
{
  "prediction_id": "PRED-2026-10-15-12345",
  "ecg_id": "ECG-2026-10-15-12345",
  "timestamp": "2026-10-15T14:30:05Z",
  "model_version": "v1.0_cleared_2026-10-15",
  "inference_time_ms": 87,
  "predictions": {
    "atrial_fibrillation": {
      "probability": 0.92,
      "ci_lower": 0.88,
      "ci_upper": 0.95
    },
    "ventricular_tachycardia": {
      "probability": 0.03,
      "ci_lower": 0.01,
      "ci_upper": 0.07
    },
    "first_degree_av_block": {
      "probability": 0.02,
      "ci_lower": 0.00,
      "ci_upper": 0.05
    },
    "normal_sinus_rhythm": {
      "probability": 0.03,
      "ci_lower": 0.01,
      "ci_upper": 0.08
    }
  },
  "clinical_interpretation": "FLAGGED",
  "flagged_classes": ["atrial_fibrillation"],
  "decision_threshold": 0.70,
  "recommended_action": "Clinician review recommended. Probability of atrial fibrillation is high (0.92). Consider cardiology consultation and evaluation for anticoagulation.",
  "confidence_level": "HIGH",
  "warnings": []
}
```

### Output Classes and Definitions

**Atrial Fibrillation (AFib):** Irregular heart rhythm originating in the atria; characterized by absence of P waves and irregular RR intervals. Probability in range [0, 1].

**Ventricular Tachycardia (VT):** Rapid heart rhythm originating in the ventricles; characterized by wide QRS complexes (>= 120 ms) and AV dissociation. Probability in range [0, 1].

**1st Degree Atrioventricular Block (1st Deg AV Block):** Conduction delay through the AV node; characterized by PR interval > 200 ms. Probability in range [0, 1].

**Normal Sinus Rhythm (NSR):** Normal cardiac rhythm; regular rate 60-100 bpm, normal P wave and QRS morphology, PR interval 120-200 ms. Probability in range [0, 1].

### Confidence Intervals
- **Method:** Softmax probability variance estimation (non-parametric)
- **Interpretation:** 95% confidence that true probability lies within reported interval
- **Use:** Clinician should regard probability < CI lower bound as conservative, probability > CI upper bound as optimistic

### Decision Threshold and Clinical Interpretation
- **Decision Threshold:** 0.70 (probability cutoff for "FLAGGED" result)
- **FLAGGED:** If any target class probability >= 0.70, result marked "FLAGGED" for clinician immediate review
- **NOT FLAGGED:** If all target class probabilities < 0.70, result marked "Normal" (no actionable arrhythmia detected)

### Recommended Actions
Device provides guidance to clinician based on predicted probabilities:
- **Probability 0.80-1.00:** "Strong evidence for [class]. Clinician action recommended (treat, refer, monitor)."
- **Probability 0.65-0.80:** "Moderate evidence for [class]. Cardiology consultation recommended for confirmation."
- **Probability 0.50-0.65:** "Equivocal. Clinical correlation and expert review recommended."
- **Probability < 0.50:** "No significant evidence for target arrhythmia."

---

## 6. Performance Characteristics

### Baseline Clinical Performance (Internal Validation on 37,500 test ECGs)

| Metric | Atrial Fibrillation | Ventricular Tachycardia | 1st Degree AV Block | Overall |
|---|---|---|---|---|
| AUROC | 0.95 | 0.93 | 0.90 | 0.94 |
| Sensitivity (@ 0.90 threshold) | 0.92 | 0.88 | 0.85 | 0.91 |
| Specificity | 0.96 | 0.94 | 0.92 | 0.94 |

### Clinical Validation Study Results (Multi-site, n=1500)

**Primary Endpoint Achieved:** AUROC 0.92 (95% CI: 0.89-0.94)  
**Secondary Endpoints Achieved:** Sensitivity 0.88, Specificity 0.92, PPV 0.90, NPV 0.91

### Inference Performance
- **Latency:** < 200 milliseconds per prediction (typical: 87 ms)
- **Throughput:** ~500 predictions per second per GPU instance
- **Availability:** 99.9% uptime (AWS multi-AZ deployment)

---

## 7. System Architecture and Deployment

### Cloud Deployment (AWS)
- **Platform:** Amazon Web Services (AWS)
- **Compute:** EC2 instances with GPU (NVIDIA A100)
- **Load balancing:** Application Load Balancer (ALB) for traffic distribution
- **Auto-scaling:** Horizontal scaling based on request volume (target: < 100 ms p99 latency)
- **Database:** RDS PostgreSQL for prediction logging (encrypted at rest, automated backups)
- **Encryption:** TLS 1.3 for data in transit; AES-256 for data at rest

### API Gateway
- **Protocol:** HTTPS (TLS 1.3)
- **Authentication:** OAuth 2.0 with encrypted bearer tokens
- **Rate limiting:** 1000 predictions/minute per health system (prevents abuse)
- **Logging:** All requests logged with timestamp, user, ECG ID, predictions (audit trail)

### Data Flow
1. EHR sends POST request with 12-lead ECG data via HTTPS to `/api/v1/predict`
2. API authenticates request via OAuth token
3. Input signal validation: quality checks, artifact detection
4. If signal quality insufficient, return error message
5. Signal preprocessing: normalization, filtering
6. Model inference: forward pass through trained neural network
7. Output post-processing: softmax to probabilities, confidence interval calculation
8. Result logged to database (de-identified, encrypted)
9. JSON response returned to EHR
10. EHR displays result to clinician within EHR UI

### Scalability and Reliability
- **Multi-AZ deployment:** Redundancy across multiple AWS availability zones
- **Auto-recovery:** Automated instance replacement if compute failure detected
- **Database replication:** Read replicas for high availability
- **Monitoring:** CloudWatch monitoring of API latency, error rates, GPU utilization
- **Alerting:** PagerDuty integration for on-call oncall alerts if error rate > 1%

---

## 8. Software Bill of Materials (SBOM)

**Framework and Libraries:**
- PyTorch 2.0.0 (deep learning framework, Apache 2.0 license)
- NumPy 1.24.0 (numeric computing, BSD 3-clause)
- SciPy 1.10.0 (scientific computing, BSD 3-clause)
- scikit-learn 1.3.0 (machine learning, BSD 3-clause)
- FastAPI 0.100.0 (web framework, MIT)
- Gunicorn 20.1.0 (WSGI server, MIT)
- Pydantic 2.0.0 (data validation, MIT)

**Infrastructure:**
- Python 3.10.12 (base runtime, PSF License)
- Docker 24.0.0 (containerization, Apache 2.0)
- Debian 12 (base OS image, GPL/proprietary mix)

**All dependencies are open-source with permissive licenses compatible with commercial use.**

---

## 9. Security Features

### Access Control
- OAuth 2.0 authentication for all API requests
- Role-based access control (RBAC) based on health system affiliation
- Encrypted API credentials managed via AWS Secrets Manager

### Data Protection
- HIPAA Business Associate Agreement (BAA) in place with AWS
- All patient data de-identified prior to storage (HIPAA Safe Harbor method)
- Encryption at rest: AES-256
- Encryption in transit: TLS 1.3
- Automated daily backups with 30-day retention

### Monitoring and Logging
- All API requests logged with timestamp, user, ECG ID
- Prediction audit trail maintained for 7 years
- Intrusion detection monitoring via AWS GuardDuty
- Vulnerability scanning: automated scans via AWS Inspector

### Compliance
- SOC 2 Type II certification
- HIPAA compliance
- Data residency: all data stored in US (no international data transfer)

---

## 10. Version Control and Change Management

### Model Versioning
- **Baseline Version:** v1.0 (FDA cleared 2026-10-15)
- **Model Artifacts:** Architecture, weights, preprocessing parameters version-controlled in private Git repository
- **Hash Verification:** All deployed models verified against published hash (sha256:4a8c9d2e7f1b5c3a6e9d2f0b4c8a1e5d) to ensure integrity

### Deployment Versioning
- **API Versioning:** /api/v1/ (major version in URL path)
- **Backward Compatibility:** v1.x updates maintain input/output format compatibility
- **Deprecation Policy:** 12-month advance notice before any API version retirement

### Change Control
- All changes documented in PCCP (Predetermined Change Control Plan)
- Model retraining requires approval from VP Clinical Affairs
- Security updates can be deployed immediately if vulnerability severity >= HIGH
- Other updates require 2-week notice to all deployed health systems

---

## References

- FDA Guidance for Industry: Predetermined Change Control Plans for Machine Learning-Enabled Medical Devices (December 2024)
- IEC 62304: Medical Device Software - Software Lifecycle Processes
- ISO 13485: Medical Devices - Quality Management Systems
