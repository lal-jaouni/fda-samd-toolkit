# FDA SaMD Toolkit Scope Boundaries

This document defines what is in scope, out of scope, and adjacent for the FDA SaMD Toolkit through v1.0. These boundaries ensure focused development and clear communication to users and contributors.

## IN SCOPE

Features that solve core FDA 510(k) AI/ML submission pain points. All features support the primary persona: AI/ML startup CTO preparing a first 510(k) submission.

### v0.1 (Shipped April 2026)

- **Predetermined Change Control Plan (PCCP) Generator**: Pydantic schema + Jinja templates that auto-generate PCCP from YAML config, following FDA Dec 2024 guidance.
- **510(k) AI/ML Templates**: 7 Markdown templates for FDA-required sections (indications for use, device description, substantial equivalence, performance testing, training data characterization, risk analysis, human factors).
- **Model Card Generator**: FDA-extended model cards (Mitchell et al. 2019 baseline + FDA-specific fields for predicate devices, subpopulation performance, bias analysis).
- **Clinical Validation Framework**: Pre-deployment validation protocols with modality-specific guidance (imaging, ECG/PPG signals, NLP/text, multimodal).
- **Submission Readiness Checklist**: 58-item checklist across 8 categories (design controls, risk, software lifecycle, AI/ML, cybersecurity, clinical evidence, QMS, documentation).
- **CLI + Rich formatting**: Click-based CLI with pretty table/tree output; `fda-samd pccp`, `model-card`, `checklist`, `templates` subcommands.
- **Worked Example (CardioGuard)**: Complete end-to-end 510(k) for a fictional ECG-based arrhythmia detector, showing all components integrated.

### v0.2 (Planned May 2026)

