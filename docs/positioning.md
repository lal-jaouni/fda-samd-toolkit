# FDA SaMD Toolkit: Product Positioning

## Executive Summary

The FDA SaMD Toolkit solves the regulatory scaffolding problem for AI/ML medical device teams. It transforms FDA guidance (PCCP, 510(k) AI/ML sections, model cards, clinical validation frameworks) into reusable templates and automated generators, cutting weeks of busywork to hours.

This document defines the three primary user personas, success metrics, anti-features, and v1.0 vision.

## Primary Personas

### Persona 1: AI/ML Startup CTO (Primary Target)

**Profile:**
- CTO or VP Engineering at pre-Series-B AI/ML healthcare startup (typically 5-20 person team)
- 8 weeks from first FDA 510(k) submission (often 16 weeks actually, but perceives the clock as shorter)
- Technical background (ML, software architecture) but limited FDA regulatory experience
- Has an excellent product; has no idea how to talk to FDA about it
- Primary constraint: time (not money; team is well-funded or venture-backed)

**Current State (without toolkit):**
- Hires regulatory consultant ($125-400/hr, ~$10-20K per submission)
- Consultant spends weeks assembling templates from scratch, prior submissions, and FDA guidance
- CTO's team learns FDA-specific terminology (PCCP, substantial equivalence, predicate device, GMLP)
- Regulatory feedback loop is slow (consultant writes drafts, CTO/founders revise, FDA comments, iterate)
- Team wants to move fast but doesn't know the regulatory baseline

**With Toolkit:**
- CTO reviews toolkit examples and documentation (2-4 hours)
- Team fills in YAML configs for their device (device name, intended use, training data, validation metrics)
- Runs `fda-samd pccp generate` and `fda-samd model-card generate` (5 minutes)
- Generated documents become the baseline for consultant review (or consultant is entirely optional for simple submissions)
- Team focuses on science (validation study design, performance analysis) instead of document formatting
- Roadmap becomes predictable: submission artifact generation, clinical validation, FDA pre-submission meeting

**Success Metric for This Persona:**
- Uses toolkit to generate 80% of PCCP and model card (consultant touches up edge cases)
- Reduces pre-submission artifact time from 4-6 weeks to 1-2 weeks
- Regulatory team is smaller (part-time consultant instead of full-time RA hire)

**Value Proposition:**
- Speed: Hours to generate scaffolding, not weeks
- Completeness: Don't miss FDA requirements (checklist catches them)
- Confidence: Built on actual FDA guidance (Dec 2024 PCCP, Jan 2025 AI/ML Lifecycle), not consultant opinions

---

### Persona 2: Regulatory Consultant / RA Director (Secondary Target)

**Profile:**
- Regulatory Affairs (RA) consultant with 10+ years experience
- Works with 2-5 AI/ML device clients per year
- Currently writes all submission documents from scratch or from personal template archives
- Wants to standardize deliverables and reduce billable hours on boilerplate
- May eventually productize deliverables or build an internal tool
- Primary constraint: time (limited by billable hours); secondary constraint is client differentiation

**Current State (without toolkit):**
- Maintains personal document templates across Google Drive, Word, SharePoint
- For each client, customizes templates, ensures FDA compliance, manages versions
- Spends 30-40% of project time on non-differentiating regulatory scaffolding
- Hard to share learnings with team (templates are personal)
- Struggles to keep up with FDA guidance updates (Dec 2024 PCCP, Jan 2025 AI/ML, June 2025 Cybersecurity)

**With Toolkit:**
- Uses toolkit templates as baseline for all clients
- Customizes only device-specific sections (IFU, device name, training data, performance metrics)
- Toolkit examples show best practices (CardioGuard ECG-AI demonstrates all sections working together)
- Updates toolkit as FDA guidance changes (subscribes to GitHub releases)
- Standardized artifacts reduce scope creep and enable faster reviews
- Can offer "FDA-aligned submission package" as differentiated service

**Success Metric for This Persona:**
- 20-30% reduction in billable hours per submission (template baseline, not custom writing)
- Higher client NPS (faster delivery, lower cost, confidence in regulatory alignment)
- Ability to take on 1-2 additional clients per year with same staffing

