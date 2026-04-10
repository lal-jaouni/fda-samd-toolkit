# CLI Reference

Complete command-line reference for the FDA SaMD Toolkit.

---

## Installation

```bash
pip install fda-samd-toolkit
```

Verify:

```bash
fda-samd --version
fda-samd --help
```

---

## Top-Level Commands

```bash
fda-samd --help
fda-samd --version
fda-samd pccp --help
fda-samd model-card --help
fda-samd validation --help
fda-samd readiness-check --help
```

---

## PCCP Commands

### Generate PCCP

```bash
fda-samd pccp generate --config <config.yaml> --output <output.md> [options]
```

**Arguments**:
- `--config`: Path to YAML configuration file (required)
- `--output`: Path to output Markdown file (required)

**Options**:
- `--template`: Path to custom Jinja2 template (optional)
- `--pdf`: Also generate PDF version using wkhtmltopdf
- `--format`: Output format: markdown (default), json, yaml
- `--validate`: Validate config before generation (default: true)

**Examples**:

```bash
# Basic usage
fda-samd pccp generate --config device.yaml --output PCCP.md

# With PDF
fda-samd pccp generate --config device.yaml --output PCCP.md --pdf

# Using custom template
fda-samd pccp generate \
  --config device.yaml \
  --output PCCP.md \
  --template my_template.j2
```

### Validate PCCP

```bash
fda-samd pccp validate --file <pccp.md> [options]
```

**Arguments**:
- `--file`: Path to PCCP Markdown file (required)

**Options**:
- `--strict`: Fail on warnings (default: warnings only)
- `--output`: Output format: text (default), json, html
- `--save-report`: Save report to file (default: print to stdout)

**Examples**:

```bash
# Basic validation
fda-samd pccp validate --file PCCP.md

# Strict mode (fail on any warning)
fda-samd pccp validate --file PCCP.md --strict

# Save HTML report
fda-samd pccp validate --file PCCP.md --output html --save-report report.html
```

**Output**:

```
PCCP Validation Report
======================
Overall Completeness: 92%

Critical Issues:
  (None)

Warnings:
  ⚠ Sub-population performance: Missing specificity for age 65+
  ⚠ Failure thresholds: No timeline for rollback procedure

Sections:
  ✓ Device and Intended Use (100%)
  ✓ Algorithm Overview (100%)
  ✓ Performance Monitoring Plan (95%)
  [...]

Estimated FDA Review Time: 2-4 weeks (with minor gaps)
```

---

## Model Card Commands

### Generate Model Card

```bash
fda-samd model-card generate --config <config.yaml> --output <output.md> [options]
```

**Arguments**:
- `--config`: Path to YAML configuration file (required)
- `--output`: Path to output Markdown file (required)

**Options**:
- `--template`: Path to custom Jinja2 template
- `--format`: markdown (default), json

**Example**:

```bash
fda-samd model-card generate \
  --config model_config.yaml \
  --output model_card.md
```

### Analyze Model Card

```bash
fda-samd model-card analyze --file <model_card.md>
```

Performs automated checks:
- Completeness of sections
- Sub-population coverage
- Performance metric documentation
- Limitations and failure modes

**Example**:

```bash
fda-samd model-card analyze --file model_card.md
```

---

## Validation Framework Commands

### Design Validation Study

```bash
fda-samd validation design \
  --device-name "Device Name" \
  --study-type retrospective|prospective|rct \
  --condition "Clinical condition" \
  [options]
```

**Options**:
- `--study-type`: Type of validation study (default: prospective)
- `--condition`: Clinical condition being diagnosed
- `--sample-size`: Target N (default: auto-calculated)
- `--prevalence`: Expected condition prevalence (default: 0.30)
- `--output`: Output markdown file

**Example**:

```bash
fda-samd validation design \
  --device-name "AI-ECG Analyzer" \
  --study-type prospective \
  --condition "Atrial Fibrillation" \
  --sample-size 2000 \
  --prevalence 0.30 \
  --output study_protocol.md
```

### Sample Size Calculator

