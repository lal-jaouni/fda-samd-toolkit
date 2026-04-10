# FDA SaMD Toolkit

> Templates and generators for FDA 510(k) AI/ML medical device submissions. Cuts weeks of regulatory busywork to hours.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Release: v0.1.0](https://img.shields.io/badge/release-v0.1.0-green)](https://github.com/lal-jaouni/fda-samd-toolkit/releases)
[![Tests: 170 passing](https://img.shields.io/badge/tests-170%20passing-brightgreen)](https://github.com/lal-jaouni/fda-samd-toolkit/actions)

Building AI/ML for healthcare? FDA Software-as-a-Medical-Device (SaMD) submissions require specific documentation that doesn't exist in any open-source form. This toolkit fills that gap.

## What's shipped (v0.1.0)

| Component | Status | Description |
|---|---|---|
| **PCCP Generator** | Shipped | Predetermined Change Control Plan generator (FDA Dec 2024 guidance) |
| **510(k) AI/ML Templates** | Shipped | 7 markdown templates: IFU, device description, substantial equivalence, performance, training data, risk analysis, human factors |
| **FDA-Extended Model Card Generator** | Shipped | Mitchell et al. 2019 sections plus FDA fields (predicate devices, classification, subpopulation analysis, PCCP linkage) |
| **Clinical Validation Framework** | Shipped | Modality guidance for imaging, signals, NLP, multimodal |
| **Submission Readiness Checklist** | Shipped | 58 items across 8 categories with interactive runner |
| **Predicate Device Discovery** | Shipped | Search openFDA 510(k) database, rank by relevance |
| **Click + Rich CLI** | Shipped | `pccp`, `templates`, `model-card`, `checklist`, `predicate` subcommands |
| **MkDocs Documentation Site** | Shipped | Per-component user guides plus API and CLI references |
| **CardioGuard ECG-AI Worked Example** | Shipped | Complete fictional 510(k) package tying every component together |

170 tests passing. CI matrix on Python 3.11 and 3.12. Coverage at 74%, gated at 70%.

## Quick start

```bash
pip install fda-samd-toolkit

# Scaffold a starter PCCP YAML for an ECG classifier
fda-samd pccp init --type ecg --output my_pccp.yaml

# Generate a Predetermined Change Control Plan from the YAML config
fda-samd pccp generate \
  --config examples/pccp_ecg_classifier.yaml \
  --output PCCP.md

# Validate a generated PCCP for FDA completeness (flags unfilled placeholders)
fda-samd pccp validate --file PCCP.md

# Generate an FDA-extended model card
fda-samd model-card generate \
  --config examples/model_card_ecg_classifier.yaml \
  --output model_card.md

# Run the readiness checklist non-interactively from a YAML
fda-samd checklist \
  --config examples/checklist_artifacts.yaml \
  --device-name "My Device" \
  --output readiness.md

# Or run the checklist interactively (prompts for each of 58 items)
fda-samd checklist

# Discover predicate devices from openFDA 510(k) database
fda-samd predicate discover \
  --device-description "12-lead ECG arrhythmia classifier" \
  --intended-use "Detection of atrial fibrillation" \
  --limit 5 \
  --output predicates.md
```

The [`examples/cardioguard-ecg-ai/`](examples/cardioguard-ecg-ai/) directory has a complete narrative worked submission package showing how every component fits together: PCCP, model card, validation plan, 5 filled 510(k) sections, risk analysis, cybersecurity, submission checklist, and project timeline. (Note: the CardioGuard YAMLs are illustrative narrative; the runnable CLI examples above use the schema-conforming fixtures in `examples/`.)

## Why this exists

Most AI/ML startups submitting to FDA are flying blind:

- The PCCP guidance (finalized Dec 2024) is 25 pages of regulatory text with no concrete templates
- 510(k) AI/ML-specific sections (intended use, performance, training data characterization) have no public templates
- Model cards exist but none address FDA-specific concerns (data drift monitoring, sub-population performance, indications for use)
- Companies pay regulatory consultants $300-500/hr to assemble what could be templated

This toolkit puts that scaffolding in the open so small teams can ship faster and iterate on real product instead of regulatory minutiae.

## Who this is for

- **AI/ML startup CTOs** preparing a first 510(k) submission (8 weeks before filing date)
- **Regulatory consultants** standardizing deliverables across multiple device clients
- **Hospital innovation teams** piloting AI tools and learning the FDA pathway

See [`docs/positioning.md`](docs/positioning.md) for detailed personas, success metrics, and the v1.0 vision.

## Roadmap

**v0.1.0 (shipped April 2026):** PCCP, 7 510(k) templates, FDA-extended model cards, validation framework, readiness checklist, CLI, MkDocs site, CardioGuard worked example. See [CHANGELOG.md](CHANGELOG.md) for details.

**v0.2 (in progress):** 5 must-use features identified by user research at [`research/must_use_features.md`](research/must_use_features.md):

- [#14](https://github.com/lal-jaouni/fda-samd-toolkit/issues/14) Cybersecurity SBOM generator (NTIA format, mandatory per June 2025 FDA guidance)
- [#15](https://github.com/lal-jaouni/fda-samd-toolkit/issues/15) Bias evaluation report generator (Jan 2025 FDA guidance requirement)
- [#16](https://github.com/lal-jaouni/fda-samd-toolkit/issues/16) Real-world performance monitoring plan generator
- [#17](https://github.com/lal-jaouni/fda-samd-toolkit/issues/17) eSTAR submission package builder (mandatory format since Oct 2023)
- [#18](https://github.com/lal-jaouni/fda-samd-toolkit/issues/18) IEC 62304 + ISO 14971 templates (OpenRegulatory integration)

**v0.3+ candidates:** Imaging AI and NLP/EHR AI validation protocols, GMLP evidence templates, regulatory intelligence auto-update, predicate device discovery. See [ROADMAP.md](ROADMAP.md).

**v1.0 (target: Q1 2027):** Stable APIs, worked examples for cardiac AI, imaging AI, and NLP/EHR AI. At least one real submission citing the toolkit. See [`docs/positioning.md`](docs/positioning.md) for the full v1.0 definition.

## Documentation

- **User guides:** [`docs/guides/`](docs/guides/) covers each generator with examples
- **API reference:** [`docs/reference/api.md`](docs/reference/api.md)
- **CLI reference:** [`docs/reference/cli.md`](docs/reference/cli.md)
- **Quality strategy:** [`docs/quality.md`](docs/quality.md) covers test pyramid, coverage targets, mutation testing
- **Product planning:** [`docs/product/`](docs/product/) has personas, metrics, scope, release cadence, v1.0 definition, definition-of-done

Run the docs site locally with `mkdocs serve` after installing dev dependencies.

## Disclaimer

This toolkit produces document scaffolding. It is **not legal, regulatory, or medical advice**. Every FDA submission requires review by qualified regulatory professionals. Generated documents must be customized to your specific device, intended use, and clinical context. The maintainers assume no liability for submissions made using this tool.

## Contributing

This project welcomes contributions from the regulatory and AI/ML community. See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing requirements, and the "Adding a new feature" walkthrough. Quality bar is documented in [`docs/quality.md`](docs/quality.md) and the per-PR checklist at [`docs/qa-checklist.md`](docs/qa-checklist.md).

Areas where help is most needed:

- Real-world PCCP examples (anonymized from cleared 510(k) submissions)
- Worked 510(k) AI/ML examples by therapy area (especially imaging and NLP)
- Validation protocol templates for specific modalities
- IEC 62304 mapping for ML pipelines

## License

MIT. Use freely in commercial products. Attribution appreciated but not required.

## Acknowledgments

Built on top of:

- [FDA AI/ML Action Plan (2021)](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-software-medical-device)
- [FDA PCCP Final Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [FDA AI/ML Lifecycle Management (Jan 2025 draft)](https://www.fda.gov/media/184856/download)
- [FDA Cybersecurity in Medical Devices (June 2025)](https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity)
- [IMDRF SaMD Framework](https://www.imdrf.org/working-groups/software-medical-device-samd)
- [Mitchell et al. 2019: Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)
