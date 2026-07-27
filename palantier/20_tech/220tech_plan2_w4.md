# 220tech plan2 — W4 高价值功能（123 项）

> **分支**：feature/220plan2
> **工作目录**：aos-platform-220plan2/
> **波次**：W4 / P1 高价值功能
> **原则**：先方案再编码 → TDD → 每模块必有单元测试 → 波次完成回归测试

---

## 代码库现有模式（严格遵循，与 W3 一致）

```
services/aos-api/aos_api/
  ├── <module>.py              ← 引擎层：Pydantic Model + Engine 单例 + threading.Lock
  ├── routers/<module>.py      ← 路由层：FastAPI APIRouter
  └── (W3 中路由直接放 aos_api/ 根目录，W4 保持一致)

services/aos-api/tests/
  └── test_<module>.py         ← 测试层：pytest class + setup_method
```

**引擎层模式**：
- `Pydantic BaseModel` 做数据模型
- `Engine` 类用 `_instance` + `_instance_lock` 做线程安全单例
- ID 生成：`f"{prefix}-{uuid.uuid4().hex[:8]}"`
- 容量限制：`_MAX = 200`，超限 LRU 淘汰
- 自定义 `Error(Exception)` 带 `code` + `message`

**路由层模式**：
- `APIRouter(prefix="/api/...", tags=[...])`
- 每个 CRUD 操作一个端点
- 引擎通过 `get_engine()` 获取

**测试层模式**：
- `class TestXxx: def setup_method(self)` → `self.eng._items = {}`
- 测试覆盖：register / get / get_not_found / list / update / update_not_found / delete / capacity_limit / singleton

---

## W4 任务分解（123 项 × 17 模块）

### 模块 1: [DC] 数据连接与集成（8 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L102 | dc_agent_yaml | Agent 高级 YAML 配置 |
| 2 | L183 | dc_stream_preview | Stream 预览 |
| 3 | L208 | dc_export_tasks | Export Tasks（旧版） |
| 4 | L236 | dc_webhook_source | Webhook ↔ Source 关联 |
| 5 | L239 | dc_curl_import | cURL 导入 |
| 6 | L245 | dc_test_connection | 测试连接 + 自动建议 |
| 7 | L292 | dc_sync_troubleshoot | Sync 故障排除指南 |
| 8 | L3196 | dc_app_state | Application State |

### 模块 2: [DI] 数据集成与流式同步（33 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L692 | di_dataset_branch | Dataset Branch 协作 |
| 2 | L695 | di_key_by | Key by（主键/排序列） |
| 3 | L722 | di_hot_cold_storage | 热缓冲区 + 冷存储 |
| 4 | L723 | di_live_archive | Live vs Archive 双视图 |
| 5 | L724 | di_stream_schema | Stream Schema 定义 |
| 6 | L726 | di_partition_control | 分区控制 |
| 7 | L727 | di_compression_toggle | 数据压缩开关 |
| 8 | L728 | di_latency_sampling | 延迟跟踪采样率 |
| 9 | L729 | di_reset_stream | Reset Stream |
| 10 | L734 | di_consistency_guarantee | 一致性保证 |
| 11 | L761 | di_text_extraction | Text Extraction Transform |
| 12 | L763 | di_virtual_storage | 虚拟存储 |
| 13 | L764 | di_streaming_latency | 流式延迟模式 |
| 14 | L784 | di_view_creation | View 创建入口 |
| 15 | L786 | di_primary_key_config | 主键配置 |
| 16 | L787 | di_auto_dedup | 自动去重 |
| 17 | L810 | di_auto_register | 自动注册开关 |
| 18 | L811 | di_db_schema_table | Database/Schema/Table 配置 |
| 19 | L812 | di_output_path | 输出路径配置 |
| 20 | L813 | di_virtual_table | 虚拟表项目 |
| 21 | L814 | di_permission_roles | 权限角色（Tables Viewer/Owner） |
| 22 | L834 | di_external_access | 外部系统访问开关 |
| 23 | L835 | di_transforms_external | transforms-external-systems 库 |
| 24 | L838 | di_export_config | Export configuration |
| 25 | L839 | di_source_based_transform | 基于源的外部变换 |
| 26 | L865 | di_freshness_detect | Freshness 检测 |
| 27 | L866 | di_force_build | Force Build |
| 28 | L870 | di_data_consistency | 数据一致性保证 |
| 29 | L892 | di_logic_change_trigger | 逻辑变更触发 |
| 30 | L930 | di_s3_api | S3 API 协议暴露 |
| 31 | L931 | di_third_party_access | 第三方客户端访问 |
| 32 | L2047 | di_external_transforms | External Transforms |
| 33 | L2075 | di_spark_engine | Spark 计算引擎 |

