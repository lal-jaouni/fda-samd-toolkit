# CardioGuard ECG-AI: FDA Submission Timeline

**Document Version:** 1.0  
**Document Date:** 2026-10-15  
**Timeline Type:** Complete project schedule from device conception through FDA clearance

---

## Phase 1: Device Conception and Planning (Months 1-2)

**Weeks 1-4: Clinical Problem Definition**
- Problem statement: Manual ECG interpretation variability in primary care
- Market research: 50+ cardiac devices, arrhythmia detection apps
- Regulatory pathway research: Class II SaMD, predicate device selection (Anumana K232488)
- Clinical advisory board: Recruitment of cardiologists and primary care physicians
- **Deliverable:** Device concept white paper; regulatory pathway decision memo

**Weeks 5-8: Technology Planning**
- Algorithm architecture exploration: CNN vs. Transformer vs. Hybrid
- Training data sourcing: Outreach to 10 health systems for ECG data partnerships
- Deployment architecture: Cloud (AWS) vs. on-premise vs. hybrid
- Regulatory requirements analysis: PCCP guidance (Dec 2024), AI/ML guidance (2021)
- **Deliverable:** Technology architecture document; data acquisition agreements (3/10 health systems committed)

---

## Phase 2: Algorithm Development (Months 3-8)

**Months 3-4: Data Preparation and Preprocessing**
- Finalize agreements with 5 health systems for 250,000 ECGs (2019-2023)
- De-identification and HIPAA-compliant data transfer
- Signal preprocessing pipeline (normalization, filtering, artifact detection)
- Dataset composition analysis: 250K ECGs, class balance, demographics
- **Deliverable:** Training dataset (250,000 ECGs) with documented composition

**Months 5-6: Model Development**
- Transformer architecture implementation in PyTorch
- Training procedure design: optimizer (Adam), loss function (weighted cross-entropy), data split (70/15/15)
- Hyperparameter search: learning rate, batch size, dropout, regularization
- 112 GPU-days of training on NVIDIA A100 cluster
- **Deliverable:** Baseline model v1.0 with internal validation performance (AUROC 0.94)

**Months 7-8: Internal Validation and Refinement**
- Test set performance evaluation (37,500 test ECGs)
- Sub-population analysis (age, sex, race/ethnicity)
- Identification of performance gaps (0.03 AUROC gap in Black population)
- Model card development (comprehensive documentation)
- **Deliverable:** Model card; internal validation report; performance gap analysis

---

## Phase 3: Clinical Validation Study Preparation (Months 9-10)

**Month 9: Study Design and Protocol Development**
- Retrospective multi-site study design (Johns Hopkins, Stanford, Mayo Clinic)
- Sample size calculation: n=1500 for primary endpoint AUROC >= 0.90 (power = 80%)
- Endpoints and statistical analysis plan
- Case report form design
- Reference standard definition: board-certified cardiologist adjudication
- **Deliverable:** Clinical validation protocol (18-month prospective study)

**Month 10: Ethics and Regulatory Approval**
- IRB submissions to all 3 sites (Johns Hopkins, Stanford, Mayo Clinic)
- IRB approval obtained (anticipated 2024-12-15)
- Data use agreements with each health system
- Data transfer agreements and HIPAA BAAs
- **Deliverable:** IRB approvals (all sites); signed data agreements

---

## Phase 4: Clinical Validation Study Execution (Months 11-26)

**Months 11-12: Study Initiation and Pilot Adjudication**
- Study activation at all sites (2025-01-01)
- ECG data access set up; random subject selection
- Pilot adjudication of 100 cases to assess inter-rater reliability (target Fleiss kappa >= 0.80)
- Adjudicator training and baseline competency assessment
- **Milestone:** Enrollment begins; n=250 by end of month 12

**Months 13-18: Main Study Enrollment**
- Enrollment ramp: 500 by month 15, 1000 by month 20, 1500 by month 24
- Continuous ECG review and adjudication (3-reviewer consensus process)
- Monthly adjudication quality monitoring (10% re-review)
- De-identification verification; data quality checks
- **Milestone:** Enrollment n=750 by month 18

