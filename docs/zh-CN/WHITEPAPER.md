# NeoCloud Cyber Security 白皮书

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 面向实施的项目草案

## 执行摘要

本项目将 “NeoCloud” 作为行业工作术语，用来描述主要服务于加速器密集型人工智能与高性能计算工作负载的专业云服务商。这个词具备沟通价值，但目前没有唯一、正式、监管认可或普遍接受的定义。因此，本白皮书依靠明确的服务边界开展讨论，而不依赖标签本身。

NeoCloud 通常把云 API、物理 GPU 集群、裸金属、Hypervisor、Kubernetes、Slurm、高吞吐存储、以太网、InfiniBand/RDMA、NVLink 感知拓扑、DPU、固件、BMC/OOB 管理、模型与制品仓库、数据服务以及能力越来越强的 AI Agent 组合在一起。昂贵且共享的算力、高价值数据与模型、多套调度器、直接内存数据路径、深层软硬件供应链，以及机器速度的委托执行，共同形成传统企业安全或通用云安全检查表无法充分表达的失效模式。

NeoCloud Cyber Security 是一套面向该环境的**厂商中立安全基线、参考架构、发展路线图与实践指南**。它描述运营方如何设计和运行一套连贯的安全控制体系：身份与委托权限决定行动主体，策略治理信任决策，执行发生在靠近受保护资源的位置，证据与独立验证决定某项安全结果是否真的成立。

本仓库不是可直接部署的安全产品、正式标准、认证体系、法律意见，也不能证明任何服务商已经安全。它是一份由项目维护者编制的草案，目标是把服务边界、风险、控制、证据、验证、责任和建设优先级表达清楚并变得可测试。

本基线包含 18 个安全域、90 项控制和五个采用等级。T0 是生产硬门，每个适用 T0 都必须被独立验证为 `VERIFIED`；T1 建立责任、范围、安全卫生、可见性、响应与恢复基础；T2 将控制建设为可规模复用的平台能力；T3 在合理场景面向敏感、受监管、主权、专属、证明或机密计算画像增加可由独立证据支持的高保证；T4 仅用于受控自适应自动化与持续验证，并且必须先证明权限、审批、停止、回滚、Trace 和 Verifier。

任何分数、补偿控制、风险接受或高管决定都不能把失败的适用 T0 变成符合项。具备权限的高管可以记录一项限时的紧急业务连续性决定，但在该硬门独立验证通过前，控制仍然失败，相关服务在本基线下仍然不符合。

## 1. 目标与系统边界

目标是在完整服务生命周期内持续维持可信决策：

```text
设计 → 引入来源 → 构建/训练 → 供应 → 认证/委托
→ 调度 → 执行 → 观测 → 响应 → 恢复
→ 导出/删除 → 清除 → 退役
```

安全是贯穿整条链路的系统属性。强 API 认证无法补偿错误的对象/租户授权；加固 Kubernetes 不能自动证明 Slurm、RDMA、Storage 或 GPU 已隔离；Artifact Signature 不能证明 Source、Build、Review、Key Custody、Policy 与 Runtime Behavior 安全；Backup 可用不能证明 Identity、Integrity、Tenant Isolation 与恢复可信；模型生成的成功声明也不能证明 Agent 在授权范围内安全完成任务。

项目覆盖服务商运营及面向客户、并会实质影响机密性、完整性、可用性、隐私、租户隔离、滥用抵抗、主权、安全性、可恢复性或客户保证的组件。一个服务可以同时选择多个画像：

