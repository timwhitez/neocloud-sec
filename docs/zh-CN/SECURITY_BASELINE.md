# NeoCloud Cyber Security 安全基线

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 面向实施的项目草案  
**规范性机器可读目录：** [`controls/neocloud-security-baseline.v1.json`](../../controls/neocloud-security-baseline.v1.json)

## 1. 目的、范围与规范语言

本基线定义由本项目制定的最低网络安全结果，适用于 GPU IaaS、裸金属 GPU、托管 Kubernetes、托管 Slurm/HPC、模型训练、模型服务、Agent 平台以及主权/监管 NeoCloud 服务。

- **必须**表示对适用服务范围的强制要求。
- **应该**表示强建议；省略时必须记录理由和剩余风险 Owner。
- **可以**表示一种实现选项。
- 适用性决定必须说明准确的服务边界、资产/租户范围、理由、Owner、复核者、证据和重新验证触发条件。“没有实施”不等于“不适用”。
- 外部框架映射仅供参考，不构成认证、法律合规、真实部署有效或精确控制等价。

本基线包含 **18 个安全域、90 项控制**。JSON 目录是稳定 Control ID、中英文规范要求、等级、默认验证频率、证据/验证画像和指标关联的权威来源。本文解释评估、生产硬门、安全域结果和服务画像叠加要求。若解释性正文与目录冲突，在冲突被修复前，以目录和[治理规则](../../GOVERNANCE.md)为准。

本文将 “NeoCloud” 作为行业工作术语，用来描述主要承载加速器密集型 AI 与 HPC 工作负载的专业云服务商；不将其视为已经正式标准化或被监管定义的服务类别。

## 2. 评估生命周期

每个服务应选择一个或多个 Service Profile，并评估所有控制。评估记录至少包含：

- Service、Profile、Environment、Region、Version、Asset/Tenant 与 Data Scope；
- Applicability 及其理由；
- 可追责的 Provider、Customer 或 Shared Owner；
- Implementation State 与依赖；
- Evidence ID、来源、采集方法、有效期和完整性保护；
- Test Method，以及适用时的禁止路径或失败行为；
- Independent Validator 与 Verification Result；
- Exception 或 Business-risk Decision、Residual Risk、Customer Impact 与 Target Date。

唯一正常完成路径为：

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

- `READY` 要求范围、可追责 Owner、要求、依赖、目标日期、失败行为、证据契约和测试方法完整。
- `IMPLEMENTED` 表示机制已经部署到声明范围，但不证明其有效。
- `CANDIDATE_DONE` 表示 Owner 已经提交当前证据并主张完成。
- 只有独立验证者针对准确范围返回 `PASS`，才能进入 `VERIFIED`。
- `FAIL`、`INCONCLUSIVE`、`NOT_TESTED`、证据过期、重大变更或无法复现断言，都会使 `VERIFIED` 失效，并退回相应更早状态。

Policy、访谈、Screenshot、Scanner Result、Vendor Dashboard、Signature 或 Attestation 都可能贡献证据，但不会自动充分。优先使用可复现 API/Query Export、Policy/Authorization Decision、受保护或可发现篡改的 Runtime Event、验证了 Claim 与 Freshness 的 Signed Attestation、Desired/Actual Reconciliation、Negative-path Test、Revocation/Restore/Rebuild/Sanitization Trace、Hash，以及来自真实部署服务的独立观察。

## 3. 采用等级

| 等级 | 含义 | 最低要求 |
|---|---|---|
| **T0—硬门槛** | 在开放生产算力或处理租户数据前必须满足的硬条件 | 每个适用 T0 都必须被独立 `VERIFIED`；否则服务在本基线下为 **NO-GO** 且不符合 |
| **T1—基础级** | 责任、清单、最低安全卫生、可见性、响应与恢复 | 应在规模化前建立；参考路线图以首个 90 天为目标 |
| **T2—生产级** | 支撑可持续多租户运营的可复用、策略化、可度量控制 | 对相关正式商用服务边界必需 |
| **T3—可信级** | 面向敏感、监管、主权、专属、证明或机密计算画像，由独立证据支持的高保证控制 | 服务商作出相应保证承诺或威胁模型要求时必需 |
| **T4—自适应级** | 受控自适应自动化与持续验证 | 只有在权限、审批、停止、回滚、Trace 与独立 Verifier 均已证明后采用 |