**Months 19-24: Continued Enrollment and Data Collection**
- Completion of main study enrollment (1500 patients) by month 24
- Ongoing adjudication of final cases
- Secondary site completion at month 24
- Final clinical follow-up data collection
- **Milestone:** Enrollment complete (1500 patients); adjudication 95% complete

**Months 25-26: Final Adjudication and Data Lock**
- Completion of all adjudication reviews
- Resolution of discordant cases
- Final data quality checks and consistency verification
- Database lock (no further data modifications)
- **Deliverable:** Final clinical validation study dataset (1500 subjects, fully adjudicated)

---

## Phase 5: Device Description and Regulatory Documentation (Months 11-20)

**Parallel to Study Execution:**

**Months 11-12: Device Description Finalization**
- Detailed technical documentation of algorithm, architecture, inputs, outputs
- Deployment architecture specification (AWS, load balancing, monitoring)
- Software bill of materials (third-party libraries, versions, licenses)
- Version control and model integrity documentation
- **Deliverable:** Device description document (02_device_description.md)

**Months 13-14: Indications for Use and Labeling Development**
- IFU statement aligned with clinical evidence and intended use
- Clinician labeling with performance data, warnings, precautions
- Quick reference cards and interpretation guidance
- User training curriculum development
- **Deliverable:** IFU statement (01_indications_for_use.md); labeling (05_labeling.md)

**Months 15-16: Predicate Device Comparison and Substantial Equivalence**
- Detailed comparison to Anumana ECG-AI (K232488)
- Technological differences analysis (transformer vs. CNN)
- Clinical performance comparison
- Risk profile analysis
- **Deliverable:** Substantial equivalence assessment (03_substantial_equivalence.md)

**Months 17-20: Risk Analysis and Cybersecurity Assessment**
- ISO 14971 hazard identification and risk assessment
- Mitigation strategy development and verification
- Cybersecurity threat modeling and control specification
- Penetration testing execution (month 19)
- Vulnerability disclosure policy development
- **Deliverables:** Risk analysis (risk_analysis.md); cybersecurity assessment (cybersecurity.md)

---

## Phase 6: Clinical Validation Analysis (Months 25-27)

**Month 25: Preliminary Analysis**
- Database lock and quality verification
- Descriptive statistics on study cohort
- Primary endpoint analysis (AUROC calculation with DeLong CI)
- Secondary endpoint analysis (sensitivity, specificity, PPV, NPV)

**Month 26: Sub-Population Analysis**
- Stratified performance by age, sex, race/ethnicity
- Gap analysis and mitigation justification
- Comparison to Anumana predicate device performance
- Safety analysis (adverse events, unexpected findings)

**Month 27: Final Report Preparation**
- Statistical analysis report finalization
- Performance summary compilation
- Clinical validation report approved by statistical lead and study PI
- **Deliverable:** Clinical validation study report (04_performance_summary.md)

---

## Phase 7: Predetermined Change Control Plan Development (Months 21-23)

**Month 21: PCCP Framework Design**
- Planned modifications definition (retraining, data expansion, hyperparameter optimization)
- Modification protocol and procedure specification
- Data management and quality assurance standards
- Drift monitoring framework (monthly AUROC tracking, drift triggers)

**Month 22: FDA Guidance Alignment**
- Alignment with FDA PCCP guidance (Dec 2024)
- Specified change thresholds (5% AUROC, 3% sensitivity)
- FDA pre-notification and reporting procedures
- Post-market surveillance integration

**Month 23: PCCP Finalization**
- Version control and document control procedures
- Retraining methodology finalization
- Hyperparameter optimization procedures
- **Deliverable:** PCCP (pccp.yaml)

---

## Phase 8: Post-Market Surveillance and Submission Readiness (Months 24-28)

**Month 24: Post-Market Plan Development**
- Real-world performance database design
- Registry participation planning (24-month commitment)
- Adverse event tracking and reporting procedures
- Annual FDA pre-notification schedule

**Month 25-26: Internal Quality and Regulatory Review**
- Design verification (unit tests, integration tests, system tests coverage >= 95%)
- Design validation (clinical validation study completion)
- QMS documentation and ISO 13485 compliance verification
- Software development plan per IEC 62304

**Month 27: Final Internal Review and Sign-Off**
- Submission package assembly and organization
- Final review by regulatory, clinical, and engineering leads
- Cross-reference and consistency check
- Document sign-off for submission
- **Deliverable:** Submission readiness confirmation (submission_checklist.yaml)

