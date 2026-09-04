# NeoCloud Cyber Security 发展路线图

**周期：** 0–24 个月  
**推进模型：** 阶段门驱动、风险优先、证据驱动

## 1. 如何使用路线图

这是一份参考推进顺序，而不是日历承诺。已经开放公网 API 和多租户 GPU 的初创服务商可能需要在数天内补齐 T0；完全专属的内部集群也可能合理地判定部分控制不适用。进展应以独立验证的安全结果和真实暴露下降衡量，而不是文档数量或采购工具数量。

先选择服务画像，定义生产边界与责任人，再评估全部 T0/T1。服务特有威胁可以进入风险台账，但任何数字评分都不能覆盖跨租户、Root Key、公网管理面、安全清除、日志、响应或恢复硬门槛失败。

每个阶段都有**退出门槛**。不同阶段工作可以并行，但在上一阶段门未满足前，不应宣称达到下一成熟度。

## 2. 24 个月目标状态

成熟 NeoCloud 应能够证明：

- 一个权威关系图连接 Service、Tenant、Identity、Workload、Node、GPU、Fabric、Data/Model、Artifact、Control、Risk 与 Evidence；
- 人员使用抗钓鱼/JIT 权限，Workload/Agent 使用经过证明的短期身份；
- 租户正确策略在 API、Controller、Scheduler、Host、GPU、Fabric、Storage、Registry、KMS 和 Tool 边界执行；
- 每种商业 SKU 都有明确且持续验证的隔离性质；
- 软件/模型/固件供应链有清单、Provenance、签名、分阶段发布与召回；
- 数据/模型全生命周期受保护，责任、驻留、保留、删除和导出对客户清晰；
- 遥测和证据完整且租户安全，检测和 Playbook 经过测试；
- Credential Revocation、Containment、Rebuild、Restore、Failover、Sanitization 和客户协同经过演练；
- AI 辅助防御有明确权限、审批、成本、回滚和 Verifier；
- 保证材料处于当前状态，并精确说明范围和例外。

## 3. 阶段 0——第 0–7 天：建立指挥

### 目标

任命可追责 Owner，建立唯一安全决策通道；识别可能造成跨租户、全局或不可恢复损害的紧急条件；在建立基线期间保护证据并防止无控制变更。

### 交付物

- 高管风险 Owner、CISO/安全负责人、服务 Owner 和 Incident Commander 轮值；
- 客户服务、生产 Region、Orchestrator、GPU Sharing、Fabric、BMC/OOB、IdP、Signing Root、Registry、KMS 和关键 Supplier 初始清单；
- Emergency Contact、独立安全通信和 SEV-0/SEV-1 标准；
- 对新公网管理面、Root/Signing Key、新 GPU Sharing、Fabric Topology 和未 Review 生产镜像实施冻结或审批；
- 轮换 Owner 未知、共享或离职人员遗留的高权限 Credential。

### 退出门槛

- 所有生产服务和关键 Root 均有 Owner；
- 已知公网服务商管理接口都具备强认证并完成必要性决策；
- 具备 24×7 吊销高权限、隔离服务和召集事件指挥的路径。

## 4. 阶段 1——第 8–30 天：停止关键暴露

### 目标

满足最紧急 T0，建立身份、控制面、租户和物理分配的最低可见性，使事件隔离不再依赖临时发挥。

### 工作包

**身份与信任根**

- 服务商高权限和支持的 Tenant Owner 强制抗钓鱼 MFA；
- 清理共享账户，盘点 Service/Automation Credential，保护 Break-glass；
- 关键服务使用集中 KMS/Secret Store，限制并审计 Signing/Root Key。

**控制面与网络**

- 服务商管理迁移到 PAM Gateway 或 Private Path；
- 验证最高风险 API 的 Object-level Tenant Authorization；
- 分离 Public、Tenant、Provider Management 与 BMC/OOB；
- 识别 InfiniBand/RDMA/NVLink/DPU 边界，隔离含糊绑定。

**计算与数据**

- 发布每种 SKU 的临时隔离矩阵：Host、GPU、Memory、Fabric、Storage、Support；
- 禁用或限制无法满足声明的 Sharing Mode；
- 定义并实测 Tenant 切换时最低 GPU/Local Disk Cleanup；
- 把 Signing Key、客户 Model/Checkpoint 和 Provider Control Plane Data 列为 Crown Jewel。

**遥测与响应**

- 集中关键 IdP、Privileged Access、API/Control Plane、Kubernetes/Slurm、BMC/Fabric Change Log；
- 防止 Source System 普通管理员篡改关键日志；
- 建立 Credential/Root Compromise、Control Plane Takeover、Cross-tenant Exposure 和 Destructive Automation Playbook。

### 退出门槛

