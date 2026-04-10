# What is a PCCP? Understanding Predetermined Change Control Plans

A **PCCP (Predetermined Change Control Plan)** is your roadmap for how you'll modify your AI/ML device after FDA approval, without needing new approval each time.

Think of it this way: You submit a cleared AI algorithm to FDA. Six months later, you have new training data. Should you retrain? FDA says yes, but only if you follow a plan that you committed to upfront. That plan is the PCCP.

This guide explains what PCCPs are, why they matter, and what goes into one.

---

## The Problem PCCPs Solve

Imagine you have a cleared AI system for heart arrhythmia detection. Over time, you encounter new variations:

- New ECG devices produce slightly different signals. You need to update preprocessing.
- New patient populations (different hospitals, different demographics). Model performance drifts.
- You collect 50,000 new ECG examples. You want to retrain to improve performance.

Without a PCCP, each change requires a new FDA submission (510(k) or amendment). That takes weeks to months, during which you can't update your device.

**With a PCCP**, you document upfront:

- "We will retrain monthly on new data" (allowed change)
- "We monitor model calibration. If it drops below 0.85, we retrain" (automated trigger)
- "We never change the intended use or decision thresholds without FDA approval" (not allowed)

FDA approves your PCCP once. Then you execute it independently, documenting what you did for future audits.

---

## When You Need a PCCP

**You need a PCCP if**:

- Your device will be modified after approval (retraining, parameter updates, new data)
- Your algorithm will learn or adapt post-market
- You plan to monitor and update based on real-world performance
- You want the flexibility to make changes without submitting to FDA each time

**You might not need a PCCP if**:

- Your algorithm is frozen (never changes, locked weights)
- You never plan to retrain or update
- All changes require FDA pre-approval (slow, but sometimes chosen for high-risk devices)

Most AI/ML devices need a PCCP because ML systems naturally benefit from retraining on new data.

---

## Three Required Sections of a PCCP

FDA's December 2024 PCCP Guidance requires three core sections:

### 1. Performance Monitoring Plan

**Question**: How do you know your model is still working?

**What goes here**:

- **Metrics you monitor**: Sensitivity, specificity, calibration, AUC on recent data
- **Data sources**: Which real-world patients/data do you use to monitor?
- **Monitoring frequency**: Daily? Weekly? Monthly?
- **Reporting**: Who sees the results and how often?

**Example**:

```
Performance Monitoring Plan

Metric: Sensitivity for atrial fibrillation detection
Target: >= 0.94 (baseline from clinical validation)
Current Performance: 0.945 (95% CI: 0.932-0.958)

Monitoring Approach:
- Daily: Run inference on 500 new ECGs
- Weekly: Calculate sensitivity on rolling 1-week window
- Monthly: Generate performance report, flag if <0.90

Data Source: Real patient ECGs from all connected hospitals
Population: All patients using the system (no exclusions)

Trigger: If sensitivity drops below 0.90 for 2 consecutive weeks, escalate to model retraining
```

### 2. Modification Categories

**Question**: What kinds of changes will you make to your model?

**What goes here**:

For each type of change you might make (retraining, data drift handling, threshold updates), you document:

- **Category name**: Retraining, Hyperparameter Tuning, Input Data Format, etc.
- **Description**: What specifically changes?
- **Frequency**: How often? (daily, monthly, as-needed)
- **Impact on safety/performance**: Does this change patient outcomes?
- **Validation approach**: How do you verify the change is safe?

**Example**:

```
Modification Category: Monthly Retraining

Description:
Retrain the model weekly on accumulated ECG data from all hospitals,
using the same architecture and hyperparameters, to improve sensitivity
on emerging ECG patterns.

Frequency: Weekly (automatic)

Impact: Potential to improve sensitivity (good) but also risk of
degraded performance if training data is biased (bad).

Validation:
- Before deployment: Test on held-out validation set (5000 ECGs from
  previous month), confirm sensitivity stays >= 0.90
- If validation fails, do not deploy, escalate to data science team
- After deployment: Monitor performance daily as above
```

### 3. Retraining and Monitoring Procedures

**Question**: What triggers a model update? What happens when it fails?

**What goes here**:

- **Retraining triggers**: Conditions that cause you to retrain (scheduled, threshold breach, etc.)
- **Data selection**: What training data do you use?
- **Validation before deployment**: How do you test the new model?
- **Failure thresholds**: What metrics trigger rollback?
- **Rollback procedure**: If new model fails, how do you revert?
- **Documentation**: What do you record for FDA audits?

