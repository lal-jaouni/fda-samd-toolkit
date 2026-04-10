"""FDA submission readiness checklist items organized by category."""

from fda_samd_toolkit.checklist.schemas import ChecklistItem, ItemSeverity

# ruff: noqa: E501

# Design Controls (21 CFR 820.30)
DESIGN_ITEMS = [
    ChecklistItem(
        id="dc-001",
        category="Design Controls",
        requirement="Design plan established and approved before design input phase",
        evidence_required="Design plan document with approval sign-off; defines design process, responsibilities, and timeline",
        standard_reference="21 CFR 820.30(b) - Design Planning",
        severity=ItemSeverity.BLOCKER,
        notes="Must precede all design activities",
    ),
    ChecklistItem(
        id="dc-002",
        category="Design Controls",
        requirement="Design inputs documented and approved",
        evidence_required="Design input document listing functional and performance requirements, safety requirements, regulatory constraints, and traceability matrix",
        standard_reference="21 CFR 820.30(c) - Design Inputs",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="dc-003",
        category="Design Controls",
        requirement="Design outputs documented and reviewed for adequacy",
        evidence_required="Design output specifications (algorithms, architecture, file formats) traced to inputs; design output review checklist",
        standard_reference="21 CFR 820.30(d) - Design Output",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="dc-004",
        category="Design Controls",
        requirement="Design review completed before release for production",
        evidence_required="Design review meeting minutes, attendee list (cross-functional team), evidence of resolution of issues identified",
        standard_reference="21 CFR 820.30(e) - Design Review",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="dc-005",
        category="Design Controls",
        requirement="Design verification completed (does design meet inputs?)",
        evidence_required="Verification plan and report; testing of algorithms/subsystems against design inputs; traceability to requirements",
        standard_reference="21 CFR 820.30(f) - Design Verification",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="dc-006",
        category="Design Controls",
        requirement="Design validation completed (does device meet user needs?)",
        evidence_required="Validation plan and report; clinical testing, field studies, or real-world performance data; statistical analysis",
        standard_reference="21 CFR 820.30(g) - Design Validation",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="dc-007",
        category="Design Controls",
        requirement="Design transfer to production documented and verified",
        evidence_required="Design transfer plan; evidence that manufacturing can reproducibly produce design specifications",
        standard_reference="21 CFR 820.30(h) - Design Transfer",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="dc-008",
        category="Design Controls",
        requirement="Design changes documented and approved via change control",
        evidence_required="Change control system with design change requests, impact assessments, approval workflows, re-verification/validation",
        standard_reference="21 CFR 820.30(i) - Design Changes",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="dc-009",
        category="Design Controls",
        requirement="Design history file maintained",
        evidence_required="DHF containing all design records: plans, inputs, outputs, reviews, verification, validation, changes, transfer",
        standard_reference="21 CFR 820.30(j) - Design History File",
        severity=ItemSeverity.BLOCKER,
    ),
]

