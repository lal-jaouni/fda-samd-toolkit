# Contributing to FDA SaMD Toolkit

Thank you for your interest in contributing! This project welcomes contributions from regulatory professionals, AI/ML engineers, and healthcare innovators.

---

## What We Need

### Documentation

- Real-world PCCP examples (anonymized)
- Worked 510(k) AI/ML examples by therapy area (cardiology, oncology, etc.)
- Validation protocol templates for specific modalities (imaging, signals, NLP)
- Regulatory checklists and decision trees
- Explanatory content for clinicians and non-technical readers

### Code

- Additional template variations (minimal PCCP, multi-device PCCP, etc.)
- Validation improvements (better checking, more specific recommendations)
- New sub-commands (e.g., IEC 62304 mapping, risk analysis generator)
- Performance optimizations
- Bug fixes

### Examples

- Real anonymized examples showing:
  - PCCP for cardiac devices
  - PCCP for imaging devices
  - PCCP for NLP/document analysis
  - Clinical validation protocols that went to FDA
  - Regulatory submissions (redacted appropriately)

### Testing

- Additional test cases covering edge cases
- Integration tests with real regulatory data
- Performance benchmarks
- Accessibility testing for documentation

---

## Getting Started

### 1. Development Setup

Clone the repository:

```bash
git clone https://github.com/lal-jaouni/fda-samd-toolkit.git
cd fda-samd-toolkit
```

Install dependencies with uv:

```bash
uv pip install -e ".[dev]"
```

Verify installation:

```bash
fda-samd --version
pytest
ruff check src tests
pyright src tests
```

### 2. Code Structure

```
fda-samd-toolkit/
├── src/fda_samd_toolkit/
│   ├── cli.py                 # Command-line interface
│   ├── config.py              # Configuration parsing
│   ├── pccp/
│   │   ├── generator.py       # PCCP generation logic
│   │   ├── validator.py       # PCCP validation
│   │   └── schemas.py         # Pydantic models
│   ├── model_cards/
│   │   ├── generator.py       # Model card generation
│   │   └── analyzer.py        # Model card analysis
│   ├── validation/
│   │   ├── framework.py       # Study design tools
│   │   └── calculator.py      # Sample size calculations
│   ├── readiness/
│   │   └── checker.py         # Readiness assessment
│   ├── templates/
│   │   ├── pccp/              # PCCP Jinja2 templates
│   │   ├── model_card/        # Model card templates
│   │   └── 510k/              # 510(k) section templates
│   └── exceptions.py          # Custom exceptions
├── tests/
│   ├── test_pccp.py
│   ├── test_model_cards.py
│   ├── test_validation.py
│   └── test_cli.py
├── docs/
│   ├── index.md
│   ├── concepts/
│   ├── guides/
│   └── reference/
├── mkdocs.yml
└── pyproject.toml
```

### 3. Branch Strategy

Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

Branch naming:
- `feature/pccp-enhancements` - New features
- `fix/validation-bug` - Bug fixes
- `docs/fda-overview` - Documentation
- `test/sample-size-coverage` - Tests

---

## Types of Contributions

### Adding a New Template

**Templates are the most impactful contribution.** Templates help users generate better regulatory documents.

Example: Adding a minimal PCCP template for small startups:

1. Create template file: `src/fda_samd_toolkit/templates/pccp/minimal.j2`

```jinja2
# PCCP: {{ device_name }}

## Device Classification
- Name: {{ device_name }}
- Class: {{ device_class }}

## Intended Use
{{ intended_use }}

## Algorithm
- Type: {{ model_info.architecture }}
- Performance: Sensitivity {{ model_info.performance.sensitivity }}

## Changes
{% for change in change_control %}
- {{ change.category }}: {{ change.description }}
{% endfor %}

## Monitoring
[PLACEHOLDER: Add your monitoring plan]
```

2. Register template in `src/fda_samd_toolkit/templates/__init__.py`:

```python
TEMPLATES = {
    'pccp': {
        'default': 'pccp/default.j2',
        'minimal': 'pccp/minimal.j2',  # Add this
    }
}
```

3. Test template:

```bash
fda-samd pccp generate --config test_config.yaml \
  --template src/fda_samd_toolkit/templates/pccp/minimal.j2 \
  --output test_output.md
```

4. Write test: `tests/test_templates_minimal.py`

```python
def test_minimal_template_generation():
    """Test that minimal PCCP template generates valid output."""
    config = load_test_config("minimal")
    output = generate_from_template("minimal", config)
    assert "PCCP:" in output
    assert config.device_name in output
```

5. Add documentation: `docs/guides/templates.md`

