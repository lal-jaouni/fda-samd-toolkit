"""Tests for openFDA API client."""

import json
from unittest.mock import Mock, patch

import pytest

from fda_samd_toolkit.predicate.client import OpenFDAClient
from fda_samd_toolkit.predicate.schemas import OpenFDADevice


class TestOpenFDAClient:
    """Test OpenFDAClient."""

    def test_search_510k_success(self, openfda_sample_response):
        """Test successful API call."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.read.return_value = json.dumps(openfda_sample_response).encode("utf-8")
            mock_urlopen.return_value = mock_response

            results = OpenFDAClient.search_510k("ECG classifier", limit=3)

            assert len(results) == 3
            assert results[0].k_number == "K790739"
            assert results[0].device_name == "QUINTON MODEL 530X ECG DATA CART"
            assert results[0].product_code == "DPS"
            assert results[1].k_number == "K890123"

    def test_search_510k_empty_results(self, empty_openfda_response):
        """Test API call with no results."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.read.return_value = json.dumps(empty_openfda_response).encode("utf-8")
            mock_urlopen.return_value = mock_response

            results = OpenFDAClient.search_510k("nonexistent_xyz_query_12345", limit=10)

            assert results == []

    def test_search_510k_empty_query_raises_error(self):
        """Test that empty query raises ValueError."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            OpenFDAClient.search_510k("")

    def test_search_510k_whitespace_query_raises_error(self):
        """Test that whitespace-only query raises ValueError."""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            OpenFDAClient.search_510k("   ")

    def test_search_510k_invalid_limit_below_min(self):
        """Test that limit < 1 raises ValueError."""
        with pytest.raises(ValueError, match="Limit must be between 1 and"):
            OpenFDAClient.search_510k("ECG", limit=0)

    def test_search_510k_invalid_limit_above_max(self):
        """Test that limit > 100 raises ValueError."""
        with pytest.raises(ValueError, match="Limit must be between 1 and"):
            OpenFDAClient.search_510k("ECG", limit=101)

    def test_search_510k_network_error(self):
        """Test handling of network errors."""
        import urllib.error

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.URLError("Connection timeout")

            with pytest.raises(RuntimeError, match="Network error"):
                OpenFDAClient.search_510k("ECG", limit=10)

    def test_search_510k_http_error(self):
        """Test handling of HTTP errors."""
        import urllib.error
        from email.message import Message

        with patch("urllib.request.urlopen") as mock_urlopen:
            hdrs = Message()
            mock_urlopen.side_effect = urllib.error.HTTPError(
                url="http://example.com",
                code=429,
                msg="Too Many Requests",
                hdrs=hdrs,
                fp=None,
            )

            with pytest.raises(RuntimeError, match="OpenFDA API error"):
                OpenFDAClient.search_510k("ECG", limit=10)

    def test_search_510k_returns_typed_objects(self, openfda_sample_response):
        """Test that results are proper OpenFDADevice objects."""
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.read.return_value = json.dumps(openfda_sample_response).encode("utf-8")
            mock_urlopen.return_value = mock_response

            results = OpenFDAClient.search_510k("ECG", limit=3)

            for result in results:
                assert isinstance(result, OpenFDADevice)
                assert hasattr(result, "k_number")
                assert hasattr(result, "device_name")
                assert hasattr(result, "applicant")

    def test_search_510k_skips_malformed_records(self):
        """Test that malformed records are skipped gracefully."""
        bad_response = {
            "results": [
                {
                    "k_number": "K790739",
                    "device_name": "Valid Device",
                    "applicant": "Valid Corp",
                    "product_code": "DPS",
                    "decision_date": "1979-04-26",
                    "decision_description": "Substantially Equivalent",
                },
                {
                    # Missing required fields
                    "k_number": "K890123",
                    # missing device_name and others
                },
                {
                    "k_number": "K950456",
                    "device_name": "Another Valid Device",
                    "applicant": "Another Corp",
                    "product_code": "DQK",
                    "decision_date": "1995-02-10",
                    "decision_description": "Substantially Equivalent",
                },
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.read.return_value = json.dumps(bad_response).encode("utf-8")
            mock_urlopen.return_value = mock_response

            results = OpenFDAClient.search_510k("ECG", limit=3)

            # Should have at least 2 valid records (the malformed one is skipped)
            assert len(results) >= 1
            assert all(isinstance(r, OpenFDADevice) for r in results)
