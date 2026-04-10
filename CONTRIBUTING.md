# Contributing to FDA SaMD Toolkit

Thanks for your interest in contributing! This guide will help you set up your development environment and submit high-quality PRs.

## Development Setup

### Prerequisites

- Python 3.11 or 3.12
- Git
- uv (install via: `pip install uv`)

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/lal-jaouni/fda-samd-toolkit.git
   cd fda-samd-toolkit
   ```

2. Install the package in development mode with all dev dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

3. Verify installation:
   ```bash
   fda-samd --version
   fda-samd --help
   ```

## Running Tests

Run the full test suite:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_cli.py
```

Run tests matching a pattern:
```bash
pytest -k "pccp" -v
```

## Code Quality

We use ruff for linting and formatting, and pyright for type checking.

### Linting

Check for lint issues:
```bash
ruff check src tests
```

Fix linting issues automatically (where possible):
```bash
ruff check --fix src tests
```

### Formatting

Check formatting:
```bash
ruff format --check src tests
```

Auto-format code:
```bash
ruff format src tests
```

### Type Checking

Run type checker:
```bash
pyright src tests
```

## Submitting a Pull Request

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and commit with clear, descriptive messages:
   ```bash
   git add .
   git commit -m "Add feature description"
   ```

3. Ensure all checks pass locally:
   ```bash
   ruff check src tests
   ruff format --check src tests
   pyright src tests
   pytest
   ```

4. Push to your fork and create a pull request:
   ```bash
   git push origin feature/my-feature
   ```

5. In your PR description, explain:
   - What problem does this solve?
   - How did you test it?
   - Any breaking changes?

## Code Style Guidelines

- Follow PEP 8 with a line length limit of 100 characters (enforced by ruff)
- Use double quotes for strings (enforced by ruff)
- Add docstrings to all public functions, classes, and modules
- Type hint function signatures where possible
- Write tests for new functionality (aim for >80% coverage)
- Use clear variable and function names

## Commit Message Guidelines

- Start with a verb (Add, Fix, Update, Refactor, etc.)
- Keep the first line under 70 characters
- Explain the "why" not just the "what" in the body
- Reference issues if applicable: "Fixes #123"

Example:
```
Add PCCP validation module

Implements schema validation against FDA regulatory requirements,
including device classification checks and modification scope limits.

Fixes #15
```

## Architecture Overview

The toolkit is organized into functional modules:

- `src/fda_samd_toolkit/pccp/` - Post-market continuous learning plans
  - `schemas.py` - Pydantic models for PCCP configuration
  - `generator.py` - PCCP document generation (in development)

- `src/fda_samd_toolkit/templates_510k/` - 510(k) submission templates
  - Template loading and customization

- `src/fda_samd_toolkit/model_cards/` - AI/ML model cards
  - Model documentation framework

- `src/fda_samd_toolkit/validation/` - Regulatory validation
  - FDA compliance checking

- `src/fda_samd_toolkit/cli.py` - Command-line interface
  - Click-based CLI with Rich output

## Testing Guidelines

- Write tests for new features and bug fixes
- Use descriptive test names: `test_<feature>_<scenario>`
- Group related tests into classes for organization
- Test both success and error cases
- Mock external dependencies

Example test structure:
```python
class TestNewFeature:
    """Test new feature functionality."""

    def test_basic_behavior(self):
        """Test normal operation."""
        result = function()
        assert result is True

    def test_error_handling(self):
        """Test error case."""
        with pytest.raises(ValueError):
            function(invalid_input)
```

### Running Golden File Tests

Golden file tests detect unintended regressions in template and generator output:

```bash
# Run golden file tests
uv run pytest tests/golden/

# Regenerate golden files after intentional template changes
uv run pytest tests/golden/ --update-golden
```

### Running Integration Tests

Integration tests verify that multiple components work together correctly:

```bash
# Run integration tests
uv run pytest tests/integration/

# Run a specific integration test
uv run pytest tests/integration/test_full_pipeline.py::TestFullPipeline::test_pccp_pipeline_ecg_classifier
```

### Mutation Testing

Mutation testing verifies that our tests actually catch bugs. Run locally before submitting:

```bash
# Run mutation testing on a specific module (takes 2-5 minutes)
uv run mutmut run --path src/fda_samd_toolkit/pccp/schemas.py --tests tests/pccp/
```

For details on the QA strategy, coverage targets, and when tests are required, see [docs/quality.md](docs/quality.md).

## Adding a New Feature

Follow this workflow to ship a new generator, CLI command, or major feature:

1. **Create a feature branch** from master:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Write tests first** (TDD):
   - Add unit tests in `tests/<module>/test_<feature>.py`
   - Test schemas, validation, and generator logic
   - Test error cases and edge cases
   - Run tests: `uv run pytest tests/<module>/test_<feature>.py -v`

3. **Implement the feature**:
   - Add schema in `src/fda_samd_toolkit/<module>/schemas.py`
   - Add generator/logic in `src/fda_samd_toolkit/<module>/generator.py`
   - Add CLI command in `src/fda_samd_toolkit/cli.py` if user-facing

4. **Add integration tests**:
   - Add to `tests/integration/test_full_pipeline.py` or create a new file
   - Test with example YAML configs from `examples/`
   - Verify the full workflow end-to-end

5. **Create golden files** (if output format changed):
   - Run the generator on an example: `uv run python -c "from ... import generate_...; generate_...('examples/example.yaml', 'output.md')"`
   - Save output to `tests/golden/data/<module>/<example>.md`
   - Create golden file test in `tests/golden/test_<module>_golden.py`

6. **Add CLI tests** (if new command):
   - Add test class to `tests/test_cli.py`
   - Test command help, missing args, invalid inputs, and happy path

7. **Verify coverage and quality**:
   - Run full test suite: `uv run pytest`
   - Check coverage: `uv run pytest --cov=src/fda_samd_toolkit --cov-report=term-missing`
   - Run linter: `uv run ruff check src tests`
   - Run formatter: `uv run ruff format src tests`
   - Run type checker: `uv run pyright src tests`

8. **Update documentation**:
   - Update README.md with usage example
   - Add docstrings to all public functions, classes, modules
   - Document CLI commands in help text (shown by `fda-samd <cmd> --help`)

9. **Update CHANGELOG.md**:
   - Add entry under `[Unreleased]` section
   - Use format: "Add <feature description>" or "Fix <bug description>"

10. **Commit and push**:
    ```bash
    git add .
    git commit -m "Add feature description
    
    Detailed explanation of changes, implementation approach,
    and any design decisions."
    git push origin feature/my-feature
    ```

11. **Create pull request**:
    - Use the QA checklist from [docs/qa-checklist.md](docs/qa-checklist.md)
    - Link to relevant issues
    - Wait for CI to pass and code review

12. **Address review feedback**:
    - Make requested changes
    - Push follow-up commits (don't force-push unless asked)
    - Re-request review

## Reporting Issues

Use GitHub Issues to report bugs or suggest features:

- **Bug Report**: Include reproduction steps, expected behavior, and actual behavior
- **Feature Request**: Explain the use case and expected benefits
- **Question**: Ask in Discussions rather than Issues if unsure

## Questions?

Check the README for general information or open a GitHub Discussion for questions.

Thank you for contributing!
