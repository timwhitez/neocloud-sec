# NeoCloud Cyber Security 范围与局限

**版本：** 1.0.0-draft.2  
**基线日期：** 2026-09-04

## 1. 本项目是什么

NeoCloud Cyber Security 是由本项目定义、保持厂商中立的专业 AI/GPU 云安全参考基线与实施指南，提供控制目录、证据模型、验证方法、参考架构、路线图、指标和实施模板。

它不是已经部署的软件产品、被行业正式采纳的标准、认证体系或经过认可机构认证的控制框架。“NeoCloud” 在本文中是操作性术语，不同服务商可能采用不同商业和技术定义。

## 2. 规范范围

在本仓库内部，机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)是 Control ID、Tier、中英文要求、Evidence Profile、Verification Profile 和 Metric Reference 的权威来源；其他文档负责解释与落地。

对于真实服务，优先级依次受适用法律、监管要求、合同和客户承诺，以及已记录的服务边界和适用性决定约束。本项目不能替组织作出法律或合同适用性结论。

## 3. 项目定义的硬门与目标

五级模型、18 个安全域、90 项控制、T0 生产门、复核频率、路线图日期和数值目标都是本项目的设计选择，目的是提供保守、可测试的规划默认值，并不表示外部标准组织或行业已认可这些准确数值。

任何失败、未知、过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的适用 T0 都不能被标记为符合。紧急偏离可以在授权后限时维持服务，但仍必须明确标记为“不符合”，并且在独立验证前不得进入 `PASS` 或 `VERIFIED`。

## 4. 技术特定局限

安全属性必须在准确部署栈上验证。

- **GPU 共享：** 整卡专属、硬件分区、受 Hypervisor 仲裁的 vGPU 和调度器级 Time-slicing 是不同机制。Kubernetes GPU 调度器级 Time-slicing 本身不提供显存或故障隔离；受支持的 vGPU 和硬件分区模式可能具有不同属性。名称本身不能证明隔离。
- **加速器清理：** GPU/HBM/Cache/Reset 行为与设备、模式、Driver、Firmware、Hypervisor 和 Workload 有关。传统介质清除指南不能自动证明易失加速器状态已经清理。
- **InfiniBand/RDMA：** P_Key 提供 Partition Membership 语义，但完整隔离还依赖 Membership Type、Default Partition、Fabric Manager 权限、DPU/NIC/Storage 配置、Controller 对账和真实负向路径测试。
- **NVLink/NVSwitch：** Topology-aware Placement 与 Domain Assignment 是实现输入；“NVLink Domain” 标签本身不是租户安全边界。
- **Kubernetes：** 托管服务面向客户的 API Endpoint 不必在所有场景绝对私有，但服务商专用 Controller 和 Database 必须受保护。公网 Endpoint 需要显式、加固且抗滥用的服务画像。
- **Slurm：** Account、Partition、QOS、Association 与 MCS Label 可以治理调度和可见性，但不能替代 OS/Runtime、Credential、Storage、Network/Fabric 与 Node 控制。
- **Attestation 与 Confidential Computing：** Attestation 只在特定 Root 与 Policy 下报告 Measured State，不能单独证明 Application Behavior、端到端机密性、Key Release 正确或不存在 Side Channel。
- **供应链签名：** 有效签名只证明某个 Key 签过制品；安全性还依赖 Source、Build/Training Lineage、Key Custody、Policy、Vulnerability State、Review 和 Revocation。
- **证据分离：** 独立保护是信任与管理分离要求，并不总是要求物理独立平台。

## 5. 共享责任与商业边界

服务商仍对自己独占运营的基础设施控制负责；客户仍对客户控制的代码、数据分类、租户角色、Guest 配置及合同约定的其他责任负责。责任必须按具体服务和事件阶段精确定义。

安全默认不意味着所有 SKU 完全相同。服务商可以提供更高保证的 Dedicated、Sovereign、Attested 或 Confidential Computing 服务，但必须准确说明基础 SKU 能保护什么、不能保护什么。

## 6. 证据与保证局限

仓库 Validator 只能证明结构一致，不能证明实际部署安全。Policy、Screenshot、Vendor Dashboard、Attestation、Signature 或通过 CI 都不能单独构成充分证据。证据必须范围明确、当前有效、受保护、尽可能可复现，并针对正常路径与禁止路径接受独立验证。

外部框架引用和映射仅供参考。正式合规或认证需要针对准确框架版本、司法辖区、审计目标、服务范围和证据，由合格评估方完成。

## 7. 发布与 License

当前版本的 GitHub 仓库是 Private，且尚未选择 License，因此不能把内容描述为 Open Source 或 Openly Licensed。公开发布前，Owner 应选择适合文档、控制数据、代码和贡献规则的 License，复核第三方引用和 Trademark 限制，并启用适当的私密漏洞报告路径。

参见[项目元数据](../../PROJECT_METADATA.md)、[安全报告规则](../../SECURITY.md)、[准确性审计](../../ACCURACY_REVIEW.md)和[参考资料](../../REFERENCES.md)。
