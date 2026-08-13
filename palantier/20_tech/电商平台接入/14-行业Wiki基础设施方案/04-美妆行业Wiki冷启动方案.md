# 美妆行业 Wiki 冷启动方案 — 知识包内容 · 种子数据 · 执行步骤

> **2026-08-13 AIP-5 E6 权威覆盖：** 美妆知识改为可安装/卸载/回滚的 `VerticalPack`，不写入核心代码。本文的 353 条是容量目标而非现有数据；没有逐条 source/license/hash/freshness Receipt 时计数为 0。CosDNA 未核验授权时禁止抓取，NMPA 需按当前动态清单版本登记。所有内容先进入 Candidate 治理链，禁止 L1/L2 或导入脚本直写 Semantic/Wiki。

> 创建时间：2026-07-29
> 状态：方案设计（先方案后编码）
> 关联：`00-总览-三层记忆系统.md` §八（冷启动骨架）· `02-七条知识管道设计.md`（管道1/5/7）· `03-知识治理三层过滤.md`（所有等级统一 Candidate 治理）
> 目标：美妆行业第一个垂直落地的知识包，冷启动后可支撑 6 数字同事 + FDE 的知识检索

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案层 |
| 最小更改 | 冷启动走管道1/5/7 已有实现，不新建管道 |
| 不影响现有功能 | 冷启动是可回滚 VerticalPack 导入；阻断时不回退 Mock |
| 涉及新增代码输出具体文件目录 | 见 §七 模块清单 |
| 自测验证 | §六 给出冷启动验收标准（可量化） |

---

## 一、冷启动目标

### 1.1 问题

新商家接入 AOS 后，行业 Wiki 是空的。6 数字同事和 FDE 检索 Semantic 层无结果，技能执行退化为"无知识辅助的裸 LLM 调用"，成功率从 85% 降到 60%。

### 1.2 目标

冷启动后，美妆行业 Wiki 需满足：

| 指标 | 目标值 | 验证方式 |
|------|--------|---------|
| Semantic 层知识条数 | ≥ 300 条 | `SELECT count(*) FROM knowledge_entries` |
| 成分知识 | ≥ 200 条 | `WHERE category = 'ingredient'` |
| 话术模板 | ≥ 50 条 | `WHERE category = 'script_template'` |
| 平台规则 | ≥ 30 条 | `WHERE category = 'platform_rule'` |
| RAG 检索准确率 | ≥ 80% | 人工标注 50 条查询的 Top-1 准确率 |
| 6 数字同事依赖覆盖 | 100% | 每个数字同事的 Semantic 依赖表至少有 1 条命中 |

### 1.3 冷启动策略

```
管道1 种子（P0）→ 23 篇方案 + 美妆 SOP
管道5 专业库（P0）→ CosDNA 成分 + NMPA 法规
管道7 人工（P0）→ 资深美妆运营经验结构化
─────────────────────────────
管道6 客户（P1）→ 微商城 30 个客户行为分析（运营 1 周后）
管道2 自学习（P2）→ 运行后自动积累（运营 2 周后）
管道3 网络（P2）→ 平台规则变化监控（运营后持续）
管道4 竞品（P3）→ 竞品周报（运营 1 个月后）
```

---

## 二、知识包内容设计

### 2.1 成分知识（管道5 — CosDNA）

| 成分类别 | 条数预估 | 关键字段 | owner_agents |
|---------|---------|---------|-------------|
| 防腐剂 | 30 | 名称/功能/安全等级/致敏性/孕妇慎用 | 导购顾问、内容官 |
| 防晒剂 | 25 | 同上 + SPF/PA 值 | 导购顾问 |
| 表面活性剂 | 20 | 同上 + 清洁力等级 | 导购顾问 |
| 香精 | 15 | 同上 + 常见过敏原标记 | 导购顾问、客服专员 |
| 功效成分 | 110 | 同上 + 功效分类（保湿/美白/抗衰/祛痘） | 导购顾问、内容官 |

**示例条目**：

