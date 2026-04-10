# Indications for Use (IFU) Statement

## Overview
The Indications for Use statement is a regulatory requirement describing the intended purpose of your device.
For AI/ML devices, this must be precise about what the algorithm does, who uses it, and the clinical context.
The IFU is the anchor for all other regulatory documentation.

**FDA Guidance:** Your IFU defines the scope of your 510(k). Any performance claim outside the IFU scope requires additional
submission or predicate justification. Keep it narrow and specific.

---

## Template

**Device Name:**
[INSERT: Official commercial name of device as it will appear on labeling and in FDA submission]

Example: "CardioDetect AI-ECG Analyzer" or "ImageAssist Cardiac Ultrasound Viewer"

---

**Intended Use:**
[INSERT: Clinical use case. Be explicit about what the AI algorithm does, not what the device as a whole does.]

The {Device Name} is a software-based clinical decision support system intended to:
- [Describe the primary diagnostic or monitoring task]
- [Specify how the output is used: diagnosis, screening, monitoring, risk assessment]
- [State whether it is used independently or in conjunction with other tools]

Example: "The CardioDetect AI-ECG Analyzer is intended to assist healthcare professionals in detecting
atrial fibrillation (AF) episodes from 12-lead electrocardiogram (ECG) recordings. The device provides
a probability score for AF presence and is intended as a clinical decision support tool to flag
potentially abnormal tracings for physician review. The device is not intended to be used as a
standalone diagnostic tool and does not replace clinical judgment."

---

**Intended User:**
[INSERT: Who uses the device? Specify clinical/technical qualifications.]

- Primary user: [e.g., Cardiologists, Emergency Medicine Physicians, Nurses, Technicians]
- Clinical setting: [e.g., Hospital cardiology departments, Emergency Departments, Outpatient clinics, Home monitoring]
- Required training: [Specify any training requirements beyond standard clinical practice]

Example: "Intended users are licensed healthcare professionals (physicians, nurse practitioners, physician assistants,
cardiac nurses) with formal training in ECG interpretation. Users must complete a 15-minute in-service
training before first use explaining the AI output format, confidence intervals, and workflow integration."

---

**Intended Patient Population:**
[INSERT: Who the device is used on. Include demographic, disease, and clinical status specifics.]

- **Age Range:** [e.g., Adults 18-85 years]
- **Disease/Condition:** [e.g., Patients with known or suspected cardiac arrhythmias, Post-MI monitoring]
- **Clinical Status:** [e.g., Acute, chronic, asymptomatic, symptomatic]
- **Exclusion Criteria:** [Any populations where the device should NOT be used]
- **Special Populations:** [Note any populations with different performance, if known]

Example: "The device is intended for use in adult patients (18+ years) with known or suspected
cardiac arrhythmias undergoing electrocardiographic monitoring in hospital or clinical settings.
The device is not intended for use in: (1) patients with pacemakers or implantable defibrillators
(ICD) due to signal artifacts; (2) pediatric patients (< 18 years); (3) patients with acute
myocardial infarction within 48 hours (performance not evaluated in this population)."

---

**Anatomic Site/Modality:**
[INSERT: What biological signal or imaging modality is analyzed.]

- Input modality: [e.g., 12-lead ECG, Cardiac ultrasound video, High-frequency ultrasound]
- Sampling rate/resolution: [e.g., 500 Hz ECG sampling, 60 fps video]
- Duration of recording: [e.g., 10-second strip, 2D cine loops]

Example: "Input consists of standard 12-lead electrocardiogram recordings at 500 Hz sampling rate.
Each recording is 10 seconds in duration as per standard clinical ECG acquisition protocols (AHA standard)."

---

**Clinical Setting:**
[INSERT: Where the device is used operationally.]

- Hospital departments: [e.g., Cardiology, Emergency Department, ICU]
- Outpatient/clinic settings: [Yes/No]
- Home use: [Yes/No, and if yes, specify constraints on patient type, monitoring protocol]
- Ambulatory monitoring: [e.g., Wearable devices, Holter monitors]