任何分数、补偿控制、风险接受或紧急业务决定都不能把失败的适用 T0 变成 `VERIFIED` 或符合项。具备合法权限的高管可以出于特殊业务连续性原因，记录一项限时的继续运营或恢复服务决定；但在所有适用 T0 独立验证通过前，相关服务在本基线下仍保持 `NO-GO`。该决定必须明确范围和期限，并记录客户/法律/隐私/安全影响、替代方案、隔离、回滚、通知和整改。

## 4. 生产硬门槛

下列任一适用硬门失败、未知、过期、无法判定或未测试时，服务不得进入或继续被表述为符合本基线的生产状态：

1. **责任：** 每项生产服务、关键依赖、Root/Signing Key、服务商控制面、Fabric 管理面、BMC/OOB 环境和 Incident Path 都有可追责 Owner。
2. **共享责任：** Provider、Customer 与 Shared 对 Identity、Guest/Workload、GPU/Fabric、Data/Model、Logging、Incident、Backup、Deletion、Support 和 Assurance 的责任明确。
3. **清单与范围：** 范围内关键 Service、Asset、Identity、Public Endpoint、GPU/Fabric/OOB State、Data/Model、高影响 Artifact、Supplier 和 Dependency 已知且持续对账；未知关键范围属于失败，不能从分母中省略。
4. **特权身份：** 适用的服务商特权访问和高影响租户 Owner 访问使用批准的抗钓鱼 MFA；禁止共享管理员；Emergency Revocation 与 Break-glass 已在各执行点测试。
5. **API 正确性：** 每个关键公网和内部 API 认证主体，并在服务端执行 Object、Action、Tenant、Purpose 与 Context Authorization；缺失或冲突 Tenant Context 时拒绝请求。
6. **私有管理：** Provider Control Plane、Orchestrator Controller/Database、Fabric Management、BMC/OOB、Debug 与 Support Path 不得从公网或 Tenant Data Plane 直接到达；访问必须走受治理的特权路径。
7. **端到端隔离：** Tenant Identity 与 Policy 贯穿 API、Controller、Scheduler、Host、Accelerator、Storage、Ethernet、InfiniBand/RDMA、DPU/NIC、Telemetry 与 Support；并在真实数据路径上测试禁止路径。
8. **计算 SKU 声明：** 每种商业 SKU 都明确并测试 Host、Hypervisor/Container、GPU/HBM/Cache、NVLink Topology、Network/RDMA、Storage、Telemetry 与 Support 的共享方式、隔离属性和限制。
9. **加速器安全：** 整卡独占、硬件分区、虚拟化与 Time-slicing 被视为不同产品；Time-slicing 不得作为显存或故障隔离边界；Reset、Error Containment、Quarantine、Memory Handling 与跨租户 Cleanup 必须在实际 Hardware/Firmware/Driver/Scheduler Stack 上验证。
10. **编排安全：** Kubernetes/Slurm Controller 与 Database 私有、强认证、补丁及时、与租户权限分离、可备份和恢复；Privileged Workload/Job、Plugin 与 Node/Device Access 受控。
11. **数据/模型保护：** Crown-jewel Data、Prompt、Output、Model、Checkpoint、Embedding、Cache、Snapshot 与 Backup 具有 Owner、Classification、Purpose、Tenant-correct Access、批准的 Encryption/Key Ownership、Lineage、Retention、Export、Deletion 与 Sanitization 规则。
12. **信任根与 Secret：** 关键 Encryption、Signing、Identity、Attestation 与 Recovery Root 被盘点、访问控制、审计、职责分离且可恢复；静态/嵌入式生产 Secret 被消除，或作为明确且到期的例外治理。
13. **制品已知：** 生产 Image、Package、Driver、Firmware、Operator、Infrastructure Bundle、Model、Checkpoint、Prompt、Policy 与 Skill 来自批准、可归因、已盘点来源；发布关键制品执行所需 Provenance、Signature、Scan、Admission、Revocation 与 Rollback 检查。
14. **威胁驱动工程：** 重大服务和发布具有当前 Threat Model、安全验收、安全默认、已测试 Rollback、Observability/Evidence 要求及明确的未解决风险决定。
15. **暴露修复：** Internet-facing、Root-of-trust、Control-plane、Isolation 和其他高影响漏洞或不安全配置持续被发现，并在风险 SLA 内修复或隔离，且对部署状态复测。
16. **受保护审计：** 每次安全相关的 Privileged Identity、Root/Key、Policy、API/Control Plane、Orchestrator、Host/GPU/Fabric/BMC、敏感 Data/Model、Artifact Admission、Support Access 与高影响 Agent Action 的使用或变更，都会生成可归因、可关联、受保护证据；必需数据源丢失会被发现。
17. **Agent 权限：** 每个生产 AI System/Agent 都按 Owner、Identity、Delegator、Use Case、Data/Tenant Scope、Model/Prompt/RAG/Memory/Skill/Tool Version、Authority、Impact Assessment、Monitoring 与 Incident Path 建立清单和边界；Tool-using 与高影响系统按风险增加 Typed Interface、Policy Mediation、Least Privilege、Approval、Stop、Trace 与 Independent Verification。
18. **滥用与容量：** AUP、Prohibited Activity、Urgent-abuse Intake、租户感知的 Quota/Rate/Cost/Concurrency/Queue/Capacity、Egress、Safe Enforcement 与 Appeal 路径存在，并测试 Bypass 与 Denial-of-wallet。
19. **事件指挥：** 7×24 路径能够建立指挥、保全证据、可靠确定受影响租户/资源、吊销 Identity/Root、在可靠边界隔离、判断通知、恢复，并独立决定重新开服。
20. **恢复：** 关键 Provider-managed State 和必需 Customer Data 具有受保护、访问分离的 Backup 或 Known-good Rebuild Source；Restore/Rebuild 演练验证 RTO/RPO、Identity、Integrity、Tenant Isolation、Monitoring 与 Reopening。
21. **物理信任根：** Facility 与 BMC/OOB 路径受控；Hardware/Firmware Identity 与生命周期受治理；GPU/Accelerator State、Local Disk/Media、Credential、Network/Fabric Assignment 与 Host State 在重分配或处置前完成可验证清除或重新供应。

