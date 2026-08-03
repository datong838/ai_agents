# Verification Loops — 验证循环

> 学习时间：2026-07-28
> 来源：[Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills)
> 定位：Agent 工程的核心机制理论，适用于任何 LLM 驱动的 Agent 系统

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 用中文回答所有问题 | 全文 |
| 先方案后编码 | 本文档为知识理论层，不含代码实现 |

---

## 一、核心概念

### 1.1 什么是 Verification Loop

Verification Loop 是一个**迭代过程**：AI agent 检查自己的工作（运行测试、linter、自定义检查），修复失败项，然后再前进。

> "A verification loop is an iterative process where an AI agent checks its own work — running tests, linters, or custom checks — and fixes any failures before moving on."

这不是事后检查，而是**嵌入到执行流程中的自验证机制**。

### 1.2 Agentic Loop 三步

Claude Code 的 Agent 循环由三步组成：

```
gathering context → taking action → verifying results
       ↑                                    │
       └────────────────────────────────────┘
                    循环
```

**关键洞察**：验证不是循环外的附加步骤，而是循环的**内生环节**。没有验证的 Agent 循环是不完整的。

### 1.3 与传统测试的区别

| 维度 | 传统测试 | Verification Loop |
|------|---------|-------------------|
| 时机 | 事后（CI/CD） | 事中（执行过程中） |
| 执行者 | CI 系统 | Agent 自己 |
| 修复 | 人工修复 | Agent 自动修复 + 重试 |
| 粒度 | 文件/模块级 | 步骤/动作级 |
| 反馈 | 延迟（分钟/小时级） | 即时（秒级） |

---

## 二、四种触发模式

### 2.1 模式总览

| 模式 | 触发方式 | 适用场景 | 类比 |
|------|---------|---------|------|
| **Standalone** | 手动触发 | 跨领域检查 | 专家会诊 |
| **Embedded** | 嵌入生产技能自动触发 | 单工作流内置检查 | 流水线质检员 |
| **Chained** | 一个技能调用另一个，形成链 | 端到端验证 | 供应链溯源 |
| **On every PR** | CI/CD 级别全员门控 | 团队基础设施 | 海关 |

### 2.2 Standalone（独立模式）

```
用户：/verify
  ↓
Agent 运行验证技能（安全扫描、无障碍审计、代码审查）
  ↓
输出报告 + 自动修复建议
```

**特点**：
- 手动触发，按需使用
- 跨领域，不绑定特定生产技能
- 输出报告，不自动修改

**适用场景**：
- 安全扫描（检查依赖漏洞、敏感信息泄露）
- 无障碍审计（WCAG 合规检查）
- 代码审查（风格、复杂度、最佳实践）
- 性能分析（bundle 大小、渲染性能）

### 2.3 Embedded（嵌入模式）

```
生产技能：生成代码
  ↓
（自动触发）内嵌的验证技能：运行 lint + 单元测试
  ↓
失败？→ 自动修复 → 重新验证
通过？→ 继续下一步
```

**特点**：
- 嵌入到生产技能内部，用户无感
- 每次执行生产技能自动触发
- 支持自动修复 + 重试

**适用场景**：
- 写代码后自动运行 lint
- 生成配置后自动验证语法
- 修改文件后自动运行相关测试

### 2.4 Chained（链式模式）

```
/code-review → /simplify → /verify → /design
     ↓              ↓           ↓          ↓
   审查代码      简化代码    验证正确性   设计审查
```

**特点**：
- 一个验证技能调用另一个，形成链
- 端到端验证，覆盖多个维度
- 每个环节的输出是下一个环节的输入

**适用场景**：
- 代码审查 → 简化 → 验证 → 设计审查（完整链）
- 生成 → 格式检查 → 安全扫描 → 性能测试（质量链）
- 数据接入 → 字段映射 → 类型验证 → 业务校验（数据链）

