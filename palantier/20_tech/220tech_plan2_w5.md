# 220plan2 W5 — 企业级增强（123 项）

> 分支：feature/220plan2  
> 前置：W3 ✅ (23项) → W4 ✅ (123项)  
> 模式：Engine(Pydantic Model + Singleton + threading.Lock) + Router(FastAPI APIRouter) + Test(pytest 9用例/模块)  
> 前端：W5 后端 API 完成，前端路由注册到 nav.ts (status="s2")，对齐 foundry/html 蓝图

## W5 模块分布（25 模块 · 123 项）

| 模块 | 前缀 | 项数 |
|------|------|------|
| 数据集成与流式同步 | DI | 8 |
| 数据质量与健康 | DH | 2 |
| 数据血缘 | DL | 4 |
| Dataset Preview | DS | 11 |
| 管道编排 | PP | 16 |
| Pipeline Builder | PB | 1 |
| 代码仓库 | CR | 10 |
| 多语言 Transform | MT | 1 |
| MediaSet | MS | 7 |
| Object Explorer | OE | 8 |
| Ontology 核心 | OC | 7 |
| Object 数据层 | OB | 11 |
| Ontology Interfaces | IF | 1 |
| Action / Function | AF | 1 |
| Action Types | AT | 9 |
| Capability Adapter | CA | 2 |
| 调度 | SC | 4 |
| 空间数据与时间序列 | GS | 1 |
| Rules / Linter | RL | 3 |
| Workshop | WK | 2 |
| 变量系统 | VS | 3 |
| 企业系统集成 | ES | 1 |
| COP 态势 | CP | 1 |
| 授权 | AU | 1 |
| IDE 开发 | ID | 8 |

## 逐项文件清单（123 模块 × 3 文件 = 369 文件）

### [DI] 8 项
1. `di_stream_alert` — 流监控告警
2. `di_monitor_rule` — 监控规则管理
3. `di_notif_sub` — 通知订阅
4. `di_checkpoint_ft` — 检查点容错
5. `di_backing_ds` — 选择 backing datasets
6. `di_live_log` — 实时日志
7. `di_schema_config` — Schema 配置
8. `di_detail_subpanel` — 详情子面板

### [DH] 2 项
1. `dh_health_summary` — 项目健康检查摘要
2. `dh_troubleshoot_guide` — 故障排除指南

### [DL] 4 项
1. `dl_ontology_browse` — Ontology 实体浏览
2. `dl_history_detail` — 历史详情
3. `dl_save_open_chart` — 保存/打开图表
4. `dl_share_link` — 快速分享链接

### [DS] 11 项
1. `ds_schedule_panel` — 计划面板
2. `ds_share_move_rename` — 共享/移动/重命名
3. `ds_stream_preview` — 流数据预览
4. `ds_stream_tag` — 流标签
5. `ds_schema_infer` — 模式推断验证
6. `ds_edit_schema_view` — 编辑模式视图
7. `ds_col_autocomplete` — 列名自动补全
8. `ds_keyboard_shortcut` — 键盘快捷键
9. `ds_resize_panel` — 可调整列宽/面板大小
10. `ds_same_name_logic` — 同名更新/不同名追加
11. `ds_sql_draft` — SQL 草稿

### [PP] 16 项
1. `pp_incremental_perf` — 增量性能维护
2. `pp_schema_infer` — Schema 推断
3. `pp_advanced_schedule` — 高级调度选项
4. `pp_schedule_troubleshoot` — 调度故障排查
5. `pp_schedule_best_practice` — 调度最佳实践
6. `pp_schedule_template` — 常见调度模板
7. `pp_classify_tag` — 分类标记（PII/PHI）
8. `pp_propagate_view` — 传播视图要求
9. `pp_org_tag` — 组织标记
10. `pp_tag_reapproval` — 标记再审批要求
11. `pp_io_classify` — 输入输出分类
12. `pp_schedule_coloring` — 调度配置着色
13. `pp_folder_convention` — 文件夹规范
14. `pp_dev_best_practice` — 开发最佳实践
15. `pp_prod_pipeline_build` — 生产管道构建
16. `pp_connect_stream` — 连接流

### [PB] 1 项
1. `pb_breaking_change_detect` — 重大更改检测

### [CR] 10 项
1. `cr_model_dev_repo` — 模型开发仓库
2. `cr_doc_assist` — 文档辅助
3. `cr_pr_review` — PR 审查
4. `cr_code_review_req` — 代码审核要求
5. `cr_dataset_alias` — 数据集别名
6. `cr_multi_artifact` — 多类型制品支持
7. `cr_artifact_credential` — 制品发布凭证
8. `cr_artifact_registry` — 制品库集成
9. `cr_ai_error_enhance` — AI 错误增强器
10. `cr_aip_template_recommend` — AIP 代码模板推荐

### [MT] 1 项
1. `mt_code_reuse` — 变换代码复用

### [MS] 7 项
1. `ms_small_file_shortcut` — 小文件短路
2. `ms_docintel_dlq` — DocIntel 死信队列
3. `ms_latency_policy` — 延迟策略
4. `ms_transcript_postproc` — 转录文本后续处理
5. `ms_transcript_output` — 转录输出选项
6. `ms_audio_import_path` — 音频文件导入路径
7. `ms_primary_key` — 主键设置

