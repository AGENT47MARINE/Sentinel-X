from __future__ import annotations

from datetime import datetime, timezone

from schemas import ShadowAIOutput


def evaluate_shadow_ai(
    *,
    instances_detected: int,
    high_risk_instances: int,
    categories: list[str],
    unsanctioned_providers: list[str],
) -> ShadowAIOutput:
    """Phase 1 metadata-based shadow AI risk summary stub."""
    if high_risk_instances >= 5:
        action = "block"
    elif high_risk_instances >= 2:
        action = "immediate_review"
    elif instances_detected > 0:
        action = "review"
    else:
        action = "monitor"

    return ShadowAIOutput(
        shadow_ai_instances_detected=max(0, instances_detected),
        high_risk_instances=max(0, high_risk_instances),
        data_categories_exposed=categories,
        top_unsanctioned_providers=unsanctioned_providers,
        recommended_action=action,
        inventory_last_updated=datetime.now(timezone.utc),
    )
