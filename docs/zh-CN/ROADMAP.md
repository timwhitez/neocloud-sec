# NeoCloud Cyber Security 发展路线图

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 面向实施的项目草案  
**参考周期：** 0–24 个月

## 1. 如何使用这份路线图

本路线图用于安排专业 AI/GPU 云的安全能力建设顺序，不能作为延后当前 T0 失败的理由。日期只是规划参考，每个阶段都必须通过证据门退出。

整个项目遵循三条规则：

1. **T0 优先：** 每个适用 T0 都必须被独立 `VERIFIED`；失败、未知、过期、无法判定或未测试的 T0 始终保持 `NO_GO_NONCONFORMANT`。
2. **建设可复用机制：** Identity、Delegated Authority、Policy、Isolation、Provenance、Evidence、Response 与 Recovery 应沉淀为共享平台能力，而不是每个服务单独堆 Ticket。
3. **最后引入自动化：** 只有 Approval、Stop、Rollback、Trace、Evidence 与 Independent Verifier 的行为可度量后，才引入自适应防御。

高管可以批准一项限时的紧急业务连续性决定，但该决定不会改变失败控制结果，也不能让相关服务被描述为符合本基线。

## 2. 24 个月目标状态

成熟的 NeoCloud 安全体系应当能够：

- 识别全部范围内 Critical Service、Asset、Tenant Relation、Privileged Identity、Root、Accelerator/Fabric/OOB State、Data/Model、Deployed Artifact、Supplier 与 Dependency；
- 从 API Authorization 一直保留 Tenant/Request Context，贯穿 Scheduler、Host/GPU、Network/RDMA/DPU、Storage、Telemetry、Cleanup 与 Deletion；
- 准确声明并测试每种商业 Compute SKU 的隔离属性；
- 通过强 Identity、范围受限的 Delegated Authority 与 Revocation 治理人员、Workload、Service、Device 与 Agent；
- 从可归因来源准入、召回和重建 Software、Firmware、Infrastructure、Model、Checkpoint、Prompt、Policy 与 Skill Artifact；
- 采集全部 T0 Required Telemetry，并分别度量 Priority Source 的 Coverage、Freshness 与 Failure；
- 建立 Incident Command、Reliable Scope、Containment、Notification、Known-good Recovery 与独立验证后的 Reopening；
- 产出服务范围明确、具有时效的 Assurance，而不是一个混合合规总分；
- 在 Threat Model 与客户承诺确实需要时，运营高保证 Dedicated、Sovereign、Attested 或 Confidential-computing Profile；
- 只有当 False Completion、Scope Violation、Approval Bypass、Stop、Rollback 与 Verifier Independence 可度量时，才使用受控自适应自动化。

## 3. 项目工作流

| Workstream | 可追责结果 | 典型 Owner |
|---|---|---|
| Governance and Assurance | Service Boundary、Responsibility、Risk、Decision、Evidence 与 Independent Review | Executive Risk Owner、CISO、Service Owner、Privacy/Legal、Assurance |
| Inventory and Exposure | 权威 Service/Asset/Identity/Data/Model/Dependency；Independent Discovery 与 Drift | Platform Security、SRE、Asset/Configuration Owner |
| Identity and Policy | Human/Tenant/Workload/Device/Agent Identity、JIT、Delegation、Policy 与 Revocation | IAM、Platform Identity、Security Architecture |
| API and Control Plane | Tenant-correct Authorization、Private Administration、Safe Change 与 Failure | Product/Platform Engineering、SRE、Security |
| Compute and Orchestration | Kubernetes/Slurm、Host/Runtime、GPU Sharing/Reset、Node Response | Compute、Kubernetes、HPC/Slurm、Accelerator Team |
| Network, Fabric and OOB | Plane Separation、Ethernet/RDMA/P_Key/DPU、BMC/OOB 与 Path Validation | Network/Fabric、Hardware Platform、Facility Security |
| Data, Model and Privacy | Purpose、Rights、Access、Lineage、Safe Format、Retention/Export/Deletion | Data/AI Platform、Privacy、Security |
| Keys and Supply Chain | KMS/HSM/PKI/Secret、Source/Build/Train、Provenance、Admission、Recall | Cryptography、DevSecOps、Release、Model Platform |
| Telemetry and Detection | Required-source Health、Evidence Integrity、Detection、Threat Hunting、Assurance Pipeline | Security Engineering、SOC、Platform Observability |
| Abuse and Resilience | Tenant Trust、Quota/Cost、Egress、Capacity、Backup、Failover 与 Recovery | Trust & Safety、Fraud、SRE、Capacity、Billing |
| Incident and Crisis | Command、Forensic、Notification、Containment、Recovery 与 Lessons | Incident Response、Legal/Privacy、Customer/Support |
| Physical and Lifecycle | Facility、BMC、Firmware、Custody、Sanitization 与 Decommissioning | Data Center、Hardware、Facility、Security |

