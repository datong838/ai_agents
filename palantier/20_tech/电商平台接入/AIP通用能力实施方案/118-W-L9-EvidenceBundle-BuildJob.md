# 118 · W-L9 EvidenceBundle Build Job + 服务端 coverage

> 状态：`DRAFT` · 2026-08-20  
> 清单：`59` §8.5 / §10.4 **W-L9**  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l9-evidence-build-job/`（待封板）  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 目标

1. 服务端 **Build Job** 产出 EvidenceBundle revision（禁调用方直填冒充 Bundle）
2. `required-facts` **coverage 服务端计算**（missing / conflicts / uncertainties）
3. 客户端只能提交 Job 输入与 exact 引用；coverage/freshness 由权威回填

## 2. 不做

- 完整三层 Disclosure/Marking 执行 API（W-L10）
- 伪造 facts / Mock Bundle 种子进权威租户

## 3. 现状（待勘察确认）

- 已有 `CreateEvidenceBundleRequest` / store create 路径；需确认是否允许客户端直填 `coverage`/`missing`
- 若已有直填：收紧为 Job 产出 + 服务端 coverage；保留只读 GET

## 4. 最小改动（拟定）

| 面 | 说明 |
|---|---|
| contracts | `EvidenceBuildJobRequest/Result` 或收紧 Bundle create |
| store | 服务端算 coverage；Job 幂等 |
| tests | 直填 coverage 被拒；Job 产出与 required-facts 一致 |

## 5. 验收

- 调用方无法用自填 coverage 冒充 complete
- Job 幂等；缺 facts → coverage=blocked/partial + missing 诚实

## 6. 风险

旧客户端若依赖直填 coverage 会 fail-closed——符合 W-L9。