# Risk Management (ISO 14971)
RISK_ITEMS = [
    ChecklistItem(
        id="rm-001",
        category="Risk Management",
        requirement="Risk management plan established",
        evidence_required="Risk management plan defining scope, strategy, responsibilities, and timeline; identifies who performs hazard analysis, risk evaluation, risk control",
        standard_reference="ISO 14971:2019 Section 4.1",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="rm-002",
        category="Risk Management",
        requirement="Hazard analysis completed (what can go wrong?)",
        evidence_required="Hazard analysis report identifying all hazards (e.g., false negatives, algorithm bias, data corruption, cybersecurity vulnerabilities); FMEA or similar structured method",
        standard_reference="ISO 14971:2019 Section 4.2",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="rm-003",
        category="Risk Management",
        requirement="Risk evaluation completed (how severe/likely?)",
        evidence_required="Risk evaluation report quantifying severity and probability for each hazard; risk matrix or scoring method; justification for risk tolerance decisions",
        standard_reference="ISO 14971:2019 Section 4.3",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="rm-004",
        category="Risk Management",
        requirement="Risk control measures designed and evaluated",
        evidence_required="Risk control plan specifying mitigation for each significant hazard; evidence of residual risk evaluation; traceability from hazard to control to design",
        standard_reference="ISO 14971:2019 Section 4.4",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="rm-005",
        category="Risk Management",
        requirement="Residual risk evaluation and overall risk analysis completed",
        evidence_required="Residual risk report; evidence that residual risks are acceptable; overall risk benefit analysis; summary of risks considered acceptable",
        standard_reference="ISO 14971:2019 Section 4.5",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="rm-006",
        category="Risk Management",
        requirement="Risk management report prepared",
        evidence_required="Comprehensive risk management report summarizing hazards, risks, controls, and residual risks; approvals from relevant stakeholders",
        standard_reference="ISO 14971:2019 Section 4.6",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="rm-007",
        category="Risk Management",
        requirement="Post-production information monitoring plan established",
        evidence_required="Plan for collecting and reviewing post-market data (complaints, adverse events, performance issues); defined feedback channels and review frequency",
        standard_reference="ISO 14971:2019 Section 4.7",
        severity=ItemSeverity.MAJOR,
    ),
]

# Software Lifecycle (IEC 62304)
SOFTWARE_ITEMS = [
    ChecklistItem(
        id="sl-001",
        category="Software Lifecycle",
        requirement="Software safety classification determined",
        evidence_required="Software safety classification document (Class A/B/C per IEC 62304); justification based on device risk level",
        standard_reference="IEC 62304:2015 Section 4.2",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-002",
        category="Software Lifecycle",
        requirement="Software development plan (SDP) established",
        evidence_required="SDP defining development lifecycle model, architecture, tools, standards, testing strategy, configuration management, documentation plan",
        standard_reference="IEC 62304:2015 Section 5.1",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-003",
        category="Software Lifecycle",
        requirement="Software requirements specification (SRS) documented",
        evidence_required="SRS specifying functional requirements, performance requirements, constraints, interfaces, regulatory requirements; traceability matrix",
        standard_reference="IEC 62304:2015 Section 5.2",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-004",
        category="Software Lifecycle",
        requirement="Software architecture defined and documented",
        evidence_required="Architecture specification (high-level design) showing modules, interfaces, data flow, component interactions, libraries/COTS used",
        standard_reference="IEC 62304:2015 Section 5.3",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-005",
        category="Software Lifecycle",
        requirement="Detailed software design completed",
        evidence_required="Detailed design documents describing each module's logic, algorithms, data structures, error handling; code structure and control flow",
        standard_reference="IEC 62304:2015 Section 5.4",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-006",
        category="Software Lifecycle",
        requirement="Software unit implementation and verification completed",
        evidence_required="Source code; unit testing results; code review records; traceability of implementation to detailed design",
        standard_reference="IEC 62304:2015 Section 5.5",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-007",
        category="Software Lifecycle",
        requirement="Software integration and integration testing completed",
        evidence_required="Integration test plan and results; evidence that integrated software functions per architecture; interface testing",
        standard_reference="IEC 62304:2015 Section 5.6",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-008",
        category="Software Lifecycle",
        requirement="Software system testing completed",
        evidence_required="System test plan and results verifying software against SRS; functional testing, performance testing, stress testing; traceability to requirements",
        standard_reference="IEC 62304:2015 Section 5.7",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sl-009",
        category="Software Lifecycle",
        requirement="Software release procedures documented",
        evidence_required="Release management process; version control procedures; release notes; deployment procedures; rollback procedures if applicable",
        standard_reference="IEC 62304:2015 Section 5.8",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="sl-010",
        category="Software Lifecycle",
        requirement="Problem resolution procedures established",
        evidence_required="Process for reporting, tracking, and resolving software issues; bug tracking system; change control integration; severity assessment",
        standard_reference="IEC 62304:2015 Section 5.9",
        severity=ItemSeverity.MAJOR,
    ),
]

