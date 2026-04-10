# Device Description for AI/ML-Enabled Devices

## Overview
The Device Description section explains how your device works. For AI/ML devices, FDA expects:
1. Overall system architecture and data flow
2. The AI/ML model itself (architecture, training, inputs, outputs)
3. How clinical users interact with the AI output
4. Software lifecycle and interoperability standards

This section bridges the gap between the Indications for Use (what the device does clinically)
and Performance Testing (how well it does it).

**FDA Guidance:** Be precise. Vague descriptions like "uses machine learning" signal
regulatory risk. FDA reviewers want to understand *exactly* what happens when a clinician
provides input, frame by frame or calculation by calculation.

---

## Template

## 1. System Overview and Architecture

### 1.1 High-Level System Description

Provide a 1-2 paragraph overview of the device and its major components.

[INSERT: System description]

Example: "The CardioDetect AI-ECG Analyzer consists of three components: (1) an ECG
data ingestion module that connects to hospital ECG management systems (MUSE, Philips, GE);
(2) a preprocessing pipeline that normalizes ECG signals and applies artifact removal;
(3) a convolutional neural network (CNN) classifier trained to detect atrial fibrillation;
and (4) a clinical reporting module that formats model outputs into a structured physician
report with confidence scores and quality flags. The system does not store patient data
beyond the duration of analysis (analyzed-on-receipt model) unless explicitly configured
for audit logging by the institution."

---

### 1.2 System Architecture Diagram

[INSERT DIAGRAM: A block diagram showing data flow from input to clinical output.]

Recommended format:
- Text-based ASCII diagram or reference to external diagram file
- Label each component (ingestion, preprocessing, AI model, post-processing, reporting)
- Show data flow: raw input -> processed input -> model inference -> post-processing -> clinical output
- Indicate where human review/override occurs
- Show any external system interfaces (EHR, PACS, laboratory systems)

Example diagram (ASCII):

```
┌─────────────────────────────────────────────────────────────────┐
│                    ECG Management System (MUSE)                 │
│                   (Hospital network or cloud)                   │
└────────────┬────────────────────────────────────────────────────┘
             │ HL7/FHIR: ECG + Patient metadata
             ▼
   ┌─────────────────────┐
   │  Ingestion Module   │ (Validates HL7, extracts ECG waveform)
   └──────────┬──────────┘
              │ Raw ECG: 12 leads, 500 Hz, 10-second window
              ▼
   ┌──────────────────────────────┐
   │  Preprocessing Pipeline      │ (Filtering, normalization, resampling)
   │  - Bandpass filter (0.5-100) │
   │  - Baseline removal          │
   │  - Lead normalization        │
   └──────────┬───────────────────┘
              │ Preprocessed ECG: standardized input tensor
              ▼
   ┌──────────────────────────────────┐
   │    AI/ML Model                   │ (CNN, trained on 200K ECGs)
   │  - Input: 12 x 5000 (5-second)  │
   │  - Output: P(AF) [0-1]           │
   └──────────┬───────────────────────┘
              │ Raw model output: probability score, confidence
              ▼
   ┌──────────────────────────────┐
   │  Post-Processing & Reporting │ (Threshold, qualitative labels, QA checks)
   │  - Threshold P(AF) > 0.5     │
   │  - Flag low-confidence cases  │
   │  - Automated quality check    │
   └──────────┬───────────────────┘
              │ Structured report with confidence intervals
              ▼
   ┌──────────────────────────────┐
   │  Clinical Reporting Module   │ (Format for physician review)
   │  - PDF + EHR integration      │
   │  - Explanation of output      │
   └──────────┬───────────────────┘
              │ Physician review: accept/override/discard
              ▼
┌────────────────────────────────────────┐
│  Electronic Health Record (EHR)        │
│  Result stored with audit trail        │
└────────────────────────────────────────┘
```

---

### 1.3 Data Flow and Processing Sequence

Describe the step-by-step progression of data through the system.

[INSERT: Detailed data flow narrative]