| 服务画像 | 典型边界 | 核心安全重点 |
|---|---|---|
| **GPU-IaaS** | 租户 VM/Container 运行于服务商加速器池 | API 授权、Host/GPU/Fabric/Storage 隔离、Image Provenance、分配与重置 |
| **Bare-Metal-GPU** | 向租户交付一台或多台物理主机 | 供应/退供、BMC/OOB、Firmware、专属/共享边界与清除 |
| **Managed-Kubernetes** | 服务商管理控制面，通常也管理 Node | Tenant RBAC、Admission、Plugin/Operator、Workload Identity、Node/GPU 隔离与恢复 |
| **Managed-Slurm-HPC** | 服务商管理 Scheduler、Partition、Node 与 Accounting | Controller/Auth、Account/Job 隔离、Queue/Fabric/Storage、Accounting 与恢复 |
| **Model-Training** | 托管 Dataset、Job、Checkpoint 与实验服务 | 权利/目的、血缘、投毒/完整性、安全格式、临时数据、导出/删除 |
| **Model-Serving** | 托管 Model Endpoint、Routing、Cache 与 Runtime | Endpoint/Model 授权、租户路由/缓存、抽取/滥用、配额与韧性 |
| **Agent-Platform** | 托管 Agent、Tool、Memory、Skill 与 Connector | 委托、外部内容边界、Tool Policy、Approval、Stop、Trace 与 Verification |
| **Sovereign-Regulated** | 人员、数据、密钥与运营受司法辖区限制 | 完整司法辖区边界、Support、Telemetry、Supplier、Recovery 与 Assurance |

合同边界外完全由客户控制的系统不属于服务商直接控制范围，但仍可能构成依赖或共同责任。具体法律结论、与安全无关的模型质量评估，以及认证声明也不属于本文范围。

## 2. NeoCloud 安全为什么不同

### 2.1 加速器共享方式实际上是不同产品

GPU 可以采用整卡独占、受支持的硬件分区、虚拟化或调度器 Time-slicing 等方式分配。它们不是可以相互替代的安全边界。

- **整卡独占**可以减少设备级共驻，但仍依赖 Host、Reset、本地盘、Network/Fabric、Telemetry、Support 与重新分配控制。
- **硬件分区**（例如受支持的 MIG 配置）可以在一个设备内提供独立的计算和显存资源；它不等于整卡或整机独占，仍依赖准确的 GPU 型号、Firmware、Driver、Virtualization、Topology、Scheduler 与运营流程。
- **虚拟化**的保证取决于具体 Passthrough/Mediated Architecture，以及 Host、IOMMU、Driver、Management 与 Reset Path。
- **Time-slicing**通过调度共享设备，不提供副本之间的显存或故障隔离；不得把它宣传或接受为硬件级租户隔离边界。

每种商业 SKU 都必须声明并测试 Host、GPU/HBM/Cache、DMA、Fault、Reset、NVLink Topology、Network/RDMA、Storage、Telemetry、Support 与 Cleanup 属性。敏感工作负载必须采用经威胁模型和客户承诺证明合适的方式。

### 2.2 高性能数据路径可能绕过普通假设

训练集群追求降低开销。Ethernet Overlay、Storage Network、InfiniBand P_Key、RDMA、DPU/NIC、NVLink Domain、BMC/OOB 和厂商 Controller 都可能形成单独的信任边界。VPC 或 Kubernetes NetworkPolicy 正确，不能证明 RDMA、DPU、Storage 或管理路径已经正确隔离。

P_Key Membership 是 InfiniBand 隔离的一项相关控制，但它依赖受到正确治理的 Fabric Management、Membership 配置、Endpoint 行为与实际 Enforcement。服务商必须保护 Subnet/Fabric Manager，对账期望与实际分配，测试禁止路径，发现 Stale/Partial State，并验证租户重新分配时的清理。

### 2.3 云与 HPC 控制模型并存

一个租户请求可能穿过 API Gateway、Identity/Policy、Provisioning Database、Kubernetes Operator、Slurm Controller、Image Factory、Node Agent、Network/Fabric Controller、Storage 以及 Billing/Quota 服务。每次转换都可能产生 Object、Action、Tenant、Purpose 或 State Confusion。因此，稳定的 Request、Tenant、Workload、Job、Node、Device、Data、Artifact、Policy 和 Evidence ID 本身就是核心安全控制。

### 2.4 数据、模型和中间状态既是资产也是攻击面

