"""
SentinelCAT Failure Ontology
===========================

This file defines the canonical failure classes used by SentinelCAT.
Once locked, class names and semantics MUST NOT CHANGE.
"""

from enum import Enum


class FailureClass(Enum):
    UNCLASSIFIED = "unclassified"

    # Control Plane & Authority
    CONTROL_PLANE_LOSS = "control_plane_loss"
    AUTHORITY_INCONSISTENCY = "authority_inconsistency"

    # Dependency Failures
    SHARED_DEPENDENCY_COLLAPSE = "shared_dependency_collapse"
    HIDDEN_TRANSITIVE_DEPENDENCY = "hidden_transitive_dependency"

    # Configuration Failures
    CONFIGURATION_FANOUT = "configuration_fanout"
    IRREVERSIBLE_CONFIGURATION_STATE = "irreversible_configuration_state"

    # Cascading Failures
    CASCADING_RESOURCE_EXHAUSTION = "cascading_resource_exhaustion"
    TIME_SKEW_AMPLIFICATION = "time_skew_amplification"

    # Recovery Failures
    RECOVERY_SYSTEM_FAILURE = "recovery_system_failure"
    SAFETY_MECHANISM_LOCKOUT = "safety_mechanism_lockout"

    # Human / Interface Failures
    OPERATOR_BLINDNESS = "operator_blindness"
    PRIVILEGE_ACCESS_DEADLOCK = "privilege_access_deadlock"