# NeoCloud Cyber Security

简体中文 | [English](README.md)

**版本：** `1.0.0-draft.1`  
**基线日期：** 2026-09-04

NeoCloud Cyber Security 是一套面向 AI-first 云基础设施的开放、证据驱动的安全架构与运营模型。

> **NeoCloud Cyber Security 是 NeoCloud 面向 AI-native 组织和专业 AI 云构建的统一网络安全控制平面：以身份为信任根、以策略为决策核心、以 Agent 与工作负载为重点保护对象，通过端点、云原生运行时、网络与高性能互联、数据、软件/模型供应链和安全运营协同，实现从“看见风险”到“实时阻断”和“持续证明”的闭环。**

本项目覆盖完整的 NeoCloud 信任面：人员、租户、AI Agent、工作负载身份、API、控制面、Kubernetes、Slurm、裸金属、虚拟化、GPU/加速器、以太网、InfiniBand/RDMA、数据集、模型、Checkpoint、密钥、固件、BMC、机房以及第三方依赖。

## 仓库交付物

| 交付物 | 中文 | English |
|---|---|---|
| 完整白皮书 | [白皮书](docs/zh-CN/WHITEPAPER.md) | [White Paper](docs/en/WHITEPAPER.md) |
| 安全基线 | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) | [Security Baseline](docs/en/SECURITY_BASELINE.md) |
| 实践指南 | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) | [Practice Guide](docs/en/PRACTICE_GUIDE.md) |
| 参考架构 | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) |
| 发展路线图 | [发展路线图](docs/zh-CN/ROADMAP.md) | [Roadmap](docs/en/ROADMAP.md) |
| 度量与持续证明 | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) |
| 机器可读控制目录 | [控制目录说明](controls/README.md) | [控制目录](controls/neocloud-security-baseline.v1.json)与 [Schema](controls/schema.json) |
| 评估模板 | [模板目录](templates/) | [Templates](templates/) |
| 标准与研究资料 | [参考资料](REFERENCES.md) | [References](REFERENCES.md) |

## 18 个安全域

1. 治理、风险、合规与共享责任
2. 资产、服务、依赖与数据流清单
3. 人员、租户、工作负载与 Agent 身份
4. 控制面、API 与管理接口安全
5. 网络、高性能互联、RDMA/InfiniBand 与 DPU 隔离
6. 计算、虚拟化、裸金属、GPU 与加速器隔离
7. Kubernetes、容器、Slurm 与调度器安全
8. 数据、数据集、模型、制品与隐私保护
9. Secret、密钥、PKI、证明与机密计算
10. 软件、模型与基础设施供应链安全
11. 安全工程、IaC、变更与配置管理
12. 漏洞、暴露面、补丁与固件管理
13. 遥测、检测工程、威胁情报与审计
14. AI 应用、Agent、Tool、Skill 与 Prompt 安全
15. 滥用防护、租户信任、出网与可接受使用
16. 事件响应、取证、危机管理与恢复
17. 韧性、可用性、容量、备份与灾难恢复
18. 物理、机房、BMC、硬件生命周期与介质清除

## 五级采用模型

- **T0—硬门槛：** 服务处理租户数据或开放生产算力前必须满足的不可妥协条件。
- **T1—基础级：** 完整可见性与必要安全卫生，通常在前 90 天完成。
- **T2—生产级：** 支撑规模化、多租户正式商用的策略化和平台化控制。
- **T3—可信级：** 面向敏感、受监管、主权或专属环境的高保证控制。
- **T4—自适应级：** 持续验证、可控自动化、机密计算和带护栏的 AI 辅助防御。

任何综合分数都不能抵消 T0 失败；生产准入必须采用硬门槛和证据判定。

## 核心原则

- **身份优先于网络位置。** 对人员、服务、工作负载、设备、租户和 Agent 统一实施强认证、短期凭据、最小权限与持续评估。
- **隔离是体系属性。** 租户边界必须贯穿 API、计算、存储、以太网、InfiniBand/RDMA、NVLink、调度、可观测性和支持运维。
- **共享责任必须显式。** 每项控制都应明确云服务方、客户方或共同责任方，以及升级路径。
- **证据属于控制本身。** 没有实现范围、覆盖率、时效、责任人、例外和独立验证证据，就不能宣称控制完成。
- **Agent 是高权限软件主体。** Agent 行为必须经过策略、最小权限、审批边界、不可抵赖审计和确定性停止条件约束。
- **恢复本身是安全能力。** 备份、重建、租户退租、数据清除和危机沟通必须通过演练证明。
- **安全默认，而非依赖客户专家能力。** MFA、日志、隔离、安全更新和安全默认配置应由服务提供方内建，而不是收费选件。

## 适用对象与服务类型

本项目适用于 NeoCloud/GPU 云服务商、AI 基础设施团队、主权 AI 运营方、平台工程、安全架构、CISO、审计方、企业采购方及开展供应商尽调的客户。

覆盖 GPU IaaS、裸金属 GPU、托管 Kubernetes、托管 Slurm/HPC、模型训练平台、推理/模型服务平台、Agent 平台以及受监管或主权部署。

## 采用顺序

1. 选择适用服务画像并建立共享责任矩阵。
2. 盘点资产、身份、数据流、信任边界和关键依赖。
3. 基于证据评估 T0/T1，先清零所有生产硬门槛失败项。
4. 将 T2 控制建设为可复用平台能力和 Policy-as-Code。
5. 对高风险服务和客户承诺增加 T3 高保证措施。
6. 只有当自动化行为有边界、可回滚、可观测并可独立验证时，才进入 T4。

## 仓库校验

在仓库根目录运行不依赖第三方包的校验器：

```bash
python3 scripts/validate_repository.py
```

校验内容包括：

- 安全域严格为 18 个，控制严格为 90 项；
- 等级分布严格为 `T0=32`、`T1=31`、`T2=19`、`T3=7`、`T4=1`；
- Control ID 完整、唯一、格式正确；
- 中英文标题和规范要求完整；
- Evidence、Verification、Tier 与 Metric 引用不存在悬空；
- JSON 控制目录与中英文安全基线完全一致；
- Release Version 和必需交付物一致；
- 相对 Markdown Link 有效。

GitHub Actions 会对 Pull Request 与 `main` 运行同一校验。查询方法和变更规则见[控制目录说明](controls/README.md)。

## 状态与边界

本项目是面向实施的行业基线，不是认证、法律意见，也不能替代特定司法辖区的强制要求。外部框架映射仅供参考；组织仍需自行判断适用性，并获得合格的法律、隐私、安全和审计意见。

变更规则见 [GOVERNANCE.md](GOVERNANCE.md)，贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。
