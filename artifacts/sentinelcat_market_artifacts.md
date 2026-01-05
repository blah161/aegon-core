# SentinelCAT — Market Artifacts
## Phase 6 (LOCKED)

This document contains the outward-facing market artifacts derived from
SentinelCAT’s internal architecture.

This is a source bundle.
Individual sections are later extracted into:
- Landing pages
- Sales emails
- Competitive pages
- Admin documentation

This document is internal and authoritative.

---

## 1. Landing Page — Hero Section

Headline:
Prevent catastrophic outages before they compound

Subheadline:
SentinelCAT is a deterministic failure-classification and containment engine
for cloud and infrastructure systems.

It identifies the failure mode you are entering and asserts what must stop
before damage escalates.

Value propositions:
- Deterministic failure classification (no AI, no heuristics)
- Stops amplification, retry storms, and global misconfiguration
- Human-controlled containment, not self-healing automation
- Deploys in 1–2 days, runs entirely inside your environment

Primary CTA:
Request Enterprise Evaluation

Secondary CTA:
See Failure Classes Covered

---

## 2. Landing Page — Diagram Logic (Source Copy)

Diagram A: Observability vs SentinelCAT

Observability flow:
Metrics → Dashboards → Alerts → Humans guess

SentinelCAT flow:
Signals → Failure Class → Containment Assertion → Humans act

Caption:
Observability tells you what is broken.
SentinelCAT tells you what must stop.

---

Diagram B: Failure Amplification Curve

Axes:
X-axis: Time
Y-axis: Economic damage

Observability curve:
Damage increases while humans investigate.

SentinelCAT curve:
Damage plateaus when containment is asserted.

Caption:
Outages do not kill companies.
Uncontained amplification does.

---

## 3. Competitive Differentiation — Not Observability

Header:
Why SentinelCAT is not observability

Key points:
- Observability systems measure symptoms.
- SentinelCAT classifies failure modes.
- Observability increases data volume.
- SentinelCAT reduces risk surface.
- Observability scales with telemetry.
- SentinelCAT scales with architecture.

One-line positioning:
If observability is a microscope, SentinelCAT is a circuit breaker.

---

## 4. Enterprise Email — Tier 1 (Structural Containment)

Subject:
Prevent outages from spiraling out of control

Body:
Most major outages do not begin as catastrophes.
They become catastrophic through retry storms,
global configuration fan-out, and recovery automation.

SentinelCAT is a deterministic containment engine that classifies
infrastructure failure modes in real time and asserts what must stop
before damage escalates.

Tier 1 — Structural Containment focuses on preventing:
- Retry storms
- Global configuration accidents
- Recovery automation worsening outages

No agents.
No AI.
No observability replacement.

Deployment typically takes 1–2 days and runs entirely inside your environment.

If stopping outage amplification is a priority this quarter,
we would welcome a short conversation.

Signature:
Adrian Diamond  
SentinelCAT

---

## 5. Enterprise Email — Tier 2 (Platform Integrity)

Subject:
Prevent platform-wide infrastructure outages

Body:
Platform-wide outages are rarely caused by a single bug.

They emerge from control-plane loss, shared dependency collapse,
time skew, or hidden transitive dependencies—and they escalate quickly.

SentinelCAT is a deterministic classification and containment system
designed to prevent these failure modes from propagating.

Tier 2 — Control & Dependency Integrity protects against:
- Control-plane paralysis
- Auth and DNS-driven global outages
- Time-based latent failures
- Undocumented critical dependencies

SentinelCAT does not ingest telemetry,
require training, or attempt self-healing.

It classifies the failure you are entering and asserts
the correct containment posture before irreversible damage occurs.

Signature:
Adrian Diamond  
SentinelCAT

---

## 6. Admin / Installation Guide — Outline

This section defines the structure of the SentinelCAT admin guide.

Outline:
1. What SentinelCAT is and is not
2. Deployment model (single internal service)
3. Signal ingestion model (JSON event contract)
4. Licensed failure classes by tier
5. Classification output format
6. Containment assertions (non-automated)
7. Human operational responsibilities
8. Versioning and upgrade policy
9. Security and isolation model

This guide is procedural and intentionally brief.

---

## Lock Statement

This document defines the SentinelCAT market artifacts for Phase 6.

Changes require:
- Pricing alignment
- Ontology compatibility
- Signal contract stability

Unauthorized marketing drift is prohibited.