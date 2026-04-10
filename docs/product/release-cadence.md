# Release Cadence and Planning

This document defines how and when features ship, including version strategy, breaking change communication, and the release process.

## Version Strategy

The FDA SaMD Toolkit follows semantic versioning (semver): `MAJOR.MINOR.PATCH`.

### Semver Interpretation for This Project

| Version Bump | Trigger | Examples | User Impact |
|---|---|---|---|
| **MAJOR** (e.g., 0.1 -> 1.0) | Stability milestone (v1.0 = 3 device classes + all v0.2 features + 1+ real submission) OR breaking API change | v0.1 -> v1.0: IEC 62304 integration + working examples for imaging AI | Users must review CHANGELOG carefully; may require minor code changes |
| **MINOR** (e.g., 0.1 -> 0.2) | New feature added (must-use or quick-win); no breaking changes to public API | v0.1 -> v0.2: +5 features (SBOM, bias, monitoring, eSTAR, IEC 62304) | Drop-in upgrade; no user code changes required |
| **PATCH** (e.g., 0.1.1) | Bug fixes, documentation updates, or schema clarifications | Fix PCCP generator crash on custom field input | Drop-in upgrade; no user code changes required |

### Pre-v1.0: YAML Schema Stability

YAML input schemas (e.g., `pccp.yaml`, `model_card.yaml`) are NOT considered breaking until v1.0. This means:
- Adding optional fields to YAML: PATCH or MINOR
- Renaming YAML fields: MINOR (new field added; old field deprecated)
- Removing YAML fields without deprecation: MINOR only if tooling gracefully warns users

After v1.0, YAML schema changes require MAJOR version bump.

### Public API (Python Module)

Python imports are considered public API:
```python
from fda_samd_toolkit.generators import PCCPGenerator
from fda_samd_toolkit.models import ModelCard
```

Renames or removals of public classes/functions require MAJOR version bump.

### CLI Commands

CLI subcommands (`fda-samd pccp`, `fda-samd model-card`, etc.) are considered public API. Renaming or removing subcommands requires MAJOR version bump.

---

## Release Timeline: v0.2 Through v1.0

### v0.2: Target Ship Date: May 24, 2026

**Effort estimate**: ~50 days across 5 parallel or serial issues

| Issue | Feature | Effort | Type | Ship date (serial) | Ship date (parallel) |
|---|---|---|---|---|---|
| #14 | Cybersecurity SBOM Generator | 5 days | quick-win | May 3 | May 3 |
| #15 | Bias & Subpopulation Report | 5 days | quick-win | May 10 | May 3 |
| #16 | Real-World Monitoring Plan | 5 days | quick-win | May 17 | May 3 |
| #17 | eSTAR Package Builder | 10 days | big-bet | May 31 | May 10 |
| #18 | IEC 62304 + ISO 14971 | 10 days | big-bet | June 7 | May 17 |

**Recommended execution**: Ship quick wins in parallel (week 1), start big bets in parallel (weeks 2-3), aim for full v0.2 completion by end of May 2026.

**Definition of done**: All 5 issues closed, milestone v0.2 achieved, CHANGELOG entry, blog post highlighting new features, PyPI release.

### v0.3: Target Ship Date: Late July 2026

**Planned features** (candidates from research/must_use_features.md):
- Validation protocol generator for imaging AI (X-ray triage, CT screening)
- Validation protocol generator for NLP/EHR AI (clinical risk prediction)
- GMLP (Good Machine Learning Practice) mapping and evidence templates
- Regulatory intelligence ingestion (auto-update toolkit when FDA guidance changes)
- Worked example for imaging AI (build on CardioGuard pattern)
- Worked example for NLP/EHR AI

**Effort**: ~4-6 weeks
**Rationale**: v0.3 consolidates device-class coverage (cardiac complete in v0.2, imaging + NLP in v0.3), positioning for v1.0 stability.

### v1.0: Target Ship Date: January 2027

