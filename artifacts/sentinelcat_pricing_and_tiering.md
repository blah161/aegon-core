# SentinelCAT — Pricing & Tiering by Failure-Class Coverage
## Version 1.0 (LOCKED)

This document defines SentinelCAT pricing as a function of
failure-class coverage.

Pricing is tied to catastrophic risk surface reduction,
not telemetry usage.

This document is internal and authoritative.

---

## Core Pricing Principles

1. Coverage-based pricing, not usage-based
2. Failure classes represent insured risk categories
3. Deterministic scope enables deterministic pricing
4. No per-host, per-metric, or per-event fees
5. Enterprise procurement simplicity

SentinelCAT is sold like infrastructure insurance,
not observability tooling.

---

## Tier Structure Overview

SentinelCAT is offered in three primary tiers,
plus an optional enterprise add-on.

Each tier answers one economic question.

---

## Tier 1 — Structural Containment

Purpose:
Prevent self-inflicted amplification and runaway outages.

Failure Classes Covered:
- CASCADING_RESOURCE_EXHAUSTION
- CONFIGURATION_FANOUT
- RECOVERY_SYSTEM_FAILURE

What this tier prevents:
- Retry storms
- Global configuration accidents
- Recovery automation worsening outages

Who this is for:
- SaaS companies
- Mid-size platforms
- Teams with observability but no containment discipline

Economic framing:
“Stops outages from getting worse.”

Price Anchor:
$25,000 per year

---

## Tier 2 — Control & Dependency Integrity

Purpose:
Protect the control fabric and shared infrastructure.

Includes Tier 1, plus:

Additional Failure Classes Covered:
- CONTROL_PLANE_LOSS
- SHARED_DEPENDENCY_COLLAPSE
- HIDDEN_TRANSITIVE_DEPENDENCY
- TIME_SKEW_AMPLIFICATION

What this tier prevents:
- Control-plane paralysis
- Auth/DNS-driven platform outages
- Time-based latent failures

Who this is for:
- Cloud-native platforms
- Regulated environments
- Infrastructure-heavy organizations

Economic framing:
“Prevents platform-wide outages.”

Price Anchor:
$75,000 per year

---

## Tier 3 — Catastrophic Risk Containment

Purpose:
Protect against existential failures and irreversible damage.

Includes Tier 2, plus:

Additional Failure Classes Covered:
- AUTHORITY_INCONSISTENCY
- IRREVERSIBLE_CONFIGURATION_STATE
- SAFETY_MECHANISM_LOCKOUT

Amplifiers Included:
- OPERATOR_BLINDNESS
- PRIVILEGE_ACCESS_DEADLOCK

What this tier prevents:
- Data corruption
- Split-brain disasters
- Lockouts blocking recovery

Who this is for:
- Hyperscale platforms
- Financial infrastructure
- National-scale systems

Economic framing:
“Prevents irreversible failure.”

Price Anchor:
$150,000 per year

---

## Enterprise Add-On — Deterministic Enforcement Mode

Availability:
Tier 3 customers only.

Adds:
- Hard enforcement flags (read-only mode, deployment freeze hooks)
- Policy export for internal control systems
- Compliance evidence artifacts

Does NOT add:
- Automation
- Managed services
- Ongoing operational support

Price Anchor:
Additional $50,000 per year

---

## What SentinelCAT Never Charges For

SentinelCAT does NOT charge based on:
- Number of services
- Number of hosts
- Metric volume
- Signal volume
- Regions
- Environments
- Incidents
- Users

Pricing is independent of telemetry scale.

---

## Competitive Pricing Positioning

| Product | Pricing Model | Incentive |
|------|---------------|----------|
| Datadog | Per-host / per-GB | More data |
| New Relic | Usage-based | More ingest |
| CloudWatch | Event volume | More noise |
| SentinelCAT | Failure coverage | Less failure |

---

## Procurement Simplicity

Each tier answers one procurement question:

- Tier 1: “Can this outage spiral?”
- Tier 2: “Can this platform go dark?”
- Tier 3: “Can this company be permanently damaged?”

No calculators.
No ingest negotiations.
No telemetry audits.

---

## Lock Statement

This document defines SentinelCAT pricing and tiering version 1.0.

Changes require:
- Explicit version bump
- Ontology compatibility review
- Signal contract alignment
- Mitigation playbook alignment

Unauthorized repricing or tier drift is prohibited.