Dataset、Prompt、Output、Model Weight、Checkpoint、Adapter、Embedding、Vector Store、KV Cache、Agent Memory、Experiment Metadata、Log、Snapshot 与 Backup 可能包含知识产权、个人信息、Credential 或运营秘密；模型与 Checkpoint 还可能包含不安全序列化或投毒行为。

保护范围必须覆盖 Purpose/Rights、Tenant-correct Access、Encryption/Key Ownership、Lineage/Integrity、Safe Format/Loader、Temporary State、Output/Export、Privacy、Residency、Retention、Deletion、Backup Treatment 与 Offboarding，而不能只停留在静态存储加密。

### 2.5 可信供应链很深且权限很高

可信计算基可能包括 Firmware、BMC、DPU、NIC、GPU Driver、Kernel、Hypervisor、Runtime、Kubernetes/Slurm、Device Plugin、Operator、Image、Package、IaC、Model-serving Framework、Model/Checkpoint Format、Prompt、Policy、Skill、Build System、Registry 与 Signing Root。

运营方必须知道正在运行什么、来自哪里、由哪个身份构建与批准、证据是什么、如何撤销，以及如何召回、隔离、回滚或重建。有效签名只证明某个 Key 签署了某些 Byte，不能自动证明 Source、Review、Key Policy、Runtime Behavior 或安全性。

### 2.6 Agent 改变授权单位与失效速度

Agent 可以读取数据、执行代码、调用基础设施或业务工具、修改资源、对外通信，并以机器速度反复决策。控制强度应随权限和影响增加，而不应对所有 AI 功能套用相同的重型机制。

每个生产 AI System 或 Agent 都需要 Owner、Identity、Use Case、Model/Prompt/RAG/Memory/Skill/Tool Inventory、Data/Tenant Scope、Delegated Authority、Impact Assessment、Monitoring 与 Incident Path。Tool-using System 还需要 Typed Interface、Policy Mediation、Least Privilege、技术可行时的短期 Credential、Egress/Data/Cost Control 与 Revocation。高影响、破坏性、对外、影响客户、高成本或不可逆动作需要确定性审批和明确 Stop/Containment。自适应或自治安全工作流还需要不可变 Goal/Scope、受保护可重放 Trace、Budget/Time/Repetition/Uncertainty Stop、Rollback/Manual Recovery，以及 Agent 无法修改的独立 Verifier。

外部 Prompt、Document、Ticket、Web Page、Package、Model、RAG Data、Memory 与 Tool Output 只能提供观察，不能提供权限，也不能扩大 Identity、Goal、Scope、Tool、Credential、Policy、Approval、Budget、Evidence 或 Verifier Authority。

### 2.7 稀缺算力吸引滥用和可用性攻击

欺诈准入、Credential 转售、挖矿、禁止用途、Quota Bypass、Queue Manipulation、Capacity Hoarding、Model Extraction、Denial of Wallet、DDoS、依赖失效和破坏性自动化会同时影响安全、客户、商业和法律风险。因此，Tenant Trust、AUP、Quota/Rate/Cost/Concurrency、Egress、Capacity Engineering、公平执行、Incident Response 与 Appeal 都属于安全基线。

## 3. 资产、信任根与威胁主体

完整清单应覆盖：

- Tenant Organization、User、Owner、Federation、Quota、Billing、Support 与 Emergency Contact；
- Human Administrator、Service/Workload/Device/Agent Identity、API Key、Certificate、Break-glass 与 Signing/Recovery Root；
- API、Controller、Scheduler、Database、Operator、Policy Engine、CI/CD、Support System 与 Evidence Pipeline；
- Host、Hypervisor、Kernel、Runtime、BMC、DPU/NIC、GPU/HBM、Local Media、Network/Fabric、Rack、Region 与公共设施；
- Image、Package、Firmware、Driver、Operator、IaC、SBOM、Provenance、Signature、Model、Checkpoint、Prompt、Skill 与 Policy；
- Customer Data/Model Artifact、Cache、Output、Log、Snapshot、Backup、Deletion 与 Sanitization State；
- Supplier、SaaS、IdP、Registry、Repository、Remote Support 与 Critical Facility。

