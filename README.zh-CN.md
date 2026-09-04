# NeoCloud Cyber Security

简体中文 | [English](README.md)

面向专业 AI/GPU 云的厂商中立安全基线、参考架构、路线图与实践指南。

**版本：** `1.0.0-draft.1`  
**基线日期：** 2026-09-04  
**最新公开问题审计：** 2026-09-05  
**状态：** 面向实施的项目草案

> NeoCloud Cyber Security 是用于设计和运营 AI 基础设施安全控制的参考框架：以身份和委托权限作为信任根，以策略作为决策机制，将人员、租户、工作负载、设备、模型和 Agent 视为明确的安全主体，并贯通预防控制、遥测、响应、恢复、证据与独立验证。

本仓库包含文档、机器可读控制目录与画像、本地校验逻辑和实施模板。**它不是可部署的安全产品、行业已采纳标准、认证体系、ClusterMAX 评级，也不能证明任何服务商已经安全。**

“NeoCloud”在本项目中是面向加速器密集型 AI/HPC 工作负载专业云服务商的行业工作术语；本项目不假定它具有唯一正式或监管定义。

## 从这里开始

| 目标 | 入口 |
|---|---|
| 理解安全问题与运营模型 | [白皮书](docs/zh-CN/WHITEPAPER.md) |
| 评估最低安全结果 | [安全基线](docs/zh-CN/SECURITY_BASELINE.md)与[基线模板](templates/baseline-assessment.csv) |
| 将要求转化为工程与运营任务 | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) |
| 设计信任区、策略、证据与恢复边界 | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| 规划 0–24 个月建设 | [发展路线图](docs/zh-CN/ROADMAP.md) |
| 定义硬门槛、指标和独立保证 | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| 核查 SemiAnalysis / ClusterMAX 公开安全问题 | [覆盖审计](docs/zh-CN/SEMIANALYSIS_COVERAGE.md)、[40 项问题评估](templates/semianalysis-public-findings-assessment.csv)和[公开 Security 页面 20 项评估](templates/clustermax-public-security-requirements-assessment.csv) |
| 将控制接入工具 | [核心目录](controls/neocloud-security-baseline.v1.json)、[公开问题画像](controls/semianalysis-public-findings-profile.v1.json)、[规范勘误](controls/neocloud-security-baseline.v1.errata.json)及 Schema |

建议第一轮：

1. 明确 Service、Region、Cluster、SKU、Hardware 和真实部署版本边界；
2. 分配 Provider、Customer 与 Shared Responsibility，但不得把 Provider-exclusive Root 转嫁给客户；
3. 使用当前且范围明确的证据评估所有适用 T0/T1；
4. 对重大隔离声明分别执行客户黑盒、服务商白盒和独立故障/恢复测试；
5. 将任何失败、未知、过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的适用 T0 视为 `NO_GO_NONCONFORMANT`；
6. 将 T2 平台化，按承诺增加 T3，只有在 Approval、Stop、Rollback、Trace 与 Verifier 被证明后才采用 T4。

## 交付物

| 交付物 | 中文 | English |
|---|---|---|
| 白皮书 | [中文](docs/zh-CN/WHITEPAPER.md) | [English](docs/en/WHITEPAPER.md) |
| 安全基线 | [中文](docs/zh-CN/SECURITY_BASELINE.md) | [English](docs/en/SECURITY_BASELINE.md) |
| 实践指南 | [中文](docs/zh-CN/PRACTICE_GUIDE.md) | [English](docs/en/PRACTICE_GUIDE.md) |
| 参考架构 | [中文](docs/zh-CN/REFERENCE_ARCHITECTURE.md) | [English](docs/en/REFERENCE_ARCHITECTURE.md) |
| 路线图 | [中文](docs/zh-CN/ROADMAP.md) | [English](docs/en/ROADMAP.md) |
| 度量与持续证明 | [中文](docs/zh-CN/METRICS_AND_ASSURANCE.md) | [English](docs/en/METRICS_AND_ASSURANCE.md) |
| SemiAnalysis 公开问题覆盖 | [中文](docs/zh-CN/SEMIANALYSIS_COVERAGE.md) | [English](docs/en/SEMIANALYSIS_COVERAGE.md) |
| 机器可读控制 | [核心目录](controls/neocloud-security-baseline.v1.json)和[规范勘误](controls/neocloud-security-baseline.v1.errata.json) | [目录说明](controls/README.md) |
| 互操作覆盖层 | [公开问题画像](controls/semianalysis-public-findings-profile.v1.json) | [入口说明](SEMIANALYSIS_COVERAGE.md) |
| 实施模板 | [模板](templates/) | [Templates](templates/) |
| 来源与边界 | [参考资料](REFERENCES.md)和[范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) | [Scope](docs/en/SCOPE_AND_LIMITATIONS.md) |

