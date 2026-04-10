# Quality Assurance Strategy

This document describes the testing philosophy, coverage targets, and quality gates for the FDA SaMD Toolkit.

## Test Pyramid

The toolkit follows Google's test pyramid: most tests are unit tests (fast, focused), with integration tests for cross-module concerns, golden file tests to prevent output regression, smoke tests for CLI commands, and end-to-end tests for critical user journeys.

### Unit Tests (70-80% of test count)
- Test individual functions and classes in isolation
- Mock external dependencies (files, APIs, network calls)
- Run in <100ms each
- Located in `tests/` with matching module structure
- Focus on schemas, validators, and generator logic

### Integration Tests (15-20% of test count)
- Test one integration point at a time (e.g., generator + template rendering)
- Use real YAML configuration files from `examples/`
- Verify output structure and content
- Run in <1 second each
- Located in `tests/integration/`

### Golden File Tests (5-10% of test count)
- Prevent accidental regressions in template output
- Compare generator output against stored reference files
- Located in `tests/golden/` with reference files in `tests/golden/data/`
- Regenerate only when template changes are intentional
- Fail the build if output differs from golden file

### Smoke Tests (per CLI command)
- Quick checks that CLI commands accept arguments and produce output
- Located in `tests/test_cli.py`
- Part of unit test runs

### End-to-End Tests (5% of test count)
- Test critical user journeys via the worked example (CardioGuard ECG-AI)
- Run every generator on the example config
- Verify outputs are valid, contain required sections
- Located in `tests/integration/test_full_pipeline.py`

## Current Coverage Level

As of the last measurement:
- **Overall coverage: 74%**
- Generators (PCCP, model cards, validation, checklist): 87% average
- CLI: 70%
- Templates loader: 0% (covered by golden file tests)
- Checklist runner: 59% (gaps in HTML/PDF export branches)

## Coverage Targets by Component

Coverage thresholds are set at floor(current coverage - 5%) to allow for refactoring while preventing regressions:

- `src/fda_samd_toolkit/pccp/`: >= 98% (generator, validator, schemas are critical)
- `src/fda_samd_toolkit/model_cards/`: >= 95% (schemas and core generation logic)
- `src/fda_samd_toolkit/validation/`: >= 87% (core validation logic)
- `src/fda_samd_toolkit/checklist/`: >= 55% (runner has optional HTML/PDF branches tested separately)
- `src/fda_samd_toolkit/cli.py`: >= 65% (many branches are integration tested, not unit tested)
- `src/fda_samd_toolkit/templates_510k/`: excluded from coverage (tested via golden files)

Global threshold: >= 70%