**Example**:

```
Retraining and Monitoring Procedures

Trigger 1 (Scheduled): Every Monday, check if >10,000 new ECGs collected
- If yes, initiate retraining; if no, continue monitoring

Trigger 2 (Performance): If sensitivity drops below 0.90 for 2 consecutive weeks
- Immediately flag for manual review
- Stop automated retraining, investigate root cause
- If due to data drift: Retrain on recent data
- If due to system error: Revert to previous model

Training Data:
- Source: All ECGs collected since last retraining
- Size: Typically 50,000-100,000 per cycle
- Exclusions: Manually flagged erroneous ECGs (< 1%)

Validation Before Deployment:
- Test new model on held-out set: 5,000 most recent ECGs
- Check metrics: sensitivity >= 0.90, specificity >= 0.92
- Compare to previous model: No degradation on any sub-population
- Approval: If all checks pass, deploy automatically

Failure Thresholds:
- Sensitivity < 0.85: Critical failure, revert immediately
- Sensitivity 0.85-0.90: Warning, investigate before next retraining
- Specificity < 0.88: Critical failure, revert immediately
- Any sub-population drops >5% relative: Flag for review

Rollback Procedure:
- New model fails validation: Auto-rollback to previous version (< 5 sec)
- Alert data science team via Slack
- Prevent new deployment until issue investigated

Documentation:
- Log all retraining events (date, size of training set, performance delta)
- Store model artifacts (version, hyperparameters, training data hash)
- Maintain audit trail for FDA inspection
```

---

## PCCP Structure: What FDA Expects

The full PCCP document should have these sections (in order):

1. **Device and Intended Use**: What is the device? Who uses it? What condition does it diagnose or monitor?

2. **Algorithm Overview**: How does the algorithm work? What's the architecture? What data does it need as input?

3. **Training Data Characterization**: Where did the original training data come from? Size, demographics, sources, preprocessing, any limitations.

4. **Initial Performance Documentation**: What were the sensitivity, specificity, AUC on the original validation set? Any performance gaps by sub-population?

5. **Change Control Overview**: Types of changes you'll make post-market.

6. **Performance Monitoring Plan**: How will you monitor the device post-market?

7. **Modification Categories**: Specific types of changes (retraining, input format changes, etc.) and their procedures.

8. **Retraining and Modification Procedures**: Detailed procedures for when and how you retrain.

9. **Failure Modes and Mitigation**: What can go wrong? How will you detect it? How will you fix it?

10. **Documentation and Traceability**: What will you document and keep for FDA?

FDA's 25-page guidance details each section. The toolkit generates a draft from your YAML config.

---

## Common Pitfalls (And How to Avoid Them)

### Pitfall 1: Vague Change Control

**Bad**: "We retrain whenever we think it helps"

**Good**: "We retrain weekly if >10,000 new labeled examples are available, or immediately if sensitivity drops below 0.90 for 2 consecutive weeks"

**Why**: FDA wants to know exactly when you change your device. Vagueness suggests you're making changes ad-hoc without oversight.

### Pitfall 2: No Failure Thresholds

**Bad**: "We monitor sensitivity and fix it if there are problems"

**Good**: "We monitor sensitivity daily. Critical failure threshold: <0.85. Warning threshold: <0.90. If critical threshold breached, we immediately revert to previous model and investigate within 24 hours."

**Why**: FDA wants to know you've thought about failure modes and have a response plan.

### Pitfall 3: No Sub-Population Analysis

**Bad**: "Average sensitivity is 0.93"

**Good**: "Overall sensitivity 0.93 (95% CI 0.91-0.95). Sub-populations: age 18-45: 0.95, age 65+: 0.91, female: 0.92, male: 0.94. Performance variation within acceptable limits."

**Why**: FDA is concerned about disparities. Show you've analyzed whether the model works for everyone.

### Pitfall 4: Retraining on Biased Data

**Bad**: "We retrain on all new data we collect"

**Good**: "We retrain on all new data, with validation that the distribution matches original training set. If we detect demographic shift, we stop automated retraining and investigate."

**Why**: Retraining on biased post-market data can degrade performance. You need safeguards.

### Pitfall 5: No Predicate Device Comparison

**Bad**: "Our model is good" (for 510(k) submissions)

**Good**: "Our model has sensitivity 0.94 vs. predicate device 0.91. Specificity 0.92 vs. predicate 0.90. Equivalent or superior on all metrics."