# AI/ML-Specific Requirements
AIML_ITEMS = [
    ChecklistItem(
        id="ml-001",
        category="AI/ML-Specific",
        requirement="Training data documentation completed",
        evidence_required="Data dictionary describing all features; data provenance (source, date range, collection method); data quality metrics; handling of missing/anomalous data; labeling methodology and validation",
        standard_reference="FDA Software as a Medical Device Action Plan (2021)",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="ml-002",
        category="AI/ML-Specific",
        requirement="Model card created with algorithm documentation",
        evidence_required="Model card per Mitchell et al. including: model description, intended use, performance metrics, limitations, sub-population analysis, ethical considerations",
        standard_reference="FDA Proposed AI/ML Regulation (2023 draft)",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="ml-003",
        category="AI/ML-Specific",
        requirement="Algorithm performance metrics established and validated",
        evidence_required="Validation study with independent test set; performance metrics (sensitivity, specificity, AUROC, AUC-PR, F1 score); comparison to predicate/standard of care",
        standard_reference="FDA Proposed AI/ML Regulation (2023 draft)",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="ml-004",
        category="AI/ML-Specific",
        requirement="Sub-population analysis completed",
        evidence_required="Performance stratified by demographics (age, gender, race/ethnicity, comorbidities); identification of sub-populations with degraded performance; mitigation strategies",
        standard_reference="FDA Proposed AI/ML Regulation (2023 draft)",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="ml-005",
        category="AI/ML-Specific",
        requirement="Data drift monitoring plan established",
        evidence_required="Plan for detecting data drift post-market (feature distribution shifts, performance degradation); defined thresholds and response actions",
        standard_reference="FDA Proposed AI/ML Regulation (2023 draft)",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="ml-006",
        category="AI/ML-Specific",
        requirement="Model retraining procedures documented (if applicable)",
        evidence_required="For PCCP: retraining plan with data selection, labeling, validation criteria; for non-PCCP: justification that retraining is not planned",
        standard_reference="FDA Software as a Medical Device Action Plan (2021)",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="ml-007",
        category="AI/ML-Specific",
        requirement="Explainability/transparency documentation",
        evidence_required="Evidence of algorithm transparency (feature importance, decision rules, or other interpretability methods); user-facing documentation about how device makes decisions",
        standard_reference="FDA Proposed AI/ML Regulation (2023 draft)",
        severity=ItemSeverity.MINOR,
    ),
    ChecklistItem(
        id="ml-008",
        category="AI/ML-Specific",
        requirement="PCCP (Post-Market Continuous Learning Plan) if modifications planned",
        evidence_required="Approved PCCP document defining pre-approved modifications, modification protocols, performance monitoring, impact assessment, or justification that PCCP not required",
        standard_reference="FDA Proposed AI/ML Regulation (2023 draft)",
        severity=ItemSeverity.BLOCKER,
        notes="Required only if algorithm retraining or data updates planned",
    ),
]