Example: "When a 12-lead ECG is acquired on a hospital ECG machine (e.g., GE MAC 5500),
the device transmits the recording via HL7 to the CardioDetect server. (1) The ingestion
module validates the HL7 message, extracts the waveform data and patient metadata (age, sex),
and logs the receipt. (2) The preprocessing pipeline applies a 0.5-100 Hz bandpass filter
to remove DC drift and high-frequency noise, resamples to exactly 500 Hz if needed, and
normalizes each lead to zero mean and unit variance. (3) The normalized 12-lead signal
(5000 samples per lead) is passed to the CNN model, which outputs a probability score
P(AF) and a confidence metric (uncertainty estimate via Monte Carlo dropout). (4) A threshold
rule converts the probability to a categorical recommendation: P(AF) > 0.7 = 'AF likely',
0.5-0.7 = 'uncertain, review', <0.5 = 'Normal rhythm'. (5) A quality control check flags
if the input ECG had >20% artifact or if the model confidence was <0.6. (6) The reporting
module formats the result as a PDF and pushes to the EHR with a discrete result code
(LOINC 8633-8 for atrial fibrillation) and an alert flag if AF is detected. (7) Physician
reviews the AI output in the EHR, with option to override or discard the result. (8) The
final interpretation (physician decision, not AI output) is stored in the medical record
with full audit trail."

---

## 2. AI/ML Model Specification

### 2.1 Model Architecture

Describe the model's mathematical structure, layers, and hyperparameters.

[INSERT: Architecture details]

Important elements:
- Model type (CNN, RNN, transformer, decision tree ensemble, etc.)
- Number of layers, layer types, dimensions
- Activation functions
- Any regularization (dropout, batch norm, L1/L2)
- Total number of trainable parameters
- Inference latency (on typical hardware)

Example: "The atrial fibrillation detection model is a 1D convolutional neural network
with the following architecture:

- Input layer: 12 channels (ECG leads), 5000 time steps (10 seconds at 500 Hz)
- Conv block 1: 32 filters (kernel=5), ReLU, Batch Norm, Max Pool (stride=2)
- Conv block 2: 64 filters (kernel=5), ReLU, Batch Norm, Max Pool (stride=2)
- Conv block 3: 128 filters (kernel=3), ReLU, Batch Norm, Max Pool (stride=2)
- Conv block 4: 256 filters (kernel=3), ReLU, Batch Norm, Max Pool (stride=2)
- Global Average Pooling
- Dropout (p=0.5)
- Dense layer: 256 units, ReLU
- Output layer: Binary softmax (AF vs. non-AF)

Total trainable parameters: 847,234. Inference latency on NVIDIA T4 GPU: ~150 ms per ECG.
Model size: 3.2 MB (quantized to 16-bit weights)."

---

### 2.2 Training Algorithm and Hyperparameters

Describe how the model was trained (loss function, optimizer, learning schedule, stopping criteria).

[INSERT: Training details]

Key information FDA expects:
- Loss function (binary cross-entropy, focal loss, custom loss)
- Optimizer (Adam, SGD, etc.) and learning rate schedule
- Batch size, training epochs, stopping criteria (early stopping patience)
- Class weights (if imbalanced data)
- Computational environment (GPU type, training time)

Example: "The model was trained using binary cross-entropy loss with Adam optimizer
(learning rate 1e-3, beta1=0.9, beta2=0.999, epsilon=1e-8). Data was presented in batches
of 64 ECGs. Training ran for up to 500 epochs with early stopping if validation loss did
not improve for 15 consecutive epochs. Class weights were applied to account for AF
prevalence in the training set: non-AF=0.35, AF=2.80 (computed as total_samples / (2 * class_samples)).
No learning rate decay was applied. Training was conducted on 8x NVIDIA A100 GPUs using
PyTorch 2.0, distributed data-parallel, taking ~24 hours to convergence. All hyperparameters
were selected via random search over 200 configurations evaluated on a held-out validation set."

---

### 2.3 Training Data Characterization

[INSERT: Summary of training data. DETAILED version is in template 05.]

Provide a brief summary here; delegate detailed treatment to Section 5 (Training Data).