Example: "The device is deployed in hospital cardiology departments and Emergency Departments via
integration with existing ECG management systems (MUSE, GE CardioLab). Use is supervised by
licensed clinicians. The device is not intended for unsupervised home use."

---

**Prescription vs. Over-the-Counter (OTC):**
[INSERT: Regulatory classification.]

- Prescription Device (RX): Device is prescribed by a licensed healthcare professional
- Over-the-Counter (OTC): Device is available for consumer self-use

Example: "This is a prescription device. It is intended to be used only under the direction
of a licensed healthcare professional and may not be sold directly to consumers."

---

**Primary Function:**
[INSERT: What the AI specifically does. Not a use case, but the algorithmic output.]

The AI component:
- **Primary Output:** [e.g., Binary classification (AF present/absent), Probabilistic score (0-1), Risk stratification (low/medium/high)]
- **Secondary Outputs:** [e.g., Confidence intervals, Feature importance explanations, Alternative diagnoses]
- **Basis:** [e.g., Trained on 200,000 ECG records with >95% inter-rater agreement on ground truth]

Example: "The neural network outputs a probability score (0-1.0) for the presence of atrial fibrillation.
Scores > 0.5 trigger a clinical alert flag recommending physician review. The model also outputs
95% confidence intervals and highlights ECG regions of high model uncertainty."

---

**Contraindications:**
[INSERT: Situations where the device should NOT be used.]

- [e.g., Patients with pacemakers due to ECG signal artifacts]
- [e.g., Non-sinus rhythm baselines where AF detection is clinically irrelevant]
- [e.g., Recordings with >30% artifact or signal dropout]

Example: "Contraindications include: (1) Patients with permanent pacemakers or ICDs, as device
interrogation signals interfere with ECG interpretation; (2) Patients with atrial flutter without
atrial fibrillation, where the device output may be misinterpreted; (3) ECG recordings with
>30% baseline artifact as assessed by automated quality control."

---

**Limitations:**
[INSERT: Known performance boundaries and operational constraints. FDA expects honesty here.]

- **Technical Limitations:** [e.g., Only validated on 12-lead ECG, not compatible with wireless or wearable ECG formats]
- **Population Limitations:** [e.g., Trained predominantly on Caucasian/African-American populations; performance in Asian populations not evaluated]
- **Operational Constraints:** [e.g., Processing time ~2 seconds per ECG; batch processing not supported]
- **Clinical Limitations:** [e.g., Does not detect paroxysmal AF episodes shorter than 5 seconds]

Example: "Limitations include: (1) Algorithm is trained exclusively on standard 12-lead ECG recordings
and has not been validated on single-lead, wearable, or wireless ECG formats; (2) Training data
primarily included adult patients with mean age 62 years; performance in patients <30 years has
not been separately characterized; (3) The device does not detect very short AF episodes (<5 seconds)
due to the 10-second window architecture; (4) Processing latency is ~2 seconds per ECG record."

---

## Worked Examples

### Example 1: Cardiac AI (ECG-based Arrhythmia Detection)

**Device Name:** ArrhythmiaWatch-AI ECG Analyzer

**Intended Use:** The ArrhythmiaWatch-AI ECG Analyzer is a clinical decision support system
intended to assist cardiac professionals in identifying irregular heart rhythms from standard
12-lead electrocardiogram recordings. The device outputs a structured report categorizing
rhythm types (sinus, atrial fibrillation, atrial flutter, ventricular ectopy) with
associated confidence scores. It is intended for use by licensed cardiologists, cardiac nurses,
and trained technicians to flag potentially abnormal tracings for physician review and is not
intended as a standalone diagnostic tool.

**Intended User:** Licensed cardiologists, cardiac electrophysiologists, nurse practitioners
in cardiology, and cardiac technicians with formal ECG training. Users must complete the
manufacturer's 30-minute training module on report interpretation.

**Intended Patient Population:** Adult patients (18-85 years) with known or suspected
cardiac arrhythmias undergoing routine ECG monitoring in inpatient or outpatient settings.
Not intended for: (1) patients with implanted pacemakers; (2) pediatric patients; (3) critical
care monitoring (use only on completed tracings).

