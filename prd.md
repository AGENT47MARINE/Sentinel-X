# SentinelX V2 — Product Requirements Document

**Version:** 2.0  
**Status:** Draft  
**Last Updated:** March 2026

---

## 1. Executive Summary

SentinelX V2 is an AI Trust Orchestration Layer built for enterprises operating LLMs and autonomous agent systems. It provides continuous, real-time risk evaluation across the full AI pipeline — from user input through retrieval, model inference, agent actions, inter-agent communication, and persistent memory — and synthesizes all signals into a unified trust verdict with recommended interventions.

The product addresses a validated gap: enterprise AI security tooling has not kept pace with the architectural complexity of modern agentic AI systems. Existing tools protect the prompt and output surface only. SentinelX V2 protects the entire trust chain.

---

## 2. Problem Statement

### 2.1 The Evolved Threat Landscape

The enterprise AI attack surface in 2026 spans five distinct layers that existing tools do not address:

| Layer | Threat | Existing Coverage |
|---|---|---|
| Prompt / Input | Injection, jailbreak, insider misuse | Partial |
| Retrieval / RAG | Knowledge poisoning, tenant leakage, embedding inversion | None |
| MCP / Plugins | Supply chain attacks, hidden instruction injection | None |
| Agent Actions | Unauthorized execution, privilege escalation | None |
| Inter-Agent Comms | Spoofed messages, goal hijacking across agent fleets | None |
| Memory Stores | Cross-session poisoning, behavioral corruption | None |
| Shadow AI | Unsanctioned AI usage, unmonitored data flows | None |

### 2.2 Business Impact

- Average enterprise has 1,200+ shadow AI applications with no visibility
- 48% of security professionals identify agentic AI as the #1 attack vector heading into 2026
- Only 34% of enterprises have any AI-specific security controls deployed
- Memory poisoning and MCP supply chain attacks are now documented in OWASP Agentic Top 10 (2026)

---

## 3. Goals & Non-Goals

### Goals
- Provide real-time trust evaluation across the full AI pipeline
- Enable human oversight of high-risk agentic actions before execution
- Surface compliance posture against GDPR, HIPAA, NIST AI RMF, and ISO 42001
- Detect and govern shadow AI usage across the enterprise
- Integrate into existing stacks without requiring architectural changes

### Non-Goals
- SentinelX is not a replacement for identity and access management (IAM) systems
- SentinelX does not train or fine-tune AI models
- SentinelX does not provide LLM inference — it wraps existing inference infrastructure
- V2 does not include a self-hosted model marketplace

---

## 4. Target Users

| Persona | Role | Primary Need |
|---|---|---|
| CISO / Security Team | Owns AI risk posture | Real-time threat detection, audit trail, compliance reporting |
| AI/ML Engineering | Builds and deploys LLM systems | Drop-in integration, structured risk signals, drift monitoring |
| Compliance / Legal | Manages regulatory exposure | GDPR/HIPAA/NIST/ISO readiness scores, evidence export |
| Platform Engineering | Operates AI infrastructure | Kubernetes sidecar, middleware API, observability |
| Executive / Board | Owns business risk | Risk dashboard, financial exposure estimates, incident history |

---

## 5. Core Modules — Detailed Requirements

### 5.1 Prompt Guard

**Purpose:** Detect malicious, manipulative, or policy-violating user inputs before they reach the model.

**Functional Requirements:**
- FR-PG-01: Classify intent across four categories: `benign`, `probing`, `exploitative`, `adversarial`
- FR-PG-02: Track prompt patterns across sessions per user; detect escalating adversarial behavior
- FR-PG-03: Compute insider risk score based on behavioral history and access patterns
- FR-PG-04: Run synthetic adversary simulations to proactively identify new attack patterns
- FR-PG-05: Produce structured JSON output including attack probability, intent class, escalation trend, insider risk score

