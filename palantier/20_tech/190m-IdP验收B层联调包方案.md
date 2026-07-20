# 190m · IdP 验收 B 层联调包（不代签收）

> **版本**：v1.2 · 2026-07-20  
> **状态**：✅ **已编码**（M1-W4a）· 自测通过  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[161](161-客户生产IdP验收规程-微商城案例.md) · [60](60-生产IdP联调手册.md)  
> **边界**：**不代 C 层书面签收**  
> **落点**：`scripts/ci/accept-idp-b-layer.sh` · `tests/test_w4_190_191_192m.py`

## 分层

| 层 | 含义 | 本刀 |
| --- | --- | --- |
| A | 规程/探针/示例 env 就绪 | 161 已齐 |
| B | 样例 token → probe → `/v1/me` 绿 | **本刀** |
| C | 客户书面签收 | 停车场 |

## 已决

- 脚本：`scripts/ci/accept-idp-b-layer.sh`（包装 `accept-customer-idp.sh`，无 token 则 FAIL）
- 报告目录：`deploy/dev/_idp_accept/`（已有）
- Checklist 写在方案 §自检 + 脚本 stdout

## 自检

- [x] 无 env/token → 非 0 退出（诚实 FAIL）  
- [x] `--help` / dry 说明含「不代签收」  
- [x] 单测：脚本存在且可解析（`test_w4_190_191_192m.py`）  

---

*v1.2 · 190m · 已编码*