**Value Proposition:**
- Standardization: Same baseline for all clients, faster customization
- Regulatory authority: Toolkitrepresents actual FDA guidance, not consultant opinions (builds credibility with clients)
- Efficiency: More time on high-value strategy work (regulatory strategy, predicate device search, evidence planning) vs. boilerplate

---

### Persona 3: Hospital Innovation / Clinical Team (Tertiary Target)

**Profile:**
- Innovation director, digital health officer, or research scientist at health system
- Piloting AI tool internally (e.g., ECG AI for cardiology, imaging AI for radiology)
- Long-term goal may be to productize and submit to FDA, but not imminent (12+ months)
- Wants to understand regulatory landscape before investing in product dev
- Primary constraint: unclear ROI on AI tools and regulatory pathway
- Secondary constraint: limited digital health/regulatory expertise on staff

**Current State (without toolkit):**
- Runs AI tool internally with disclaimer ("For research use only")
- Unclear on pathway to clinical validation and FDA submission
- Hires external consultant for strategic advice (expensive, slow)
- Risk of falling into compliance gap if tool gains adoption without proper governance

**With Toolkit:**
- Reviews toolkit documentation and worked examples to understand FDA landscape
- Uses validation framework to design internal pilot studies
- Builds business case for productization (knows regulatory costs, timeline, effort upfront)
- Makes informed decision: submit to FDA, license to medtech vendor, or keep internal only
- If pursuing FDA pathway, toolkit becomes baseline for submission work (possibly with external RA partner)

**Success Metric for This Persona:**
- 80% clarity on FDA regulatory pathway within 1 week (vs. 4-6 weeks consulting engagement)
- Informed business decision on whether to pursue FDA submission (vs. vaporware or accidental non-compliance)

**Value Proposition:**
- Clarity: FDA pathway is documented, not mysterious
- Speed: Understand regulatory landscape before hiring consultants
- Risk reduction: Avoid building compliance debt that becomes expensive to fix later

---

## Success Metrics & Targets

### 3 Months (by July 2026)

- **GitHub stars:** 100+ (indicates awareness in regulatory community)
- **PyPI downloads:** 50/month (sustained adoption beyond initial launch)
- **GitHub issues opened by external users:** 5+ (signals real usage and engagement)
- **Real-world trial:** 1 startup reports using toolkit for actual 510(k) (via community outreach)

### 6 Months (by October 2026)

- **GitHub stars:** 300+
- **PyPI downloads:** 200/month
- **Public mention:** Toolkit cited in 1 public blog post, regulatory conference, or professional community (KevinMD, Hacker News, Product Hunt, RAPS)
- **Consultant partnerships:** 2-3 RA consultants publicly using toolkit for client work
- **v0.2 adoption:** 5+ downloads per month of v0.2 features (SBOM, bias evaluation)

### 12 Months (by April 2027)

- **GitHub stars:** 500+
- **PyPI downloads:** 300-500/month
- **Real submissions:** 1-2 publicly documented 510(k) submissions citing toolkit
- **Consultant ecosystem:** 3-5 RA consulting firms standardizing on toolkit
- **Contributed examples:** 2-3 additional worked examples submitted by community (imaging, NLP, multimodal)
- **Industry recognition:** Mentioned in FDA guidance update or industry standards (RAPS, IMDRF, OpenRegulatory ecosystem)

### Success Signals Beyond Metrics

1. **RA professionals recommend it to colleagues** (community word-of-mouth)
2. **Toolkit GitHub issues shift from feature requests to domain questions** (signal of baseline completion)
3. **Consultant job postings list toolkit familiarity as preferred skill**
4. **Healthcare startups reference it in fundraising decks** as evidence of regulatory preparedness

---

## v1.0 Definition

v1.0 is "stable with complete worked examples for 3 device classes."

### Scope: Three Device Classes

Focused on highest-pain AI/ML categories (cardiology, imaging, clinical NLP):

