# 115 · W-L3 AgentRun / Handoff 可消费 HTTP 面

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L3** · 验收：Canonical `issue → get → consume` HTTP 可跑；无第二真源  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l3-handoff-consume/`

## 1. 目标（已落地）

1. `POST/GET /v1/aip/handoffs` + `POST .../consume`
2. `POST/GET /v1/aip/agent-runs`（create/get；execute 仍独立）
3. HTTP 测：幂等 issue 二次无 bearer、consume 一次性、跨租户 get 404
4. **未改 w2**；w2 SDK 消费仍外部等待

## 2. 落地文件

- `routers/aip_handoffs.py`（新）
- `routers/aip_agent_runs.py`（create/get）
- `domain_aggregates.py` / `domain_manifest.json`
- `aip_agent_registry_contracts.py`（`ConsumeHandoffRequest` / `AgentRunCommandResponse`）
- `tests/aip/test_aip_handoff_api.py` + `test_aip_agent_run_api.py`

## 3. 不做（仍成立）

- W-L12 HandoffDecision、画布 handoff≠Envelope、w2 SDK
