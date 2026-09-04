# NeoCloud Cyber Security 参考架构

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 面向实施的项目草案

## 1. 目标与架构契约

本参考架构描述专业 AI/GPU 云的目标安全体系。它是逻辑架构且保持厂商中立：组件可以合并或拆分部署，但信任决策、执行点、失败行为、证据和恢复边界必须保持明确。

本架构不是可直接部署的软件，也不规定唯一产品栈。它通过七个协同平面落实[安全基线](SECURITY_BASELINE.md)：

```text
治理与保证
    │
身份、委托与策略
    │
边缘、API 与服务商控制面
    │
编排与工作负载运行时
    │
计算、加速器、Fabric、存储与物理 Root
    │
数据、模型与软硬件供应链
    │
遥测、响应、恢复与持续证明
```

每个重大动作都应该回答：

```text
谁或什么正在行动？
由谁委托？
针对哪个租户和目的？
操作哪个资源与版本？
依据哪一版策略和审批？
通过哪些执行点？
实际发生了什么变化？
哪些证据能证明结果及失败行为？
谁能够独立验证并恢复？
```

## 2. 信任假设

- 网络位置本身不是身份或授权。
- 公网入口可以从未认证但被明确标记为**匿名/不可信主体**开始；任何 Tenant-specific、Privileged、State-changing、高成本或敏感动作发生前，必须完成所需认证和授权。
- Identity 可以长期存在；在技术可行时，Credential、Session、Privilege Grant 与 Delegated Authority 应短期化且范围受限。
- Tenant Context 在请求路径中显式且不可被中途替换；缺失或冲突时拒绝请求。
- Prompt、Ticket、Document、Web Page、Package、Model、RAG Data、Memory 与 Tool Output 等外部内容只能提供观察，不能授予权限。
- Provider Control Plane、BMC/OOB、Fabric Manager、Host Reset 与 Signing Root 等服务商独占 Root 仍由服务商负责。
- Central Policy、Identity、Evidence 或 Orchestration Service 可能失效；Local Enforcement 必须定义 Fail-closed 或 Safe-degraded 行为，而不能因 Decision 过期或缺失静默允许。
- 任何组件都不能只靠自己的状态或 Dashboard 证明自己有效。
- 恢复必须重新建立对 Identity、Artifact、Data、Isolation 与 Monitoring 的信任，而不只是恢复进程可用。

## 3. 稳定身份与关联模型

为以下对象使用稳定、不可复用的标识：

- Service、Service Profile、Environment、Region 与 Release；
- Tenant、Organization、User、Service、Workload、Device 与 Agent；
- Human/Service Delegator 与 Delegated Session；
- Request、Change、Approval、Policy Version 与 Decision；
- Kubernetes Cluster/Namespace/ServiceAccount/Pod 与 Slurm Cluster/Account/Job；
- Host、Hypervisor、GPU/Accelerator、Partition/Virtual Function、DPU/NIC、Rack 与 Fabric Port；
- VLAN/VXLAN/VRF/P_Key、Storage Account/Volume/Object 与 Local Media；
- Dataset、Prompt、Output、Model、Checkpoint、Embedding、Cache、Image/Package/Driver/Firmware/Policy/Skill；
- Key、Certificate、Secret、Attestation 与 Signing/Recovery Root；
- Event、Evidence、Finding、Case、Incident、Restore、Sanitization 与 Verifier Result。

这些 ID 必须出现在 API Object、Message、Desired/Actual Controller State、Scheduler Allocation、Enforcement Decision、Log、Evidence 与 Cleanup Record 中。标识之间的转换本身也必须受控、留证并对账。

## 4. 策略决策模型

可复用授权请求如下：

```text
subject identity
+ delegation chain
+ action
+ resource
+ tenant
+ purpose
+ context
+ resource and artifact state
+ policy version
→ allow | deny | require approval | quarantine
+ obligations
```

Context 可以包括 Device/Workload/Agent State、Authentication Strength、Service/Profile、Region、Data Class、Isolation SKU、Quota/Cost、Vulnerability/Exposure、Artifact Provenance、Attestation Freshness、Incident State 与 Risk Decision。

Obligation 可以要求整卡或硬件分区放置、Restricted Egress、Masking、Rate/Quota/Cost、JIT Session Evidence、Dual Approval、Attestation、Sandbox、Post-action Verification、Cleanup、Notification 或 Manual Review。

Policy Decision 应包含 Reason、Decision ID、Version、Expiry/Staleness Rule 与 Evidence Destination。受保护资源负责执行；只有中央策略判定但没有资源侧 Enforcement 不构成完整控制。

