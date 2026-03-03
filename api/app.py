from __future__ import annotations

from fastapi import FastAPI

from orchestrator import evaluate
from schemas import TrustOrchestratorInput

from .models import EvaluateResponse

app = FastAPI(title="SentinelX API", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/evaluate", response_model=EvaluateResponse)
def post_evaluate(payload: TrustOrchestratorInput) -> EvaluateResponse:
    verdict = evaluate(payload)
    return EvaluateResponse(
        request_id=payload.request_id,
        overall_trust_score=verdict.overall_trust_score,
        contextual_profile=verdict.contextual_profile,
        causal_chains_triggered=verdict.causal_chains_triggered,
        intervention=verdict.intervention,
    )
