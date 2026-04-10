# FDA SaMD Toolkit

> Open-source tooling for AI/ML medical device submissions to the U.S. FDA.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)](https://github.com/lal-jaouni/fda-samd-toolkit)

Building AI/ML for healthcare? FDA Software-as-a-Medical-Device (SaMD) submissions require specific documentation that doesn't exist in any open-source form. This toolkit fills that gap.

## What's in here

| Component | Status | Description |
|-----------|--------|-------------|
| **PCCP Generator** | In development | Predetermined Change Control Plan generator (FDA Dec 2024 guidance) |
| **510(k) AI/ML Templates** | Planned | Markdown templates for AI/ML-specific 510(k) sections |
| **Model Card Generator** | Planned | Clinical-context model cards (extends Mitchell et al. 2019 for FDA) |
| **Validation Framework** | Planned | Pre-deployment clinical validation test plans |
| **Submission Checklist** | Planned | Pre-submission readiness checker for AI/ML 510(k) |

## Quick start

```bash
pip install fda-samd-toolkit

# Generate a Predetermined Change Control Plan from a YAML config
fda-samd pccp generate --config my_device.yaml --output PCCP.md

# Validate a PCCP for completeness against FDA guidance
fda-samd pccp validate --file PCCP.md

# Generate a clinical model card
fda-samd model-card generate --config model_config.yaml
```

See [`examples/`](examples/) for ready-to-modify configurations.

## Why this exists

Most AI/ML startups submitting to FDA are flying blind:

- The PCCP guidance (finalized Dec 2024) is 25 pages of regulatory text with no concrete templates
- 510(k) AI/ML-specific sections (intended use, performance, training data characterization) have no public templates
- Model cards exist but none address FDA-specific concerns (data drift monitoring, sub-population performance, indications for use)
- Companies pay regulatory consultants $300-500/hr to assemble what could be templated

This toolkit puts that scaffolding in the open so small teams can ship faster and iterate on real product instead of regulatory minutiae.

## Who this is for

- AI/ML startups preparing a first 510(k) submission
- Regulatory consultants who want to standardize their deliverables
- Researchers translating clinical AI to deployed products
- Hospital innovation teams piloting AI tools

## Roadmap

**v0.1 (current)**: PCCP generator + first 510(k) section templates
**v0.2**: Model card generator with FDA-specific fields
**v0.3**: Clinical validation framework
**v0.4**: Submission readiness checker
**v1.0**: All components stable, with worked examples for 3 device classes

## Disclaimer

This toolkit produces document scaffolding. It is **not legal, regulatory, or medical advice**. Every FDA submission requires review by qualified regulatory professionals. Generated documents must be customized to your specific device, intended use, and clinical context. The maintainers assume no liability for submissions made using this tool.

## Contributing

This project welcomes contributions from the regulatory and AI/ML community. See [CONTRIBUTING.md](docs/contributing.md).

Areas where help is needed:
- Real-world PCCP examples (anonymized)
- Worked 510(k) AI/ML examples by therapy area
- Validation protocol templates for specific modalities (imaging, signals, NLP)
- IEC 62304 mapping for ML pipelines

## License

MIT -- use freely in commercial products. Attribution appreciated but not required.

## Acknowledgments

Built on top of:
- [FDA AI/ML Action Plan (2021)](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-software-medical-device)
- [FDA PCCP Final Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [IMDRF SaMD Framework](https://www.imdrf.org/working-groups/software-medical-device-samd)
- [Mitchell et al. 2019: Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)
