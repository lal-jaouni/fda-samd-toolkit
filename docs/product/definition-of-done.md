# Definition of Done (DoD) Checklist for v0.2 Features

This document defines what "done" means for each v0.2 issue (#14, #15, #16, #17, #18). Every merged PR must satisfy all items in this checklist.

Use this checklist as part of the PR review process. Create a checklist block in the GitHub issue and check off items as work progresses.

---

## DoD Template (Apply to All Issues)

```markdown
## Definition of Done

This PR is ready to merge when:

### Code

- [ ] Component follows v0.1 pattern (Pydantic schema + Jinja templates + generator class)
- [ ] Schema documented with docstrings and field descriptions
- [ ] Generator class has public `generate()` method returning string or dict
- [ ] All custom logic encapsulated in generator (no inline template logic)
- [ ] No hardcoded values; all inputs from YAML config or CLI args
- [ ] Python code formatted with `black` (run `black src/ tests/`)
- [ ] No unused imports or dead code

### Tests

- [ ] At least 20 unit tests written (test schema validation, generator output, edge cases)
- [ ] At least 1 integration test (full YAML config -> output)
- [ ] At least 1 golden file test (output matches expected file, checked into repo)
- [ ] All tests pass: `pytest tests/ -v` green
- [ ] Tests include both happy path and error cases (invalid YAML, missing required fields, etc.)
- [ ] Golden file infrastructure used (see `tests/goldenfiles/` pattern from v0.1)
- [ ] No test skips (xfail) without documented reason

### CLI

- [ ] Subcommand wired into `src/fda_samd_toolkit/cli.py`
- [ ] Subcommand name is verb-noun (e.g., `sbom-generate`, `bias-report`)
- [ ] `--help` works and describes all flags
- [ ] All flags have type hints and default values
- [ ] Graceful error messages for missing required fields
- [ ] If component module not installed, CLI shows helpful error (not traceback)

### Documentation

- [ ] 1 user guide in `docs/guides/` explaining what, when, how to use (500-1000 words)
- [ ] 1 API reference page in `docs/reference/api.md` documenting public classes/methods
- [ ] YAML schema documented in `docs/reference/schema/` with field descriptions and examples
- [ ] README.md updated with section for new component (already done by tech-writer agent, but verify it exists)
- [ ] At least 1 worked example YAML in `examples/cardioguard-ecg-ai/` or similar
- [ ] Examples are runnable: `fda-samd <component> generate --config examples/.../xxx.yaml` works without errors

### Integration

- [ ] Worked example YAML produces valid output
- [ ] Generated output matches expected format (Markdown, JSON, etc.)
- [ ] Example YAML added to CardioGuard example directory
- [ ] CardioGuard README updated to show how to use new component
- [ ] If new component depends on another component, verify integration (e.g., bias report should reference model card)

### Changelog

- [ ] Entry added to `CHANGELOG.md` under `[Unreleased]` section
- [ ] Entry describes feature in user-friendly language (not technical)
- [ ] Entry includes issue number (e.g., "Closes #15")

### Pull Request

- [ ] PR linked to GitHub issue (use `Closes #XX` in PR description)
- [ ] Milestone set to `v0.2`
- [ ] Label `must-use` applied (all v0.2 features are must-use by definition)
- [ ] All CI checks green (GitHub Actions, lint, tests)
- [ ] At least 1 reviewer comment addressed (even if self-review; maintainer should review or explicitly self-approve)
- [ ] No merge until checklist complete

### Acceptance

- [ ] Issue status moved to "Closed" with comment: "Merged in PR #XYZ. See [component guide](link) for usage."
- [ ] GitHub milestone v0.2 now shows N/5 issues closed

---
```

## Component-Specific Notes

### Issue #14: Cybersecurity SBOM Generator

**Additional DoD Items**:
- [ ] SBOM output validates against NTIA JSON schema (https://cyclonedx.org/schema/cyclonedx-1.4.schema.json or similar)
- [ ] Example SBOM includes software components, libraries, and third-party dependencies
- [ ] SBOM field mapping clear (component name, version, license, hashes)
- [ ] CLI flag: `fda-samd sbom-generate --config sbom.yaml --format json --output sbom.json`
- [ ] Supports both JSON and SPDX formats (or document why not)

**Example YAML location**: `examples/cardioguard-ecg-ai/sbom.yaml`

**Test coverage**: Invalid licenses, missing component versions, duplicate components, hash validation

### Issue #15: Bias & Subpopulation Performance Report

**Additional DoD Items**:
- [ ] Report template covers demographics: race, ethnicity, sex, age, BMI (configurable)
- [ ] Performance metrics for each demographic: sensitivity, specificity, AUC, F1 (depends on classification type)
- [ ] Report includes performance parity analysis (difference from overall performance)
- [ ] CLI flag: `fda-samd bias-report generate --config bias.yaml --output bias_report.md`
- [ ] Report format: Markdown with tables and narrative sections
- [ ] Supports regression metrics (MSE, MAE by subgroup) and classification metrics (AUC, F1, sensitivity/specificity by subgroup)

**Example YAML location**: `examples/cardioguard-ecg-ai/bias_evaluation.yaml`

**Test coverage**: Missing demographic groups, invalid metric values, edge cases (100% sensitivity, 0% specificity)

### Issue #16: Real-World Performance Monitoring Plan

**Additional DoD Items**:
- [ ] Monitoring plan covers data sources (EHR, device, claims, patient-reported)
- [ ] Plan includes metrics (sensitivity/specificity, drift, AUC), thresholds (e.g., "alert if sensitivity drops below 92%"), and escalation procedures
- [ ] CLI flag: `fda-samd monitoring-plan generate --config monitoring.yaml --output monitoring_plan.md`
- [ ] Output format: Markdown with structured sections (data ingestion, metrics, thresholds, escalation)
- [ ] Supports both binary classification and regression monitoring
- [ ] Includes drift detection guidance (statistical tests, thresholds)

**Example YAML location**: `examples/cardioguard-ecg-ai/monitoring_plan.yaml`

**Test coverage**: Invalid metric names, missing data sources, threshold conflicts (alert threshold higher than safe threshold)

### Issue #17: eSTAR Submission Package Builder

**Additional DoD Items**:
- [ ] Generates eSTAR folder structure (eSTAR format spec, Oct 2023)
- [ ] Creates manifest file (metadata.json or similar)
- [ ] Validates that all required submission files are present before packaging
- [ ] CLI flag: `fda-samd estar-package generate --config submission_config.yaml --output estar-package/`
- [ ] Output is a directory tree ready for FDA eSubmitter upload
- [ ] Document eSTAR structure expected (e.g., `/submissions/510k-123/form-1571.pdf`, `/submissions/510k-123/modules/...`)
- [ ] No automated upload to eSubmitter (user handles via web UI)
- [ ] Validates PDF presence and naming conventions

**Example YAML location**: `examples/cardioguard-ecg-ai/submission_package.yaml`

**Test coverage**: Missing required files, invalid PDF names, folder structure validation

### Issue #18: IEC 62304 + ISO 14971 Template Integration

**Additional DoD Items**:
- [ ] Integrates OpenRegulatory MIT-licensed templates for IEC 62304 (software lifecycle) and ISO 14971 (risk management)
- [ ] Templates linked in code, not copied (point to OpenRegulatory GitHub)
- [ ] CLI provides guided workflow: `fda-samd lifecycle generate --config iec62304.yaml --output lifecycle_report.md`
- [ ] Risk analysis output: ISO 14971 risk table (hazard, severity, probability, mitigation, residual risk)
- [ ] Software lifecycle output: IEC 62304 SVLM (software version, lifecycle stage, configuration management)
- [ ] Customizable for device risk classification (Class A/B/C)
- [ ] Legal compliance verified (OpenRegulatory MIT license allows integration)

**Example YAML location**: `examples/cardioguard-ecg-ai/iec62304.yaml`

**Test coverage**: Different device risk classes, missing hazards, risk table completeness

---

## Review Checklist for Maintainers

When reviewing a PR:

1. **Run locally**: Clone PR branch, `pip install -e .`, run tests and examples
2. **Check golden files**: New golden files should be committed; outputs should match expected files
3. **Verify documentation**: Read guide and API reference for clarity and completeness
4. **Test CLI**: Run `fda-samd <component> --help` and at least one example
5. **Code quality**: Docstrings present, no dead code, consistent with v0.1 patterns
6. **Integration**: Verify component works with CardioGuard example (or creates new example)
7. **Issue closure**: Confirm PR addresses all acceptance criteria from the issue
8. **Changelog**: Verify CHANGELOG entry is clear and non-technical

### Self-Review Template

If the contributor is also the maintainer (common for v0.2), create a comment on the PR:

```markdown
## Self-Review Checklist

- [ ] Code follows v0.1 component pattern
- [ ] Tests pass: `pytest tests/ -v`
- [ ] Golden files committed and match outputs
- [ ] Documentation complete and readable
- [ ] Example YAML added and runs without errors
- [ ] CHANGELOG updated
- [ ] No breaking changes to v0.1 API

**Approved for merge** (or note blockers if any remain)
```

---

## Closing the Issue

Once PR is merged:

1. **Issue status**: Click "Linked pull request -> Closes this issue" (auto-close on merge)
2. **Issue comment** (optional, for visibility):
   ```
   Merged in #PR_NUM. Feature available in v0.2.0 (release target: May 24, 2026).
   
   Usage:
   ```bash
   fda-samd <component> generate --config examples/xxx.yaml --output output.md
   ```
   
   See docs/guides/<component>.md for detailed guide.
   ```
3. **Milestone**: Verify issue appears in v0.2 milestone as "Closed"

---

## Exception: Partial DoD

In rare cases, a feature may ship with partial DoD if:
- **Blocker removed**: e.g., SBOM schema validation deferred to v0.2.1 if upstream library update is needed
- **Clear path forward**: e.g., "Golden file infrastructure in place; tests added in PR #XX following this PR"

Document the exception in the issue with a comment: "Shipped with partial DoD: [reason]. Follow-up: [next steps]."

Example:
```
Shipped with partial DoD: eSTAR validation deferred pending FDA spec clarification.
Follow-up: Will add file validation in v0.2.1 once spec is released.
Tracking issue: #99
```

---

## v0.3+ DoD

After v1.0, DoD may be expanded (e.g., requiring 30+ tests instead of 20, requiring load testing for CLI). This document reflects v0.2 minimums.
