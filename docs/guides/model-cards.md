# Model Cards: FDA-Aligned Model Documentation

Model cards document machine learning models. This guide covers FDA-specific model card fields, focusing on clinical validation and real-world performance.

---

## What is a Model Card?

A model card is a standardized way to document an ML model. It answers:

- What is this model? (Name, version, purpose)
- How was it trained? (Data, preprocessing, hyperparameters)
- How well does it perform? (Metrics, across populations)
- What are its limitations? (Edge cases, failure modes)
- How should it be used? (Intended use, not-intended-use)

Mitchell et al. (2019) published the foundational model card format. This toolkit extends it with FDA-specific fields for medical devices.

---

## FDA Model Card Sections

An FDA model card should have:

### 1. Model Details

**Basic Information**

```markdown
## Model Details

**Model Name**: AI-ECG Arrhythmia Detector
**Model Version**: 2.0.1
**Release Date**: 2025-03-15
**Model Type**: Convolutional Neural Network
**Framework**: PyTorch 2.0
**Model Architecture**: ResNet-50, fine-tuned
**Pre-training**: ImageNet (general image recognition)
**Fine-tuning Dataset**: 150,000 12-lead ECGs
**Model Size**: 98 MB (FP32 weights)
**Inference Latency**: 1-2 seconds on AWS Lambda
**Training Time**: 3 days on 8x V100 GPUs

**Intended Users**:
- Cardiologists
- Emergency medicine physicians
- ECG technicians
- Hospital IT (deployment/maintenance)

**Primary Use Case**: Automated detection of atrial fibrillation from ECG
**Deployment Target**: Cloud-based SaMD via AWS
```

### 2. Data Characterization

FDA requires detailed documentation of training data.

```markdown
## Training Data

**Data Sources**:
- MIMIC-III: 80,000 ECGs (USA, ICU patients, open access)
- Partner Hospital A: 50,000 ECGs (USA, academic medical center, 2020-2022)
- Partner Hospital B: 20,000 ECGs (USA, community hospital, 2022-2023)
- Total: 150,000 ECGs

**Data Characteristics**:
- Patient demographics:
  - Age: Mean 62 years, range 18-95
  - Gender: 55% male, 45% female
  - Race/ethnicity: [Document if available, note limitations]
- Clinical characteristics:
  - 30% with documented atrial fibrillation
  - 40% normal sinus rhythm
  - 30% other arrhythmias (PVCs, bradycardia, etc.)
- ECG hardware:
  - Philips PageWriter (40%)
  - GE MAC (35%)
  - Schiller (25%)
- Signal characteristics:
  - Sampling rate: 500 Hz
  - Duration: 10 seconds
  - 12-lead standard
  - Missing data: <1% have incomplete leads

**Data Preprocessing**:
- Bandpass filter: 0.5-40 Hz (removes baseline wander and high-frequency noise)
- Normalization: Z-score normalization (zero mean, unit variance) per lead
- Segmentation: Fixed 10-second windows
- Resampling: Interpolation for non-standard rates
- Artifact removal: Manual review, <1% flagged as unusable

**Data Limitations**:
- Not representative of pediatric patients (<18 years)
- Limited racial/ethnic diversity [specify if known]
- Predominantly from USA hospitals [generalization risk to other countries]
- No data from wearable ECG devices
- Limited representation of patients on pacemakers
- Training data not uniformly distributed by arrhythmia type

**Data Provenance**:
- MIMIC-III: Publicly available, Johnson Lab, MIT
- Partner data: De-identified via [method], approved by [IRB #]
- Data retention: [How long is training data kept?]
- Data version control: [How are versions tracked?]
```

### 3. Performance Documentation

FDA wants to see detailed performance metrics, broken down by sub-population.

