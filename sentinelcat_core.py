"""
SentinelCAT Core Engine
Deterministic classification only.
No heuristics. No AI. No probabilities.
"""

from sentinelcat_classes import FailureClass


def classify_event(event: dict) -> dict:
    """
    Classify an infrastructure failure event.

    Returns a deterministic failure class and rationale.
    """

    # Placeholder logic until Phase 2
    return {
        "failure_class": FailureClass.UNCLASSIFIED.value,
        "root_cause": "ontology_not_yet_bound",
        "recommended_action": "none",
        "deterministic": True,
    }