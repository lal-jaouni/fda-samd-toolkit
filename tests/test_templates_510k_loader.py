"""Tests for the 510(k) template loader module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from fda_samd_toolkit.templates_510k.loader import (
    TEMPLATE_DESCRIPTIONS,
    TEMPLATE_FILES,
    copy_all_templates,
    copy_template,
    get_template_content,
    get_template_description,
    list_templates,
)


class TestListTemplates:
    """Tests for list_templates()."""

    def test_returns_list(self):
        result = list_templates()
        assert isinstance(result, list)

    def test_returns_expected_count(self):
        result = list_templates()
        assert len(result) == 7

    def test_returns_copy_not_reference(self):
        """Mutating the returned list should not affect the module state."""
        result = list_templates()
        result.append("fake.md")
        assert "fake.md" not in list_templates()

    def test_contains_all_documented_templates(self):
        result = list_templates()
        expected = [
            "01_indications_for_use.md",
            "02_device_description.md",
            "03_substantial_equivalence.md",
            "04_performance_testing.md",
            "05_training_data_characterization.md",
            "06_risk_analysis.md",
            "07_human_factors.md",
        ]
        assert result == expected


class TestGetTemplateDescription:
    """Tests for get_template_description()."""

    def test_returns_string_for_valid_template(self):
        result = get_template_description("01_indications_for_use.md")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_description_mentions_topic(self):
        result = get_template_description("04_performance_testing.md")
        assert "performance" in result.lower() or "testing" in result.lower()

    def test_raises_value_error_for_unknown_template(self):
        with pytest.raises(ValueError) as excinfo:
            get_template_description("nonexistent.md")
        assert "Unknown template" in str(excinfo.value)

    def test_error_lists_valid_templates(self):
        with pytest.raises(ValueError) as excinfo:
            get_template_description("99_fake.md")
        msg = str(excinfo.value)
        assert "01_indications_for_use.md" in msg

    def test_all_templates_have_descriptions(self):
        """Every entry in TEMPLATE_FILES must have a corresponding description."""
        for template_name in TEMPLATE_FILES:
            assert template_name in TEMPLATE_DESCRIPTIONS
            desc = get_template_description(template_name)
            assert len(desc) > 20, f"Description for {template_name} is too short"


class TestGetTemplateContent:
    """Tests for get_template_content()."""

    def test_returns_string_for_valid_template(self):
        result = get_template_content("01_indications_for_use.md")
        assert isinstance(result, str)
        assert len(result) > 100

    def test_content_is_markdown(self):
        result = get_template_content("02_device_description.md")
        # Template files are markdown, so they should have at least one heading
        assert "#" in result

    def test_raises_value_error_for_unknown_template(self):
        with pytest.raises(ValueError) as excinfo:
            get_template_content("not_a_real_template.md")
        assert "Unknown template" in str(excinfo.value)

    def test_raises_file_not_found_if_template_missing_from_disk(self):
        """If a template is in TEMPLATE_FILES but the file is missing, raise FileNotFoundError."""
        with (
            patch(
                "fda_samd_toolkit.templates_510k.loader.TEMPLATES_DIR",
                Path("/nonexistent/templates"),
            ),
            pytest.raises(FileNotFoundError),
        ):
            get_template_content("01_indications_for_use.md")


class TestCopyTemplate:
    """Tests for copy_template()."""

    def test_copies_to_destination(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir)
            result = copy_template("01_indications_for_use.md", dest)
            assert result.exists()
            assert result.name == "01_indications_for_use.md"
            assert result.parent == dest

    def test_copied_content_matches_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir)
            result = copy_template("03_substantial_equivalence.md", dest)
            copied = result.read_text(encoding="utf-8")
            original = get_template_content("03_substantial_equivalence.md")
            assert copied == original

    def test_creates_destination_directory_if_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "new" / "nested" / "dir"
            assert not dest.exists()
            result = copy_template("06_risk_analysis.md", dest)
            assert dest.exists()
            assert result.exists()

    def test_raises_value_error_for_unknown_template(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError) as excinfo:
                copy_template("fake.md", Path(tmpdir))
            assert "Unknown template" in str(excinfo.value)

    def test_raises_file_not_found_if_template_missing(self):
        with (
            tempfile.TemporaryDirectory() as tmpdir,
            patch(
                "fda_samd_toolkit.templates_510k.loader.TEMPLATES_DIR",
                Path("/nonexistent/templates"),
            ),
            pytest.raises(FileNotFoundError),
        ):
            copy_template("01_indications_for_use.md", Path(tmpdir))

    def test_accepts_string_destination(self):
        """copy_template should accept Path or string destinations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = copy_template("07_human_factors.md", tmpdir)
            assert result.exists()


class TestCopyAllTemplates:
    """Tests for copy_all_templates()."""

    def test_copies_all_seven_templates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            results = copy_all_templates(Path(tmpdir))
            assert len(results) == 7

    def test_all_copied_files_exist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            results = copy_all_templates(Path(tmpdir))
            for path in results:
                assert path.exists()
                assert path.stat().st_size > 0

    def test_creates_destination_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "510k_templates"
            assert not dest.exists()
            copy_all_templates(dest)
            assert dest.exists()

    def test_accepts_string_destination(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            results = copy_all_templates(tmpdir)
            assert len(results) == 7
            for path in results:
                assert path.exists()

    def test_continues_on_partial_failure(self, capsys):
        """If one template fails to copy, the rest should still copy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Patch copy_template to fail on one specific file
            original_copy = copy_template

            def flaky_copy(name, dest):
                if name == "04_performance_testing.md":
                    raise OSError("simulated copy failure")
                return original_copy(name, dest)

            with patch("fda_samd_toolkit.templates_510k.loader.copy_template", side_effect=flaky_copy):
                results = copy_all_templates(Path(tmpdir))

            # 6 of 7 should have copied successfully
            assert len(results) == 6
            captured = capsys.readouterr()
            assert "Warning" in captured.out or "Failed" in captured.out