Example: "The model was trained on 200,000 ECG recordings from three academic medical centers
(Mayo Clinic, Cleveland Clinic, Johns Hopkins) collected between 2015-2020. Records were
selected to represent the full spectrum of clinical AF presentations: paroxysmal (35%),
persistent (50%), permanent (15%). Demographic breakdown: mean age 67 years (SD=14), 58% male,
82% Caucasian, 12% African-American, 3% Asian, 3% other. AF ground truth was established by
cardiologist consensus review (>2 independent readers) or clinical diagnosis confirmed by
continuous monitoring (Holter, event monitor, pacemaker logging). Details on data splits,
exclusion criteria, annotation quality, and bias analysis are in Section 5."

---

## 3. Input Data Specification

### 3.1 Input Data Format and Requirements

Describe exactly what data the model accepts.

[INSERT: Input specification]

- Data modality: [e.g., 12-lead ECG, single-lead, continuous waveform]
- File format: [e.g., DICOM-ECG, HL7 OBX segments, CSV, manufacturer proprietary]
- Sampling rate: [e.g., 500 Hz for ECG, frame rate for video]
- Duration/length: [e.g., 10-second window, minimum/maximum]
- Pre-processing applied before input to model: [e.g., filtering, normalization]
- Acceptable ranges/constraints: [e.g., signal amplitude limits, artifact tolerance]

