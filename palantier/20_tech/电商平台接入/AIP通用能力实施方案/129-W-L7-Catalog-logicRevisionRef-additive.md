# 129 · W-L7 Catalog logicRevisionRef additive 传输锁

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` **W-L7** · 上游工作台 ADR `109`  
> 证据：既有 `test_aip_catalog_skill_logic_revision_ref_contract.py` + 本波对账  
> 边界：additive only；不冒充 Binding/授权/AgentRun

## 结论

AIP Catalog / Skill JSON **已**始终携带 `logicRevisionRef` 键（可为 null）；与 w2 `c827928` parser additive 兼容。本波不新增旁路授权语义。

## 验收

- [x] Skill dump 含 `logicRevisionRef`（null 亦保留键）  
- [x] 禁止 `exclude_none` 丢掉该键（负向锁测已在契约测试）  
- [x] 不宣称八菜单导航 / 浏览器矩阵 GREEN（属 w2 B4/B5/B7）
