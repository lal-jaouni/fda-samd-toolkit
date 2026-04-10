"""Fixtures for predicate discovery tests."""

import pytest


@pytest.fixture
def openfda_sample_response():
    """Sample openFDA API response for testing."""
    return {
        "meta": {
            "disclaimer": "Do not rely on openFDA to make decisions regarding medical care.",
            "terms": "https://open.fda.gov/terms/",
            "license": "https://open.fda.gov/license/",
            "last_updated": "2026-03-30",
            "results": {"skip": 0, "limit": 3, "total": 622},
        },
        "results": [
            {
                "k_number": "K790739",
                "device_name": "QUINTON MODEL 530X ECG DATA CART",
                "applicant": "Quinton, Inc.",
                "product_code": "DPS",
                "decision_date": "1979-04-26",
                "decision_description": "Substantially Equivalent",
                "advisory_committee_description": "Cardiovascular",
                "statement_or_summary": "",
            },
            {
                "k_number": "K890123",
                "device_name": "Digital 12-Lead ECG Recorder with Arrhythmia Detection",
                "applicant": "Cardiac Innovations LLC",
                "product_code": "DQK",
                "decision_date": "1989-06-15",
                "decision_description": "Substantially Equivalent",
                "advisory_committee_description": "Cardiovascular",
                "statement_or_summary": "AI-assisted rhythm detection algorithm.",
            },
            {
                "k_number": "K950456",
                "device_name": "PhantomECG Simulator System",
                "applicant": "Medical Trainer Corp",
                "product_code": "GEU",
                "decision_date": "1995-02-10",
                "decision_description": "Substantially Equivalent",
                "advisory_committee_description": "Cardiovascular",
                "statement_or_summary": "Training device with ECG simulation.",
            },
        ],
    }


@pytest.fixture
def empty_openfda_response():
    """Empty openFDA API response."""
    return {
        "meta": {
            "disclaimer": "Do not rely on openFDA.",
            "last_updated": "2026-03-30",
            "results": {"skip": 0, "limit": 10, "total": 0},
        },
        "results": [],
    }