```markdown
## Model Performance

**Performance Metrics** (on holdout test set, 30,000 ECGs):

| Metric | Value | 95% CI |
|--------|-------|--------|
| Sensitivity (True Positive Rate) | 0.940 | 0.920-0.960 |
| Specificity (True Negative Rate) | 0.910 | 0.890-0.930 |
| Positive Predictive Value (Precision) | 0.880 | 0.860-0.900 |
| Negative Predictive Value | 0.950 | 0.930-0.970 |
| Area Under ROC Curve (AUC) | 0.970 | 0.960-0.980 |
| Balanced Accuracy | 0.925 | 0.905-0.945 |

**Sub-Population Performance** (Critical for FDA):

Performance by Age:
| Age Group | N | Sensitivity | Specificity | AUC |
|-----------|---|-------------|-------------|-----|
| 18-45 | 5,000 | 0.960 | 0.930 | 0.980 |
| 45-65 | 10,000 | 0.945 | 0.915 | 0.975 |
| 65+ | 15,000 | 0.920 | 0.895 | 0.960 |
| Overall | 30,000 | 0.940 | 0.910 | 0.970 |

Assessment: Performance consistent across age groups. Slight decrease in older 
patients (65+) expected due to comorbidities and signal quality. Differences 
within acceptable limits for clinical use.

Performance by Gender:
| Gender | N | Sensitivity | Specificity | AUC |
|--------|---|-------------|-------------|-----|
| Female | 13,500 | 0.935 | 0.920 | 0.970 |
| Male | 16,500 | 0.945 | 0.905 | 0.970 |
| Overall | 30,000 | 0.940 | 0.910 | 0.970 |

Assessment: No significant disparities by gender. Sensitivity slightly higher 
in males, specificity slightly higher in females, difference <2%.

Performance by Comorbidity:
| Condition | N | Sensitivity | Specificity |
|-----------|---|-------------|-------------|
| Hypertension | 18,000 | 0.938 | 0.908 |
| No hypertension | 12,000 | 0.943 | 0.914 |
| Diabetes | 8,000 | 0.935 | 0.905 |
| No diabetes | 22,000 | 0.942 | 0.912 |
| Prior MI | 5,000 | 0.930 | 0.900 |
| No prior MI | 25,000 | 0.943 | 0.913 |

Assessment: Performance stable across relevant comorbidities. No group shows 
unacceptable degradation.

**Comparison to Reference Standard**:

Comparison to cardiologist manual interpretation (blinded, 5,000 ECGs):
| Measure | Cardiologists | AI Model | Difference |
|---------|---------------|----------|------------|
| Sensitivity | 0.900 | 0.940 | +4.0% |
| Specificity | 0.950 | 0.910 | -4.0% |
| AUC | 0.950 | 0.970 | +2.0% |

Assessment: Model achieves higher sensitivity (fewer missed AFib) at cost of 
slightly lower specificity (more false alarms). Trade-off acceptable for 
screening/detection use case.

**Confidence Intervals**: All performance metrics include 95% confidence 
intervals calculated via bootstrapping (10,000 iterations).
```

### 4. Limitations and Failure Modes

FDA wants you to be honest about limitations.

```markdown
## Limitations and Failure Modes

### Known Limitations

**Signal Quality Dependence**:
- Model trained on clean 12-lead ECGs
- Performance degrades on noisy signals (e.g., patient movement, electrical interference)
- Recommendation: Reject ECGs with signal quality <0.8 (on 0-1 scale)

**Hardware Dependence**:
- Training data from 3 specific ECG devices (Philips, GE, Schiller)
- No data from consumer wearable ECGs (Apple Watch, Fitbit)
- New hardware may require revalidation

**Pediatric Patients**:
- Model NOT validated in patients <18 years
- Do not use in children without additional clinical validation
- ECG morphology differs significantly in pediatric population

**Pacemaker Patients**:
- Model shows high false positive rate in paced rhythms (pacing artifacts mimic arrhythmias)
- Not recommended for pacemaker patients without operator verification

**Special Populations**:
- Limited data on patients with prior cardiac surgery
- Unknown performance in patients on specific medications
- Not tested on rare arrhythmia types

### Failure Modes and Detection

**Failure Mode 1: Data Drift**
- Description: Real-world ECG distribution differs from training data
- Impact: Sensitivity drops from 0.94 to 0.85 on new hospital's data
- Detection: Weekly monitoring of model confidence distribution vs. baseline
- Mitigation: Retrain on new data, or investigate root cause (new hardware, patient population shift)

**Failure Mode 2: Corrupt/Incomplete Input**
- Description: ECG with missing leads, extreme baseline shift, or noise
- Impact: Model inference on corrupt signal may be meaningless
- Detection: Input validation before inference (check for >8 valid leads)
- Mitigation: Reject input, request re-acquisition of ECG

**Failure Mode 3: Concept Drift**
- Description: New arrhythmia types or presentations appear over time
- Impact: Model not trained on new patterns, performance unknown
- Detection: Audit logs identify ECGs where model confidence is low but clinician reviews
- Mitigation: Investigate, potentially trigger retraining

### Edge Cases

The model's performance has not been validated in:
- Extreme bradycardia (<30 bpm)
- Extreme tachycardia (>200 bpm)
- Atrial fibrillation with rapid ventricular response
- Complex arrhythmia combinations
- Patients on specific drugs (amiodarone, etc.)

Operator should manually review ambiguous cases.

### Recommendations for Use

- Use as screening/adjunct tool, not sole diagnostic tool
- Clinician should review model output and ECG waveform
- In case of disagreement: prioritize clinical judgment
- For high-risk patients, consider multiple ECGs over time
- When in doubt, refer to cardiology

### Mitigation Strategies

We mitigate these limitations through:

1. **Monitoring**: Continuous performance tracking (sensitivity/specificity daily)
2. **Retraining**: Monthly retraining on new data to adapt to drift
3. **Alerts**: Automatic alerts when sensitivity drops below 0.90
4. **Documentation**: Audit trail of all model decisions
5. **Human-in-the-loop**: Design ensures clinician reviews all high-risk cases
```