每个 Workstream 必须有一个最终可追责 Owner，并定义 Dependency、Milestone、Service Coverage、Metric、Evidence、Test 与 Exit Criteria。“由安全团队负责”不能作为最终责任模型。

## 4. 阶段 0：立即建立指挥与暴露控制（第 0–7 天）

### 目标结果

- 为 Production Service、Critical Dependency、Control Plane、Root/Signing Key、Fabric Manager、BMC/OOB 与 Incident Command 指定 Owner；
- 建立 Secure Incident Channel、Severity Model、On-call Escalation 与 Emergency Decision Record；
- 建立 Service、Critical Asset/Identity、Public Exposure 与 Crown-jewel Data/Model 的第一版 Inventory；
- 冻结或显式审批新的 Public Provider Administration、Accelerator Sharing Mode、Root/Fabric Change 与未审查 Production Artifact；
- 轮换或禁用共享、未知、孤儿或离职人员遗留的 Privileged Credential；
- 明确 Revocation、Quarantine、Isolation 与停止高风险发布的权限。

### 退出门

服务商能够建立指挥、识别正在调查的 Service/Tenant/Resource、撤销特权，并通过已知可信路径隔离服务。未知 Critical Root 或 Provider-admin Path 不得被表示为健康。

## 5. 阶段 1：T0 隔离与最低可见性（第 8–30 天）

### 目标结果

- 为适用 Provider Privilege 与高影响 Tenant-owner Access 部署抗钓鱼 MFA；
- Provider Control Plane、Kubernetes/Slurm Controller、Fabric Management 与 BMC/OOB 通过私有受治理路径访问；
- 对关键 API 执行 Object/Action/Tenant/Purpose/Context Test；
- 为每种 Commercial SKU 精确声明 Host/GPU/Cache/NVLink/Network/RDMA/Storage/Telemetry/Support 属性；
- 隔离或移除边界含糊的 Time-slicing、Hardware Partition、Virtualization、P_Key/DPU、Storage、Support 或 Cleanup 模式；
- 集中保护并验证 Root、Secret、PKI 与 Break-glass 的恢复；
- 为关键 Trust Boundary 建立受保护的 Required Telemetry 与 Source-health Monitoring；
- 建立 Cross-tenant、Root/Key、Control-plane、Accelerator/Fabric/BMC、Destructive Agent 与 Irrecoverable Data 场景的核心 Playbook。

### 退出门

每个适用 T0 都有 Scope、Owner、当前 Implementation State、Evidence Requirement、Validator 和有日期的 Containment/Remediation。任何失败或未知 T0 都不能被计为完成，也不能被综合分数覆盖。

## 6. 阶段 2：权威状态与独立验证（第 31–90 天）

### 目标结果

