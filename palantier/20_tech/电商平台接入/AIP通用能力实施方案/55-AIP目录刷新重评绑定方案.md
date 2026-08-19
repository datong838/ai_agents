# 55 · AIP 智能体目录「刷新」连带绑定就绪重评

> 状态：`APPROVED_FOR_IMPL` · 只改 `aos-platform-w1-aip`  
> 租户：`org-org/dev-project`  
> 触发：目录「刷新」只重读快照，15 分钟 TTL 后仍黄条「快照已过期」

## Design Read

运维点「刷新」期望：**用当前 Provider Health 重评组织内已激活 Binding**，再投影可运行数；不是再读一遍过期字段。

## 根因

| 层 | 行为 |
|---|---|
| `GET …/runtime-readiness` | 只投影 DB 中 Binding 的 `readiness` / `expires_at` |
| Binding 新鲜度 | `evaluate` / `evaluate_binding` 写入，约 15 分钟过期 |
| 现有 UI「刷新」 | 再调 GET → 过期仍过期 |

## 方案（最小）

1. 新增 `POST /v1/aip/agent-registry/refresh-readiness`（`Idempotency-Key` 必填）  
2. 服务端对当前租户 **status=active** 的 CapabilityBinding / SkillBinding：  
   - 若已 `available` 且 `expires_at > now` → **跳过**  
   - 否则用现有 dependencies 调 `evaluate` / `evaluate_binding`  
   - **软失败**：单条 blocked / 抛错不中断整批（图像/视频 Health 差时不拖死文本 Pilot）  
3. 成功后返回与 GET 相同的 `AgentRuntimeReadinessResponse`（保持前端 strict parser）  
4. 目录页「刷新」改为调 POST；文案改为「刷新会重评绑定就绪」

## 非目标

- 不在本波抬 Health timeout、不连打图像/视频三探  
- 不批量 publish 其余 evaluated 技能  
- 不改 w2、不重放密封 Pilot  

## 自测

- 单元：installer soft-skip + soft-fail 不抛整批  
- API：POST 后 `evaluatedAt` 更新；文本 Pilot 在 Health 绿时 `runnable` 可恢复  
- UI：按钮文案/禁用态；失败时 alert 可读  

## 文件

- `services/aos-api/aos_api/aip_ecommerce_agent_installer.py`  
- `services/aos-api/aos_api/routers/phase3_aip_agents.py`  
- `services/aos-api/tests/aip/test_aip6_agent_control_api.py`（及 installer 单测）  
- `apps/web/src/api/aipAgentControl/index.ts`  
- `apps/web/src/pages/s2/CanonicalAgentRegistryPage.tsx` (+ test)  