### 5. Intended Use and Usage Restrictions

Be explicit about what the model should and shouldn't be used for.

```markdown
## Intended Use and Usage Restrictions

### Intended Use

The AI-ECG Arrhythmia Detector is intended for:
- Automated screening of 12-lead ECGs for atrial fibrillation
- Adjunctive analysis to cardiologist review
- Hospital inpatient and outpatient ECG analysis
- Adult patients aged 18-85 with typical ECG hardware

### NOT Intended For

The model is NOT intended for:
- Pediatric patients (<18 years) - not validated
- Pacemaker patients - high false positive rate
- Consumer wearables or non-standard ECG devices
- Real-time continuous monitoring (designed for discrete 10-second ECGs)
- Diagnosis of non-arrhythmia cardiac conditions (e.g., myocardial infarction)
- Countries/healthcare systems with different ECG standards
- Patients unable to lie still for 10-second recording

### Usage Context

- **Setting**: Hospital ECG lab, ER, outpatient clinic
- **User**: Cardiologist, emergency physician, ECG technician
- **Workflow**: ECG acquired, sent to system, result reviewed by clinician
- **Decision**: Clinician makes final decision based on ECG + model output
- **Risk**: False negative misses AFib; false positive causes unnecessary workup

### Restrictions

- Do not use model output as sole basis for diagnosis
- Do not use for 24-hour Holter or event monitors (different format)
- Do not redistribute model or use it in unauthorized systems
- Do not combine with other models without validation
```

### 6. Training and Validation Procedures

```markdown
## Training and Validation Procedures

### Training Procedure

**Data Split**:
- Training: 70% (105,000 ECGs)
- Validation: 15% (22,500 ECGs) - used for hyperparameter tuning
- Test: 15% (22,500 ECGs) - held out, used for final evaluation

**Hyperparameters**:
- Optimizer: Adam (learning rate 0.001)
- Batch size: 32
- Epochs: 50 (early stopping if validation loss plateaus for 5 epochs)
- Loss function: Cross-entropy
- Regularization: Dropout (0.2), L2 (0.0001)

**Training Environment**:
- Hardware: 8x NVIDIA V100 GPUs
- Time: 3 days total
- Framework: PyTorch 2.0
- Version control: Git, reproducible from commit hash abc123def

### Validation Procedures

**External Validation** (Recommended Before Submission):
- Prospective evaluation on 1,000 ECGs from new hospital not in training
- Sensitivity: 0.93, Specificity: 0.90
- No significant performance degradation vs. test set

**Stress Testing**:
- Adversarial inputs: ECGs with added noise, clipping, missing leads
- Model remains robust (sensitivity >0.90) up to SNR of 10 dB

**Sub-population Testing**:
- Stratified sampling by age, gender, comorbidity
- Results shown above
```

### 7. Monitoring and Maintenance

