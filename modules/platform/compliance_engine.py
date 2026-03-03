from __future__ import annotations

from schemas import ComplianceOutput


def evaluate_compliance(
    *,
    jurisdiction: str,
    pii_detected: bool,
    healthcare_content_detected: bool,
    policy_coverage: float,
    threat_model_coverage: float,
    intervention_readiness: float,
) -> ComplianceOutput:
    """Phase 1 compliance scoring stub for wiring to the orchestrator."""
    gdpr_exposure = 0.75 if pii_detected and jurisdiction.upper() in {"EU", "EEA"} else 0.2
    hipaa_risk = "high" if healthcare_content_detected else "low"

    govern = max(0.0, min(1.0, policy_coverage))
    map_score = max(0.0, min(1.0, threat_model_coverage))
    measure = max(0.0, min(1.0, 0.4 * (1.0 - gdpr_exposure) + 0.6 * govern))
    manage = max(0.0, min(1.0, intervention_readiness))

    nist = max(0.0, min(1.0, (govern + map_score + measure + manage) / 4.0))
    iso_readiness = max(0.0, min(1.0, (govern + manage) / 2.0))
    gaps = []
    if manage < 0.7:
        gaps.append("incident_response_procedure")
    if map_score < 0.7:
        gaps.append("third_party_audit_trail")

    return ComplianceOutput(
        jurisdiction=jurisdiction,
        gdpr_exposure=gdpr_exposure,
        regulatory_classification="sensitive_processing" if gdpr_exposure > 0.6 else "standard_processing",
        hipaa_risk=hipaa_risk,
        nist_ai_rmf_alignment=nist,
        nist_pillar_breakdown={
            "govern": govern,
            "map": map_score,
            "measure": measure,
            "manage": manage,
        },
        iso_42001_readiness=iso_readiness,
        iso_gaps=gaps,
    )