# Cybersecurity (FDA 2023 Guidance)
CYBERSECURITY_ITEMS = [
    ChecklistItem(
        id="cs-001",
        category="Cybersecurity",
        requirement="Software bill of materials (SBOM) prepared",
        evidence_required="SBOM listing all software components, libraries, and dependencies with versions and known vulnerabilities; in SPDX or CycloneDX format",
        standard_reference="FDA 2023 Cybersecurity Guidance",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="cs-002",
        category="Cybersecurity",
        requirement="Threat model created and vulnerabilities identified",
        evidence_required="Threat model document (STRIDE or similar); identified threats; assessment of likelihood and impact; vulnerability inventory",
        standard_reference="FDA 2023 Cybersecurity Guidance",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="cs-003",
        category="Cybersecurity",
        requirement="Security testing completed",
        evidence_required="Penetration testing results; fuzz testing; static analysis results; dynamic analysis results; evidence of remediation of identified vulnerabilities",
        standard_reference="FDA 2023 Cybersecurity Guidance",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="cs-004",
        category="Cybersecurity",
        requirement="Vulnerability disclosure policy established",
        evidence_required="Published policy describing how security researchers can report vulnerabilities; security.txt file; commitment to timely patching",
        standard_reference="FDA 2023 Cybersecurity Guidance",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="cs-005",
        category="Cybersecurity",
        requirement="Incident response plan prepared",
        evidence_required="Security incident response plan; defined roles and responsibilities; communication procedures; evidence of testing/drills",
        standard_reference="FDA 2023 Cybersecurity Guidance",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="cs-006",
        category="Cybersecurity",
        requirement="Post-market cybersecurity monitoring plan established",
        evidence_required="Plan for monitoring for security vulnerabilities post-market; defined update/patch procedures; communication plan for security updates",
        standard_reference="FDA 2023 Cybersecurity Guidance",
        severity=ItemSeverity.MAJOR,
    ),
]

# Clinical Evidence
CLINICAL_ITEMS = [
    ChecklistItem(
        id="ce-001",
        category="Clinical Evidence",
        requirement="Clinical evaluation report prepared",
        evidence_required="Comprehensive clinical evaluation report reviewing literature, predicate device data, and clinical validation study results; discussion of safety and efficacy",
        standard_reference="21 CFR 807.87(e) - Clinical Data",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="ce-002",
        category="Clinical Evidence",
        requirement="Clinical validation study conducted (if required)",
        evidence_required="Prospective or retrospective clinical study with predefined protocol; IRB approval; informed consent (if applicable); statistical analysis plan; results report",
        standard_reference="21 CFR Part 56 - Institutional Review Boards",
        severity=ItemSeverity.BLOCKER,
        notes="Required for most AI/ML devices; may be waived for cleared predicates",
    ),
    ChecklistItem(
        id="ce-003",
        category="Clinical Evidence",
        requirement="Performance statistics documented and justified",
        evidence_required="Sensitivity, specificity, predictive values, confidence intervals; comparison to predicate or reference standard; subgroup analysis; statistical power justification",
        standard_reference="FDA Guidance - Analytical Validation of Diagnostic Tests",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="ce-004",
        category="Clinical Evidence",
        requirement="Substantial equivalence established (510k only)",
        evidence_required="Substantial equivalence assessment comparing device to predicate on intended use, technology, and performance; explanation of any differences",
        standard_reference="21 CFR 807.87(a) - 510(k) Summary",
        severity=ItemSeverity.BLOCKER,
        notes="Required for 510(k) submissions",
    ),
]

# Quality Management (ISO 13485)
QUALITY_ITEMS = [
    ChecklistItem(
        id="qm-001",
        category="Quality Management",
        requirement="Document control procedures established",
        evidence_required="Document management system; procedures for creation, review, approval, distribution, and archival of quality documents; version control",
        standard_reference="ISO 13485:2016 Section 4.2",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="qm-002",
        category="Quality Management",
        requirement="Supplier/vendor controls established",
        evidence_required="Supplier evaluation and approval procedures; purchasing specifications; supplier audit records; COTS software license tracking",
        standard_reference="ISO 13485:2016 Section 8.4",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="qm-003",
        category="Quality Management",
        requirement="Corrective and preventive action (CAPA) system implemented",
        evidence_required="CAPA procedures; tracking system; completed CAPA records; evidence of root cause analysis; effectiveness checks",
        standard_reference="ISO 13485:2016 Section 8.5",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="qm-004",
        category="Quality Management",
        requirement="Internal audits completed",
        evidence_required="Internal audit schedule; audit reports covering all quality system areas; audit findings and corrective actions; management review minutes",
        standard_reference="ISO 13485:2016 Section 8.2",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="qm-005",
        category="Quality Management",
        requirement="Management review performed",
        evidence_required="Management review meeting minutes; review of audit results, customer feedback, product performance, and effectiveness of corrective actions",
        standard_reference="ISO 13485:2016 Section 5.6",
        severity=ItemSeverity.MINOR,
    ),
]

