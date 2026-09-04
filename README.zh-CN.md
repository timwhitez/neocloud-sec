# NeoCloud Cyber Security

简体中文 | [English](README.md)

面向专业 AI 云与 GPU 云的厂商中立安全基线、参考架构、发展路线图与实践指南。

**版本：** `1.0.0-draft.1`  
**基线日期：** 2026-09-04  
**状态：** 面向实施的草案

> NeoCloud Cyber Security 是一套用于**设计和运营统一安全控制体系**的参考框架：以身份与委托权限为信任根，以策略为决策机制，把人员、租户、工作负载、设备、模型和 Agent 都作为明确的安全主体，并在完整服务边界内关联预防控制、遥测、响应、恢复、证据和独立验证。

本仓库交付文档、机器可读控制目录、校验逻辑和实施模板。**它不是可直接部署的安全产品，不是认证体系，也不能证明任何服务商已经安全。**

本文将 “NeoCloud” 作为一个行业工作术语，用来描述主要承载加速器密集型 AI 与 HPC 工作负载的专业云服务商；项目不假定该术语已经存在唯一、正式、监管认可或普遍接受的定义。

## 从这里开始

| 目标 | 推荐入口 |
|---|---|
| 理解 NeoCloud 安全问题和运营模型 | [白皮书](docs/zh-CN/WHITEPAPER.md) |
| 按最低安全结果评估具体服务 | [安全基线](docs/zh-CN/SECURITY_BASELINE.md)和[基线评估模板](templates/baseline-assessment.csv) |
| 将要求转化为工程和运营工作 | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) |
| 设计信任区、策略点、证据流和恢复边界 | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| 制定 0–24 个月建设计划 | [发展路线图](docs/zh-CN/ROADMAP.md) |
| 定义准入门、证据、指标和独立保证 | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| 将控制目录接入内部工具 | [机器可读控制目录](controls/neocloud-security-baseline.v1.json)和 [Schema](controls/schema.json) |

建议第一轮按以下顺序执行：

1. 选择一个或多个服务画像，并定义准确的生产边界。
2. 明确服务商、客户和共同责任。
3. 使用当前、范围明确的证据评估全部适用 T0 和 T1。
4. 对任何失败、未知、证据过期、无法判定或未测试的适用 T0，阻断上线或移除相关暴露。
5. 将 T2 建设为平台能力，按承诺增加 T3，并且只有在权限与失败模式被证明后才引入 T4 自适应自动化。

## 仓库交付物

| 交付物 | 中文 | English |
|---|---|---|
| 完整白皮书 | [白皮书](docs/zh-CN/WHITEPAPER.md) | [White Paper](docs/en/WHITEPAPER.md) |
| 安全基线 | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) | [Security Baseline](docs/en/SECURITY_BASELINE.md) |
| 实践指南 | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) | [Practice Guide](docs/en/PRACTICE_GUIDE.md) |
| 参考架构 | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) |
| 发展路线图 | [发展路线图](docs/zh-CN/ROADMAP.md) | [Roadmap](docs/en/ROADMAP.md) |
| 度量与持续证明 | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) |
| 机器可读控制 | [控制目录说明](controls/README.md) | [控制目录](controls/neocloud-security-baseline.v1.json)、[Schema](controls/schema.json) |
| 评估与运营模板 | [模板目录](templates/) | [Templates](templates/) |
| 标准与研究依据 | [参考资料](REFERENCES.md) | [References](REFERENCES.md) |

## 适用范围

项目覆盖服务商运营及面向客户的以下信任边界：

- GPU IaaS 与裸金属 GPU；
- 托管 Kubernetes 与托管 Slurm/HPC；
- 模型训练、模型服务与 Agent 平台；
- 主权或受监管服务画像；
- 人员、租户、工作负载、设备、服务和 Agent 身份；
- API、控制面、调度器、Host、加速器、存储、以太网、InfiniBand/RDMA、NVLink 感知放置、DPU、BMC/OOB、机房和供应商；
- 数据集、Prompt、输出、模型、Checkpoint、Embedding、Cache、密钥、软件、固件和安全证据。

本基线不能替代服务特定的威胁建模、真实部署路径测试、合同责任、适用法律、隐私/安全评估或合格独立审计。

## 安全模型

基线包含 **18 个安全域、90 项控制**：