## 5. 按安全域划分的控制目录

### GOV—治理、风险、合规与共享责任

**结果：** 决策可追责、责任明确、例外受控且到期、保证可由独立证据支持。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-GOV-01 | T0 | 安全授权与可追责 Owner |
| NCS-GOV-02 | T0 | 共享责任与安全承诺 |
| NCS-GOV-03 | T1 | 风险与威胁建模治理 |
| NCS-GOV-04 | T2 | 合规、隐私与主权治理 |
| NCS-GOV-05 | T2 | 例外、保证与独立验证治理 |

### ASM—资产、服务、依赖与数据流清单

**结果：** 知道什么存在、谁负责、如何关联、影响哪个租户，以及实际状态是否符合意图。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-ASM-01 | T0 | 权威生产服务与资产清单 |
| NCS-ASM-02 | T1 | 身份、软件、数据与模型清单 |
| NCS-ASM-03 | T1 | 数据流与信任边界 |
| NCS-ASM-04 | T2 | 依赖与服务关系图 |
| NCS-ASM-05 | T3 | 持续发现与控制范围对账 |

### IAM—人员、租户、工作负载与 Agent 身份

**结果：** 每个行动主体都具有强、受限、可复核的身份；在技术可行时，Credential、Session 与 Delegated Authority 短期化。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-IAM-01 | T0 | 集中联邦与抗钓鱼 MFA |
| NCS-IAM-02 | T0 | 最小权限、JIT 管理与 Break-glass |
| NCS-IAM-03 | T2 | 经过证明的工作负载与服务身份 |
| NCS-IAM-04 | T1 | 租户、服务账户与访问生命周期 |
| NCS-IAM-05 | T2 | Agent 身份、委托与动作范围 |

### API—控制面、API 与管理接口

**结果：** 租户正确授权、私有服务商管理、抗滥用、变更可追踪、安全失败和 API 生命周期安全。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-API-01 | T0 | 租户正确的 API 认证与授权 |
| NCS-API-02 | T0 | 私有且受治理的管理接口 |
| NCS-API-03 | T1 | API 抗滥用与资源控制 |
| NCS-API-04 | T1 | 控制面变更完整性与审计 |
| NCS-API-05 | T2 | 安全 API 生命周期、测试与退役 |

