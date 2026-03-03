from __future__ import annotations

from datetime import datetime, timezone

from orchestrator import evaluate
from schemas import TrustOrchestratorInput


def _payload() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": "v1",
        "request_id": "req_eval_1",
        "prompt_guard": {
            "schema_version": "v1",
            "attack_probability": 0.2,
            "intent_class": "benign",
            "escalation_trend": "stable",
            "insider_risk_score": 0.1,
            "top_signals": [],
        },
        "retrieval_integrity": {
            "schema_version": "v1",
            "poison_risk": 0.2,
            "provenance_integrity": 0.9,
            "tenant_isolation_status": "clean",
            "consensus_confidence": 0.8,
            "embedding_inversion_risk": "low",
        },
        "mcp_integrity": {
            "schema_version": "v1",
            "plugin_id": "plugin-1",
            "signature_valid": True,
            "runtime_anomaly_detected": False,
            "injection_scan_result": "clean",
            "privilege_scope_violations": 0,
            "dependency_risk": "low",
        },
        "output_grounding": {
            "schema_version": "v1",
            "grounding_score": 0.92,
            "unsupported_spans": 0,
            "hallucination_probability": 0.05,
            "data_leakage_risk": "low",
            "code_execution_risk": "none",
            "pii_detected": False,
        },
        "agent_action": {
            "schema_version": "v1",
            "action": "read_statement",
            "action_category": "read",
            "irreversibility_score": 0.1,
            "blast_radius": "single-user",
            "blast_radius_estimate": 1,
            "financial_risk_estimate": "low",
            "financial_exposure_range": "<$1K",
            "requires_human_approval": False,
            "agent_identity_verified": True,
            "originating_agent": "assistant-1",
            "privilege_chain_valid": True,
            "privilege_violation": None,
        },
        "inter_agent": {
            "schema_version": "v1",
            "message_origin_verified": True,
            "goal_drift_detected": False,
            "goal_similarity_score": 0.95,
            "delegation_chain_valid": True,
            "anomalous_cluster_behavior": False,
            "flagged_agents": [],
        },
        "memory_poisoning": {
            "schema_version": "v1",
            "memory_store_integrity": 0.95,
            "suspicious_writes_detected": 0,
            "behavioral_delta_score": 0.05,
            "quarantine_triggered": False,
            "affected_session_ids": [],
            "last_clean_snapshot": now,
        },
        "drift_monitor": {
            "schema_version": "v1",
            "model_drift_score": 0.2,
            "compliance_drop": 0.05,
            "reasoning_variance": "stable",
            "drift_alert_level": "low",
            "top_drift_signals": [],
            "baseline_version": "v2.1-2026-02-01",
        },
        "compliance": {
            "schema_version": "v1",
            "jurisdiction": "EU",
            "gdpr_exposure": 0.3,
            "regulatory_classification": "standard_processing",
            "hipaa_risk": "low",
            "nist_ai_rmf_alignment": 0.8,
            "nist_pillar_breakdown": {"govern": 0.8, "map": 0.8, "measure": 0.8, "manage": 0.8},
            "iso_42001_readiness": 0.75,
            "iso_gaps": [],
        },
        "shadow_ai": {
            "schema_version": "v1",
            "shadow_ai_instances_detected": 0,
            "high_risk_instances": 0,
            "data_categories_exposed": [],
            "top_unsanctioned_providers": [],
            "recommended_action": "monitor",
            "inventory_last_updated": now,
        },
        "prompt_risk": 0.2,
        "retrieval_risk": 0.2,
        "mcp_integrity_risk": 0.1,
        "grounding_risk": 0.1,
        "action_risk": 0.1,
        "agent_identity_risk": 0.1,
        "inter_agent_risk": 0.1,
        "memory_integrity_risk": 0.1,
        "compliance_risk": 0.2,
        "drift_risk": 0.2,
        "shadow_ai_risk": 0.1,
    }


def test_engine_returns_monitor_for_low_risk_payload():
    payload = TrustOrchestratorInput.model_validate(_payload())
    verdict = evaluate(payload)
    assert verdict.intervention == "monitor"
    assert verdict.overall_trust_score > 0.7


def test_engine_blocks_on_action_identity_chain():
    data = _payload()
    data["action_risk"] = 0.9
    data["agent_identity_risk"] = 0.8
    payload = TrustOrchestratorInput.model_validate(data)
    verdict = evaluate(payload)
    assert verdict.intervention == "block"
    assert "action_identity_chain" in verdict.causal_chains_triggered
