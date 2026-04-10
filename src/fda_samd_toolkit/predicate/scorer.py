"""Scoring and ranking logic for predicate device discovery."""

import difflib
import re
from collections.abc import Sequence

from fda_samd_toolkit.predicate.schemas import OpenFDADevice, ScoredPredicate


class PredicateScorer:
    """Scores predicate devices for relevance to user query."""

    # Common stopwords for keyword filtering
    STOPWORDS = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "as",
        "is",
        "was",
        "are",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "must",
        "use",
        "used",
        "using",
    }

    @classmethod
    def score_predicates(
        cls,
        predicates: Sequence[OpenFDADevice],
        device_description: str,
        intended_use: str = "",
        product_code: str = "",
    ) -> list[ScoredPredicate]:
        """
        Score and rank predicates based on relevance to device description and intended use.

        Args:
            predicates: List of candidate predicate devices from openFDA
            device_description: Description of the user's device
            intended_use: Intended use statement (optional)
            product_code: FDA product code to boost match on (optional)

        Returns:
            List of ScoredPredicate objects, sorted by match_score descending.
        """
        if not predicates:
            return []

        scored = []
        for predicate in predicates:
            score = cls._compute_score(
                predicate,
                device_description,
                intended_use,
                product_code,
            )
            scored.append(score)

        # Sort by match_score descending
        return sorted(scored, key=lambda x: x.match_score, reverse=True)

    @classmethod
    def _compute_score(
        cls,
        predicate: OpenFDADevice,
        device_description: str,
        intended_use: str = "",
        product_code: str = "",
    ) -> ScoredPredicate:
        """Compute a single predicate's relevance score."""
        scores = {}
        reasons = []

        # 1. Device name fuzzy match (weight: 0.5)
        desc_match = cls._fuzzy_match(device_description, predicate.device_name)
        scores["description"] = desc_match
        if desc_match > 0.6:
            reasons.append(f"Device name similarity: {desc_match:.1%}")

        # 2. Intended use keyword overlap (weight: 0.3)
        use_match = cls._keyword_overlap(intended_use, predicate.device_name)
        if intended_use:  # Only compute if user provided intended use
            scores["use"] = use_match
            if use_match > 0.3:
                reasons.append(f"Intended use alignment: {use_match:.1%}")
        else:
            scores["use"] = 0.0

        # 3. Product code match (weight: 0.2)
        code_match = cls._product_code_match(product_code, predicate.product_code)
        scores["code"] = code_match
        if code_match > 0.0:
            reasons.append("Product code match")

        # Weighted combination
        total_score = 0.5 * scores["description"] + 0.3 * scores["use"] + 0.2 * scores["code"]

        # Add general reasoning if no specific matches
        if not reasons:
            reasons.append("Moderate relevance based on device category")

        reasoning = ", ".join(reasons) if reasons else "No specific match criteria met"

        return ScoredPredicate(
            k_number=predicate.k_number,
            device_name=predicate.device_name,
            applicant=predicate.applicant,
            product_code=predicate.product_code,
            decision_date=predicate.decision_date,
            match_score=min(max(total_score, 0.0), 1.0),  # Clamp to [0, 1]
            match_reasoning=reasoning,
        )

    @staticmethod
    def _fuzzy_match(query: str, target: str) -> float:
        """
        Compute fuzzy string similarity using SequenceMatcher.

        Returns score in [0, 1].
        """
        if not query or not target:
            return 0.0
        query_lower = query.lower().strip()
        target_lower = target.lower().strip()
        return difflib.SequenceMatcher(None, query_lower, target_lower).ratio()

    @classmethod
    def _keyword_overlap(cls, query: str, target: str) -> float:
        """
        Compute keyword overlap as Jaccard similarity.

        Tokenizes both strings, removes stopwords, and computes intersection/union.
        Returns score in [0, 1].
        """
        if not query or not target:
            return 0.0

        query_tokens = cls._tokenize(query)
        target_tokens = cls._tokenize(target)

        if not query_tokens or not target_tokens:
            return 0.0

        query_set = set(query_tokens)
        target_set = set(target_tokens)

        intersection = len(query_set & target_set)
        union = len(query_set | target_set)

        if union == 0:
            return 0.0

        return intersection / union

    @classmethod
    def _tokenize(cls, text: str) -> list[str]:
        """
        Tokenize text: lowercase, split on non-alphanumeric, remove stopwords.
        """
        # Split on non-alphanumeric and lowercase
        tokens = re.findall(r"\b\w+\b", text.lower())
        # Filter out stopwords and very short tokens
        return [t for t in tokens if t not in cls.STOPWORDS and len(t) > 1]

    @staticmethod
    def _product_code_match(query_code: str, target_code: str) -> float:
        """
        Return 1.0 if product codes match exactly, 0.0 otherwise.
        """
        if not query_code or not target_code:
            return 0.0
        return 1.0 if query_code.upper() == target_code.upper() else 0.0
