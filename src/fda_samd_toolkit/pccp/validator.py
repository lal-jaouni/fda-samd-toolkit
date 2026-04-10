"""Validator for PCCP markdown documents."""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationIssue:
    """A single validation issue found in a PCCP document."""

    level: str  # "error", "warning", "info"
    section: str  # Section title or name
    message: str  # Human-readable issue description
    line: int | None = None  # Line number if known


class PCCPValidator:
    """Validates PCCP markdown documents for completeness and correctness."""

    REQUIRED_SECTIONS = [
        "Predetermined Change Control Plan",
        "Section 1: Description of Modifications",
        "Section 2: Modification Protocol",
        "Section 3: Impact Assessment",
    ]

    REQUIRED_SUBSECTIONS = {
        "Section 1": [
            "Device Identification",
            "Overview of Planned Modifications",
            "Detailed Modification Descriptions",
        ],
        "Section 2": [
            "Data Management",
            "Data Quality Assurance",
            "Retraining Methodology",
            "Model Validation Strategy",
            "Validation Acceptance Criteria",
            "Performance Thresholds and Monitoring",
            "Data Drift Monitoring",
            "Deployment Process",
        ],
        "Section 3": [
            "Benefits of Planned Modifications",
            "Potential Risks and Mitigations",
            "Sub-Population Analysis",
            "Post-Market Surveillance and Reporting",
        ],
    }

    PLACEHOLDER_PATTERNS = [
        r"\[Signature/Name[^\]]*\]",
        r"\[Date\]",
        r"\[TODO\]",
        r"\[TBD\]",
        r"XXXXX",
        r"TODO:",
        r"FIXME:",
    ]

    def __init__(self) -> None:
        """Initialize the validator."""
        self.issues: list[ValidationIssue] = []
        self.content: str = ""
        self.lines: list[str] = []

    def validate(self, path: str) -> list[ValidationIssue]:
        """
        Validate a PCCP markdown file.

        Args:
            path: Path to PCCP markdown file

        Returns:
            List of validation issues found (empty list = valid)

        Raises:
            FileNotFoundError: If file does not exist
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"PCCP file not found: {path}")

        with open(file_path, encoding="utf-8") as f:
            self.content = f.read()

        self.lines = self.content.split("\n")
        self.issues = []

        self._check_required_sections()
        self._check_required_subsections()
        self._check_placeholder_text()
        self._check_table_content()
        self._check_references()

        return self.issues

    def _check_required_sections(self) -> None:
        """Check that all required top-level sections are present."""
        for section in self.REQUIRED_SECTIONS:
            if section not in self.content:
                self.issues.append(
                    ValidationIssue(
                        level="error",
                        section=section,
                        message=f"Required section '{section}' not found in document",
                    )
                )

    def _check_required_subsections(self) -> None:
        """Check that required subsections are present under each main section."""
        for section, subsections in self.REQUIRED_SUBSECTIONS.items():
            for subsection in subsections:
                if subsection not in self.content:
                    self.issues.append(
                        ValidationIssue(
                            level="warning",
                            section=section,
                            message=f"Expected subsection '{subsection}' under {section} not found",
                        )
                    )

    def _check_placeholder_text(self) -> None:
        """Check for common placeholder patterns that should be filled in."""
        for i, line in enumerate(self.lines, start=1):
            for pattern in self.PLACEHOLDER_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(
                        ValidationIssue(
                            level="error",
                            section="General",
                            message=f"Placeholder text found: {line.strip()}",
                            line=i,
                        )
                    )

    def _check_table_content(self) -> None:
        """Check that tables have actual content, not just headers."""
        table_started = False
        table_has_data = False
        table_start_line = 0

        for i, line in enumerate(self.lines, start=1):
            if "|" in line and "---" not in line:
                if not table_started:
                    table_started = True
                    table_has_data = False
                    table_start_line = i
                else:
                    table_data = line.replace("|", "").strip()
                    if table_data and not all(c == "-" for c in table_data.replace(" ", "")):
                        table_has_data = True

            elif table_started and "|" not in line:
                if not table_has_data:
                    self.issues.append(
                        ValidationIssue(
                            level="warning",
                            section="General",
                            message="Table found with no data rows (only headers)",
                            line=table_start_line,
                        )
                    )
                table_started = False
                table_has_data = False

    def _check_references(self) -> None:
        """Check that FDA guidance references are present."""
        if "[^1]" not in self.content or "Predetermined Change Control Plans" not in self.content:
            self.issues.append(
                ValidationIssue(
                    level="warning",
                    section="References",
                    message="FDA PCCP guidance reference may be missing or incomplete",
                )
            )


def validate_pccp(path: str) -> list[ValidationIssue]:
    """
    Validate a PCCP markdown document.

    Args:
        path: Path to PCCP markdown file

    Returns:
        List of validation issues (empty list indicates valid document)

    Raises:
        FileNotFoundError: If file does not exist

    Example:
        >>> issues = validate_pccp('PCCP.md')
        >>> if issues:
        ...     for issue in issues:
        ...         print(f"{issue.level}: {issue.message}")
    """
    validator = PCCPValidator()
    return validator.validate(path)