### 模块 3: [DL] 数据血缘（15 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L506 | dl_node_indicators | 4 种节点指示器 |
| 2 | L508 | dl_chart_tools | 图表工具（设计/展开/查找/选择） |
| 3 | L509 | dl_branch_aware | 分支感知 |
| 4 | L510 | dl_flow_animation | 数据沿袭流动动画 |
| 5 | L530 | dl_property_histogram | 属性和直方图面板 |
| 6 | L531 | dl_related_artifacts | 相关工件面板 |
| 7 | L548 | dl_permission_coloring | 权限着色（用户切换） |
| 8 | L549 | dl_stale_coloring | 过时着色（数据/逻辑） |
| 9 | L568 | dl_dataset_preview_300 | 数据集预览（300 行） |
| 10 | L593 | dl_plan_management | 计划管理（从沿袭） |
| 11 | L614 | dl_svg_export | SVG 导出 |
| 12 | L615 | dl_share_permission | 分享权限管理 |
| 13 | L634 | dl_user_permission_view | 以用户视角查看权限 |
| 14 | L635 | dl_permission_simulation | 权限标记模拟 |
| 15 | L653 | dl_faq_troubleshoot | FAQ 式问题排查 |

### 模块 4: [DS] Dataset Preview（2 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L1583 | ds_backtick_search | 反引号数据集搜索 |
| 2 | L1595 | ds_inline_upload | 数据集页面内直接上传 |

### 模块 5: [PP] 管道编排（7 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L1007 | pp_toolbar_share | 顶部工具栏 - 分享 |
| 2 | L1009 | pp_chart_pan | 图表 - 平移模式 |
| 3 | L1010 | pp_chart_drag_select | 图表 - 拖动选择 |
| 4 | L1037 | pp_parse_paths | 四类解析路径 |
| 5 | L1123 | pp_mediasets_code | MediaSets 代码处理 |
| 6 | L1133 | pp_cross_project_flow | 跨项目数据流 |
| 7 | L1141 | pp_role_permission | 角色权限 |

### 模块 6: [PB] Pipeline Builder（20 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L1176 | pb_view_switch | 三种视图切换 |
| 2 | L1178 | pb_detail_sidebar | 详细信息侧栏 |
| 3 | L1182 | pb_history_records | 历史记录 |
| 4 | L1183 | pb_add_data_modes | 四种添加数据方式 |
| 5 | L1184 | pb_virtual_data_gen | 虚拟数据生成 |
| 6 | L1196 | pb_fp_growth | 频繁模式挖掘（FP-Growth） |
| 7 | L1200 | pb_structured_semi | 结构化 vs 半结构化变换 |
| 8 | L1201 | pb_snapshot_incremental | 快照 vs 增量计算模式 |
| 9 | L1215 | pb_override_dataset | 覆盖数据集配置 |
| 10 | L1228 | pb_branch_activity | 分支活动管理 |
| 11 | L1238 | pb_color_groups | 颜色组 |
| 12 | L1243 | pb_param_system | 参数系统 |
| 13 | L1244 | pb_show_hide_nodes | 显示/隐藏节点 |
| 14 | L1266 | pb_unit_test | 单元测试 |
| 15 | L1289 | pb_export_java | 导出 Java 代码 |
| 16 | L1290 | pb_marketplace_pkg | Marketplace 打包 |
| 17 | L3338 | pb_ai_functions | AI 函数（useLlmV2/OCR/嵌入） |
| 18 | L3340 | pb_transform_library | 变换函数库 |
| 19 | L3723 | pb_branch_version | 分支版本 |
| 20 | L3725 | pb_data_expectations | 数据期望 |

