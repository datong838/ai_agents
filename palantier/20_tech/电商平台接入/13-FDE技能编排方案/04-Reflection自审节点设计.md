# Reflection 自审节点设计 — 每步执行后的自检

> 创建时间：2026-07-28
> 状态：方案设计（先方案后编码）
> 关联：`00-总览-从静态文档到可编排技能链.md` §三 · `../11-AIP决策引擎升级方案/01-Plan-Mode与TAOR循环设计.md` §2.4
> 参考：Claude Code Reflection 机制（成功率 60% → 85%）

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层 |
| 最小更改 | Reflection 节点为新增模块，不修改现有 TAOR 循环骨架 |
| 不影响现有功能 | Reflection 失败不阻断流程，仅触发重试或告警 |
| 自测验证 | 每条自审规则需有对应的测试用例 |

---

## 一、设计目标

### 1.1 Reflection 的价值

参考 Claude Code 实测数据：每轮 Act 后插入自审节点，**成功率从 60% 提升到 85%**，代价是多一轮模型调用。

### 1.2 FDE 的自审场景

| 技能 | 自审目标 | 失败后果 |
|------|---------|---------|
| 技能1 对话理解 | 必填参数齐全 + 置信度足够 | 接入方向错误 |
| 技能2 认证配置 | 连通性测试通过 + credentials 格式有效 | 后续 API 调用全部失败 |
| 技能3 API 探索 | 必需 API 全部发现 + 频率合规 | 字段映射缺数据源 |
| 技能4 字段映射 | 覆盖率 ≥ 0.8 + 置信度 ≥ 0.7 | 数据污染 Ontology |
| 技能5 同步配置 | 首次同步成功 + Ontology 物化完成 | 同步链路中断 |
| 技能6 测试验证 | 数据质量 ≥ 0.7 + Schema 一致 | 接入即污染 |

### 1.3 三种自审结果

```python
class ReflectionResult(BaseModel):
    """Reflection 自审结果。"""
    passed: bool                    # 是否通过
    should_retry: bool = False      # 是否需要重试当前技能
    should_rollback: bool = False   # 是否需要回滚到上一步
    should_pause: bool = False      # 是否需要暂停等待用户
    updated_context: dict = {}      # 重试时的更新上下文
    issues: list[ReflectionIssue] = []  # 发现的问题
    recommendation: str = ""        # 建议下一步
```

| 结果 | passed | should_retry | should_rollback | should_pause |
|------|--------|--------------|-----------------|--------------|
| 通过 | True | False | False | False |
| 重试 | False | True | False | False |
| 回滚 | False | False | True | False |
| 暂停 | False | False | False | True |

---

## 二、六技能的自审规则

### 2.1 技能1：对话理解

```python
SKILL_1_REFLECTION_RULES = [
    ReflectionRule(
        name="required_params_check",
        description="所有必填参数必须齐全",
        condition="all(p in context.params for p in ['platform', 'merchant_id', 'api_credentials'])",
        on_fail=ReflectionAction(
            action="ask_user",
            message="缺失必填参数：{missing_params}",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="confidence_check",
        description="理解置信度必须 ≥ 0.8",
        condition="context.confidence >= 0.8",
        on_fail=ReflectionAction(
            action="ask_user",
            message="理解置信度不足（{confidence}），请确认：{ambiguous_fields}",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="platform_supported_check",
        description="平台必须在支持列表中",
        condition="context.platform in ['taobao', 'pinduoduo', 'jd', 'douyin', 'shopify', 'amazon', 'niushop', 'kuaishou']",
        on_fail=ReflectionAction(
            action="ask_user",
            message="不支持的平台：{platform}，请选择支持的平台",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="data_types_valid_check",
        description="数据类型必须在允许列表中",
        condition="all(dt in ['orders', 'products', 'customers', 'logistics'] for dt in context.data_types)",
        on_fail=ReflectionAction(
            action="ask_user",
            message="不支持的数据类型：{invalid_types}",
            should_pause=True
        )
    ),
]
```

### 2.2 技能2：认证配置

