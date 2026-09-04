# NeoCloud 网络安全实践指南

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 面向实施的项目草案  
**适用读者：** 管理层、安全、平台工程、SRE、网络/Fabric、Kubernetes、Slurm/HPC、数据与 AI、机房、支持、Trust & Safety、隐私、风险与保证团队

本指南把[白皮书](WHITEPAPER.md)、[安全基线](SECURITY_BASELINE.md)、[参考架构](REFERENCE_ARCHITECTURE.md)和[发展路线图](ROADMAP.md)转化为可执行的运营模型。本文保持厂商中立；技术和产品名称只是示例，不能自动证明控制有效。

## 1. 从具体服务与信任决策开始

每个生产服务建立一套独立、版本化、可审计的评估包，至少包含：

1. Service Profile、准确合同边界、Environment、Region、Version 与客户承诺；
2. 业务、技术、安全、数据和事件的唯一可追责 Owner；
3. Tenant、Identity、Data/Model、API/Control Plane、Orchestration、Host/GPU、Storage、Ethernet/RDMA、DPU、BMC/OOB、Supplier、Support、Evidence 与 Recovery Boundary；
4. 全部适用控制，以及每个经过 Review 的 Not-applicable Decision；
5. Threat Model、攻击者假设、灾难性失败路径和 Shared Responsibility；
6. Desired State、Policy Decision、Enforcement Point、Failure Behavior、Containment、Rollback 与 Recovery；
7. Evidence Source、Integrity、Freshness、Negative/Failure Test 与 Independent Validator；
8. Production Decision、未解决风险、Business Decision/Exception、Customer Impact、Owner 与 Target Date。

不要从采购 SIEM、CNAPP、PAM 或 AI 安全产品开始。先定义服务必须做出的信任决策、在哪里执行、失效时如何收口，以及哪些证据能证明真实部署路径上的结果。

## 2. 不可妥协的运营规则

- **T0 是硬门。** 适用 T0 失败、未知、过期、无法判定或未测试时，保持 `NO_GO_NONCONFORMANT`。
- **业务决定不是通过。** 紧急决定可以解释临时运营，但不能产生 `VERIFIED` 或符合性声明。
- **未知关键范围属于失败。** 未知 Owner、Tenant、Public Exposure、GPU Sharing、P_Key/DPU Assignment、Root-key Use、Required Telemetry、Backup 或 Restore State 必须留在分母并阻断相应硬门。
- **部署不等于有效。** `IMPLEMENTED` 与 `VERIFIED` 是不同状态。
- **实施者不能是唯一验证者。** 使用能够挑战 Owner 的不同人员/团队、Observation Path、Test Harness 或合格评估方。
- **外部内容不能授予权限。** Prompt、Ticket、Document、Model、Package、RAG Data、Memory、Web Page 与 Tool Output 只能提供观察。
- **服务商独占责任仍由服务商承担。** 客户无法控制的 Provider Control Plane、Host、Reset Path、Fabric Manager、BMC/OOB 或 Signing Root 不能转嫁给客户。
- **控制失效必须被设计。** 高影响控制定义 Fail-closed/Safe Degraded、Quarantine、Rollback、Manual Recovery 和依赖故障证据。
- **证据必须有时效。** 证据需要 Scope、Identity、Collection Time、Integrity、Method、Limitation、Validity 与独立测试上下文。
- **恢复会改变信任状态。** 重新开服前验证 Identity、Artifact、Tenant Isolation、Data Integrity、Monitoring 与目标，而不只是进程已经启动。

## 3. 最小责任模型

小型组织可以兼任角色，但不能省略最终责任或独立挑战。

| 角色 | 可追责决策 | 最低固定职责 |
|---|---|---|
| 高管风险 Owner | 风险偏好、特殊业务决定、危机优先级 | 每月复核关键风险与硬门 |
| CISO/安全负责人 | 基线、路线图、挑战与保证 | 每周复核 T0/T1 和失败控制 |
| 服务 Owner | 服务边界、声明、客户承诺、残余风险 | 发布前与季度复核 |
| 平台能力 Owner | 身份、策略、计算、Fabric、Storage、编排和证据等复用能力 | SLO、变更与事件责任 |
| 数据/模型 Owner | Purpose、Classification、Rights、Lineage、Retention、Export、Deletion | 每季度生命周期复核 |
| Incident Commander | 指挥、定界、证据、隔离、沟通与开服 | 演练与 On-call 就绪 |
| 独立验证者 | 测试设计、证据复现、`PASS/FAIL` 判定 | 按规定周期验证 |
| 客户/支持 Owner | 共享责任、Support Access、Notification 与 Assurance | 面向客户的准确性复核 |