```python
KnowledgeEntry(
    title="成分: 烟酰胺（Niacinamide）",
    content="""
中文名: 烟酰胺
英文名: Niacinamide / Vitamin B3
功能: 美白/控油/修护屏障
安全等级: 1（最安全）
致敏性: 低（高浓度可能刺激）
孕妇慎用: 否
浓度建议: 2-5%
常见搭配: 与透明质酸搭配增强保湿
禁忌: 避免与高浓度 VC 同时使用（pH 冲突）
""",
    category="ingredient",
    confidence_level="L2",
    source="pipe5_cosdna",
    tags=["功效成分", "美白", "安全等级1"],
    owner_agents=["shopping_advisor", "content_officer"],
)
```

### 2.2 话术模板（管道1+7）

| 模板类型 | 条数预估 | 适用数字同事 |
|---------|---------|------------|
| 破冰话术 | 10 | 私域管家 |
| 跟进话术 | 10 | 私域管家 |
| 产品推荐话术 | 10 | 导购顾问 |
| 内容文案模板 | 10 | 内容官 |
| 售后安抚话术 | 5 | 客服专员 |
| 活动邀约话术 | 5 | 活动策划师 |

**示例条目**：

```python
KnowledgeEntry(
    title="话术: 敏感肌破冰（VIP客户）",
    content="""
适用场景: VIP 客户首次触达，肤质为敏感肌
话术模板: {客户称呼}您好，注意到您之前关注过{产品类别}，
          我们刚到了一批专为敏感肌设计的{品牌}新品，
          成分不含酒精和香精，要不要为您寄一份体验装？
约束:
  - 长度 ≤ 30 字
  - 必须提到具体产品名
  - 不含敏感词
  - VIP 客户需提到权益
""",
    category="script_template",
    confidence_level="L2",
    source="pipe7_manual",
    tags=["破冰", "敏感肌", "VIP"],
    owner_agents=["private_butler"],
    platform_scope=[],  # 跨平台通用
)
```

### 2.3 平台规则（管道1）

| 规则类型 | 条数预估 | platform_scope |
|---------|---------|---------------|
| 淘宝内容审核规则 | 8 | taobao |
| 天猫商品发布规则 | 5 | tmall |
| 抖音短视频/直播规则 | 8 | douyin |
| 快手电商规则 | 5 | kuaishou |
| 微商城运营规则 | 4 | niushop |

### 2.4 FDE API 文档（管道1）

| 平台 | 条数 | 内容 |
|------|------|------|
| 淘宝开放平台 | 5 | 商品/订单/会员 API Schema |
| 微商城 API | 5 | 商品/订单/客户 API Schema |
| 抖音电商 API | 5 | 商品/订单/粉丝 API Schema |
| 通用 Ontology | 5 | 统一字段定义 |

### 2.5 专家经验（管道7）

| 经验类型 | 条数预估 | owner_agents |
|---------|---------|-------------|
| 美妆客户分层标签体系 | 5 | 私域管家、数据参谋 |
| 美妆选品方法论 | 5 | 活动策划师 |
| 美妆定价基准线 | 3 | 活动策划师 |
| 美妆售后处理 SOP | 5 | 客服专员 |
| 美妆内容爆款标题规律 | 5 | 内容官 |
| 美妆成分搭配禁忌 | 5 | 导购顾问 |

---

## 三、管道5 对接 CosDNA 接口设计

### 3.1 CosDNA 历史爬取草图（许可未知，已禁止）

下列 crawler 代码仅保留历史审计，禁止实现或运行。恢复此来源必须先提供可审计的授权、使用政策、版本和允许保存范围，再经 E5 专业数据库管道与 E6 trusted adapter 评审；否则持续返回 `license_unknown`。

