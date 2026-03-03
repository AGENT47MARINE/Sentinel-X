from __future__ import annotations

from schemas import DriftMonitorOutput


def evaluate_drift(
    *,
    entropy_shift: float,
    compliance_drop: float,
    reasoning_variance_score: float,
    baseline_version: str,
) -> DriftMonitorOutput:
    """Phase 1 deterministic drift stub used for integration wiring."""
    drift_score = min(
        1.0,
        max(0.0, (0.45 * entropy_shift) + (0.35 * compliance_drop) + (0.20 * reasoning_variance_score)),
    )

    if drift_score > 0.8:
        alert = "critical"
    elif drift_score > 0.65:
        alert = "high"
    elif drift_score > 0.4:
        alert = "medium"
    else:
        alert = "low"

    variance = "high" if reasoning_variance_score > 0.8 else "elevated" if reasoning_variance_score > 0.4 else "stable"
    signals: list[str] = []
    if entropy_shift > 0.4:
        signals.append("entropy_increase")
    if compliance_drop > 0.2:
        signals.append("compliance_drop")
    if reasoning_variance_score > 0.4:
        signals.append("reasoning_variance")

    return DriftMonitorOutput(
        model_drift_score=drift_score,
        compliance_drop=max(0.0, min(1.0, compliance_drop)),
        reasoning_variance=variance,
        drift_alert_level=alert,
        top_drift_signals=signals,
        baseline_version=baseline_version,
    )