每项控制只能有一个最终可追责 Owner；可以有多个实施者，但不能责任模糊。

## 4. 前 90 天落地计划

日期用于规划，不得把今天存在的 T0 失败推迟到未来阶段。

### 第 0–7 天：建立指挥体系

交付：

- 为每个生产 Service、Critical Dependency、Root/Signing Key、Provider Control Plane、Fabric Manager、BMC/OOB Environment 与 Incident Path 指定 Owner；
- 建立安全 Incident Channel、Severity Matrix、On-call Escalation、Emergency-decision Record 和撤销/隔离权限；
- 建立第一版 Service、Critical Asset、Critical Identity、Public Exposure 与 Crown Jewel Inventory；
- 对新 Public Admin Interface、Sharing Mode、Root/Fabric Change 与未审查 Production Artifact 设置冻结或显式审批；
- 轮换或禁用未知、共享、无人认领或离职人员遗留的特权 Credential。

退出条件：服务商可以建立指挥、撤销特权、识别活动租户资源，并在可靠边界隔离一个服务。

### 第 8–30 天：移除关键暴露

优先完成：

- 为适用 Provider Privilege 与高影响 Tenant-owner Access 启用批准的抗钓鱼 MFA；
- Provider Administration 私有化，BMC/OOB 走隔离路径；
- 对关键 API 执行 Object/Action/Tenant/Purpose/Context Authorization Test；
- 为每种 Commercial Compute SKU 明确隔离声明；
- 隔离边界不清晰的 GPU Sharing、RDMA/P_Key、DPU、Storage、Support 或 Reassignment；
- 保护并验证 KMS/HSM、Signing Root、Secret、PKI 与 Break-glass 的恢复；
- 为 Identity、API/Control Plane、Kubernetes/Slurm、Host/GPU/Fabric/BMC、Key、Artifact、Support 与高影响 Agent 建立受保护的必需 Telemetry；
- 建立 Cross-tenant Access、Root Compromise、Control-plane Takeover、Destructive Automation 与 Irrecoverable Data Risk Playbook。

退出条件：每个适用 T0 都有 Scope、Owner、当前状态、Evidence Requirement、Validator 和有日期的 Containment/Remediation，并且没有失败硬门被显示为健康。

### 第 31–60 天：形成权威状态

建设：

- Service、Asset、Identity、Dependency、Data Flow、Model、Artifact、Key、Supplier 与 Support Inventory；
- Shared-responsibility Matrix 与客户安全联系人；
- Joiner/Mover/Leaver、Service Account、Workload Identity、Agent、Certificate 与 Secret Lifecycle；
- 与真实 Asset 和 Tenant/Service Context 关联的 Vulnerability/Exposure Discovery；
- Data/Model Purpose、Rights、Classification、Residency、Retention、Export、Deletion 与 Backup Requirement；
- Backup/Rebuild-source Inventory 和依赖映射；
- 对 Tenant、Scheduler、Host、Accelerator、Network/Fabric、DPU、Storage、Quota、Artifact 与 Policy 执行 Desired/Actual Reconciliation。

退出条件：Independent Discovery Coverage 可度量；Unknown/Unowned Resource 明确显示为缺陷；关键未知对象不能从报表中消失。

### 第 61–90 天：验证基础能力

执行：