- 建立 Service、Asset、Identity、Dependency、Data Flow、Model、Artifact、Key 与 Supplier Inventory；
- 建立 Shared-responsibility Matrix 与客户安全联系人；
- 建立 Joiner/Mover/Leaver、Service Account、Workload Identity、Agent、Certificate 与 Secret Lifecycle；
- 将 Vulnerability/External Exposure 与真实 Asset 关联；
- 定义 Data/Model Purpose、Rights、Classification、Residency、Retention、Export、Deletion 与 Backup Requirement；
- 建立 Backup/Rebuild-source Inventory 与 Dependency Mapping；
- 对 Tenant、Scheduler、Host/GPU、Network/Fabric/DPU、Storage、Quota、Policy 与 Artifact State 执行 Desired/Actual Reconciliation；
- 对 API、Host/GPU、Storage、Ethernet/RDMA、DPU、Telemetry 与 Support 执行独立禁止路径测试；
- 执行 Privileged Revocation/Break-glass、Orchestrator Restore/Rebuild、Critical Data/Model Restore、Tenant Offboarding/Deletion 与 End-to-end Incident Exercise；
- 产出第一版 Service-scoped Assurance Package。

### 退出门

- 所有适用 T0 均被独立 `VERIFIED`；
- 范围内 Critical Asset 与 Privileged Identity Owner 覆盖为 100%；
- Required T0 Telemetry Source Health 为 100%；
- Priority Independent Discovery 与非硬门 Telemetry Coverage 具有明确分母并达到约定目标，95% 只是参考起点，不能替代硬门；
- 失败测试均有可追责 Containment 与 Remediation；
- Service Claim 与当前部署证据一致。

## 7. 阶段 3：平台化基础能力（第 3–6 个月）

### 目标结果

- 将 Workload/Service Identity 与 Short-lived Credential 集成到 Kubernetes、Slurm、Storage、Registry 与 Internal API；
- 对 Authorization、Sharing Mode、Placement、Egress、Quota/Cost、Artifact Admission 与 Agent Tool 实施 Policy-as-code；
- 对 Material Tenant/Isolation Drift 执行 Desired/Actual Reconciliation 与 Quarantine；
- 建立 Hardened、Versioned Host/Node/Controller Image 与 Rapid Rebuild；
- 对高影响 Artifact 实施 Inventory/BOM、适用的 Provenance/Signature、Scan、Compatibility、Admission 与 Recall；
- 建立带 Stable Service/Tenant/Request/Resource ID 的 Protected Evidence Pipeline；
- 定义 Secure Engineering Gate、Canary、Rollback 与 Post-deployment Verification；
- 建立 Tenant Trust Tier、Urgent Abuse Path 与 Quota/Rate/Cost/Capacity Control；
- 发布面向客户的 Responsibility 与 Isolation Statement。

### 退出门

新生产服务从平台能力继承 Identity、Policy、Telemetry、Evidence、Response 与 Recovery 默认能力，而不是手工重复实现。Material Drift 会产生带 Owner 与 Evidence 的 Alert、Block 或 Quarantine。

## 8. 阶段 4：可持续多租户生产（第 6–12 个月）

### 目标结果

- 关闭 Engineering、Data/Model Lifecycle、Supply Chain、Key、Orchestration、Vulnerability Management、Evidence、Incident 与 Resilience 的适用 T2 缺口；
- 持续或高频执行 Service/Asset/Identity/Artifact/Fabric Reconciliation；
- 按真实 Exposure、Exploitability、Privilege、Tenant Impact 与 Blast Radius 排序 Vulnerability；
- 在代表性的 Hardware/Firmware/Driver/Mode 组合上测试 GPU Reset/Error/Quarantine 与 Tenant Reassignment；
- 定期测试 API、Kubernetes/Slurm、Fabric/RDMA/DPU、Storage、Support 与 OOB 禁止路径；
- 将 Detection Engineering 关联到当前 ATT&CK/ATLAS-informed Threat Scenario，并执行授权 Behavior Replay；
- 演练 Customer、Legal/Privacy 与 Ecosystem Notification；
- 演练 Backup、Restore、Region/Fabric Failure 与 Known-good Rebuild；
- 建立 Evidence Quality、Freshness、False-positive/False-negative Proxy 与 Remediation Metric。

### 退出门

适用 T2 作为有 Owner、有 SLO、有 Change Control、有 Failure Behavior、有当前 Evidence 且测试可重复的服务运行。Recovery 与 Isolation 结果满足服务承诺，而不是只在 Tabletop 中成立。