## 5. 七个安全平面

### 5.1 治理与保证平面

维护：

- Service Catalog 与准确边界；
- Control Applicability 与 Shared Responsibility；
- 法律、监管、隐私、安全、主权、合同与客户承诺；
- Threat Model、Risk 与灾难性失败路径；
- 不改变控制结果的 Business Decision/Exception；
- Control Lifecycle、Evidence Validity、Independent Verification 与 Assurance Package；
- Supplier/Dependency Assurance；
- Release 与 Reopening Decision。

该平面必须区分项目符合性、法律义务、业务风险决定与外部认证。紧急决定不能把失败 T0 变成 `VERIFIED`。

### 5.2 身份、委托与策略平面

提供：

- Human/Tenant Federation、Authenticator Policy 与抗钓鱼 Privileged Access；
- JIT/JEA Administration、Session Control、Emergency Revocation 与 Break-glass；
- Workload、Service、Device 与 Agent Identity；
- Short-lived Certificate/Token、Audience 与 Tenant/Resource Scope；
- Delegation Chain、Purpose 与 Approval；
- Policy Evaluation、Distribution 与 Revocation；
- PKI、KMS/HSM、Attestation Verification 与 Key-release Decision；
- Identity/Access Lifecycle 与 Review。

不得向 Tenant Workload 暴露共享 Provider Identity。Workload 或 Agent 不能扩大自己的 Delegation、Policy、Credential、Evidence 或 Verifier Authority。

### 5.3 边缘、API 与服务商控制面

包含 Public Ingress、API Gateway、Tenant Console、Support Entry、Provisioning、Quota/Billing、Provider Administration 与 Service Controller。

要求：

- 公网匿名流量在需要并完成认证前保持显式不可信；
- 关键 API 在服务端执行 Object、Action、Tenant、Purpose 与 Context Authorization；
- 控制 Schema、Size、Replay、Idempotency、Rate、Quota、Concurrency 与 Cost；
- Provider Administration、Debug、Controller/Database、Fabric 与 BMC 通过私有受治理路径访问，而不是从公网或 Tenant Data Plane 直接到达；
- 高影响变更关联 Actor、Request、Tenant、Policy、Approval、Desired State、Actual State、Result 与 Rollback；
- Partial Provisioning 必须回滚或隔离，不能形成状态含糊的活动资源；
- API Inventory、Test、Versioning、Deprecation 与 Credential Removal 受治理。

### 5.4 编排与工作负载运行时平面

包括 Kubernetes、Slurm、Scheduler Service、Admission/Job Policy、Node Agent、Runtime、Sandbox、CNI/CSI/Device Plugin、Operator、Webhook、Prolog/Epilog、SPANK、Module 与 Workload Telemetry。

要求：

- 私有、已修补且可恢复的 Controller/Database；
- Least-privilege RBAC 与 Service Identity；
- 限制 Privileged Workload/Job、Host、Mount、Device 与 Network Access；
- Tenant Namespace/Account/Partition/Queue、Quota、Priority 与 Reservation Boundary；
- 带 Tenant Context 的 Topology-aware Host/GPU/Fabric/Storage Placement；
- 适用时实施 Artifact/Attestation Admission；
- Secret 与 Workload Credential JIT 交付并在结束时撤销；
- Runtime Detection、Node Quarantine 与 Known-good Rebuild；
- Controller、Database 与 Accounting Backup/Restore，并测试 Tenant/Integrity。

### 5.5 计算、加速器、Fabric、存储与物理 Root 平面

包含 Host、Hypervisor、Kernel、Runtime、GPU/HBM/Cache、Accelerator Partition/Virtualization、NVLink Topology、DPU/NIC、Ethernet、InfiniBand/RDMA、Storage、Local Media、BMC/OOB、Rack 与 Facility。

要求：

- 每种 Commercial SKU 声明 Host、GPU、Memory/Cache、Fault、Reset、DMA、NVLink、Ethernet/RDMA、Storage、Telemetry 与 Support 属性；
- 整卡独占、硬件分区、虚拟化与 Time-slicing 作为不同安全产品；
- Time-slicing 不能作为 Memory/Fault Isolation；
- 硬件分区不能表述为整卡或整机专属；
- 在准确 Hardware/Firmware/Driver/Hypervisor/Scheduler Stack 上测试 Allocation、Reset、Error Containment、Quarantine、Local-state Cleanup 与 Tenant Reassignment；
- Packet、Storage、Management 与 Direct-memory Path 分别隔离并测试；
- 对账 P_Key Membership/Enforcement、Fabric-manager Authority、DPU/NIC Assignment、Stale/Partial State 与 Cleanup；
- BMC/OOB 与 Public、Tenant 和普通 Corporate Network 隔离；
- 治理 Firmware Identity、Secure Configuration、Update、Detection 与 Recovery；
- 控制 Facility、Maintenance、Custody、Environment 与 Emergency Response；
- 按数据敏感度和设备能力选择 Media/Device Sanitization 方法，并在 Reassignment/Disposal 前验证。

