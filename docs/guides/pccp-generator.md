# PCCP Generator: From Config to Regulatory Document

The PCCP Generator takes a YAML configuration file and produces a complete, FDA-aligned Predetermined Change Control Plan document. This guide walks you through the process.

---

## Overview

The generator works in three steps:

1. **Write YAML config** with your device details, algorithm info, and change procedures
2. **Run the generator** to produce Markdown document
3. **Validate and customize** the output for your specific regulatory strategy

---

## Step 1: Write Your Configuration File

Create a YAML file (e.g., `my_device.yaml`) with your device information. Here's the full schema:

```yaml
# Device Information
device_name: "Device Name"
device_class: "Class I|Class II|Class III"
intended_use: |
  Clear statement of what the device diagnoses, treats, or monitors.
  Include patient population, clinical setting, and indications.

# Model Information
model_info:
  architecture: "Description of model architecture"
  training_approach: "How was the model trained?"
  training_data_size: 100000
  training_data_sources:
    - "Source 1 (description)"
    - "Source 2 (description)"
  
  # Performance metrics (required)
  performance:
    - metric: "sensitivity"
      value: 0.95
      confidence_interval: "0.93-0.97"
      sub_populations:
        - "age 18-45": 0.96
        - "age 65+": 0.94
        - "female": 0.95
        - "male": 0.95
    - metric: "specificity"
      value: 0.93
      confidence_interval: "0.91-0.95"

# Change Control Plan
change_control:
  # Define each type of change you'll make post-market
  - category: "retraining"
    description: "Periodic retraining on new ECG data"
    frequency: "weekly"
    impact: "May improve sensitivity on emerging patterns"
    validation: "Test on held-out validation set"
    
  - category: "input_data"
    description: "Support for new ECG hardware formats"
    frequency: "as_needed"
    impact: "Preprocessing changes to handle new signals"
    validation: "Clinical validation study (FDA consult)"

# Performance Monitoring Plan
monitoring:
  metrics:
    - name: "sensitivity"
      target: 0.90
      frequency: "daily"
    - name: "specificity"
      target: 0.88
      frequency: "daily"
    - name: "calibration"
      target: 0.85
      frequency: "weekly"
  
  # Failure thresholds
  failure_thresholds:
    - metric: "sensitivity"
      critical: 0.85
      warning: 0.90
    - metric: "specificity"
      critical: 0.85
      warning: 0.88
  
  # What triggers intervention
  triggers:
    - "Metric below warning threshold for 2 consecutive monitoring periods"
    - "Unplanned model degradation detected by automated tests"
    - "New ECG hardware introduces data distribution shift"

# Retraining Procedures
retraining:
  frequency: "weekly"
  data_sources: "Real-world ECGs from all connected hospitals"
  validation_approach: |
    Test new model on held-out validation set (5000 most recent ECGs).
    Confirm sensitivity >= 0.90, specificity >= 0.88 on all sub-populations.
  rollback_procedure: |
    If validation fails, do not deploy new model. Revert to previous version.
    Alert on-call data scientist for investigation.
  documentation: |
    Log all retraining events (date, dataset size, performance metrics).
    Store model artifacts and training data provenance for audit.

# Changes NOT Allowed (require new FDA approval)
not_allowed:
  - "Change intended use (e.g., add new arrhythmia types)"
  - "Change decision thresholds that alter clinical performance"
  - "Retrain on data outside hospital ECG domain"
  - "Change to a different device class without pre-approval"

---

## Minimal Example

Don't have all the details? Start with a minimal config:

```yaml
device_name: "ECG Arrhythmia Detector"
device_class: "Class II"
intended_use: |
  Automated detection of atrial fibrillation from 12-lead ECG
  in adult patients (18-85) in hospital and clinic settings.

model_info:
  architecture: "ResNet-50 CNN on ECG signals"
  training_data_size: 150000
  training_data_sources:
    - "MIMIC-III"
    - "Partner Hospital A (2021-2023)"
  performance:
    - metric: "sensitivity"
      value: 0.94

change_control:
  - category: "retraining"
    frequency: "weekly"
    description: "Retrain on new ECG data"

monitoring:
  metrics:
    - name: "sensitivity"
      target: 0.90
      frequency: "daily"