1. **Cardiac/Biosignal AI** (e.g., ECG, PPG arrhythmia detection), CardioGuard ECG-AI (v0.1 complete)
2. **Medical Imaging AI** (e.g., CT/MRI/X-ray classification or segmentation), v0.2/v0.3 candidate
3. **Clinical NLP AI** (e.g., clinical note summarization, adverse event extraction), v0.2/v0.3 candidate

Each worked example demonstrates:
- Complete 510(k) section templates (IFU, device description, performance, risk analysis)
- PCCP with realistic retraining cadence and drift triggers
- Model card with subpopulation performance (by sex, age, race/ethnicity where applicable)
- Validation study design (sample size, adjudication protocol, performance targets)
- Checklist assessment (design controls, risk, software lifecycle, clinical evidence)

### Stability Criteria

1. **API Stability** - No breaking changes to CLI commands or Python API
2. **Template Completeness** - All 8 categories in submission checklist have associated templates or guidance
3. **Test Coverage** - >90% code coverage; >5 tests per major component
4. **Documentation** - All user guides have worked examples; no missing reference docs
5. **Regulatory Accuracy** - Templates reviewed against FDA guidance published through April 2027 (or latest at v1.0 release)

### Out of Scope for v1.0

- PMA (Premarket Approval) submissions (Class III devices), different regulatory pathway
- EU MDR submissions, beyond FDA scope
- 505(b)(2) drug approval interactions, pharmaceutical regulatory science
- Automated regulatory intelligence ingestion (FDA guidance auto-updates), planned for v2.0+
- Machine learning model fairness certification tools, out of scope; template-based guidance only
- Post-market surveillance data integration, planned for v2.0+

---

## Anti-Features: What the Toolkit Will NOT Do

1. **NOT Medical or Regulatory Advice** - Toolkit generates scaffolding and templates. Every submission must be reviewed by qualified regulatory professionals. Maintainers assume no liability for submissions using this toolkit.

2. **NOT Automated Submission Filing** - Toolkit does not auto-submit to FDA or generate eSTAR packages directly (as of v0.1). Manual review and eSTAR package assembly required. v0.2 will automate eSTAR assembly.

3. **NOT a Replacement for eQMS** - Toolkit generates submission documents, not quality management system artifacts (design history file, CAPA, audit trails). Recommend integrating with Greenlight Guru, Qualio, or OpenRegulatory eQMS tools.

4. **NOT AI Safety Certification** - Toolkit does not verify model safety, fairness, robustness, or adversarial resilience. It provides templates for documenting these assessments; actual analysis is the developer's responsibility.

5. **NOT Real-Time Monitoring** - Toolkit generates monitoring plans and drift detection strategies. Implementation and integration with production monitoring systems is the developer's responsibility.

6. **NOT Decision-Making Software** - Toolkit does not recommend predicate devices, estimate submission success probability, or advise on regulatory strategy. These decisions require domain expertise and are explicitly out of scope.

7. **NOT Global Regulatory Compliance** - Toolkit is FDA-focused (US 510(k) and De Novo pathways). EU MDR, PMDA, NMPA, and other regional frameworks are not covered in v1.0. May add in v2.0+.

---

## Competitive Positioning

### vs. Greenlight Guru / Qualio / eQMS Tools

**Toolkit advantage:** Specific to FDA AI/ML 510(k) submissions (PCCP generators, bias evaluation, validation frameworks). eQMS tools are generic QMS platforms; toolkit is domain-specific.

**eQMS advantage:** Integrated design history file (DHF), CAPA, audit management, document control. Toolkit does not cover QMS infrastructure.

**Recommendation:** Use toolkit for submission artifact generation; use eQMS for DHF and QMS governance. Both are complementary.

### vs. OpenRegulatory (Free IEC 62304 + ISO 14971 Templates)

**Toolkit advantage:** FDA-specific templates, PCCP generator, model cards, worked examples. OpenRegulatory is software lifecycle agnostic.

**OpenRegulatory advantage:** MIT-licensed, larger template library, industry-agnostic QMS templates. Toolkit focuses narrowly on FDA AI/ML.