```python
class CosDNACrawler:
    """CosDNA 成分库爬取器。

    策略：按成分类别分批爬取，LLM 结构化后入库。
    """

    CATEGORIES = [
        "/ ingredient.php?class=1",  # 防腐剂
        "/ingredient.php?class=2",  # 防晒剂
        "/ingredient.php?class=3",  # 表面活性剂
        "/ingredient.php?class=4",  # 香精
        "/ingredient.php?class=5",  # 功效成分
    ]

    async def crawl_category(self, category_url: str) -> list[dict]:
        """爬取一个成分类别。"""
        # 1. Kitewright 浏览器自动化翻页
        pages = await self._browser.paginate(category_url, max_pages=10)

        # 2. 解析成分列表
        ingredients = []
        for page in pages:
            items = self._parse_ingredient_list(page)
            ingredients.extend(items)

        # 3. 逐条详情页爬取
        for ing in ingredients:
            detail = await self._browser.fetch(ing["detail_url"])
            ing.update(self._parse_detail(detail))

        return ingredients

    def _parse_detail(self, html: str) -> dict:
        """解析成分详情页。"""
        # 提取：中文名/英文名/功能/安全等级/致敏性/孕妇慎用
        return {
            "chinese_name": ...,
            "english_name": ...,
            "function": ...,
            "safety_rating": ...,  # 1-5
            "allergen": ...,
            "pregnancy_warning": ...,
        }
```

### 3.2 NMPA 法规同步

```python
class NMPASyncer:
    """NMPA 法规同步器。"""

    REGULATION_LIST = [
        "化妆品监督管理条例",
        "化妆品注册备案管理办法",
        "化妆品生产经营监督管理办法",
        "化妆品标签管理办法",
    ]

    async def sync(self) -> int:
        count = 0
        for reg_name in self.REGULATION_LIST:
            reg = await self._fetch_nmpa_document(reg_name)
            if reg:
                entry = KnowledgeEntry(
                    title=f"法规: {reg['title']}",
                    content=reg["content"],
                    category="platform_rule",
                    confidence_level="L1",
                    source="pipe5_nmpa",
                    source_url=reg.get("url", ""),
                    tags=["regulation", "nmpa", "cosmetics"],
                    effective_until=None,
                    review_cycle_days=90,
                )
                await self._semantic.store(entry)  # L1 直接入库
                count += 1
        return count
```

---

## 四、冷启动执行步骤

### 4.1 执行顺序

```
Step 1: 已授权专业来源 Candidate 导入（目标 200 条；当前 0，DATA_BLOCKED）
  └─ 预计耗时：2h（爬取 + 结构化 + 入库）

Step 2: 管道5 NMPA 法规导入（10 条）
  └─ 预计耗时：30min

Step 3: 管道1 种子知识导入（115 条）
  └─ 23 篇方案 + 美妆 SOP 结构化入库
  └─ 预计耗时：1h

Step 4: 管道7 人工经验注入（28 条）
  └─ 资深运营录入经验
  └─ 预计耗时：2h（人工）

Step 5: 向量化 + 索引构建
  └─ 对已治理知识构建可重建全文索引；向量 capability 未就绪时诚实降级
  └─ 预计耗时：30min

Step 6: 验收测试
  └─ 检索准确率 + 依赖覆盖
  └─ 预计耗时：1h
```

### 4.2 冷启动脚本

```python
# scripts/bootstrap_beauty_wiki.py

async def bootstrap():
    """美妆行业 Wiki 冷启动脚本。"""
    memory = MemorySystem(...)

    # Step 1: CosDNA 成分库
    cosdna = CosDNACrawler(...)
    ing_count = 0
    for cat_url in cosdna.CATEGORIES:
        ingredients = await cosdna.crawl_category(cat_url)
        for ing in ingredients:
            entry = KnowledgeEntry(
                title=f"成分: {ing['chinese_name']}",
                content=format_ingredient(ing),
                category="ingredient",
                confidence_level="L2",
                source="pipe5_cosdna",
                owner_agents=["shopping_advisor", "content_officer"],
            )
            await memory.semantic.store(entry)
            ing_count += 1
    print(f"Step 1: CosDNA 成分导入 {ing_count} 条")

    # Step 2: NMPA 法规
    nmpa = NMPASyncer(...)
    reg_count = await nmpa.sync()
    print(f"Step 2: NMPA 法规导入 {reg_count} 条")

    # Step 3: 种子知识
    seed = Pipe1SeedImport(...)
    seed_count = await seed.run()
    print(f"Step 3: 种子知识导入 {seed_count} 条")

    # Step 4: 人工经验（从 Excel 加载）
    manual = Pipe7ManualInjection(...)
    manual_count = await manual.inject_batch(load_expert_excel("美妆专家经验.xlsx"))
    print(f"Step 4: 人工经验导入 {manual_count} 条")

    # Step 5: 向量化（store 时自动生成，确认全部完成）
    total = await memory.semantic.count()
    print(f"Step 5: 总知识量 {total} 条，向量化完成")

    # Step 6: 验收
    await run_acceptance_test(memory)
```