**Performance Requirements:**
- PR-PG-01: P99 latency ≤ 50ms for synchronous prompt evaluation
- PR-PG-02: False positive rate ≤ 3% on benign enterprise prompts

---

### 5.2 Retrieval Integrity Engine

**Purpose:** Protect the RAG layer from poisoning, cross-tenant data leakage, low-authority sources, and embedding inversion attacks.

**Functional Requirements:**
- FR-RI-01: Detect anomalous embeddings that indicate knowledge store poisoning
- FR-RI-02: Track document hash, timestamp, and source lineage for all retrieved chunks
- FR-RI-03: Enforce namespace boundaries between tenants; flag cross-tenant anomalies
- FR-RI-04: Score retrieved sources by authority, independence, and consensus confidence
- FR-RI-05 *(New)*: Detect Vec2Text-style embedding inversion attempts against vector database contents; alert when reconstruction probability exceeds configurable threshold

**Performance Requirements:**
- PR-RI-01: Retrieval integrity check must not increase RAG pipeline latency by more than 20ms P99

---

### 5.3 MCP / Plugin Integrity Verifier *(New)*

**Purpose:** Validate the integrity and behavior of MCP servers and third-party plugins before and during execution.

**Functional Requirements:**
- FR-MCP-01: Verify plugin signatures and hashes against a trusted registry before any execution
- FR-MCP-02: Monitor runtime behavior per plugin call; detect deviations from expected behavioral profile
- FR-MCP-03: Scan all content received from MCP servers for hidden instructions or injection payloads
- FR-MCP-04: Perform dependency chain analysis for npm/PyPI packages used by plugins
- FR-MCP-05: Enforce privilege scope per plugin; block calls that exceed declared permissions
- FR-MCP-06: Maintain a plugin allowlist/blocklist with operator override capability

**Security Requirements:**
- SR-MCP-01: Any plugin that fails signature verification must be blocked by default
- SR-MCP-02: Injection scan must run on all inbound MCP content before it enters the model context

---

### 5.4 Output Grounding & Safety Engine

**Purpose:** Evaluate LLM outputs for factual grounding, safety, code risk, and data leakage.

**Functional Requirements:**
- FR-OG-01: Map each output sentence to its source retrieval chunk (span-level attribution)
- FR-OG-02: Score output grounding confidence using entailment-based verification
- FR-OG-03: Flag unsupported claims — output sentences with no retrievable evidence
- FR-OG-04: Analyze any code or commands in output for destructive operations and injection risk
- FR-OG-05: Scan outputs for PII, API keys, tokens, credentials, and confidential source bleed

**Performance Requirements:**
- PR-OG-01: Grounding analysis must complete within 100ms P95 for standard output length (≤ 1,000 tokens)

---

### 5.5 Agent Action Risk Engine *(Enhanced)*

**Purpose:** Evaluate and govern autonomous agent actions before execution, including validating the authority chain that produced the action.

**Functional Requirements:**
- FR-AA-01: Score each action on irreversibility (0.0–1.0)
- FR-AA-02: Estimate blast radius: number of systems, accounts, and users affected
- FR-AA-03: Evaluate action against corporate policy ruleset; compute conflict probability
- FR-AA-04: Estimate financial exposure range for high-impact actions
- FR-AA-05 *(New)*: Verify the identity and privilege level of the originating agent
- FR-AA-06 *(New)*: Trace the full instruction chain back to the original authorized human user
- FR-AA-07 *(New)*: Reject actions where instructions were routed through an agent with insufficient privilege, regardless of the action's own risk score
- FR-AA-08: Route any action with `irreversibility_score > 0.8` OR `requires_human_approval: true` to the human approval queue before execution

**Security Requirements:**
- SR-AA-01: No action with `privilege_chain_valid: false` may be auto-approved under any configuration

---

### 5.6 Inter-Agent Communication Monitor *(New)*

**Purpose:** Secure the communication fabric between agents in multi-agent systems and detect goal hijacking, spoofed messages, and unauthorized delegation.

