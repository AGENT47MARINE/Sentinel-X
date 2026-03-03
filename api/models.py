from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EvaluateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    overall_trust_score: float = Field(ge=0.0, le=1.0)
    contextual_profile: str
    causal_chains_triggered: list[str]
    intervention: Literal["monitor", "throttle", "human_review", "block"]
