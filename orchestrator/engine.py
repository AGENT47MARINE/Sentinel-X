from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from schemas import TrustOrchestratorInput


Intervention = Literal["monitor", "throttle", "human_review", "block"]


@dataclass(frozen=True)
class TrustVerdict:
    overall_trust_score: float
    intervention: Intervention
    causal_chains_triggered: list[str]
    contextual_profile: str


def evaluate(payload: TrustOrchestratorInput) -> TrustVerdict:
    # Default causal-chain rules from Phase 1 tasks.
    chains: list[str] = []
    intervention: Intervention = "monitor"

    if payload.action_risk > 0.7 and payload.agent_identity_risk > 0.5:
        chains.append("action_identity_chain")
        intervention = "block"
    elif payload.memory_integrity_risk > 0.5 and payload.drift_risk > 0.6:
        chains.append("memory_drift_chain")
        intervention = "human_review"

    if payload.mcp_integrity.injection_scan_result == "malicious":
        chains.append("mcp_injection_chain")
        intervention = "block"

    if payload.agent_action.privilege_chain_valid is False and intervention != "block":
        chains.append("privilege_chain_violation")
        intervention = "human_review"

    risk_values = [
        payload.prompt_risk,
        payload.retrieval_risk,
        payload.mcp_integrity_risk,
        payload.grounding_risk,
        payload.action_risk,
        payload.agent_identity_risk,
        payload.inter_agent_risk,
        payload.memory_integrity_risk,
        payload.compliance_risk,
        payload.drift_risk,
        payload.shadow_ai_risk,
    ]
    avg_risk = sum(risk_values) / len(risk_values)
    trust_score = round(max(0.0, min(1.0, 1.0 - avg_risk)), 4)

    # Threshold fallback only when causal rules did not already force stricter action.
    if not chains:
        if avg_risk >= 0.75:
            intervention = "block"
        elif avg_risk >= 0.5:
            intervention = "human_review"
        elif avg_risk >= 0.3:
            intervention = "throttle"
        else:
            intervention = "monitor"

    profile_parts: list[str] = []
    profile_parts.append("action-risk-high" if payload.action_risk > 0.6 else "action-risk-stable")
    profile_parts.append("grounding-weak" if payload.grounding_risk > 0.5 else "grounding-strong")
    profile_parts.append("memory-integrity-weak" if payload.memory_integrity_risk > 0.5 else "memory-integrity-strong")

    return TrustVerdict(
        overall_trust_score=trust_score,
        intervention=intervention,
        causal_chains_triggered=chains,
        contextual_profile=",".join(profile_parts),
    )