```python
SKILL_2_REFLECTION_RULES = [
    ReflectionRule(
        name="credential_format_check",
        description="credentials 格式必须符合平台规范",
        condition="validate_credential_format(context.platform, context.credentials)",
        on_fail=ReflectionAction(
            action="ask_user",
            message="credentials 格式错误：{format_error}",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="connectivity_test",
        description="认证后必须能成功调用平台 API",
        condition="context.connectivity_test_passed == True",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=3,
            backoff_seconds=5,
            message="认证连通性测试失败，正在重试..."
        ),
        on_fail_exhausted=ReflectionAction(
            action="rollback",
            to_checkpoint="CP1",
            message="认证失败3次，回滚到对话理解重新确认参数"
        )
    ),
    ReflectionRule(
        name="credentials_not_logged",
        description="credentials 不能出现在日志中",
        condition="not credentials_in_logs(context)",
        on_fail=ReflectionAction(
            action="alert",
            message="严重：credentials 出现在日志中！",
            severity="critical"
        )
    ),
]
```

### 2.3 技能3：API 探索

```python
SKILL_3_REFLECTION_RULES = [
    ReflectionRule(
        name="required_apis_found",
        description="所有必需 API 必须可用",
        condition="all(context.required_apis_available.values())",
        on_fail=ReflectionAction(
            action="report_missing",
            message="缺失必需 API：{missing_apis}",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="rate_limit_check",
        description="API 调用频率必须在限制内",
        condition="context.current_rate <= context.rate_limit",
        on_fail=ReflectionAction(
            action="throttle",
            message="触发平台限流，自动降低频率",
            updated_context={"rate_limit_multiplier": 0.5}
        )
    ),
    ReflectionRule(
        name="api_schema_complete",
        description="API Schema 必须包含必需字段",
        condition="validate_api_schema_completeness(context.discovered_apis)",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=2,
            message="API Schema 不完整，重新拉取..."
        )
    ),
    ReflectionRule(
        name="api_version_check",
        description="API 版本必须是最新或稳定版",
        condition="context.api_version in ['stable', 'latest']",
        on_fail=ReflectionAction(
            action="warn",
            message="API 版本可能过旧：{api_version}，建议升级"
        )
    ),
]
```

### 2.4 技能4：字段映射

```python
SKILL_4_REFLECTION_RULES = [
    ReflectionRule(
        name="coverage_check",
        description="映射覆盖率必须 ≥ 0.8",
        condition="context.coverage >= 0.8",
        on_fail=ReflectionAction(
            action="conditional",
            branches={
                "coverage < 0.5": ReflectionAction(action="rollback", to_checkpoint="CP3",
                    message="覆盖率过低，回滚重新探索 API"),
                "0.5 <= coverage < 0.8": ReflectionAction(action="pause",
                    message="覆盖率不足，请确认未映射字段是否可忽略")
            }
        )
    ),
    ReflectionRule(
        name="confidence_check",
        description="平均置信度必须 ≥ 0.7",
        condition="context.avg_confidence >= 0.7",
        on_fail=ReflectionAction(
            action="pause",
            message="映射置信度过低（{avg_confidence}），以下规则需人工确认：{low_confidence_rules}",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="no_conflicting_mappings",
        description="同一源字段不能映射到多个目标",
        condition="not has_conflicting_mappings(context.mapping_rules)",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=2,
            message="发现冲突映射，重新生成..."
        )
    ),
    ReflectionRule(
        name="transform_valid_check",
        description="类型转换规则必须有效",
        condition="validate_transforms(context.mapping_rules)",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=2,
            message="类型转换规则无效，重新生成..."
        )
    ),
    ReflectionRule(
        name="episodic_memory_match",
        description="映射方案应与历史经验一致或更优",
        condition="context.episodic_match_score >= 0.6 or context.is_new_platform",
        on_fail=ReflectionAction(
            action="warn",
            message="映射方案与历史经验差异较大，请人工审查"
        )
    ),
]
```

### 2.5 技能5：同步配置