# Submission Documents
SUBMISSION_ITEMS = [
    ChecklistItem(
        id="sub-001",
        category="Submission Documents",
        requirement="510(k) cover letter prepared and complete",
        evidence_required="Signed cover letter with device name, manufacturer info, product code, predicate devices, substantial equivalence statement, and certifications",
        standard_reference="21 CFR 807.85 - 510(k) Cover Letter",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sub-002",
        category="Submission Documents",
        requirement="Indications for use statement finalized",
        evidence_required="Clear statement of intended use, patient population, disease/condition, method of operation, and user environment",
        standard_reference="21 CFR 807.87(a) - 510(k) Summary",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sub-003",
        category="Submission Documents",
        requirement="Device description document prepared",
        evidence_required="Detailed description of device, components, hardware, software, accessories; diagrams and technical specifications",
        standard_reference="21 CFR 807.87(a) - 510(k) Summary",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sub-004",
        category="Submission Documents",
        requirement="Substantial equivalence comparison documentation completed",
        evidence_required="Detailed comparison to predicate device(s) on design, materials, performance, and intended use; explanation of any differences",
        standard_reference="21 CFR 807.87(b) - Substantial Equivalence",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sub-005",
        category="Submission Documents",
        requirement="Performance data summary prepared",
        evidence_required="Summary of validation study results, algorithm performance metrics, safety data, and clinical evidence supporting device performance",
        standard_reference="21 CFR 807.87(c) - Performance Data",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sub-006",
        category="Submission Documents",
        requirement="Labeling and instructions for use finalized",
        evidence_required="Device labeling (packaging, instructions, warnings); user manual; training materials; IFU includes all required information per 21 CFR 801",
        standard_reference="21 CFR 801 - Labeling",
        severity=ItemSeverity.MAJOR,
    ),
    ChecklistItem(
        id="sub-007",
        category="Submission Documents",
        requirement="Summary of safety and performance (SSED) prepared",
        evidence_required="Comprehensive SSED document summarizing device design, non-clinical testing, clinical testing, and safety data",
        standard_reference="FDA 510(k) Submission Guidance",
        severity=ItemSeverity.BLOCKER,
    ),
    ChecklistItem(
        id="sub-008",
        category="Submission Documents",
        requirement="Biocompatibility assessment completed (if applicable)",
        evidence_required="Biocompatibility testing per ISO 10993 (materials, duration of contact); test reports or justification if not required",
        standard_reference="ISO 10993 Series - Biocompatibility",
        severity=ItemSeverity.MAJOR,
        notes="Required if device contacts patient or user",
    ),
    ChecklistItem(
        id="sub-009",
        category="Submission Documents",
        requirement="Software documentation package prepared",
        evidence_required="Software lifecycle documentation: SDP, SRS, architecture, design, source code listings, test reports, risk analysis, security assessment",
        standard_reference="IEC 62304 + FDA SaMD Guidance",
        severity=ItemSeverity.BLOCKER,
    ),
]

# Compile all items into a complete list
ALL_ITEMS = (
    DESIGN_ITEMS
    + RISK_ITEMS
    + SOFTWARE_ITEMS
    + AIML_ITEMS
    + CYBERSECURITY_ITEMS
    + CLINICAL_ITEMS
    + QUALITY_ITEMS
    + SUBMISSION_ITEMS
)


def get_items_by_category(category: str) -> list[ChecklistItem]:
    """Get all items for a specific category."""
    return [item for item in ALL_ITEMS if item.category == category]


def get_all_categories() -> list[str]:
    """Get unique list of all categories."""
    return sorted(set(item.category for item in ALL_ITEMS))


def get_item_by_id(item_id: str) -> ChecklistItem | None:
    """Get a single item by ID."""
    return next((item for item in ALL_ITEMS if item.id == item_id), None)
