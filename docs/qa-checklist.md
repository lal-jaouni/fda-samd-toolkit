# PR QA Checklist

Use this checklist for every pull request. Copy and paste into the PR description or as a review comment.

## Testing

- [ ] New feature: added unit test(s) covering happy path and edge cases
- [ ] New feature: added integration test or golden file test
- [ ] Schema change: added validation tests for new/changed fields
- [ ] Template change: regenerated golden file with `pytest tests/golden/ --update-golden`
- [ ] CLI command change: added or updated CLI smoke test in `tests/test_cli.py`
- [ ] Bug fix: added regression test that would have caught the bug
- [ ] All existing tests pass: `uv run pytest`

## Coverage and Quality Gates

- [ ] Coverage maintained or improved (run `uv run pytest --cov=src/fda_samd_toolkit` locally)
- [ ] No new lint warnings: `uv run ruff check src tests` passes
- [ ] Code is formatted: `uv run ruff format src tests` passes
- [ ] Type hints added for new functions: `uv run pyright src tests` passes
- [ ] No circular imports or unresolved references

## Documentation

- [ ] New feature documented in README.md or relevant docs/ file
- [ ] New CLI command: included in `docs/` or help text is self-documenting
- [ ] CHANGELOG.md updated: added entry under `[Unreleased]` section
- [ ] Docstrings added for new public functions, classes, modules

## Code Quality

- [ ] Code follows PEP 8 (100-character line limit, double quotes)
- [ ] No hardcoded paths or credentials
- [ ] Error messages are clear and actionable
- [ ] No commented-out code or debug print statements

## Golden Files and Output Regression

- [ ] If templates changed: golden files regenerated and committed
- [ ] If output format changed: golden files updated intentionally
- [ ] Golden file diffs are reviewed to ensure intentional changes only

## Integration and Compatibility

- [ ] Tested on Python 3.11 (CI will verify 3.12)
- [ ] No breaking changes to public APIs (or clearly documented if intentional)
- [ ] Backwards compatible with existing YAML configs (if applicable)

## Pre-Merge Verification

Before clicking merge:

1. All required status checks pass (CI workflows)
2. At least one approval from a maintainer
3. No merge conflicts
4. Branch is up-to-date with main/master

## Notes for Reviewers

- Verify that tests match the implementation changes
- Check that golden file diffs are intentional and correct
- Ensure coverage thresholds are still met
- Look for missing test cases in complex logic branches