**Functional Requirements:**
- FR-IA-01: Authenticate the origin of all inter-agent messages using cryptographic identity
- FR-IA-02: Detect goal drift by comparing each agent's stated objective against the original task
- FR-IA-03: Verify that delegation chains (agent A instructing agent B) are authorized by policy
- FR-IA-04: Monitor agent cluster behavior for coordinated anomalies not detectable at the individual agent level
- FR-IA-05: Alert on any agent receiving instructions from an unregistered or unverified agent

---

### 5.7 Memory & Context Poisoning Detector *(New)*

**Purpose:** Protect persistent memory stores from being corrupted in ways that alter agent behavior across sessions.

**Functional Requirements:**
- FR-MP-01: Perform integrity verification on memory stores at configurable intervals and on every write
- FR-MP-02: Compute a behavioral delta score by comparing recent agent behavior against memory-less baseline
- FR-MP-03: Detect semantic drift in stored context — gradual changes inconsistent with legitimate use
- FR-MP-04: Enforce write authorization: only approved agents and sessions may modify persistent memory
- FR-MP-05: Automatically quarantine suspicious memory records and log affected session IDs
- FR-MP-06: Provide memory rollback capability to a verified-clean snapshot

---

### 5.8 Behavioral Drift Monitor

**Purpose:** Detect silent model changes, policy degradation, and reasoning pattern shifts over time.

**Functional Requirements:**
- FR-BD-01: Establish and maintain a behavioral baseline for each deployed model and agent
- FR-BD-02: Track output entropy across rolling time windows
- FR-BD-03: Monitor policy compliance rate as a continuous metric
- FR-BD-04: Alert when drift score, compliance drop, or reasoning variance exceeds configurable thresholds

---

### 5.9 Compliance & Regulatory Engine *(Enhanced)*

**Purpose:** Map AI pipeline risk signals to regulatory and governance frameworks required by enterprise legal and compliance teams.

**Functional Requirements:**
- FR-CR-01: Evaluate data exposure risk against GDPR requirements per jurisdiction
- FR-CR-02: Classify healthcare-sensitive content under HIPAA guidelines
- FR-CR-03: Enforce financial advisory disclaimer requirements where applicable
- FR-CR-04 *(New)*: Score alignment with each pillar of the NIST AI Risk Management Framework (Govern, Map, Measure, Manage)
- FR-CR-05 *(New)*: Produce ISO 42001 audit readiness score with gap analysis
- FR-CR-06: Export compliance evidence reports in formats accepted by enterprise audit workflows

---

### 5.10 Shadow AI Discovery Engine *(New)*

**Purpose:** Discover and risk-classify unsanctioned AI usage across the enterprise to close the governance blind spot.

**Functional Requirements:**
- FR-SA-01: Fingerprint network traffic to identify calls to known AI API endpoints (OpenAI, Anthropic, Cohere, Google, Meta, Mistral, and others)
- FR-SA-02: Detect AI usage from unsanctioned models or applications
- FR-SA-03: Map data categories flowing through shadow AI instances
- FR-SA-04: Risk-classify each discovered instance: `low / medium / high / critical`
- FR-SA-05: Generate automated policy enforcement recommendations per discovered instance
- FR-SA-06: Produce a Shadow AI inventory report exportable to security and compliance teams

**Privacy Requirements:**
- PR-SA-01: Traffic fingerprinting must operate on metadata and endpoint signatures only; content inspection of employee traffic requires explicit operator opt-in and appropriate legal basis

---

### 5.11 Trust Orchestrator — Cascading Risk Chain Model *(Enhanced)*

**Purpose:** Fuse all module signals into a unified trust verdict, modeling causal relationships between risk dimensions rather than treating them as independent variables.