### 2.5 On every PR（CI/CD 模式）

```
开发者提交 PR
  ↓
CI/CD 自动触发验证技能
  ↓
全部通过？→ 允许合并
有失败？→ 阻止合并 + 通知修复
```

**特点**：
- 团队级基础设施
- 强制门控，不可跳过
- 覆盖所有提交

**适用场景**：
- 团队代码质量门控
- 安全合规检查
- 依赖更新验证

---

## 三、Skill 编码方式

### 3.1 SKILL.md 文件结构

Claude Code 的验证技能用 `.claude/skills/SKILL.md` 文件编码：

```yaml
---
name: verify-code-quality
description: |
  检查代码质量：运行 lint、类型检查、单元测试。
  失败时自动修复并重新验证。
trigger: embedded  # standalone | embedded | chained | pr
parent_skill: generate-code  # 嵌入模式时指定父技能
max_retries: 3
---

# Verify Code Quality

## 检查项
1. 运行 `npm run lint` — 检查代码风格
2. 运行 `npx tsc --noEmit` — 检查类型
3. 运行 `npm test` — 运行单元测试

## 自动修复规则
- lint 错误：运行 `npm run lint --fix`
- 类型错误：根据错误信息修复类型
- 测试失败：分析失败原因，修复代码或测试

## 严重性分级
- critical：阻止继续执行，需人工介入
- high：自动修复后重试，3次失败则停止
- medium：记录警告，继续执行
- low：仅记录，不影响流程
```

### 3.2 Frontmatter 字段说明

| 字段 | 说明 | 可选值 |
|------|------|--------|
| `name` | 技能唯一标识 | 小写+连字符 |
| `description` | 技能描述 | 多行文本 |
| `trigger` | 触发模式 | standalone / embedded / chained / pr |
| `parent_skill` | 父技能（嵌入模式） | 技能名 |
| `max_retries` | 最大重试次数 | 整数 |
| `severity` | 默认严重性 | critical / high / medium / low |

### 3.3 skill-creator 插件

Claude Code 提供 `skill-creator` 插件，可以自动生成 SKILL.md 骨架：

```
/skill-creator
  → 输入技能名称
  → 输入触发模式
  → 输入检查项
  → 自动生成 .claude/skills/SKILL.md
```

---

## 四、验证技能的设计原则

### 4.1 单一职责

每个验证技能只检查**一个维度**：

```
✅ 好的设计：
verify-lint        → 只检查代码风格
verify-types       → 只检查类型
verify-tests       → 只运行测试
verify-security    → 只检查安全

❌ 坏的设计：
verify-everything  → 检查所有（职责不清，无法组合）
```

### 4.2 可组合

验证技能应该可以**自由组合**为链：

```
# Chained 模式的自由组合
/code-review → /simplify → /verify → /design

# 也可以单独使用
/verify
```

### 4.3 自动修复优先

验证失败时，优先尝试自动修复，而非直接报错：

```
验证失败
  ↓
有 auto_fix 策略？
  ├── 是 → 执行自动修复 → 重新验证
  │        ↓
  │        修复成功？→ 继续
  │        修复失败？→ 重试次数 < max_retries？→ 重试
  │                                          → 超限？→ 报错
  └── 否 → 记录失败 → 是否 critical？
                          ├── 是 → 停止执行，需人工
                          └── 否 → 记录警告，继续
```

### 4.4 严重性分级

| 级别 | 含义 | 处理方式 |
|------|------|---------|
| **critical** | 不可恢复的严重错误 | 立即停止，需人工介入 |
| **high** | 重要问题，影响功能 | 自动修复 + 重试（最多 max_retries 次） |
| **medium** | 次要问题，不影响主流程 | 记录警告，继续执行 |
| **low** | 提示性信息 | 仅记录，不影响任何流程 |

### 4.5 Generator-Evaluator 分离

这是 Claude 产品哲学的核心原则之一：

