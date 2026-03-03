# SentinelX Schema Contract (SC-01)

This package contains the shared output and orchestration input contracts for:
- Member 1 modules (`PromptGuardOutput`, `RetrievalIntegrityOutput`, `MCPIntegrityOutput`, `OutputGroundingOutput`)
- Member 2 modules (`AgentActionOutput`, `InterAgentOutput`, `MemoryPoisoningOutput`)
- Team Lead modules (`DriftMonitorOutput`, `ComplianceOutput`, `ShadowAIOutput`)
- Trust orchestrator integration (`TrustOrchestratorInput`)

## Contract Rules
- `schema_version` is mandatory and locked to `v1` for Phase 1.
- Unknown fields are rejected (`extra = forbid`).
- Risk fields are normalized to `[0.0, 1.0]`.
- Any schema change requires review from Member 1, Member 2, and Team Lead.

## Usage
```python
from schemas import TrustOrchestratorInput

payload = TrustOrchestratorInput.model_validate(data)
```
