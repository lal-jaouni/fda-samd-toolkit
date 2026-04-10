"""Pydantic v2 schemas for predicate device discovery."""

from pydantic import BaseModel, ConfigDict, Field


class OpenFDADevice(BaseModel):
    """A 510(k) device record from the openFDA API."""

    model_config = ConfigDict(str_strip_whitespace=True)

    k_number: str = Field(..., description="FDA 510(k) number (e.g., K790739)")
    device_name: str = Field(..., description="Device name or marketing name")
    applicant: str = Field(..., description="Applicant/manufacturer name")
    product_code: str = Field(..., description="FDA product code (e.g., DPS)")
    decision_date: str = Field(..., description="Decision date (YYYY-MM-DD format)")
    decision_description: str = Field(..., description="Decision (e.g., 'Substantially Equivalent')")
    advisory_committee_description: str | None = Field(
        None, description="Advisory committee classification (e.g., 'Cardiovascular')"
    )
    statement_or_summary: str | None = Field(None, description="Statement or summary from the 510(k)")


class ScoredPredicate(BaseModel):
    """A predicate device scored for relevance to a query."""

    model_config = ConfigDict(str_strip_whitespace=True)

    k_number: str = Field(..., description="FDA 510(k) number")
    device_name: str = Field(..., description="Device name")
    applicant: str = Field(..., description="Manufacturer name")
    product_code: str = Field(..., description="FDA product code")
    decision_date: str = Field(..., description="Decision date")
    match_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Match confidence score from 0.0 (no match) to 1.0 (perfect match)",
    )
    match_reasoning: str = Field(..., description="Explanation of why this device ranks highly")