**Month 28: Submission Package Preparation**
- PDF compilation and bookmarking
- Cover letter drafting
- FDA Form 510(k) completion
- Facility registration verification
- Final submission file preparation (electronic submission via eCopy)
- **Deliverable:** Complete 510(k) submission package ready for FDA

---

## Phase 9: FDA Submission and Review (Months 29-40)

**Month 29: FDA Submission**
- Electronic submission to FDA via eSTARs
- Cover letter signed and dated
- All required documents included
- Submission confirmation receipt (expected within 2 business days)
- **Milestone:** Submission date = 2026-10-15

**Months 29-30: FDA Initial Review and CDRH Assignment**
- FDA receipt acknowledgment and establishment of case number
- Assignment to CDRH review division (Cardiovascular/Software division)
- Pre-submission review for completeness
- Determination of standard vs. expedited review (expected: standard, 90-day clock)
- **Expected by:** 2026-11-15 (one month after submission)

**Months 31-39: Substantive FDA Review**
- FDA review of indications, substantial equivalence, performance data
- FDA questions or deficiency notice (if any)
- CardioGuard response to deficiencies (within 30 days of notice)
- Additional data or clarifications as requested
- **Standard review clock:** 90 calendar days = 3 months
- **Expected clearance decision:** December 2026 to January 2027

**Month 40: FDA Clearance or Additional Review**
- Potential outcomes:
  1. **Clearance (most likely):** 510(k) clearance letter issued; device approved for marketing
  2. **Substantial Equivalence Not Demonstrated:** Request to resubmit with additional data or modify predicate
  3. **Request for Reclassification:** If FDA determines Class II inappropriate (unlikely)

---

## Key Milestones and Decision Points

| Milestone | Target Date | Actual Date | Status | Responsible |
|---|---|---|---|---|
| Device concept finalized | 2025-03-31 | 2025-03-25 | COMPLETE | Product |
| Training dataset collected | 2025-07-31 | 2025-07-20 | COMPLETE | Data Science |
| Baseline model v1.0 complete | 2025-08-31 | 2025-08-15 | COMPLETE | ML Engineering |
| Clinical validation study protocol approved by IRBs | 2024-12-31 | 2024-12-15 | COMPLETE | Regulatory |
| Study enrollment begins | 2025-01-15 | 2025-01-01 | COMPLETE | Clinical Affairs |
| Study 50% enrollment (750 patients) | 2025-09-30 | 2025-09-28 | COMPLETE | Clinical Affairs |
| Study enrollment complete (1500 patients) | 2026-06-30 | 2026-06-28 | COMPLETE | Clinical Affairs |
| Clinical validation report complete | 2026-08-31 | 2026-07-30 | COMPLETE | Biostatistics |
| Regulatory documentation complete | 2026-09-30 | 2026-09-25 | COMPLETE | Regulatory |
| Internal review approval | 2026-10-10 | 2026-10-12 | COMPLETE | Leadership |
| **FDA 510(k) Submission** | **2026-10-15** | **[IN PROGRESS]** | **ON SCHEDULE** | **Regulatory** |
| FDA submission receipt | 2026-11-15 | TBD | EXPECTED | FDA |
| FDA substantive review begins | 2026-11-20 | TBD | EXPECTED | FDA |
| FDA requests clarifications (if any) | 2026-12-15 | TBD | POSSIBLE | FDA |
| FDA clearance decision | 2027-01-15 | TBD | EXPECTED | FDA |

---

## Critical Path Analysis

**Critical path items** (no schedule slack; any delay delays entire submission):

1. **Clinical validation study execution** (Months 11-26)
   - Longest pole in the tent; determines overall timeline
   - 18-month retrospective study cannot be accelerated below practical minimum
   - Any delay in enrollment or adjudication delays FDA submission

2. **Clinical validation analysis** (Months 25-27)
   - Depends on study completion
   - Cannot start statistical analysis until database locked
   - Any data quality issues during analysis require adjudication review

3. **Device description documentation** (Months 11-20)
   - Parallel track to study but must be complete before submission
   - Dependent on finalized algorithm and deployment design
   - Risk: any algorithm changes post-study require new performance data