### [OE] 8 项
1. `oe_pivot_linked` — 透视到链接对象
2. `oe_compare_objects` — 比较对象集
3. `oe_metadata_state` — 元数据状态体系
4. `oe_render_hint` — 渲染提示
5. `oe_gotham_integration` — Gotham 集成
6. `oe_linked_view` — 链接 Object 视图
7. `oe_version_mgmt` — 版本管理
8. `oe_comment_system` — 评论系统

### [OC] 7 项
1. `oc_model_aiml` — 模型 AI/ML 集成
2. `oc_audit_edit_dialog` — 审核编辑对话框
3. `oc_task_model` — 任务模型
4. `oc_review_view` — 审查视图
5. `oc_compute_attribution` — 计算归因
6. `oc_cross_ontology_migrate` — 跨 Ontology 迁移
7. `oc_ontology_switcher` — Ontology 切换器

### [OB] 11 项
1. `ob_billion_throughput` — 数十亿级吞吐量
2. `ob_osv1_osv2` — OSv1→OSv2 迁移框架
3. `ob_batch_reindex` — 批量全量重索引
4. `ob_index_monitor` — 索引监控视图
5. `ob_object_monitor` — 对象监视器
6. `ob_realtime_eval` — 实时评估
7. `ob_monitor_to_action` — 监视器→自动操作
8. `ob_monitor_activity` — 监视器活动历史
9. `ob_granular_policy` — 细粒度三层策略
10. `ob_edit_history` — 编辑历史保留
11. `ob_inline_edit` — 内联编辑

### [IF] 1 项
1. `if_interface_metadata` — 接口元数据

### [AF] 1 项
1. `af_archetypes_toggle` — Archetypes 切换

### [AT] 9 项
1. `at_param_desc` — 参数描述/帮助
2. `at_value_source` — 值来源选择
3. `at_rule_order_conflict` — 规则顺序冲突检测
4. `at_oma_7tab` — OMA Action 编辑器 7 Tab
5. `at_archetypes_toggle` — Archetypes 切换
6. `at_edit_count_warn` — 编辑计数 + 警告
7. `at_edited_marker` — Edited 字段标记
8. `at_func_op_types` — 函数支持的操作类型
9. `at_func_onboarding` — 函数操作入门向导

### [CA] 2 项
1. `ca_platform_facade` — 平台 Facade
2. `ca_heavy_capability` — 重能力接入页

### [SC] 4 项
1. `sc_logic_change_trigger` — 逻辑变更触发
2. `sc_calendar_view` — 日程安排日历
3. `sc_readonly_dynamic` — 只读/动态双模式
4. `sc_dynamic_drag_drop` — 动态模式拖放

### [GS] 1 项
1. `gs_ontology_geo` — Ontology 地理集成

### [RL] 3 项
1. `rl_rule_workflow` — 规则工作流
2. `rl_transform_pipeline_rule` — 变换管道规则
3. `rl_workshop_integration` — Workshop 应用集成

### [WK] 2 项
1. `wk_overlay` — Overlay
2. `wk_object_table_advanced` — Object Table 进阶

### [VS] 3 项
1. `vs_module_interface` — Module interface
2. `vs_events` — Events
3. `vs_event_idempotent` — 事件幂等

### [ES] 1 项
1. `es_auto_ontology_gen` — 自动 Ontology 生成

### [CP] 1 项
1. `cp_multi_spoke_monitor` — 多 Spoke 监控

### [AU] 1 项
1. `au_policy_hot_reload` — 策略热更新

### [ID] 8 项
1. `id_shell_terminal` — Shell 终端
2. `id_key_binding` — 键绑定自定义
3. `id_vsix_install` — VSIX 扩展安装
4. `id_command_palette` — 命令面板集成
5. `id_python_snippet` — Python Transform 代码片段
6. `id_refresh_token` — Refresh Token
7. `id_install_python_env` — Install Python Environment
8. `id_public_extension` — 公共扩展支持

## 编码模式（与 W3/W4 一致）

```
引擎: aos_api/{prefix}_{name}.py
  - Pydantic Model (dataclass)
  - Engine class (Singleton + threading.Lock)
  - CRUD: register/create + get + list + update + delete
  - 业务方法 (1-2 个特定方法)

路由: aos_api/{prefix}_{name}_router.py
  - APIRouter(prefix="/api/{prefix}/{name}")
  - GET / → list
  - GET /{id} → get
  - POST / → create
  - PUT /{id} → update
  - DELETE /{id} → delete

测试: tests/test_{prefix}_{name}.py
  - @pytest.fixture (setup/teardown)
  - 9 用例: create + get + get_not_found + list + update + update_not_found + delete + capacity_limit + singleton
```

## 前端注意事项

W5 主要在后端 API 层。前端路由注册到 `nav.ts`（status="s2"），App.tsx 的 BlueprintStubPage 会自动加载 foundry/html 对应蓝图。
W5 不新增前端页面，因为前端已通过 `S2_STUB_ROUTES` 自动渲染所有 s2 状态路由。