```python
SKILL_5_REFLECTION_RULES = [
    ReflectionRule(
        name="sync_strategy_check",
        description="同步策略必须符合数据特性",
        condition="validate_sync_strategy(context.data_types, context.sync_config)",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=2,
            message="同步策略不合理，重新推荐..."
        )
    ),
    ReflectionRule(
        name="first_sync_success",
        description="首次同步必须成功",
        condition="context.first_sync_succeeded == True",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=3,
            backoff_seconds=30,
            message="首次同步失败，正在重试..."
        ),
        on_fail_exhausted=ReflectionAction(
            action="rollback",
            to_checkpoint="CP4",
            message="同步3次失败，回滚重新生成映射方案"
        )
    ),
    ReflectionRule(
        name="record_count_reasonable",
        description="同步记录数符合预期",
        condition="abs(context.actual_records - context.estimated_records) / max(context.estimated_records, 1) < 0.5",
        on_fail=ReflectionAction(
            action="warn",
            message="同步记录数与预期差异较大：预期 {estimated}，实际 {actual}"
        )
    ),
    ReflectionRule(
        name="ontology_materialized",
        description="Ontology 物化必须完成",
        condition="context.ontology_materialized == True",
        on_fail=ReflectionAction(
            action="retry",
            max_retries=2,
            message="Ontology 物化失败，重试..."
        ),
        on_fail_exhausted=ReflectionAction(
            action="rollback",
            to_checkpoint="CP4",
            message="物化失败，回滚检查映射规则"
        )
    ),
]
```

### 2.6 技能6：测试验证

```python
SKILL_6_REFLECTION_RULES = [
    ReflectionRule(
        name="data_freshness",
        description="数据必须在新鲜度阈值内",
        condition="context.data_age_hours <= 24",
        on_fail=ReflectionAction(
            action="check_sync",
            message="数据不新鲜（{data_age_hours}h），检查同步状态"
        )
    ),
    ReflectionRule(
        name="schema_match",
        description="实际 Schema 必须与映射 Schema 一致",
        condition="context.schema_consistent == True",
        on_fail=ReflectionAction(
            action="report_schema_drift",
            message="Schema 漂移：{drift_details}",
            should_pause=True
        )
    ),
    ReflectionRule(
        name="quality_check",
        description="数据质量评分必须 ≥ 0.7",
        condition="context.data_quality_score >= 0.7",
        on_fail=ReflectionAction(
            action="conditional",
            branches={
                "score < 0.5": ReflectionAction(action="rollback", to_checkpoint="CP5",
                    message="质量极差，回滚调整同步配置"),
                "0.5 <= score < 0.7": ReflectionAction(action="report",
                    message="数据质量一般，生成报告但不阻断接入")
            }
        )
    ),
    ReflectionRule(
        name="null_rate_check",
        description="关键字段 null 率必须 < 5%",
        condition="context.null_rate < 0.05",
        on_fail=ReflectionAction(
            action="report",
            message="null 率过高：{null_fields}，请检查源数据"
        )
    ),
    ReflectionRule(
        name="uniqueness_check",
        description="主键字段必须唯一",
        condition="context.duplicate_rate == 0",
        on_fail=ReflectionAction(
            action="report",
            message="主键重复：{duplicate_count} 条，请检查去重规则"
        )
    ),
]
```

---

## 三、自审执行器

### 3.1 ReflectionExecutor