These targets are enforced by the coverage gate in CI (see [running coverage locally](#running-coverage-locally)).

## Mutation Testing

Mutation testing verifies that our tests actually catch bugs, not just exercise code. A mutation introduces a small change (e.g., `>` becomes `>=`), and if a test fails, the mutation is "killed." We target >= 70% kill rate on critical logic.

### What to Mutate
- Schema validation logic (`*/schemas.py`): rules that enforce FDA requirements
- Generator logic (`*/generator.py`): template rendering and output structure
- Validation rules (`validation/generator.py`): FDA compliance checks

### What NOT to Mutate
- CLI argument parsing (tested via Click integration tests)
- Template content (tested via golden files, not mutation)
- Checklist item lists (tested via golden files)

### Running Mutation Testing
Mutation testing is slow (2-5 minutes per component) and is run on a weekly schedule, not per-PR:

```bash
mutmut run --path src/fda_samd_toolkit/pccp/schemas.py --tests tests/pccp/
mutmut run --path src/fda_samd_toolkit/pccp/generator.py --tests tests/pccp/
# See docs/quality.md for full mutation workflow
```

Results are posted as a weekly CI report. Target: >= 70% kill rate for each critical module.

## When Tests Are Required

Every pull request must include tests for:

1. **New feature**: unit test(s) for the feature, integration test if it involves multiple modules
2. **Schema change**: unit tests validating the new/changed fields
3. **Template change**: update the golden file and commit the new output
4. **CLI command change**: update CLI smoke test or add new test for new command
5. **Generator change**: update golden file and add unit tests for the logic change
6. **Bug fix**: regression test that would have caught the bug

Optional but encouraged:
- Golden file regression test for any template or output format change
- Mutation test for critical schema validation logic (run locally before PR)

## Test Naming Conventions

Tests follow Google's AAA pattern (Arrange, Act, Assert) with names in the format:

```python
class Test<ComponentName>:
    """Test <component> functionality."""

    def test_<methodName>_<stateUnderTest>_<expectedBehavior>(self):
        """One-line description of scenario and assertion."""
```

Examples:
- `test_pccp_generator_valid_config_produces_markdown()`
- `test_model_card_schemas_missing_fda_field_raises_validation_error()`
- `test_validation_plan_generator_empty_device_name_produces_empty_device_section()`

## Fixture Conventions

Reusable fixtures are in `tests/conftest.py`:

```python
@pytest.fixture
def cardioguard_pccp_yaml():
    """Load the CardioGuard ECG-AI PCCP example."""
    with open("examples/cardioguard-ecg-ai/pccp.yaml") as f:
        return yaml.safe_load(f)
```

Fixtures should:
- Be as small as possible (test one concern)
- Use descriptive names matching their content
- Live in `conftest.py` if reused across multiple test files
- Include a docstring explaining what they provide

## Running Tests Locally

### Full test suite
```bash
uv run pytest
```

### With coverage report
```bash
uv run pytest --cov=src/fda_samd_toolkit --cov-report=term-missing
```

### HTML coverage report
```bash
uv run pytest --cov=src/fda_samd_toolkit --cov-report=html
# Open htmlcov/index.html in your browser
```

### Golden file tests only
```bash
uv run pytest tests/golden/
```

### Integration tests only
```bash
uv run pytest tests/integration/
```

### Run tests matching a pattern
```bash
uv run pytest -k "pccp" -v
```

### Run a single test file
```bash
uv run pytest tests/test_cli.py
```

### Run with verbose output
```bash
uv run pytest -v
```

### Regenerate golden files (after intentional template changes)
```bash
uv run pytest tests/golden/ --update-golden
```

## Adding a Test for a New Feature

Follow this checklist for a new generator or feature:

1. **Write the unit tests first** (TDD style):
   - Create `tests/<module>/test_<feature>.py`
   - Test schema validation for valid and invalid inputs
   - Test the generator with example config
   - Test error handling and edge cases

2. **Write the feature code** to make tests pass

3. **Add an integration test** if it spans modules:
   - Add to `tests/integration/test_full_pipeline.py` or create a new file
   - Use the CardioGuard example or create a new example YAML
   - Verify the output structure and content

4. **Create a golden file test**:
   - Add `tests/golden/test_<feature>_golden.py`
   - Run the generator on the CardioGuard example
   - Save output to `tests/golden/data/<feature>/cardioguard.md`
   - Assert output matches the golden file

5. **Add CLI smoke test** (if exposed via CLI):
   - Add test case to `tests/test_cli.py` in the appropriate test class
   - Verify the command accepts arguments and returns success

6. **Update CHANGELOG.md**:
   - Add entry under `[Unreleased]` section
   - Follow convention: "Add <feature description>" or "Fix <bug description>"

7. **Update docs**:
   - Add usage example to README or docs/
   - Document new CLI command with `fda-samd <cmd> --help`

## Test Quality Checks

Every test should pass these checks before it's committed:

- **Does it fail when the feature breaks?** Run the test, break the code, verify the test fails. If not, the test isn't testing the right thing.
- **Does the test name describe the scenario?** A reviewer should understand what the test checks without reading the test body.
- **Is there one assertion concern per test?** If a test checks 5 things, split it into 5 tests.
- **Is the test independent?** No shared mutable state, no test order dependencies.
- **Does it run in <1 second?** If not, it belongs in integration tests or should be split.
- **Are there any `if` statements in the test?** Conditional logic in tests causes flakiness. Use parametrized tests instead.

## Anti-Patterns

Avoid these patterns in tests:

- **Testing implementation details**: Test what the code does, not how it does it. If the test breaks when you refactor without changing behavior, it's testing the wrong thing.
- **Assertion-free tests**: A test that doesn't assert anything is not a test.
- **Flaky tests**: If a test fails intermittently, fix it or delete it immediately. Flaky tests erode confidence in the entire suite.
- **Shared mutable state**: Use fixtures or factories, not class attributes or module-level state.
- **Testing the mock instead of the real code**: Mock external dependencies (files, APIs), not the code you're testing.
- **Copy-paste test setup**: Use fixtures or a builder pattern, not copy-pasted test data.

## Coverage Exclusions

The following code is excluded from coverage because it's tested via other means:

- `src/fda_samd_toolkit/templates_510k/`: Tested via golden files, not unit tests
- `tests/`: Test code is not counted
- `examples/`: Examples are working test inputs, not production code
- `*/__init__.py`: Typically empty or re-exports tested elsewhere
- `__main__.py` entries: Tested via CLI smoke tests

## CI/CD Integration

This quality framework is enforced by GitHub Actions:

- **ci.yml**: Runs on every PR and push to main/master
  - Lint check (ruff)
  - Format check (ruff format)
  - Type check (pyright)
  - Unit and integration tests
  - Coverage gate (fail if below threshold)
  - Test report upload

- **quality.yml**: Runs weekly (Monday 6am UTC)
  - Mutation testing on critical schemas and generators
  - Full test suite on Python 3.12 only
  - Weekly coverage report

See [.github/workflows/](../.github/workflows/) for workflow definitions.

## Reference Links

- [Pytest documentation](https://docs.pytest.org/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Mutmut documentation](https://mutmut.readthedocs.io/)
- [Google Testing Philosophy](https://abseil.io/resources/practices)
- [FDA AI/ML Software as a Medical Device Guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-and-machine-learning-software-medical-device)