**Functional Requirements:**
- FR-TO-01: Maintain a risk vector with one dimension per active module
- FR-TO-02: Define and evaluate causal chain rules (e.g., high action risk + invalid agent identity → CRITICAL regardless of other scores)
- FR-TO-03: Produce an overall trust score and a contextual trust profile per request
- FR-TO-04: Output one of four interventions: `monitor`, `throttle`, `human_review`, `block`
- FR-TO-05: Expose all orchestration logic as configurable rules accessible to operators

**Causal Chain Rule Examples:**
- `action_risk > 0.7` AND `agent_identity_risk > 0.5` → `CRITICAL / block`
- `memory_integrity < 0.5` AND `drift_score > 0.6` → `human_review`
- `mcp_injection_detected = true` → `block` (no other conditions required)

---

## 6. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Latency | Full pipeline evaluation (excluding Shadow AI) ≤ 200ms P99 |
| Availability | 99.9% uptime SLA for middleware API deployment |
| Scalability | Horizontal scaling; stateless module design |
| Data Residency | All evaluation data must remain within customer-configured region |
| Auditability | All risk decisions logged with full input/output snapshots, immutable for 90 days minimum |
| Configurability | All thresholds, rules, and intervention policies configurable per tenant |

---

## 7. Deployment Architecture

| Mode | Target Customer | Description |
|---|---|---|
| Middleware API | Any LLM consumer | Drop-in HTTPS proxy; route existing LLM calls through SentinelX |
| Kubernetes Sidecar | Cloud-native enterprises | Container deployed alongside agent pods in the same namespace |
| LangChain Plugin | LLM application developers | Native middleware hooks for chain evaluation |
| LlamaIndex Plugin | RAG application developers | Native hooks for retrieval integrity and grounding |
| A2A Fabric Proxy | Multi-agent system operators | Transparent proxy on inter-agent communication channels |

---

## 8. Phased Delivery Plan

### Phase 1 — Foundational Trust *(Target: Q2 2026)*
Prompt Guard · Retrieval Integrity + Embedding Inversion Guard · Output Grounding · MCP/Plugin Integrity Verifier · Memory Poisoning Detector · Cascading Risk Chain Orchestrator · Core API

### Phase 2 — Enterprise Security *(Target: Q3 2026)*
Agent Action Risk + Identity Verification · Inter-Agent Communication Monitor · Tenant Isolation Verifier · Full Compliance Layer (GDPR/HIPAA/NIST AI RMF/ISO 42001) · Sensitive Data Tracing · Shadow AI Discovery · Enterprise Dashboard v1

### Phase 3 — Autonomous Control Plane *(Target: Q4 2026)*
Behavioral Drift Detection · Economic Impact Model · Red-Team Simulation Engine · Full Dashboard + Analytics · Automated Policy Enforcement · Regulatory Evidence Export · Per-Agent Risk Profiles

---

## 9. Success Metrics

| Metric | Target |
|---|---|
| False positive rate (benign prompts blocked) | ≤ 3% |
| Agent action risk detection accuracy | ≥ 92% on labeled test set |
| MCP injection detection rate | ≥ 95% on known attack patterns |
| Memory poisoning detection latency | ≤ 2 sessions after initial write |
| Shadow AI discovery coverage | ≥ 85% of AI API endpoints in use |
| Time to integrate (middleware API mode) | ≤ 2 hours for engineering team |
| NIST AI RMF alignment score improvement | ≥ 0.2 improvement within 90 days of deployment |

---

## 10. Open Questions

1. Should Shadow AI discovery require a dedicated network sensor, or can it operate purely on egress proxy data?
2. What is the preferred memory store integration pattern — agent framework SDK hooks, or database-level write interceptors?
3. ISO 42001 audit readiness scoring — should this be self-assessed via questionnaire integration, or derived purely from runtime signal data?
4. What is the minimum viable dashboard for Phase 1 — CLI/API output only, or a lightweight web UI?

---

*SentinelX V2 PRD — Internal working document. Not for external distribution without review.*