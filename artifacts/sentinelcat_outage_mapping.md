# SentinelCAT — Failure Class → Real Outage Mapping

This document binds each SentinelCAT failure class
to real-world catastrophic infrastructure outages.

Purpose:
- Validate the ontology
- Ground SentinelCAT in historical fact
- Extract deterministic pre-failure signals

This document is not user-facing.

---

## CONTROL_PLANE_LOSS

Representative outages:
- Amazon Web Services EC2 control-plane outage (us-east-1, Nov 2020)
- Microsoft Azure ARM outage (Sept 2020)

Primary failure:
Loss of authoritative control APIs while underlying resources continued running.

Pre-failure signals:
- Control-plane API latency rising while data-plane traffic remains stable
- Partial success / timeout patterns on provisioning and scaling calls
- Increased reliance on cached control state

Economic impact:
- Inability to deploy, scale, or recover services
- Multi-hour regional downtime
- Tens to hundreds of millions in downstream losses

---

## AUTHORITY_INCONSISTENCY

Representative outages:
- AWS internal DNS split-brain events
- Multi-region Kubernetes control-plane divergence incidents

Primary failure:
Multiple control authorities simultaneously believe they are primary.

Pre-failure signals:
- Conflicting control-plane state across regions
- Divergent leader-election outcomes
- Write success in one region, rejection in another

Economic impact:
- Data corruption risk
- Forced global freezes
- Prolonged recovery windows

---

## SHARED_DEPENDENCY_COLLAPSE

Representative outages:
- Meta global outage (Oct 2021 – BGP + DNS)
- Cloudflare internal dependency outages

Primary failure:
Failure of a central shared service (DNS, IAM, auth) underpinning many systems.

Pre-failure signals:
- Authentication latency spikes across unrelated services
- Elevated error rates tied to identity or name resolution
- Control-plane health masking dependency failure

Economic impact:
- Global service unavailability
- Billions in lost revenue and market cap movement

---

## HIDDEN_TRANSITIVE_DEPENDENCY

Representative outages:
- AWS logging / metrics dependencies impacting request paths
- Cloud services failing when “non-critical” telemetry systems went down

Primary failure:
Undocumented dependency becomes critical at runtime.

Pre-failure signals:
- Increased tail latency correlated with observability services
- Failures only under load or degraded modes
- Inconsistent dependency graphs across teams

Economic impact:
- Hard-to-diagnose outages
- Long MTTR due to incorrect mental models

---

## CONFIGURATION_FANOUT

Representative outages:
- Cloudflare global routing configuration outage (July 2020)
- Global feature-flag misconfigurations at multiple SaaS providers

Primary failure:
Single configuration change propagated globally without blast-radius control.

Pre-failure signals:
- High-velocity config propagation
- Absence of regional or staged rollouts
- Config applied faster than verification

Economic impact:
- Instant global outage
- Near-zero reaction time
- Massive customer impact

---

## IRREVERSIBLE_CONFIGURATION_STATE

Representative outages:
- Database schema changes causing prolonged downtime
- Control-plane upgrades that mutate persistent state

Primary failure:
Rollback impossible due to state mutation.

Pre-failure signals:
- Schema or state changes without reversible migrations
- One-way upgrade paths
- Rollback plans that depend on ideal conditions

Economic impact:
- Extended outages
- Forced rebuilds or restores
- Data loss risk

---

## CASCADING_RESOURCE_EXHAUSTION

Representative outages:
- Retry storms during partial cloud outages
- API throttling cascades at scale

Primary failure:
Failure induces retries; retries amplify load; load deepens failure.

Pre-failure signals:
- Rapid increase in retry rates
- CPU / connection pool exhaustion
- Latency cliffs instead of gradual degradation

Economic impact:
- Self-sustaining outages
- Infrastructure cost spikes
- Customer-facing downtime

---

## TIME_SKEW_AMPLIFICATION

Representative outages:
- Certificate expiry events
- Lease / lock expiry failures in distributed systems

Primary failure:
Correct logic fails due to time divergence.

Pre-failure signals:
- Clock skew across nodes
- Approaching cert / lease expiry windows
- Time-based assumptions unverified at runtime

Economic impact:
- Sudden service failure
- Security incidents
- Forced emergency rotations

---

## RECOVERY_SYSTEM_FAILURE

Representative outages:
- Auto-remediation loops worsening outages
- Failover logic repeatedly flapping services

Primary failure:
Recovery mechanism becomes the outage.

Pre-failure signals:
- Automated remediation triggering repeatedly
- Oscillating failovers
- Recovery actions increasing error rates

Economic impact:
- Prolonged outages
- Loss of operator trust in automation

---

## SAFETY_MECHANISM_LOCKOUT

Representative outages:
- Rate limiters blocking administrators
- Safety interlocks preventing restart or rollback

Primary failure:
Safeguards prevent recovery once in abnormal state.

Pre-failure signals:
- Admin actions treated as hostile traffic
- Safety rules without override paths
- Control-plane rate limits shared with operators

Economic impact:
- Recovery paralysis
- Extended downtime despite human availability

---

## OPERATOR_BLINDNESS

Representative outages:
- Telemetry loss during major incidents
- Conflicting dashboards across systems

Primary failure:
No authoritative system truth during failure.

Pre-failure signals:
- Monitoring depends on same systems being monitored
- Inconsistent metrics sources
- Alert storms with no signal hierarchy

Economic impact:
- Slowed diagnosis
- Human error under pressure

---

## PRIVILEGE_ACCESS_DEADLOCK

Representative outages:
- IAM outages blocking remediation
- Bastion or jump-host dependency failures

Primary failure:
Humans cannot intervene because access systems fail with the system.

Pre-failure signals:
- Access paths coupled to primary infrastructure
- No out-of-band admin access
- Centralized identity without fallback

Economic impact:
- Inability to recover
- Escalation to extreme measures (provider intervention)

---

## Phase 2 Status

- Ontology validated
- Grounded in real-world outages
- Deterministic pre-failure signals identified