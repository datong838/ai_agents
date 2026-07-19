# 183m · 清数据 MinIO 对象物理删除

> **版本**：v1.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · **已编码**（M1-W1c）  
> **分支**：`m1` · [180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[166](166-TWA11-组织工作区删除与清数据方案.md) · [165](165-本机平台依赖自动拉起方案.md)  
> **消化**：179 ③ **166 MinIO 物理删**  
> **实现**：`object_store.delete_prefix` · `tenant_data.clear` 尾声 · `AOS_CLEAR_DELETE_OBJECTS`（默认 1）· `tests/test_twa_clear_objects_183m.py`

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小 | 挂在既有 clear workspace/org API 之后；不改「非空禁删」语义 |
| 诚实 | 仅删 **约定前缀**；失败计入报告，不假装全成功 |
| 不破坏 | 元数据/业务行清理逻辑保持；本刀补对象层 |

## 1. 已决

| 项 | 值 |
| --- | --- |
| 触发 | `POST …/clear`（工作区/组织）成功路径尾声 |
| 范围 | bucket=`AOS_S3_BUCKET`；前缀建议 `orgs/{orgId}/projects/{projectId}/`（与现写入约定对齐，编码前核对真前缀） |
| 动作 | list + delete objects（SDK）；返回 `{ deleted, failed, prefix }` |
| 开关 | `AOS_CLEAR_DELETE_OBJECTS=1` 默认 Dev 开；生产显式开 |
| 回收站 | **不做**（仍 166 非目标） |

## 2. 非目标

- 软删/回收站  
- 跨 bucket 扫描  
- 改 Win 脚本  

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `tenant_data.py` / clear 路径 | 调对象删除 |
| 单测 | mock MinIO client |
| 166 / 179 | 回写 |

## 4. 自检

- [ ] clear 后前缀下对象数下降  
- [ ] 开关关闭时行为与 166 一致（只清元数据）  
- [ ] 失败项出现在响应/日志  

---

*v1.0 · 183m · M1-W1c*
