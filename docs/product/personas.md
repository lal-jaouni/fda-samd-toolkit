# FDA SaMD Toolkit User Personas

These personas represent the three core user segments for the FDA SaMD Toolkit, grounded in user research and real consulting candidate profiles.

## Persona 1: AI/ML Startup CTO (Primary)

**Name:** Alex, Chief Technology Officer  
**Company stage:** Series A-funded AI/ML healthcare startup ($2-10M raised)  
**Team size:** 5-15 engineers, 1-2 regulatory hires  
**Timeline:** 8 weeks to first FDA 510(k) submission  
**Prior FDA experience:** None; CEO hired external regulatory consultant 3 months ago

### Profile

Alex leads technical strategy for a cardiac AI startup that has built an ECG-based arrhythmia detection algorithm and validated it across a 5,000-patient retrospective study. The algorithm achieves 98% sensitivity/specificity on held-out test sets. The company has identified a predicate device (Eko Health's cleared algorithm) and is now mapping the submission package.

Regulatory consultant (hired at $250/hr) is requesting structured inputs: model documentation, training data lineage, validation protocol, cybersecurity architecture, bias analysis by demographics, and a PCCP for future algorithm updates. The consultant estimates 8 weeks to submission-ready package.

### What They Do Today (Without Toolkit)

- CTO spends 40-60 hours assembling regulatory scaffolding from scratch using generic Word templates and FDA guidance PDFs
- Regulatory consultant generates custom Markdown/Word documents at $300-500/hr billing
- No version control on regulatory documents; collaboration happens via email and shared Google Docs
- Manual cross-referencing between model card, PCCP, and validation protocols creates inconsistencies
- Team discovers gaps during FDA pre-submission meeting because internal processes weren't validated against actual guidance

### What They'd Do With Toolkit

- Use toolkit YAML configs to define model, training data, validation plan, bias thresholds, and PCCP all in one place
- Generate submission-ready Markdown that tracks to FDA guidance automatically
- Cut consultant hours from 120 to 40 by having CTO pre-populate structured templates
- Version control regulatory docs alongside source code (git-tracked YAML + outputs)
- Run toolkit's readiness checklist 4 weeks before submission to catch gaps early
- Integrate toolkit into CI/CD to regenerate docs when algorithm parameters change
- Customize Model Card and PCCP templates for imaging AI pipeline (secondary indications coming later)

### Frustration List

1. Regulatory consultants are expensive (>$300/hr) and act as gatekeepers on basic documentation format
2. FDA guidance PDFs are dense and lack worked examples; teams waste time interpreting intent
3. No standard open-source way to document AI/ML submissions; every startup reinvents the wheel
4. Cybersecurity SBOM and bias evaluation seem mandatory but no free templates exist
5. Version control of regulatory docs is painful; changes to algorithm require manually updating 5+ documents
6. eSTAR format requirements are opaque; Cruxi charges per-submission to handle formatting
7. Validation protocols are template-heavy boilerplate; high effort, low value-add
8. No integration between model card and PCCP; must manually sync changes

### Why They'd Recommend It

"Our startup went from 120 consultant hours to 40 because we had structured templates in the toolkit. We caught bias issues in week 3 instead of FDA round 2. The PCCP generator saved 2 weeks of back-and-forth on change control rules. Every AI startup filing 510(k) should use this."

### Frequency of Use

- Intensive: weeks 1-12 (before and during 510(k) prep, multiple daily)
- Maintenance: post-submission (quarterly for PCCP updates, quarterly for real-world monitoring plans)
- Expected value unlock: 40-60 hours of consultant time saved, $15-20K cost reduction, 2-4 week acceleration

**Example companies (Tier 1 consulting candidates):** Cardiosense (ECG+PPG wearable AI pipeline), Salomatic (cardiac medication AI), Anumana (multi-indication ECG-AI post-first-clearance)

---

## Persona 2: Regulatory Consultant (Secondary)

**Name:** Dr. Jordan, Principal Regulatory Affairs Specialist  
**Company type:** Boutique regulatory consulting firm  
**Client portfolio:** 3-5 concurrent medical device clients (mix of startup, mid-market, private equity-backed)  
**Billing model:** $250-400/hr + per-submission project rates; typical engagement $40-150K per 510(k)  
**Prior FDA experience:** 12 years, 40+ 510(k) and 3 PMA submissions; deep expertise in device classes

### Profile

Jordan runs regulatory strategy for a consulting firm that specializes in AI/ML medical device submissions. Clients range from Series A startups ($2-10M raised, 1-2 regulatory hires) to established medtech companies (500+ employees, mature QMS) launching new AI features. Jordan's practice focuses on cardiac, imaging, and diagnostic AI.

Each client engagement requires standardizing deliverables (model cards, validation protocols, risk analysis, PCCP) while customizing for device class, indication, and predicate device. Jordan currently uses a mix of Word templates, home-grown Python scripts for PCCP formatting, and manual cross-checks.

### What They Do Today (Without Toolkit)

- Start each engagement with 20-40 hours of bespoke template assembly and client customization
- Maintain private GitHub repos with 50+ Word/Markdown template variants (one per device class)
- Write custom Python script per project to cross-validate model card and PCCP sections
- Manually transcribe regulatory requirements into client-specific language
- Bill template assembly as part of project scope; clients have no visibility into reusable vs. custom work
- Struggle with version control when clients modify templates mid-engagement
- Re-educate each new client on FDA AI/ML guidance structure (repeated 3-5 times per year)

### What They'd Do With Toolkit

- Use toolkit as baseline and customize only the device-class-specific and company-specific sections
- Standardize YAML inputs across all clients; templates become company IP, not toolkit IP
- Build custom extensions for specialized domains (e.g., closed-loop, adaptive AI) on top of toolkit
- Embed toolkit in advisory services ("We recommend using FDA SaMD Toolkit as scaffolding; our value is science interpretation and FDA strategy")
- Generate client proposal materials using toolkit (e.g., "Here's what your submission structure will look like")
- Train clients to maintain their own regulatory docs post-submission (lower ongoing support burden)
- Package toolkit customizations into productized service ("FDA AI/ML submission prep: $25K", down from $80-150K consultant-heavy approach)

### Why They'd Adopt (And Why They Might NOT)

**Reasons to adopt:**
- Frees up 100+ consultant hours/year (expensive time) to focus on high-value strategy and FDA negotiation
- Improves client outcomes (fewer resubmissions due to gaps caught upfront)
- Creates marketing differentiation ("We use the open-source FDA SaMD Toolkit plus 12 years of regulatory strategy")
- Reduces delivery risk (toolkit templates validated against FDA guidance; less custom code)

**Reasons to NOT adopt:**
- Toolkit commoditizes basic regulatory scaffolding (reduces billable hours for template assembly)
- Open-source adoption suggests consultant is not adding unique value (myth, but perception barrier)
- Customization and validation effort to integrate toolkit into practice may exceed initial savings (needs buy-in from leadership)
- Risk of client discovering toolkit independently and thinking they no longer need consulting ("Why pay you $150K if I can use the open-source tool for free?")

### Frustration List

1. Template assembly is repetitive busywork, not high-value strategy work
2. FDA guidance updates (Dec 2024, Jan 2025, June 2025) force re-training on new requirements every quarter
3. Clients expect consultants to "just know" the latest FDA AI/ML expectations (no public data on what's being approved)
4. SBOM, bias evaluation, and monitoring plans are mandated by FDA but no standard templates exist
5. eSTAR format is vendor-specific and opaque; must teach clients or use paid tools (Cruxi)
6. Version control of regulatory docs across client orgs is a nightmare
7. Predicate device mapping is manual; no tool helps identify / compare cleared devices
8. Subpopulation performance documentation lacks templates; every firm rebuilds this from scratch

### Why They'd Recommend It

"The FDA SaMD Toolkit accelerated our client engagements by 30% and improved submission quality. We now position ourselves as 'science and FDA strategy partners' instead of 'template vendors.' Clients get faster turnaround and better outcomes because we spend time on what matters: device science and FDA negotiation."

### Frequency of Use

- High intensity: each new client engagement (4-8 weeks, daily)
- Ongoing: quarterly FDA guidance monitoring, annual template updates
- Expected value unlock: 100-150 billable hours/year freed for higher-value work, improved client retention, faster engagement cycles

**Example companies (Tier 1-2 consulting candidates):** Eko Health (actively hiring Director Global Regulatory Affairs), Cleerly (hiring Principal RA Specialist), NeoSoft LLC (hiring RA specialist)

---

## Persona 3: Hospital Innovation Team (Tertiary)

**Name:** Dr. Sam, Director of AI & Innovation  
**Organization:** 500-bed academic medical center  
**Team:** 2-3 clinical informaticists, 1 data scientist, 0.5 FTE regulatory/compliance  
**Timeline:** 12-18 months to pilot-to-deployment decision  
**Prior FDA experience:** None; hospital QMS exists for devices but not for software-as-medical-device (SaMD)

### Profile

Sam leads a clinical innovation lab that partners with data science teams to pilot AI tools for patient care: ECG-based triage, chest X-ray interpretation, EHR-based sepsis prediction. The lab has published 2 retrospective validation studies (500-2000 patient cohorts) and is now evaluating whether tools should transition to clinical deployment.

Deployment requires hospital governance approval: IRB review, IT security sign-off, clinical validation plan, and documentation that the tool meets FDA SaMD expectations (even if not formally submitted to FDA). Sam's institution has never submitted an FDA 510(k) and has minimal regulatory expertise.

### What They Do Today (Without Toolkit)

- Clinical team publishes retrospective validation study; lab director assumes FDA compliance is "someone else's problem"
- IT security team requires cybersecurity documentation; hospital uses generic vendor templates (not AI-specific)
- Hospital legal/compliance asks "do we need FDA 510(k)?" (ambiguous; depends on indications, control of algorithm, etc.)
- No structured validation protocol exists; clinicians assume "we published it so it's validated"
- Bias evaluation and subpopulation analysis are not part of clinical research workflow
- Real-world monitoring plan is assumed to be covered by EHR logging; no structured approach
- Governance approval takes 6-12 months due to lack of clear documentation and regulatory framework
- If toolkit did not exist: might file FDA 510(k) based on consultant recommendations, but no clear path

### What They'd Do With Toolkit

- Use toolkit's Clinical Validation Framework to structure retrospective study analysis (modality guidance for imaging/signals/NLP)
- Generate Submission Readiness Checklist early (6-12 months before deployment) to identify gaps in validation, bias analysis, monitoring
- Use Model Card template to document algorithm behavior, subpopulation performance, and drift sensitivity with hospital governance
- Generate SBOM and cybersecurity documentation to satisfy IT security reviews
- Determine whether tool qualifies as SaMD or falls under 21 CFR 860.3 (general wellness exemption) with toolkit guidance
- If SaMD submission is indicated, use toolkit to generate FDA-ready documentation for consultant review (reduce consulting costs from $50K to $10K for fine-tuning)
- Set up real-world monitoring plan before deployment (using toolkit template) instead of retrofitting post-launch
- Train clinical staff on algorithm limitations and bias considerations using toolkit outputs

### Frustration List

1. FDA SaMD classification is unclear; hospital doesn't know if tool requires 510(k) or exemption
2. Clinical validation for AI is different from device validation; no local expertise
3. Bias evaluation is required by hospital governance but no standard template exists
4. Real-world monitoring is ad-hoc; no structured approach or escalation procedures
5. Cybersecurity SBOM is new requirement; hospital has no template for AI software
6. Regulatory consultants are expensive ($250+/hr) and assume commercial device knowledge (not hospital context)
7. No integration between clinical research (IRB) and regulatory (FDA) timelines
8. Staff turnover means regulatory knowledge is lost; no documented process

### Why They'd Recommend It

"The toolkit answered questions our hospital was asking but nobody could answer: What does FDA expect from our ECG algorithm? Are we validating this correctly? What about bias and real-world monitoring? We used the toolkit as a governance framework before deciding whether to file 510(k). Cut our consulting costs by 80% and enabled our clinical team to own the validation process instead of waiting for external consultants."

### Frequency of Use

- Moderate intensity: 6-12 months during pilot validation and governance approval (2-5 hrs/week)
- Post-deployment: quarterly monitoring plan review and documentation updates
- Expected value unlock: $40-80K consulting cost avoidance, clearer governance path, faster deployment decisions, safer real-world monitoring

**Example organizations:** Large academic medical centers (UCSF, Johns Hopkins, Mayo Clinic) and large integrated delivery networks (Kaiser Permanente, Cleveland Clinic, Geisinger) with AI innovation labs but no internal regulatory expertise

---

## Persona Cross-Summary

| Aspect | CTO (Primary) | Consultant (Secondary) | Hospital (Tertiary) |
|--------|---------------|------------------------|---------------------|
| Primary use case | Build first 510(k) submission | Standardize across clients | Validate tool for deployment |
| Effort saved | 40-60 consultant hours | 100-150 billable hours/year | $40-80K consulting, 6-12 months |
| Risk if not adopted | Missed FDA gaps, budget overruns | Loss of agility, staff burnout | Unclear governance, unsafe deployment |
| Adoption barrier | Preference for consultant-led process | Commoditization fear | Regulatory risk aversion |
| Time horizon | 8-12 weeks intensive use | Continuous, quarterly spikes | 12-18 months moderate use |