6. Commit:

```bash
git add src/fda_samd_toolkit/templates/pccp/minimal.j2
git add src/fda_samd_toolkit/templates/__init__.py
git add tests/test_templates_minimal.py
git commit -m "Add minimal PCCP template for early-stage startups

Templates for smaller teams that need a simpler PCCP structure.
Focuses on essentials: device, algorithm, monitoring, changes.

See docs/guides/templates.md for examples."
```

### Adding an Example

Examples show real-world usage. Very helpful for users.

1. Create example: `examples/cardiac_monitor_pccp.yaml`

```yaml
device_name: "Cardiac Rhythm Monitor AI v2"
device_class: "Class II"
# ... full config
```

2. Create README explaining: `examples/cardiac_monitor/README.md`

```markdown
# Cardiac Rhythm Monitor PCCP Example

This is a worked example of a PCCP for an AI system that detects
arrhythmias from ECG data.

## Use This If...
- Your device analyzes cardiac signals (ECG, Holter, etc.)
- You plan monthly retraining on new patient data
- You need to demo regulatory preparation to investors

## Files
- `config.yaml`: Full PCCP configuration
- `PCCP.md`: Generated output (what FDA sees)
- `study_protocol.md`: Clinical validation study design
- `model_card.md`: Model documentation

## Commands
\`\`\`bash
fda-samd pccp generate --config cardiac_monitor_pccp.yaml
\`\`\`
```

3. Add to docs: Reference in [Getting Started](getting-started.md) and [Examples](examples.md)

4. Commit:

```bash
git add examples/cardiac_monitor/
git commit -m "Add cardiac monitoring device PCCP example

Comprehensive example showing full PCCP workflow for AI-based
arrhythmia detection from ECG data. Includes change control,
monitoring plan, and sample sub-population analysis."
```

### Improving Documentation

Documentation is critical. Typos, unclear sections, and missing examples all slow users down.

1. Edit the relevant markdown file in `docs/`

2. Test the docs site locally:

```bash
pip install mkdocs-material mkdocstrings
mkdocs serve
# Open http://localhost:8000
```

3. Verify links work, examples are correct, formatting is clean

4. Commit:

```bash
git add docs/guides/pccp-generator.md
git commit -m "Clarify PCCP monitoring section with additional examples

Added breakdown of weekly vs. monthly monitoring, with specific
metrics and thresholds. Addresses GitHub issue #42."
```

### Writing Tests

Every change should include tests.

Example test structure:

```python
import pytest
from fda_samd_toolkit.pccp import PCCPGenerator
from fda_samd_toolkit.config import DeviceConfig

class TestPCCPGenerator:
    """Test PCCP generation functionality."""

    @pytest.fixture
    def sample_config(self):
        """Sample device configuration."""
        return DeviceConfig(
            device_name="Test Device",
            device_class="Class II",
            intended_use="Test indication"
        )

    def test_basic_generation(self, sample_config):
        """Test that PCCP generates without error."""
        generator = PCCPGenerator(config=sample_config)
        pccp = generator.generate()
        
        assert pccp is not None
        assert sample_config.device_name in pccp.to_string()

    def test_all_sections_present(self, sample_config):
        """Test that all required sections are present."""
        generator = PCCPGenerator(config=sample_config)
        pccp = generator.generate()
        output = pccp.to_string()
        
        required_sections = [
            "Device Classification",
            "Intended Use",
            "Algorithm Overview",
            "Performance Monitoring"
        ]
        
        for section in required_sections:
            assert section in output, f"Missing section: {section}"

    def test_json_export(self, sample_config):
        """Test that PCCP can be exported to JSON."""
        generator = PCCPGenerator(config=sample_config)
        pccp = generator.generate()
        json_output = pccp.to_json()
        
        assert "device_name" in json_output
        assert json_output["device_name"] == "Test Device"
```

Run tests:

```bash
pytest tests/test_pccp.py -v
pytest --cov=src --cov-report=html  # Coverage report
```

### Bug Fixes

Found a bug? Here's how to fix it:

1. Create an issue describing the bug
2. Create a test that reproduces the bug
3. Fix the code
4. Verify test passes
5. Commit with issue reference

```bash
git commit -m "Fix PCCP validation crash on empty config

Previous code assumed device_name was always present.
Now safely handles missing optional fields with helpful error message.

Fixes #123"
```

---

## Code Standards

### Style

Code follows PEP 8 with these enforcements:

```bash
# Format code
ruff format src tests

# Check for lint issues
ruff check src tests --fix

# Type checking
pyright src tests
```

### Docstrings