- 对所有适用 T0 进行独立验证；
- Privileged-access Denial、Expiry、Emergency Revocation 与 Break-glass Test；
- 覆盖 API、Scheduler、Host/GPU、Storage、Ethernet、InfiniBand/RDMA、DPU、Telemetry 与 Support 的跨租户禁止路径测试；
- 在相关 Hardware/Firmware/Driver/Sharing Variant 上执行代表性 Accelerator 与 Local-media Reset/Sanitization Test；
- Kubernetes/Slurm Controller Restore 或 Known-good Rebuild；
- 一次包含 Reliable Scope、Customer/Legal/Privacy Notification、Containment、Recovery 与 Reopening 的完整 Incident Exercise；
- 一次 Critical Data/Model Restore，以及一次 Tenant Offboarding/Export/Deletion Exercise；
- 一份服务范围明确的 Shared-responsibility 与 Assurance Package。

退出条件：所有适用 T0 均被独立 `VERIFIED`；范围内 Critical Asset 与 Privileged Identity Owner 覆盖为 100%；T0 Required Telemetry Source 100% 健康且可查询；Priority Discovery 与非硬门 Telemetry Coverage 具有明确分母，参考目标至少 95%；失败演练均有可追责 Containment 与 Remediation。

## 5. 每项控制采用相同实施生命周期

### 5.1 确定范围

记录 Service/Profile、Environment、Region、Version、Tenant、Asset、Identity、Data Class、Supplier、Dependency 与 Excluded Component。“全局”但没有真实 Population 不构成有效范围。

### 5.2 分析威胁与失败

说明 Attacker/Compromised-subject Assumption、允许和禁止路径、Cross-tenant、Root、Destructive、Privacy、Sovereignty、Availability Failure、Dependency Outage、Stale/Partial Controller State、Rollback/Recovery、Evidence Tampering 与 Verifier Failure。

### 5.3 定义控制契约

```text
subject + delegation + action + resource + tenant + purpose
+ context + policy version
→ allow | deny | approve | quarantine + obligations
```

Obligation 可以要求 Dedicated Placement、Restricted Egress、Masking、Dual Approval、Session Evidence、Quota、Attestation、Post-action Verification 或 Cleanup。

### 5.4 落实执行与失败行为

将 Prevention Enforcement 放在靠近资源的位置。中央 Policy Service 可以分发决策，但 API Gateway、Scheduler、Node、KMS、Registry、Fabric、Storage 与 Tool Boundary 在中央服务故障时不得静默 Fail-open。定义 Stale-decision Limit、Local Cache、Safe Degradation、Quarantine、Rollback 与 Manual Recovery。

### 5.5 生成证据并独立验证

从真实部署路径生成 API/Configuration Export、Authorization Decision、Protected Runtime Event、Verified Attestation、Desired/Actual Reconciliation、Prohibited-path/Failure Test、Revocation/Restore/Rebuild/Sanitization Trace、Hash 与 Independent Observation。

验证者确认 Scope 与 Freshness、复现断言、测试相关禁止路径或失败，并返回 `PASS`、`FAIL`、`INCONCLUSIVE` 或 `NOT_TESTED`。只有 `PASS` 可以产生 `VERIFIED`。

### 5.6 运营与重验证

在 Evidence Expiry、Material Release、新 Service/SKU/Region、Sharing/Isolation Change、Controller/Orchestrator/Firmware/Driver Update、Identity/Key/Policy Change、Supplier/Data-flow/Support Change、Agent-authority Expansion、Incident、Failed Control、Restore/Rebuild 或无法复现时重验证。

## 6. 十八个安全域的实施模式