```python
# aip_fde_reflection.py（新增模块）

class ReflectionExecutor:
    """Reflection 自审执行器。

    在 TAOR 循环的 Reflect 阶段被调用。
    """

    def __init__(self, llm_adapter: LLMAdapter):
        self._llm = llm_adapter
        self._rules = self._load_all_rules()

    async def reflect(self, skill_id: str, action_result: ActionResult, context: dict) -> ReflectionResult:
        """执行自审。"""
        rules = self._rules.get(skill_id, [])

        # 1. 执行所有规则
        issues = []
        for rule in rules:
            issue = await self._evaluate_rule(rule, action_result, context)
            if issue:
                issues.append(issue)

        # 2. 汇总结果
        if not issues:
            return ReflectionResult(
                passed=True,
                recommendation="所有自审规则通过，继续下一步"
            )

        # 3. 按严重性排序
        issues.sort(key=lambda i: i.severity, reverse=True)
        critical_issues = [i for i in issues if i.severity == "critical"]
        high_issues = [i for i in issues if i.severity == "high"]

        # 4. 决策
        if critical_issues:
            return ReflectionResult(
                passed=False,
                should_pause=True,
                issues=issues,
                recommendation=critical_issues[0].recommended_action
            )

        if high_issues:
            # 高严重性问题，根据规则定义决定动作
            first_high = high_issues[0]
            return ReflectionResult(
                passed=False,
                should_retry=first_high.should_retry,
                should_rollback=first_high.should_rollback,
                should_pause=first_high.should_pause,
                issues=issues,
                recommendation=first_high.recommended_action
            )

        # 低严重性问题，仅警告，不阻断
        return ReflectionResult(
            passed=True,
            issues=issues,
            recommendation="存在低严重性问题，已记录但继续执行"
        )

    async def _evaluate_rule(
        self, rule: ReflectionRule, action_result: ActionResult, context: dict
    ) -> ReflectionIssue | None:
        """评估单条规则。"""
        try:
            # 简单条件用 Python eval
            if rule.condition_type == "python":
                passed = eval(rule.condition, {"context": SimpleNamespace(**context), "action_result": action_result})
            # 复杂条件用 LLM 判断
            elif rule.condition_type == "llm":
                passed = await self._llm_evaluate(rule, action_result, context)
            else:
                passed = True  # 默认通过

            if not passed:
                return ReflectionIssue(
                    rule_name=rule.name,
                    severity=rule.severity,
                    message=rule.message_template.format(**context),
                    recommended_action=rule.on_fail.action
                )
        except Exception as e:
            # 自审本身失败不阻断流程
            return ReflectionIssue(
                rule_name=rule.name,
                severity="low",
                message=f"自审规则执行异常：{e}",
                recommended_action="continue"
            )

        return None
```

### 3.2 与 TAOR 循环的集成

```python
# AIP 层（aip_taor_loop.py）

class TAORLoopController:
    async def run_skill(self, skill_template: SkillTemplate, context: dict) -> SkillResult:
        # 1. Think
        plan = await self._think(skill_template.taor_spec.think, context)

        # 2. Act
        action_result = await self._act(skill_template.taor_spec.act, context, plan)

        # 3. Reflect ← FDE 的 ReflectionExecutor 在此被调用
        reflection = await self._reflection_executor.reflect(
            skill_id=skill_template.id,
            action_result=action_result,
            context=context
        )

        if reflection.should_retry:
            # 重试当前技能（带更新后的上下文）
            return await self.run_skill(skill_template, {**context, **reflection.updated_context})

        if reflection.should_rollback:
            # 触发回滚（详见 02-Checkpoint 与回滚设计）
            await self._rollback_manager.rollback_to(
                task=context["task"],
                target_cp_id=reflection.rollback_target,
                reason=reflection.issues[0].message
            )
            return SkillResult(success=False, rolled_back=True)

        if reflection.should_pause:
            # 暂停等待用户（详见 02-Checkpoint §三.3）
            await self._pause_task(context["task"], reflection)
            return SkillResult(success=False, paused=True)

        # 4. Observe
        await self._observe(skill_template.taor_spec.observe, action_result, context)

        return SkillResult(success=True)
```

---

## 四、自审规则配置

### 4.1 规则加载

```python
# aip_fde_reflection_config.py

ALL_REFLECTION_RULES = {
    "fde-skill-1-dialog": SKILL_1_REFLECTION_RULES,
    "fde-skill-2-auth": SKILL_2_REFLECTION_RULES,
    "fde-skill-3-api-explore": SKILL_3_REFLECTION_RULES,
    "fde-skill-4-field-mapping": SKILL_4_REFLECTION_RULES,
    "fde-skill-5-sync-config": SKILL_5_REFLECTION_RULES,
    "fde-skill-6-test": SKILL_6_REFLECTION_RULES,
}


def register_fde_reflection_rules(reflection_executor: ReflectionExecutor):
    """注册 FDE 自审规则。"""
    for skill_id, rules in ALL_REFLECTION_RULES.items():
        reflection_executor.register_rules(skill_id, rules)
```

### 4.2 规则统计数据

| 技能 | 规则数 | 硬规则（Python） | 软规则（LLM） |
|------|-------|----------------|-------------|
| 技能1 对话理解 | 4 | 4 | 0 |
| 技能2 认证配置 | 3 | 2 | 1（credentials 格式） |
| 技能3 API 探索 | 4 | 3 | 1（Schema 完整性） |
| 技能4 字段映射 | 6 | 4 | 2（冲突检测、经验匹配） |
| 技能5 同步配置 | 4 | 3 | 1（策略合理性） |
| 技能6 测试验证 | 5 | 5 | 0 |
| **总计** | **26** | **21** | **5** |