- 所有适用 T0 有 Owner、Scope、Implementation State、Evidence Requirement 和 Target Date；
- 不存在未知 Critical Root、Privileged Identity 或 Production Management Path；
- 可识别某租户当前资源并紧急吊销其访问；
- 已知跨租户隔离不确定性被阻断、改为独占或明确升级，不能静默接受。

## 5. 阶段 2——第 31–90 天：建立基础

### 目标

生产范围完成 T0 并建立 T1；用权威清单、责任和实测流程替代口口相传；建立后续自动化所需的遥测与证据。

| 工作流 | 90 天交付物 |
|---|---|
| 治理 | 安全章程、Service Profile、Risk/Exception、Shared Responsibility、Customer Commitment Register |
| 资产 | 有 Owner 且持续对账的 Service/Asset/Identity/Data/Model/Dependency Inventory |
| 身份 | Federation、MFA、JML、Privileged JIT Roadmap、Break-glass Test、Service Account Lifecycle |
| API/控制面 | Inventory、AuthN/AuthZ Standard、Rate/Quota、Private Admin、Audit 与 Change Trace |
| 计算/Fabric | SKU Isolation、Host Baseline、Placement、Reset/Sanitization Test、Network/P_Key Owner |
| Kubernetes/Slurm | Hardened Control Plane、RBAC/Account Review、Admission/Job Control、Private Admin、Backup |
| 数据/模型 | Classification、Encryption/Key Ownership、Residency/Retention/Deletion、Access/Lineage Minimum |
| 供应链 | Approved Source、Image/Model Registry、SBOM、Signature/Provenance Pilot、Emergency Rollback |
| 漏洞 | Asset-linked Scan、Exploitability SLA、Emergency Patch、Firmware/Driver Coverage |
| 检测/IR | Log Coverage Dashboard、Core Detection、Severity、On-call、Evidence Handling、Tabletop |
| 韧性 | Dependency Map、SLO/RTO/RPO、Critical Control Plane Immutable Backup、Restore/Revocation Test |
| 滥用 | AUP、Tenant Risk Tier、Quota、Rate Control、Prohibited-use/Escalation Process |

### 退出门槛

- 每项适用 T0 均独立 `VERIFIED`，否则阻断服务上线；
- 至少 95% Critical Asset 和 100% Privileged Identity 有 Owner 与当前记录；
- Critical Log Source Coverage 至少 95%，缺口有 Owner 和日期；
- 完成 Restore、Privileged Revocation 和一个 Cross-tenant Incident Exercise；
- 客户可以获取 Shared Responsibility 与安全联系路径。

## 6. 阶段 3——第 3–6 个月：控制产品化

### 目标

把人工控制转换为可复用 Paved Road；将策略决定和证据生成放入正常供应/部署路径；减少静态 Secret、Config Drift 和逐服务例外。

### 核心项目

1. **Workload Identity：** 为 Service、Job、Node、Agent 颁发短期、经过证明的 Identity，逐步消除嵌入 Credential。
2. **Policy-as-Code：** 建立 Tenant Authorization、Isolation SKU、Region、Data Class、Artifact Admission、Egress、Tool Use 和 Approval 通用策略。
3. **Trusted Artifact Pipeline：** 保护 Source、隔离 Build、SBOM、Provenance、Signature、Registry Policy 和 Admission Verification。
4. **Desired/Actual Reconciliation：** 持续对比 API Intent 与 Kubernetes/Slurm、Host、GPU、Storage、Network、DPU 和 P_Key。
5. **Runtime/Node Response：** Host/Runtime Telemetry、Quarantine 和 Immutable Node/Rapid Rebuild。
6. **Evidence Automation：** 从策略和基础设施直接生成 Evidence ID、Hash、Scope 和 Freshness。
7. **Tenant Trust/Abuse：** 将 Onboarding Risk、Quota、Egress、Behavior 和 Appeal 融入运营。
8. **Secure Engineering：** 把 Threat Model、Security Test、Rollback 和 Observability 设为发布标准。

### 退出门槛

- 新 Tier-1 服务统一接入 Identity、Logging、Secret、Policy、Artifact 和 Incident 能力；
- 至少 80% 生产 Workload 使用短期或 Brokered Credential；
- 高影响 Artifact 有 Inventory，关键 Build 产生 SBOM/Provenance；
- Tenant/Fabric/GPU Assignment 错配可以检测并 Paging；
- 优先控制证据自动生成且经过正确性 Review。

## 7. 阶段 4——第 6–12 个月：生产成熟

### 目标

关闭 T2 缺口，并在攻击、故障和恢复条件下证明有效；使客户保证准确可重复；建立可持续运营节奏。

### 核心项目