**Success criteria** (see docs/product/v1.0-definition.md for full details):
- 3 stable device classes with worked examples (cardiac, imaging, NLP)
- All v0.2 components shipped and stable (semver stability guarantees)
- 1+ external contributor
- 1+ real FDA submission citing the toolkit
- Full documentation coverage (every component has guide + API reference)
- 200+ unit tests with golden file validation infrastructure

---

## Release Cut Criterion: Time-Boxed vs Feature-Boxed

### v0.2: Feature-Boxed

**Cut criterion**: Don't ship v0.2 until all 5 issues (#14-#18) are closed and merged.

**Rationale**: Each feature is independently valuable and mandatory per FDA guidance. Shipping incomplete feature set (e.g., SBOM without bias report) leaves gaps in submission scaffolding. Features are not interdependent, so sequential delays don't block others.

**Risk**: If one issue (e.g., #17 eSTAR package builder) gets blocked or extended, full v0.2 ships late. Mitigation: Break #17 into smaller sub-issues; ship SBOM, bias, monitoring as v0.2 early release if eSTAR slips.

### v0.3+: Time-Boxed

**Cut criterion**: Freeze features at T-2 weeks; ship whatever's ready by target date.

**Rationale**: v0.3 features are improvements and device-class additions, not mandatory blockers. Time-boxing prevents indefinite feature creep and maintains quarterly cadence.

**Process**:
1. Set target release date (e.g., July 28, 2026 for v0.3)
2. At T-2 weeks (July 14), freeze feature additions
3. Use final 2 weeks for testing, documentation, bug fixes
4. Release on target date regardless of feature completion (unfinished features move to v0.4)

---

## Breaking Change Communication

When a breaking change is necessary (MAJOR version bump or late-v0.x MINOR schema change):

### 1. Deprecation Warnings (Optional, MINOR only)

For pre-v1.0 YAML schema changes, add a deprecation notice 1 release ahead:

```yaml
# Example: model_card.yaml v0.1
# DEPRECATED: 'model_version' renamed to 'version' in v0.2
# Please update your YAML by release v0.3 (April 30, 2026)
model_version: "1.0"  # Use 'version' instead
```

Tooling accepts both old and new field names but prints warning:
```
⚠️  model_card.yaml: 'model_version' is deprecated. Use 'version' instead (v0.3 required).
```

### 2. CHANGELOG Entry

Every breaking change gets a prominent entry:

```markdown
# Unreleased

## Breaking Changes

- **YAML Schema**: `model_card.yaml` field renamed `model_version` -> `version` (v0.1 still accepts old field with deprecation warning)
  - Migration: Rename `model_version:` to `version:` in your YAML files
  - Deprecation timeline: Old field supported through v0.2; removed in v0.3
  - Reference: See [upgrade guide](docs/upgrading/v0.1-to-v0.2.md)

## Features

- ...
```

### 3. Upgrade Guide (For Major Breaks)

For MAJOR version bumps, create a new file: `docs/upgrading/v{old}-to-v{new}.md`

```markdown
# Upgrading from v0.2 to v1.0

## What Changed

...

## Migration Checklist

- [ ] Update imports: `from fda_samd_toolkit_v2` -> `from fda_samd_toolkit`
- [ ] Re-run tests against new schema
- [ ] Review CHANGELOG for API changes

## Getting Help

- GitHub Issues: #XXX
- Discussions: [link]
```

### 4. Release Notes

Announce breaking changes prominently in release notes:

```
# v1.0.0 (January 15, 2027)

🚨 **BREAKING CHANGES**: This release includes major API changes. See [upgrade guide](docs/upgrading/v0.2-to-v1.0.md).

... (other content)
```

---

## Release Process Steps

Executed by maintainer when cutting a release:

### 1. Verify Milestone Completion

```bash
cd /home/laith/workspaces/fda-samd-toolkit
git checkout master
git pull origin master

# Check milestone: all issues closed?
gh milestone view v0.2
```

### 2. Update Version Number

Update in `pyproject.toml` and `src/fda_samd_toolkit/__init__.py`:

```toml
# pyproject.toml
[project]
version = "0.2.0"
```

```python
# src/fda_samd_toolkit/__init__.py
__version__ = "0.2.0"
```

### 3. Update CHANGELOG

Move `[Unreleased]` section to release date:

```markdown
# Changelog

## [0.2.0] - 2026-05-24

### Added
- Cybersecurity SBOM generator (NTIA format) #14
- Bias and subpopulation performance report generator #15
- Real-world performance monitoring plan generator #16
- eSTAR submission package builder #17
- IEC 62304 + ISO 14971 template integration #18

### Changed
- Model card YAML schema: added `subpopulation_performance` field

### Fixed
- PCCP generator crash on custom risk fields #12

## [0.1.0] - 2026-04-10

... (previous releases)
```

### 4. Create Git Tag

```bash
git tag -a v0.2.0 -m "Release v0.2.0: Must-have features for 510(k) submissions"
git push origin v0.2.0
```

### 5. Build and Test

```bash
python -m pytest tests/ -v
python -m build
twine check dist/*
```

### 6. Release to PyPI

```bash
twine upload dist/* --verbose
```

Verify:
```bash
pip install --upgrade fda-samd-toolkit==0.2.0
fda-samd --version
```

### 7. Create GitHub Release

```bash
gh release create v0.2.0 \
  --title "v0.2.0: Must-Have Features for FDA 510(k)" \
  --notes "$(cat <<'EOF'
## Must-Use Features

Five features that solve acute regulatory pain points:

- **Cybersecurity SBOM Generator**: Machine-readable SBOM (NTIA format) required by June 2025 FDA guidance
- **Bias Evaluation Report**: Demographic breakdowns (race, ethnicity, sex, age) per Jan 2025 FDA guidance
- **Real-World Monitoring Plan**: Post-market data sources, metrics, and escalation procedures
- **eSTAR Package Builder**: Auto-assemble FDA submission files into mandatory eSTAR format
- **IEC 62304 + ISO 14971**: Integrate OpenRegulatory software lifecycle and risk management templates

See [docs/product/metrics.md](docs/product/metrics.md) for expected impact.

## Migration Notes

No breaking changes. Update via `pip install --upgrade fda-samd-toolkit`.

## Contributors

Thanks to [list of contributors].
EOF
)"
```

### 8. Announce Release

- Update README.md badge (status-v0.2 released)
- Post on Twitter/LinkedIn: "FDA SaMD Toolkit v0.2 ships with 5 must-have features for 510(k) submissions: SBOM, bias evaluation, monitoring plan, eSTAR, IEC 62304."
- Blog post (if applicable): case study or feature deep-dive
- Email to known users (if applicable): "Your toolkit is ready to upgrade"

---

## Communication Channels for Breaking Changes

If a MAJOR breaking change is planned:

1. **GitHub Discussion**: Announce 4-6 weeks ahead with migration plan
2. **Deprecation warnings in code**: Add in MINOR release 1-2 releases ahead
3. **Blog post**: Detailed migration guide and rationale
4. **Email to PyPI-tracked users** (if possible): Direct notification
5. **Release notes and CHANGELOG**: Prominent placement, link to upgrade guide

---

## Cadence Rationale

- **v0.2 by end of May 2026**: Capitalize on momentum from v0.1 launch; fulfill must-use features research
- **v0.3 by late July 2026**: Expand device-class coverage (imaging, NLP) ahead of H2 2026 customer engagement
- **v1.0 by January 2027**: Stability and real adoption signals (north-star metric: 3+ real submissions citing toolkit)
- **Quarterly thereafter**: Maintenance releases and refinements

This cadence balances feature velocity against documentation quality and test coverage. It assumes:
- 1-2 maintainers or core contributors
- Parallel work on parallel features where possible
- Regular community feedback loop (GitHub Discussions, issues)