| 安全域 | 最低实施 | 必做有效性测试 | 强证据 |
|---|---|---|---|
| GOV | Charter、Service/Control Owner、Obligation、Risk、Decision/Exception、Independent Assurance | 过期决定和无 Owner 服务不能显示为健康 | 范围明确的批准决定与当前独立复核 |
| ASM | API 驱动的 Service/Asset/Identity/Data/Model/Dependency Inventory 与 Reconciliation | 发现受控 Unknown 或 Stale Assignment | 带 Owner、Tenant、Service Context 的 Desired/Actual Diff |
| IAM | Federation、抗钓鱼 Privileged MFA、JIT/JEA、Workload Identity、Lifecycle、Break-glass | 在每个必需执行点拒绝、过期和撤销 | IdP/PAM/IAM Export 与关联 Revocation Trace |
| API | Tenant-correct Authorization、Private Admin、Schema/Replay/Idempotency/Rate/Quota、Change Trace | Object/Action/Tenant Confusion 与 Partial-provisioning Failure | Request、Policy、Approval、Desired/Actual State 与 Rollback 关联 |
| NET | Plane Separation、Default Deny、Tenant-aware Ethernet/Storage/RDMA/DPU/OOB Policy | Cross-tenant/Management Path，含 Stale VRF/P_Key/DPU State | Topology、Controller State、Path Test 与 Reconciliation |
| CMP | Explicit SKU Model、Hardened Host、安全 Allocation/Reset/Error | Memory、Fault、Reset、Quarantine 与 Cross-allocation Cleanup | 关联 Tenant、Hardware、Firmware 与 Driver 的 Allocation/Cleanup |
| ORC | 私有加固 K8s/Slurm Controller、RBAC、Admission/Job Policy、Quota、Node/Plugin Security | 禁止 Privileged Workload/Job 与 Controller-loss Recovery | Policy Export、Audit、Negative Test 与 Restore/Rebuild Trace |
| DAT | Purpose/Classification、Tenant Access、Encryption/Key、Lineage、Safe Format、Deletion | Unauthorized Access、Malicious Format、Export/Deletion/Offboarding | Object Lineage、Access/Key、Cleanup 与 Restore Proof |
| KMS | KMS/HSM、Root Hierarchy、Short-lived Secret、PKI、Recovery | Root/Credential Revocation、Failed Attestation、Key Recovery | Key Inventory、Ceremony、Audit、Rotation 与 Recovery Trace |
| SSC | Approved Source、Inventory、BOM、Required Provenance/Signature、Isolated Build、Admission、Recall | 拒绝 Unknown、Revoked、Incompatible 或 Unsigned-when-required Artifact | Source-to-deploy Provenance、Policy Decision 与 Rollback |
| ENG | Threat Model、Safe Default、IaC/Policy Review、Test、Canary、Rollback | Unsafe Configuration 与 Failed Rollout | Review、Test、Deployment、Drift 与 Post-deploy Verification |
| VEM | Asset-linked Discovery、Exposure/Exploitability Priority、Patch/Firmware Lifecycle | Emergency Patch/Canary 与 Deployed-state Retest | Finding→Asset→Remediation→Retest 链路 |
| TEL | Protected Required Telemetry、Coverage/Freshness Inventory、Detection-as-code | Source Loss、Evidence Tamper、ATT&CK/ATLAS Behavior Replay | Event Sample、Health、Test、Limitation 与 Alert Quality |
| AIR | Inventory、Identity、Delegation、Impact、Component Integrity、Typed Tool、Policy | Prompt Injection、Confused Deputy、Tool Abuse、Memory/Skill Poisoning | 按风险提供 Versioned Config、Policy/Approval、Trace 与 Verifier Result |
| ABU | Trust Tier、AUP、Quota/Rate/Cost/Capacity、Egress、Case 与 Appeal | Quota Bypass、Mining、Denial of Wallet、Prohibited Egress | Onboarding Decision、Enforcement Reason、Case 与 Restoration |
| IRR | Command、Playbook、Forensic Readiness、Notification 与 Reopening Gate | Cross-tenant/Root/Agent/Availability Exercise | Timeline、Evidence Chain、Decision、Recovery 与 Independent Closure |
| RES | Dependency/SLO/RTO/RPO、Protected Backup、Safe Degradation、Rebuild/Failover | Primary Identity/Key 依赖不可用与 Region/Fabric Failure 下恢复 | Objective、Integrity/Isolation Check 与 Reopening Decision |
| PHY | Facility、BMC/OOB Isolation、Hardware/Firmware Lifecycle 与 Sanitization | Unauthorized OOB Path 与代表性 Reassignment/Decommission | Access、Firmware、Maintenance、Sanitization 与 Custody Evidence |

## 7. 服务画像上线检查

### GPU IaaS

