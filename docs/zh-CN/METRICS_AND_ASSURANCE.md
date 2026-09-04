# NeoCloud 网络安全度量与持续证明指南

**版本：** 1.0.0-draft.1  
**基线日期：** 2026-09-04  
**状态：** 面向实施的项目草案  
**目标：** 度量安全结果在真实部署服务中是否成立，而不只是度量安全活动是否发生

本指南应与[安全基线](SECURITY_BASELINE.md)、机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)、[实践指南](PRACTICE_GUIDE.md)和仓库模板共同使用。

## 1. 持续证明原则

1. **先判硬门，再看分数。** 任一适用 T0 失败、未知、过期、`INCONCLUSIVE` 或 `NOT_TESTED`，都会产生 `NO_GO_NONCONFORMANT`。
2. **风险接受不等于控制验证。** 业务决定可以临时授权运营，但不能改变控制失败结果或支持符合性声明。
3. **度量真实部署边界。** Service、Profile、Environment、Region、Version、Tenant/Asset/Data Scope 与 Observation Time 都属于重大断言的一部分。
4. **区分部署与有效。** Implementation State、Population Coverage、Evidence Freshness、Negative-test Success、Failure Behavior 与 Independent Verification 是不同事实。
5. **未知范围必须可见。** 未知或无 Owner 的关键资源属于失败，不能从指标分母中静默删除。
6. **使用独立观察。** 高影响断言必须由能够挑战实施者的验证方复核，并在可行时使用不同 Observation/Test Path。
7. **优先结果，不堆活动量。** 度量不安全访问是否被拒绝、漂移是否纠正、撤销是否生效、清理是否安全、恢复是否成功、范围是否可靠，而不只是 Policy、Scan、Alert 或 Ticket 数量。
8. **可复现属于证据质量。** 合格审阅者应能按声明的 Query/Test 和范围复现结果。
9. **指标需要抗博弈。** 在报告趋势前定义分子、分母、排除项、数据 Owner、Source、Latency、Sampling、Target、Gate 与 Change Control。
10. **Assurance Plane 本身是敏感系统。** 必须实施 Tenant Partitioning、Minimization、Access Control、Integrity、Retention、Legal/Privacy 与 Source-health Monitoring。
11. **自动化先赢得信任。** 除速度外，还要度量 Approval Bypass、Scope Violation、False Completion、Rollback、Stop、Evidence Integrity 与 Verifier Independence。

## 2. 控制与验证状态

唯一正常完成路径为：

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

| 状态 | 含义 | 可以作出的声明 |
|---|---|---|
| `PROPOSED` | 已识别目标，范围或 Owner 可能不完整 | 不得声明已实现 |
| `READY` | 范围、Owner、依赖、要求、测试、证据、失败行为和目标日期完整 | 可以开始实施 |
| `IMPLEMENTED` | 机制已经部署到声明范围 | 只能声明部署，不能声明有效 |
| `CANDIDATE_DONE` | Owner 已提供当前证据并主张完成 | 等待独立验证 |
| `VERIFIED` | 独立验证者针对准确范围和有效期返回 `PASS` | 在失效前可以声明控制有效 |

验证结果只有 `PASS`、`FAIL`、`INCONCLUSIVE` 和 `NOT_TESTED`。只有 `PASS` 可以产生 `VERIFIED`。证据到期、重大变更、事件、控制失败、范围冲突或无法复现都会使结论失效。

## 3. 生产准入门

任何成熟度或进度分数之前，先计算硬门：