每个关键对象都需要可追责 Owner、Service/Tenant Relation、Identity、Location、Lifecycle、Expected State、Classification、Dependency、Telemetry、Recovery 与 Disposal Method。未知关键范围属于断言失败，不能从指标分母中删除。

威胁主体包括外部攻击者、恶意或失陷租户、欺诈客户、失陷 Workload/Model/Agent、内部人员、Support、失陷 Provider Identity、供应链攻击者、恶意或故障自动化、司法辖区行为者与物理攻击者。基础失效类型包括：

| 失效类型 | 示例 | 主要后果 |
|---|---|---|
| Identity/API | Credential 被盗、Federation 错误、Object/Tenant Authorization 缺陷 | Account Takeover、跨租户访问、欺诈消耗 |
| Provider Control Plane | 公网管理路径、Controller/Operator 漏洞、Automation Identity 泄露 | Fleet-wide Compromise、持久化、破坏性变更 |
| Compute/Runtime | VM/Container Escape、Privileged Job、Host Compromise | 访问 Host、邻居、Credential 或 Device |
| Accelerator | Memory Remanence、不安全共享、Reset/Error 失败、Side Channel | Data/Model 泄露与跨分配影响 |
| Fabric/Storage | VRF/VXLAN/P_Key/DPU/Storage 分配错误、RDMA Bypass | 跨租户直达或数据破坏 |
| Data/Model | 窃取、投毒、不安全格式/反序列化、删除失败 | IP/Privacy 损失、Code Execution、模型失陷 |
| Supply Chain | 被投毒的 Package/Image/Operator/Driver/Firmware/Model/Skill | 大规模高权限失陷 |
| Agent/Tool | Prompt Injection、Confused Deputy、权限过大、False Completion | 外传、未授权动作、破坏 |
| Abuse/Capacity | 欺诈、Quota/Cost Bypass、囤积、DDoS | 财务损失、服务退化、法律/安全风险 |
| Insider/Support | Standing Privilege、隐蔽访问、Evidence Tampering | 高可信路径访问与保证失效 |
| Recovery/Availability | Ransomware、Region/Fabric Failure、错误自动化、Backup 不可用 | 长时间中断、数据丢失、不安全开服 |
| Physical/Firmware | BMC Compromise、恶意部件、恶意维护 | OS 以下持久控制 |

威胁建模必须覆盖正常和禁止路径、依赖与 Controller Failure、Stale/Partial State、Operator Error、Malicious Configuration、Recovery 与 Evidence Integrity。灾难性的跨租户、Root-of-trust、破坏性或不可恢复失败不能被综合风险分数平均掉。

## 4. 安全原则

1. **身份与委托优先于位置。** 人员、租户、服务、工作负载、设备、Agent 与自动化都应独立认证和授权。
2. **最小权限同时绑定时间、任务、租户、目的和资源。** 技术可行时优先使用短期 Credential、Session 与 Delegated Authority。
3. **租户隔离必须端到端。** 测试 API、Control Plane、Scheduler、Host、GPU、Storage、Cache、Telemetry、Ethernet、RDMA、DPU、OOB 与 Support Path。
4. **共享方式必须作为不同产品明确说明。** 不得把整卡、硬件分区、虚拟化和 Time-slicing 混成一个“隔离 GPU”声明。
5. **服务商独占控制仍由服务商负责。** 客户无法访问和治理的基础设施不能通过文档转嫁责任。
6. **外部内容是不可信数据，而不是权限。** 授权来自 Identity、Delegation、Policy 与批准决定。
7. **证据属于控制。** 机制部署后，还需要 Scope、Failure Behavior、Negative Test、Freshness 与 Independent Verification 才能证明有效。
8. **假设失陷并限制爆炸半径。** 设计快速 Revocation、Isolation、Quarantine、Rebuild、Recall 与租户安全取证。
9. **恢复要恢复信任，而不只是可用性。** 重新开服前验证 Identity、Artifact、Data、Tenant Isolation、Monitoring 与目标。
10. **自动化先赢得权限。** 只有在 Approval、Stop、Rollback、Trace、Budget 与 Verifier 被证明后才增加自主性。
11. **复杂性必须证明值得。** 优先采用 Identity、Policy、Isolation、Provenance、Evidence、Recovery、Feedback 与 Verification 等通用机制。
12. **准确表达不确定性。** 使用“完整”“不可变”“专属”“机密”“零信任”等词时必须附带范围和证据契约。