```

The generator will fill in boilerplate and mark missing sections with `[PLACEHOLDER]` for you to complete.

---

## Step 2: Run the Generator

### Basic Usage

```bash
fda-samd pccp generate --config my_device.yaml --output PCCP.md
```

This creates `PCCP.md` with the full PCCP structure.

### With PDF Output

```bash
fda-samd pccp generate --config my_device.yaml --output PCCP.md --pdf
```

Also generates `PCCP.pdf` (requires wkhtmltopdf or similar).

### With Custom Template

```bash
fda-samd pccp generate \
  --config my_device.yaml \
  --output PCCP.md \
  --template /path/to/custom_template.j2
```

See [Contributing](../contributing.md) for how to create custom templates.

---

## Step 3: Validate the Output

After generating, validate for completeness:

```bash
fda-samd pccp validate --file PCCP.md
```

Output example:

```
PCCP Validation Report
======================
File: PCCP.md
Generated: 2025-04-10

Overall Completeness: 92%

Critical Issues (Must Fix):
  (None)

Warnings (Should Address):
  ⚠ Performance Metrics: Missing specificity for sub-population 'age 65+'
    Add: specificity breakdown by age group
  
  ⚠ Retraining Procedures: Rollback time not specified
    Add: Time to rollback from failed retraining (e.g., "< 5 minutes")

Sections Status:
  [✓] Device and Intended Use (100%)
  [✓] Algorithm Overview (100%)
  [✓] Training Data Characterization (100%)
  [✓] Initial Performance Documentation (100%)
  [✓] Performance Monitoring Plan (95%)
  [✓] Change Control Categories (100%)
  [✓] Retraining Procedures (90%)
  [✓] Failure Modes and Thresholds (100%)
  [✓] Documentation and Traceability (100%)
  [ ] Sub-Population Performance Analysis (50%) [PLACEHOLDER]

Recommendations:
  - Add more detail to failure mode analysis (currently generic)
  - Consider adding data drift detection procedure
  - Document how you'll handle edge cases (e.g., corrupted ECGs)

Estimated FDA Review Time: 2-4 weeks (assuming no major gaps)
```

---

## Step 4: Customize and Complete

The generated document has three types of content:

### 1. Filled Sections (From Your YAML)

These are complete and specific to your device. Example:

```markdown
## Device Classification

Device Name: ECG Arrhythmia Detector
Device Class: Class II
Intended Use: Automated detection of atrial fibrillation from 12-lead ECG
```

### 2. Boilerplate (Generic, FDA-Aligned)

These provide structure and context. Example:

```markdown
## Performance Monitoring Overview

Continuous monitoring of model performance post-deployment is critical
to ensure the algorithm continues to function as intended. This section
outlines the specific metrics, frequency, and failure thresholds.
```

Feel free to customize to your specific approach.

### 3. Placeholders (You Must Complete)

These are marked `[PLACEHOLDER]` or `[TODO]`. Example:

```markdown
## Sub-Population Analysis

The model's performance across key sub-populations is:

[PLACEHOLDER: Add your sub-population performance breakdown here.
Include at least age, sex, and any relevant clinical factors.
Format: Sub-population name, metric (sensitivity/specificity), value, confidence interval]
```

Replace each placeholder with your device-specific details.

---

## Common Customizations

### Adding Sub-Population Performance

Replace:

```markdown
[PLACEHOLDER: Sub-population performance breakdown]
```

With:

```markdown
### Sub-Population Performance

The model was validated on key clinical sub-populations:

| Sub-Population | Sensitivity | Specificity | N |
|---|---|---|---|
| Age 18-45 | 0.96 | 0.94 | 15,000 |
| Age 65+ | 0.92 | 0.91 | 20,000 |
| Female | 0.93 | 0.92 | 18,000 |
| Male | 0.95 | 0.93 | 17,000 |
| With hypertension | 0.94 | 0.91 | 22,000 |
| Without hypertension | 0.94 | 0.94 | 13,000 |

No significant disparities detected. Performance consistent across demographics.
```

### Defining Failure Modes

Replace:

```markdown
[PLACEHOLDER: List failure modes and mitigation]
```

With:

```markdown
### Failure Modes

| Failure Mode | Detection | Mitigation |
|---|---|---|
| Data drift (new ECG hardware) | Weekly distribution comparison | Retrain with new preprocessing |
| Model degradation | Daily sensitivity/specificity tracking | Revert to previous model |
| Incomplete ECG data | Input validation during inference | Reject, request retransmission |
| Extreme patient demographics | Age/sex distribution monitoring | Investigate sub-population performance |
```

### Specifying Monitoring Infrastructure

Replace:

```markdown
[PLACEHOLDER: Describe monitoring infrastructure]
```

With:

```markdown
### Monitoring Infrastructure

