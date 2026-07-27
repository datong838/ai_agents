# 222 Phase B 技术方案 · 模型路由编辑器

> **版本**：v1.0 · 2026-07-25
> **关联**：[222plan-分阶段开发与里程碑计划.md](222plan-分阶段开发与里程碑计划.md)
> **对应章节**：222 第 24 章
> **目标**：实现模型路由编辑器的 Fallback 链可视化 + 权重滑块 + 熔断器 + 路由测试
> **状态**：✅ 已完成

---

## 一、现状审计结论

| 维度 | 现状 | 差距 |
|------|------|------|
| **后端引擎** | `llm_routing.py`(784行) 已有 SmartRouter + ScenarioRouter + FailoverEngine 三大引擎 | 引擎内存存储、重启丢失 |
| **后端 API** | `routers/llm_routing.py`(416行) 已有 22 个端点 `/v1/aip/smart-router/*` 等 | 前端完全没调用这些端点 |
| **前端实际使用** | `wave_ext.py` 的 `/v1/aip/model-routes`(GET/PUT) | 只有 primary/fallback 二选一，无权重分配 |
| **KV 存储** | `aip_kv_store.py` 持久化 RouteRule | 缺少 weights、circuit_config_v2、fallback_chain |
| **前端 ModelRouterPage** | aip.tsx L1644(385行) 已有规则表 + 保存 + 熔断演练 + 试聊 | 缺少权重滑块、全局熔断配置面板、Fallback 链可视化、路由测试 |
| **视觉稿** | aip-model-router.html(407行) 完整 UI | 权重分配条 + 熔断滑块组 + Fallback 链 SVG + 预热状态 |

**核心洞察**：后端引擎能力（智能路由+场景路由+熔断状态机）远超前端使用深度。Phase B 的本质是**让前端接入已有的 22 个 API 端点**，同时补齐 KV 层缺失的字段。

## 二、数据模型扩展

在 `aip_kv_store.py` 的 RouteRule 基础上增加字段（向后兼容）：

```python
# aip_kv_store.py 扩展字段
class RouteRuleV2:
    id: str
    task: str
    primary: str
    fallback: str
    egress: str
    span: bool
    # --- V2 新增 ---
    weights: list[dict]          # [{"model":"gpt-4o","pct":60}, {"model":"gpt-4o-mini","pct":40}]
    fallback_chain: list[str]    # ["gpt-4o", "gpt-4o-mini", "报错"]
    circuit_config: dict         # {"error_rate_threshold":10, "latency_p99_ms":3000, "cooldown_s":30, "half_open_probes":3}
    strategy: str                # "weighted" | "failover" | "lowest_latency" | "lowest_cost"
```

全局熔断配置（独立持久化）：

```python
class GlobalCircuitConfig:
    error_rate_threshold_pct: int = 10      # 5xx 错误率
    latency_p99_ms: int = 3000              # 延迟阈值
    cooldown_seconds: int = 30              # 熔断时长
    half_open_probes: int = 3               # 半开探测数
```

## 三、API 端点设计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/models/router` | 列出所有路由配置 |
| GET | `/api/models/router/{id}` | 获取单条路由配置 |
| PUT | `/api/models/router/{id}` | 更新路由配置 |
| POST | `/api/models/router/{id}/test` | 路由测试（模拟决策） |
| GET | `/api/models/router/circuit-config` | 获取全局熔断配置 |
| PUT | `/api/models/router/circuit-config` | 更新全局熔断配置 |

## 四、编码顺序（3 批）

| 批次 | 内容 | 文件 |
|------|------|------|
| **B-1** | KV 层扩展 RouteRuleV2 + 全局熔断配置 + 路由 CRUD API + 测试 | aip_kv_store.py 扩展, model_router_config.py, model_router_config_router.py, test |
| **B-2** | 路由测试 API + 融合熔断引擎 + 测试 | model_router_config.py 扩展, test |
| **B-3** | 前端 ModelRouterPage 深度增强 | aip.tsx 增强 |

## 五、CircuitBreaker 状态机

```
closed（正常） → 错误率 > 阈值 → open（熔断，拒绝请求）
  ↑                                      ↓ cooldown_s 秒后
  └── 探测成功 ← half_open（允许 N 个探测请求） ←──┘
                    ↓ 探测失败
                  open（重新熔断）
```

## 六、前端增强

**ModelRouterPanels（4 面板）**：
1. **路由规则表** — 已有，增加 weights 列显示
2. **Fallback 链可视化** — SVG 节点链 + 拖拽排序
3. **全局熔断配置** — 4 个滑块（错误率/P99延迟/冷却/探测数）
4. **路由测试** — 输入 prompt → 模拟决策 → 输出模型选择 + 延迟

## 七、验收标准

- [x] 路由配置 API 支持 CRUD
- [x] 路由测试 API 可模拟决策并返回模型选择 + 延迟
- [x] Fallback 链可拖拽排序，节点状态实时更新
- [x] 权重滑块总和始终 = 100%
- [x] 熔断器状态可视化（绿/红/黄三色）
- [x] 17 个单元测试全部 PASS
