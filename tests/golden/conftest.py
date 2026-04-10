"""Shared fixtures for golden file tests."""

from pathlib import Path

import pytest
import yaml


@pytest.fixture
def golden_data_dir():
    """Return the path to the golden data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def pccp_example_yaml():
    """Load the PCCP ECG classifier example."""
    example_path = Path(__file__).parent.parent.parent / "examples" / "pccp_ecg_classifier.yaml"
    with open(example_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def model_card_example_yaml():
    """Load the model card ECG classifier example."""
    example_path = Path(__file__).parent.parent.parent / "examples" / "model_card_ecg_classifier.yaml"
    with open(example_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def validation_example_yaml():
    """Load the validation plan ECG classifier example."""
    example_path = Path(__file__).parent.parent.parent / "examples" / "validation_plan_ecg_classifier.yaml"
    with open(example_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def checklist_example_yaml():
    """Load the checklist example."""
    example_path = Path(__file__).parent.parent.parent / "examples" / "checklist_artifacts.yaml"
    with open(example_path) as f:
        return yaml.safe_load(f)