All public functions need docstrings. Use Google style:

```python
def generate_pccp(config: DeviceConfig) -> str:
    """Generate a PCCP document from device configuration.
    
    Reads the configuration, applies the PCCP template, and returns
    a Markdown-formatted PCCP document ready for FDA submission.
    
    Args:
        config: Device configuration with algorithm, training data,
            and change control information.
    
    Returns:
        Markdown-formatted PCCP document as a string.
    
    Raises:
        ConfigError: If required fields are missing from config.
        TemplateError: If template cannot be loaded or rendered.
    
    Example:
        >>> config = DeviceConfig.from_yaml("device.yaml")
        >>> pccp = generate_pccp(config)
        >>> print(pccp[:100])
        '# PCCP: Device Name ...'
    """
```

### Type Hints

All function signatures need type hints:

```python
def validate_pccp(
    file_path: str,
    strict: bool = False
) -> ValidationResult:
    """Validate a PCCP document."""
```

### Testing

Aim for >80% code coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Cover:
- Happy path (normal operation)
- Error cases (missing config, invalid input)
- Edge cases (empty lists, extreme values)

---

## Commit Guidelines

Commit messages should be clear and descriptive:

**Good**:
```
Add sub-population performance analysis to model card

Extends model card template to include performance breakdowns by
age, gender, and comorbidity. Addresses FDA guidance on fairness
and bias documentation.

Adds 3 new fields to ModelCardConfig schema and updates validator.
```

**Bad**:
```
Fix stuff
Update code
Add things
```

Format:
- First line: imperative mood, <70 characters, no period
- Blank line
- Body: Explain what and why (not just what)
- Reference issues: "Fixes #123" or "Related to #456"

---

## Pull Request Process

1. **Create PR from your feature branch**

```bash
git push origin feature/your-feature
# Go to GitHub, create PR
```

2. **PR Title Format**: `[Type] Description`

Examples:
- `[Feature] Add minimal PCCP template`
- `[Docs] Clarify sub-population analysis section`
- `[Fix] Handle missing ECG channels gracefully`

3. **PR Description**: Explain what, why, and testing:

```markdown
## What
Adds a new minimal PCCP template for early-stage startups.

## Why
Users with limited resources need a simpler, shorter PCCP that
focuses only on essentials. Current default template is 30+ pages.

## Testing
- Tested with sample cardiac device config
- All existing tests still pass
- Added 5 new tests for minimal template

## Checklist
- [x] Code formatted with ruff
- [x] Tests added/updated
- [x] Docs updated
- [x] No breaking changes
```

4. **CI/CD Checks**: Ensure all checks pass:

- Linting (ruff check)
- Formatting (ruff format --check)
- Type checking (pyright)
- Tests (pytest)
- Coverage (>80%)

5. **Code Review**: Address feedback from maintainers

6. **Merge**: Once approved, maintainer will merge to main

---

## Community Standards

This project is committed to a welcoming and inclusive environment.

### Conduct

- Be respectful of others' time and expertise
- Assume good intent
- Welcome diverse perspectives
- Focus on ideas, not personalities
- Resolve disagreements via discussion

### Contribution Credits

Contributors are credited in:
- CHANGELOG.md (for feature/fix contributions)
- README.md (for significant ongoing contributors)
- GitHub contributors page

---

## Getting Help

- **Questions about FDA?** Check [FDA Overview](concepts/fda-overview.md) or [PCCP Explained](concepts/pccp-explained.md)
- **How to use the toolkit?** See [Getting Started](getting-started.md) or [Guides](guides/)
- **How to contribute code?** See this file or GitHub issues
- **Report a bug?** Open a GitHub issue with reproduction steps
- **Want to discuss an idea?** Start a GitHub discussion

---

## Recognition

Contributors are recognized:

- **First contribution**: Added to CONTRIBUTORS.md
- **3+ contributions**: Added to README.md
- **Major features**: May be invited to co-maintain area of toolkit

---

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with changes
3. Create release branch: `git checkout -b release/0.2.0`
4. Tag release: `git tag -a v0.2.0 -m "Release 0.2.0"`
5. Push: `git push --tags`
6. GitHub Actions auto-builds and publishes to PyPI

---

## Resources

- [FDA PCCP Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [Good ML Practice (2021)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-machine-learning-practice-medical-device-development)
- [GitHub Contribution Guide](https://docs.github.com/en/get-started/exploring-integrations/about-integrations)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## Thank You!

Your contributions help make FDA compliance accessible to everyone. Thank you for being part of this mission.

Questions? Open a GitHub issue or discussion. We're here to help!
