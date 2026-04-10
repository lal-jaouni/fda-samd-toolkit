"""Tests for checklist schemas, items loading, and report generation."""

import tempfile
from pathlib import Path

import pytest
import yaml

from fda_samd_toolkit.checklist.items import (
    ALL_ITEMS,
    get_all_categories,
    get_item_by_id,
    get_items_by_category,
)
from fda_samd_toolkit.checklist.runner import (
    report_to_markdown,
    run_from_yaml,
)
from fda_samd_toolkit.checklist.schemas import (
    CategoryResult,
    ChecklistItem,
    ItemSeverity,
    ItemStatus,
    ReadinessReport,
)


class TestChecklistSchemas:
    """Test Pydantic schema validation."""

    def test_checklist_item_creation(self):
        """Test creating a ChecklistItem."""
        item = ChecklistItem(
            id="test-001",
            category="Test Category",
            requirement="Test requirement",
            evidence_required="Test evidence",
            standard_reference="Test reference",
            severity=ItemSeverity.MAJOR,
        )
        assert item.id == "test-001"
        assert item.status == ItemStatus.MISSING  # Default

    def test_item_status_enum(self):
        """Test ItemStatus enum values."""
        assert ItemStatus.MISSING.value == "missing"
        assert ItemStatus.PARTIAL.value == "partial"
        assert ItemStatus.COMPLETE.value == "complete"

    def test_item_severity_enum(self):
        """Test ItemSeverity enum values."""
        assert ItemSeverity.BLOCKER.value == "blocker"
        assert ItemSeverity.MAJOR.value == "major"
        assert ItemSeverity.MINOR.value == "minor"

    def test_category_result_completion_pct(self):
        """Test completion percentage calculation."""
        items = [
            ChecklistItem(
                id="1",
                category="Test",
                requirement="Test",
                evidence_required="Test",
                standard_reference="Test",
                severity=ItemSeverity.MAJOR,
                status=ItemStatus.COMPLETE,
            ),
            ChecklistItem(
                id="2",
                category="Test",
                requirement="Test",
                evidence_required="Test",
                standard_reference="Test",
                severity=ItemSeverity.MAJOR,
                status=ItemStatus.MISSING,
            ),
        ]
        cat = CategoryResult(
            category="Test",
            items=items,
            total=2,
            complete=1,
            partial=0,
            missing=1,
        )
        assert cat.completion_pct == 50.0

    def test_category_result_blockers_property(self):
        """Test blockers property filters correctly."""
        items = [
            ChecklistItem(
                id="blocker-1",
                category="Test",
                requirement="Test",
                evidence_required="Test",
                standard_reference="Test",
                severity=ItemSeverity.BLOCKER,
                status=ItemStatus.MISSING,
            ),
            ChecklistItem(
                id="blocker-2",
                category="Test",
                requirement="Test",
                evidence_required="Test",
                standard_reference="Test",
                severity=ItemSeverity.BLOCKER,
                status=ItemStatus.COMPLETE,
            ),
            ChecklistItem(
                id="major-1",
                category="Test",
                requirement="Test",
                evidence_required="Test",
                standard_reference="Test",
                severity=ItemSeverity.MAJOR,
                status=ItemStatus.MISSING,
            ),
        ]
        cat = CategoryResult(
            category="Test",
            items=items,
            total=3,
            complete=1,
            partial=0,
            missing=2,
        )
        blockers = cat.blockers
        assert len(blockers) == 1
        assert blockers[0].id == "blocker-1"

    def test_readiness_report_properties(self):
        """Test ReadinessReport properties."""
        items = [
            ChecklistItem(
                id="1",
                category="Test",
                requirement="Test",
                evidence_required="Test",
                standard_reference="Test",
                severity=ItemSeverity.MAJOR,
                status=ItemStatus.COMPLETE,
            ),
        ]
        cat = CategoryResult(
            category="Test",
            items=items,
            total=1,
            complete=1,
            partial=0,
            missing=0,
        )
        report = ReadinessReport(
            categories=[cat],
            overall_pct=100.0,
            timestamp="2026-04-10T10:00:00",
            device_name="Test Device",
        )
        assert report.total_items == 1
        assert report.total_complete == 1
        assert report.total_blockers_missing == 0