### 4.3 规则更新机制

```python
# 规则可通过 API 动态更新（不重启服务）

POST /v1/fde/reflection/rules
Body: {
    "skill_id": "fde-skill-4-field-mapping",
    "rule": {
        "name": "coverage_check",
        "condition": "context.coverage >= 0.85",  # 提高阈值
        "on_fail": {...}
    }
}

# 规则版本追溯
GET /v1/fde/reflection/rules/{rule_id}/versions
```

---

## 五、与记忆系统的协作

### 5.1 Reflection 结果写入 Episodic Memory

```python
class ReflectionMemoryWriter:
    """将 Reflection 结果写入 Episodic Memory。"""

    async def write_reflection_result(self, task_id: str, skill_id: str, result: ReflectionResult):
        """记录自审结果到情景记忆，供后续接入复用。"""
        episodic_record = EpisodicRecord(
            task_id=task_id,
            event_type="reflection",
            skill_id=skill_id,
            content={
                "passed": result.passed,
                "issues": [issue.dict() for issue in result.issues],
                "recommendation": result.recommendation,
                "timestamp": time.time(),
            },
            tags=["fde", "reflection", skill_id],
            ttl_days=90,  # 90 天后过期
        )
        await self._episodic_store.write(episodic_record)


# 示例：下次接入同平台时检索历史自审问题
async def get_historical_reflection_issues(platform: str, skill_id: str) -> list[dict]:
    """检索该平台该技能的历史自审问题。"""
    records = await episodic_store.search(
        tags=["fde", "reflection", skill_id],
        filter={"platform": platform},
        limit=10
    )
    return [
        {
            "issue": r.content["issues"],
            "resolution": r.content.get("resolution"),
            "frequency": r.metadata.get("frequency", 1)
        }
        for r in records if not r.content["passed"]
    ]
```

### 5.2 自审规则自适应

```python
class AdaptiveReflectionRules:
    """根据历史自审结果调整规则阈值。"""

    async def adjust_thresholds(self, platform: str, skill_id: str):
        """根据历史数据调整阈值。"""
        historical_issues = await get_historical_reflection_issues(platform, skill_id)

        if not historical_issues:
            return  # 无历史数据，使用默认阈值

        # 示例：如果某平台历史映射覆盖率从未超过 0.85，可适当降低阈值
        if skill_id == "fde-skill-4-field-mapping":
            avg_coverage = calculate_avg_coverage(historical_issues)
            if avg_coverage < 0.85:
                new_threshold = max(0.7, avg_coverage - 0.05)
                update_rule_threshold("fde-skill-4", "coverage_check", new_threshold)
                log.info(f"调整 {platform} 映射覆盖率阈值：0.8 → {new_threshold}")
```

---

## 六、与现有代码的对接

| 新增模块 | 对接的现有代码 | 改动方式 |
|---------|-------------|---------|
| `aip_fde_reflection.py` | AIP `TAORLoopController._reflect()` | 替换 `_reflect` 方法实现 |
| `aip_fde_reflection_config.py` | AIP `ReflectionExecutor` | 通过 `register_rules` 注册 |
| `aip_fde_reflection.py` | AIP `EpisodicMemoryStore` | 写入自审结果 |
| `aip_fde_reflection.py` | AIP `RollbackManager` | 触发回滚 |
| `aip_fde_reflection.py` | AIP `TaskStateMachine` | 触发暂停 |

**不修改的现有模块**：
- `aip_taor_loop.py` — 仅扩展 `_reflect` 方法实现
- `aip_logic_engine.py` — 不修改
- `aip_checkpoint_store.py` — 仅调用

---

## 七、测试方案

### 7.1 自动化测试用例