### 5.6 数据、模型与供应链平面

治理 Dataset、Prompt、Output、Model、Checkpoint、Adapter、Embedding、Vector Store、Cache、Snapshot、Backup、Image、Package、Operator、Driver、Firmware、IaC、Policy、Skill、Source、Build/Training、Registry 与 Signing Root。

要求：

- Owner、Purpose、Rights、Classification、Tenant、Jurisdiction、Lifecycle 与 Customer Ownership 已知；
- Access 具备正确 Tenant 语义，并关联 Identity、Purpose 与 Policy；
- Encryption/Key Ownership 覆盖 Transit、Storage、Snapshot/Backup，并在合理场景覆盖 Use；
- 保留 Source-to-use Lineage 与 Integrity；
- 拒绝或隔离 Unsafe Format 与 Unrestricted Deserialization；
- Release-critical Artifact 具有适用的 Inventory/BOM、Provenance、Signature、Scanner、Compatibility、Policy、Revocation 与 Admission Evidence；
- 只有 Policy 明确要求时才必须签名；对 Unsigned-when-required、Unknown、Revoked、Incompatible 或 Unapproved Artifact 拒绝准入；
- 保护 Build/Train Identity 与 Environment，分离 Approval，分阶段发布并可回滚；
- 清理 Intermediate File、Cache、Credential 与 Temporary Data；
- 测试 Export、Retention、Deletion、Backup Treatment、Offboarding 与 Recall。

### 5.7 遥测、响应、恢复与持续证明平面

从 Identity/Policy、API/Control Plane、Kubernetes/Slurm、Host/GPU/Fabric/BMC、Data/Model、Key、Artifact/Supply Chain、Support、Agent、Abuse、Backup 与 Recovery System 采集并关联必需的安全相关 Telemetry。

要求：

- 定义 Required-source Inventory、Event Field、Source Identity、Time Integrity、Coverage、Freshness 与 Failure Detection；
- 实施 Tenant-safe Collection、Minimization、Redaction、Access、Retention 与 Legal Hold；
- 关键 Evidence 导出到普通 Source Admin 无法静默修改的边界；
- Detection 来自当前 Threat Model，并用授权 Behavior Replay 测试；
- Case/Incident 关联稳定 Service/Tenant/Resource/Evidence ID；
- 快速建立 Command、可靠定界、Identity/Key Revocation，并在可信边界 Contain；
- 实施 Protected Backup、Restore、Failover 与 Known-good Rebuild；
- 处理 Independent Verification 与 Evidence Expiry/Invalidation；
- 自监控 Collector、Schema、Permission、Clock、Test、Evidence Store 与 Verifier Availability。

## 6. 信任区与允许通信

典型部署至少分离：

1. Public Edge；
2. Tenant API 与 Service Front Door；
3. Provider Privileged-access Zone；
4. Provider Control-plane Zone；
5. Orchestrator-controller Zone；
6. Tenant Workload/Data Plane；
7. Storage Plane；
8. Ethernet/Fabric/RDMA Plane；
9. BMC/OOB 与 Hardware-management Plane；
10. Build/Train/Registry 与 Supply-chain Zone；
11. Security Evidence/Response Zone；
12. Backup/Recovery Zone；
13. Corporate IT 与 Support Environment。

跨区通信必须明确 Source Principal，或明确标记 Anonymous/Untrusted；同时定义 Destination、Protocol/Interface、Action、适用的 Tenant/Purpose、Authentication Requirement、Authorization Decision、Rate/Cost Rule、Encryption/Integrity、Telemetry、Owner、Failure Behavior 与 Expiry。“Internal Any-to-any”不能作为默认规则。

Provider Management、Fabric、BMC/OOB、Evidence 与 Backup Zone 不应从 Tenant/Public Data Plane 直接到达。Corporate IT 不得成为通往生产 Root 的不受控桥梁。

## 7. 端到端工作流

### 7.1 租户工作负载或训练 Job