## 5. 运营模型与共享责任

高管风险 Owner 设定风险偏好并作出特殊业务决定；CISO 或等效角色负责安全体系。每个客户服务都应有业务、技术、安全、数据和事件 Owner。平台团队建设复用能力，服务团队仍对接入正确性和服务声明负责。

即使组织很小，也要区分三类功能：

- **实施与运营：** Product、Platform、Infrastructure、SRE、Network、Facility、Data 与 AI Team；
- **Policy、Risk、Privacy 与 Challenge：** Security、Privacy、Legal/Risk 与 Compliance；
- **独立验证：** 能挑战实施者的不同人员/团队、Observation Path、Test Harness 或 Qualified Assessor。

服务商不能把 BMC/OOB、Fabric Manager、Host Reset、Provider Control Plane、Signing Root 等独占控制转嫁给客户。除非合同另有约定，客户对自身 Code、Data Classification、Role Assignment、Guest/Workload Configuration 与 Use 负责。每项服务必须明确正常运营和事件期间的 Identity、Workload、Data/Model、GPU/Fabric、Logging、Support、Backup/Restore、Export/Deletion、Evidence 与 End-of-service 责任。

## 6. 参考架构

目标安全体系由七个协同平面构成：

1. **治理与保证：** Service、Scope、Obligation、Responsibility、Risk、Decision、Exception、Control State、Evidence 与 Assurance。
2. **身份与策略：** Human/Tenant/Service/Workload/Device/Agent Identity、Federation、PKI、JIT Privilege、Delegation、Policy Decision 与 Approval。
3. **边缘与控制面：** Public API、Support/Privileged Access、Provisioning、Quota/Billing、Controller 与 Administrative Interface。
4. **编排与运行时：** Kubernetes、Slurm、Admission/Job Policy、Scheduler、Runtime、Node Agent、Sandbox 与 Workload Control。
5. **计算、Fabric、存储与物理 Root：** Host、Hypervisor、Accelerator、DPU/NIC、Ethernet、InfiniBand/RDMA、NVLink Topology、Storage、BMC/OOB、Facility、Reset 与 Sanitization。
6. **数据、模型与供应链：** Source、Build/Train、Registry、SBOM/Provenance/Signing、Dataset、Model、Checkpoint、Prompt、Skill、Policy、Safe Loading 与 Release。
7. **遥测、响应与恢复：** 必需 Log/Trace、Inventory/Reconciliation、Detection、Case、Protected Evidence、Revocation、Containment、Backup、Restore 与 Known-good Rebuild。

Policy Enforcement 应靠近受保护资源；中央 Decision 或 Evidence Service 故障时不能形成静默 Fail-open。稳定 ID 应关联 Subject、Delegation、Tenant、Request、Policy Version、Desired/Actual State、Workload/Job、Host/GPU/Fabric/Storage Assignment、Data/Model Access、Result、Cleanup 与 Evidence。

任何组件都不能只凭自己的 Dashboard 证明自己有效。关键证据应导出到普通源系统管理员无法静默修改的边界，同时实施 Tenant Partitioning、Minimization、Privacy、Retention、Legal Hold、Time Integrity 与 Access Audit。

## 7. 十八个安全域