### 模块 7: [CR] 代码仓库（4 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L1807 | cr_default_branch | 默认分支配置 |
| 2 | L1810 | cr_fallback_branch | 回退分支配置 |
| 3 | L1823 | cr_impact_analysis | 影响分析 |
| 4 | L1825 | cr_build_affected | 构建受影响数据集 |

### 模块 8: [BD] Build 引擎（3 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L1350 | bd_freshness | Freshness 检测 |
| 2 | L1351 | bd_force_build | Force Build |
| 3 | L1353 | bd_dep_task_abort | 依赖 Task 事务 ABORT |

### 模块 9: [FN] Funnel 映射（1 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L2805 | fn_pipeline_status | Funnel Pipeline 状态页 |

### 模块 10: [MS] MediaSet（2 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L1667 | ms_file_add | 文件添加 |
| 2 | L1735 | ms_create_pipeline_menu | 创建新流水线上下文菜单 |

### 模块 11: [OE] Object Explorer（3 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L2700 | oe_column_config | 结果表格列排序/配置/冻结/行内编辑 |
| 2 | L2706 | oe_admin_config | Object Explorer 管理员配置 |
| 3 | L2760 | oe_app_sidebar | 应用侧边栏 |

### 模块 12: [OC] Ontology 核心（6 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L2356 | oc_global_search | 全局搜索（Cmd+K） |
| 2 | L2357 | oc_sidebar_filter | 侧边栏筛选 |
| 3 | L2381 | oc_destructive_confirm | 破坏性更改确认 |
| 4 | L2411 | oc_permission_migration | 权限迁移工具 |
| 5 | L2438 | oc_org_level_toggle | 组织级开关 |
| 6 | L2485 | oc_metric_toggle | 指标启用开关 |

### 模块 13: [OB] Object 数据层（3 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L2538 | ob_agg_precision | 聚合精度控制 |
| 2 | L2617 | ob_monitor_notify | 监视器通知 |
| 3 | L2642 | ob_stream_permission | 流数据源权限 |

### 模块 14: [AF] Action / Function（6 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L2868 | af_oma_editor | OMA Action 编辑器 |
| 2 | L2873 | af_action_types | 6 种 Action 类型 |
| 3 | L2878 | af_edit_counter | 编辑计数 + 警告 |
| 4 | L2883 | af_capabilities | Capabilities 能力 |
| 5 | L2891 | af_edited_marker | Edited 字段标记 |
| 6 | L2894 | af_param_help | 参数描述/帮助 |

### 模块 15: [AT] Action Types（6 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L2956 | at_notification_link | 通知链接配置 |
| 2 | L2962 | at_notification_permission | 通知权限检查 |
| 3 | L2995 | at_action_apply_perm | 操作应用权限 |
| 4 | L2996 | at_edit_only_mode | 仅操作编辑模式 |
| 5 | L2997 | at_side_effect_perm | 副作用权限 |
| 6 | L3001 | at_marketplace_types | Marketplace Action Types |

### 模块 16: [WK] Workshop（2 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L3384 | wk_conditional_section | Conditional Section |
| 2 | L3385 | wk_widget_permission | Widget 级权限 |

### 模块 17: [ID] IDE 开发（2 项）

| # | 220w | 文件前缀 | 功能 |
|---|------|---------|------|
| 1 | L3624 | id_osdk_react | OSDK React 应用开发 |
| 2 | L3628 | id_feature_matrix | IDE 功能对比矩阵 |

---

## 交付清单

| 类别 | 数量 |
|------|------|
| 引擎文件 | 123 |
| 路由文件 | 123 |
| 测试文件 | 123 |
| main.py 更新 | 1（123 个 import + include_router） |
| **合计新增文件** | **369** |

## 回归测试

```bash
cd services/aos-api
.venv/bin/python -m pytest tests/ --ignore=tests/test_external_jwks.py --ignore=tests/test_jwks_failover.py -q
```