Example: "Input to the model is a 12-lead ECG waveform with the following specifications:
- Modality: Standard 12-lead electrocardiogram (leads: I, II, III, aVR, aVL, aVF, V1-V6)
- Sampling rate: 500 Hz (tolerance: 480-520 Hz, resampled to exactly 500 Hz)
- Duration: 10 seconds (50 arbitrary drift or baseline wander
- Quality constraint: Maximum 20% baseline artifact (detected via automated QC)
- Voltage range: -5 to +5 mV (signals outside this range are flagged as technical errors)
- File format: HL7 v2.5 with ECG waveform in OBX segments, or DICOM-ECG as defined by DICOM
  Part 16. API also accepts raw binary files (ECG.dat format defined in appendix).
- Preprocessing: The ingestion module applies a digital 0.5-100 Hz Butterworth filter, mean
  subtraction, and per-lead z-score normalization (μ=0, σ=1) before passing to the model.
  Resampling uses linear interpolation if sampling rate != 500 Hz."

---

### 3.2 Data Quality and Rejection Criteria

What causes the device to reject input or flag it as low-confidence?

[INSERT: Rejection criteria]

Example: "Input ECGs are rejected (not processed) if: (1) HL7 validation fails; (2) waveform
data is missing for any of the 12 leads; (3) recording duration is <8 seconds or >12 seconds;
(4) any single lead contains >30% artifact (detected via signal entropy and power spectral analysis);
(5) voltage amplitude on any lead exceeds +/-6 mV (suggests electrode malfunction). ECGs that pass
input validation but show markers of low confidence include: (1) overall signal artifact >15%;
(2) model confidence score <0.6; (3) inconsistent predictions across overlapping windows
(5-second sliding window with 50% overlap). Such cases are flagged with a 'MANUAL REVIEW RECOMMENDED'
label in the clinical output."

---

## 4. Output Data Specification

### 4.1 Model Output Format

Describe exactly what the model outputs.

[INSERT: Output specification]

- Primary output: [e.g., binary classification, probabilistic score, continuous value]
- Secondary outputs: [e.g., confidence intervals, feature importance, attention maps]
- Output range and interpretation: [e.g., 0-1 probability, class labels]
- Post-processing applied: [e.g., threshold rules, confidence filtering]

Example: "The model outputs a dictionary with the following fields:

- `prediction_class`: String, one of {'AF', 'Non-AF'}. Derived from thresholding the
  probability score (p_af >= 0.5).
- `p_af`: Float [0, 1]. Raw model output (softmax probability for AF class).
- `confidence`: Float [0, 1]. Model uncertainty quantified via Monte Carlo dropout:
  10 stochastic forward passes with dropout=0.3; confidence = 1 - variance(predictions).
  Confidence < 0.6 triggers manual review flag.
- `explanation`: Dictionary containing per-lead saliency scores (values [-1, 1]).
  Computed via GradCAM applied to the temporal attention layer.
  Indicates which leads/timepoints drove the prediction.
- `processing_info`: Dictionary with metadata: `input_heart_rate` (BPM, computed from
  QRS intervals), `artifact_level` (0-1 fraction), `timestamp`, `model_version`.

Example output (JSON):
{
  "prediction_class": "AF",
  "p_af": 0.87,
  "confidence": 0.94,
  "explanation": {
    "lead_II": 0.62,
    "lead_V1": 0.58,
    "lead_III": -0.15
  },
  "processing_info": {
    "input_heart_rate": 112,
    "artifact_level": 0.08,
    "model_version": "1.2.1",
    "inference_time_ms": 147
  }
}
"

---

### 4.2 Clinical Presentation of Output

How does the output appear to the physician?

[INSERT: Clinical output format]

Example: "The AI output is formatted as a structured report integrated into the hospital
EHR. The report displays:

CLINICAL REPORT
- Title: 'Automated Atrial Fibrillation Detection'
- Key result: [Red alert box if AF detected] 'ATRIAL FIBRILLATION LIKELY PRESENT (Confidence: 94%)'
  or [Green box if normal] 'Normal sinus rhythm (Confidence: 91%)'
- Numerical data: Probability score as percentage, confidence interval (95% CI: 0.84-0.91)
- Visual explanation: Color-coded ECG waveform highlighting leads with highest AF likelihood
- Physician action items: 'Recommend: Clinical review. If AF confirmed, consider rate/rhythm control.'
- Disclaimer: 'This is a clinical decision support tool. Interpretation by a qualified
  clinician is required. Do not rely on this output for clinical decision-making without
  manual verification.'

The report also includes a 'View Raw Output' option that displays the complete JSON
payload for electronic systems or research use.

Labeling includes: LOINC code 8633-8 (Atrial fibrillation episode indicator),
reference range 'Negative', abnormal flag if AF is detected."

---

## 5. Software Development Lifecycle (SDLC)

### 5.1 Version Control and Release Management

Describe how the software is versioned, tested, and released.

[INSERT: SDLC details]

Reference FDA guidance: IEC 62304 (medical device software lifecycle)

Example: "The device software follows IEC 62304 Class C (highest rigor) practices:

- Version control: Git with signed commits. Main branch protected; all changes via code review
  (2+ reviewers minimum). Tags mark official releases (semantic versioning: MAJOR.MINOR.PATCH).
- Testing: Automated test suite covers unit tests (>90% code coverage), integration tests
  (full data pipeline), and validation tests (reference ECG sets). All tests must pass before release.
- Deployment: Releases are cryptographically signed. Hospital installations pull updates
  from a secure registry (Docker Hub) with vulnerability scanning (Trivy).
- Change management: Any change to model, preprocessing, or thresholds requires:
  (1) engineering design review; (2) impact assessment (does it affect predicate equivalence?);
  (3) abbreviated validation (performance on held-out test set); (4) labeling update if needed;
  (5) post-market surveillance plan modification. All tracked in change control log.
- Documentation: Every release is accompanied by release notes specifying changes,
  impact on performance (compared to prior version), and any labeling updates."

---

### 5.2 Regulatory Compliance

[INSERT: Compliance and standards]

- IEC 62304 compliance level: [A, B, or C]
- Cybersecurity: [NIST Cybersecurity Framework, IEC 62304-1 Annex D]
- Data protection: [HIPAA, GDPR]
- Software as a Service (SaaS) vs. installed: [Model and processing location]
- Updates and patches: [Frequency, mechanism, rollback procedures]

Example: "The device software development and maintenance complies with IEC 62304:2015
(medical device software lifecycle) at Class C (highest rigor). Cybersecurity follows
NIST Cybersecurity Framework (v1.1): all data in transit is encrypted (TLS 1.3), data
at rest is encrypted (AES-256), and authentication uses OAuth 2.0 with multi-factor
authentication. The device is HIPAA BAA compliant; patient data is encrypted end-to-end
and is never stored on shared infrastructure. The AI model itself (weights + architecture)
is version-controlled and digitally signed; any unauthorized modification is detectable.
All hospital deployments are containerized (Docker) with immutable images; rollback to
prior version takes <5 minutes. Model updates are released monthly (if needed) with
abbreviated validation on the held-out test set (>95% of original performance required
for deployment)."

---

## 6. Interoperability and Integration Standards

### 6.1 System Interoperability

Describe how the device integrates with clinical systems.

[INSERT: Interoperability details]

- Data exchange standards: [HL7 v2/FHIR, DICOM, proprietary APIs]
- EHR integration: [Which systems are supported? Cerner, Epic, Meditech, etc.]
- Data storage: [Device-local database, EHR-embedded, cloud]
- Authentication: [OAuth, LDAP, SSO]

Example: "The device integrates with hospital ECG management systems and EHRs using:

- Data ingest: HL7 v2.5 messages (standard hospital integration) or FHIR R4 API (future
  interoperability). ECG waveforms are sent as base64-encoded binary or DICOM-ECG format.
- EHR integration: RESTful API with OAuth 2.0 authentication. Supported EHR systems:
  Epic (v2023), Cerner (v2024), Philips (e-HIS). Results are written as discrete HL7
  OBX segments (result code LOINC 8633-8) and appear in the physician's standard result
  review interface.
- Authentication: Hospitals integrate via secure API key or SSO (SAML 2.0). User roles
  (physician, technician, admin) are synced from EHR role-based access control (RBAC).
- Data storage: Patient data (name, ID, ECG waveform) is never stored in the AI device;
  it is temporarily held in memory during processing (~1 second) and discarded after
  result generation. Audit logs (event, user, timestamp) are stored locally for 90 days
  (configurable) then purged."

---

### 6.2 Standards Compliance

[INSERT: Standards adopted]

- DICOM: [Which parts? Part 3 (Information Object Definitions), Part 4 (Service Class User), Part 18 (Web Services)]
- HL7: [v2.5, FHIR R4, CDA]
- LOINC/SNOMED: [Result codes and terminology]

Example: "The device adheres to:
- DICOM Part 3: Information Object Definitions for ECG (IOD Definitions, ECG Module)
- DICOM Part 4: Service Class User (Store SCP, Query/Retrieve SCP)
- DICOM Part 18: Web Services (RESTful QIDO-RS, WADO-RS)
- HL7 v2.5: Standard hospital messaging for ECG transmission and result reporting
- LOINC: Result codes (8633-8 for AF detection, 3625-0 for heart rate)
- SNOMED CT: Diagnosis codes (164890007 'Atrial fibrillation', 426627006 'Paroxysmal atrial fibrillation')
- IEC 62304: Software lifecycle management for medical devices"

---

## 7. Regulatory Classification and Predicate Device Justification

### 7.1 Device Classification

[INSERT: FDA classification and regulatory pathway]

Example: "This device is classified by the FDA as a Class II Medical Device (moderate risk).
The predicate devices are:

- K232488 (Anumana ECG-AI, atrial fibrillation detection) - same intended use, same modality
- K233429 (Eko AI-Cardiac Murmur Detection) - same use of AI for cardiovascular screening

The subject device (CardioDetect) demonstrates substantial equivalence to these predicates
based on: (1) identical intended use (AF detection from ECG); (2) identical input modality
(12-lead ECG); (3) similar output (probabilistic classification); (4) non-significant
technological differences (different neural network architecture, but same preprocessing,
same performance benchmarks). See Section 3 (Substantial Equivalence) for detailed comparison."

---

## Checklist Before Finalizing

- [ ] Architecture diagram is clear and labeled (shows data flow, interfaces, AI model location)
- [ ] Model specification includes enough detail to reproduce (architecture, hyperparameters, training procedure)
- [ ] Input and output formats are precise and match actual implementation (no ambiguity for FDA reviewer)
- [ ] Data quality and rejection criteria are documented (prevents misuse)
- [ ] SDLC practices comply with IEC 62304 (demonstrates control over software changes)
- [ ] Interoperability details are complete (EHR system support, standards, authentication)
- [ ] All references to external standards are specific (e.g., DICOM Part 18, HL7 v2.5, not just "DICOM" or "HL7")
- [ ] Cybersecurity and HIPAA compliance are addressed (FDA cares about data protection)
- [ ] Version control and change management procedures are documented (post-market surveillance depends on this)