## 9. 阶段 5：高保证服务（第 12–18 个月）

### 目标结果

只在 Threat Model、监管、主权、数据敏感度或客户承诺确实值得成本时采用：

- Dedicated Host/Full-device，或准确声明的 Hardware-partitioned Service；
- Measured Boot/Firmware，以及 Attestation-bound Admission 或 Key Release；
- 明确 Hardware/Software/Attestation Boundary 与 Unsupported Component 的 Confidential-computing Profile；
- Jurisdiction-bounded People、Identity、Key、Data、Support、Telemetry、Backup、Supplier 与 Recovery；
- 更强 Build/Train Isolation、Reproducibility、Root Separation 与 Cryptographic Recovery；
- 独立 Architecture、Penetration、Isolation、Supplier 与 Recovery Assessment；
- 包含准确 Scope、Version、Limitation、Finding 与 Evidence Validity 的 Customer Assurance Package。

### 退出门

每个 T3 Claim 都关联到明确的 Service/Profile 与真实部署边界，至少每年及重大变更后独立验证；证据到期或假设变化时，必须移除或降级声明。

## 10. 阶段 6：受控自适应安全（第 18–24 个月）

### 前置条件

只有当相关 Action Class 的 Identity/Delegation、Typed Tool、Least Privilege、Deterministic Approval、Stop/Containment、Rollback/Manual Recovery、Protected Trace、Independent Verification、Evidence Quality 与 Incident Ownership 均已证明后，才进入本阶段。

### 候选用途

- Evidence Collection 与 Scope Reconciliation；
- Detection Triage 与 Investigation Planning；
- 可回滚的低风险 Configuration Correction；
- Artifact/Vulnerability Prioritization；
- 受控 Containment Preparation；
- 在授权环境执行 Red-team、Validation 与 Recovery Exercise。

### 默认禁止用途

- 无限制破坏性动作；
- 自行扩大 Credential、Tool、Scope 或 Budget；
- 自行审批影响客户的动作；
- 自行修改 Policy、Evidence 或 Verifier；
- 自主执行不可逆 Customer Communication、Legal Conclusion 或 Production Deletion；
- 缺少独立 Evidence 却把自己的任务声明为 `VERIFIED`。

### 退出门

对每类自动动作，度量并达到 Approval Bypass、Policy/Scope Violation、False Completion、Rollback/Manual Recovery、Stop Effectiveness、Evidence Integrity、Customer Impact 与 Independent-verifier Disagreement 目标。Kill Switch 与人工 Incident Path 均经过测试。

## 11. 指标与高管 Scorecard

不要使用一个混合完成百分比。至少报告：

- 按 Service/Profile 的 Production Decision；
- Failed、Unknown、Stale、Inconclusive 或 Untested T0；
- Critical Unknown/Unowned Scope；
- Commercial SKU 的精确 Isolation Declaration 与最近 Prohibited-path Test；
- Required T0 Telemetry Health，以及单独度量的 Priority-source Coverage；
- Privileged MFA/JIT/Revocation 与 Root/Secret State；
- Vulnerability/Exposure SLA 与 Deployed-state Retest；
- Artifact Inventory、Provenance/Admission 与 Recall；
- Incident Command、Reliable Scope 与 Effective Containment Time；
- Restore/Rebuild、Tenant Offboarding/Deletion 与 Sanitization Result；
- Agent Approval Bypass、Scope Violation、False Completion、Stop 与 Rollback；
- Customer Commitment Drift、Evidence Expiry 与未关闭 Business Decision。

具体定义与分母见[度量与持续证明指南](METRICS_AND_ASSURANCE.md)。

## 12. Build、Buy 与人员优先级

### 应自建或深度集成

- Tenant-correct Authorization 与 Desired/Actual Reconciliation；
- GPU/NVLink/Fabric/DPU/Storage/Scheduler Assignment Evidence；
- Reset、Cleanup、Sanitization 与 Reassignment Workflow；
- Model/Checkpoint Lineage、Safe Loading 与 Lifecycle；
- Agent Identity、Delegation、Tool Policy、Approval、Stop 与 Verifier；
- Service-specific Containment、Recovery 与 Reopening。