验证 Tenant-correct API/Image Authorization；明确整卡、硬件分区、虚拟化或 Time-slicing 语义；Host、GPU/HBM/Cache、NVLink、Storage、Ethernet/RDMA、Telemetry 与 Support Boundary；Allocation Lineage；Reset/Error/Quarantine；Local-state Cleanup；Driver/Firmware Lifecycle；Node Isolation/Rebuild；Quota、Billing、Abuse 与 Egress。除非逐项说明专属与共享资源，否则不得使用“Dedicated”笼统声明。

### 裸金属 GPU

增加 Provider Credential Removal；隔离 BMC/OOB 与 JIT Support；Approved/Measured Firmware 与 Provisioning Image；专属或精确声明的 Network/Fabric/Storage；覆盖 GPU、Local Media、TPM、NIC/DPU、BMC User/Certificate 与 Fabric Assignment 的 Deprovisioning；Chain of Custody；以及重分配前与设备方法匹配的 Sanitization。

### 托管 Kubernetes

验证 Private API Server/etcd；强 Administrator/Workload Identity；Restricted Pod Security Standards；Least-privilege RBAC；适用的 Default-deny Admission/Network Policy；Tenant Namespace/Account 与 Quota；CNI/CSI/Device Plugin/Operator/Webhook/Node Privilege；Artifact Admission；Audit/Runtime Detection；Node Quarantine；etcd Backup 与 Known-good Restore/Rebuild。

### 托管 Slurm/HPC

验证私有、已修补的 Controller/Database/REST；强 Authentication；Account/Association/Partition/QOS/Reservation/Job Ownership；Prolog/Epilog、SPANK、Module、Container Runtime、Shared Storage 与 Node Credential；Queue/Priority Abuse；与 Job/Tenant Identity 关联的 Node/GPU/Fabric Placement/Cleanup；Accounting Integrity、Backup、Failover 与 Recovery。

### 模型训练

验证 Dataset Purpose/Rights/Provenance、Integrity 与 Poisoning；Experiment Identity；Code/Image/Config/Data/Model Lineage；Safe Checkpoint/Model Format 与 Restricted Deserialization；Intermediate/Cache/Secret/Temp Cleanup；Evaluation Integrity；Output/Export、Retention/Deletion、Privacy 与 Customer Ownership。

### 模型服务

验证 Endpoint/Model Authorization；Tenant-safe Routing 与 KV/Cache/Session Isolation；Prompt/Output Handling 与 Telemetry Minimization；Model Provenance/Runtime Integrity；Extraction/Enumeration/Adversarial Input；Quota/Rate/Cost/Capacity；Safe Fallback/Degradation；Rollback 与 Privacy-safe Incident Evidence。

### Agent 平台

每个生产系统都需要 Inventory、Owner、Identity、Delegator、Use Case、Component Version、Data/Tenant/Authority Scope、Impact Assessment、Monitoring 与 Incident Path。Tool-using System 增加 Typed Interface、Policy Mediation、Least Privilege、技术可行时的 Short-lived Credential、Egress/Data/Cost Control 与 Revocation。高影响或自适应系统再增加 Immutable Scope、Deterministic Approval/Stop、Protected Replayable Trace、Rollback/Manual Recovery 与 Agent 无法修改的 Independent Verifier。

### 主权或受监管服务

验证完整司法辖区边界，覆盖 People、Identity、Data、Key Release、Support、Telemetry、Backup、Supplier、Incident Response、Recovery、Deletion 与 Evidence。Storage Residency 单独不足以满足要求。

## 8. 关键工程模式

### 端到端保留 Tenant 与 Request Context

在 API Object、Message、Controller Record、Kubernetes/Slurm Object、Allocation、GPU/Fabric/Storage Rule、Log 与 Evidence 中使用稳定 Tenant/Request ID。缺失或冲突时拒绝请求，并持续比较 Intended 与 Actual State。

### 分别治理共享方式

分别记录整卡、硬件分区、虚拟化与 Time-slicing 的 Memory、Cache、DMA、Fault、Reset、Telemetry、Topology 与运营属性。Time-slicing 不提供显存或故障隔离；硬件分区不等于整卡或整机专属。必须测试准确的 Hardware/Firmware/Driver/Hypervisor/Scheduler 组合。

### 在真实路径验证 InfiniBand/RDMA 与 DPU