- Workload Identity/Policy 覆盖所有生产服务；
- 授权测试 GPU Memory Reset、Partition/Dedication、Device Error 和 Placement Transition；
- 端到端验证 Ethernet、Storage、InfiniBand/RDMA，包括 Controller Misconfiguration 和 Stale Assignment；
- 建立 ATT&CK/ATLAS Detection Engineering 与 Purple Team；
- Provider Support 使用 JIT/JEA、Session Evidence 和 Tenant-safe Access；
- 漏洞平台纳入 Exploitability、Exposure、Asset Criticality 以及 Firmware/BMC/DPU/Driver/Operator；
- 演练 Cross-tenant Data、Signing/Root、Scheduler/Control-plane 和 Malicious/Destructive Agent；
- 演练 Region/Major Dependency DR、Immutable Backup Restore 和 Known-good Rebuild；
- 形成包含 Scope、Control Status、Test、Exception 和 Responsibility 的客户保证包。

### 退出门槛

- T2 Verified Completion 达到组织目标，T0 失败为零，Critical Exception 无逾期；
- 所有生产画像的 Cross-tenant Negative Test 和 Restore/Rebuild 通过；
- Priority Detection Coverage/Alert Quality 达标并接受独立抽样；
- Customer Notification、Evidence Exchange 和 Support Access 经过演练；
- Privileged/Workload Revocation 与 Tenant/Resource Isolation 达到 SLO。

## 8. 阶段 5——第 12–18 个月：高保证

### 目标

为敏感、受监管、专属或主权工作负载增加有必要性的控制，提高对信任根、隔离、供应链和内部风险的信心。

### 核心项目

- 明确覆盖 GPU/Fabric/Control Plane 的独立渗透与架构测试；
- Dedicated Host/Fabric/Storage 和 Regulated Service Profile；
- Measured Boot、Node/Device Attestation 与 Policy-governed Key Release；
- 对适用威胁模型提供 Confidential Computing；
- Region/Jurisdiction-specific Key Custody、Support Personnel、Telemetry 和 Recovery；
- Root/Signing、High-impact Release、Destructive Fleet Action 和 Sensitive Support 双人控制；
- Hardware/Firmware/Driver/Operator/Remote Support/Supplier Assurance；
- 兼顾员工隐私和正当程序的 Insider Risk；
- Cryptographic Agility、Signing Root Rotation 和 Compromise Recovery Exercise。

### 退出门槛

- T3 声明有 Service-specific Independent Evidence；
- Sovereign/Regulated Boundary 覆盖 Data、Identity、Key、Support、Telemetry、Backup 和 Supplier Flow；
- Root/Key Compromise 和 Confidential Workload Recovery 经过演练；
- Dedicated/Isolation 使用精确资源边界，不使用模糊营销词。

## 9. 阶段 6——第 18–24 个月：受控自适应安全

### 目标

引入持续控制监控和边界严格的 AI 辅助防御，在不让自动化成为无控制信任根的前提下缩短 Detection、Evidence、Triage 与 Safe Remediation 闭环。

### 核心项目

- 持续评估 Identity、Policy、Asset、Vulnerability、Artifact、GPU/Fabric 和 Evidence State；
- 安全 Agent 轨迹采用 `Goal → State Summary → Evidence → Reasoning → Action → Observation → Verifier → State Update`；
- Planner 与 Executor 分离，主动测试必须 Explicit Authorization 和 Sandbox；
- Typed Tool、Least Privilege、Short-lived Credential、Immutable Scope、Budget 和 Deterministic Stop；
- Destructive、External、Customer-impacting、High-cost 或 Irreversible 行为 Human Approval；
- 只有 Independent Verifier 通过后，Control/Incident/Remediation 才能变成 `VERIFIED`/Closed；
- Replayable Environment 与 Signed Trace 支持 Regression、Evaluation、SFT/RL Data 和 Failure Analysis；
- 自主等级逐步提升：Recommend → Draft → Execute Reversible Low-risk → Execute Bounded Containment；禁止类别永不自主执行。

### 退出门槛

- 自动化具备 Precision、Rollback Success、Approval-bypass、Policy-violation 和 False-completion 指标；
- Agent 无法修改自身 Goal、Scope、Tool、Credential、Policy、Approval Authority、Evidence 或 Verifier；
- 每条自动隔离/修复路径有实测 Kill Switch 和 Manual Recovery；
- 自适应控制降低 Verified Time-to-containment 或成本，同时不提高重大事件/Unsupported Claim。

## 10. 并行工作流与 Owner

