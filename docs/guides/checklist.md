# Readiness Checklist: Pre-Submission Gap Analysis

Before submitting to FDA, use this checklist to ensure you have all required documentation and haven't missed critical sections.

---

## Running the Readiness Checker

The toolkit includes an automated readiness checker:

```bash
fda-samd readiness-check \
  --pccp PCCP.md \
  --model-card model_card.md \
  --510k 510k_submission.md \
  --output readiness_report.html
```

This generates a detailed report showing:
- Completeness score (0-100%)
- Missing sections
- Recommended fixes
- Estimated FDA review time

---

## Pre-Submission Checklist

Use this checklist manually before automated review:

### Section 1: Device Fundamentals

- [ ] Device name clearly defined
- [ ] Device classification (Class I/II/III) specified
- [ ] Regulatory pathway chosen (510(k)/De Novo/PMA)
- [ ] Intended use statement is specific and clear
- [ ] Patient population clearly described
- [ ] Clinical setting specified (hospital/outpatient/home)
- [ ] Limitations of intended use documented

**Gap**: If missing, contact FDA via pre-submission meeting to confirm pathway

### Section 2: Algorithm Documentation

- [ ] Algorithm type clearly stated (CNN/RNN/etc.)
- [ ] Architecture described (layers, hyperparameters)
- [ ] Training approach documented (loss function, optimization)
- [ ] Input data format specified (dimensions, sampling rate, units)
- [ ] Output format specified (probabilities, confidence scores, thresholds)
- [ ] Version control in place (model versioning system)

**Gap**: If missing, FDA will ask for clarification during review

### Section 3: Training Data

- [ ] Total dataset size documented (N examples)
- [ ] Data sources listed (hospitals, datasets, proprietary)
- [ ] Demographics of training data described
  - [ ] Age: range and mean
  - [ ] Gender distribution
  - [ ] Race/ethnicity (if applicable and available)
  - [ ] Disease prevalence
- [ ] Data preprocessing described (filtering, normalization)
- [ ] Data quality measures documented (exclusion criteria, QA flags)
- [ ] Data limitations acknowledged

**Gap**: FDA requires detailed data characterization. If vague, expect questions

### Section 4: Performance Documentation

- [ ] Overall sensitivity documented with 95% CI
- [ ] Overall specificity documented with 95% CI
- [ ] Additional metrics (AUC, PPV, NPV) if relevant
- [ ] Performance by age group (sub-population analysis)
- [ ] Performance by gender (sub-population analysis)
- [ ] Performance by relevant comorbidity
- [ ] Performance by clinical setting (if multiple)
- [ ] Confidence intervals include all metrics

**Gap**: Sub-population analysis is critical. FDA will ask if missing

### Section 5: Predicate Device (510(k) Only)

- [ ] Predicate device identified with K-number
- [ ] Predicate's intended use clearly stated
- [ ] Comparison to predicate: intended use (same or narrower?)
- [ ] Comparison to predicate: technology (similar approach?)
- [ ] Comparison to predicate: performance (equivalent or better?)
- [ ] Head-to-head data if available (tested both on same dataset)
- [ ] No new safety concerns identified

**Gap**: Wrong predicate = wrong pathway. Confirm with FDA early

### Section 6: Clinical Validation

- [ ] Validation study protocol written
- [ ] Study type justified (retrospective/prospective/RCT)
- [ ] Sample size calculation shown
- [ ] Enrollment criteria defined
- [ ] Reference standard (ground truth) defined
- [ ] Results: sensitivity, specificity with 95% CIs
- [ ] Sub-population results presented
- [ ] Baseline characteristics of study population documented
- [ ] Comparison to reference standard (cardiologist, existing device, etc.)

**Gap**: Without clinical validation data, FDA may not clear device. Plan study early

### Section 7: PCCP (Post-Market Change Control)

- [ ] PCCP document generated
- [ ] Device classification and intended use in PCCP
- [ ] Training data characterization in PCCP
- [ ] Initial performance in PCCP
- [ ] Change control categories defined (retraining, preprocessing, etc.)
- [ ] Performance monitoring plan detailed
- [ ] Monitoring metrics and thresholds specified
- [ ] Retraining frequency and procedures defined
- [ ] Failure thresholds and rollback procedures specified
- [ ] Not-allowed changes documented

**Gap**: PCCP is required if device will change post-market. Most AI/ML devices need one

### Section 8: Labeling and Instructions for Use