```markdown
## Monitoring and Maintenance Plan

### Post-Deployment Monitoring

**Daily Metrics**:
- Number of ECGs analyzed
- Model sensitivity on rolling 1000-ECG window
- Model specificity on rolling 1000-ECG window
- Inference latency and error rate

**Weekly Reporting**:
- Performance summary compared to baseline
- Flag if sensitivity drops below 0.90
- Alert if specificity drops below 0.88

**Monthly Actions**:
- Full performance analysis across sub-populations
- Check for data drift (KL divergence vs. training distribution)
- Review audit logs for failures or edge cases
- Decide: maintain current model or trigger retraining

### Retraining Triggers

- **Scheduled**: Monthly retraining if >50,000 new ECGs available
- **Performance**: If sensitivity drops below 0.90 for 2 weeks
- **Data Drift**: If KL divergence >0.1 vs. training distribution
- **Clinical**: If cardiologists report systematic disagreement

### Rollback Procedure

If new model fails validation:
- Revert to previous model (< 5 seconds downtime)
- Alert data science team
- Investigation required before next retraining
- Document incident for FDA audit trail

### Model Versioning

- Version 2.0: Initial release, 150K ECG training
- Version 2.0.1: Patch for inference latency optimization
- Version 2.1: [Planned] Quarterly retraining, expanded hardware support

All versions kept in model registry with exact weights and hyperparameters.
```

---

## Model Card Template (Markdown)

Here's a complete markdown template you can copy:

```markdown
# Model Card: [Model Name]

## Model Details

**Model Name**: [Name]
**Version**: [v0.1]
**Release Date**: [YYYY-MM-DD]
**Model Type**: [CNN / RNN / etc.]
**Framework**: [PyTorch / TensorFlow / etc.]

## Intended Use

**Primary Use**: [What does it do?]
**Patient Population**: [Age, conditions, settings]
**Intended Users**: [Cardiologists, technicians, etc.]

## Training Data

**Data Sources**:
- [Source 1]: N examples
- [Source 2]: N examples

**Data Characteristics**:
- Demographics: [Age mean/range, gender %, etc.]
- Size: [Total N examples]
- Quality: [Preprocessing steps, QA flags]

## Model Performance

**Test Set Performance**:

| Metric | Value | 95% CI |
|--------|-------|--------|
| Sensitivity | [X] | [Y-Z] |
| Specificity | [X] | [Y-Z] |
| AUC | [X] | [Y-Z] |

**Sub-Population Performance**:
[Table by age, gender, comorbidity, etc.]

## Limitations

- [Limitation 1]
- [Limitation 2]
- [Limitation 3]

## References

- [Paper 1]
- [Dataset citation]
```

---

## Tips for FDA Model Cards

### 1. Be Specific About Data

FDA will ask: "How do you know your data is representative?"

Answer: Document data sources, size, demographics, preprocessing, limitations.

### 2. Show Sub-Population Performance

FDA cares about equity. Show:
- Age breakdowns (young vs. old)
- Gender if relevant
- Relevant clinical factors (comorbidities, disease stage)

### 3. Acknowledge Limitations

Models have limitations. FDA respects honesty. Examples:

- "Not validated in pediatrics"
- "Unknown performance on [rare condition]"
- "May fail on corrupted signals"

Showing you understand limitations builds trust.

### 4. Confidence Intervals Matter

Don't just say "Sensitivity 0.94". Say "Sensitivity 0.94 (95% CI: 0.92-0.96)".

CI shows statistical precision and robustness.

### 5. Compare to Reference Standard

If you can, test your model vs. human expert on same data.

Example: "Sensitivity 0.94 vs. cardiologist 0.90"

---

## When to Update a Model Card

Update model card when:

- **New version deployed**: Document new performance
- **Retraining completed**: Update training data and performance
- **New limitations discovered**: Add to known limitations
- **Monitoring reveals drift**: Document performance change
- **FDA requests clarification**: Update for clarity

Keep model card in version control with your model.

---

## Resources

- [Mitchell et al. 2019: Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) - Original paper
- [Google Model Cards Toolkit](https://github.com/google/model-card-toolkit) - Open-source implementation
- [FDA AI/ML Guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-machine-learning-practice-medical-device-development)
- [Fairness and Bias in ML](https://arxiv.org/abs/1810.03993) - Addressing disparities

---

## Next Steps

1. Write your model card using the template above
2. Document training data in detail
3. Show performance by sub-population
4. Acknowledge limitations honestly
5. Include with your 510(k) or PCCP submission
6. Update regularly as your model evolves

Have questions? Open a [GitHub issue](https://github.com/lal-jaouni/fda-samd-toolkit/issues).