- **Cybersecurity SBOM Generator** (#14): Machine-readable SBOM (NTIA format) auto-generated from Pydantic schema of software components. Mandatory per FDA June 2025 guidance.
- **Bias & Subpopulation Performance Report** (#15): Generates demographic breakdown template (race, ethnicity, sex, age, BMI, comorbidities) and performance analysis table. Supports Jan 2025 FDA guidance requirement.
- **Real-World Performance Monitoring Plan** (#16): Post-market monitoring protocol including data sources (EHR, claims, devices), metrics (sensitivity, specificity, drift, AUC), thresholds, escalation, and rollback procedures.
- **eSTAR Submission Package Builder** (#17): Auto-assembles FDA submission files into eSTAR structure (required Oct 2023). Generates folder tree, manifest, and metadata for upload to FDA eSubmitter.
- **IEC 62304 + ISO 14971 Templates** (#18): Integrates OpenRegulatory MIT-licensed templates for software lifecycle (IEC 62304) and risk management (ISO 14971), completing the submission scaffold.

### Rationale for v0.2 Scope

Each v0.2 feature:
1. Solves an acute pain point backed by user research (must-use from research/must_use_features.md)
2. Is mandatory per FDA guidance (SBOM, bias, monitoring) or industry standard (eSTAR, IEC 62304)
3. Is expensive to outsource ($3-15K per feature via consultants)
4. Is missing from competing open-source tools
5. Is requested by Tier 1 consulting candidate companies

---

## OUT OF SCOPE (Through v1.0)

Features that solve adjacent problems but are outside the core mission. These are explicitly de-prioritized.

### Why These Are Out of Scope

Each boundary is defensible against "but isn't this just X?" objections.

| Feature | Why Out of Scope | Alternative |
|---------|------------------|-------------|
| **Medical/clinical advice** | Toolkit generates regulatory scaffolding, not clinical guidance. Users are responsible for clinical validity of their device. | Work with clinical consultants before using toolkit |
| **Regulatory advice** | Toolkit implements FDA guidance, not legal interpretation. Users must work with regulatory affairs professionals for strategy. | Engage regulatory consultants for FDA negotiations, presubmission meetings |
| **Automated FDA submission filing** | eSTAR package builder (v0.2) generates folder structure; FDA eSubmitter upload and form completion are user responsibility. Liability risk if automation fails. | Manual eSubmitter upload (10 min per submission) |
| **eQMS replacement** | Toolkit generates documents; eQMS tools (Greenlight Guru, Qualio, Formwork) manage design history files, change control, and audit trails. Different problems. | Use eQMS alongside toolkit (common pattern) |
| **PMA submissions (v1.0)** | PMA scope is 10x larger than 510(k) (6-12 month FDA review). Toolkit focuses on 510(k) first. | Toolkit may support PMA post-v1.0 if demand exists |
| **De Novo submissions (v1.0)** | De Novo requires novel classification (FDA establishes predicate devices). Toolkit assumes 510(k) predicate-based pathway. | Toolkit may support De Novo post-v1.0 if demand exists |
| **EU MDR / CE marking** | EU MDR is a different regulatory regime (different risk classification, technical documentation, notified body review). Toolkit is US FDA-focused. | Create separate toolkit for EU (future project) |
| **IVD (In Vitro Diagnostics)** | IVDs (lab tests, diagnostics) have separate FDA pathway (CLIA, IVD guidance, different predicate logic). Toolkit focuses on in-vivo devices. | Create separate IVD toolkit (future project) |

### Why Scope Matters

- **Avoids feature creep**: Each out-of-scope item is someone's urgent need. Saying "no" preserves focus on core users.
- **Clarifies liability**: By stating "not medical or regulatory advice," toolkit creators protect users and themselves.
- **Enables community**: Out-of-scope items become opportunities for contributing projects or community extensions.

---

## ADJACENT (Possible Post-v1.0)

Features that complement core mission and may move in-scope if demand justifies. Criteria for moving in-scope: 50%+ of user personas would benefit + feasible to implement within toolkit pattern + backed by FDA guidance or industry standard.

| Feature | Current Status | Rationale for Future In-Scope | Estimated Effort |
|---------|---|---|---|
| **IEC 62366 (Usability Engineering)** | Adjacent | Usability is mandatory for medical devices (FDA guidance). Toolkit could generate usability validation protocols (e.g., heuristic evaluation, user testing templates). | 2-3 weeks |
| **Cybersecurity Threat Modeling** | Adjacent | Current SBOM (v0.2) is passive inventory. Threat modeling (STRIDE, attack trees) helps identify mitigation strategies. But scope is specialized (AppSec engineers needed). | 3-4 weeks + expert review |
| **Post-Market Surveillance Dashboards** | Adjacent | Monitoring plan (v0.2) specifies what to track. Dashboard template for real-world data ingestion, drift detection, and alert escalation would close the loop. But requires data infrastructure (database, ETL). | 4-6 weeks |
| **Real-World Device Dissection / Case Study Builder** | Adjacent | Toolkit could parse public FDA submissions (Innolitics, Cruxi) and generate structured case studies. Helps users learn by example. But requires reverse-engineering effort per device. | 2 weeks per device class |
| **IRB Submission Scaffolding** | Adjacent | Hospital persona (Persona 3) needs IRB approval for clinical validation. Toolkit could generate IRB submission templates. But IRB requirements vary by institution (not standardized like FDA). | 2-3 weeks |
| **HIPAA Compliance Documentation** | Adjacent | Hospital innovation teams need privacy documentation. But HIPAA is legal/compliance requirement, not FDA regulatory scaffolding. | 2 weeks |
| **GMLP (Good Machine Learning Practice) Evidence Templates** | Adjacent | FDA Jan 2025 guidance references GMLP principles. Toolkit could map each principle to a scaffold / evidence generator. But GMLP is emerging standard; guidance is still fluid. | 3-4 weeks |

### Decision Rule for Future Scope Expansion

A feature moves from adjacent to in-scope if:
1. **Minimum 50% of user personas would benefit** (e.g., if feature helps only hospital persona, it fails this gate unless usage is very high)
2. **Backed by FDA guidance or industry standard** (not internal request or competitor feature)
3. **Follows existing component pattern** (Pydantic schema + Jinja templates + CLI subcommand; no novel architecture)
4. **Adds <30% effort to existing component** (no major new infrastructure)

Example: **Post-Market Monitoring Plan (v0.2) is in-scope** because:
- All 3 personas benefit (CTO needs to plan for it, consultant packages it, hospital uses for governance)
- FDA is actively soliciting input (Nov 2024 Federal Register notice)
- Follows pattern: monitoring_config.yaml -> Jinja template -> markdown report
- ~1 week effort

Example: **Cybersecurity Threat Modeling** would need to be adjacent until:
- 50%+ of users request it (currently only Tier 1 startups with AppSec teams would benefit)
- FDA publishes concrete threat modeling guidance (not yet finalized)

---

## Component-Level Scope Definition

For maintainers: each component has a clear scope.

### PCCP Generator
- **In scope**: Generate PCCP from YAML following FDA Dec 2024 guidance structure
- **Out of scope**: Validate that proposed changes are actually "predetermined" (requires domain expertise); integrate with ML pipeline (different layer)

### Model Card Generator
- **In scope**: Generate clinical-context model cards with FDA fields (predicate, subpopulation perf, bias)
- **Out of scope**: Train models or run evaluation (data science layer); advise on bias mitigation strategies (science layer)

### Cybersecurity SBOM Generator
- **In scope**: Auto-generate NTIA-format SBOM from software component inventory
- **Out of scope**: Vulnerability scanning (use OWASP CycloneDX tools), threat modeling, mitigation recommendations

### Bias Report Generator
- **In scope**: Organize demographic performance data (sensitivity, specificity, AUC by subgroup) into FDA-expected format
- **Out of scope**: Run bias evaluation (data science layer), recommend mitigation strategies

### Real-World Monitoring Plan Generator
- **In scope**: Define data sources, metrics, thresholds, escalation procedures
- **Out of scope**: Build monitoring infrastructure, integrate with EHR systems

### eSTAR Package Builder
- **In scope**: Organize generated documents into eSTAR folder structure and manifest
- **Out of scope**: Upload to FDA eSubmitter (user responsibility), fill out FDA forms beyond what package generator can infer

### IEC 62304 + ISO 14971 Templates
- **In scope**: Integrate OpenRegulatory templates into toolkit (follow component pattern)
- **Out of scope**: Train users on software lifecycle v. design process (educational; covered in guides)

---

## API Stability and Breaking Changes

Through v1.0:
- **YAML schemas** are considered unstable; breaking changes allowed with semver minor bump (e.g., v0.2 -> v0.3)
- **CLI subcommands** are considered public API; breaking changes require major version bump (e.g., v0.x -> v1.0)
- **Python module imports** (e.g., `from fda_samd_toolkit.generators import pccp`) are public API; breaking changes require major version bump

---

## Cutoff Criteria: When to Say "No" to a Request

Contributors and users will ask for features outside this scope. Use this decision tree:

1. **Is it FDA-guidance-backed or industry-standard?**
   - No -> Consider as enhancement proposal, evaluate via "adjacent" gate
   - Yes -> Proceed to gate 2

2. **Do 50%+ of personas benefit?**
   - No -> Suggest as community extension or future v1.1+ feature
   - Yes -> Proceed to gate 3

3. **Can it be implemented in <2 weeks following existing component pattern?**
   - No -> Suggest breaking into smaller issues or future release
   - Yes -> Proceed to gate 4

4. **Does it fit existing component structure or add new component?**
   - New component and >4 weeks effort -> Defer to v0.3 or later
   - New component and <4 weeks -> Consider for v0.2+ if backlog allows
   - Fits existing component -> Prioritize immediately

Example rejections:
- "Can we generate sample training data?" (Data science, not scaffolding)
- "Can we integrate with our EHR API?" (Infrastructure, not templates)
- "Can we support De Novo submissions?" (Deferred to post-v1.0; requires new predicate logic)
