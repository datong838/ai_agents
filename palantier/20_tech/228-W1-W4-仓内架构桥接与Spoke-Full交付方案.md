# 228-W1-W4 仓内架构桥接与 Spoke Full 交付方案

> 日期：2026-07-31
> Worker：W4 / `aos-platform-w4` / `feature/223-worker-4`
> 基线：`7f6434a`
> 状态：✅ 已完成并合入 `m1`

## 1. 目标

在不开发具体电商接入、不宣称真实多集群舰队已完成的前提下，完成两项通用平台收敛：

1. 让独立克隆仓库具备自包含的架构、边界、开发、测试和外部设计桥接说明。
2. 把 Spoke Full 从不可验证的 stub 收敛为可 lint、可 template、只引用 Secret、具备基础安全/探针/资源/持久化/Ingress 配置面的交付参考 chart。

## 2. 诚实边界

- 本波交付的是 Helm 包格式与静态渲染门，不代表 kind/生产集群安装、Argo 舰队或远程发布已验收。
- 不把 AGPL/BSL 服务端组件或 `deploy/dev` 依赖打入客户 chart。
- values 不保存 Token、密码、私钥或连接串正文，只允许 Kubernetes Secret 名称与 key 引用。
- 不修改 Lite promote/recall、Ferry 签名、Apollo 状态机或具体电商运行时。

## 3. 文件所有权

可修改：

- `README.md`
- 新增 `docs/ARCHITECTURE.md`、`docs/EXTERNAL_DESIGN.md`、`docs/DEPLOYMENT.md`
- `deploy/spoke-full/chart/**`
- 更新既有 `scripts/ci/helm-template-spoke-full.sh`，把“缺 Helm 可跳过、单次渲染”收紧为可要求 Helm、lint、双配置重复渲染与静态安全检查；统一 `scripts/ci.sh` 接线由总控合并阶段完成

禁止修改：

- API、Web、Desktop、Ontology SDK 业务代码
- package manifests / locks
- OpenAPI 契约、CSS/nav
- 外部 `docs/palantier` 大文档正文（仅总控回写 228）

## 4. Chart 最小设计

- `values.schema.json`：校验 image、service、spoke、Secret 引用和可选配置。
- Deployment：readiness/liveness、pod/container securityContext、resources、termination grace、可选 imagePullSecrets。
- ServiceAccount：默认创建，可覆盖名称，默认不挂载 API token。
- Secret：只通过 `existingSecret.name` 与 key 名引用 Hub token/可选外部配置。
- Config：Hub 地址、Spoke ID、Channel、poll 模式保持非敏感 values。
- Persistence：默认关闭；开启时创建 PVC 或引用 existingClaim。
- Ingress：默认关闭，显式 hosts/tls；不生成证书或明文 Secret。
- Service：selector 与 Deployment 标签一致。

## 5. 测试

- 安装固定版本 Helm CLI（环境缺失时主动安装）。
- `helm lint deploy/spoke-full/chart`。
- 默认 values 与一组 production-like override 各执行两次 `helm template`，输出确定。
- 检查渲染 YAML 无明文 Secret、无 `latest`、探针/securityContext/资源齐全。
- 安全扫描源码与渲染产物。
- README/仓内文档链接检查。

## 6. 验收

- [x] 独立克隆用户不依赖父目录文档即可理解架构、边界和测试入口。
- [x] 外部设计文档链接同时提供 monorepo 路径和不可用时替代说明。
- [x] Helm lint 与两组 template 通过且重复渲染一致。
- [x] values 只引用 Secret，不含明文凭据。
- [x] chart 保持 `helm-mock / K8s deferred` 诚实标识。
- [x] 专项扫描、Wave 1 回归与最终 full 门通过。

## 7. 完成证据

- Worker `c354249`，合并 `1290731`；总控 Helm 接线 `e34c66e`。
- Helm v3.18.4 strict lint 通过；默认/production 渲染 SHA-256 分别为 `c1e4b5b9...`、`e98d6277...`，双次渲染一致。
- Deployment/Service/ServiceAccount、探针、资源、安全上下文、可选 Ingress/PVC 与 existingSecret 引用均通过静态断言。
- W4 阶段 wave 8/8、最终 `full` 12/12；源码/产物扫描 critical=0。

## 8. 回滚

W4 独立 commit 回滚即可恢复基线；不执行集群 install、不创建真实 Secret/PVC，不修改任何用户数据。