**Why**: For 510(k), you must compare to a cleared predicate. Show you're at least as good.

---

## Real Example: ECG Arrhythmia Detector

Here's a condensed real PCCP excerpt for an AI ECG system:

```
Device: AI Cardiac Rhythm Analysis System (v1.0)

Intended Use: Automated detection of atrial fibrillation, ventricular
ectopy, and bradycardia from 12-lead ECG in patients aged 18-85
presenting to hospitals and ambulatory settings.

Algorithm: CNN-based classifier on raw ECG waveforms
- Architecture: ResNet-50, pretrained on ImageNet, fine-tuned
- Input: 12-lead ECG at 500 Hz, 10 seconds (5000 samples per lead)
- Output: Binary classification (arrhythmia present/absent) + confidence

Training Data: 150,000 ECGs
- MIMIC-III: 80,000 (publicly available)
- Partner Hospital A: 50,000 (proprietary, 2020-2022)
- Partner Hospital B: 20,000 (proprietary, 2021-2023)
- Demographics: 55% male, mean age 62 (range 18-95)
- Conditions: 30% known AFib, 40% normal sinus, 30% other arrhythmias

Initial Performance:
- Overall Sensitivity: 0.94 (95% CI: 0.92-0.96)
- Overall Specificity: 0.91 (95% CI: 0.89-0.93)
- By age: Age 18-45: Sen 0.96, Spec 0.93
         Age 65+: Sen 0.92, Spec 0.90
- By sex: Female: Sen 0.93, Spec 0.91
         Male: Sen 0.95, Spec 0.91

Performance Monitoring:
- Daily: Run on 300 new ECGs, track sensitivity, specificity, calibration
- Weekly: Generate performance report, flag if sensitivity <0.90
- Monthly: Full population analysis, check for demographic drift
- Alert: If sensitivity <0.90, page on-call data scientist

Change Category 1: Weekly Retraining
- Frequency: Weekly (Monday 2am)
- Trigger: If >10,000 new ECGs collected
- Validation: Test on held-out 5,000 ECGs, confirm Sen >= 0.90, Spec >= 0.88
- Rollback: If validation fails, use previous model
- Documentation: Log training date, dataset size, performance delta

Change Category 2: Preprocessing Updates
- Frequency: As-needed
- Trigger: New ECG hardware causes data drift (detected in monitoring)
- Impact: May affect sensitivity/specificity
- Validation: Full clinical validation study (FDA consult) before deployment
- Documentation: Update preprocessing SOP, notify FDA

Failure Thresholds:
- Sensitivity < 0.85: CRITICAL, revert immediately, page team
- Sensitivity 0.85-0.90: WARNING, investigate before next retraining
- Specificity < 0.88: CRITICAL, revert immediately
- Any sub-population drops >10% relative: WARNING, investigate

Not Allowed (Requires New FDA Approval):
- Change to 5-lead ECG (changes intended use)
- Change decision threshold to 0.7 (changes clinical performance)
- Add new arrhythmia type not in original intended use
- Use training data outside hospital ECG domain (e.g., wearable ECGs)
```

This is the level of detail FDA expects in a PCCP.

---

## How the Toolkit Helps

The toolkit generates PCCP scaffolding from a YAML config, covering:

- Boilerplate and structure (gets most of the document written)
- FDA-required sections (performance monitoring, modification categories, procedures)
- Placeholder integration (you fill in device-specific details)
- Validation checking (ensures completeness)

What the toolkit doesn't do:

- Doesn't run your clinical validation study
- Doesn't analyze your sub-population performance
- Doesn't write your failure mode analysis (you do that based on your specific device)
- Doesn't replace regulatory expert review

---

## Next Steps

1. **Learn FDA basics**: See [FDA SaMD Overview](fda-overview.md)
2. **Build your PCCP**: See [PCCP Generator Guide](../guides/pccp-generator.md)
3. **Review FDA guidance**: [PCCP Final Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
4. **Talk to FDA**: Pre-submission meeting. Ask: "Is my proposed PCCP acceptable?" FDA will give feedback.

---

## Key Takeaway

A PCCP is your promise to FDA: "Here's exactly how we'll modify our device, monitor it, and keep it safe." If you follow your PCCP, you can make changes without new submissions. If you deviate, you need FDA pre-approval.

Written well, a PCCP gives you operational flexibility and regulatory predictability.