Performance metrics are collected via:

- **Data Collection**: Real-time inference logging (every ECG processed)
- **Storage**: Cloud database (AWS RDS) with daily snapshots
- **Analysis**: Python pipeline runs daily at 2am UTC
- **Alerting**: Slack notifications if any metric breaches warning threshold
- **Reporting**: Weekly email report to quality team, monthly board report
- **Audit Trail**: All decisions logged with timestamps and rationale
```

---

## Validation Strategy

The validator checks for:

1. **Completeness**: Do all required sections have content (not placeholders)?
2. **Consistency**: Does monitoring match change control? Are thresholds reasonable?
3. **FDA Alignment**: Does the document follow FDA guidance structure?
4. **Specificity**: Are claims specific to your device (not generic)?

### Completeness Scoring

- 100%: All sections complete, no placeholders
- 80-99%: Minor placeholders remain, mostly ready
- 60-79%: Significant gaps, still in draft phase
- <60%: Major work needed before FDA review

---

## Example: Full PCCP Config

Here's a more complete real-world example:

```yaml
device_name: "Cardiac Rhythm Monitor AI v2.0"
device_class: "Class II"

intended_use: |
  Automated detection of clinically significant cardiac arrhythmias
  (atrial fibrillation, ventricular ectopy, bradycardia) from continuous
  12-lead ECG waveforms in adult patients (age 18-85) hospitalized in
  intensive care or step-down settings.

model_info:
  architecture: |
    ResNet-50 convolutional neural network. Pretrained on ImageNet,
    fine-tuned on 12-lead ECG data. Input: 10-second window at 500 Hz
    (5000 samples per lead). Output: Multi-class classification (normal
    sinus, AFib, V-ectopy, bradycardia).
  
  training_approach: |
    Supervised learning with cross-entropy loss. Train/val/test split 60/20/20.
    Data augmentation: noise injection, time warping. Hyperparameters optimized
    via grid search on validation set.
  
  training_data_size: 150000
  
  training_data_sources:
    - "MIMIC-III: 80,000 ICU ECGs, openly available"
    - "Partner Hospital A: 50,000 ECGs (2020-2022), proprietary"
    - "Partner Hospital B: 20,000 ECGs (2022-2023), proprietary"
  
  performance:
    - metric: "sensitivity"
      value: 0.94
      confidence_interval: "0.92-0.96"
      sub_populations:
        - "age 18-45": 0.96
        - "age 65+": 0.92
        - "female": 0.93
        - "male": 0.95
        - "hypertension": 0.93
        - "no hypertension": 0.95
    
    - metric: "specificity"
      value: 0.91
      confidence_interval: "0.89-0.93"
      sub_populations:
        - "age 18-45": 0.93
        - "age 65+": 0.90
        - "female": 0.92
        - "male": 0.91

change_control:
  - category: "retraining"
    description: |
      Monthly retraining on accumulated ECG data from all hospitals
      using same architecture and hyperparameters. Improves sensitivity
      on emerging arrhythmia patterns.
    frequency: "monthly"
    impact: "Potential performance improvement, but risk if training data biased"
    validation: "Test on held-out validation set, require sensitivity >= 0.90"
  
  - category: "input_preprocessing"
    description: |
      Updates to ECG signal preprocessing (filtering, baseline wander removal)
      to support new ECG hardware models.
    frequency: "as_needed"
    impact: "Changes input features, may affect sensitivity/specificity"
    validation: "Requires clinical validation study and FDA pre-approval"
  
  - category: "threshold_adjustment"
    description: |
      Fine-tuning decision thresholds (confidence cutoffs for arrhythmia detection)
      to optimize specificity vs. sensitivity based on clinical feedback.
    frequency: "semi-annually"
    impact: "Direct impact on clinical performance and false alarm rate"
    validation: "Internal validation study, recommend FDA pre-approval"

