# Getting Started

This guide will get you from zero to your first PCCP in 5 minutes. For deeper dives into each component, see the [Guides](guides/pccp-generator.md) section.

---

## Installation

### Requirements

- Python 3.11 or 3.12
- pip or uv

### Install the Package

```bash
pip install fda-samd-toolkit
```

Or with uv:

```bash
uv pip install fda-samd-toolkit
```

Verify installation:

```bash
fda-samd --version
fda-samd --help
```

---

## Your First PCCP (5 Minutes)

### Step 1: Create a Config File

Create `my_device.yaml` in your project directory:

```yaml
device_name: "AI ECG Analysis System"
device_class: "Class II"
intended_use: |
  Automated analysis of 12-lead electrocardiograms to detect
  atrial fibrillation, ventricular ectopy, and bradycardia in
  hospital and ambulatory settings.

model_info:
  architecture: "ResNet-50 pretrained, fine-tuned"
  training_data_size: 150000
  training_data_sources:
    - "MIMIC-III (open)"
    - "Hospital A ECG archives (proprietary)"
  performance:
    - metric: "sensitivity"
      value: 0.96
      sub_populations:
        - "age 18-45": 0.94
        - "age 65+": 0.95
    - metric: "specificity"
      value: 0.94

change_control:
  - category: "retraining"
    description: "Monthly model retraining on new patient data"
    frequency: "monthly"
    impact: "Performance drift detection"
  - category: "input_data"
    description: "Support for new ECG hardware formats"
    frequency: "as_needed"
    impact: "Signal preprocessing changes"
```

### Step 2: Generate the PCCP

```bash
fda-samd pccp generate --config my_device.yaml --output PCCP.md
```

This creates `PCCP.md` with FDA-aligned sections:
- Device classification and intended use
- Algorithm overview
- Training data characterization
- Performance documentation
- Change control procedures
- Monitoring and retraining triggers

### Step 3: Validate Completeness

```bash
fda-samd pccp validate --file PCCP.md
```

Output:

```
PCCP Validation Report
======================
Overall Completeness: 94%

Critical Issues:
  (None)

Warnings:
  ⚠ Clinical sub-population performance: Limited documentation
    Recommendation: Add performance breakdown by age, sex, device type

Sections Status:
  ✓ Device Classification
  ✓ Intended Use
  ✓ Algorithm Overview
  ✓ Training Data Characterization
  ✓ Performance Documentation
  ✓ Change Control Plan
  ✓ Monitoring Plan
  ✓ Performance Thresholds
  ✓ Retraining Procedures
  ✓ Documentation
```

### Step 4: Customize and Review

The generated PCCP is a complete draft. Now:

1. **Review for accuracy**: Verify all device, algorithm, and performance details are correct
2. **Fill placeholders**: The generator leaves `[PLACEHOLDER]` marks where you need device-specific details
3. **Add sub-population data**: If you have performance breakdowns by age, sex, comorbidities, add them
4. **Document your process**: Link to your training pipeline, validation protocols, monitoring systems

### Step 5: Get Regulatory Review

**Important**: Have a qualified regulatory affairs professional review your PCCP before submission. This toolkit generates a scaffold, not a submission-ready document.

---

## What's Next?

Now you have a PCCP template. Depending on your device, you may also need:

### Need a 510(k) Submission?

See [510(k) Templates](guides/510k-templates.md) for:
- Indications for Use section
- Device Description with ML/AI specifics
- Substantial Equivalence and predicate device analysis
- Predicate Performance table

### Need to Document Your Model?

See [Model Cards](guides/model-cards.md) for:
- FDA-specific model card fields
- Data characterization (provenance, demographics, limitations)
- Performance documentation across sub-populations
- Monitoring and drift detection procedures

### Need a Clinical Validation Study?

See [Validation Framework](guides/validation-framework.md) for:
- Study design templates (RCT, observational, real-world)
- Sample size calculation scaffolding
- Sub-population analysis plans
- Statistical analysis outlines

### Ready to Submit?

See [Readiness Checklist](guides/checklist.md) for:
- Pre-submission gap analysis
- Completeness scoring across 9 domains
- Section-by-section checklist

---

## Common Questions

**Q: Is the generated document ready to submit to FDA?**

A: No. The generated document is a scaffold that you customize with your device-specific details, clinical data, and regulatory strategy. Always have a qualified regulatory affairs professional review before submission.

**Q: Can I use this for De Novo or PMA submissions?**

A: v0.1 focuses on PCCP (post-market change control). De Novo and PMA pathways require additional sections. Check the [roadmap](https://github.com/lal-jaouni/fda-samd-toolkit#roadmap) for future versions.

**Q: How do I add my own templates?**

A: See [Contributing](contributing.md). The toolkit uses Jinja2 templates. You can customize the template directory or contribute back publicly.

**Q: What if my device is a novel classifier (not retraining)?**

A: A PCCP applies to devices that may change after approval (retraining, performance monitoring, etc.). If your algorithm is locked and never changes, you may not need a PCCP. Consult with FDA or your regulatory team.

**Q: Does this toolkit handle IEC 62304 compliance?**

A: Not yet. v0.2+ will add IEC 62304 (medical device software lifecycle) mapping. Currently, the toolkit focuses on FDA AI/ML-specific guidance.

---

## Troubleshooting

### Command Not Found: `fda-samd`

Make sure the package is installed and in your Python environment:

```bash
pip show fda-samd-toolkit
```

If it shows the package but the command fails, try:

```bash
python -m fda_samd_toolkit.cli --help
```

### YAML Parse Error

Check your YAML syntax. Common issues:
- Strings with colons need quotes: `"device: v2"`
- Indentation must be spaces, not tabs
- Lists use `-` with a space: `- item`

### Validation Reports Too Many Warnings

Warnings are expected for alpha releases. Focus on critical issues first. See [PCCP Generator Guide](guides/pccp-generator.md) for how to address common gaps.

---

## Next Steps

1. **Understand the FDA landscape**: Read [FDA SaMD Overview](concepts/fda-overview.md)
2. **Learn PCCP concepts**: See [What is a PCCP?](concepts/pccp-explained.md)
3. **Deep dive into components**: Check [Guides](guides/pccp-generator.md)
4. **Contribute**: Help improve templates and examples. See [Contributing](contributing.md)

For questions or issues, [open a GitHub issue](https://github.com/lal-jaouni/fda-samd-toolkit/issues).
