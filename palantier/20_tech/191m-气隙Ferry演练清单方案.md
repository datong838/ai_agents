# 191m · 气隙 Ferry 演练清单（不代签收）

> **版本**：v1.2 · 2026-07-20  
> **状态**：✅ **已编码**（M1-W4b）· 自测通过  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[162](162-Ferry现场加严MVP方案.md)  
> **边界**：≠ 客户气隙 Full Channel 签收  
> **落点**：`scripts/ci/drill-ferry-airgap.sh` · `deploy/dev/_ferry_drill/` · `tests/test_w4_190_191_192m.py`

## 已决

聚合脚本 `scripts/ci/drill-ferry-airgap.sh`：

1. （可选）curl Ferry status  
2. 既有探针：large-images / skopeo / cosign（缺工具 SKIP）  
3. 写报告 `deploy/dev/_ferry_drill/<ts>.md`  
4. 文首声明「演练 ≠ 签收」

不改 `ferry.py` 默认行为。

## 自检

- [x] `--help` 含不代签收  
- [x] 无 Docker 时 SKIP 仍 exit 0（默认；`--skip-curl` 可测）  
- [x] `--require-report` 必写报告文件  
- [x] pytest 编排钩子  

---

*v1.2 · 191m · 已编码*