| 工作流 | Accountable Owner | 关键协作方 | 主要结果 |
|---|---|---|---|
| 治理与保证 | CISO / Risk Executive | Legal、Privacy、Audit、Product | 决策、义务、证据和例外明确 |
| 身份与策略 | Identity/Platform | Security Architecture、Product、IT | 统一人员/工作负载/租户/Agent 信任模型 |
| API 与控制面 | Product/Platform Engineering | AppSec、SRE、IAM | Tenant-correct、Private、Resilient、Auditable |
| Compute/GPU/Runtime | Compute Platform | Virtualization、Kernel、SRE、Vendor | 隔离、重置、加固和重建可证明 |
| Network/Fabric/OOB | Network/Platform Security | HPC、Facility、Vendor | 端到端租户与管理平面隔离 |
| Kubernetes/Slurm | Orchestration Platform | Service Team、SRE、Security | 安全调度、准入、作业与 Controller Lifecycle |
| Data/Model/Privacy | Data/AI Platform | Privacy、Product、Customer Team | 数据/模型 Lifecycle 与 Provenance |
| Supply Chain/Engineering | Engineering Productivity | AppSec、Build、Procurement | 可信 Source-to-deployment 与 Recall |
| Detection/Response | SecOps / IR | Platform、Legal、Support | 完整遥测、实测检测、快速安全恢复 |
| Abuse/Customer Trust | Trust & Safety / Product | Fraud、Legal、Support、SRE | 安全准入、容量保护、公平处置 |
| Resilience/Facility | SRE/Infrastructure | Network、Facility、Security | 连续性、重建、备份和物理信任根 |

小型组织可以兼任，但责任与独立验证不能消失。

## 11. Build / Buy / 平台化建议

**自行开发或深度集成**表达 NeoCloud 特有租户/拓扑的能力：Tenant-aware Authorization、Provisioning Reconciliation、GPU/Fabric Placement Evidence、Reset/Sanitization、Scheduler Policy、Model/Checkpoint Lifecycle、Agent Tool Mediation 和 Service-specific Containment。

**采购或采用成熟托管/开源组件**处理标准化问题：IdP/MFA、PAM、KMS/HSM、Secret Manager、Vulnerability Scanner、SIEM/Data Lake、EDR/Runtime、Ticket、PKI、Backup、DDoS/WAF 和 Artifact Signing Infrastructure。

**责任不能外包。** 厂商 Dashboard 不能证明完整服务边界已覆盖。采购必须要求可导出 Log/API、租户安全、HA/Degraded Mode、明确 Data Handling、独立测试、安全更新、事件通知、Exit/Migration，并与稳定身份集成。

## 12. 优先级方法

按以下顺序排期：

1. T0 生产门失败；
2. 已确认 Active Compromise 或 Cross-tenant Path；
3. Root of Trust、Fleet-wide Blast Radius 或 Irrecoverable Data Loss；
4. 外部可达且可利用路径；
5. 高价值 Data/Model 或 Destructive Authority；
6. 导致范围无法判断的 Control/Evidence Blind Spot；
7. 重复运营失败或过期例外；
8. 可消除大量人工风险的平台控制；
9. 由服务承诺或量化价值支撑的 T3/T4。

可以估算工作量和依赖，但不能让低成本卫生项长期挤掉困难的 T0 隔离问题。

## 13. 项目风险与对策

| 风险 | 对策 |
|---|---|
| 先买工具、后找问题 | 采购前定义 Service/Control/Evidence Outcome 和 Integration Owner |
| 合规表演 | 要求部署范围证据、Negative Test 和独立验证 |
| 隐藏共享责任 | 发布 Per-service Matrix 并测试 Incident/Offboarding Handoff |
| 安全总在末期阻塞产品 | 尽早提供 Identity、Policy、Artifact、Logging、Isolation Paved Road |
| 例外变成架构 | Expiration、Owner、Customer Impact、Compensating Control、高管可见 |
| 中央策略/日志成为单点 | Distributed Enforcement、Bounded Cache、Protected Buffer、Degraded Test |
| AI 自动化虚假完成 | State Machine、Immutable Evidence、Independent Verifier、False-completion Metric |
| 敏感日志形成新风险 | Minimization、Tenant Partition、Masking、Role Separation、Retention、Access Audit |
| GPU/Fabric 假设不测试 | Service-specific Isolation Matrix 和 Authorized End-to-end Negative Test |
| 高速增长超过资产盘点 | Event-driven Registration、Reconciliation 和绑定 Service ID 的 Launch Gate |

## 14. 首月高管决策

领导层需要明确决定：生产 Service/Region 范围；何种 Isolation Mode 可承载何种 Data Class；是否允许 Provider Admin 公网暴露；Root/Signing/KMS/BMC/Fabric Owner；T0 Exception Authority/Maximum Lifetime；Notification Commitment；Support Access 与 Customer Visibility；默认 Tenant Identity/MFA/Egress/Quota；Evidence Retention 与 Assurance；RTO/RPO 和 Known-good Rebuild；禁止 Agent 自主执行的行为类别；首 90 天 Owner 与资源。

没有这些决策，技术团队无法可靠落地控制，因为信任边界和可接受失败尚未定义。
