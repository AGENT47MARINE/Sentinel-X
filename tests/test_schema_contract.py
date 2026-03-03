from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from schemas import TrustOrchestratorInput


def valid_payload() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": "v1",
        "request_id": "req_001",
        "prompt_guard": {
            "schema_version": "v1",
            "attack_probability": 0.2,
            "intent_class": "benign",
            "escalation_trend": "stable",
            "insider_risk_score": 0.1,
            "top_signals": ["normal_usage"],
        },
        "retrieval_integrity": {
            "schema_version": "v1",
            "poison_risk": 0.1,
            "provenance_integrity": 0.95,
            "tenant_isolation_status": "clean",
            "consensus_confidence": 0.8,
            "embedding_inversion_risk": "low",
        },
        "mcp_integrity": {
            "schema_version": "v1",
            "plugin_id": "email-connector-v3",
            "signature_valid": True,
            "runtime_anomaly_detected": False,
            "injection_scan_result": "clean",
            "privilege_scope_violations": 0,
            "dependency_risk": "low",
        },
        "output_grounding": {
            "schema_version": "v1",
            "grounding_score": 0.91,
            "unsupported_spans": 0,
            "hallucination_probability": 0.05,
            "data_leakage_risk": "low",
            "code_execution_risk": "none",
            "pii_detected": False,
        },
        "agent_action": {
            "schema_version": "v1",
            "action": "transfer_funds",
            "action_category": "transfer",
            "irreversibility_score": 0.95,
            "blast_radius": "multi-account",
            "blast_radius_estimate": 150,
            "financial_risk_estimate": "high",
            "financial_exposure_range": "$50K-$1M",
            "requires_human_approval": True,
            "agent_identity_verified": True,
            "originating_agent": "finance-bot-v2",
            "privilege_chain_valid": False,
            "privilege_violation": "instruction_routed_through_low_privilege_agent",
        },
        "inter_agent": {
            "schema_version": "v1",
            "message_origin_verified": True,
            "goal_drift_detected": False,
            "goal_similarity_score": 0.93,
            "delegation_chain_valid": True,
            "anomalous_cluster_behavior": False,
            "flagged_agents": [],
        },
        "memory_poisoning": {
            "schema_version": "v1",
            "memory_store_integrity": 0.9,
            "suspicious_writes_detected": 0,
            "behavioral_delta_score": 0.1,
            "quarantine_triggered": False,
            "affected_session_ids": [],
            "last_clean_snapshot": now,
        },
        "drift_monitor": {
            "schema_version": "v1",
            "model_drift_score": 0.33,
            "compliance_drop": 0.08,
            "reasoning_variance": "elevated",
            "drift_alert_level": "medium",
            "top_drift_signals": ["entropy_increase"],
            "baseline_version": "v2.1-2026-02-01",
        },
        "compliance": {
            "schema_version": "v1",
            "jurisdiction": "EU",
            "gdpr_exposure": 0.7,
            "regulatory_classification": "sensitive_processing",
            "hipaa_risk": "low",
            "nist_ai_rmf_alignment": 0.82,
            "nist_pillar_breakdown": {
                "govern": 0.88,
                "map": 0.79,
                "measure": 0.91,
                "manage": 0.72,
            },
            "iso_42001_readiness": 0.68,
            "iso_gaps": ["incident_response_procedure"],
        },
        "shadow_ai": {
            "schema_version": "v1",
            "shadow_ai_instances_detected": 14,
            "high_risk_instances": 3,
            "data_categories_exposed": ["PII", "financial_records"],
            "top_unsanctioned_providers": ["openai", "cohere"],
            "recommended_action": "immediate_review",
            "inventory_last_updated": now,
        },
        "prompt_risk": 0.2,
        "retrieval_risk": 0.1,
        "mcp_integrity_risk": 0.05,
        "grounding_risk": 0.09,
        "action_risk": 0.8,
        "agent_identity_risk": 0.1,
        "inter_agent_risk": 0.2,
        "memory_integrity_risk": 0.15,
        "compliance_risk": 0.45,
        "drift_risk": 0.33,
        "shadow_ai_risk": 0.6,
    }


def test_trust_orchestrator_input_validates():
    payload = valid_payload()
    model = TrustOrchestratorInput.model_validate(payload)
    assert model.request_id == "req_001"
    assert model.schema_version == "v1"


def test_rejects_unknown_fields():
    payload = valid_payload()
    payload["unknown_field"] = "should_fail"
    with pytest.raises(ValidationError):
        TrustOrchestratorInput.model_validate(payload)


def test_rejects_out_of_range_risk():
    payload = valid_payload()
    payload["drift_risk"] = 1.3
    with pytest.raises(ValidationError):
        TrustOrchestratorInput.model_validate(payload)
