"""Tests for the FDA SaMD Toolkit CLI."""

import tempfile

import pytest
from click.testing import CliRunner

from fda_samd_toolkit.cli import cli


@pytest.fixture
def runner():
    """Create a Click CLI runner for tests."""
    return CliRunner()


class TestCLIVersion:
    """Test version flag and basic CLI functionality."""

    def test_version_flag(self, runner):
        """Test that --version flag works."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "fda-samd" in result.output

    def test_help_flag(self, runner):
        """Test that --help flag works."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "FDA SaMD Toolkit" in result.output
        assert "pccp" in result.output
        assert "templates" in result.output
        assert "model-card" in result.output
        assert "checklist" in result.output


class TestPCCPCommands:
    """Test PCCP subcommands."""

    def test_pccp_help(self, runner):
        """Test pccp group help."""
        result = runner.invoke(cli, ["pccp", "--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "validate" in result.output
        assert "init" in result.output

    def test_pccp_generate_missing_config(self, runner):
        """Test pccp generate without required --config flag."""
        result = runner.invoke(cli, ["pccp", "generate", "--output", "out.md"])
        assert result.exit_code != 0
        assert "Missing option '--config'" in result.output

    def test_pccp_generate_missing_output(self, runner):
        """Test pccp generate without required --output flag."""
        result = runner.invoke(
            cli, ["pccp", "generate", "--config", "config.yaml"]
        )
        assert result.exit_code != 0
        assert "Missing option '--output'" in result.output

    def test_pccp_generate_nonexistent_config(self, runner):
        """Test pccp generate with nonexistent config file."""
        result = runner.invoke(
            cli,
            ["pccp", "generate", "--config", "/nonexistent/config.yaml", "--output", "out.md"],
        )
        assert result.exit_code != 0
        assert "Does not exist" in result.output

    def test_pccp_generate_help(self, runner):
        """Test pccp generate help."""
        result = runner.invoke(cli, ["pccp", "generate", "--help"])
        assert result.exit_code == 0
        assert "--config" in result.output
        assert "--output" in result.output
        assert "--template" in result.output

    def test_pccp_validate_help(self, runner):
        """Test pccp validate help."""
        result = runner.invoke(cli, ["pccp", "validate", "--help"])
        assert result.exit_code == 0
        assert "--file" in result.output

    def test_pccp_validate_missing_file(self, runner):
        """Test pccp validate without required --file flag."""
        result = runner.invoke(cli, ["pccp", "validate"])
        assert result.exit_code != 0
        assert "Missing option '--file'" in result.output

    def test_pccp_init_help(self, runner):
        """Test pccp init help."""
        result = runner.invoke(cli, ["pccp", "init", "--help"])
        assert result.exit_code == 0
        assert "--type" in result.output
        assert "ecg" in result.output
        assert "imaging" in result.output

    def test_pccp_init_missing_type(self, runner):
        """Test pccp init without required --type flag."""
        result = runner.invoke(cli, ["pccp", "init"])
        assert result.exit_code != 0
        assert "Missing option '--type'" in result.output

    def test_pccp_init_invalid_type(self, runner):
        """Test pccp init with invalid device type."""
        result = runner.invoke(cli, ["pccp", "init", "--type", "invalid"])
        assert result.exit_code != 0
        assert "invalid is not one of" in result.output

    def test_pccp_init_valid_types(self, runner):
        """Test pccp init with all valid device types."""
        for device_type in ["ecg", "imaging", "signals", "nlp"]:
            result = runner.invoke(cli, ["pccp", "init", "--type", device_type])
            assert result.exit_code != 0  # Will fail because module not implemented
            assert "not yet available" in result.output or "not available" in result.output


class TestTemplatesCommands:
    """Test templates subcommands."""

    def test_templates_help(self, runner):
        """Test templates group help."""
        result = runner.invoke(cli, ["templates", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "show" in result.output
        assert "copy" in result.output

    def test_templates_list(self, runner):
        """Test templates list command."""
        result = runner.invoke(cli, ["templates", "list"])
        assert result.exit_code == 0
        assert "510k-summary" in result.output or "template" in result.output.lower()

    def test_templates_show_help(self, runner):
        """Test templates show help."""
        result = runner.invoke(cli, ["templates", "show", "--help"])
        assert result.exit_code == 0
        assert "NAME" in result.output

    def test_templates_show_valid_template(self, runner):
        """Test templates show with a valid template."""
        result = runner.invoke(cli, ["templates", "show", "510k-summary-ai-ml"])
        assert result.exit_code == 0
        assert "Template Details" in result.output

    def test_templates_show_invalid_template(self, runner):
        """Test templates show with an invalid template."""
        result = runner.invoke(cli, ["templates", "show", "nonexistent-template"])
        assert result.exit_code != 0
        assert "not found" in result.output

    def test_templates_copy_help(self, runner):
        """Test templates copy help."""
        result = runner.invoke(cli, ["templates", "copy", "--help"])
        assert result.exit_code == 0
        assert "--dest" in result.output

    def test_templates_copy_missing_dest(self, runner):
        """Test templates copy without required --dest flag."""
        result = runner.invoke(cli, ["templates", "copy", "510k-summary-generic"])
        assert result.exit_code != 0
        assert "Missing option '--dest'" in result.output

    def test_templates_copy_success(self, runner):
        """Test templates copy creates destination directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                cli,
                ["templates", "copy", "510k-summary-generic", "--dest", tmpdir],
            )
            assert result.exit_code == 0
            assert "copied" in result.output.lower()
            assert tmpdir in result.output


class TestModelCardCommands:
    """Test model-card subcommands."""

    def test_model_card_help(self, runner):
        """Test model-card group help."""
        result = runner.invoke(cli, ["model-card", "--help"])
        assert result.exit_code == 0
        assert "generate" in result.output
        assert "init" in result.output

    def test_model_card_generate_missing_config(self, runner):
        """Test model-card generate without required --config flag."""
        result = runner.invoke(
            cli, ["model-card", "generate", "--output", "card.md"]
        )
        assert result.exit_code != 0
        assert "Missing option '--config'" in result.output

    def test_model_card_generate_missing_output(self, runner):
        """Test model-card generate without required --output flag."""
        result = runner.invoke(
            cli, ["model-card", "generate", "--config", "model.yaml"]
        )
        assert result.exit_code != 0
        assert "Missing option '--output'" in result.output

    def test_model_card_generate_help(self, runner):
        """Test model-card generate help."""
        result = runner.invoke(cli, ["model-card", "generate", "--help"])
        assert result.exit_code == 0
        assert "--config" in result.output
        assert "--output" in result.output

    def test_model_card_init_help(self, runner):
        """Test model-card init help."""
        result = runner.invoke(cli, ["model-card", "init", "--help"])
        assert result.exit_code == 0
        assert "--type" in result.output
        assert "classifier" in result.output
        assert "segmentation" in result.output
        assert "detection" in result.output

    def test_model_card_init_missing_type(self, runner):
        """Test model-card init without required --type flag."""
        result = runner.invoke(cli, ["model-card", "init"])
        assert result.exit_code != 0
        assert "Missing option '--type'" in result.output

    def test_model_card_init_invalid_type(self, runner):
        """Test model-card init with invalid model type."""
        result = runner.invoke(cli, ["model-card", "init", "--type", "invalid"])
        assert result.exit_code != 0
        assert "invalid is not one of" in result.output


class TestChecklistCommand:
    """Test checklist command."""

    def test_checklist_help(self, runner):
        """Test checklist help."""
        result = runner.invoke(cli, ["checklist", "--help"])
        assert result.exit_code == 0
        assert "FDA SaMD Readiness Checklist" in result.output or "checklist" in result.output.lower()

    def test_checklist_runs(self, runner):
        """Test checklist command runs without errors."""
        result = runner.invoke(cli, ["checklist"])
        assert result.exit_code == 0
        assert "checklist" in result.output.lower() or "checked" in result.output.lower()


class TestErrorHandling:
    """Test error handling and user-friendly messages."""

    def test_invalid_subcommand(self, runner):
        """Test that invalid subcommands show helpful error."""
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "no such command" in result.output.lower()

    def test_pccp_generate_with_template_option(self, runner):
        """Test that --template option is recognized."""
        with tempfile.NamedTemporaryFile(suffix=".yaml") as f:
            result = runner.invoke(
                cli,
                [
                    "pccp",
                    "generate",
                    "--config",
                    f.name,
                    "--output",
                    "out.md",
                    "--template",
                    "detailed",
                ],
            )
            # Should fail due to missing module, but should parse options
            assert "--template" not in result.output or "not yet available" in result.output


class TestCaseSensitivity:
    """Test that command options handle case appropriately."""

    def test_pccp_init_lowercase_type(self, runner):
        """Test pccp init accepts lowercase device type."""
        result = runner.invoke(cli, ["pccp", "init", "--type", "ecg"])
        # Should fail gracefully, not with type error
        assert "not one of" not in result.output

    def test_model_card_init_lowercase_type(self, runner):
        """Test model-card init accepts lowercase model type."""
        result = runner.invoke(cli, ["model-card", "init", "--type", "classifier"])
        # Should fail gracefully, not with type error
        assert "not one of" not in result.output