4. **FDA regulatory approval timeline** (Months 29-40)
   - Out of CardioGuard control; FDA 90-day standard review clock
   - Deficiencies or requests for additional data extend clock beyond 90 days
   - Submission quality critical to minimize FDA requests

---

## Contingency Planning

**Risk: Clinical validation study enrollment slower than planned**
- Mitigation: Pre-enrolled sites with data availability confirmed; backup sites identified
- Contingency: If enrollment 10% below target, can still power primary endpoint with n=1350

**Risk: Algorithm performance in clinical validation < target (AUROC < 0.90)**
- Mitigation: Internal validation performance supports margin (AUROC 0.94 > 0.90 target)
- Contingency: Additional training data and retraining; 6-month delay to clinical validation re-run

**Risk: Identified performance disparity in Black population unresolvable**
- Mitigation: Gap disclosed transparently; mitigation plan in PCCP addresses root causes
- Contingency: Gap disclosed to FDA; submission proceeds with equity commitment; device approved with Post-Market mitigation

**Risk: FDA deficiency notice requesting additional clinical data**
- Mitigation: Clinical validation protocol designed conservatively; sample size > minimum required
- Contingency: 30-day response window; CardioGuard performs additional sub-group analysis if requested

**Risk: Cybersecurity vulnerability discovered in final testing**
- Mitigation: Annual penetration testing completed; no critical issues identified
- Contingency: Security patch deployed; FDA notified of remediation

**Risk: Key personnel unavailable (illness, departure)**
- Mitigation: Succession planning; cross-training of regulatory and clinical teams
- Contingency: Regulatory consultant retained as backup resource

---

## Success Criteria and Definition of Done

**FDA Submission Ready:**
- All required documents compiled and reviewed
- Submission checklist 100% complete
- Internal QA sign-off obtained
- Submission package error-free and complete

**FDA Clearance Criteria:**
1. Primary endpoint achieved (AUROC >= 0.90, CI lower bound >= 0.87)
2. Secondary endpoints achieved (sensitivity >= 0.85, specificity >= 0.90)
3. Substantial equivalence demonstrated to Anumana K232488
4. Risk analysis shows acceptable residual risk
5. No safety signals identified
6. Cybersecurity controls verified
7. Performance equity assessment transparent with mitigation plan

**Post-Clearance Readiness:**
1. Clinical training program deployed to health systems
2. Post-market surveillance database operational
3. Quarterly retraining process established
4. FDA pre-notification procedures documented
5. Adverse event reporting system operational

---

## Communication and Stakeholder Updates

**Monthly Steering Committee Meetings:**
- Regulatory Affairs, Clinical Affairs, Engineering, Quality
- Status review of milestones, risks, decisions
- Decisions on design changes or scope adjustments
- Budget and resource tracking

**Quarterly Executive Briefings:**
- CEO, CFO, Board
- Overall project status and timeline
- Investment tracking
- Market readiness assessment

**FDA Pre-Submission Meeting (if conducted):**
- Q-Submission not planned; direct 510(k) selected as appropriate
- Pre-submission meeting considered only if deficiencies expected post-submission

**Health System Communication (Post-Clearance):**
- Deployment readiness communications
- Training schedule and requirements
- Go-live planning and support

---

## Budget and Resource Allocation

**Key Resource Roles:**
- **Regulatory Lead:** 1.0 FTE (Sarah Chen, MD, PhD)
- **Clinical Science Lead:** 0.5 FTE (Michael Rodriguez, MD)
- **Biostatistics:** 0.5 FTE (Robert Kumar, PhD)
- **Engineering/DevOps:** 1.0 FTE (CTO + 1 contractor)
- **Clinical Affairs:** 1.0 FTE (Coordination with sites)
- **Quality/Compliance:** 0.5 FTE

**Estimated Costs:**
- Clinical validation study: $800K (site fees, adjudication, data management)
- Regulatory consulting (external): $150K
- Third-party penetration testing: $50K
- Miscellaneous (travel, systems, etc.): $100K
- **Total estimated cost: $1.1M**

---

## Document Certification

This timeline is accurate and reflects CardioGuard ECG-AI's planned submission schedule as of 2026-10-15.

**Prepared by:** Sarah Chen, MD, PhD (VP Regulatory Affairs)  
**Date:** 2026-10-15
