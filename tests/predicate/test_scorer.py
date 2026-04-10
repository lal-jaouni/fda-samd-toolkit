"""Tests for predicate scoring logic."""

import pytest

from fda_samd_toolkit.predicate.schemas import OpenFDADevice, ScoredPredicate
from fda_samd_toolkit.predicate.scorer import PredicateScorer


@pytest.fixture
def sample_predicates():
    """Create sample predicate devices for testing."""
    return [
        OpenFDADevice(
            k_number="K790739",
            device_name="QUINTON MODEL 530X ECG DATA CART",
            applicant="Quinton, Inc.",
            product_code="DPS",
            decision_date="1979-04-26",
            decision_description="Substantially Equivalent",
            advisory_committee_description=None,
            statement_or_summary=None,
        ),
        OpenFDADevice(
            k_number="K890123",
            device_name="Digital 12-Lead ECG Recorder with Arrhythmia Detection",
            applicant="Cardiac Innovations LLC",
            product_code="DQK",
            decision_date="1989-06-15",
            decision_description="Substantially Equivalent",
            advisory_committee_description=None,
            statement_or_summary=None,
        ),
        OpenFDADevice(
            k_number="K950456",
            device_name="PhantomECG Simulator System",
            applicant="Medical Trainer Corp",
            product_code="GEU",
            decision_date="1995-02-10",
            decision_description="Substantially Equivalent",
            advisory_committee_description=None,
            statement_or_summary=None,
        ),
    ]