```
Generator（生产技能）     Evaluator（验证技能）
─────────────────       ──────────────────
生成代码                检查代码
生成配置                验证配置
生成文案                审查文案

  ↓                        ↓
  产出 Artifact            产出 VerifyResult
  ↓                        ↓
  └──────── 匹配 ──────────┘
        ↓
   通过？交付 / 失败？修复
```

**关键**：生成和验证是**分离的两个技能**，不是同一个技能的自审。这避免了"自己检查自己"的盲区。

---

## 五、验证技能的检查类型

### 5.1 检查类型分类

| 类型 | 说明 | 示例 |
|------|------|------|
| **语法检查** | 代码/配置的语法正确性 | lint, tsc, JSON validate |
| **类型检查** | 类型系统的约束 | TypeScript type check |
| **测试运行** | 单元/集成/E2E 测试 | npm test, pytest |
| **安全扫描** | 安全漏洞和敏感信息 | dependency scan, PII check |
| **性能检查** | 性能指标 | bundle size, render time |
| **合规检查** | 业务规则和合规要求 | GDPR, brand guideline |
| **一致性检查** | 多文件/模块间的一致性 | API contract, import/export |

### 5.2 检查的输入和输出

```yaml
# 验证技能的输入
input:
  artifact: ActResult        # 生产技能的产出
  context: TaskContext        # 任务上下文
  step: TaskStep              # 当前步骤

# 验证技能的输出
output:
  passed: bool                # 是否通过
  issues:                     # 发现的问题列表
    - severity: high
      message: "Type error on line 42"
      auto_fixable: true
      fix_strategy: "add type annotation"
  should_retry: bool          # 是否应重试
  is_fatal: bool              # 是否致命错误
```

---

## 六、验证循环的状态机

```
                    ┌─────────┐
                    │  START  │
                    └────┬────┘
                         ↓
                   ┌───────────┐
                   │  EXECUTE  │ ← 执行生产技能
                   └─────┬─────┘
                         ↓
                  ┌──────────────┐
                  │  VERIFY      │ ← 运行验证技能
                  └──────┬───────┘
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
         PASSED      NEEDS_FIX   FATAL
              │          │          │
              ↓          ↓          ↓
          CONTINUE   AUTO_FIX    STOP
                         │
                    ┌────┴────┐
                    ↓         ↓
                 RETRY    EXHAUSTED
                    │         │
                    ↓         ↓
                 EXECUTE    FATAL
                (重试)     (人工介入)
```

---

## 七、与 Plan Mode 的关系

### 7.1 Plan Mode 是"执行前验证"

```
Plan Mode（执行前）          Verification Loop（执行后）
═══════════════════         ════════════════════════════
用户提出任务                  生产技能执行完毕
  ↓                            ↓
Agent 生成执行计划             验证技能检查结果
  ↓                            ↓
用户审核计划                   失败？→ 自动修复 → 重试
  ↓                            ↓
批准？→ 执行                  通过？→ 继续
拒绝？→ 修改计划
```

### 7.2 两层防线

```
任务输入 → [Plan Mode] → 执行 → [Verification Loop] → 交付
              ↑                      ↑
         执行前验证               执行后验证
         (人验证Agent)           (Agent验证自己)
```

- **Plan Mode**：保护用户 — 确保 Agent 理解了任务才执行
- **Verification Loop**：保护质量 — 确保 Agent 的产出是正确的才交付

---

## 八、最佳实践

### 8.1 什么时候需要 Verification Loop

| 场景 | 需要？ | 理由 |
|------|--------|------|
| 生成代码 | ✅ 必须 | 代码错误会导致系统故障 |
| 修改配置 | ✅ 必须 | 配置错误会导致服务不可用 |
| 生成文案 | ⚠️ 建议 | 文案错误影响品牌但可撤回 |
| 查询数据 | ❌ 不需要 | 只读操作，无副作用 |
| 删除文件 | ✅ 必须 | 不可逆操作，必须验证 |