1. 治理、风险、合规与共享责任；
2. 资产、服务、依赖与数据流清单；
3. 人员、租户、工作负载与 Agent 身份；
4. 控制面、API 与管理接口；
5. 网络、Fabric、RDMA/InfiniBand 与 DPU 隔离；
6. 计算、虚拟化、裸金属、GPU 与加速器隔离；
7. Kubernetes、容器、Slurm 与调度器；
8. 数据、数据集、模型、制品与隐私；
9. Secret、密钥、PKI、Attestation 与机密计算；
10. 软件、模型与基础设施供应链；
11. 安全工程、IaC、变更与配置；
12. 漏洞、暴露面、补丁与固件；
13. 遥测、检测工程、威胁情报与审计；
14. AI 应用、Agent、Tool、Skill 与 Prompt；
15. 滥用防护、租户信任、出网与 AUP；
16. 事件响应、取证、危机管理与恢复；
17. 韧性、可用性、容量、备份与灾难恢复；
18. 物理、机房、BMC、硬件生命周期与介质清除。

[安全基线](SECURITY_BASELINE.md)定义稳定 ID 和生产硬门；机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)提供双语要求、证据/验证画像、等级频率与指标关联。

## 8. 等级、验证与例外

| 等级 | 目的 | 默认验证方式 |
|---|---|---|
| **T0 硬门槛** | 生产准入硬门 | 技术可行时持续监控；至少每季度及重大变更后独立验证 |
| **T1 基础级** | 责任、范围、安全卫生、可见性、响应与恢复 | 至少每季度及重大变更后验证 |
| **T2 生产级** | 可复用、可执行、可度量控制 | 至少每半年及重大变更后验证 |
| **T3 可信级** | 服务特定高保证 | 至少每年独立验证，并在重大变更后验证 |
| **T4 自适应级** | 受控自适应自动化 | 持续度量，并至少每季度进行对抗与失败模式复核 |

控制生命周期为：

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

`IMPLEMENTED` 只证明已经部署，不证明有效。只有独立验证者针对明确 Service、Version、Region、Asset/Tenant Scope、Test、Evidence 与 Validity Period 返回 `PASS`，才能进入 `VERIFIED`。`FAIL`、`INCONCLUSIVE`、`NOT_TESTED`、证据过期、重大变更或无法复现都会使原结论失效。

Exception Record 可以记录偏离要求的运营事实，但不能改变要求或结果。适用 T0 的例外仍然是失败/不符合硬门。对外保证必须说明 Scope、Date、Version、Limitation、Failed Test、Exception 与 Verifier，而不能只展示一个混合分数。

## 9. 融入完整生命周期

### 设计

实现前定义 Service Profile、Tenant/Trust Boundary、Isolation SKU、Data Class/Purpose、Jurisdiction、Responsibility、Abuse Case、SLO/RTO/RPO、Evidence Contract、Failure Behavior、Recovery、Deletion 与 Decommission。安全要求必须成为发布验收标准。

### 引入来源、构建、训练与发布

保护 Source/Build Identity；Review IaC 与 Policy-as-Code；隔离高影响 Build；盘点直接/传递依赖；生成适当 BOM/Provenance/Signature；治理 Dataset、Model、Prompt、Skill、Driver 与 Firmware；只允许符合 Policy 的 Artifact；分阶段部署；观察规定信号；测试 Recall 与 Rollback。

### 供应、调度与执行

认证 Subject/Tenant；评估 Action、Object、Purpose、Context、Isolation 与 Cost Policy；生成不可变 Request/Correlation ID；带 Tenant Identity 分配 Network/Fabric/Storage/Host/Accelerator；对账 Desired/Actual State；签发范围受限的短期 Workload Credential；在 Admission/Node 边界复验 Artifact 与 Placement；关联 Runtime Event；任务结束时清理 Credential、Accelerator/Local State 和 Assignment。

### 观测与响应

