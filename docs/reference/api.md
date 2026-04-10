# API Documentation

Programmatic API reference for using the FDA SaMD Toolkit as a Python library.

---

## Installation

```python
from fda_samd_toolkit.pccp import PCCPGenerator, validate_pccp
from fda_samd_toolkit.model_cards import ModelCardGenerator
from fda_samd_toolkit.validation import SampleSizeCalculator
from fda_samd_toolkit.readiness import ReadinessChecker
```

---

## PCCP Generator API

### PCCPGenerator Class

```python
from fda_samd_toolkit.pccp import PCCPGenerator

generator = PCCPGenerator(
    config_path="device.yaml",
    template_path=None,  # Optional custom template
    output_format="markdown"  # markdown, json, yaml
)

# Generate PCCP
pccp = generator.generate()

# Save to file
pccp.save("PCCP.md")

# Get as string
pccp_text = pccp.to_string()

# Get as JSON
pccp_json = pccp.to_json()
```

### PCCP Validation

```python
from fda_samd_toolkit.pccp import validate_pccp

# Validate PCCP file
result = validate_pccp("PCCP.md", strict=False)

# Check completeness
print(f"Completeness: {result.completeness_percent}%")

# Get issues
for issue in result.critical_issues:
    print(f"Critical: {issue.message}")

for warning in result.warnings:
    print(f"Warning: {warning.message}")

# Get section scores
for section, score in result.section_scores.items():
    print(f"{section}: {score}%")

# Save report
result.save_report("validation_report.html", format="html")
```

---

## Model Card Generator API

### ModelCardGenerator Class

```python
from fda_samd_toolkit.model_cards import ModelCardGenerator

generator = ModelCardGenerator(
    config_path="model_config.yaml",
    template_path=None  # Optional custom template
)

# Generate model card
card = generator.generate()

# Save
card.save("model_card.md")

# Get as text
card_text = card.to_string()
```

### Model Card Analysis

```python
from fda_samd_toolkit.model_cards import analyze_model_card

result = analyze_model_card("model_card.md")

# Check completeness
print(f"Completeness: {result.completeness_percent}%")

# Verify sub-population coverage
if result.has_sub_population_analysis:
    print("Sub-population analysis found")
else:
    print("Warning: No sub-population analysis")

# Get missing sections
for section in result.missing_sections:
    print(f"Missing: {section}")
```

---

## Validation Framework API

### Sample Size Calculator

```python
from fda_samd_toolkit.validation import SampleSizeCalculator

calc = SampleSizeCalculator(
    null_hypothesis=0.90,        # Device doesn't meet minimum
    alternative_hypothesis=0.94,  # Expected performance
    significance=0.05,           # Alpha
    power=0.90,                  # 1-beta
    prevalence=0.30              # Disease prevalence
)

# Calculate
result = calc.calculate()

# Get required N
print(f"Total N required: {result.total_n}")
print(f"Disease positive: {result.positive_n}")
print(f"Disease negative: {result.negative_n}")
print(f"With 5% drop-out: {result.total_n_with_dropout}")
```

### Study Protocol Generator

```python
from fda_samd_toolkit.validation import StudyProtocolGenerator

generator = StudyProtocolGenerator(
    device_name="AI-ECG Analyzer",
    study_type="prospective",  # retrospective, prospective, rct
    condition="Atrial Fibrillation",
    sample_size=2000,
    prevalence=0.30
)

# Generate protocol
protocol = generator.generate()

# Save
protocol.save("study_protocol.md")
```

---

## Readiness Check API

### ReadinessChecker Class

```python
from fda_samd_toolkit.readiness import ReadinessChecker

checker = ReadinessChecker(
    pccp_file="PCCP.md",
    model_card_file="model_card.md",
    submission_file="510k_submission.md"
)

# Run full check
result = checker.check()

# Get overall score
print(f"Completeness: {result.overall_completeness_percent}%")

# Get section scores
for section, score in result.section_scores.items():
    print(f"{section}: {score}%")

# Get recommendations
for recommendation in result.recommendations:
    print(f"- {recommendation}")

# Get estimated FDA review time
print(f"Est. review time: {result.estimated_review_days} days")

# Save HTML report
result.save_html_report("readiness_report.html")
```

---

## Configuration Classes

### Device Configuration

```python
from fda_samd_toolkit.config import DeviceConfig

config = DeviceConfig(
    device_name="AI-ECG Analyzer",
    device_class="Class II",
    intended_use="Detection of atrial fibrillation from ECG"
)

# Parse from file
config = DeviceConfig.from_yaml("device.yaml")

# Validate
if config.is_valid():
    print("Config is valid")
else:
    for error in config.validation_errors:
        print(f"Error: {error}")
```

### Model Configuration

```python
from fda_samd_toolkit.config import ModelConfig

config = ModelConfig(
    model_name="AI-ECG Detector v2.0",
    architecture="ResNet-50",
    training_data_size=150000
)

# Parse from file
config = ModelConfig.from_yaml("model_config.yaml")
```