```text
if applicable_T0_failed_or_unknown_or_stale_or_inconclusive_or_untested > 0:
    decision = NO_GO_NONCONFORMANT
elif critical_scope_unknown > 0:
    decision = NO_GO_NONCONFORMANT
elif required_isolation_revocation_restore_incident_or_sanitization_test_failed:
    decision = NO_GO_NONCONFORMANT
elif unresolved_high_risk_without_accountable_decision > 0:
    decision = NO_GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

紧急业务决定单独记录，不会改变 `NO_GO_NONCONFORMANT`，也不会产生 `VERIFIED`。

Gate Record 必须记录 Service/Profile、Environment、Region、Version、Tenant/Asset/Data Scope、Assessment Time、Control/Evidence Version、Decision Owner、Validator、失败或未知断言、Business-risk Decision、Customer Impact 和下次验证时间。

## 4. 指标契约

每个指标必须定义：

| 字段 | 要求 |
|---|---|
| ID 与名称 | 稳定、版本化、含义唯一 |
| 安全问题 | 指标支持哪个决策 |
| 分子与分母 | 精确 Population、计数规则、Unknown 与 Duplicate 处理 |
| 范围 | Service、Profile、Tenant、Region、Environment、Asset/Data Class、Version、Isolation SKU |
| 数据源 | 权威系统与独立观察路径 |
| 采集 | Owner、Method/Query/Test Version、Frequency、Latency、Integrity 与 Failure Detection |
| 目标与硬门 | 目标区间、预警和适用的硬失败条件 |
| 排除项 | 显式、有理由、获批、到期且单独报告 |
| 失败响应 | Alert、Block、Quarantine、Escalation、Risk Decision 或 Manual Review |
| 验证者 | 独立审阅者及抽样/复现方法 |
| 局限 | Blind Spot、Error、Ambiguity、False Signal 与 Unsupported Population |
| 变更控制 | 定义、数据源、目标或分母变更的审批 |

每个百分比同时报告分子和分母。灾难性延迟相关指标应报告 p50、p95 与 Max，或给出合理的尾部指标。分母缩小、数据源缺失或范围突然消失属于告警，不是自动改善。

## 5. 证据数据契约

```yaml
evidence_id: EVID-...
control_id: NCS-...
assertion: 人类可读且可测试的断言
scope:
  service: ...
  profile: ...
  environment: production
  tenants: [all | sampled identifiers]
  regions: [...]
  assets: [...]
  data_classes: [...]
  software_firmware_versions: [...]
observation:
  collected_at: RFC3339 timestamp
  collector_identity: ...
  source_system: ...
  method_or_query_version: ...
  result: ...
  population_and_sample: ...
integrity:
  protection: hash | signature | tamper-evident store | other
  protected_location: ...
validity:
  expires_at: ...
  invalidation_triggers: [...]
verification:
  validator: ...
  test_id: ...
  result: PASS | FAIL | INCONCLUSIVE | NOT_TESTED
  limitations: [...]
  findings: [...]
  retest_due: ...