```bash
fda-samd validation sample-size \
  --null-hypothesis 0.90 \
  --alternative-hypothesis 0.94 \
  --significance 0.05 \
  --power 0.90 \
  --prevalence 0.30
```

**Arguments**:
- `--null-hypothesis`: Null sensitivity (device doesn't work)
- `--alternative-hypothesis`: Expected sensitivity
- `--significance`: Alpha level (typically 0.05)
- `--power`: Power to detect difference (typically 0.90)
- `--prevalence`: Expected disease prevalence

**Output**:

```
Sample Size Calculation
======================
Null sensitivity: 0.90
Expected sensitivity: 0.94
Significance level: 0.05
Power: 0.90
Disease prevalence: 0.30

Required N: 1832 total subjects
  - Disease positive: 550
  - Disease negative: 1282
  
(Add 5% for drop-outs): 1923 total subjects recommended
```

---

## Readiness Check Commands

### Run Full Readiness Check

```bash
fda-samd readiness-check \
  --pccp <pccp.md> \
  --model-card <model_card.md> \
  --510k <510k_submission.md> \
  [options]
```

**Options**:
- `--output`: Output file (default: readiness_report.html)
- `--verbose`: Verbose output with detailed recommendations

**Example**:

```bash
fda-samd readiness-check \
  --pccp PCCP.md \
  --model-card model_card.md \
  --510k submission.md \
  --output readiness_report.html
```

**Output**: Interactive HTML report with:
- Overall completeness score (0-100%)
- Section-by-section gaps
- Recommended fixes
- FDA review timeline estimate

### Check Individual Components

```bash
# Check just PCCP
fda-samd readiness-check --pccp PCCP.md --output pccp_report.html

# Check just model card
fda-samd readiness-check --model-card model_card.md
```

---

## Utility Commands

### Show Config Schema

```bash
fda-samd schema pccp
fda-samd schema model-card
fda-samd schema validation
```

Prints the YAML schema for configuration files.

**Example**:

```bash
fda-samd schema pccp
```

Output:

```yaml
device_name: string (required)
device_class: string (required) - "Class I", "Class II", or "Class III"
intended_use: string (required) - Multi-line description
model_info:
  architecture: string
  training_data_size: integer
  performance:
    - metric: string
      value: float
      sub_populations:
        - name: float
...
```

### List Templates

```bash
fda-samd templates list
```

Shows available built-in templates:

```
Available Templates
===================
PCCP:
  - pccp_v1_default (FDA Dec 2024)
  - pccp_v1_minimal (bare minimum)
  
Model Cards:
  - model_card_fda (with FDA-specific fields)
  - model_card_mitchell (original Mitchell et al. 2019)

510(k):
  - 510k_indications_for_use
  - 510k_device_description
  - 510k_substantial_equivalence
```

### Show Template

```bash
fda-samd templates show <template_name>
```

Display a template's Jinja2 syntax:

```bash
fda-samd templates show pccp_v1_default
```

---

## Configuration Examples

### PCCP Config Example

```yaml
device_name: "AI-ECG Analyzer v2.0"
device_class: "Class II"
intended_use: |
  Automated detection of atrial fibrillation from 12-lead ECG
  in adult patients aged 18-85 in hospital settings.

model_info:
  architecture: "ResNet-50 CNN"
  training_data_size: 150000
  training_data_sources:
    - "MIMIC-III: 80,000 ECGs"
    - "Partner Hospital A: 70,000 ECGs"
  
  performance:
    - metric: "sensitivity"
      value: 0.94
      confidence_interval: "0.92-0.96"
      sub_populations:
        - "age 18-45": 0.96
        - "age 65+": 0.92

change_control:
  - category: "retraining"
    frequency: "monthly"
    description: "Update model with new patient data"
```

### Model Card Config Example

```yaml
model_name: "AI-ECG Arrhythmia Detector"
model_version: "2.0.1"
training_data:
  sources:
    - "MIMIC-III"
    - "Partner hospitals"
  size: 150000
  preprocessing: "Bandpass filter, normalization"

performance:
  sensitivity: 0.94
  specificity: 0.91
  auc: 0.97
  
  sub_populations:
    age:
      - "18-45": 0.96
      - "65+": 0.92
```

---

## Error Messages and Solutions

### Error: "Config file not found"

```bash
fda-samd pccp generate --config missing.yaml
# Error: Config file 'missing.yaml' not found
```

**Solution**: Verify file path:

```bash
ls -la my_device.yaml
fda-samd pccp generate --config my_device.yaml --output PCCP.md
```

### Error: "Invalid YAML syntax"

```bash
# Error: YAML parse error in config.yaml, line 5: ...
```

**Solution**: Check YAML formatting:
- Indentation must be spaces, not tabs
- Colons need spaces (key: value, not key:value)
- Strings with special characters need quotes

### Error: "Missing required field: device_name"

```bash
# Error: Config validation failed. Required fields missing: ['device_name']
```

**Solution**: Add required fields to config:

```yaml
device_name: "Your Device Name"
device_class: "Class II"
intended_use: "..."
```

### Warning: "No sub-population performance data"

```bash
# Warning: Performance monitoring section: No sub-population analysis
# Recommendation: Add age, gender, and comorbidity breakdowns
```

**Solution**: Add sub-population data to config or accept warning.

---

## Advanced Usage

### Using Environment Variables

```bash
# Set output directory
export FDA_SAMD_OUTPUT_DIR=/path/to/output

fda-samd pccp generate --config device.yaml --output PCCP.md
# Output will go to /path/to/output/PCCP.md
```

### Batch Processing

```bash
# Process multiple configs
for config in devices/*.yaml; do
  fda-samd pccp generate --config "$config" \
    --output "output/$(basename $config .yaml).md"
done
```

### JSON Output

```bash
# Get PCCP as JSON
fda-samd pccp generate --config device.yaml --format json \
  > pccp.json

# Useful for programmatic processing
cat pccp.json | jq '.device_name'
```

---

## Troubleshooting

### Command Not Found

If `fda-samd` is not found:

```bash
# Check installation
pip list | grep fda-samd-toolkit

# Try module invocation
python -m fda_samd_toolkit.cli --version

# Reinstall if needed
pip install --upgrade fda-samd-toolkit
```

### Permission Denied (on Linux/Mac)

```bash
# Make script executable
chmod +x /path/to/fda-samd

# Or use python module
python -m fda_samd_toolkit.cli pccp generate --config device.yaml
```

### PDF Generation Failed

Requires wkhtmltopdf:

```bash
# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# macOS (with Homebrew)
brew install wkhtmltopdf

# Then retry
fda-samd pccp generate --config device.yaml --output PCCP.md --pdf
```

---

## Getting Help

```bash
# Show version
fda-samd --version

# Show help for any command
fda-samd --help
fda-samd pccp --help
fda-samd pccp generate --help

# View documentation
# Online: https://lal-jaouni.github.io/fda-samd-toolkit/
```

---

## Performance and Limits

Typical performance:

| Operation | Time |
|-----------|------|
| Generate PCCP | 1-2 seconds |
| Validate PCCP | 1-2 seconds |
| Generate model card | 1 second |
| Full readiness check | 3-5 seconds |

Limits:
- Config file size: No practical limit (tested to 1MB+)
- Number of sub-populations: Tested to 20+
- Output file size: Markdown, typically 5-10MB max (use PDF for larger)

---

## API Usage

If using the toolkit as a library (Python):

```python
from fda_samd_toolkit.pccp import PCCPGenerator
from fda_samd_toolkit.model_cards import ModelCardGenerator

# Generate PCCP programmatically
generator = PCCPGenerator(config_path="device.yaml")
pccp = generator.generate()
pccp.save("PCCP.md")

# Validate
from fda_samd_toolkit.pccp import validate_pccp
result = validate_pccp("PCCP.md")
print(f"Completeness: {result.completeness_percent}%")
```

See [API docs](../reference/api.md) for more details.

---

## Next Steps

- [Getting Started](../getting-started.md) - Quick 5-minute start
- [PCCP Generator Guide](../guides/pccp-generator.md) - Detailed PCCP instructions
- [FAQ & Troubleshooting](../getting-started.md#troubleshooting)
