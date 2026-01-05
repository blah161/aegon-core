"""
SentinelCAT — Deterministic Detection Rules

Invariant-based rules that classify infrastructure systems into SentinelCAT
failure classes BEFORE catastrophic outage.

No heuristics.
No probabilities.
No learning.

Model:
- Inputs are simple numeric/boolean signals (customer can map from Prometheus, CloudWatch, logs, etc.)
- Rules evaluate invariants / cross-signal contradictions
- Output: one primary FailureClass + optional amplifiers
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple

from sentinelcat_classes import FailureClass


# -----------------------------
# Signal model (minimal)
# -----------------------------

@dataclass(frozen=True)
class Signals:
    """
    Canonical signal snapshot.
    All values are optional; missing values simply disable dependent rules.

    Time window guidance: customer should feed values computed over a consistent window,
    e.g. last 1-5 minutes for rates/latency, last 15-60 minutes for drift/expiry.
    """
    # Control plane vs data plane health
    cp_api_p95_ms: Optional[float] = None
    cp_api_error_rate: Optional[float] = None          # 0.0 - 1.0
    dp_request_success_rate: Optional[float] = None    # 0.0 - 1.0
    dp_p95_ms: Optional[float] = None

    authority_inconsistency_detected: Optional[bool] = None

    # Provisioning / orchestration
    provisioning_error_rate: Optional[float] = None    # 0.0 - 1.0
    scaling_action_fail_rate: Optional[float] = None   # 0.0 - 1.0

    # Dependency health (auth/DNS/etc)
    auth_error_rate: Optional[float] = None            # 0.0 - 1.0
    dns_error_rate: Optional[float] = None             # 0.0 - 1.0

    # Rollout / configuration
    config_push_rate_per_min: Optional[float] = None
    rollout_scope_percent: Optional[float] = None      # 0 - 100
    rollback_possible: Optional[bool] = None           # declared capability
    state_mutation_detected: Optional[bool] = None     # e.g., schema migration / irreversible write

    # Cascading / load amplification
    retry_rate_per_req: Optional[float] = None         # retries per primary request
    queue_depth: Optional[float] = None
    connection_pool_exhausted: Optional[bool] = None
    cpu_utilization: Optional[float] = None            # 0 - 1

    # Time / clock / cert
    max_clock_skew_ms: Optional[float] = None
    cert_expiry_hours: Optional[float] = None          # hours until expiry
    lease_expiry_errors_rate: Optional[float] = None

    # Recovery automation
    autoremediation_actions_per_min: Optional[float] = None
    failover_flaps_per_hour: Optional[float] = None
    recovery_actions_increase_errors: Optional[bool] = None

    # Safety / lockout
    admin_actions_blocked: Optional[bool] = None
    admin_rate_limited: Optional[bool] = None
    safety_interlock_active: Optional[bool] = None

    # Operator visibility
    telemetry_drop_rate: Optional[float] = None        # 0.0 - 1.0
    dashboards_unavailable: Optional[bool] = None
    alert_storm_active: Optional[bool] = None

    # Privilege / access path
    iam_unavailable: Optional[bool] = None
    bastion_unreachable: Optional[bool] = None
    oob_access_available: Optional[bool] = None        # out-of-band access exists


def signals_from_event(event: Dict[str, Any]) -> Signals:
    """
    Accepts event payload shaped like:
      {
        "signals": { "cp_api_p95_ms": 1200, "dp_request_success_rate": 0.995, ... }
      }
    Extra keys ignored. Missing keys are None.
    """
    raw = (event or {}).get("signals", {}) or {}
    # Only map known fields; ignore everything else
    return Signals(
        cp_api_p95_ms=raw.get("cp_api_p95_ms"),
        cp_api_error_rate=raw.get("cp_api_error_rate"),
        dp_request_success_rate=raw.get("dp_request_success_rate"),
        dp_p95_ms=raw.get("dp_p95_ms"),

        authority_inconsistency_detected=raw.get("authority_inconsistency_detected"),

        provisioning_error_rate=raw.get("provisioning_error_rate"),
        scaling_action_fail_rate=raw.get("scaling_action_fail_rate"),
        auth_error_rate=raw.get("auth_error_rate"),
        dns_error_rate=raw.get("dns_error_rate"),
        config_push_rate_per_min=raw.get("config_push_rate_per_min"),
        rollout_scope_percent=raw.get("rollout_scope_percent"),
        rollback_possible=raw.get("rollback_possible"),
        state_mutation_detected=raw.get("state_mutation_detected"),
        retry_rate_per_req=raw.get("retry_rate_per_req"),
        queue_depth=raw.get("queue_depth"),
        connection_pool_exhausted=raw.get("connection_pool_exhausted"),
        cpu_utilization=raw.get("cpu_utilization"),
        max_clock_skew_ms=raw.get("max_clock_skew_ms"),
        cert_expiry_hours=raw.get("cert_expiry_hours"),
        lease_expiry_errors_rate=raw.get("lease_expiry_errors_rate"),
        autoremediation_actions_per_min=raw.get("autoremediation_actions_per_min"),
        failover_flaps_per_hour=raw.get("failover_flaps_per_hour"),
        recovery_actions_increase_errors=raw.get("recovery_actions_increase_errors"),
        admin_actions_blocked=raw.get("admin_actions_blocked"),
        admin_rate_limited=raw.get("admin_rate_limited"),
        safety_interlock_active=raw.get("safety_interlock_active"),
        telemetry_drop_rate=raw.get("telemetry_drop_rate"),
        dashboards_unavailable=raw.get("dashboards_unavailable"),
        alert_storm_active=raw.get("alert_storm_active"),
        iam_unavailable=raw.get("iam_unavailable"),
        bastion_unreachable=raw.get("bastion_unreachable"),
        oob_access_available=raw.get("oob_access_available"),
    )


# -----------------------------
# Deterministic thresholds (configurable later)
# -----------------------------

DEFAULT_THRESHOLDS = {
    # Control-plane vs data-plane divergence
    "cp_api_p95_ms_high": 1000.0,
    "cp_api_error_rate_high": 0.05,
    "dp_success_good": 0.98,

    # Provisioning failure
    "provisioning_error_high": 0.10,
    "scaling_fail_high": 0.10,

    # Shared deps
    "auth_error_high": 0.10,
    "dns_error_high": 0.05,

    # Config fanout
    "config_push_rate_high": 30.0,     # per minute
    "rollout_scope_global": 80.0,      # percent

    # Cascading exhaustion
    "retry_rate_high": 0.50,           # retries per primary request
    "cpu_high": 0.90,
    "telemetry_drop_high": 0.30,

    # Time
    "clock_skew_high_ms": 250.0,
    "cert_expiry_soon_hours": 24.0,
    "lease_errors_high": 0.05,

    # Recovery loops
    "autoremediation_high": 10.0,      # per minute
    "failover_flaps_high": 3.0,        # per hour
}


# -----------------------------
# Rule evaluation
# -----------------------------

@dataclass
class RuleResult:
    primary: FailureClass
    amplifiers: List[FailureClass]
    matched_rules: List[str]
    rationale: List[str]


def _present(x) -> bool:
    return x is not None


def evaluate_rules(sig: Signals, thresholds: Dict[str, float] = DEFAULT_THRESHOLDS) -> RuleResult:
    """
    Returns a primary class. Amplifiers are optional secondary tags.
    Deterministic selection: first-match in priority order below.
    """

    matched: List[str] = []
    rationale: List[str] = []
    amplifiers: List[FailureClass] = []

    # ---- Amplifier detectors (do not decide primary by themselves) ----
    # Operator blindness amplifier
    if (_present(sig.telemetry_drop_rate) and sig.telemetry_drop_rate >= thresholds["telemetry_drop_high"]) or sig.dashboards_unavailable:
        amplifiers.append(FailureClass.OPERATOR_BLINDNESS)
        matched.append("AMP_OP_BLINDNESS")
        rationale.append("Telemetry visibility degraded (telemetry_drop_rate high and/or dashboards unavailable).")

    # Privilege/access deadlock amplifier
    if (sig.iam_unavailable is True) or (sig.bastion_unreachable is True) or (sig.oob_access_available is False):
        amplifiers.append(FailureClass.PRIVILEGE_ACCESS_DEADLOCK)
        matched.append("AMP_PRIV_DEADLOCK")
        rationale.append("Operator access paths impaired (IAM/bastion/OOB access issue).")

    # ---- Primary classification priority order ----
    # 1) Safety mechanism lockout (blocks recovery)
    if sig.safety_interlock_active or sig.admin_actions_blocked or sig.admin_rate_limited:
        matched.append("P_SAFETY_LOCKOUT")
        rationale.append("Safety mechanisms or admin controls are blocking intervention.")
        return RuleResult(FailureClass.SAFETY_MECHANISM_LOCKOUT, amplifiers, matched, rationale)

    # 2) Recovery system failure (automation worsening situation)
    if (
        (_present(sig.autoremediation_actions_per_min) and sig.autoremediation_actions_per_min >= thresholds["autoremediation_high"])
        or (_present(sig.failover_flaps_per_hour) and sig.failover_flaps_per_hour >= thresholds["failover_flaps_high"])
        or (sig.recovery_actions_increase_errors is True)
    ):
        matched.append("P_RECOVERY_FAILURE")
        rationale.append("Recovery mechanisms are looping/flapping or increasing error rates.")
        return RuleResult(FailureClass.RECOVERY_SYSTEM_FAILURE, amplifiers, matched, rationale)

    # 3) Time skew amplification
    if (
        (_present(sig.max_clock_skew_ms) and sig.max_clock_skew_ms >= thresholds["clock_skew_high_ms"])
        or (_present(sig.cert_expiry_hours) and sig.cert_expiry_hours <= thresholds["cert_expiry_soon_hours"])
        or (_present(sig.lease_expiry_errors_rate) and sig.lease_expiry_errors_rate >= thresholds["lease_errors_high"])
    ):
        matched.append("P_TIME_SKEW")
        rationale.append("Time-based invariants violated (clock skew, cert expiry soon, or lease expiry errors).")
        return RuleResult(FailureClass.TIME_SKEW_AMPLIFICATION, amplifiers, matched, rationale)

    # 4) Configuration fan-out
    if (
        (_present(sig.config_push_rate_per_min) and sig.config_push_rate_per_min >= thresholds["config_push_rate_high"])
        and (_present(sig.rollout_scope_percent) and sig.rollout_scope_percent >= thresholds["rollout_scope_global"])
    ):
        matched.append("P_CFG_FANOUT")
        rationale.append("High-velocity configuration propagation with global scope (fan-out).")
        return RuleResult(FailureClass.CONFIGURATION_FANOUT, amplifiers, matched, rationale)

    # 5) Irreversible configuration state
    if (sig.state_mutation_detected is True) and (sig.rollback_possible is False):
        matched.append("P_CFG_IRREVERSIBLE")
        rationale.append("State mutation detected and rollback declared impossible.")
        return RuleResult(FailureClass.IRREVERSIBLE_CONFIGURATION_STATE, amplifiers, matched, rationale)

    # 6) Shared dependency collapse (auth/DNS class of deps)
    if (
        (_present(sig.auth_error_rate) and sig.auth_error_rate >= thresholds["auth_error_high"])
        or (_present(sig.dns_error_rate) and sig.dns_error_rate >= thresholds["dns_error_high"])
    ):
        matched.append("P_SHARED_DEP")
        rationale.append("Shared dependency errors elevated (auth and/or DNS).")
        return RuleResult(FailureClass.SHARED_DEPENDENCY_COLLAPSE, amplifiers, matched, rationale)

    # 7) Control plane loss (cp degraded while dp still ok)
    if (
        (
            (_present(sig.cp_api_p95_ms) and sig.cp_api_p95_ms >= thresholds["cp_api_p95_ms_high"])
            or (_present(sig.cp_api_error_rate) and sig.cp_api_error_rate >= thresholds["cp_api_error_rate_high"])
        )
        and (_present(sig.dp_request_success_rate) and sig.dp_request_success_rate >= thresholds["dp_success_good"])
    ):
        matched.append("P_CP_LOSS")
        rationale.append("Control-plane degraded (latency/errors) while data-plane success remains good.")
        return RuleResult(FailureClass.CONTROL_PLANE_LOSS, amplifiers, matched, rationale)

    # 8) Cascading resource exhaustion (retry storm + resource saturation)
    if (
        (_present(sig.retry_rate_per_req) and sig.retry_rate_per_req >= thresholds["retry_rate_high"])
        and (
            (sig.connection_pool_exhausted is True)
            or (_present(sig.cpu_utilization) and sig.cpu_utilization >= thresholds["cpu_high"])
            or (_present(sig.queue_depth) and sig.queue_depth > 0)
        )
    ):
        matched.append("P_CASCADE_EXHAUST")
        rationale.append("Retries elevated with resource saturation indicators (CPU/conn pool/queues).")
        return RuleResult(FailureClass.CASCADING_RESOURCE_EXHAUSTION, amplifiers, matched, rationale)

    # 9) Hidden transitive dependency (dp failures correlated with “should-be-noncritical” deps)
    # Deterministic proxy: dp degrades while cp appears OK and either auth/dns are not elevated.
    if (
        (_present(sig.dp_request_success_rate) and sig.dp_request_success_rate < thresholds["dp_success_good"])
        and (
            (_present(sig.cp_api_error_rate) and sig.cp_api_error_rate < thresholds["cp_api_error_rate_high"])
            or not _present(sig.cp_api_error_rate)
        )
        and (
            (not _present(sig.auth_error_rate) or sig.auth_error_rate < thresholds["auth_error_high"])
            and (not _present(sig.dns_error_rate) or sig.dns_error_rate < thresholds["dns_error_high"])
        )
    ):
        matched.append("P_HIDDEN_TRANSITIVE")
        rationale.append("Data-plane degraded without obvious control-plane or shared-dependency failure.")
        return RuleResult(FailureClass.HIDDEN_TRANSITIVE_DEPENDENCY, amplifiers, matched, rationale)

    # 10) Authority inconsistency (split brain)
    # Deterministic proxy: inconsistent control outcomes across zones/regions.
    # Customer provides a boolean in signals when detected via their own invariants.
    # (We keep core canonical, customer supplies signal.)
    if (event_flag := getattr(sig, "authority_inconsistency_detected", None)) is True:
        matched.append("P_AUTH_INCONSISTENCY")
        rationale.append("Customer-provided authority inconsistency signal asserted true.")
        return RuleResult(FailureClass.AUTHORITY_INCONSISTENCY, amplifiers, matched, rationale)

    # Fallback
    matched.append("P_UNCLASSIFIED")
    rationale.append("Insufficient signals to deterministically classify into a known failure class.")
    return RuleResult(FailureClass.UNCLASSIFIED, amplifiers, matched, rationale)


def classify(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public API: event dict -> classification dict.
    """
    sig = signals_from_event(event)
    result = evaluate_rules(sig)

    return {
        "primary_failure_class": result.primary.value,
        "amplifiers": [a.value for a in result.amplifiers],
        "matched_rules": result.matched_rules,
        "rationale": result.rationale,
        "deterministic": True,
    }