# CardioGuard ECG-AI: Complete FDA Submission Example

This directory contains a fully worked example of a Class II software-as-a-medical-device (SaMD) submission to the FDA using the SaMD Toolkit. CardioGuard ECG-AI is a fictional but realistic 12-lead ECG arrhythmia detection system intended for use in primary care settings.

## Device Summary

**Device Name:** CardioGuard ECG-AI  
**Classification:** Class II  
**Regulatory Pathway:** 510(k) Traditional with Predetermined Change Control Plan (PCCP)  
**Predicate Device:** Anumana ECG-AI (K232488)  
**Intended Use:** Detection and characterization of atrial fibrillation, ventricular tachycardia, and 1st degree AV block in ambulatory adult patients (18+ years) presenting with signs/symptoms of arrhythmia.  

## Why This Example

The FDA's PCCP guidance (finalized December 2024) and AI/ML submission requirements present a steep learning curve for first-time submitters. This example demonstrates:

1. How to structure a complete submission across all toolkit components
2. Realistic (not perfect) performance metrics with sub-population analysis
3. Transparent discussion of known limitations and disparities
4. Coherent numbering and cross-referencing across regulatory documents
5. Actual reference to published FDA guidance and standards

All files use the same device, same training data, same clinical validation study, and same performance metrics to show how components fit together.

## Submission Timeline

```
Week 1-2:   Device characterization, intended use finalization
Week 3-4:   Risk analysis (ISO 14971), cybersecurity assessment
Week 5-6:   Predicate device comparison, substantial equivalence argument
Week 7-10:  Clinical validation study design and protocol
Week 11-14: Validation study execution (3-site retrospective data collection)
Week 15-16: Model card development, performance summary analysis
Week 17-18: PCCP development with retraining/drift monitoring strategy
Week 19-20: Labeling development, user training material
Week 21-22: 510(k) module assembly, internal review, Q&A preparation
Week 23:    Submission and FDA queue entry (expected clock start)
Week 23-27: FDA Pre-Submission Review (if requested)
Week 28-40: FDA substantive review (90 calendar day clock for Class II)
```

Expected time to clearance: 6-8 months from submission (assumes no major deficiencies).

## Artifacts in This Example

### Device Characterization
- **device_overview.md** - Clinical problem statement, technology, training data, intended use details
- **pccp.yaml** - Retraining and drift monitoring strategy (YAML config for PCCP generator)

### Regulatory Documentation
- **510k/01_indications_for_use.md** - IFU statement
- **510k/02_device_description.md** - Architecture, algorithm, I/O specifications
- **510k/03_substantial_equivalence.md** - Comparison to Anumana (K232488) predicate
- **510k/04_performance_summary.md** - Validation study results
- **510k/05_labeling.md** - Draft clinician labeling with interpretation guidance

### Clinical Validation
- **model_card.yaml** - FDA-extended model card with sub-population metrics (YAML config)
- **validation_plan.yaml** - Retrospective study protocol (3 sites, 1500 patients, adjudication)

### Safety & Compliance
- **risk_analysis.md** - ISO 14971 hazard analysis with mitigations
- **cybersecurity.md** - Threat model, software bill of materials (SBOM), vulnerability disclosure

### Submission Readiness
- **submission_checklist.yaml** - Artifact inventory (some complete, some partial) for readiness assessment

## How to Use This Example

### For regulatory professionals:
1. Read device_overview.md first to understand the clinical context
2. Review 510k/01-05 in sequence to see how a complete submission is structured
3. Cross-reference the model_card.yaml and validation_plan.yaml to see how clinical evidence feeds regulatory claims
4. Use risk_analysis.md and cybersecurity.md as templates for your own device

### For toolkit users:
1. Copy pccp.yaml and validation_plan.yaml to your own project
2. Customize device_info, device_name, and clinical parameters
3. Run: `fda-samd pccp generate --config pccp.yaml --output PCCP.md`
4. Run: `fda-samd validation-plan generate --config validation_plan.yaml` (future v0.3)
5. Use model_card.yaml as input to the model card generator (future v0.2)