| 治理与可见性 | 平台与工作负载保护 | 运营与保证 |
|---|---|---|
| 治理、风险、合规与共享责任 | 网络、Fabric、RDMA/InfiniBand 与 DPU 隔离 | 安全工程、IaC、变更与配置 |
| 资产、服务、依赖与数据流清单 | 计算、虚拟化、裸金属、GPU 与加速器隔离 | 漏洞、暴露面、补丁与固件管理 |
| 人员、租户、工作负载与 Agent 身份 | Kubernetes、容器、Slurm 与调度安全 | 遥测、检测工程、威胁情报与审计 |
| 控制面、API 与管理接口安全 | 数据、数据集、模型、制品与隐私保护 | 滥用防护、租户信任、出网与可接受使用 |
| Secret、密钥、PKI、证明与机密计算 | 软件、模型与基础设施供应链安全 | 事件响应、韧性、恢复、物理和硬件生命周期 |
| AI 应用、Agent、Tool、Skill 与 Prompt 安全 |  |  |

五级采用模型为：

- **T0—硬门槛：** 生产准入硬门。每个适用 T0 都必须被独立验证为 `VERIFIED`；任何例外或综合分数都不能把未满足的 T0 变成符合项。
- **T1—基础级：** 建立责任、清单、基本安全卫生、可见性、响应与恢复基础。
- **T2—生产级：** 支撑可持续多租户运营的可复用、策略化、可度量控制。
- **T3—可信级：** 在承诺需要时，为敏感、监管、主权、专属、证明或机密计算画像提供可独立支持的高保证控制。
- **T4—自适应级：** 在权限、审批、停止、回滚、Trace 和 Verifier 已被证明后，引入受控自适应自动化与持续验证。

高管可以批准限时的紧急业务决定，但该决定**不会**将失败 T0 变为 `VERIFIED`，也不能将相关服务表述为符合本基线。

## 核心原则

- **身份优先于网络位置。** 主体应具有强、受限、可复核的身份；在技术可行时，凭据、会话和委托权限应短期化。
- **隔离是体系属性。** 租户边界必须贯穿 API、计算、加速器显存与故障域、存储、以太网、InfiniBand/RDMA、NVLink 拓扑、调度、遥测和支持运维。
- **共享模式不等价。** 整卡独占、硬件分区、虚拟化与 Time-slicing 必须分别声明和测试；Time-slicing 不能作为显存或故障隔离边界。
- **共享责任必须显式。** 每项控制都应明确服务商、客户或共同责任方，并具备升级路径。
- **证据属于控制本身。** 已部署不等于已有效；还需要范围、负向测试、失败行为、恢复与独立验证。
- **Agent 权限按风险治理。** 每个生产 Agent 都需要清单和边界；高影响或自适应工作流还需要确定性审批/停止、受保护 Trace 和独立验证。
- **恢复要恢复信任，而不只是恢复可用性。** 重新开服前必须检查身份、制品、租户隔离、数据完整性和监控。
- **安全默认属于服务商责任。** 服务商独占控制的能力不能通过文档转嫁给客户。

## 控制状态与证据

唯一正常完成路径为：

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

只有独立验证者针对明确的服务、版本、Region、租户/资产范围、测试和证据有效期返回 `PASS`，才能进入 `VERIFIED`。

## 仓库校验

在仓库根目录运行不依赖第三方包的校验器：

```bash
python3 scripts/validate_repository.py
```

校验内容包括：

- 安全域严格为 18 个，控制严格为 90 项；
- 等级分布严格为 `T0=32`、`T1=31`、`T2=19`、`T3=7`、`T4=1`；
- Control ID 完整、唯一且格式正确；
- 中英文标题与规范要求完整；
- Evidence、Verification、Tier 与 Metric 引用不存在悬空；
- JSON 控制目录与中英文安全基线一致；
- Release Version 与必需交付物一致；
- 相对 Markdown Link 有效。

同一校验会通过 [GitHub Actions](.github/workflows/validate.yml)在 Pull Request 和 `main` 上运行。

## 项目治理与状态

- 贡献规则：[CONTRIBUTING.md](CONTRIBUTING.md)
- 控制和证据治理：[GOVERNANCE.md](GOVERNANCE.md)
- 安全问题报告：[SECURITY.md](SECURITY.md)
- 推荐的 GitHub About、Topics 与仓库设置：[.github/REPOSITORY_SETTINGS.md](.github/REPOSITORY_SETTINGS.md)
- 变更历史：[CHANGELOG.md](CHANGELOG.md)

本仓库当前没有授予开源许可证。在对外公开或允许外部复用前，Owner 应选择并添加明确 License；建议决策方案已写入仓库设置指南。