---

## Template Management

### Template Handling

```python
from fda_samd_toolkit.templates import TemplateManager

# List available templates
manager = TemplateManager()
templates = manager.list_templates("pccp")
# Returns: ['pccp_v1_default', 'pccp_v1_minimal', ...]

# Load template
template = manager.get_template("pccp_v1_default")

# Get template variables
variables = template.get_required_variables()
# Returns: ['device_name', 'intended_use', ...]

# Render template
output = template.render({
    'device_name': 'My Device',
    'intended_use': '...',
    # ... other variables
})

# Create custom template
custom = manager.create_custom_template(
    path="/path/to/my_template.j2",
    format="markdown"
)
```

---

## Example: Complete Workflow

Here's a complete example showing how to use the API end-to-end:

```python
#!/usr/bin/env python3
"""Complete workflow example using FDA SaMD Toolkit API."""

from fda_samd_toolkit.config import DeviceConfig
from fda_samd_toolkit.pccp import PCCPGenerator, validate_pccp
from fda_samd_toolkit.model_cards import ModelCardGenerator
from fda_samd_toolkit.validation import SampleSizeCalculator
from fda_samd_toolkit.readiness import ReadinessChecker

# Step 1: Load device configuration
device_config = DeviceConfig.from_yaml("device.yaml")
print(f"Device: {device_config.device_name}")

# Step 2: Generate PCCP
pccp_gen = PCCPGenerator(config_path="device.yaml")
pccp = pccp_gen.generate()
pccp.save("PCCP.md")
print("✓ PCCP generated")

# Step 3: Validate PCCP
pccp_result = validate_pccp("PCCP.md")
print(f"PCCP completeness: {pccp_result.completeness_percent}%")

# Step 4: Generate model card
model_gen = ModelCardGenerator(config_path="model_config.yaml")
model_card = model_gen.generate()
model_card.save("model_card.md")
print("✓ Model card generated")

# Step 5: Calculate validation study sample size
calc = SampleSizeCalculator(
    null_hypothesis=0.90,
    alternative_hypothesis=0.94,
    significance=0.05,
    power=0.90,
    prevalence=0.30
)
sample_result = calc.calculate()
print(f"Required N: {sample_result.total_n}")

# Step 6: Run readiness check
checker = ReadinessChecker(
    pccp_file="PCCP.md",
    model_card_file="model_card.md",
    submission_file="submission.md"
)
readiness = checker.check()
print(f"Overall readiness: {readiness.overall_completeness_percent}%")

# Step 7: Save report
readiness.save_html_report("readiness_report.html")

print("✓ All components generated and validated")
print(f"Ready for FDA submission: {readiness.is_ready_for_submission}")
```

---

## Error Handling

### Exception Types

```python
from fda_samd_toolkit.exceptions import (
    ConfigError,
    ValidationError,
    TemplateError,
    GenerationError
)

try:
    config = DeviceConfig.from_yaml("invalid.yaml")
except ConfigError as e:
    print(f"Config error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    pccp = generator.generate()
except GenerationError as e:
    print(f"Generation error: {e}")
    # Handle gracefully
```

### Logging

```python
import logging
from fda_samd_toolkit import get_logger

# Configure logging
logger = get_logger("fda_samd_toolkit", level=logging.DEBUG)

# Operations will now log progress
logger.debug("Starting PCCP generation...")
pccp = generator.generate()
logger.info("PCCP generation complete")
```

---

## Performance Considerations

### Memory Usage

For large configurations:

```python
# Stream output to file instead of loading in memory
generator = PCCPGenerator(config_path="large.yaml")
pccp = generator.generate()
pccp.save("output.md", stream=True)  # Streams to file
```

### Caching

```python
# Enable template caching for repeated use
from fda_samd_toolkit.templates import TemplateManager

manager = TemplateManager(cache=True)
template1 = manager.get_template("pccp_v1_default")
template2 = manager.get_template("pccp_v1_default")  # From cache
```

---

## Advanced: Custom Validation Rules

```python
from fda_samd_toolkit.validation import CustomValidator

# Define custom validation rule
class MyValidator(CustomValidator):
    def validate(self, pccp: str) -> bool:
        # Custom rule: must mention sub-populations
        return "sub-population" in pccp.lower()

# Use custom validator
validator = MyValidator()
is_valid = validator.validate(pccp.to_string())
```

---

## API Stability

This API is currently in **alpha**. Expect:

- Method signatures may change before v1.0
- New methods will be added based on community feedback
- Deprecated methods will have 2-release notice

For production use, pin to a specific version:

```bash
pip install fda-samd-toolkit==0.1.0
```

---

## Next Steps

- [CLI Reference](cli.md) - Command-line usage
- [Contributing](../contributing.md) - Extend the toolkit
- [GitHub Issues](https://github.com/lal-jaouni/fda-samd-toolkit/issues) - Report bugs