- [ ] Indications for Use statement
- [ ] Contraindications documented (who shouldn't use it)
- [ ] Warnings (what could go wrong?)
- [ ] Precautions (what to be careful about?)
- [ ] Instructions for use (step-by-step workflow)
- [ ] Symbols explained (if used on labeling)
- [ ] Language clear and non-technical for intended users

**Gap**: Labeling must be reviewed by legal/regulatory. Don't skip

### Section 9: Risk Analysis

- [ ] Failure modes identified (what can go wrong?)
- [ ] Root causes of failures documented
- [ ] Severity of each failure (catastrophic/major/minor)
- [ ] Likelihood of each failure (rare/occasional/frequent)
- [ ] Mitigation strategy for each failure (prevention or detection)
- [ ] Residual risk acceptable (risk benefit analysis)

**Gap**: FDA expects systematic risk management. Use FMEA (Failure Modes and Effects Analysis) format

### Section 10: Quality System and Manufacturing

- [ ] Software version control in place (Git, etc.)
- [ ] Testing procedures documented (unit, integration, system tests)
- [ ] Code review process defined
- [ ] Configuration management (how are changes controlled?)
- [ ] Data validation and integrity measures
- [ ] Encryption and security measures documented
- [ ] Backup and disaster recovery procedures
- [ ] Audit trail and logging capabilities

**Gap**: FDA expects professional software engineering practices. Can ask to see test results

### Section 11: Reference Standards and Comparisons

- [ ] Reference standard for your validation clearly defined
- [ ] Comparison to human expert (cardiologist) if applicable
- [ ] Comparison to predicate device (510(k)) if available
- [ ] Performance vs. other published algorithms cited
- [ ] Benchmark datasets used justified
- [ ] Literature review of similar devices included

**Gap**: Contextualizing your performance matters. Show how you compare

### Section 12: Edge Cases and Limitations

- [ ] Known limitations acknowledged (honest assessment)
- [ ] Edge cases identified (extreme values, rare conditions)
- [ ] Failure modes where model confidence is low documented
- [ ] Populations where model may not work identified (pediatrics, etc.)
- [ ] Conditions where device should not be used (contraindications)
- [ ] Recommendation for manual review documented

**Gap**: Acknowledged limitations increase FDA trust. Hiding them looks bad

### Section 13: Retraining and Modification Plan

- [ ] Retraining procedure defined (when, how often, on what data)
- [ ] Performance monitoring frequency (daily/weekly/monthly)
- [ ] Thresholds that trigger retraining defined
- [ ] Validation before deployment (test on holdout set)
- [ ] Rollback procedure if new model fails
- [ ] Documentation and versioning of all model changes
- [ ] Communication plan if failures detected

**Gap**: Integral to post-market management. FDA will audit this regularly

### Section 14: Data Drift and Concept Drift

- [ ] Plan for monitoring data distribution shift
- [ ] Thresholds for detecting meaningful drift
- [ ] Procedure for handling drift (retrain vs. investigate)
- [ ] Concept drift detection (new arrhythmias, new presentations)
- [ ] Plan if model performance degrades on new population

**Gap**: Shows sophisticated understanding. Especially important for long-lived devices

### Section 15: Sub-Population Equity

- [ ] Performance analyzed by age (young, middle, older)
- [ ] Performance analyzed by gender
- [ ] Performance analyzed by race/ethnicity if data available
- [ ] Performance in rare sub-groups documented
- [ ] Any disparities acknowledged and explained
- [ ] Mitigation for disparities documented

**Gap**: FDA increasingly cares about equity. Demonstrate thinking around disparities

### Section 16: Regulatory Justification

- [ ] Chosen pathway (510(k)/De Novo/PMA) justified
- [ ] Comparison to similar cleared devices
- [ ] Rationale for predicate selection
- [ ] Pre-submission meeting summary (if conducted)
- [ ] FDA feedback incorporated

**Gap**: Shows you engaged with FDA and have clear reasoning

---

## Completeness Scoring

Count checkmarks:

- 90-100: Ready for submission review
- 80-89: Minor gaps, can address during FDA Q&A
- 70-79: Significant gaps, address before submission
- <70: Major work needed, not ready for submission

**Example Scoring**:

```
Total items: 80
Checked items: 72
Completeness: 72/80 = 90%

Assessment: Ready for submission with minor gaps

Gaps to Address:
- [ ] Reference standard comparison (Section 11)
- [ ] Data drift monitoring plan (Section 14)

Action: Add reference standard analysis, then resubmit
```

---

## FDA Review Timeline Estimates

Based on completeness:

- **90-100%**: FDA review 2-4 weeks, 1-2 rounds of questions
- **80-89%**: FDA review 4-8 weeks, 2-3 rounds of questions
- **70-79%**: FDA review 8-12 weeks, 3+ rounds of questions
- **<70%**: Likely refuse-to-file (ask for more before reviewing)

Timeline is per submission round, not total time.

---

## Common Gaps and How to Fix Them

### Gap 1: Missing Sub-Population Analysis

**What FDA will ask**: "How does your device perform in elderly patients? Women? Other races?"

**Fix**:
1. Re-analyze test set by age, gender, comorbidity
2. Create performance tables (see Model Cards guide)
3. Discuss any disparities (expected? concerning?)
4. Document mitigation if performance varies significantly

**Effort**: 2-3 days of data analysis

### Gap 2: No Clear Predicate (510(k))

**What FDA will ask**: "Why is this device substantially equivalent to [predicate]?"

**Fix**:
1. Search FDA database for similar devices (accessdata.fda.gov)
2. Compare intended use, technology, performance
3. Run head-to-head testing if possible
4. Document substantial equivalence argument

**Effort**: 1 week research

### Gap 3: Insufficient Clinical Validation

**What FDA will ask**: "How many patients did you test on? What was the study design?"

**Fix**:
1. Design validation study (retrospective ok for 510(k))
2. Enroll minimum 1000-2000 patients
3. Calculate sensitivity/specificity with 95% CI
4. Analyze sub-populations

**Effort**: 2-6 months depending on study type

### Gap 4: No PCCP (Post-Market Changes)

**What FDA will ask**: "If you retrain this model, what's your procedure? What's the failure threshold?"

**Fix**:
1. Decide: will you retrain post-market?
2. If yes: write PCCP (use toolkit generator)
3. If no: document why (model locked, or all changes require new submission)
4. FDA will likely want PCCP for any ML device

**Effort**: 1 week with toolkit generator

### Gap 5: Vague Risk Analysis

**What FDA will ask**: "What could go wrong? How will you detect it? How will you fix it?"

**Fix**:
1. Systematic failure mode analysis (FMEA)
2. For each failure: detection method and mitigation
3. Example: If model sensitivity drops, daily monitoring detects this within 24 hours, triggers retraining

**Effort**: 1-2 weeks

---

## Regulatory Review Readiness Scorecard

Print this and review with your team:

| Criterion | Score (1-5) | Comments |
|-----------|-----------|----------|
| Device classification is clear | ___ | |
| Intended use is specific | ___ | |
| Algorithm is documented | ___ | |
| Training data is characterized | ___ | |
| Performance is measured | ___ | |
| Sub-populations are analyzed | ___ | |
| Clinical validation is done | ___ | |
| PCCP is written | ___ | |
| Risk analysis is complete | ___ | |
| Labeling is clear | ___ | |

**Scoring**: 1=Missing, 2=Partial, 3=Adequate, 4=Good, 5=Excellent

**Target**: Average score 4.0 before submission

---

## Pre-Submission Meeting with FDA

Before submitting, consider requesting a Type C pre-submission meeting:

**Why**: FDA tells you if you're on the right track before you invest time in full submission

**What to ask**:
- Is [device type] appropriate for 510(k)? Or do you want De Novo/PMA?
- Is [predicate device] suitable?
- What clinical validation study do you want to see?
- Are there any novel safety concerns you're worried about?
- Should we include a PCCP?

**How**: FDA form 1571 + executive summary (2-3 pages)

**Timeline**: Request 30 days before planned submission, get FDA response in ~30 days

**Cost**: Free

**Benefit**: Saves months if FDA says "you're on the wrong track"

---

## Submission Readiness Checklist

Final checklist before submitting:

- [ ] Spell-check all documents
- [ ] Verify all references (links work, citations correct)
- [ ] Consistent terminology (don't say "algorithm" and "model" for the same thing)
- [ ] All figures and tables referenced in text
- [ ] All abbreviations defined on first use
- [ ] Page numbers and table of contents correct
- [ ] No PHI (patient names, MRN, dates) in submission
- [ ] Legal/regulatory review complete
- [ ] Executive team (CEO, legal) aware of what's being submitted

**Tip**: FDA reviewers are human. Clear, organized submissions get faster reviews

---

## Post-Submission

After submitting 510(k):

- **FDA acknowledgment**: ~2 weeks (confirms they received it)
- **Substantial equivalence review**: 4-8 weeks typically
- **FDA questions**: Likely 1-2 rounds (expect ~5-10 questions)
- **Applicant response**: 30 days to answer each round of questions
- **Clearance or Not Substantially Equivalent (NSE)**: Final decision

If NSE: Can revise and resubmit, or switch to De Novo

---

## Resources

- [FDA 510(k) Guidance](https://www.fda.gov/medical-devices/premarket-submissions/510k-submissions)
- [FDA Pre-Submission Meetings](https://www.fda.gov/medical-devices/premarket-submission-types/pre-submission-meetings)
- [PCCP Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [Good ML Practice (2021)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-machine-learning-practice-medical-device-development)

---

## Next Steps

1. **Run the automated checker**: `fda-samd readiness-check --pccp PCCP.md`
2. **Review this manual checklist**: Mark gaps
3. **Address gaps**: Prioritize high-impact items
4. **Get regulatory review**: Internal (QA, Legal) and external (regulatory consultant)
5. **Consider pre-submission meeting**: If uncertain about pathway
6. **Submit to FDA**: When checklist is 90%+

Questions? Open a [GitHub issue](https://github.com/lal-jaouni/fda-samd-toolkit/issues) or consult a regulatory professional.