测试 P_Key Membership/Enforcement、RDMA Reachability、Fabric-manager Authority、DPU/NIC Assignment、Storage Access、Stale/Partial Controller State 与 Reallocation Cleanup。按 Provider Root 保护 Fabric/DPU Controller。VPC 或 Kubernetes NetworkPolicy 不能作为充分证据。

### 消除静态 Workload Credential

使用 Workload Identity、范围受限的 Short-lived Certificate/Token、Audience Restriction、Tenant/Resource Scope、Revocation，并在合理场景绑定 Attested State。Metadata 与默认 Service Identity 不得向 Tenant Workload 提供宽泛 Provider/Project Authority。

### 将 Artifact Trust 变成 Admission Decision

对 Image、Package、Model、Checkpoint、Driver、Firmware、Operator、IaC、Prompt、Policy 与 Skill 保留 Source、Build/Train Lineage、Inventory/BOM、适用的 Provenance/Signature、Scan、Policy、Revocation 与 Deployed Version。有效签名只证明发生了签名，不证明安全。

### 将 Evidence 与被评估系统隔离

关键证据导出到普通源系统管理员无法静默修改的边界，保留 Stable ID、Time Integrity、Tenant Partitioning、Access Audit、Minimization/Redaction、Retention 与 Legal Hold。缺失证据属于控制失败。

### 从 Known-good State 恢复

Root、Host、Controller、Fabric Manager 或 Build System 可信状态不确定时，优先 Revocation 与 Known-good Rebuild，而不是乐观清理。重新开服前独立检查 Identity、Artifact、Data、Isolation 与 Monitoring。

## 9. 固定运营节奏

| 周期 | 必须执行的活动 |
|---|---|
| 持续 | 技术可行时的 T0、Identity/Policy、Public Exposure、Critical Source Health、Root Use、Assignment Drift、Capacity/Abuse、Backup 与高影响 Agent Action |
| 每日 | Failed Control/Collector/Test、Unknown/Unowned Critical State、Urgent Exposure 与 Containment Backlog |
| 每周 | Vulnerability SLA、Privilege、Release、Risk Decision、Detection Failure 与 Incident Action |
| 每月 | 高管 Gate/Risk、Customer Commitment Drift、Supplier/Capacity Risk 与 Metric Quality |
| 每季度 | T0/T1 Verification、Access Review、Isolation、Revocation/Restore、Detection Replay 与适用 Agent Test |
| 每半年 | T2 Verification 与重大 Incident/Control-plane/Recovery Exercise |
| 每年 | 独立 T3 Architecture/Isolation、Regional Recovery/Rebuild、Supplier 与 Cryptographic Recovery |
| 重大变更 | 立即重新确定并验证受影响断言 |

## 10. 最低事件 Playbook 集合

每个 Playbook 必须定义 Detection、Command、Reliable Scope Query、Evidence Preservation、Containment Boundary、Identity/Key Action、Tenant/Customer Impact、Legal/Privacy Assessment、Communication、Recovery、Reopening 与 Independent Verified Closure。

至少覆盖：

1. Cross-tenant API、Storage、GPU/Cache、Telemetry、Fabric 或 Support Access；
2. Provider Root、Signing Key、KMS/HSM、IdP、PAM 或 Break-glass Compromise；
3. Kubernetes/Slurm/Controller/Operator/Provisioning Takeover；
4. BMC/OOB、DPU、Fabric Manager、Firmware 或 Supply-chain Compromise；
5. Accelerator Remanence、Unsafe Sharing、Reset 或 Error-domain Failure；
6. Malicious Model/Checkpoint/Image/Package/Driver/Operator/Prompt/Policy/Skill；
7. Destructive/Exfiltrating Agent/Tool Workflow 与 False Completion；
8. Ransomware、Region/Fabric/Storage Outage、Capacity Exhaustion 或 Backup Failure；
9. Tenant Fraud、Mining、Prohibited Workload、Quota Bypass 或 Denial of Wallet；
10. Data/Model Deletion Failure、Residency Breach 或 Customer-notification Failure。

只有技术演练证明 Isolation、Revocation、Evidence 与 Recovery Path 有效后，Playbook 才能标记 Ready。

## 11. Build、Buy 与深度集成

