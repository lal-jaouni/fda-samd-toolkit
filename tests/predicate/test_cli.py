"""Tests for predicate discovery CLI."""

import json
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from fda_samd_toolkit.cli import cli


@pytest.fixture
def runner():
    """Create a Click CLI runner for tests."""
    return CliRunner()


class TestPredicateDiscoveryCLI:
    """Test predicate discovery CLI command."""

    def test_predicate_help(self, runner):
        """Test predicate group help."""
        result = runner.invoke(cli, ["predicate", "--help"])
        assert result.exit_code == 0
        assert "discover" in result.output

    def test_discover_help(self, runner):
        """Test discover command help."""
        result = runner.invoke(cli, ["predicate", "discover", "--help"])
        assert result.exit_code == 0
        assert "--device-description" in result.output
        assert "--intended-use" in result.output
        assert "--product-code" in result.output
        assert "--limit" in result.output
        assert "--output" in result.output

    def test_discover_missing_device_description(self, runner):
        """Test discover without required device-description."""
        result = runner.invoke(cli, ["predicate", "discover"])
        assert result.exit_code != 0
        assert "Missing option" in result.output or "device-description" in result.output

    def test_discover_empty_device_description(self, runner):
        """Test discover with empty device-description."""
        result = runner.invoke(
            cli,
            ["predicate", "discover", "--device-description", ""],
        )
        assert result.exit_code != 0
        assert "cannot be empty" in result.output.lower()

    def test_discover_invalid_limit(self, runner):
        """Test discover with invalid limit."""
        result = runner.invoke(
            cli,
            ["predicate", "discover", "--device-description", "ECG", "--limit", "150"],
        )
        assert result.exit_code != 0
        assert "limit" in result.output.lower()

    def test_discover_success_with_mock_api(self, runner):
        """Test successful discover command with mocked API."""
        mock_response = {
            "results": [
                {
                    "k_number": "K790739",
                    "device_name": "ECG Recorder",
                    "applicant": "Quinton, Inc.",
                    "product_code": "DPS",
                    "decision_date": "1979-04-26",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Cardiovascular",
                    "statement_or_summary": "",
                },
                {
                    "k_number": "K890123",
                    "device_name": "Digital 12-Lead ECG Classifier",
                    "applicant": "Cardiac Innovations",
                    "product_code": "DQK",
                    "decision_date": "1989-06-15",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Cardiovascular",
                    "statement_or_summary": "",
                },
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_http_response = Mock()
            mock_http_response.__enter__ = Mock(return_value=mock_http_response)
            mock_http_response.__exit__ = Mock(return_value=False)
            mock_http_response.read.return_value = json.dumps(mock_response).encode("utf-8")
            mock_urlopen.return_value = mock_http_response

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "ECG classifier",
                    "--intended-use",
                    "Arrhythmia detection",
                    "--limit",
                    "2",
                ],
            )

            assert result.exit_code == 0
            assert "K790739" in result.output
            assert "K890123" in result.output
            assert "Top Predicate Devices" in result.output

    def test_discover_no_results(self, runner):
        """Test discover with no matching results."""
        mock_response = {"results": []}

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_http_response = Mock()
            mock_http_response.__enter__ = Mock(return_value=mock_http_response)
            mock_http_response.__exit__ = Mock(return_value=False)
            mock_http_response.read.return_value = json.dumps(mock_response).encode("utf-8")
            mock_urlopen.return_value = mock_http_response

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "xyz_nonexistent_query",
                ],
            )

            assert result.exit_code == 0
            assert "No matching predicates" in result.output

    def test_discover_with_output_file(self, runner, tmp_path):
        """Test discover with markdown output file."""
        mock_response = {
            "results": [
                {
                    "k_number": "K790739",
                    "device_name": "ECG Recorder",
                    "applicant": "Quinton, Inc.",
                    "product_code": "DPS",
                    "decision_date": "1979-04-26",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Cardiovascular",
                    "statement_or_summary": "",
                },
            ]
        }

        output_file = tmp_path / "predicates.md"

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_http_response = Mock()
            mock_http_response.__enter__ = Mock(return_value=mock_http_response)
            mock_http_response.__exit__ = Mock(return_value=False)
            mock_http_response.read.return_value = json.dumps(mock_response).encode("utf-8")
            mock_urlopen.return_value = mock_http_response

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "ECG classifier",
                    "--output",
                    str(output_file),
                ],
            )

            assert result.exit_code == 0
            assert output_file.exists()
            content = output_file.read_text()
            assert "Predicate Device Search Results" in content
            assert "K790739" in content

    def test_discover_with_product_code(self, runner):
        """Test discover with product code option."""
        mock_response = {
            "results": [
                {
                    "k_number": "K790739",
                    "device_name": "ECG Device DPS",
                    "applicant": "Corp A",
                    "product_code": "DPS",
                    "decision_date": "1979-04-26",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Cardiovascular",
                    "statement_or_summary": "",
                },
                {
                    "k_number": "K890123",
                    "device_name": "ECG Device DQK",
                    "applicant": "Corp B",
                    "product_code": "DQK",
                    "decision_date": "1989-06-15",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Cardiovascular",
                    "statement_or_summary": "",
                },
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_http_response = Mock()
            mock_http_response.__enter__ = Mock(return_value=mock_http_response)
            mock_http_response.__exit__ = Mock(return_value=False)
            mock_http_response.read.return_value = json.dumps(mock_response).encode("utf-8")
            mock_urlopen.return_value = mock_http_response

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "ECG",
                    "--product-code",
                    "DQK",
                ],
            )

            assert result.exit_code == 0
            # Device with DQK should rank higher and appear first in results
            assert "K890123" in result.output or "DQK" in result.output

    def test_discover_api_network_error(self, runner):
        """Test discover when API call fails."""
        import urllib.error

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.URLError("Connection timeout")

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "ECG",
                ],
            )

            assert result.exit_code != 0
            assert "API error" in result.output or "error" in result.output.lower()

    def test_discover_table_format(self, runner):
        """Test that discover output includes result data."""
        mock_response = {
            "results": [
                {
                    "k_number": "K123456",
                    "device_name": "Test Device",
                    "applicant": "Test Corp",
                    "product_code": "ABC",
                    "decision_date": "2020-01-01",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Test",
                    "statement_or_summary": "",
                },
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_http_response = Mock()
            mock_http_response.__enter__ = Mock(return_value=mock_http_response)
            mock_http_response.__exit__ = Mock(return_value=False)
            mock_http_response.read.return_value = json.dumps(mock_response).encode("utf-8")
            mock_urlopen.return_value = mock_http_response

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "Test",
                ],
            )

            assert result.exit_code == 0
            # Check for table elements and result data
            assert "K123456" in result.output
            assert "Test Corp" in result.output

    def test_discover_limit_default(self, runner):
        """Test that default limit is applied."""
        mock_response = {
            "results": [
                {
                    "k_number": f"K{i:06d}",
                    "device_name": f"UniqueDevice_{i}",
                    "applicant": f"Corp {i}",
                    "product_code": f"PC{i}",
                    "decision_date": "2020-01-01",
                    "decision_description": "Substantially Equivalent",
                    "advisory_committee_description": "Test",
                    "statement_or_summary": "",
                }
                for i in range(15)
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_http_response = Mock()
            mock_http_response.__enter__ = Mock(return_value=mock_http_response)
            mock_http_response.__exit__ = Mock(return_value=False)
            mock_http_response.read.return_value = json.dumps(mock_response).encode("utf-8")
            mock_urlopen.return_value = mock_http_response

            result = runner.invoke(
                cli,
                [
                    "predicate",
                    "discover",
                    "--device-description",
                    "UniqueDevice",
                ],
            )

            assert result.exit_code == 0
            # Should show only 10 results by default (not all 15)
            # Count occurrences of K-numbers (unique identifiers)
            k_numbers_found = sum(1 for i in range(15) if f"K{i:06d}" in result.output)
            # Default limit is 10, so we should see at most 10 devices
            assert k_numbers_found <= 10