### NET—网络、高性能互联、RDMA/InfiniBand 与 DPU 隔离

**结果：** 报文、存储、管理和直接内存路径的隔离经过测试，并覆盖 Controller 与 Stale-state 失败模式。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-NET-01 | T0 | 安全平面分离与默认拒绝 |
| NCS-NET-02 | T0 | 端到端租户网络、存储与 Fabric 隔离 |
| NCS-NET-03 | T1 | InfiniBand P_Key 与 RDMA 隔离验证 |
| NCS-NET-04 | T1 | 出网、DPU/NIC 与带外隔离 |
| NCS-NET-05 | T3 | 持续路径与隔离保证 |

### CMP—计算、虚拟化、裸金属、GPU 与加速器隔离

**结果：** 隔离属性明确、分配与重置安全、Host 加固、供应可信，并提供与服务匹配的高保证选项。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-CMP-01 | T0 | 每种计算 SKU 的明确隔离模型 |
| NCS-CMP-02 | T0 | 安全加速器共享、重置与显存处理 |
| NCS-CMP-03 | T1 | Host、Hypervisor 与容器加固 |
| NCS-CMP-04 | T2 | 安全供应、度量状态与证明 |
| NCS-CMP-05 | T3 | 高保证计算与侧信道控制 |

### ORC—Kubernetes、容器、Slurm 与调度安全

**结果：** Controller、授权、准入、调度、运行时、清理、备份与恢复安全。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-ORC-01 | T0 | 加固且私有的编排控制面 |
| NCS-ORC-02 | T1 | RBAC、准入、作业与特权工作负载控制 |
| NCS-ORC-03 | T1 | 租户调度、配额与放置边界 |
| NCS-ORC-04 | T2 | 运行时、节点、Secret 与插件安全 |
| NCS-ORC-05 | T2 | 编排系统备份、恢复与对抗验证 |

### DAT—数据、数据集、模型、制品与隐私保护

**结果：** 分类、目的、访问、使用、血缘、输出、保留、导出、删除和退租全过程受控。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-DAT-01 | T0 | 数据与模型分类、Owner 和生命周期 |
| NCS-DAT-02 | T0 | 加密、租户分离与访问控制 |
| NCS-DAT-03 | T1 | 血缘、完整性与安全制品处理 |
| NCS-DAT-04 | T1 | 删除、导出、退租与清除 |
| NCS-DAT-05 | T2 | 隐私、DLP 与敏感遥测/输出保护 |

### KMS—Secret、密钥、PKI、证明与机密计算

**结果：** 密码信任根受保护、Secret/Credential 短期化、身份/密钥释放受治理、Root 恢复经过测试。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-KMS-01 | T0 | 集中 KMS/HSM、密钥层级与 Root 保护 |
| NCS-KMS-02 | T0 | Secret 生命周期与静态凭据消除 |
| NCS-KMS-03 | T1 | PKI、证书与服务身份轮换 |
| NCS-KMS-04 | T3 | 证明驱动的准入与密钥释放 |
| NCS-KMS-05 | T2 | 密码敏捷与信任根恢复 |

### SSC—软件、模型与基础设施供应链安全

**结果：** 生产输入已知、获批、可归因、可验证、可召回且可回滚。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-SSC-01 | T0 | 批准来源与完整制品清单 |
| NCS-SSC-02 | T1 | 来源证明、签名与准入验证 |
| NCS-SSC-03 | T2 | 隔离构建、发布审批与回滚 |
| NCS-SSC-04 | T1 | 依赖漏洞、VEX 与开源风险 |
| NCS-SSC-05 | T2 | 固件、驱动、Operator 与模型供应保证 |

### ENG—安全工程、IaC、变更与配置

**结果：** 威胁驱动设计、安全默认、变更可 Review、测试门、漂移控制、可观测和可靠回滚。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-ENG-01 | T0 | 安全开发生命周期与威胁驱动设计 |
| NCS-ENG-02 | T1 | IaC/Policy-as-Code 与安全默认 |
| NCS-ENG-03 | T1 | 受保护变更、同伴 Review 与职责分离 |
| NCS-ENG-04 | T2 | 安全测试门、Canary 与回滚 |
| NCS-ENG-05 | T2 | 工程隐私、Secret 与可观测性要求 |