```

关键证据应导出到受保护边界，并使用稳定 ID 关联 Service、Tenant、Subject、Request、Workload/Job、Host、GPU、Fabric、Storage、Data/Model、Artifact、Policy、Action 与 Result。

## 6. 核心指标目录

下列目标是本项目的参考起点，不能替代威胁建模、服务承诺、法律义务或控制硬门。

### 6.1 治理、Owner 与保证

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-GOV-01 | 适用 T0 验证率 | 已独立验证的适用 T0 / 适用 T0 | 100%；硬门 |
| NCSM-GOV-02 | 关键服务责任完整度 | 同时具备业务、技术、安全、数据和事件 Owner 的关键服务 / 关键服务 | 100% |
| NCSM-GOV-03 | 超期关键决定/例外 | 已过期或超期的 P0/P1 Risk/Exception Record 数 | 0；硬升级 |
| NCSM-GOV-04 | 客户承诺漂移 | 被部署状态或当前证据证伪的承诺 / 有效承诺 | 重大漂移为 0 |
| NCSM-GOV-05 | 独立验证完成度 | 周期内已独立验证控制 / 周期内应验证控制 | 到期 T0/T1 与有承诺 T3 为 100% |
| NCSM-GOV-06 | 证据新鲜度 | 未过期必需证据 / 必需证据 | T0 为 100%；其他优先证据参考目标至少 95%，缺口必须可见 |

### 6.2 清单与范围完整性

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ASM-01 | 范围内关键资产 Owner 覆盖 | 同时具备 Service、适用 Tenant、Lifecycle 与 Owner 的关键资产 / 包含已发现未知对象在内的全部范围内关键资产 | 100%；未知关键资源导致硬门失败 |
| NCSM-ASM-02 | 特权身份 Owner 覆盖 | 有 Owner 与 Lifecycle 的特权身份 / 特权身份 | 100% |
| NCSM-ASM-03 | Desired/Actual 漂移发现延迟 | 重大状态偏差到被发现的时间 | 按服务目标；租户/隔离 Root 参考 p95≤15 分钟 |
| NCSM-ASM-04 | 未知生产资源 | 未映射到 Service、适用 Tenant 与 Owner 的生产资源数 | 关键资源为 0，其他明确下降 |
| NCSM-ASM-05 | 独立发现覆盖 | 至少被一条独立 Discovery/Reconciliation 路径观察的生产范围 / 预期生产范围 | 第 90 天参考至少 95%；排除项显式；关键未知仍然失败 |

### 6.3 人员、工作负载与 Agent 身份

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-IAM-01 | 特权抗钓鱼 MFA 覆盖 | 已覆盖的适用特权/高影响人员身份 / 适用总体 | 100%；硬门 |
| NCSM-IAM-02 | Standing Privilege | 持久高权限身份 / 特权身份总体 | 未审批为 0；已审批最小化 |
| NCSM-IAM-03 | JIT 特权时长 | Grant 到 Expiry 的时长 | p95 不超过批准任务窗口 |
| NCSM-IAM-04 | 紧急撤销时间 | 请求到所有必需执行点验证拒绝的时间 | 按场景 SLO，报告 p50/p95/max |
| NCSM-IAM-05 | 短期工作负载凭据 | 使用 Short-lived/Brokered Credential 的生产工作负载 / 生产工作负载 | 第 6 个月参考至少 80%，成熟目标至少 95% |
| NCSM-IAM-06 | 孤儿身份关闭 | SLA 内关闭的孤儿身份 / 已发现孤儿身份 | 关键 100%，总体参考至少 98% |
| NCSM-IAM-07 | Agent 委托完整度 | 具备 Owner、Identity、Delegator、Use Case、Scope、Tool、Authority 与 Expiry/Review 的生产 Agent / 生产 Agent | 100% |

### 6.4 API 与控制面正确性

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-API-01 | 租户授权负向测试通过率 | 通过的 Object/Action/Tenant/Purpose/Context 测试 / 必需已执行测试 | 关键 API 100% |
| NCSM-API-02 | 服务商管理面直接暴露 | 在受治理特权路径之外，可从 Public 或 Tenant Data Plane 直达的 Provider Administration | 0；硬门 |
| NCSM-API-03 | 缺失/冲突 Tenant Context 拒绝率 | 正确拒绝的生成请求 / 生成请求 | 100% |
| NCSM-API-04 | Control-state Trace 完整度 | 关联 Request、Actor、Tenant、Policy、Approval、Desired/Actual State 与 Result 的高影响变更 / 高影响变更 | 100% |
| NCSM-API-05 | 部分供应安全收口 | 已回滚或隔离并验证的重大失败工作流 / 重大失败工作流 | 100% |

### 6.5 网络、Fabric、计算与加速器隔离

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ISO-01 | SKU 隔离声明覆盖 | 有当前 Host/GPU/Cache/NVLink/Network/RDMA/Storage/Telemetry/Support 声明的商业 SKU / 商业 SKU | 100%；硬门 |
| NCSM-ISO-02 | 跨租户负向测试通过率 | 通过的必需禁止路径测试 / 必需已执行测试 | 100%；任一失败即事件/硬门失败 |
| NCSM-ISO-03 | Placement Policy 一致率 | 符合批准策略的实际 Host/GPU/Fabric/Storage 分配 / 活动分配 | 关键路径 100%；重大偏差隔离 |
| NCSM-ISO-04 | 加速器重分配清理率 | 具有已验证 Reset/Error/Cleanup 证据的跨租户重分配 / 适用重分配 | 100% |
| NCSM-ISO-05 | Fabric 分配对账率 | 符合批准租户意图的 VRF/VLAN/VXLAN/P_Key/DPU 分配 / 活动分配 | 100% |
| NCSM-ISO-06 | BMC/OOB 未授权可达路径 | 代表性测试中成功的未授权路径数 | 0 |
| NCSM-ISO-07 | 隔离证据年龄 | 按 Service/SKU/Region/Hardware/Firmware/Driver/Mode 的最近测试时间 | 不超过 Policy；重大变更立即失效 |

### 6.6 编排与数据/模型生命周期

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ORC-01 | 加固控制面覆盖 | 满足适用基线的生产 Cluster/Controller / 生产总体 | 100% |
| NCSM-ORC-02 | 特权 Workload/Job Policy 有效性 | 被拒绝的禁止提交 / 生成的禁止提交 | 100% |
| NCSM-ORC-03 | 编排恢复成功率 | 同时满足 Identity、Integrity、Isolation 与 RTO 的 Restore/Known-good Rebuild / 演练 | 100% |
| NCSM-DAT-01 | Crown Jewel 生命周期覆盖 | 具备 Owner、Classification、Purpose 与 Lifecycle 的 Crown Jewel Data/Model/Key/Artifact / 已识别总体 | 100% |
| NCSM-DAT-02 | 数据/模型血缘完整度 | 具备必需 Source-to-Use Lineage 的发布/重大制品 / 适用制品 | 发布关键 100%；其他重大制品参考至少 95% |
| NCSM-DAT-03 | 删除/退租验证率 | 在承诺内完成且独立留证的到期请求 / 到期请求 | 100% |
| NCSM-DAT-04 | 不安全制品拒绝率 | 被拒绝的恶意/不支持/已吊销 Model/Checkpoint 测试 / 生成测试 | 100% |

### 6.7 密钥、Secret 与供应链

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-KMS-01 | 未知关键密钥 | 缺少 Owner、Purpose、Location、Access、Rotation 或 Recovery 的关键 Key 数 | 0 |
| NCSM-KMS-02 | 静态生产 Secret 暴露 | 批准且到期的例外之外仍活动的静态/嵌入式 Secret | 关键为 0，其他持续下降 |
| NCSM-KMS-03 | Key/Certificate 轮换与恢复成功 | 未产生未授权访问或非计划重大中断的演练 / 计划与紧急演练 | 100% |
| NCSM-SSC-01 | 高影响制品清单 | 有 Identity、Owner、Source 与 Version 的已部署高影响制品 / 已部署高影响制品 | 100% |
| NCSM-SSC-02 | 必需 Provenance/Signature 覆盖 | 满足适用 Provenance/Signature Policy 的发布关键制品 / 适用发布关键制品 | 100% |
| NCSM-SSC-03 | Admission Policy 有效性 | 被拒绝的未知、在要求签名时未签名、已吊销或不兼容制品 / 生成测试 | 100% |
| NCSM-SSC-04 | 制品召回时间 | 决策到 Required Registry/Runtime 完成验证 Deny/Quarantine 的时间 | 测试 SLO，报告 p50/p95/max |

### 6.8 漏洞、暴露、遥测与检测

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-VEM-01 | Internet/Root 暴露 SLA | SLA 内修复或可靠隔离的到期关键暴露 / 到期关键暴露 | 100% |
| NCSM-VEM-02 | 已验证修复率 | 经部署状态 Retest 的已关闭 Finding / 已关闭 Finding | 关键 100%，总体参考至少 95% |
| NCSM-VEM-03 | Firmware/Driver 状态可见度 | 具有当前、可归因 Firmware/Driver State 的生产设备 / 生产设备 | 关键 Root 100%，总体参考至少 95% |
| NCSM-TEL-01 | T0 必需遥测覆盖 | 健康且可查询的 T0 必需 Source / T0 必需 Source | 100%；硬门；缺失遥测不能解释为没有活动 |
| NCSM-TEL-02 | 遥测新鲜度 | 在期望延迟内交付的 Source / Required Source | 按 Source 设定；关键参考至少 99% |
| NCSM-TEL-03 | Detection 验证通过率 | 通过授权 Behavior Replay 的 Priority Detection / 到期 Priority Detection | 灾难性场景 100%，其他优先项参考至少 95% |
| NCSM-TEL-04 | Alert Decision Precision 与 Recall Proxy | 可行动结果和已知漏检测试行为 / 已复核 Alert 与 Test Corpus | 按 Use Case 跟踪，披露局限和抽样 |
| NCSM-TEL-05 | Evidence Tamper 与 Source-failure Detection | 被发现的模拟未授权修改或 Source-health Failure / 测试 | 优先测试 100% |
| NCSM-TEL-06 | 非硬门优先遥测覆盖 | 健康且可查询的 T0 Required Set 之外 Priority Source / 已定义 Non-gate Priority Source | 第 90 天参考至少 95%，缺口与风险显式 |

### 6.9 AI Agent 与自动化防御

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-AIR-01 | 生产 Agent 清单 | 具备 Owner、Identity、Use Case、Impact Assessment 与版本化组件的 Agent / 生产 Agent | 100% |
| NCSM-AIR-02 | Tool 仲裁覆盖 | 通过 Typed Validation 与 Policy Enforcement 的重大 Tool Call / 重大 Tool Call | 100% |
| NCSM-AIR-03 | 必需审批绕过 | 未取得必需确定性审批却执行的高影响动作 / 高影响动作 | 0 |
| NCSM-AIR-04 | 重大 Scope 违规 | 超出不可变或已批准 Goal/Tenant/Data/Tool/Egress/Cost Boundary 的动作 / Agent Action | 0 |
| NCSM-AIR-05 | 确定性停止有效率 | 在 Success/Budget/Time/Repetition/Policy/Uncertainty Boundary 正确停止的优先场景 / 生成场景 | 适用优先场景 100% |
| NCSM-AIR-06 | False Completion | 缺少充分证据却被声明完成/验证的任务 / 抽样完成任务 | Verifier-gated Claim 为 0 |
| NCSM-AIR-07 | Verifier 否决率 | 被独立 Verifier 推翻的重大 Candidate Claim / Candidate | 按失败类型跟踪，调查所有重大分歧 |
| NCSM-AIR-08 | 自动回滚/人工恢复成功率 | 安全 Reverse 或 Contain 的失败自动变更 / 适用演练 | 已测试类别 100% |

### 6.10 滥用、事件响应、韧性与物理 Root

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ABU-01 | Quota/Rate/Cost 绕过 | 授权测试中成功绕过次数 | 0 |
| NCSM-ABU-02 | 紧急滥用隔离时间 | 已验证紧急 Abuse 到实际验证隔离的时间 | 服务 SLO，报告 p50/p95/max |
| NCSM-IRR-01 | 建立指挥时间 | 符合条件的 Alert/Report 到明确 IC 与安全频道 | 按严重性目标 |
| NCSM-IRR-02 | 可靠定界时间 | Incident Declaration 到有证据支撑的受影响 Service/Tenant/Resource Set | 按场景目标，报告不确定性 |
| NCSM-IRR-03 | 实际隔离时间 | Incident Declaration 到可靠边界完成验证 Isolation/Revocation | 按场景目标 |
| NCSM-IRR-04 | 验证关闭质量 | 具备 Evidence、Cause、Recovery Check、Action 与 Independent Review 的重大事件 / 已关闭重大事件 | 100% |
| NCSM-RES-01 | 恢复目标成功率 | 同时满足 RTO/RPO、Identity、Integrity 与 Isolation 的演练 / 演练 | 关键服务 100% |
| NCSM-RES-02 | 受保护 Backup/Rebuild Source 覆盖 | 具备必需受保护 Backup 或 Known-good Source 的关键 Provider-managed State / 适用关键状态 | 100% |
| NCSM-RES-03 | Known-good Rebuild 成功率 | 满足 Version、Identity、Integrity、Isolation、Data 与 Monitoring 的重建 / 演练 | 100% |
| NCSM-PHY-01 | BMC/Root 基线覆盖 | 具备 Owner、Inventory、Hardened State、Patch、Access 与 Recovery 的 BMC/OOB / Device | 100% |
| NCSM-PHY-02 | Sanitization 验证率 | 具有成功且方法适配的清除证据的 Reassignment/Decommission / 适用事件 | 100%；重分配/处置前硬门 |

机器可读目录当前只关联上述指标中的稳定子集。本指南新增但尚未进入目录的 Metric ID，在未来经过治理流程加入目录前均为参考性指标。

## 7. 证据强度

证据等级可辅助安排复核优先级，但不能替代控制硬门：

| 等级 | 证据类型 | 典型结论 |
|---:|---|---|
| 0 | 无证据或无支持声明 | 失败或未知 |
| 1 | Policy、Design Statement 或 Interview | 只证明意图 |
| 2 | Screenshot 或人工报告 | 方向性实施迹象 |
| 3 | 与范围关联的可复现 API/Query/Export | 当前实施与 Population Coverage |
| 4 | Protected Runtime Event、Verified Attestation 或 Automated Reconciliation | 具备 Integrity/Freshness 的运营断言 |
| 5 | 经授权 Negative/Failure/Recovery Test 并由独立方复现 | 对已测试范围的高置信有效性 |

T0 必须使用与准确断言匹配的证据并独立验证；“Level 5”也不能让范围不完整的控制变成符合项。

## 8. 抽样

Identity、Configuration、Assignment、Public Endpoint、Deployed Artifact、Exception、Ownership 与 Evidence Freshness 应尽量全量评估。只有在对抗、破坏性或物理测试成本很高时才使用抽样，并且必须满足：

- 总体、分层和选择方法有记录；
- 覆盖所有重大 Service/SKU/Region/Hardware/Firmware/Driver/Mode 变体；
- 高风险和近期变更对象获得更高概率；
- 报告置信度、Blind Spot 与 Unsupported Population；
- 任一失败扩大范围并触发 Incident 或 Remediation；
- 灾难性边界不得只从便利样本推断。

代表性的 Accelerator Reset/Cleanup 测试必须区分 Hardware Model、Firmware、Driver、Virtualization/Sharing Mode、Scheduler Path、Region、Error State 与 Tenant Reassignment Workflow。

## 9. 持续证明管道

```text
发现实际状态
  → 规范化身份、范围和关系
  → 评估策略/控制断言
  → 采集受保护证据
  → 执行授权的正向、禁止路径与失败测试
  → 比较 Desired 与 Actual State
  → 独立 Verifier 判定
  → Gate、Alert、Quarantine、Contain 或记录 Risk Decision
  → 整改并复测
  → 发布范围明确且有时效的 Assurance