### 可以采购或采用成熟组件

- IdP、抗钓鱼 MFA、PAM、KMS/HSM、PKI 与 Secret Management；
- Vulnerability、Exposure 与 Attack-surface Management；
- SIEM/Data Lake、Runtime Detection、Case Management 与 Evidence Storage；
- Backup、DDoS/WAF/API Gateway、Signing 与 Transparency Service。

采购必须要求 Exportable API/Event、Stable Identity Integration、Tenant-safe Behavior、Secure Update、HA 与 Safe Degradation、Incident Notification、Evidence Quality、Independent Testing 与 Migration/Exit。厂商 Dashboard 不能单独证明覆盖。

### 人员顺序

早期人员配置应覆盖可追责安全负责人、Platform Security Architecture、Identity/Policy、Cloud/HPC/GPU/Fabric Engineering、Detection/Response、Data/Model Security、Vulnerability/Exposure、Facility/Hardware 与 Assurance/Privacy。规模较小时一人可以覆盖多个职能，但 Implementation 与 Independent Verification 不能合并成未经检查的同一角色。

## 13. 主要项目风险

| 风险 | 失败模式 | 应对措施 |
|---|---|---|
| Compliance Theater | Policy 与 Dashboard 替代真实部署测试 | T0 Gate、Negative Test、Evidence Freshness 与 Independent Review |
| Platform/Security 割裂 | Service Owner 误以为中央安全团队承担全部正确性 | 明确 Shared Responsibility 与 Service Acceptance Criteria |
| GPU 营销歧义 | “Dedicated/Isolated”隐藏真实 Sharing | 精确 SKU Statement 与版本化 Deployed-path Test |
| Coverage Gaming | Unknown Asset/Log 从分母中消失 | Unknown Critical Scope 直接失败；公布分子、分母与排除项 |
| Control-plane Centralization | Identity/Policy/Evidence 故障导致 Fail-open | Local Safe Behavior、Bounded Cache、Expiry、Quarantine 与 Recovery Test |
| Tool Sprawl | 产品之间不共享 Identity、State 与 Evidence | Capability Contract、Integration Architecture 与 Retirement Plan |
| Agent Overreach | 尚未证明就获得破坏性权限 | Risk Tier、Deterministic Approval/Stop、Rollback、Trace 与 Verifier |
| Recovery Optimism | Backup 存在，但 Root/Data/Isolation 不可信 | Known-good Rebuild 与独立 Reopening Test |
| Unreviewed Standards Drift | 正式版、草案和厂商指南被视为同等权威 | Reference Status Tracking 与定期 Evidence-cutoff Review |

## 14. 管理层必须作出的决定

1. Service Profile、Risk Appetite 与 Customer Assurance Commitment；
2. 可追责 Service/Control Owner 与 Independent-verification Authority；
3. 哪些失败 T0 暴露必须立即停止，以及谁可以在不改变符合性结果的前提下作出单独的限时紧急业务决定；
4. 公司对外销售哪些 Isolation Product，以及每个声明的准确含义；
5. 接受哪些 Jurisdiction、Data/Model Class 与 Workload；
6. Build/Buy Boundary 与战略平台投资；
7. Recovery Objective、Capacity Reserve 与 Notification Principle；
8. 哪些高影响 Agent Action Class 允许、禁止或需要 Approval；
9. Publication、License、Vulnerability Reporting 与 External Assurance Strategy；
10. 每月审阅哪些 Metric 与 Evidence。

## 15. 路线图完成定义

路线图成功的标志，是安全不再是一组互不相连的控制：Service Boundary 与 Identity 权威可信；Tenant Context 穿过每次转换；Isolation Claim 精确且经过测试；Data/Model/Artifact 具有 Lifecycle 与 Provenance；Required Telemetry 健康；Response/Recovery 经历演练；Evidence 可被独立复现；Automation 无法超越、审批或验证自身权限。
