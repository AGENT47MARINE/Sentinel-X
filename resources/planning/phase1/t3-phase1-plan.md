# T3 Phase 1 Plan (Team Lead)

Owner: T3 (Team Lead)
Date: 2026-03-04
Scope: Behavioral Drift Monitor, Compliance Engine, Shadow AI Discovery, Platform/Integration leadership

## 1) Sprint Objective
Deliver Team Lead-owned Phase 1 foundations and unblock Member 1/Member 2 integration by locking schema contracts, risk-vector inputs, and shared test fixtures.

## 2) Priority Order (Execution)
1. LR-01: Schema sign-off and ownership boundaries (blocker for everyone)
2. INF-01: Monorepo scaffolding + CODEOWNERS + CI baseline
3. BD-01 to BD-03: Behavioral Drift Monitor MVP
4. CR-01 to CR-05: Compliance Engine MVP (GDPR/HIPAA + NIST/ISO scoring + outputs)
5. SA-01 to SA-05: Shadow AI Discovery MVP + inventory outputs
6. LR-03: Cross-module integration fixtures and weekly smoke suite
7. DASH-01: Decide CLI/API vs lightweight web UI and implement selected MVP

## 3) Week-by-Week Plan

### Week 1 (Unblock + Contracts)
- Approve SC-01 schema contract in `schemas/`
- Define canonical Team Lead output schemas:
  - Drift output
  - Compliance output
  - Shadow AI output
- Finalize integration contract for TO risk vector fields:
  - `drift_risk`, `compliance_risk`, `shadow_ai_risk`
- Establish `tests/fixtures/` seed sets for:
  - poisoned docs
  - spoofed inter-agent messages
  - synthetic risky prompts

Exit Criteria:
- SC-01 approved by Team Lead
- Schema version `v1` tagged and referenced by all modules

### Week 2 (Behavioral Drift + Compliance Core)
- Implement baseline capture (per model + environment)
- Implement composite drift score with explainability
- Implement GDPR/HIPAA classifiers and disclaimer enforcement
- Implement NIST pillar mapping framework and score method doc

Exit Criteria:
- Drift score pipeline runs on rolling window
- Compliance score reproducible from logged signals

### Week 3 (Shadow AI + Export + Integration)
- Implement AI endpoint fingerprint DB and unsanctioned detection
- Build inventory persistence and risk classification
- Implement compliance evidence export (JSON first, PDF second)
- Run first end-to-end integration smoke suite

Exit Criteria:
- Shadow AI inventory exports JSON/CSV
- End-to-end evaluation path passes defined smoke tests

### Week 4 (Hardening + Dashboard Decision)
- Tune thresholds for drift/compliance/shadow-ai alerts
- Resolve review queue backlog (LR-02 items)
- Deliver MVP dashboard mode decision and implementation
- Freeze Phase 1 release candidate and handoff notes

Exit Criteria:
- Review turnaround SLA <= 24h achieved
- Phase 1 Team Lead scope marked release-ready

## 4) Deliverables by Epic

### Behavioral Drift (BD)
- Baseline capture service
- Rolling drift engine (entropy + compliance delta + reasoning variance)
- Alert router (dashboard + webhook)
- Canonical JSON schema + validation tests

### Compliance (CR)
- GDPR/HIPAA/financial disclaimer checks
- NIST AI RMF scorer + pillar breakdown
- ISO 42001 readiness + actionable gaps
- Evidence exporter (JSON/PDF)
- Canonical JSON schema + tests

### Shadow AI (SA)
- Fingerprint registry (providers, headers, endpoint patterns)
- Unsanctioned endpoint detector
- Data flow mapper + risk classifier
- Persistent inventory + policy recommendations
- Canonical JSON schema + tests

## 5) Decisions Needed This Sprint
1. DASH-01: CLI/API only vs lightweight web UI
2. SA implementation: proxy-first vs sensor-first integration
3. ISO scoring source: runtime-only vs runtime + questionnaire
4. Memory integration preference for Phase 2 readiness: SDK hooks vs DB interceptors

## 6) Review Queue SLA (LR-02)
- Daily review window: fixed 2 slots/day
- Max turnaround: 24h
- Escalate blockers immediately if:
  - schema mismatch
  - latency budget regression
  - trust verdict determinism risk

## 7) Suggested Next Implementation Slice
1. Build `schemas/` contract pack for all module outputs
2. Implement Team Lead schemas and stubs:
   - drift
   - compliance
   - shadow_ai
3. Connect to Member 2 TO-01 via mock risk vector fixture tests
