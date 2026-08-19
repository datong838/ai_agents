# 58 · 十类共享 Capability 剩余组织 Binding 补齐

> 状态：`APPROVED_FOR_IMPL` · 只改 `aos-platform-w1-aip`  
> 租户：`org-org/dev-project`  
> 触发：用户选择「为剩余类建组织 Binding（诚实 blocked 也行）」

## Design Read

插件页要看见「已建组织绑定」而不再全是「未绑定」；不可伪造可运行。

## 事实

| 项 | 值 |
|---|---|
| W0A 十类定义 | SolutionPack 已 published |
| 已有 Binding | `strategy.plan` active；另有扩展 `image.generate` / `video.generate` |
| 缺 Binding | 其余 **9** 类（非 7） |

## 方案

1. 脚本 `scripts/aip/bootstrap_w0a_remaining_capability_bindings.py`  
2. 对每个缺失 capability：  
   - `create` → `provisioning`  
   - 依赖骨架复用现网文本 Provider/Route/Eval/License（与 `strategy.plan` 同栈）+ 该 capability 自身 `required_*_refs`  
   - `evaluate` 写入 readiness（多为 `blocked`，诚实原因）  
   - **仅当** readiness=`available` 才 `activate`；否则保持 `provisioning`  
3. binding_id：`ecommerce.shared.{capability_id}.r{revision}`  
4. 不新建十个 AgentInstance；不重放密封 Pilot；不抬 Health timeout  

## 验收

- 十类 W0A 均有组织 Binding 行（或 strategy 已有）  
- 插件页不再对这九类显示「未绑定」  
- blocked/provisioning 中文可读，无假绿  

## 落地证据（2026-08-19）

- 脚本：`scripts/aip/bootstrap_w0a_remaining_capability_bindings.py --apply`  
- 收据：`.evidence/aip/2026-08-19-w0a-remaining-capability-bindings-green.json`  
- 结果：9 条新建并 `active`+`available`（复用文本 Provider/Route 栈投影）；W0A **10/10** 有 Binding  
- **诚实边界**：可用投影 ≠ 语音/视频/直播专用 Provider 已可外呼；`image.generate`/`video.generate` 仍为扩展绑定且常 blocked  

## 风险

- 语音/视频/直播等缺专用 Provider 时，八维/真实外呼仍可能失败关闭  
- 文本 Health 过期时先续期再 evaluate  