### VEM—漏洞、暴露面、补丁与固件管理

**结果：** 对每个范围内层次持续发现，并按风险修复，且通过部署状态复测闭环。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-VEM-01 | T0 | 持续漏洞与暴露面发现 |
| NCS-VEM-02 | T0 | 风险驱动修复与紧急补丁 |
| NCS-VEM-03 | T1 | 固件、驱动与平台补丁生命周期 |
| NCS-VEM-04 | T1 | 外部攻击面与配置漂移 |
| NCS-VEM-05 | T3 | 独立渗透、隔离与对抗测试 |

### TEL—遥测、检测工程、威胁情报与审计

**结果：** 必需证据租户安全、可发现篡改，检测针对相关威胁与失败模式经过测试。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-TEL-01 | T0 | 集中、受保护且租户安全的遥测 |
| NCS-TEL-02 | T0 | 信任根与控制边界强制审计 |
| NCS-TEL-03 | T1 | 映射威胁的检测工程 |
| NCS-TEL-04 | T1 | 证据保留、时间完整性与客户安全访问 |
| NCS-TEL-05 | T3 | 持续控制监控、威胁狩猎与 Purple Team |

### AIR—AI 应用、Agent、Tool、Skill 与 Prompt 安全

**结果：** 按风险治理权限、上下文、制品、Tool、Approval、Stop、Trace 与独立验证。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-AIR-01 | T0 | AI 系统与 Agent 清单及安全风险评估 |
| NCS-AIR-02 | T1 | 输入、Prompt、输出与 Schema 强制 |
| NCS-AIR-03 | T0 | Tool、Skill 与 Connector 最小权限及审批门 |
| NCS-AIR-04 | T2 | 模型、RAG、Memory 与 Skill 完整性 |
| NCS-AIR-05 | T4 | Agent Trace、确定性停止与独立验证 |

### ABU—滥用防护、租户信任、出网与可接受使用

**结果：** 分级准入、资源/外部交互控制、误用检测、安全执行、恢复与申诉。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-ABU-01 | T1 | 风险驱动租户身份与信任分级 |
| NCS-ABU-02 | T0 | 可接受使用、禁止活动与滥用响应 |
| NCS-ABU-03 | T0 | 配额、速率、成本与容量保护 |
| NCS-ABU-04 | T1 | 出网与外部交互控制 |
| NCS-ABU-05 | T2 | 滥用检测、协同与申诉质量 |

### IRR—事件响应、取证、危机管理与恢复

**结果：** 快速指挥、可靠定界、证据保全、安全隔离、可辩护通知、恢复与独立验证关闭。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-IRR-01 | T0 | 事件指挥、角色与安全通信 |
| NCS-IRR-02 | T1 | NeoCloud 特定事件 Playbook |
| NCS-IRR-03 | T1 | 取证就绪与证据保全 |
| NCS-IRR-04 | T1 | 客户、监管与生态通知 |
| NCS-IRR-05 | T2 | 演练、经验反馈与验证闭环 |

### RES—韧性、可用性、容量、备份与灾难恢复

**结果：** 降级行为安全、备份受保护、切换/恢复/重建经过测试，并验证后开服。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-RES-01 | T0 | 服务目标、依赖与恢复要求 |
| NCS-RES-02 | T0 | 不可变备份与验证恢复 |
| NCS-RES-03 | T2 | 控制面与 Region 韧性 |
| NCS-RES-04 | T1 | 容量、DDoS、队列与 GPU 耗尽韧性 |
| NCS-RES-05 | T3 | 已知可信重建、灾备与退出可迁移性 |

### PHY—物理、机房、BMC、硬件生命周期与介质清除

**结果：** 机房/硬件信任根受控、OOB 隔离、设备状态可信、清除与退役可证明。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-PHY-01 | T0 | 机房、物理访问与环境安全 |
| NCS-PHY-02 | T0 | BMC 与带外信任根安全 |
| NCS-PHY-03 | T1 | 安全硬件供应、固件清单与锁定 |
| NCS-PHY-04 | T0 | 加速器、本地盘与 Host 清除验证 |
| NCS-PHY-05 | T1 | 退役、介质销毁与保管链 |

## 6. 服务画像叠加要求