---

## 五、冷启动后的知识分布

### 5.1 预期知识分布

```
美妆行业 Wiki 冷启动后
├── 成分知识（ingredient）     200 条  (57%)
├── 平台规则（platform_rule）  45 条  (13%)
├── 话术模板（script_template） 50 条  (14%)
├── 专家经验（expert_knowledge）28 条  (8%)
├── FDE API 文档（fde_api_doc）20 条  (6%)
└── Ontology 模型              10 条  (3%)
────────────────────────────────
总计目标                       353 条（非现有资产，不得作为完成计数）
```

### 5.2 按数字同事覆盖

| 数字同事 | 可检索条数 | 覆盖率 |
|---------|----------|--------|
| 导购顾问 | 200(成分)+10(推荐话术)+5(搭配禁忌) = 215 | 100% |
| 内容官 | 200(成分)+10(文案模板)+5(标题规律) = 215 | 100% |
| 私域管家 | 10(破冰)+10(跟进)+5(分层标签) = 25 | 100% |
| 客服专员 | 5(售后话术)+5(售后SOP)+4(微商城规则) = 14 | 100% |
| 活动策划师 | 5(选品)+3(定价)+5(活动话术) = 13 | 100% |
| 数据参谋 | 5(分层标签)+3(行业基准) = 8 | 100% |
| FDE | 20(API文档)+5(Ontology) = 25 | 100% |

---

## 六、验收标准

### 6.1 量化验收

| 验收项 | 目标 | 验证 SQL/方法 |
|--------|------|-------------|
| 总知识量 | ≥ 300 条 | `SELECT count(*) FROM knowledge_entries WHERE effective_until IS NULL OR effective_until > now()` |
| 成分知识 | ≥ 200 条 | `WHERE category = 'ingredient'` |
| 话术模板 | ≥ 50 条 | `WHERE category = 'script_template'` |
| 平台规则 | ≥ 30 条 | `WHERE category = 'platform_rule'` |
| L1+L2 占比 | ≥ 70% | `WHERE confidence_level IN ('L1','L2')` |
| 向量化覆盖率 | 100% | `WHERE embedding IS NOT NULL` |
| owner_agents 非空率 | ≥ 90% | `WHERE array_length(owner_agents, 1) > 0` |

### 6.2 检索准确率验收

人工标注 50 条查询，验证 Top-1 准确率：

```python
ACCEPTANCE_QUERIES = [
    {"query": "烟酰胺能不能和VC一起用", "expected_category": "ingredient", "expected_keyword": "烟酰胺"},
    {"query": "敏感肌推荐什么防晒", "expected_category": "ingredient", "expected_keyword": "防晒"},
    {"query": "淘宝直播有什么规则", "expected_category": "platform_rule", "expected_keyword": "直播"},
    {"query": "VIP客户破冰话术", "expected_category": "script_template", "expected_keyword": "破冰"},
    {"query": "退款怎么处理", "expected_category": "expert_knowledge", "expected_keyword": "售后"},
    # ... 共 50 条
]

async def run_acceptance_test(memory: MemorySystem) -> float:
    correct = 0
    for q in ACCEPTANCE_QUERIES:
        results = await memory.semantic.retrieve(q["query"], top_k=1)
        if results and q["expected_keyword"] in results[0].content:
            correct += 1
    accuracy = correct / len(ACCEPTANCE_QUERIES)
    print(f"检索准确率: {accuracy:.1%}（目标 ≥ 80%）")
    assert accuracy >= 0.8, f"检索准确率 {accuracy:.1%} 低于 80%"
    return accuracy
```