class TestChecklistItems:
    """Test checklist items loading and organization."""

    def test_all_items_loaded(self):
        """Test that all items are loaded."""
        assert len(ALL_ITEMS) >= 50
        assert len(ALL_ITEMS) <= 100  # Sanity check for reasonable count

    def test_get_all_categories(self):
        """Test categories are properly extracted."""
        categories = get_all_categories()
        expected_categories = [
            "Design Controls",
            "Risk Management",
            "Software Lifecycle",
            "AI/ML-Specific",
            "Cybersecurity",
            "Clinical Evidence",
            "Quality Management",
            "Submission Documents",
        ]
        assert len(categories) == len(expected_categories)
        for expected in expected_categories:
            assert expected in categories

    def test_get_items_by_category(self):
        """Test retrieving items by category."""
        items = get_items_by_category("Design Controls")
        assert len(items) == 9
        for item in items:
            assert item.category == "Design Controls"

    def test_get_item_by_id(self):
        """Test retrieving a single item by ID."""
        item = get_item_by_id("dc-001")
        assert item is not None
        assert item.id == "dc-001"
        assert item.category == "Design Controls"

    def test_get_item_by_id_not_found(self):
        """Test retrieving non-existent item returns None."""
        item = get_item_by_id("nonexistent-id")
        assert item is None

    def test_all_items_have_required_fields(self):
        """Test all items have required fields."""
        for item in ALL_ITEMS:
            assert item.id
            assert item.category
            assert item.requirement
            assert item.evidence_required
            assert item.standard_reference
            assert item.severity
            assert item.status is not None

    def test_item_ids_are_unique(self):
        """Test all item IDs are unique."""
        ids = [item.id for item in ALL_ITEMS]
        assert len(ids) == len(set(ids)), "Duplicate item IDs found"

    def test_item_ids_have_prefix(self):
        """Test item IDs follow expected prefixes."""
        prefixes = {"dc", "rm", "sl", "ml", "cs", "ce", "qm", "sub"}
        for item in ALL_ITEMS:
            prefix = item.id.split("-")[0]
            assert prefix in prefixes, f"Unexpected prefix in {item.id}"

    def test_design_controls_count(self):
        """Test Design Controls category has expected count."""
        items = get_items_by_category("Design Controls")
        assert len(items) == 9

    def test_risk_management_count(self):
        """Test Risk Management category has expected count."""
        items = get_items_by_category("Risk Management")
        assert len(items) == 7

    def test_software_lifecycle_count(self):
        """Test Software Lifecycle category has expected count."""
        items = get_items_by_category("Software Lifecycle")
        assert len(items) == 10

    def test_aiml_specific_count(self):
        """Test AI/ML-Specific category has expected count."""
        items = get_items_by_category("AI/ML-Specific")
        assert len(items) == 8

    def test_cybersecurity_count(self):
        """Test Cybersecurity category has expected count."""
        items = get_items_by_category("Cybersecurity")
        assert len(items) == 6

    def test_clinical_evidence_count(self):
        """Test Clinical Evidence category has expected count."""
        items = get_items_by_category("Clinical Evidence")
        assert len(items) == 4

    def test_quality_management_count(self):
        """Test Quality Management category has expected count."""
        items = get_items_by_category("Quality Management")
        assert len(items) == 5

    def test_submission_documents_count(self):
        """Test Submission Documents category has expected count."""
        items = get_items_by_category("Submission Documents")
        assert len(items) == 9

    def test_blocker_items_present(self):
        """Test that blocker severity items exist."""
        blockers = [item for item in ALL_ITEMS if item.severity == ItemSeverity.BLOCKER]
        assert len(blockers) > 0
        assert len(blockers) >= 20  # Should have many blockers

    def test_major_items_present(self):
        """Test that major severity items exist."""
        majors = [item for item in ALL_ITEMS if item.severity == ItemSeverity.MAJOR]
        assert len(majors) > 0

    def test_minor_items_present(self):
        """Test that minor severity items exist."""
        minors = [item for item in ALL_ITEMS if item.severity == ItemSeverity.MINOR]
        assert len(minors) > 0


class TestReportGeneration:
    """Test report generation functions."""

    def test_report_to_markdown_structure(self):
        """Test markdown report has expected sections."""
        items = [
            ChecklistItem(
                id="1",
                category="Test",
                requirement="Test requirement",
                evidence_required="Test evidence",
                standard_reference="Test reference",
                severity=ItemSeverity.BLOCKER,
                status=ItemStatus.COMPLETE,
            ),
        ]
        cat = CategoryResult(
            category="Test",
            items=items,
            total=1,
            complete=1,
            partial=0,
            missing=0,
        )
        report = ReadinessReport(
            categories=[cat],
            overall_pct=100.0,
            timestamp="2026-04-10T10:00:00",
            device_name="Test Device",
        )

        markdown = report_to_markdown(report)

        assert "FDA SaMD Submission Readiness Report" in markdown
        assert "Test Device" in markdown
        assert "100.0%" in markdown
        assert "Category Breakdown" in markdown
        assert "Summary" in markdown

    def test_report_with_blockers(self):
        """Test markdown report includes blocker section when present."""
        items = [
            ChecklistItem(
                id="1",
                category="Test",
                requirement="Blocker requirement",
                evidence_required="Evidence",
                standard_reference="Ref",
                severity=ItemSeverity.BLOCKER,
                status=ItemStatus.MISSING,
            ),
        ]
        cat = CategoryResult(
            category="Test",
            items=items,
            total=1,
            complete=0,
            partial=0,
            missing=1,
        )
        report = ReadinessReport(
            categories=[cat],
            overall_pct=0.0,
            timestamp="2026-04-10T10:00:00",
            device_name="Test Device",
        )

        markdown = report_to_markdown(report)

        assert "BLOCKERS" in markdown
        assert "1 blocker items" in markdown
        assert "Blocker requirement" in markdown

    def test_report_without_blockers(self):
        """Test markdown report excludes blocker section when none present."""
        items = [
            ChecklistItem(
                id="1",
                category="Test",
                requirement="Test requirement",
                evidence_required="Evidence",
                standard_reference="Ref",
                severity=ItemSeverity.MINOR,
                status=ItemStatus.COMPLETE,
            ),
        ]
        cat = CategoryResult(
            category="Test",
            items=items,
            total=1,
            complete=1,
            partial=0,
            missing=0,
        )
        report = ReadinessReport(
            categories=[cat],
            overall_pct=100.0,
            timestamp="2026-04-10T10:00:00",
            device_name="Test Device",
        )

        markdown = report_to_markdown(report)

        # Should not have blockers section if no blockers
        assert "BLOCKERS" not in markdown or "0 blocker" in markdown