### For startup founders:
1. Time the submission timeline (Week 1-23) against your product roadmap
2. Estimate regulatory costs: PCCP development (20 hrs), risk/cybersecurity analysis (30 hrs), clinical validation (200+ hrs)
3. Use the predicate device selection (Anumana K232488) as a model for your own predicate search
4. Note that quarterly retraining (PCCP drift threshold of 5% AUROC) is a realistic commitment to FDA

## FDA References

This example aligns with:

- **FDA PCCP Guidance (Dec 2024):** [Predetermined Change Control Plans for Machine Learning-Enabled Medical Devices](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- **FDA AI/ML Action Plan (2021):** [Artificial Intelligence and Machine Learning in Software as a Medical Device](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-software-medical-device)
- **ISO 14971 (2019):** Risk management for medical devices
- **IEC 62304 (2015):** Medical device software lifecycle processes
- **IMDRF SaMD Framework:** [Software as a Medical Device (SaMD): Key Definitions](https://www.imdrf.org/working-groups/software-medical-device-samd)

## Performance Summary

**Overall Model Performance (Internal Validation):**
- AUROC: 0.94 (95% CI: 0.92-0.95)
- Sensitivity (AFib): 0.91
- Specificity (AFib): 0.95
- Operating Point: sensitivity-optimized at 0.90 threshold

**Clinical Validation Study Results (Retrospective, 3 sites, n=1500):**
- Primary endpoint AUROC >= 0.90 with 95% CI lower bound >= 0.87: ACHIEVED (0.92, CI: 0.89-0.94)
- Sensitivity across all arrhythmias >= 0.85: ACHIEVED (0.88)
- Specificity >= 0.90: ACHIEVED (0.92)

**Sub-Population Performance:**
- By sex: M AUROC 0.94, F AUROC 0.93 (difference: 0.01, not clinically significant)
- By age: 18-40 AUROC 0.91, 41-65 AUROC 0.95, 66+ AUROC 0.94
- By race/ethnicity: White 0.94, Black 0.91, Hispanic 0.92, Asian 0.93
  - Note: 0.03 gap between White and Black populations identified; mitigation in progress (additional diverse training data, re-validation planned for v1.1)

**Known Limitations:**
- Performance has not been validated in pediatric populations (excluded from study)
- Model trained on North American hospital data; generalization to non-US settings unknown
- ECG devices from manufacturers not represented in training data (GE, Philips, Mortara) may produce variable signal quality
- Does not detect paced rhythms (explicitly excluded from intended use)

## Predicate Device

**Anumana ECG-AI (K232488):** FDA 510(k) clearance 2021. Same intended use: detection of atrial fibrillation and supraventricular arrhythmias from single-lead or 12-lead ECG. CardioGuard is substantially equivalent with documented differences in algorithm architecture (transformer vs. CNN), training data source, and performance characteristics.

## Clinical Validation Study

**Study Design:** Retrospective, double-blinded, multi-site  
**Sites:** Johns Hopkins Medical Center, Stanford Health, Mayo Clinic  
**Sample Size:** n=1500 adult patients (18+)  
**Adjudication:** Board-certified cardiologists (3-reviewer consensus)  
**Reference Standard:** Clinical ECG diagnosis or implantable device confirmation  
**Primary Endpoint:** AUROC >= 0.90 (95% CI lower bound >= 0.87)  
**Timeline:** 18 months execution, starting Month 11 of submission prep

## PCCP Strategy

**Retraining Cadence:** Quarterly  
**Drift Trigger:** 5% relative AUROC decrease on validation set  
**Data Sources:** Continuous collection from 3 partnered health systems  
**Approval Pathway:** Pre-notification to FDA every 12 months or per PCCP framework  

See pccp.yaml for full control plan configuration.

## Questions?

This toolkit is evolving. If you encounter gaps, ambiguities, or would like to contribute your own worked example, see [CONTRIBUTING.md](../../CONTRIBUTING.md) in the main repo.

For regulatory questions, this example assumes you have access to a qualified regulatory consultant for submission preparation.