### 6.3 依赖覆盖验收

```python
async def verify_dependency_coverage(memory: MemorySystem) -> None:
    """验证 6 数字同事 + FDE 的 Semantic 依赖全部有命中。"""
    dependencies = {
        "private_butler": ["美妆话术模板", "敏感词库", "防封规则"],
        "shopping_advisor": ["成分兼容库", "肤质匹配规则", "产品知识"],
        "content_officer": ["平台内容规则", "品牌调性指南", "爆款标题模板"],
        "service_agent": ["售后政策", "话术库", "情绪识别规则"],
        "event_planner": ["大促节奏模板", "品类占比基准", "定价方法论"],
        "data_advisor": ["行业基准值", "归因方法论", "漏斗参考值"],
        "fde_orchestrator": ["平台认证文档", "API Schema", "Ontology"],
    }

    for agent, deps in dependencies.items():
        for dep in deps:
            results = await memory.semantic.retrieve(
                dep, filters=RetrievalFilters(owner_agents=[agent]), top_k=1
            )
            assert len(results) > 0, f"{agent} 的依赖 '{dep}' 无命中"

    print("✅ 6 数字同事 + FDE 依赖覆盖 100%")
```

---

## 七、新增模块清单

| 模块 | 路径 | 职责 | 来源章节 |
|------|------|------|---------|
| `scripts/bootstrap_beauty_wiki.py` | `aos-platform-w4/services/aos-api/` | 冷启动执行脚本 | §四 |
| `scripts/cosdna_crawler.py` | 同上 | CosDNA 成分库爬取器 | §三 |
| `scripts/nmpa_syncer.py` | 同上 | NMPA 法规同步器 | §三 |
| `data/美妆专家经验.xlsx` | `aos-platform-w4/services/aos-api/data/` | 人工经验录入模板 | §四 |

### 对接现有代码

| 新增模块 | 对接现有代码 | 对接方式 |
|---------|-----------|---------|
| `bootstrap_beauty_wiki.py` | `aip_memory.py`（01 文档） | 调用 `MemorySystem.semantic.store()` |
| `cosdna_crawler.py` | `aip_knowledge_pipeline.py`（02 文档 Pipe5） | 扩展 Pipe5 的爬取实现 |
| `nmpa_syncer.py` | `aip_knowledge_pipeline.py`（02 文档 Pipe5） | 扩展 Pipe5 的法规同步 |

**零修改**：不修改任何现有核心模块

---

## 八、关键设计决策

| # | 决策 | Why | 影响 |
|---|------|-----|------|
| 1 | 冷启动优先管道1/5/7（种子+专业库+人工） | 这三条管道提供 L1/L2 级知识，无需审核直接入库，冷启动最快 | L3/L4 管道运营后逐步积累 |
| 2 | CosDNA 成分库 200 条作为冷启动核心 | 成分知识是导购顾问和内容官的核心依赖，覆盖 6 数字同事中 2 个最关键角色 | 冷启动后导购/内容官可立即工作 |
| 3 | 人工经验走 Excel 批量导入 | 运营人员更习惯 Excel，降低录入门槛 | 录入效率高，经验结构化快 |
| 4 | 检索准确率验收 50 条人工标注 | 量化验证冷启动质量，不靠"感觉" | 不达标可及时发现 |
| 5 | 依赖覆盖验收 100% | 每个数字同事至少有 1 条 Semantic 命中 | 保证冷启动后所有数字同事可用 |
| 6 | 冷启动总耗时 ≤ 7h | 2h CosDNA + 30min NMPA + 1h 种子 + 2h 人工 + 30min 向量化 + 1h 验收 | 一天内完成 |

---

*本文档为方案设计层，实施前需用户确认。*
*关联：`00-总览-三层记忆系统.md` §八（骨架）· `02-七条知识管道设计.md`（管道1/5/7）· `03-知识治理三层过滤.md`（所有等级统一 Candidate 治理）*