monitoring:
  metrics:
    - name: "sensitivity"
      target: 0.90
      frequency: "daily"
      calculation: "Tp / (Tp + Fn) on latest 1000 ECGs"
    
    - name: "specificity"
      target: 0.88
      frequency: "daily"
      calculation: "Tn / (Tn + Fp) on latest 1000 ECGs"
    
    - name: "calibration"
      target: 0.85
      frequency: "weekly"
      calculation: "Expected Calibration Error on rolling 1-week window"
  
  failure_thresholds:
    - metric: "sensitivity"
      critical: 0.85
      warning: 0.90
      action_critical: "Immediate rollback, page on-call engineer"
      action_warning: "Investigate root cause, consider rollback"
    
    - metric: "specificity"
      critical: 0.85
      warning: 0.88
      action_critical: "Immediate rollback, notify clinical team of false alarms"
      action_warning: "Investigate, monitor next 48 hours"
  
  triggers:
    - "Any metric below critical threshold triggers immediate alert"
    - "Any metric below warning threshold for 2 consecutive days triggers investigation"
    - "Data distribution shift detected (KL divergence > 0.1 vs. training) triggers review"
    - "Sub-population performance drops >5% relative triggers analysis"

retraining:
  frequency: "Monthly (first Monday of each month, 2am UTC)"
  data_selection: |
    All ECGs collected since last retraining, excluding:
    - ECGs with manual QA flags (< 1%)
    - Incomplete 10-second windows (< 0.5%)
    - Duplicate/test ECGs (< 0.1%)
  
  data_sources: "Real-world ECGs from all connected hospitals"
  
  validation_approach: |
    Before deployment, test new model on held-out validation set:
    - 5,000 most recent ECGs not in training set
    - Require sensitivity >= 0.90, specificity >= 0.88
    - Check all sub-populations: no group drops >5% relative
    - Compare AUC vs. previous model: must be equal or better
    - If all checks pass: auto-deploy new model
    - If any check fails: do not deploy, investigate
  
  rollback_procedure: |
    If new model fails validation or shows failure threshold breach post-deployment:
    - Automatic revert to previous model (< 5 second downtime)
    - Alert on-call data scientist and clinical team
    - Root cause analysis required before next retraining attempt
    - Log all relevant data for FDA audit trail
  
  documentation: |
    Log all retraining activities:
    - Date/time of retraining
    - Training dataset size and composition
    - Model artifacts (weights, hyperparameters)
    - Performance metrics (sensitivity, specificity, AUC)
    - Validation results (pass/fail, any issues)
    - Deployment status (deployed successfully, rolled back, pending, etc.)
    - Any incidents or anomalies

not_allowed:
  - "Extend intended use to outpatient/home settings without pre-approval"
  - "Add new arrhythmia types (bradycardia, ectopy) without FDA notification"
  - "Change from 12-lead to 6-lead or single-lead ECG without revalidation"
  - "Retrain on ECG data from non-hospital sources (wearables, consumer devices)"
  - "Change decision threshold without clinical validation"
  - "Switch to different model architecture (RNN, transformer) without FDA submission"
```

---

## Tips for Success

### 1. Be Specific, Not Generic

Bad: "We monitor performance and fix issues as needed"

Good: "We monitor sensitivity daily on a rolling 1000-ECG window. Critical threshold <0.85 triggers automatic rollback."

### 2. Document Your Infrastructure

FDA wants to know: Do you actually have the monitoring systems you describe?

Include: Database names, alert channels, monitoring frequency, who gets notified.

### 3. Define Clear Thresholds

FDA wants decision rules, not judgment calls.

Include: Exact numbers (sensitivity >= 0.90), failure modes (sensitivity < 0.85), and automatic responses.

### 4. Plan for Real-World Complexity

Good PCCPs acknowledge:

- Data may be noisier in production
- Sub-populations may have different performance
- Hardware varies across hospitals
- Clinical practices change over time

### 5. Show Sub-Population Thinking

FDA cares about equity. Show you've thought about:

- Age ranges
- Gender
- Race/ethnicity (if applicable)
- Comorbidities
- Clinical setting (ICU vs. floor)

---

## Next Steps

1. **Write your config**: Use the schema and examples above
2. **Generate your PCCP**: `fda-samd pccp generate --config my_device.yaml --output PCCP.md`
3. **Validate**: `fda-samd pccp validate --file PCCP.md`
4. **Customize**: Replace placeholders with device-specific details
5. **Review with experts**: Regulatory affairs, data science, and clinical teams
6. **Submit to FDA**: Via your 510(k), De Novo, or pre-submission meeting

---

## Resources

- [FDA PCCP Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [What is a PCCP?](../concepts/pccp-explained.md)
- [Contributing Templates](../contributing.md)
- [GitHub Issues](https://github.com/lal-jaouni/fda-samd-toolkit/issues) for questions