采集定义好的安全相关 Telemetry；监控 Source Coverage/Freshness；保全 Evidence；建立 Incident Command；确定可靠 Scope；在最强可信边界 Contain；吊销 Identity/Key；按需隔离 Artifact、Node、Device、Path、Data 或 Tenant；判断 Customer/Regulatory Impact；记录决定。

### 恢复、删除与退役

Root 无法确认可信时，优先 Revocation 与 Known-good Rebuild。Restore/Rebuild 在满足 RTO/RPO 的同时验证 Identity、Artifact Integrity、Tenant Isolation、Data Correctness 与 Monitoring。执行授权 Export/Deletion，按 Policy 处理 Backup Retention，依据风险和设备能力清除 Media 与 Accelerator/Host State，移除 Network/Fabric Assignment 和 Credential，并保留 Chain-of-custody Evidence。

## 10. 证据与持续证明

有效证据项应标识：

- Control 与人类可读 Assertion；
- Service/Profile、Environment、Region、Version、Tenant/Asset/Data Scope；
- Collector Identity、Source System、Method/Query/Test Version 与 Time；
- Result、Limitation、Sampling 与 Blind Spot；
- Integrity Protection 与 Protected Location；
- Validity Period 与 Invalidation Trigger；
- Validator、Test Result、Finding 与 Retest Date。

证据强度通常从 Statement、Screenshot/Manual Report、Reproducible Query/Export、Protected Runtime Event 或 Verified Attestation、Authorized Negative/Failure/Recovery Test，逐步提升到通过独立 Observation Path 的复现。具体证据必须与断言匹配，Evidence Score 不能替代判断或生产硬门。

持续证明组合 Inventory Reconciliation、Policy Evaluation、Exposure Discovery、Required-source Health、Isolation Test、Revocation/Restore Exercise、Detection Replay、Artifact Recall、Sanitization Evidence、Agent Adversarial Evaluation、Exception Expiry 与 Independent Sampling。系统还必须发现自身 Collector、Schema、Permission、Clock、Evidence Store、Test 与 Verifier 的故障。

## 11. 发展路线

典型体系通过证据门推进，而不能只按日期宣称成熟：

1. **第 0–7 天：** 建立 Owner、Incident Command、关键清单、Change Freeze 与 Emergency Revocation。
2. **第 8–30 天：** 清理关键公网/管理暴露；实施抗钓鱼特权访问、私有管理、明确 SKU 隔离、Root Protection、必需 Telemetry 与核心 Playbook。
3. **第 31–90 天：** 建立权威 Service/Asset/Identity/Data/Model/Dependency 清单、共享责任、生命周期、漏洞/暴露管理、Backup Dependency 与 Desired/Actual Reconciliation；独立验证所有适用 T0。
4. **第 3–6 个月：** 产品化 Workload Identity、Policy-as-Code、Trusted Artifact、Reconciliation、Node/Runtime Response、Evidence Automation、Tenant Trust 与 Secure Engineering。
5. **第 6–12 个月：** 关闭 T2 缺口；执行跨租户、Accelerator、Fabric、Recovery、Detection、Incident 与 Customer-notification 演练。
6. **第 12–18 个月：** 按专属、敏感、监管、主权、证明或机密计算承诺增加 T3；独立测试 Root、Isolation、Supplier 与 Recovery。
7. **第 18–24 个月：** 只有在 Precision、Approval Bypass、Scope Violation、False Completion、Rollback、Kill Switch 与 Independent Verifier 可度量时，才引入 T4 自适应自动化。

[发展路线图](ROADMAP.md)定义 Workstream、Dependency、Exit Gate 与 Build/Buy 建议。日期只是参考；今天存在的 T0 失败不能因为路线图把工作排到未来阶段而继续暴露。

## 12. 客户与生态透明度

可信服务商应能在适当保密条件下提供：

