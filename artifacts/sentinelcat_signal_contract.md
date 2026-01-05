# SentinelCAT — Canonical Signal Contract
## Version 1.0 (LOCKED)

This document defines the canonical signal interface for SentinelCAT.

It specifies:
- What signals SentinelCAT accepts
- How those signals are interpreted
- Which failure classes each signal group enables
- What SentinelCAT explicitly does NOT require

This document is internal product law.
It is not user-facing documentation.

Once locked, changes require an explicit version bump.

---

## Core Principles (Non-Negotiable)

1. Signals are customer-owned  
   SentinelCAT does not collect metrics. It consumes them.

2. Signals are pre-aggregated  
   SentinelCAT never computes percentiles, rates, or windows.

3. All signals are optional  
   Missing signals disable rules, not the system.

4. Boolean > Numeric > Derived  
   Determinism prefers explicit boolean assertions over inferred values.

5. No telemetry dependency  
   SentinelCAT must continue to classify even when monitoring systems degrade.

---

## Canonical Signal Groups

Signal groups map directly to SentinelCAT failure classes.
This mapping is intentional and contractual.

---

## 1. Control Plane Signals (CP Classes)

Used by:
- CONTROL_PLANE_LOSS
- HIDDEN_TRANSITIVE_DEPENDENCY

| Signal | Type | Required |
|------|------|---------|
| cp_api_p95_ms | float | optional |
| cp_api_error_rate | float (0–1) | optional |
| dp_request_success_rate | float (0–1) | optional |
| dp_p95_ms | float | optional |

Contract rule:
SentinelCAT does not infer control-plane health from data-plane metrics.

---

## 2. Authority / Split-Brain Signals

Used by:
- AUTHORITY_INCONSISTENCY

| Signal | Type | Required |
|------|------|---------|
| authority_inconsistency_detected | bool | optional |

Contract rule:
Authority inconsistency is customer-asserted.
SentinelCAT never heuristically infers split-brain conditions.

---

## 3. Dependency Health Signals

Used by:
- SHARED_DEPENDENCY_COLLAPSE

| Signal | Type | Required |
|------|------|---------|
| auth_error_rate | float (0–1) | optional |
| dns_error_rate | float (0–1) | optional |

Contract rule:
If customers do not track dependency health explicitly, SentinelCAT does not guess.

---

## 4. Configuration & Deployment Signals

Used by:
- CONFIGURATION_FANOUT
- IRREVERSIBLE_CONFIGURATION_STATE

| Signal | Type | Required |
|------|------|---------|
| config_push_rate_per_min | float | optional |
| rollout_scope_percent | float (0–100) | optional |
| state_mutation_detected | bool | optional |
| rollback_possible | bool | optional |

Critical invariant:
Rollback capability is declarative, not assumed.

---

## 5. Cascading / Resource Exhaustion Signals

Used by:
- CASCADING_RESOURCE_EXHAUSTION

| Signal | Type | Required |
|------|------|---------|
| retry_rate_per_req | float | optional |
| cpu_utilization | float (0–1) | optional |
| queue_depth | float | optional |
| connection_pool_exhausted | bool | optional |

---

## 6. Time / Expiry Signals

Used by:
- TIME_SKEW_AMPLIFICATION

| Signal | Type | Required |
|------|------|---------|
| max_clock_skew_ms | float | optional |
| cert_expiry_hours | float | optional |
| lease_expiry_errors_rate | float (0–1) | optional |

---

## 7. Recovery Automation Signals

Used by:
- RECOVERY_SYSTEM_FAILURE

| Signal | Type | Required |
|------|------|---------|
| autoremediation_actions_per_min | float | optional |
| failover_flaps_per_hour | float | optional |
| recovery_actions_increase_errors | bool | optional |

---

## 8. Safety / Lockout Signals

Used by:
- SAFETY_MECHANISM_LOCKOUT

| Signal | Type | Required |
|------|------|---------|
| safety_interlock_active | bool | optional |
| admin_actions_blocked | bool | optional |
| admin_rate_limited | bool | optional |

---

## 9. Operator Visibility Signals (Amplifiers)

Used as amplifiers:
- OPERATOR_BLINDNESS

| Signal | Type | Required |
|------|------|---------|
| telemetry_drop_rate | float (0–1) | optional |
| dashboards_unavailable | bool | optional |
| alert_storm_active | bool | optional |

Amplifier rule:
These signals do not define primary failure classes.

---

## 10. Privilege / Access Signals (Amplifiers)

Used as amplifiers:
- PRIVILEGE_ACCESS_DEADLOCK

| Signal | Type | Required |
|------|------|---------|
| iam_unavailable | bool | optional |
| bastion_unreachable | bool | optional |
| oob_access_available | bool | optional |

---

## Explicit Non-Requirements (Product Differentiation)

SentinelCAT does NOT require:
- Logs
- Traces
- Spans
- Agents
- Machine learning
- Training periods
- Historical baselines
- Dashboards
- Alerts
- Continuous telemetry availability

SentinelCAT is a deterministic classification engine,
not an observability platform.

---

## Lock Statement

This document defines the SentinelCAT signal interface version 1.0.

Changes require:
- Explicit version bump
- Ontology compatibility review
- Pricing tier reevaluation

Unauthorized signal expansion is prohibited.