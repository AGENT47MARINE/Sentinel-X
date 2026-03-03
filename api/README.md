# API
Owner: Team Lead

## Phase 1 skeleton
- `GET /healthz`
- `POST /evaluate` accepts `TrustOrchestratorInput` and returns trust verdict fields.

Run locally:
```bash
uvicorn api.app:app --reload
```