**Recommendation:** Use OpenRegulatory for IEC 62304 + ISO 14971 templates (v0.2 will integrate these). Use toolkit for FDA 510(k) AI/ML-specific sections (which OpenRegulatory does not cover).

### vs. Cruxi (eSTAR Editor + Consultant Directory)

**Toolkit advantage:** Open source, no per-submission fees, automation of PCCP and model card generation. Cruxi is a service (eSTAR editor + human consultants).

**Cruxi advantage:** Hands-on human regulatory guidance, eSTAR editor with built-in compliance checks. Toolkit is DIY + self-service.

**Recommendation:** Toolkit for self-service, cost-effective submission artifacts. Cruxi for premium guided service and eSTAR submission handling.

### vs. Complizen (AI-Powered Regulatory Strategy)

**Toolkit advantage:** Open source, specific templates for FDA 510(k) sections, worked examples. Complizen is closed-source and strategy-focused.

**Complizen advantage:** Claims to guide regulatory strategy (predicate device selection, evidence planning). Toolkit is template-based.

**Recommendation:** Use toolkit for regulatory document generation. Use Complizen (or regulatory consultant) for strategy decisions. Both can be used together.

---

## Community & Contribution Strategy

### Target Contributors

1. **Regulatory Professionals** - Contribute real-world examples (anonymized), edge cases, lessons learned
2. **Healthcare AI Researchers** - Contribute modality-specific validation protocols (imaging, signals, NLP)
3. **Open-Source DevOps/MLOps** - Contribute CI/CD improvements, monitoring integrations, automated testing
4. **Healthcare Entrepreneurs** - Share their submission experience; identify gaps in toolkit

### Contribution Channels

- **GitHub Issues** - Feature requests, bug reports, worked example suggestions
- **Discussions** - Strategic conversations about v0.2+ roadmap, personas, success metrics
- **CONTRIBUTING.md** - Guidelines for submitting PRs, examples, and documentation
- **Conference Talks** - Annual update on toolkit adoption (target: RAPS 2026, Hacker News, Product Hunt)

### Long-Term Vision (v2.0+)

- **Regulatory Intelligence Integration** - Auto-update toolkit when FDA guidance changes
- **Predicate Device Search** - Auto-identify predicate devices from FDA 510(k) database
- **Evidence Planning Engine** - Recommend evidence sources and study designs based on device type
- **Post-Market Surveillance Integration** - Connect to real-world performance monitoring platforms
- **Global Regulatory Expansion** - EU MDR, PMDA, NMPA templates and guidance

---

## Quotes We Want Users to Say

(Aspirational; derived from personas and success metrics)

> "The toolkit gave us FDA 510(k) templates in 2 hours. Without it, we would have hired a consultant for 4 weeks."
>, CTO at cardiac AI startup, 8 weeks pre-submission

> "We use the toolkit as a baseline for every client project. It ensures we don't miss FDA requirements and gives clients confidence we're aligned with the latest guidance."
>, Regulatory consultant, 10+ years RA experience

> "The CardioGuard example showed us what a complete 510(k) looks like. Now we know whether our internal AI project should pursue FDA submission or stay research-only."
>, Hospital innovation director

> "The PCCP generator automatically generated our change control plan. We just filled in device-specific parameters. Saved us weeks."
>, Startup regulatory director

> "Open source FDA 510(k) templates. This is exactly what the community has been waiting for."
>, Healthcare AI researcher on Hacker News

---

## Metrics Dashboard (For Maintainers)

Track quarterly:
- GitHub stars (linear growth target: +200/quarter)
- PyPI downloads (linear growth target: +50/month each quarter)
- Community contributions (issues, PRs, discussions)
- Real-world submissions (crowdsourced via GitHub issues, Slack, community outreach)
- Regulatory guidance updates (monitor FDA website for new guidance; flag for toolkit updates)
- Consultant partnerships (track companies publicly using toolkit for client work)

See `/home/laith/workspaces/fda-samd-toolkit/ROADMAP.md` for tracking mechanism (GitHub milestones + labels).