```text
1. 认证 Tenant Subject，解析 Organization/Role。
2. 验证 Request Schema、Replay/Idempotency、Quota、Cost 与 Data Classification。
3. 授权 Object、Action、Tenant、Purpose 与 Context，生成 Request/Decision ID。
4. 验证 Image/Code/Model/Checkpoint Policy 及必需 Provenance/Signature/Scan。
5. 选择允许的 Host/GPU/Sharing/Fabric/Storage Topology。
6. 写入与 Tenant 关联的 Desired State。
7. Controller 对账 Actual State 并报告偏差。
8. 签发 Scope 受限的 Short-lived Workload Identity/Secret。
9. Admission/Node Enforcement 复验 Artifact、Identity 与 Placement。
10. 关联 Job、Node、GPU、Fabric、Storage、Data/Model 与 Policy Event。
11. 完成或失败后撤销 Credential，并清理 Accelerator/Local/Fabric State。
12. 独立抽样或测试结果断言和证据。
```

任一步失败都必须 Rollback、Quarantine 或留下显式可恢复状态；含糊的 Partial Provisioning 属于控制失败。

### 7.2 服务商特权操作

```text
identity + phishing-resistant MFA
→ ticket/purpose and risk context
→ JIT least-privilege grant
→ approved private access path
→ command/action policy
→ protected session and target evidence
→ post-action desired/actual verification
→ expiry/revocation
→ independent review for high-impact change
```

Break-glass 独立保存、严密控制、持续监控、定期测试，并在每次使用后 Review。

### 7.3 Agent Tool 执行

```text
agent identity + human/service delegator
→ approved use case and versioned components
→ goal, tenant/data/tool/egress/cost scope
→ typed tool request
→ policy and required deterministic approval
→ sandbox/resource enforcement where applicable
→ execution through scoped short-lived credential
→ protected security-relevant trace
→ output and post-condition validation
→ deterministic stop/rollback/manual recovery where risk requires
→ independent verifier for high-impact/adaptive claims
```

低影响辅助系统不需要全部 T4 机制，但每个生产 Agent 都必须被盘点、认领、限定范围、监控并可归因。高影响系统不能修改自己的 Policy、Approval Authority、Credential、Evidence 或 Verifier。

### 7.4 事件与恢复

```text
qualifying alert/report
→ establish command and secure communication
→ preserve evidence and establish reliable scope
→ revoke identity/key and contain at trusted boundary
→ assess tenant, privacy, legal and customer impact
→ quarantine compromised artifact/path/node/device/service
→ restore or rebuild from known-good state
→ verify identity, artifact, tenant isolation, data and monitoring
→ authorize reopening independently
→ notify as required and track remediation/retest
```

## 8. 失败模式矩阵

| 依赖失效 | 不安全行为 | 必须设计的收口方式 |
|---|---|---|
| Identity/Federation 不可用 | Fail-open 或无限复用 Stale Session | 只在合理场景使用有时限 Cache；拒绝 Privileged/State-changing Access；测试 Emergency Path |
| Policy Service 不可用 | Local Component 默认允许 | Signed/Versioned Policy Cache + Expiry；默认 Deny/Quarantine；显式 Degradation |
| Controller/Scheduler Stale 或网络分区 | Desired/Actual Tenant State 偏离 | Versioned State、Lease/Epoch、Reconciliation、Mismatch Quarantine 与 Manual Recovery |
| Fabric/DPU Manager 不可用 | Stale P_Key/VRF/DPU Assignment 静默保留 | 冻结高风险 Reallocation、独立 Path Test、Recovery Authority 与 Cleanup Evidence |
| KMS/HSM/PKI 不可用 | 绕过 Key Policy 或使用 Embedded Secret | Controlled Degradation、Protected Recovery Key、合理且有时限的 Cache、测试 Recovery |
| Registry/Build/Provenance 不可用 | Unverified Artifact 被准入 | 只允许有到期时间的 Trusted Cached Set，或阻断 Admission；若 T0 失败，紧急决定仍不符合 |
| Telemetry/Evidence Pipeline 不可用 | 把观测缺失解释为安全 | 发现 Source Loss、安全情况下 Local Buffer、限制高影响动作、恢复后 Reconcile |
| Backup/Recovery Dependency 不可用 | 从不可信或不完整状态恢复 | Dependency-aware Plan、Alternate Root/Source 与测试 Manual Path |
| Agent Verifier 不可用 | Agent 自行确认完成 | 高影响/自适应 Claim 保持未验证；停止、排队或要求合格人工验证 |

## 9. 服务画像差异