## 安全模型

稳定核心包含 **18 个安全域、90 项控制**和五级采用模型：

- **T0—硬门槛：** 所有适用 T0 必须被独立验证为 `VERIFIED`；
- **T1—基础级：** Owner、清单、基础卫生、可见性、响应与恢复；
- **T2—生产级：** 可复用、策略化且可度量的多租户生产控制；
- **T3—可信级：** 面向敏感、受监管、主权、专属、Attested 或 Confidential Computing 服务的高保证控制；
- **T4—自适应级：** 在权限与失败模式被证明后采用带护栏的自适应自动化与持续验证。

控制状态：

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

只有独立验证者针对准确 Service、Environment、Version、Scope 与 Evidence Validity 返回 `PASS`，才可赋予 `VERIFIED`。

## SemiAnalysis / ClusterMAX 公开覆盖

独立互操作画像目前映射：

- **5 类公开文章高层问题，由本项目拆分为 40 项原子测试模式**；
- **主站公开 ClusterMAX Security 页面当前可枚举的 20/20 项要求**；
- InfiniBand 管理/服务密钥、SR-IOV QP0/MAD 限制、BlueField/RShim、vCluster/共享节点、Kubelet、Prometheus/Grafana 租户隔离、Provider-wide Root Key、动态最低安全版本、漏洞披露、敌意 Renderer/Cache、推理响应供应链风险及三视角保证等显式检查。

审计截止时，另一个 ClusterMAX Host 报告 21 项 Security Criteria，但额外一项无法被独立枚举，因此项目**不声明 21/21、不声明与 ClusterMAX 精确等价，也不生成评级、认证或背书**。ClusterMAX 还包含本网络安全项目不会复刻的非安全评级维度。

[v1 规范勘误](controls/neocloud-security-baseline.v1.errata.json)细化了 `NCS-CMP-02`：整卡独占、硬件分区、Hypervisor 仲裁 vGPU 和基于裸 Device Plugin 的调度器级 Time-slicing 是不同机制。Kubernetes GPU Operator Time-slicing 的 Replica 间没有显存/故障隔离；受仲裁 vGPU 的声明则必须绑定产品、版本与配置验证。

## 核心原则

- **身份优先于位置。** 技术可行时让 Credential、Session、Privilege Grant 与 Delegated Authority 短期化；
- **隔离必须逐路径证明。** 分别验证 API、Compute、Accelerator Memory/Fault、Storage、Ethernet、RDMA/InfiniBand、DPU、Scheduler、Telemetry、Support 与 OOB；
- **共享模式不等价。** 整卡、硬件分区、受仲裁 vGPU 与调度器级 Time-slicing 是不同产品；
- **Provider-exclusive Root 始终由服务商负责。** Control Plane、Host/GPU Reset、Fabric Manager、BMC/OOB 和 Provider Signing/Key Root 不能通过文档转嫁；
- **证据属于控制。** 已部署不等于有效，禁止路径、失败行为、恢复与独立复现同样重要；
- **模型输出不授予权限。** 外部内容和推理响应是不可信建议，Typed Tool 与 Local Policy 决定动作；
- **恢复要恢复信任。** 重新开服需验证 Identity、Artifact、Tenant Isolation、Data Integrity 与 Monitoring。

## 本地校验

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_accuracy_invariants.py
python3 scripts/validate_semianalysis_profile.py
```

校验器检查稳定的 18 域/90 控制契约、中英文一致性、交叉引用、版本、链接、模板语义、10 维/40 项公开问题画像、主站公开 Security 页面 20 项映射及当前规范勘误。

## 治理与 License

- [贡献规则](CONTRIBUTING.md)
- [控制与证据治理](GOVERNANCE.md)
- [安全问题报告](SECURITY.md)
- [准确性审计](ACCURACY_REVIEW.md)
- [GitHub 设置建议](.github/REPOSITORY_SETTINGS.md)
- [变更历史](CHANGELOG.md)

当前没有授予开源 License。公开发布或外部复用前，Owner 应选择并添加明确 License。