class TestRunFromYAML:
    """Test YAML loading and report generation."""

    def test_run_from_yaml_basic(self):
        """Test loading and generating report from YAML."""
        yaml_data = {
            "device_name": "Test Device",
            "items": [
                {"id": "dc-001", "status": "complete"},
                {"id": "dc-002", "status": "partial"},
                {"id": "dc-003", "status": "missing"},
            ],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(yaml_data, f)
            f.flush()

            try:
                report = run_from_yaml(f.name)

                assert report.device_name == "Test Device"
                assert report.total_items >= 3
                # dc-001 should be complete
                dc001 = get_item_by_id("dc-001")
                assert dc001 is not None
            finally:
                Path(f.name).unlink()

    def test_run_from_yaml_missing_file(self):
        """Test error handling for missing YAML file."""
        with pytest.raises(FileNotFoundError):
            run_from_yaml("/nonexistent/path.yaml")

    def test_run_from_yaml_invalid_format(self):
        """Test error handling for invalid YAML format."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: here: too: many: colons")
            f.flush()

            try:
                # Invalid YAML raises yaml.scanner.ScannerError or similar
                with pytest.raises(Exception):  # Catches any YAML parsing error
                    run_from_yaml(f.name)
            finally:
                Path(f.name).unlink()

    def test_run_from_yaml_missing_id_field(self):
        """Test error handling for missing item ID."""
        yaml_data = {
            "device_name": "Test",
            "items": [{"status": "complete"}],  # Missing id
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(yaml_data, f)
            f.flush()

            try:
                with pytest.raises(ValueError, match="id.*status"):
                    run_from_yaml(f.name)
            finally:
                Path(f.name).unlink()

    def test_run_from_yaml_invalid_status(self):
        """Test error handling for invalid status value."""
        yaml_data = {
            "device_name": "Test",
            "items": [{"id": "dc-001", "status": "invalid_status"}],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(yaml_data, f)
            f.flush()

            try:
                with pytest.raises(ValueError, match="Invalid status"):
                    run_from_yaml(f.name)
            finally:
                Path(f.name).unlink()

    def test_run_from_yaml_override_device_name(self):
        """Test device name can be overridden."""
        yaml_data = {
            "device_name": "YAML Device",
            "items": [{"id": "dc-001", "status": "complete"}],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(yaml_data, f)
            f.flush()

            try:
                report = run_from_yaml(f.name, device_name="Override Device")
                assert report.device_name == "Override Device"
            finally:
                Path(f.name).unlink()

    def test_run_from_yaml_partial_items(self):
        """Test that unspecified items default to missing."""
        yaml_data = {
            "device_name": "Test",
            "items": [{"id": "dc-001", "status": "complete"}],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(yaml_data, f)
            f.flush()

            try:
                report = run_from_yaml(f.name)

                # dc-001 should be complete
                dc001_item = None
                for cat in report.categories:
                    for item in cat.items:
                        if item.id == "dc-001":
                            dc001_item = item
                            break

                assert dc001_item is not None
                assert dc001_item.status == ItemStatus.COMPLETE

                # dc-002 should be missing
                dc002_item = None
                for cat in report.categories:
                    for item in cat.items:
                        if item.id == "dc-002":
                            dc002_item = item
                            break

                assert dc002_item is not None
                assert dc002_item.status == ItemStatus.MISSING
            finally:
                Path(f.name).unlink()


class TestExampleYAML:
    """Test with provided example YAML."""

    def test_example_yaml_loads(self):
        """Test that example YAML file loads successfully."""
        example_path = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"

        if example_path.exists():
            report = run_from_yaml(example_path)
            assert report.device_name == "Cardiac Arrhythmia Detection Algorithm (CADA)"
            assert report.total_items >= 50
        else:
            pytest.skip("Example YAML file not found")