| 画像 | 架构重点 |
|---|---|
| GPU-IaaS | Tenant-correct API、明确 Sharing Model、Allocation Lineage、Host/GPU/Fabric/Storage Cleanup 与 Abuse/Capacity |
| Bare Metal | BMC/OOB、Firmware、Provider Credential Removal、Dedicated/Shared Path Statement、Sanitization 与 Custody |
| Managed Kubernetes | Private API/etcd、RBAC/Admission、CNI/CSI/Device Plugin/Operator、Workload Identity、Node Response 与 Restore |
| Managed Slurm/HPC | Controller/Database/Auth、Account/Partition/QOS、Prolog/Epilog/SPANK/Module、Shared Storage/Fabric、Accounting/Recovery |
| Model Training | Purpose/Rights、Data/Experiment/Model Lineage、Poisoning/Integrity、Safe Checkpoint、Temp/Cache Cleanup、Export/Deletion |
| Model Serving | Endpoint/Model Auth、Tenant Routing/Cache/Session Isolation、Extraction/Abuse、Rate/Cost/Capacity、Fallback/Rollback |
| Agent Platform | Delegation、Component Provenance、Context Separation、Typed Tool、Policy、按影响增加 Approval/Stop、Trace、Revocation 与 Independent Verification |
| Sovereign/Regulated | Jurisdiction-bounded People、Identity、Key、Data、Support、Telemetry、Backup、Supplier、Response、Recovery 与 Evidence |

## 10. 实施顺序

1. 定义 Service Profile、Boundary、Responsibility、Identity 与 Stable ID。
2. 移除 Public/Tenant 对 Provider Administration、Fabric 与 BMC/OOB 的直接可达。
3. 建立 Critical Inventory、Root Protection、Required Telemetry、Incident Command 与 Recovery Source。
4. 实施 Tenant-correct API Authorization 与 Desired/Actual Reconciliation。
5. 为每种 SKU 声明并测试 Accelerator、Fabric、Storage 与 Support Isolation。
6. 加固 Kubernetes/Slurm、Workload Identity、Artifact Admission、Node Response 与 Cleanup。
7. 建立 Data/Model Lifecycle、Source-to-deploy Provenance、Revocation 与 Recall。
8. 产品化 Evidence、Negative/Failure Test、Restore/Rebuild/Sanitization 与 Assurance。
9. 在合理场景增加 T3 Dedicated、Attested、Confidential 或 Sovereign Assurance。
10. 只有在 Approval、Stop、Rollback、Trace 与 Verifier 可度量后增加 T4 Adaptive Automation。

## 11. 架构反模式

- 把文档或 Dashboard 称为“统一控制平面”，却没有实际可部署 Enforcement 与 Evidence；
- 把 Network Location 或 Kubernetes Namespace 当作 Identity 或完整租户隔离；
- 把 Time-sliced GPU 当作 Memory/Fault-isolated Tenant；
- 把 MIG 或其他硬件分区描述为 Full-device/Full-host Dedication；
- 用 VPC 或 NetworkPolicy 证明 RDMA、DPU、Storage 或 BMC 隔离；
- 在 Tenant Workload 使用 Shared Provider Identity 或 Broad Metadata Credential；
- Central Policy/Evidence Service 失效时 Silent Fail-open；
- 不看 Source/Key-policy/Compatibility/Admission 就接受所有 Signed Artifact，或没有明确要求却拒绝所有 Unsigned Artifact；
- Agent 权限无边界，或自行审批/验证；
- Evidence 只保存在被评估系统内；
- Backup 从未 Restore、Sanitization 从未验证、Recovery 没有 Reopening Gate；
- Risk Decision 覆盖原始 Failed Control Result。

## 12. 架构就绪定义

服务架构只有同时满足以下条件才算就绪：

- 准确 Boundary、Profile、Version、Identity 与 Responsibility 有记录；
- 每个适用 T0 均独立 `VERIFIED`；
- Policy/Tenant Context 到达每个必需 Enforcement Point；
- API、Host/GPU、Fabric/RDMA/DPU、Storage、Support 与 OOB 的禁止路径已测试；
- Required Telemetry/Evidence Source 健康、受保护且可独立检查；
- 已知 Control-plane、Identity/Key、Artifact、Node、Region 与 Evidence-pipeline Failure Behavior；
- Restore/Rebuild、Revocation、Incident、Cleanup 与 Sanitization 演练通过；
- 面向客户的声明精确说明 Dedicated/Shared 与 Provider/Customer Boundary；
- 高影响 Agent 具备受限权限、确定性 Approval/Stop、Protected Trace、Recovery 与 Independent Verification。

实施顺序见[实践指南](PRACTICE_GUIDE.md)，准入、证据和度量见[度量与持续证明指南](METRICS_AND_ASSURANCE.md)。