```

管道必须自监控：Collector/Source 丢失、延迟、Schema Error、Identifier Conflict、Permission Loss、Clock Problem、Partial Test、Evidence-store Integrity、Verifier Unavailable 与 Denominator Change 都是一等失败。

## 10. Dashboard 与报告

不要只发布一个混合“安全百分比”。至少区分：

- **高管视图：** Service/Profile Production Decision；失败/未知/过期 T0；关键决定；客户承诺漂移；Root/Cross-tenant/Data/Recovery Risk；Owner 与期限。
- **服务 Owner 视图：** Control State、Evidence Expiry、Scope Gap、Desired/Actual Drift、Test Failure、Customer Responsibility 与 Revalidation Trigger。
- **安全运营视图：** Required-source Health、Active Exposure、Identity/Root/Fabric/GPU/Agent Anomaly、Detection Test、Containment 与 Automation Health。
- **保证视图：** Evidence Scope/Strength/Freshness/Integrity/Reproducibility、Validator Independence、Sample、Exception、Failed Test 与可对外支持的声明。

精确陈述示例：

- 好：“截至 2026-09-04，GPU-IaaS 服务 X 在 Region A/B、Release 2026.09 的全部适用 T0 已独立验证；两项 T1 证据将在 14 天内到期。”
- 差：“安全建设完成度 96%。”
- 好：“SKU Y 专属 Host、整卡 GPU、租户数据网络与本地存储；Provider BMC 与安全 Telemetry 仍为共享服务，通过 JIT 控制访问。”
- 差：“完全专属、全面零信任。”

每个外部保证声明必须标识 Scope、Date、Version、Limitation、Failed/Untested Area、Business-risk Decision 与 Verifier。

## 11. 保证节奏

| 周期 | 最低复核内容 |
|---|---|
| 持续 | 技术可行时的 T0、Identity/Policy、Public Exposure、Allocation Drift、Required Telemetry、Root Use、Backup Health、高影响 Agent Action |
| 每日 | Failed Collector/Test、Unknown/Unowned Critical State、Urgent Exposure 与 Containment Backlog |
| 每周 | Vulnerability SLA、Privilege、Release、Decision/Exception、Detection Failure 与 Incident Action |
| 每月 | 高管 Gate/Risk、Customer Commitment Drift、Denominator/Source Quality 与 Overdue Remediation |
| 每季度 | T0/T1 Verification、Access Review、Isolation、Revocation/Restore、Detection Replay 与适用 Agent Adversarial Test |
| 每半年 | T2 Verification 与重大 Incident/Control-plane/Recovery Exercise |
| 每年 | 独立 T3 Architecture/Isolation、Regional Recovery/Rebuild、Supplier 与 Cryptographic Recovery |
| 重大变更 | 立即重新确定并验证受影响断言 |

## 12. Assurance Package

服务保证包至少包含：

1. Service Description、Profile、Boundary、Region、Version 与 Shared Responsibility；
2. Applicable Control 与 Production-gate Decision；
3. 精确 Host/GPU/Cache/NVLink/Network/RDMA/Storage/Telemetry/BMC/Support 共享与隔离声明；
4. Identity、Key、Artifact、Data/Model、Logging、Incident、Backup、Deletion 与 Residency 摘要；
5. 包含 Scope、Freshness、Strength、Source、Integrity 与 Validator 的 Evidence Index；
6. Negative-path、Failure、Revocation、Restore/Rebuild、Sanitization 与 Incident Test 摘要；
7. Material Finding、Unknown、Risk Decision/Exception、Compensating Control、Customer Impact 与 Remediation Date；
8. Independent-review Statement 与 Limitation；
9. 下次验证与 Invalidation Trigger。

## 13. 常见度量失败

- 适用 T0 失败时仍报告百分比；
- 把业务风险决定转换为“通过”；
- 从分母中删除未知或难以度量资产；
- 把遥测缺失解释为没有恶意活动；
- 用 Scan、Policy、Ticket 或 Alert 数量证明风险下降；
- 不验证 Claim/Scope 就接受 Vendor Dashboard、Signature 或 Attestation；
- 只报告平均响应时间，不报告严重性与尾部延迟；
- 允许 Owner、Control 或 Agent 自我验证；
- 证据过期后继续计为 Pass；
- 通过修改定义或分母改善趋势；
- 只度量自动化速度，不度量 Approval、Scope、False Completion、Stop 与 Rollback；
- 恢复后未独立检查 Identity、Artifact、Data、Tenant Isolation 与 Monitoring 就重新开服。

## 14. 可度量安全的最低定义

一个 NeoCloud 控制只有在适用范围与 Owner 已知、机制存在于真实部署路径、必需证据当前且受保护并可复现、相关禁止路径和失败行为已测试、独立验证者能够复现断言、失败会触发明确运营响应，并在证据到期或重大变更后重新验证时，才能称为可度量且有效。
