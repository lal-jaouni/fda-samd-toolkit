"""Pydantic v2 schemas for FDA submission readiness checklist."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ItemStatus(StrEnum):
    """Status of a checklist item."""

    MISSING = "missing"
    PARTIAL = "partial"
    COMPLETE = "complete"


class ItemSeverity(StrEnum):
    """Severity level of missing items."""

    BLOCKER = "blocker"
    MAJOR = "major"
    MINOR = "minor"


class ChecklistItem(BaseModel):
    """A single requirement in the FDA submission readiness checklist."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(..., description="Unique identifier (e.g., 'dc-001')")
    category: str = Field(..., description="Category (Design Controls, Risk Management, etc.)")
    requirement: str = Field(..., description="Specific regulatory requirement (clear, actionable)")
    evidence_required: str = Field(..., description="What artifacts/evidence must be provided")
    standard_reference: str = Field(
        ..., description="Reference to standard or regulation (e.g., '21 CFR 820.30(b)')"
    )
    status: ItemStatus = Field(default=ItemStatus.MISSING, description="Current completion status")
    severity: ItemSeverity = Field(..., description="Severity if missing (blocker/major/minor)")
    notes: str | None = Field(None, description="Optional notes about this requirement")


class CategoryResult(BaseModel):
    """Summary results for a single checklist category."""

    model_config = ConfigDict(str_strip_whitespace=True)

    category: str = Field(..., description="Category name")
    items: list[ChecklistItem] = Field(..., description="All items in this category")
    total: int = Field(..., description="Total number of items")
    complete: int = Field(..., description="Number of complete items")
    partial: int = Field(..., description="Number of partial items")
    missing: int = Field(..., description="Number of missing items")

    @property
    def completion_pct(self) -> float:
        """Calculate completion percentage."""
        if self.total == 0:
            return 100.0
        return round((self.complete / self.total) * 100, 1)

    @property
    def blockers(self) -> list[ChecklistItem]:
        """Return all blocker items that are not complete."""
        return [
            item
            for item in self.items
            if item.severity == ItemSeverity.BLOCKER and item.status != ItemStatus.COMPLETE
        ]


class ReadinessReport(BaseModel):
    """Complete FDA submission readiness assessment report."""

    model_config = ConfigDict(str_strip_whitespace=True)

    categories: list[CategoryResult] = Field(..., description="Results for each category")
    overall_pct: float = Field(..., description="Overall completion percentage")
    timestamp: str = Field(..., description="Report generation timestamp (ISO 8601)")
    device_name: str | None = Field(None, description="Name of device being assessed")

    @property
    def blockers(self) -> list[tuple[str, ChecklistItem]]:
        """Return all blocker items across categories that are not complete."""
        blockers = []
        for cat in self.categories:
            for item in cat.blockers:
                blockers.append((cat.category, item))
        return blockers

    @property
    def total_items(self) -> int:
        """Total count of all items."""
        return sum(cat.total for cat in self.categories)

    @property
    def total_complete(self) -> int:
        """Total count of complete items."""
        return sum(cat.complete for cat in self.categories)

    @property
    def total_blockers_missing(self) -> int:
        """Count of blocker items that are not complete."""
        return len(self.blockers)