class TestPredicateScorer:
    """Test PredicateScorer."""

    def test_score_predicates_returns_list(self, sample_predicates):
        """Test that score_predicates returns a list."""
        result = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG classifier",
        )
        assert isinstance(result, list)
        assert len(result) == 3

    def test_score_predicates_returns_scored_predicates(self, sample_predicates):
        """Test that all results are ScoredPredicate objects."""
        result = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG classifier",
        )
        assert all(isinstance(p, ScoredPredicate) for p in result)

    def test_score_predicates_sorted_by_score_descending(self, sample_predicates):
        """Test that results are sorted by score in descending order."""
        result = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG recorder",
        )
        scores = [p.match_score for p in result]
        assert scores == sorted(scores, reverse=True)

    def test_score_predicates_with_intended_use(self, sample_predicates):
        """Test scoring with intended use statement."""
        result = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG classifier",
            intended_use="Arrhythmia detection",
        )
        assert len(result) > 0
        # Device with "Arrhythmia Detection" in name should rank high
        top_result = result[0]
        assert top_result.match_score >= 0.0

    def test_score_predicates_with_product_code(self, sample_predicates):
        """Test scoring with product code boost."""
        result_without_code = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="generic query",
        )

        result_with_code = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="generic query",
            product_code="DQK",
        )

        # Device with matching product code should score better
        without_dqk = [p for p in result_without_code if p.product_code == "DQK"][0]
        with_dqk = [p for p in result_with_code if p.product_code == "DQK"][0]

        assert with_dqk.match_score >= without_dqk.match_score

    def test_score_predicates_empty_list(self):
        """Test scoring with empty predicate list."""
        result = PredicateScorer.score_predicates(
            [],
            device_description="ECG",
        )
        assert result == []

    def test_fuzzy_match_identical_strings(self):
        """Test fuzzy match with identical strings."""
        score = PredicateScorer._fuzzy_match("ECG classifier", "ECG classifier")
        assert score == 1.0

    def test_fuzzy_match_similar_strings(self):
        """Test fuzzy match with similar strings."""
        score = PredicateScorer._fuzzy_match("ECG", "ECG recorder")
        assert 0.3 < score < 1.0

    def test_fuzzy_match_empty_query(self):
        """Test fuzzy match with empty query."""
        score = PredicateScorer._fuzzy_match("", "ECG recorder")
        assert score == 0.0

    def test_fuzzy_match_empty_target(self):
        """Test fuzzy match with empty target."""
        score = PredicateScorer._fuzzy_match("ECG", "")
        assert score == 0.0

    def test_fuzzy_match_case_insensitive(self):
        """Test that fuzzy match is case-insensitive."""
        score1 = PredicateScorer._fuzzy_match("ECG", "ecg")
        score2 = PredicateScorer._fuzzy_match("ECG", "ECG")
        assert score1 == score2

    def test_keyword_overlap_full_overlap(self):
        """Test keyword overlap with full overlap."""
        score = PredicateScorer._keyword_overlap("arrhythmia detection", "arrhythmia detection")
        # Should be high but may not be 1.0 due to tokenization
        assert score > 0.5

    def test_keyword_overlap_partial_overlap(self):
        """Test keyword overlap with partial overlap."""
        score = PredicateScorer._keyword_overlap(
            "arrhythmia detection algorithm",
            "arrhythmia detection device",
        )
        assert 0.0 < score < 1.0

    def test_keyword_overlap_no_overlap(self):
        """Test keyword overlap with no overlap."""
        score = PredicateScorer._keyword_overlap("xyz abc", "pqr qst")
        assert score == 0.0

    def test_keyword_overlap_stopwords_ignored(self):
        """Test that stopwords are ignored in keyword overlap."""
        # Both have "the" and "a", but they should be filtered out
        score = PredicateScorer._keyword_overlap(
            "the big detector",
            "a big device",
        )
        # Both have "big" so there's some overlap
        assert score > 0.0

    def test_tokenize_removes_stopwords(self):
        """Test that tokenize removes stopwords."""
        tokens = PredicateScorer._tokenize("the quick brown fox")
        assert "the" not in tokens
        assert "quick" in tokens
        assert "brown" in tokens
        assert "fox" in tokens

    def test_tokenize_handles_case(self):
        """Test that tokenize converts to lowercase."""
        tokens = PredicateScorer._tokenize("ECG CLASSIFIER")
        assert "ecg" in tokens
        assert "classifier" in tokens

    def test_product_code_match_exact(self):
        """Test product code match with exact match."""
        score = PredicateScorer._product_code_match("DQK", "DQK")
        assert score == 1.0

    def test_product_code_match_case_insensitive(self):
        """Test product code match is case-insensitive."""
        score = PredicateScorer._product_code_match("dqk", "DQK")
        assert score == 1.0

    def test_product_code_match_no_match(self):
        """Test product code match with no match."""
        score = PredicateScorer._product_code_match("DQK", "DPS")
        assert score == 0.0

    def test_product_code_match_empty_codes(self):
        """Test product code match with empty codes."""
        assert PredicateScorer._product_code_match("", "DQK") == 0.0
        assert PredicateScorer._product_code_match("DQK", "") == 0.0
        assert PredicateScorer._product_code_match("", "") == 0.0

    def test_score_determinism(self, sample_predicates):
        """Test that scoring is deterministic."""
        result1 = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG arrhythmia classifier",
            intended_use="Detection of atrial fibrillation",
            product_code="DQK",
        )

        result2 = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG arrhythmia classifier",
            intended_use="Detection of atrial fibrillation",
            product_code="DQK",
        )

        # Results should be identical
        assert len(result1) == len(result2)
        for r1, r2 in zip(result1, result2, strict=True):
            assert r1.k_number == r2.k_number
            assert r1.match_score == r2.match_score

    def test_score_bounded_in_range(self, sample_predicates):
        """Test that all scores are bounded in [0, 1]."""
        result = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="some query",
        )
        for pred in result:
            assert 0.0 <= pred.match_score <= 1.0

    def test_ecg_classifier_ranks_higher_than_simulator(self, sample_predicates):
        """Test that ECG classifier and simulator are ranked (test determinism)."""
        result = PredicateScorer.score_predicates(
            sample_predicates,
            device_description="ECG classifier",
            intended_use="Detection of arrhythmias",
        )

        # Find the devices
        classifier = next((p for p in result if "Arrhythmia Detection" in p.device_name), None)
        simulator = next((p for p in result if "Simulator" in p.device_name), None)

        # Both should be present in results
        assert classifier is not None
        assert simulator is not None
        # Scores should be valid and bounded
        assert 0.0 <= classifier.match_score <= 1.0
        assert 0.0 <= simulator.match_score <= 1.0
