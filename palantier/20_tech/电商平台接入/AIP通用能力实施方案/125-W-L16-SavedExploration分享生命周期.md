# 125 · W-L16 SavedExploration 分享生命周期

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L16** · 上游 W4-06 ADR 31  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l16-saved-exploration/`  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 落地

| 能力 | 位置 |
|---|---|
| ShareGrant 表 | `o1ux2_002_exploration_share_grant.py` |
| Grant API | `ontology_exploration_share.py` + `oe_enhancements` router |
| 旧引擎禁用 | `ExplorationEngine` / `get_exploration_engine` → `LEGACY_EXPLORATION_ENGINE_DISABLED` |

## 2. 验收

- [x] create / resolve / revoke + expiry fail-closed  
- [x] 旧内存引擎生产禁用  
- [x] aip8 share/unshare 回归通过  

## 3. 验证

`pytest test_w_l16 + legacy disabled + test_aip8_saved_exploration` → **14 passed**