应自建或深度集成编码服务特定租户和拓扑语义的能力：Tenant-correct Authorization、Desired/Actual Reconciliation、GPU/NVLink/Fabric/DPU/Storage/Scheduler Evidence、Reset/Sanitization、Model/Checkpoint Safe Loading 与 Lifecycle、Agent Delegation/Tool Mediation、Containment 与 Reopening。

成熟且接口/证据清晰的能力可以采购或采用：IdP/MFA、PAM、KMS/HSM、Secret/PKI、Vulnerability/Attack-surface Management、SIEM/Data Lake、EDR/Runtime Security、Case Management、Backup、DDoS/WAF/API Gateway、Signing/Transparency。

要求可导出 API/Event、Stable Identity、Tenant-safe Behavior、Secure Update、HA 与 Safe Degradation、Incident Notification、Data Handling、Independent Test Support、Migration/Exit 和 Correlated Evidence。产品 Dashboard 不能单独证明全服务覆盖。

## 12. 尽调问题

要求服务商或供应商精确回答：

- 哪些 Host、GPU/HBM/Cache、NVLink、Network/RDMA、Storage、Telemetry、BMC 与 Support Resource 是专属或共享？
- Tenant/Request Context 如何从 API 保留到物理分配、清理与删除？
- 使用哪些 Accelerator Mode，Memory、Fault、Reset 与 Reassignment 保证如何测试？
- P_Key、RDMA、DPU/NIC、BMC/OOB 与 Fabric Controller 如何治理和独立测试？
- 谁能通过什么 JIT Workflow 访问 Customer Data/Model，留下何种 Evidence 与 Notification？
- Plaintext/Key 在哪里存在，谁控制 Key Release，Root 如何 Revocation/Recovery？
- 哪些 Artifact 要求 Inventory、Provenance、Signature、Admission、Revocation 与 Recall？
- Notification、Evidence Exchange、Restore、Export、Deletion、Residency 与 Offboarding 承诺是什么？
- 事件期间哪些控制仍分别属于 Provider、Customer 或 Shared？
- 哪些声明在什么时间、针对哪个准确 Service/Version 被独立测试，存在什么限制？

## 13. 必须拒绝的反模式

- 用一个综合分数隐藏 T0 失败；
- 把风险决定写成 `PASS`；
- 使用“Dedicated”“Isolated”“Zero Trust”“Encrypted”“Confidential”“Immutable”“Complete”却没有精确范围和证据；
- 将 VPC/Namespace 隔离作为 GPU/RDMA/Storage 隔离证明；
- 将 Time-sliced GPU 表述为显存/故障隔离租户；
- 向 Tenant Workload 暴露共享 Provider Identity 或宽权限 Metadata Credential；
- Standing Administration 与无记录 Support Access；
- 缺少 Source/Build/Key-policy/Admission Context 就接受 Signed Artifact；
- 只使用 Screenshot 或 Vendor Dashboard 作为证据；
- Backup 从未恢复，Sanitization 从未测试；
- Agent 自行批准或验证高影响动作；
- Exception 缺少 Owner、Customer Impact、Containment、Expiry 与 Remediation；
- 安全产品缺少 Service Owner、Integration Contract、Evidence Output 与 Failure Mode。

## 14. Definition of Done

服务只有同时满足以下条件，才能被表述为符合本基线：

- Boundary、Profile、Version、Responsibility 与 Customer Commitment 明确；
- 所有适用 T0 均被独立 `VERIFIED`；
- Critical Service/Asset/Identity/Root/GPU/Fabric/OOB/Data/Model/Artifact Scope 已知；
- Required Telemetry Source 健康，且已测试 Missing-source Behavior；
- Prohibited-path Isolation、Revocation、Restore/Rebuild、Incident 与 Sanitization Test 通过；
- Evidence 当前、范围明确、受保护、可复现并独立复核；
- 未解决风险具有可追责决定，且不改变控制结果；
- Monitoring 能发现 Drift，团队能够在不临时 improvisation 的情况下完成 Containment 与 Recovery。

机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)是稳定 Control ID、等级、中英文要求、Evidence/Verification Profile 与 Metric Association 的规范来源。
