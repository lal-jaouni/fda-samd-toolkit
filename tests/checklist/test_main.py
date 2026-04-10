"""Tests for the checklist CLI entry point (__main__.py)."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from fda_samd_toolkit.checklist.__main__ import main


@pytest.fixture
def runner():
    return CliRunner()


class TestChecklistMainHelp:
    """Basic CLI surface tests."""

    def test_help_flag(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "FDA SaMD Submission Readiness Checklist" in result.output
        assert "--yaml" in result.output
        assert "--output" in result.output
        assert "--device-name" in result.output

    def test_missing_yaml_triggers_interactive_mode(self, runner):
        """Without --yaml, the command falls through to run_interactive()."""
        with patch("fda_samd_toolkit.checklist.__main__.run_interactive") as mock_interactive:
            mock_interactive.return_value = _make_fake_report()
            result = runner.invoke(main, ["--device-name", "Test Device"])
            assert result.exit_code == 0
            mock_interactive.assert_called_once()


class TestChecklistMainFromYAML:
    """Test the YAML-config code path."""

    def test_loads_from_yaml_config(self, runner):
        """Running with --yaml calls run_from_yaml and prints the report."""
        example_yaml = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"
        if not example_yaml.exists():
            pytest.skip("Example YAML not found")

        result = runner.invoke(main, ["--yaml", str(example_yaml), "--device-name", "Test Device"])
        assert result.exit_code == 0

    def test_writes_markdown_output_when_requested(self, runner):
        """--output should write a markdown file to the specified path."""
        example_yaml = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"
        if not example_yaml.exists():
            pytest.skip("Example YAML not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"
            result = runner.invoke(
                main,
                [
                    "--yaml",
                    str(example_yaml),
                    "--device-name",
                    "Test Device",
                    "--output",
                    str(output_path),
                ],
            )
            assert result.exit_code == 0
            assert output_path.exists()
            content = output_path.read_text(encoding="utf-8")
            assert len(content) > 100


class TestChecklistMainErrorHandling:
    """Test the exception handlers in main()."""

    def test_file_not_found_exits_nonzero(self, runner):
        """Click's Path(exists=True) rejects missing files before main() sees them."""
        result = runner.invoke(main, ["--yaml", "/nonexistent/checklist.yaml"])
        # Click's built-in validation gives exit code 2 for invalid options
        assert result.exit_code != 0

    def test_run_from_yaml_file_not_found_handled(self, runner):
        """If run_from_yaml raises FileNotFoundError, main() catches it with exit code 1."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("name: test\n")
            tmp_path = f.name

        try:
            with patch(
                "fda_samd_toolkit.checklist.__main__.run_from_yaml",
                side_effect=FileNotFoundError("missing"),
            ):
                result = runner.invoke(main, ["--yaml", tmp_path])
            assert result.exit_code == 1
            assert "Error" in result.output
        finally:
            Path(tmp_path).unlink()

    def test_run_from_yaml_value_error_handled(self, runner):
        """If run_from_yaml raises ValueError, main() catches it with exit code 1."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("name: test\n")
            tmp_path = f.name

        try:
            with patch(
                "fda_samd_toolkit.checklist.__main__.run_from_yaml",
                side_effect=ValueError("bad config"),
            ):
                result = runner.invoke(main, ["--yaml", tmp_path])
            assert result.exit_code == 1
            assert "Error" in result.output
            assert "bad config" in result.output
        finally:
            Path(tmp_path).unlink()

    def test_keyboard_interrupt_exits_zero(self, runner):
        """Ctrl-C during interactive mode exits cleanly with exit code 0."""
        with patch(
            "fda_samd_toolkit.checklist.__main__.run_interactive",
            side_effect=KeyboardInterrupt(),
        ):
            result = runner.invoke(main, [])
        assert result.exit_code == 0
        assert "cancelled" in result.output.lower()


def _make_fake_report():
    """Construct a minimal ReadinessReport-compatible object for mocking."""
    from fda_samd_toolkit.checklist.schemas import CategoryResult, ReadinessReport

    return ReadinessReport(
        device_name="Mock Device",
        timestamp="2026-01-01T00:00:00Z",
        categories=[
            CategoryResult(
                category="Mock Category",
                total=1,
                complete=1,
                partial=0,
                missing=0,
                items=[],
            )
        ],
        overall_pct=100.0,
    )