- 精确 Service Boundary、Profile、Region 与 Version；
- 当前 Provider/Customer/Shared Responsibility；
- Host、GPU/HBM/Cache、NVLink、Network/RDMA、Storage、Telemetry、BMC 与 Support 的共享/隔离声明；
- Data/Model Purpose、Access、Encryption/Key Ownership、Residency、Retention、Export 与 Deletion；
- Support Access、Vulnerability、Incident、Notification 与 Evidence-exchange 承诺；
- Artifact/Firmware Provenance 方案；
- Backup、Restore、Rebuild、Offboarding 与 Sanitization 行为；
- Independent Test、Evidence Validity、Material Finding、Exception 与 Remediation Date；
- 与声明有关的 Supplier、Subprocessor 与 Critical Dependency。

安全声明必须精确。“专属”要说明每种专属和共享资源；“加密”要说明明文在哪里存在、谁控制 Key Release；“机密”要说明 Threat Model、Hardware/Software/Attestation Boundary、Unsupported Component 与 Key-release Policy；“零信任”要说明 Subject、Policy、Enforcement Point、Failure Behavior 与 Verification；“合规”要说明具体 Obligation、Scope、Assessor、Date 与 Exception。

## 13. Build、Buy 与深度集成

应自建或深度集成编码 NeoCloud 特有租户与拓扑语义的能力：Tenant-aware Authorization、Desired/Actual Reconciliation、GPU/NVLink/Fabric/DPU/Storage/Scheduler Placement Evidence、Reset/Sanitization、Model/Checkpoint Lifecycle 与 Safe Loading、Agent Delegation/Tool Mediation，以及服务特定的 Containment/Reopening。

成熟且接口和证据清晰的能力可以采购或采用托管/开源组件，例如 IdP/MFA、PAM、KMS/HSM、Secret Management、PKI、Vulnerability/Attack-surface Management、SIEM/Data Lake、Runtime Detection、Case Management、Backup、DDoS/WAF/API Gateway、Signing/Transparency Infrastructure。

厂商 Dashboard 不能证明边界覆盖。必须要求可导出数据/API、稳定 Identity、Tenant-safe Behavior、Secure Update、HA 与 Safe Degraded Mode、Failure Detection、Incident Notification、Data Handling、Independent Testing、Migration/Exit，以及能够关联服务边界的证据。

## 14. 局限

本基线有意覆盖较广，无法编码每种产品、司法辖区、服务合同、硬件代际、Driver/Firmware 组合、威胁主体与 Safety Requirement。部分指标只是参考起点，不是普遍阈值。草案和厂商资料可以影响项目，但不会自动成为规范要求。Control Mapping 不是认证；通过基线也不能消除所有风险；失败控制不应被虚假的精确分数隐藏。

组织必须按当前服务威胁模型调整控制，获取合格 Legal/Privacy/Safety/Audit 意见，测试真实部署路径，明确表达不确定性，并使 Assurance 保持时效。

## 15. 结论

NeoCloud 安全的本质，是在物理密集、高度共享、软件定义、深度依赖供应链并越来越自主化的 AI 基础设施中，持续维持可信、租户正确且可恢复的决策。

最低可行体系包括：明确服务边界、可追责责任、强身份与委托、准确的 Accelerator/Fabric/Storage 隔离、受保护的 Data/Model/Artifact、必需 Telemetry、经过测试的 Response/Recovery/Sanitization、按风险治理的 Agent，以及经得住独立挑战的证据。

先落实 T0 生产硬门；建立 T1 责任与可见性；将 T2 转为平台服务；只有在后果或承诺需要时增加 T3；只有在权限和失败模式可度量、可约束时引入 T4。这个顺序可以让安全随 Compute、Model、Agent、Customer 与 Regulation 扩展，而不把每种新风险变成无法验证的例外。

## 免责声明

本白皮书是一份由项目维护者编制、面向实施的草案，不构成认证、正式标准、法律意见、绝对保证，也不能替代适用法律法规、合同、隐私评估、安全评估、产品文档或合格独立审计。外部框架映射与来源引用仅供参考，必须针对实际组织、服务、司法辖区、采用版本与保证目标重新验证。
