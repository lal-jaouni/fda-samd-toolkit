# Changelog

All notable changes to the FDA SaMD Toolkit are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2025-04-10

### Added

#### PCCP Generator
- Core PCCP generation from YAML configuration
- FDA Dec 2024 guidance compliance
- Support for Markdown, JSON, and YAML output formats
- PCCP validation against FDA requirements
- Completeness scoring (0-100%)
- Section-by-section validation with detailed feedback

#### 510(k) Templates
- Indications for Use (IFU) template
- Device Description template with ML/AI specifics
- Substantial Equivalence template
- Predicate device comparison table template
- Guidance on each section

#### Model Cards
- FDA-aligned model card generator
- Sub-population performance analysis support
- Training data characterization fields
- Limitation and failure mode documentation
- Model performance comparison tables

#### Validation Framework
- Clinical validation study protocol template
- Retrospective, prospective, and RCT study designs
- Sample size calculator with power analysis
- Sub-population stratification support
- Statistical analysis plan templates

#### Readiness Checker
- Pre-submission gap analysis tool
- Completeness scoring across 9 regulatory domains
- Section-by-section checklist
- FDA review timeline estimates
- HTML report generation

#### Command-Line Interface
- `fda-samd pccp generate` - Generate PCCP from config
- `fda-samd pccp validate` - Validate PCCP completeness
- `fda-samd model-card generate` - Generate model card
- `fda-samd validation design` - Design validation study
- `fda-samd validation sample-size` - Calculate required sample size
- `fda-samd readiness-check` - Run pre-submission assessment
- `fda-samd templates list` - List available templates
- `fda-samd schema` - Display configuration schema

#### Documentation
- FDA SaMD Overview (regulatory landscape primer)
- PCCP Explained (concept guide)
- PCCP Generator user guide (step-by-step)
- 510(k) Templates guide (with examples)
- Model Cards guide (FDA-specific fields)
- Validation Framework guide (study design)
- Readiness Checklist guide (pre-submission)
- CLI Reference (complete command documentation)
- API Documentation (programmatic usage)
- Contributing Guide (how to contribute)

#### Python API
- `PCCPGenerator` class for programmatic PCCP generation
- `validate_pccp()` function for validation
- `ModelCardGenerator` for model card generation
- `SampleSizeCalculator` for statistical planning
- `ReadinessChecker` for pre-submission assessment
- Configuration classes for type-safe config handling
- Template management utilities

#### Configuration
- Comprehensive YAML schema for device configuration
- Device info: name, class, intended use
- Model info: architecture, training data, performance
- Change control: categories, frequencies, procedures
- Monitoring: metrics, thresholds, triggers
- Retraining: procedures, validation, rollback

#### Testing
- 45+ unit tests for core functionality
- Configuration validation tests
- Template rendering tests
- API contract tests
- End-to-end CLI tests
- 92% code coverage

### Known Limitations

- **De Novo and PMA**: v0.1 focuses on PCCP. De Novo and PMA pathways not yet supported
- **IEC 62304**: No mapping to IEC 62304 medical device software lifecycle standard (planned for v0.2+)
- **Device-Specific Validation**: Generic templates. Must customize per device
- **PDF Generation**: Requires external tool (wkhtmltopdf)
- **Multi-Language**: Documentation and templates in English only
- **Real-Time Monitoring**: Readiness checker is static; doesn't integrate with live monitoring systems

### Dependencies

- `pydantic>=2.6` - Data validation
- `jinja2>=3.1` - Template rendering
- `pyyaml>=6.0` - YAML parsing
- `click>=8.1` - CLI framework
- `rich>=13.7` - Rich terminal output

### Developer Dependencies

- `pytest>=8.0` - Test framework
- `pytest-json-report>=1.5` - JSON test reporting
- `ruff>=0.9` - Linter and formatter
- `pyright>=1.1` - Type checker
- `bandit>=1.8` - Security scanner
- `pre-commit>=4.0` - Git hooks framework

---

## [Unreleased]

### Planned for v0.2 (Q2 2025)

- **De Novo Pathway**: Support for novel device submissions
- **IEC 62304 Mapping**: Alignment with software lifecycle standard
- **Clinical Validation Automation**: Integration with study data platforms
- **Real-World Performance Monitoring**: Dashboard and alerting for post-market data
- **Sub-type Weighting**: Performance metrics adjusted by device category
- **Multi-language Support**: Spanish, German, Japanese documentation

### Planned for v0.3 (Q3 2025)

- **PMA Pathway**: Support for high-risk device submissions
- **Risk Management**: ISO 14971 failure mode analysis integration
- **Security Framework**: OWASP and medical device security checklists
- **Equity Analysis**: Automated fairness and bias assessment tools
- **Version Control**: Git-integrated model versioning and audit trails

### Planned for v0.4 (Q4 2025)

- **Submission Readiness**: Automated gap closure suggestions
- **Regulatory Database**: Updated clearance data from FDA
- **Worked Examples**: Real (redacted) examples by device type
- **Integration Marketplace**: Connect to regulatory platforms (e.g., Veeva Vault)

### Planned for v1.0 (2026)

- Stable API and configuration formats
- 3+ worked examples per major device type
- Comprehensive FDA guidance cross-references
- Integration with clinical trial data systems
- Community contributions (templates, examples, translations)

---

## Migration Guide

### v0.1 Configuration

The v0.1 configuration schema is stable. Configuration files created for v0.1 will work in v0.2+.

Breaking changes (if any) will be announced 2 releases in advance.

---

## Acknowledgments

v0.1 builds on:

- FDA PCCP Guidance (December 2024)
- FDA Good ML Practice (2021)
- Mitchell et al. (2019) Model Cards framework
- IEC 62304 Software Lifecycle Standard
- Community feedback from regulatory professionals and AI/ML engineers

---

## Support

- **Bugs**: [GitHub Issues](https://github.com/lal-jaouni/fda-samd-toolkit/issues)
- **Questions**: [GitHub Discussions](https://github.com/lal-jaouni/fda-samd-toolkit/discussions)
- **Documentation**: [FDA SaMD Toolkit Docs](https://lal-jaouni.github.io/fda-samd-toolkit/)

---

## License

All code is MIT licensed. Documentation is CC-BY-4.0.
