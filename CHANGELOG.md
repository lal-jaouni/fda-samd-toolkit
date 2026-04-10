# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `fda-samd predicate discover` command for searching and ranking predicate 510(k) devices via the openFDA API. Users provide device description and intended use, the tool searches openFDA, scores results using fuzzy matching and keyword overlap, and returns a ranked table of candidates. Results can be exported to markdown for inclusion in a 510(k) submission. Includes 46 tests achieving 95% coverage across client, scorer, and CLI layers.

## [0.1.1] - 2026-04-10

Hotfix release: wires the validation CLI, restores spell-check CI job, and documents known limitations uncovered by post-ship QA.

### Added

- `fda-samd validation generate` and `fda-samd validation init` CLI subcommands. The clinical validation plan generator was shipped in v0.1.0 with example YAMLs and a working backend, but no CLI entry point. This adds the missing Click group and 8 test cases that exercise it end-to-end on the example configs.
- Spell-check CI job re-enabled. The `.typos.toml` config was restructured to use the correct `[default.extend-words]` table format required by typos >= 1.x. The previous array form caused a TOML parse error in typos v1.28.4 and was temporarily disabled during the v0.1.0 release cut.

### Fixed

- Typo fix in `docs/guides/model-cards.md` (verb spelling corrected in the pacemaker patients subgroup note).
- Added `ehr`, `rto`, `rpo`, and `stard` to the typos allowlist. These are real clinical and regulatory acronyms the spell-checker was incorrectly flagging.

### Planned for v0.2

- Cybersecurity SBOM Generator (NTIA format, mandatory per June 2025 FDA guidance)
- Bias & Subpopulation Performance Evaluation Report (Jan 2025 FDA guidance requirement)
- Real-World Performance Monitoring & Drift Detection Plan
- eSTAR Package Builder (auto-assemble FDA submission packages in mandatory format)
- IEC 62304 + ISO 14971 Integration (OpenRegulatory templates)

## [0.1.0] - 2026-04-10

First release: complete 510(k) AI/ML submission toolkit with PCCP, model cards, templates, and worked examples.

### Added

#### Core Generators
- **PCCP (Predetermined Change Control Plan) Generator** - Auto-generates change control plans from YAML configs aligned with FDA Dec 2024 guidance. Supports retraining triggers, drift detection, and data source specification.
- **FDA-Extended Model Card Generator** - Clinical context model cards extending Mitchell et al. 2019 with FDA-specific fields: predicate devices, training data demographics, subpopulation performance analysis, intended use linkage.
- **510(k) AI/ML Section Templates** (7 templates in Markdown):
  - Indications for Use (IFU) statement template
  - Device Description and Algorithm Architecture
  - Substantial Equivalence Argument
  - Performance Testing Summary and Clinical Validation
  - Training Data Characterization and Bias Analysis
  - Risk Analysis (ISO 14971 mapping)
  - Human Factors Evaluation and Labeling

#### Clinical Validation
- **Clinical Validation Framework** with modality-specific guidance:
  - Imaging AI validation protocol template
  - Biosignal AI validation protocol template
  - NLP/Clinical Text AI validation protocol template
  - Multimodal AI validation protocol template
- Validation study design patterns (retrospective, prospective, real-world evidence)
- Subpopulation performance evaluation guidance (demographics, indications, clinical context)

#### Quality & Compliance
- **Submission Readiness Checklist** - 58-item assessment across 8 categories:
  - Design Controls (FDA QSR Part 11 alignment)
  - Risk Management (ISO 14971)
  - Software Lifecycle (IEC 62304)
  - AI/ML-Specific Considerations (GMLP, data governance, model monitoring)
  - Cybersecurity (threat model, software bill of materials)
  - Clinical Evidence (validation study quality, bias assessment)
  - Quality Management System (design history file, traceability)
  - Submission Documentation (eSTAR readiness, completeness)

#### User Interface
- **Click + Rich CLI** with subcommands:
  - `fda-samd pccp generate` - Generate PCCP from YAML config
  - `fda-samd pccp validate` - Validate PCCP completeness
  - `fda-samd model-card generate` - Generate model card from YAML config
  - `fda-samd templates list` - List available 510(k) templates
  - `fda-samd checklist assess` - Run submission readiness assessment
  - `fda-samd checklist export` - Export checklist as PDF/JSON/Markdown

#### Examples & Documentation
- **CardioGuard ECG-AI Complete Worked Example** - Realistic 510(k) submission for fictional Class II cardiac AI device:
  - Device overview and clinical context
  - PCCP configuration (retraining cadence, drift triggers)
  - Model card with subpopulation performance (sex, age, race/ethnicity)
  - Validation study protocol (3 sites, n=1500, retrospective design)
  - Risk analysis and cybersecurity assessment
  - Submission checklist with completion status
  - 510(k) sections (IFU, device description, substantial equivalence, performance summary)
- **MkDocs Material Documentation Site** with:
  - Getting Started guide
  - FDA SaMD and PCCP concepts
  - Component-specific user guides (PCCP generator, model cards, validation, checklist)
  - Python API reference
  - CLI command reference
  - FAQ and troubleshooting
- **ROADMAP.md** - Dual tracking (GitHub milestones + labels) for transparency

#### Testing & CI/CD
- **157 Unit Tests** covering:
  - YAML config parsing and validation
  - Jinja template rendering
  - PCCP generator output correctness
  - Model card field validation
  - Checklist scoring and exports
- **GitHub Actions CI Pipeline** - Runs on Python 3.11 and 3.12
  - Pytest unit tests with JSON report
  - Ruff linting and formatting
  - Pyright static type checking
  - Bandit security analysis
- **Release Workflow** - Automated PyPI publishing on tag push (trusted publisher setup pending)

### Changed

- None (first release)

### Fixed

- None (first release)

### Known Limitations

- eSTAR package assembly is manual (v0.2 will automate)
- Cybersecurity SBOM generation not yet included (v0.2 planned)
- IEC 62304 and ISO 14971 templates are guidance only; integration with OpenRegulatory planned for v0.2
- Bias evaluation is template-based; no automated demographic fairness analysis (v0.2 planned)
- Real-world monitoring is planning template only; no integration with post-market data sources (v0.2 planned)

---

For a detailed list of changes, commits, and contributors, see the [GitHub releases page](https://github.com/lal-jaouni/fda-samd-toolkit/releases).