```python
# tests/test_fde_reflection.py

class TestFDEReflection:

    async def test_skill_1_missing_params_paused(self, reflection_executor):
        """技能1 缺失必填参数时暂停。"""
        context = {"params": {"platform": "taobao"}}  # 缺 merchant_id, credentials
        action_result = ActionResult(success=True)

        result = await reflection_executor.reflect("fde-skill-1-dialog", action_result, context)

        assert result.passed == False
        assert result.should_pause == True
        assert "merchant_id" in result.issues[0].message

    async def test_skill_2_connectivity_fail_retry(self, reflection_executor):
        """技能2 连通性测试失败时重试。"""
        context = {
            "platform": "taobao",
            "credentials": {"app_key": "xxx", "app_secret": "yyy"},
            "connectivity_test_passed": False
        }
        action_result = ActionResult(success=True)

        result = await reflection_executor.reflect("fde-skill-2-auth", action_result, context)

        assert result.passed == False
        assert result.should_retry == True

    async def test_skill_4_low_coverage_rollback(self, reflection_executor):
        """技能4 覆盖率极低时回滚。"""
        context = {"coverage": 0.4, "avg_confidence": 0.5}
        action_result = ActionResult(success=True)

        result = await reflection_executor.reflect("fde-skill-4-field-mapping", action_result, context)

        assert result.passed == False
        assert result.should_rollback == True

    async def test_skill_4_medium_coverage_paused(self, reflection_executor):
        """技能4 覆盖率中等时暂停。"""
        context = {"coverage": 0.65, "avg_confidence": 0.7}
        action_result = ActionResult(success=True)

        result = await reflection_executor.reflect("fde-skill-4-field-mapping", action_result, context)

        assert result.passed == False
        assert result.should_pause == True

    async def test_skill_6_quality_issues_reported(self, reflection_executor):
        """技能6 质量问题生成报告但不阻断。"""
        context = {
            "data_quality_score": 0.6,
            "null_rate": 0.08,
            "schema_consistent": True
        }
        action_result = ActionResult(success=True)

        result = await reflection_executor.reflect("fde-skill-6-test", action_result, context)

        assert result.passed == False
        assert result.should_pause == True  # 暂停等用户确认是否接受质量

    async def test_reflection_result_recorded_to_episodic(self, reflection_executor, episodic_store):
        """自审结果写入 Episodic Memory。"""
        context = {"coverage": 0.4}
        await reflection_executor.reflect("fde-skill-4-field-mapping", ActionResult(success=True), context)

        records = await episodic_store.search(tags=["fde", "reflection", "fde-skill-4-field-mapping"])
        assert len(records) >= 1
        assert records[0].content["passed"] == False
```

### 7.2 验收标准

- [ ] 技能1 缺失必填参数触发暂停
- [ ] 技能2 认证连通性失败触发重试（最多3次）
- [ ] 技能3 必需 API 缺失触发暂停
- [ ] 技能4 覆盖率 < 0.5 触发回滚到 CP3
- [ ] 技能4 0.5 ≤ 覆盖率 < 0.8 触发暂停
- [ ] 技能4 置信度 < 0.7 触发暂停
- [ ] 技能5 首次同步失败重试3次后回滚到 CP4
- [ ] 技能6 数据质量差生成报告
- [ ] 自审结果写入 Episodic Memory
- [ ] 自审规则可通过 API 动态更新
- [ ] `pytest tests/test_fde_reflection.py` 全部通过

---

## 八、新增模块清单

| 模块 | 路径 | 职责 |
|------|------|------|
| `aip_fde_reflection.py` | `aos-platform-w4/services/aos-api/aos_api/` | Reflection 执行器 |
| `aip_fde_reflection_config.py` | 同上 | 26 条自审规则配置 |
| `tests/test_fde_reflection.py` | `aos-platform-w4/services/aos-api/tests/` | 自动化测试 |

**新增 API 端点**：
- `POST /v1/fde/reflection/rules` — 动态更新规则
- `GET /v1/fde/reflection/rules/{rule_id}/versions` — 查看规则版本

**不修改的现有模块**：
- `aip_taor_loop.py` — 仅扩展 `_reflect` 方法实现
- `aip_logic_engine.py` — 不修改
- `aip_checkpoint_store.py` — 仅调用

---

*本文档为方案设计层，实施前需用户确认。*
*关联文档：`../11-AIP决策引擎升级方案/01-Plan-Mode与TAOR循环设计.md` · `00-总览-从静态文档到可编排技能链.md` · `01-电商FDE技能链设计.md` · `02-Checkpoint与回滚设计.md` · `03-六层权限防线设计.md`*
