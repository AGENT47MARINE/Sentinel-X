from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SchemaVersion = Literal["v1"]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: SchemaVersion = "v1"


class PromptGuardOutput(ContractModel):
    attack_probability: float = Field(ge=0.0, le=1.0)
    intent_class: str
    escalation_trend: Literal["decreasing", "stable", "increasing"]
    insider_risk_score: float = Field(ge=0.0, le=1.0)
    top_signals: list[str] = Field(default_factory=list)


class RetrievalIntegrityOutput(ContractModel):
    poison_risk: float = Field(ge=0.0, le=1.0)
    provenance_integrity: float = Field(ge=0.0, le=1.0)
    tenant_isolation_status: Literal["clean", "anomaly", "violation"]
    consensus_confidence: float = Field(ge=0.0, le=1.0)
    embedding_inversion_risk: Literal["low", "medium", "high", "critical"]


class MCPIntegrityOutput(ContractModel):
    plugin_id: str
    signature_valid: bool
    runtime_anomaly_detected: bool
    injection_scan_result: Literal["clean", "suspicious", "malicious"]
    privilege_scope_violations: int = Field(ge=0)
    dependency_risk: Literal["low", "medium", "high", "critical"]


class OutputGroundingOutput(ContractModel):
    grounding_score: float = Field(ge=0.0, le=1.0)
    unsupported_spans: int = Field(ge=0)
    hallucination_probability: float = Field(ge=0.0, le=1.0)
    data_leakage_risk: Literal["none", "low", "medium", "high", "critical"]
    code_execution_risk: Literal["none", "low", "medium", "high", "critical"]
    pii_detected: bool


class AgentActionOutput(ContractModel):
    action: str
    action_category: Literal["read", "write", "execute", "transfer", "communicate", "delete"]
    irreversibility_score: float = Field(ge=0.0, le=1.0)
    blast_radius: Literal["single-user", "multi-user", "account", "multi-account", "organization"]
    blast_radius_estimate: int = Field(ge=0)
    financial_risk_estimate: Literal["low", "medium", "high", "critical"]
    financial_exposure_range: str
    requires_human_approval: bool
    agent_identity_verified: bool
    originating_agent: str
    privilege_chain_valid: bool
    privilege_violation: str | None = None


class InterAgentOutput(ContractModel):
    message_origin_verified: bool
    goal_drift_detected: bool
    goal_similarity_score: float = Field(ge=0.0, le=1.0)
    delegation_chain_valid: bool
    anomalous_cluster_behavior: bool
    flagged_agents: list[str] = Field(default_factory=list)


class MemoryPoisoningOutput(ContractModel):
    memory_store_integrity: float = Field(ge=0.0, le=1.0)
    suspicious_writes_detected: int = Field(ge=0)
    behavioral_delta_score: float = Field(ge=0.0, le=1.0)
    quarantine_triggered: bool
    affected_session_ids: list[str] = Field(default_factory=list)
    last_clean_snapshot: datetime


class DriftMonitorOutput(ContractModel):
    model_drift_score: float = Field(ge=0.0, le=1.0)
    compliance_drop: float = Field(ge=0.0, le=1.0)
    reasoning_variance: Literal["stable", "elevated", "high"]
    drift_alert_level: Literal["low", "medium", "high", "critical"]
    top_drift_signals: list[str] = Field(default_factory=list)
    baseline_version: str


class NISTPillarBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")
    govern: float = Field(ge=0.0, le=1.0)
    map: float = Field(ge=0.0, le=1.0)
    measure: float = Field(ge=0.0, le=1.0)
    manage: float = Field(ge=0.0, le=1.0)


class ComplianceOutput(ContractModel):
    jurisdiction: str
    gdpr_exposure: float = Field(ge=0.0, le=1.0)
    regulatory_classification: str
    hipaa_risk: Literal["none", "low", "medium", "high", "critical"]
    nist_ai_rmf_alignment: float = Field(ge=0.0, le=1.0)
    nist_pillar_breakdown: NISTPillarBreakdown
    iso_42001_readiness: float = Field(ge=0.0, le=1.0)
    iso_gaps: list[str] = Field(default_factory=list)


class ShadowAIOutput(ContractModel):
    shadow_ai_instances_detected: int = Field(ge=0)
    high_risk_instances: int = Field(ge=0)
    data_categories_exposed: list[str] = Field(default_factory=list)
    top_unsanctioned_providers: list[str] = Field(default_factory=list)
    recommended_action: Literal["monitor", "review", "immediate_review", "block", "remediate"]
    inventory_last_updated: datetime


class TrustOrchestratorInput(ContractModel):
    request_id: str

    prompt_guard: PromptGuardOutput
    retrieval_integrity: RetrievalIntegrityOutput
    mcp_integrity: MCPIntegrityOutput
    output_grounding: OutputGroundingOutput

    agent_action: AgentActionOutput
    inter_agent: InterAgentOutput
    memory_poisoning: MemoryPoisoningOutput

    drift_monitor: DriftMonitorOutput
    compliance: ComplianceOutput
    shadow_ai: ShadowAIOutput

    # Normalized risks consumed by TO-01 vector. These are explicit to avoid
    # coupling orchestrator math to per-module internal scoring details.
    prompt_risk: float = Field(ge=0.0, le=1.0)
    retrieval_risk: float = Field(ge=0.0, le=1.0)
    mcp_integrity_risk: float = Field(ge=0.0, le=1.0)
    grounding_risk: float = Field(ge=0.0, le=1.0)
    action_risk: float = Field(ge=0.0, le=1.0)
    agent_identity_risk: float = Field(ge=0.0, le=1.0)
    inter_agent_risk: float = Field(ge=0.0, le=1.0)
    memory_integrity_risk: float = Field(ge=0.0, le=1.0)
    compliance_risk: float = Field(ge=0.0, le=1.0)
    drift_risk: float = Field(ge=0.0, le=1.0)
    shadow_ai_risk: float = Field(ge=0.0, le=1.0)