### 8.2 验证技能的粒度

```
太粗：verify-all（检查一切）     → 职责不清，无法组合
太细：verify-function-name（检查函数名）→ 过度碎片化
合适：verify-types（检查类型系统） → 单一职责，可组合
```

### 8.3 自动修复的边界

```
可以自动修复：
  - lint 错误（格式/风格）
  - 类型标注缺失
  - import 排序
  - 配置语法错误

不应自动修复：
  - 逻辑错误（需理解意图）
  - 安全漏洞（需人工审查）
  - 架构问题（需讨论决策）
  - 业务逻辑错误（需领域知识）
```

### 8.4 重试策略

```python
# 指数退避重试
retry_delays = [0, 1, 3]  # 第一次立即重试，第二次1秒后，第三次3秒后

# 不是无限重试
max_retries = 3  # 最多重试3次

# 超限后降级
if retry_count >= max_retries:
    if severity == "critical":
        return FATAL  # 停止，需人工
    else:
        return WARN  # 记录警告，继续
```

---

## 九、与其他机制的关系

### 9.1 在 Agent 架构中的位置

```
┌──────────────────────────────────────────┐
│              Agent Loop                  │
│                                          │
│   Think → Act → Verify → Observe         │
│            ↑      ↑                      │
│         执行动作  验证结果                 │
│                    │                      │
│              ┌─────┴──────┐               │
│              │ Verify     │               │
│              │ Skills     │               │
│              │ (可编排)    │               │
│              └────────────┘               │
│                                          │
│   Plan Mode（执行前）←→ Verify（执行后）  │
└──────────────────────────────────────────┘
```

### 9.2 与 Reflection 的关系

| 维度 | Reflection（自审） | Verification Loop（验证循环） |
|------|-------------------|---------------------------|
| 本质 | 单步检查 | 可编排的验证技能链 |
| 触发 | 固定在每步之后 | 四种模式灵活触发 |
| 修复 | 只报告问题 | 自动修复 + 重试 |
| 组合 | 不可组合 | 可链式组合 |
| 关系 | Verification Loop 的子集 | Reflection 的超集 |

**结论**：Verification Loop 是 Reflection 的系统化升级。

### 9.3 与 Permission Gate 的关系

```
Permission Gate（权限门控）     Verification Loop（验证循环）
═════════════════════════      ════════════════════════════
执行前检查权限                   执行后检查质量
"能不能做？"                    "做得对不对？"
                              ↑
                    ┌─────────┴─────────┐
                    ↓                   ↓
              权限通过 → 执行       执行完 → 验证
```

两者是互补的：Permission Gate 管"能不能做"，Verification Loop 管"做得对不对"。

---

## 十、总结

### 核心要点

1. **验证是 Agent 循环的内生环节**，不是可选的附加步骤
2. **四种触发模式**覆盖从手动到全自动的全部场景
3. **Generator-Evaluator 分离** — 生成和验证是两个独立技能
4. **自动修复优先** — 验证失败时先尝试自动修复，而非直接报错
5. **严重性分级** — critical/high/medium/low 对应不同处理策略
6. **可组合** — 验证技能可以链式组合，形成端到端验证链
7. **与 Plan Mode 互补** — 执行前验证 + 执行后验证 = 双重防线

### 设计启示

```
没有验证的 Agent              有验证的 Agent
═════════════════            ══════════════════════
执行 → 产出 → 下一步          执行 → 产出 → 验证
                              ↓
可能产出错误结果               通过？→ 下一步
错误一路传播                   失败？→ 修复 → 重验
最终：积重难返                 最终：质量可控
```

---

*本文档为 Claude Blog 学习笔记，记录 Verification Loops 的完整理论体系。*
*来源：https://claude.com/blog/building-verification-loops-in-claude-code-with-skills*