**Anatomic Site/Modality:** Standard 12-lead electrocardiograms at 500 Hz sampling rate,
10-second duration per AHA/ACC standards.

**Clinical Setting:** Hospital cardiology departments, cardiac catheterization labs, and
outpatient cardiology clinics. Device is deployed via secure cloud connection or local
hospital server. Supervised use only.

**Prescription:** RX. Available only to healthcare institutions and licensed practitioners.

**Primary Function:** Outputs multi-class probability distribution across 5 arrhythmia types
(sinus, AF, atrial flutter, PVC, other). Primary output is the highest-confidence classification
with >0.85 confidence threshold triggers flagging for mandatory physician review.

**Contraindications:** Pacemakers, pediatric patients, non-standard ECG formats.

**Limitations:** Validated only on standard 12-lead ECG. Training dataset biased toward
Caucasian populations (87%); African-American performance gap of 3.2%. Does not detect
paroxysmal events <10 seconds.

---

### Example 2: Imaging AI (Cardiac Ultrasound Analysis)

**Device Name:** EchoAssist AI Cardiac Function Analyzer

**Intended Use:** The EchoAssist AI Cardiac Function Analyzer is a computer-aided diagnostic
system intended to automatically measure left ventricular ejection fraction (LVEF) from
transthoracic echocardiography videos. The device outputs LVEF percentage with qualitative
categorization (normal, mildly reduced, moderately reduced, severely reduced) and is intended
as a time-saving screening tool for sonographers and cardiologists to prioritize cases and
flag measurements requiring cardiologist review. It does not replace standard LVEF measurement
by trained sonographers and is not intended for automated clinical decision-making.

**Intended User:** Registered Diagnostic Medical Sonographers (RDMS) or physicians with
formal echocardiography training. Minimum 100 patient exposures with manual LVEF measurement
recommended before using device-assisted workflow. Institutions must designate a cardiologist
or sonographer lead as quality assurance oversight.

**Intended Patient Population:** Adult patients (18-90 years) undergoing transthoracic
echocardiography for clinical indications (dyspnea, chest pain, known cardiomyopathy, post-MI
follow-up). Excluded populations: (1) patients with insufficient echo window (BMI >40, emphysema);
(2) post-cardiac surgery (within 1 week); (3) atrial fibrillation (LVEF measurement unreliable).

**Anatomic Site/Modality:** 2D cardiac ultrasound video (apical 4-chamber view) at 60 fps,
minimum 2 cardiac cycles, standard probe (phased array 2-4 MHz). Video must be in DICOM or
proprietary ultrasound machine export format.

**Clinical Setting:** Echocardiography labs within hospitals, outpatient cardiology clinics,
and regional medical centers. Device runs on Windows workstations connected to ultrasound
machines via proprietary interface. Requires PACS integration for medical records.

**Prescription:** RX. Available only to accredited echocardiography labs and hospitals.

**Primary Function:** Automated segmentation of left ventricular endocardium and epicardium
in apical 4-chamber view; outputs LVEF % with 95% CI and qualitative interpretation.
Confidence score indicates reliability of automated measurement (flagged if <0.80).

**Contraindications:** Suboptimal echocardiographic windows, arrhythmias, post-operative
state (confounding edema).

**Limitations:** Validated only on apical 4-chamber view at standard frame rates. Performance
drops in obese patients (BMI >35). Training data skewed toward male patients (64%). Does not
measure RV function, strain, or diastolic parameters. Requires offline processing (not real-time).

---

## Checklist Before Finalizing

- [ ] Device name is consistent with labeling and submission documents
- [ ] IFU is specific enough that performance requirements are unambiguous
- [ ] All limitations and contraindications are documented (no surprises for FDA reviewer)
- [ ] Intended user qualifications are clearly stated (supports labeling requirements)
- [ ] Population exclusions are explicit (needed for risk analysis and post-market surveillance)
- [ ] Clinical setting is operationally realistic (FDA will ask "where is this actually used?")
- [ ] Output format matches what the algorithm actually produces (no confusion about confidence scores vs. binary decisions)
- [ ] If there are performance differences by subgroup, they are reflected in the IFU limitations
