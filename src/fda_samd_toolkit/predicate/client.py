"""OpenFDA API client for 510(k) device discovery."""

import json
import urllib.error
import urllib.parse
import urllib.request

from fda_samd_toolkit.predicate.schemas import OpenFDADevice


class OpenFDAClient:
    """Client for querying the openFDA 510(k) devices API."""

    BASE_URL = "https://api.fda.gov/device/510k.json"
    TIMEOUT = 10
    MAX_RESULTS = 100  # openFDA allows max 100 per request

    @classmethod
    def search_510k(cls, query: str, limit: int = 10) -> list[OpenFDADevice]:
        """
        Search for 510(k) devices via openFDA API.

        Args:
            query: Search query string (e.g., "ECG classifier" or "K790739")
            limit: Maximum number of results to return (default 10, max 100)

        Returns:
            List of OpenFDADevice objects matching the query.

        Raises:
            ValueError: If query is empty or limit is invalid.
            RuntimeError: If API request fails.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not isinstance(limit, int) or limit < 1 or limit > cls.MAX_RESULTS:
            raise ValueError(f"Limit must be between 1 and {cls.MAX_RESULTS}")

        # Build search query for openFDA
        # Try to search across device_name and applicant fields
        search_terms = [
            f"device_name:{query}",
            f"applicant:{query}",
        ]
        search_query = " OR ".join(search_terms)

        params = {"search": search_query, "limit": limit}
        url = f"{cls.BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            with urllib.request.urlopen(url, timeout=cls.TIMEOUT) as response:
                data = json.loads(response.read().decode("utf-8"))

                if not data.get("results"):
                    return []

                devices = []
                for record in data["results"]:
                    try:
                        device = OpenFDADevice(
                            k_number=record.get("k_number", ""),
                            device_name=record.get("device_name", ""),
                            applicant=record.get("applicant", ""),
                            product_code=record.get("product_code", ""),
                            decision_date=record.get("decision_date", ""),
                            decision_description=record.get("decision_description", ""),
                            advisory_committee_description=record.get("advisory_committee_description"),
                            statement_or_summary=record.get("statement_or_summary"),
                        )
                        devices.append(device)
                    except Exception:
                        # Skip malformed records; log but continue
                        pass

                return devices

        except urllib.error.HTTPError as e:
            raise RuntimeError(f"OpenFDA API error {e.code}: {e.reason}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error querying openFDA: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response from openFDA: {e}") from e
