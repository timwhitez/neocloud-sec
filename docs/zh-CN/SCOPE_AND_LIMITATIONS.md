# NeoCloud Cyber Security 范围与局限

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 项目编制的实施草案

## 1. 本项目是什么

NeoCloud Cyber Security 是面向专业 AI/GPU 云服务、保持厂商中立的参考基线与实施指南，提供中英文控制目录、证据与验证模型、参考架构、路线图、指标、治理规则和实施模板。

它**不是**已经部署的软件产品、被行业正式采纳的标准、认证体系、经认可机构认可的控制框架，也不能证明任何服务商已经安全。“NeoCloud” 在本文中是面向高强度 AI/HPC 加速器工作负载专业云服务的工作术语，不同服务商可能使用不同商业与技术定义。

## 2. 规范范围

在本仓库内部，机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)是 Stable Control ID、Tier、中英文要求、Evidence Profile、Verification Profile 和 Metric Association 的权威来源。安全基线解释生产硬门和服务画像，其他文档负责将目录转化为工程与运营工作。

对于真实服务，外部义务由适用法律、监管要求、合同、客户承诺、已记录服务边界和合格的适用性决定共同确定。本项目不能替采用方作出法律、隐私、安全、合同或认证结论。

## 3. 项目定义的硬门与目标

五级模型、18 个安全域、90 项控制、T0 生产硬门、默认验证频率、路线图日期和数值目标都是本项目的设计选择。它们是保守的规划默认值与可测试运营规则，并不表示外部标准机构或行业已经认可这些准确数值。

任何失败、未知、过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的适用 T0 都保持 `NO_GO_NONCONFORMANT`。经法律和组织授权的紧急业务连续性决定可以在本基线符合性结论之外限时维持服务，但不能形成 `PASS`、`VERIFIED` 或符合性声明。

## 4. 技术特定局限

安全属性必须在准确部署栈上验证。

- **GPU 共享：** 整卡独占、硬件分区、受 Hypervisor 仲裁的 vGPU 与调度器级 Time-slicing/超卖是不同机制。Kubernetes GPU 调度器级 Time-slicing 本身不提供显存或故障隔离；受支持的 vGPU 和硬件分区模式可能具有不同、绑定产品的属性。名称本身不能证明隔离。
- **加速器清理：** GPU/HBM/Cache/Reset 行为与 Device、Mode、Firmware、Driver、Hypervisor、Error State 和 Workload 有关。传统介质清除指南不能自动证明易失加速器状态已经清理。如果无法建立可辩护的跨租户清理声明，可能必须 Quarantine、退役或 Dedicated Allocation。
- **InfiniBand/RDMA：** P_Key 提供 Partition Membership 语义，不是完整隔离证明。有效性还依赖 Membership Type、Default Partition、Fabric Manager 权限、DPU/NIC/Storage 配置、Topology、Endpoint Behavior、Controller Reconciliation、Stale-state Handling 和真实路径负向测试。
- **NVLink/NVSwitch：** Topology-aware Placement 与 Domain Assignment 是实现输入；“NVLink Domain” 标签本身不是租户安全边界。
- **Kubernetes：** 服务商专用 Controller 与 Database 应保持私有。面向客户的托管 API Endpoint 可以通过公网 Edge 提供，但必须经过显式批准，并实施强认证、来源/速率限制、DDoS 防护、抗滥用和完整审计。
- **Slurm：** Account、Association、Partition、QOS、Reservation 与 MCS Label 可以治理调度和可见性，但不能替代 OS/Runtime、Credential、Storage、Network/Fabric 与 Node Enforcement。
- **Attestation 与 Confidential Computing：** Attestation 只在特定 Product、Root、Policy、Nonce/Freshness Model 和 Configuration 下报告 Measured Claim，不能单独证明 Application Behavior、端到端机密性、Key Release 正确或不存在 Side Channel。
- **供应链签名：** 有效签名只证明某个 Key 签过制品；安全性仍取决于 Source、Build/Training Lineage、Key Custody、Compatibility、Policy、Review、Vulnerability State、Admission、Revocation 和 Recall。
- **证据独立性：** 独立保证需要足够的组织与观察分离，使验证者能够挑战实施者；并不普遍要求单独的物理平台。

## 5. 共享责任与商业边界

服务商仍对其独占运营的基础设施控制负责；客户仍对客户控制的代码、数据分类、租户角色、Guest 配置和合同规定的其他责任负责。责任必须按具体服务、服务等级和事件阶段精确定义。

安全默认不意味着所有 SKU 具有相同保证。服务商可以提供 Dedicated、Sovereign、Attested 或 Confidential Computing 服务，但必须准确说明基础级与高保证级分别保护、共享和排除什么，以及客户需要承担什么。

## 6. 证据与保证局限

仓库 Validator 通过只能证明结构一致，不能证明真实部署安全。Policy、Screenshot、Vendor Dashboard、Scanner Result、Signature 或 Attestation 都不能单独构成充分证据。证据必须当前有效、范围明确、受保护、尽可能可复现、关联真实部署路径，并针对相关允许、禁止、失败、撤销、恢复与清理路径接受独立验证。

外部框架引用和映射仅供参考。正式合规或认证需要针对准确框架版本、司法辖区、审计目标、服务范围和证据，由合格评估方完成。

## 7. 发布与 License

当前版本的 GitHub 仓库是 Private，且尚未选择 License，因此不能把内容描述为 Open Source 或 Openly Licensed。公开发布前，Owner 应选择适用于文档、结构化控制数据、脚本、Schema 和贡献的 License，复核第三方引用与 Trademark 约束，清除敏感材料，并建立受支持的私密报告路径。

即使添加到 Private Repository，GitHub Topic 名称也始终公开。建议 Description、Topics、发布检查与管理防护见[仓库设置建议](../../.github/REPOSITORY_SETTINGS.md)。

参见[准确性审计](../../ACCURACY_REVIEW.md)、[安全问题报告](../../SECURITY.md)和[参考资料](../../REFERENCES.md)。