- **GPU-IaaS：** API 正确性；VM/Container 边界；明确整卡、硬件分区、虚拟化或 Time-slicing 的语义；Accelerator Reset/Error/Cleanup；Fabric/Storage 隔离；Image Provenance；Host/GPU Lineage；Quota、Billing 与 Egress。
- **Bare-Metal-GPU：** Provision/Deprovision Ceremony；BMC/OOB；Firmware 与 Measured State；Provider Credential Removal；专属或精确声明的共享 Network/Fabric/Storage；完整 Sanitization 与 Chain of Custody。
- **Managed-Kubernetes：** 私有/加固控制面；Tenant RBAC；Restricted Admission 与 Pod Security Standards；CNI/CSI/Device Plugin/Operator/Webhook 权限；Workload Identity；etcd Backup；Node Quarantine 与 Known-good Rebuild。
- **Managed-Slurm-HPC：** Controller/Database/Authentication；Account/Association/QOS/Partition/Reservation；Prolog/Epilog/SPANK/Module/Container Runtime；Shared Storage；Queue/Fabric Isolation；Job/Accounting Integrity 与 Recovery。
- **Model-Training：** Dataset Purpose/Rights/Provenance；Experiment 与 Source-to-Model Lineage；Poisoning/Integrity；Safe Format 与受限 Deserialization；Checkpoint、Temp/Cache；Evaluation Integrity；Export、Retention、Deletion 与 Ownership。
- **Model-Serving：** Endpoint/Model Authorization；Tenant-safe Routing 与 KV/Cache/Session Isolation；Prompt/Output 与 Telemetry Minimization；Model Provenance/Runtime Integrity；Extraction、Adversarial Input、Quota、Rate、Cost、Capacity、Fallback 与 Rollback。
- **Agent-Platform：** Inventory、Identity、Delegation；高影响工作流的不可变 Scope；Model/Prompt/RAG/Memory/Skill/Tool Provenance；Typed Interface；Policy Mediation；Least Privilege；Egress/Data/Cost；按风险要求的确定性 Approval/Stop；Protected Trace、Revocation 与 Independent Verification。
- **Sovereign-Regulated：** 司法辖区内的人员、身份、数据、密钥、支持、遥测、备份、供应商、事件响应、恢复、删除和可由独立证据支持的保证。只有 Storage Residency 不足以满足要求。

## 7. 证据有效期与重验证

证据超过规定有效期，或重大变更影响断言时即失效。重大触发器包括新 Service/SKU/Region/Fabric；Sharing/Isolation 变化；Orchestrator/Controller/Firmware/Driver 更新；Identity/Key/Policy 变化；Data Flow、Supplier、Support、Model、Agent、Tool、Recovery 或 Evidence Pipeline 变化；Control Failure；Incident；Restore/Rebuild；或无法复现原结论。

规范目录定义的默认最长间隔为：

| 等级 | 默认最低验证频率 |
|---|---|
| T0 | 技术可行时持续监控；至少每季度及重大变更后独立验证 |
| T1 | 至少每季度及重大变更后验证 |
| T2 | 至少每半年及重大变更后验证 |
| T3 | 至少每年独立验证，并在重大变更后验证 |
| T4 | 持续度量，并至少每季度进行对抗与失败模式复核 |

合同、法律、威胁、证据到期、发布或事件要求更短周期时，以更短周期为准。

## 8. 生产决策算法

```text
if 任一适用 T0 为 FAIL、UNKNOWN、STALE、INCONCLUSIVE 或 NOT_TESTED:
    decision = NO_GO_NONCONFORMANT
elif 任一关键服务或资产范围未知:
    decision = NO_GO_NONCONFORMANT
elif 任一必需 Isolation、Revocation、Restore、Incident 或 Sanitization 测试失败:
    decision = NO_GO_NONCONFORMANT
elif 任一未解决高风险缺少可追责决定:
    decision = NO_GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

紧急业务决定可以单独记录，但不会改变 `NO_GO_NONCONFORMANT`，也不会产生 `VERIFIED`。

采用[基线评估模板](../../templates/baseline-assessment.csv)、[实践指南](PRACTICE_GUIDE.md)与[度量指南](METRICS_AND_ASSURANCE.md)。Control 与 Evidence 变更遵循 [GOVERNANCE.md](../../GOVERNANCE.md)。
