# 228 · AIP Assist 建议契约与空白页修复方案

> 版本：v1.0（2026-08-01）
> 状态：已完成
> 页面：`/aip/assist`
> 产品依据：`02-四大金刚与子产品拆解.md` 模块 2.4、`07-AIP引擎k-LLM与AgentStudio产品方案.md`、`AIP/assist/aip-best-practices.md`

## 1. 使用 Rules

1. 先复核产品定位、前后端契约和浏览器错误，再编码。
2. 只修建议问题契约不一致导致的空白页，不借机重构对话、SSE 或持久化逻辑。
3. 页面必须兼容当前后端对象 DTO 与历史字符串 DTO；无效项过滤、重复项去重，空结果回到明确的内置建议。
4. 新增纯函数契约测试和真实组件渲染测试；专项通过后再做 Web 类型检查与浏览器回归。
5. 页面不得因单个建议项格式异常整页崩溃，也不得把对象直接作为 React child/key。

## 2. 现状与根因

浏览器访问 `/aip/assist` 后整页空白。控制台确认 React 抛出：`Objects are not valid as a React child (found: object with keys {id, category, text})`，并伴随重复 key。

前端把 `GET /v1/aip/assist/suggestions` 声明为 `items?: string[]`，直接存入 `string[]` 并渲染；后端实际返回 `[{id, category, text}]`。TypeScript 的静态泛型没有运行时校验，因此接口成功反而触发渲染崩溃。

## 3. 最小修复

1. 在 `AipAssistPage.tsx` 增加建议项运行时归一化函数：接受 `unknown`，只提取字符串项或对象的非空 `text`。
2. 按建议文本稳定去重，避免重复 key；无效或空数组继续使用现有上下文/默认建议。
3. API 读取类型改为 `unknown`，只有归一化成功后才进入页面状态。
4. 保持按钮行为、建议回填、SSE、localStorage 与权限逻辑不变。

## 4. 文件范围

- `aos-platform/apps/web/src/pages/s2/AipAssistPage.tsx`
- `aos-platform/apps/web/src/pages/s2/AipAssistPage.test.ts`
- `aos-platform/apps/web/src/pages/s2/AipAssistPageInteractions.test.tsx`（新增）

不修改后端 DTO：当前对象 DTO 自身包含稳定 ID、分类和文本，且已有后端测试；本次由消费端按真实契约兼容。

## 5. 验收门

1. 归一化测试覆盖对象数组、历史字符串数组、非法项、空文本和重复文本。
2. 组件测试模拟真实后端对象 DTO，页面可渲染、展示建议文本、点击后写入输入框，且不出现对象子节点崩溃。
3. AIP Assist 专项测试、Web typecheck 通过。
4. 浏览器强制刷新后页面非空，建议按钮可点击，输入框得到文本；控制台无 React child/key 错误。
5. 最终更新本文状态、测试与浏览器证据。

## 6. 风险与回滚

- 风险：未来 DTO 改字段名时会过滤为默认建议，但不会整页崩溃，属于 fail-soft。
- 回滚：只需回退页面归一化及对应测试；不涉及数据库、后端状态或用户数据迁移。

## 7. 完成证据

1. 新增 `normalizeSuggestionItems`，兼容对象/字符串 DTO，过滤非法项并按文本去重。
2. 专项测试：`2 files / 21 tests` 通过；Web 全量回归：`102 files / 1672 tests` 通过。
3. Web typecheck 通过；production build `198 modules` 通过。
4. 浏览器强制刷新 `/aip/assist` 后页面完整显示；真实 12 条对象建议均正确渲染为文本，点击“今天有哪些数据流出现了延迟？”后输入框正确回填。
5. 本次刷新后的 `Objects are not valid as a React child` 与重复 key 错误均为 0；仅保留项目既有 React Router v7 future flag 提示。
