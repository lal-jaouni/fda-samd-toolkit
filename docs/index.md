# FDA SaMD Toolkit

## Regulatory scaffolding for AI/ML medical devices. In minutes, not months.

Building an AI/ML system for healthcare? You'll submit to FDA. That submission requires 40+ pages of regulatory documentation that doesn't exist in any open-source form. A regulatory consultant costs $300-500/hr. This toolkit generates the scaffolding in minutes.

The **FDA SaMD Toolkit** is open-source tooling for AI/ML medical device submissions. It ships with:

- **PCCP Generator**: Build FDA Predetermined Change Control Plans from a YAML config (Dec 2024 guidance, final)
- **510(k) AI/ML Templates**: Sections on intended use, performance validation, training data characterization
- **Model Cards**: Clinical-context model documentation that addresses FDA-specific concerns
- **Validation Framework**: Protocol templates for pre-deployment clinical validation studies
- **Readiness Checker**: Pre-submission gap analysis against FDA requirements

No generated document is complete without regulatory review. But you won't start from a blank page anymore.

---

## Who This Is For

**AI/ML Startup**
: Preparing your first FDA submission? This toolkit gives you templates for the 8-10 regulatory documents you actually need, saving 20-30 hours of research and standardization work. Iterate on your product, not compliance boilerplate.

**Regulatory Consultant**
: Tired of rebuilding the same templates for every client? Version your deliverables here. Contribute examples and scenarios. Build competitive advantage through faster turnaround.

**Hospital Innovation Team**
: Piloting an AI tool? This toolkit helps you document validation and operational safety the way FDA expects to see it, whether you're pursuing formal clearance later or just need evidence for IRB.

**Researcher**
: Translating your ML research into clinical deployment? PCCP, model card, and validation sections map your methodology to FDA language. Bridges the gap between academic and regulatory worlds.

---

## What You Get (v0.1)

```
PCCP Generator
├── YAML configuration interface
├── FDA Dec 2024 guidance alignment
├── Section completeness validation
└── Markdown + PDF export

510(k) Templates
├── Indications for Use
├── Device Description (with ML/AI specifics)
├── Substantial Equivalence (predicate device analysis)
└── Placeholder system for easy customization

Model Cards
├── FDA-specific metadata (sub-populations, drift monitoring)
├── Data characterization
├── Performance documentation
└── Limitations and assumptions

Validation Framework
├── Study design templates (RCT, observational, real-world)
├── Sample size calculation stubs
├── Sub-population analysis scaffolding
└── Statistical analysis plan outlines

Readiness Checker
├── Submission checklist against FDA AI/ML guidance
├── Gap analysis across 9 regulatory domains
└── Section-by-section completeness score
```

See [the README](https://github.com/lal-jaouni/fda-samd-toolkit) for current component status.

---

## Quick Start (5 Minutes)

### 1. Install

```bash
pip install fda-samd-toolkit
fda-samd --version
```

### 2. Create a PCCP Config

```yaml
# my_device.yaml
device_name: "Cardiac Arrhythmia Monitor v2"
intended_use: |
  AI/ML algorithm for real-time detection of atrial fibrillation
  from ECG waveforms in continuous monitoring.

model_info:
  type: "neural_network"
  training_data_size: 50000
  performance:
    - metric: "sensitivity"
      value: 0.94
      sub_populations:
        - "age>65": 0.91
        - "females": 0.93

changes:
  - category: "retraining"
    description: "Quarterly model retraining on new patient cohorts"
    frequency: "quarterly"
  - category: "data_drift"
    description: "ECG preprocessing changes to handle new hardware"
    frequency: "as_needed"
```

### 3. Generate PCCP

```bash
fda-samd pccp generate --config my_device.yaml --output PCCP.md
```

### 4. Validate

```bash
fda-samd pccp validate --file PCCP.md
```

Output:
```
PCCP Validation Report
======================
Overall Completeness: 92%

Issues Found:
  ⚠ Clinical validation section missing sub-population performance breakdown
  ⚠ Data drift monitoring procedure needs failure thresholds

Sections (9/10 complete):
  ✓ Device Classification
  ✓ Intended Use
  ✓ Algorithm Overview
  ✓ Training Data Characterization
  ✓ Performance Documentation
  ✓ Change Categories
  ...
```

Your generated PCCP is now ready for regulatory review.

**Next**: Check out [Getting Started](getting-started.md) for installation, working examples, and where to go from here.

---

## Why This Toolkit Exists

The problem is real:

- **FDA PCCP Guidance (Dec 2024)**: 25 pages of regulatory requirements. Zero templates. Every company reinvents it.
- **AI/ML 510(k) Sections**: Intended use, performance validation, training data characterization. No public examples exist.
- **Model Cards**: Mitchell et al. 2019 standard is excellent for ML. But it doesn't address FDA's concerns (sub-population drift, monitoring thresholds, retraining triggers).
- **Regulatory Debt**: Startups spend 200-300 hours on documentation that could be scaffolded in 2 hours.

We're open-sourcing that scaffolding so:

1. **Small teams ship faster** without paying regulatory consultants $300/hr for boilerplate
2. **The FDA gets better submissions** with consistent, thoughtful documentation
3. **The regulatory AI/ML community standardizes** around evidence-based best practices

---

## How to Use These Docs

- **New to FDA SaMD?** Start with [FDA SaMD Overview](concepts/fda-overview.md). 15-minute primer on 510(k) vs De Novo vs PMA, and why AI/ML devices need extra scrutiny.

- **Want to build a PCCP?** Go to [PCCP Generator](guides/pccp-generator.md). Step-by-step walkthrough with real examples.

- **Implementing 510(k) sections?** See [510(k) Templates](guides/510k-templates.md) for what FDA expects and how to fill each section.

- **Building a model card?** [Model Cards](guides/model-cards.md) explains FDA-specific metadata, sub-population analysis, and monitoring frameworks.

- **Designing a clinical validation study?** [Validation Framework](guides/validation-framework.md) walks you through study design, sample size, and statistical analysis.

- **Running the readiness checker?** [Readiness Checklist](guides/checklist.md) shows how to run gap analysis before your submission.

- **Contributing?** See [Contributing](contributing.md) for how to add templates, examples, or fix docs.

---

## Disclaimer

This toolkit generates document scaffolding. It is **not legal, regulatory, or medical advice**. Every FDA submission requires review by qualified regulatory professionals (RA, QA, legal). Generated documents are starting points, not finished products. Customize thoroughly to your specific device, intended use, clinical context, and patient population.

The maintainers assume no liability for submissions made using this tool.

---

## License

MIT. Use freely in commercial products. Attribution appreciated but not required.

---

## Acknowledgments

Built on:

- [FDA AI/ML Action Plan (2021)](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-software-medical-device)
- [FDA PCCP Final Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [IMDRF SaMD Framework](https://www.imdrf.org/working-groups/software-medical-device-samd)
- [Mitchell et al. 2019: Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)
- [IEC 62304: Life Cycle Processes for Medical Device Software](https://en.wikipedia.org/wiki/IEC_62304)

---

Ready? [Get started.](getting-started.md)
