# NeoCloud 网络安全度量与持续证明指南

**版本：** 1.0.0-draft.2  
**基线日期：** 2026-09-04  
**目标：** 度量安全结果在真实部署的 NeoCloud 服务中是否成立，而不是只度量安全活动是否发生

本指南定义[安全基线](SECURITY_BASELINE.md)的度量、证据、验证和报告模型，应与机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)、[实践指南](PRACTICE_GUIDE.md)、[范围与局限](SCOPE_AND_LIMITATIONS.md)及仓库模板共同使用。

## 1. 持续证明原则

1. **先判硬门槛，再看分数。** 任一适用 T0 失败或未知都产生 `NO-GO`，综合百分比不能覆盖该结果。
2. **度量真实部署边界。** 缺少服务、租户、Region、版本、资产和时间范围的指标，无法支持可靠决策。
3. **区分实现与有效。** 部署状态、覆盖率、证据时效、负向测试通过率和独立验证是不同事实。
4. **使用独立观察路径。** 高影响声明需要不完全由实施者控制的证据边界或测试方法。
5. **优先结果，不堆活动量。** 应统计不安全访问是否被拒绝、恢复是否成功，而不只是 Policy、Scan 或 Ticket 数量。
6. **未知、过期和无法判定必须显式。** 不得静默转换为通过。
7. **可复现属于证据质量。** 审阅者应能够按相同范围执行 Query/Test 并获得一致结果。
8. **指标需要抗博弈。** 在设置目标前定义分子、分母、排除项、Owner、数据源、延迟、抽样和变更控制。
9. **安全度量数据本身是敏感数据。** Assurance Plane 也必须实施租户分区、最小化、访问控制、完整性、保留和法务/隐私要求。
10. **自动化需要先证明可信。** 自动证据和自动修复必须度量 Precision、Rollback、Failure Mode 和 Independent Verifier。

## 2. 控制状态模型

唯一正常完成路径为：

`PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`

| 状态 | 含义 | 可以作出的声明 |
|---|---|---|
| `PROPOSED` | 已识别目标，但范围或 Owner 可能不完整 | 不得声明已实现 |
| `READY` | 范围、Owner、依赖、要求、测试、证据和目标日期均已定义 | 可以开始实施 |
| `IMPLEMENTED` | 机制已部署到声明范围 | 只能声明已部署，不能声明有效 |
| `CANDIDATE_DONE` | Owner 已提交证据并主张完成 | 等待独立验证 |
| `VERIFIED` | 独立验证者对当前范围和证据返回 `PASS` | 在证据过期或失效前可声明控制有效 |

验证结果：

- `PASS`：断言可复现，必需正向与负向测试通过；
- `FAIL`：断言被证伪，或必需测试失败；
- `INCONCLUSIVE`：证据或测试不足以支持可靠结论；
- `NOT_TESTED`：没有当前测试结果。

`INCONCLUSIVE`、`NOT_TESTED`、证据过期、范围缺失或验证者缺失均不能计为 Verified。

## 3. 生产准入门

对每个服务画像，先计算准入门，再计算任何成熟度分数。

```text
if applicable_T0_failed > 0:
    decision = NO_GO
elif applicable_T0_unknown_or_stale > 0:
    decision = NO_GO
elif critical_scope_unknown > 0:
    decision = NO_GO
elif required_isolation_revocation_restore_or_sanitization_test_failed:
    decision = NO_GO
elif unresolved_critical_risk_without_authorized_acceptance > 0:
    decision = NO_GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

准入记录必须包含服务、画像、环境、Region、版本、评估时间、决策 Owner、验证者、失败断言、例外和下次验证时间。

## 4. 指标契约

每个指标定义至少包含：

| 字段 | 要求 |
|---|---|
| ID 与名称 | 稳定、版本化、含义唯一 |
| 安全问题 | 该指标支持哪个决策 |
| 分子与分母 | 精确定义总体与计数规则 |
| 范围维度 | 服务、租户、Region、环境、资产类型、版本、数据分类、隔离 SKU |
| 数据源 | 权威系统与独立观察路径 |
| 采集 | Owner、频率、Query/Test、延迟、完整性保护 |
| 目标与硬门 | 目标区间、预警阈值、适用时的硬失败条件 |
| 排除项 | 显式、有理由、有期限并单独报告 |
| 失败行为 | 告警、阻断、隔离、升级或人工复核 |
| 验证者 | 谁独立复核定义并抽样结果 |
| 局限性 | 盲点、抽样误差、歧义和预期误报 |
| 变更控制 | 定义、数据源或目标变更的 Owner 与审批 |

百分比必须同时公布分子和分母；灾难性延迟相关指标除 Median 外必须提供尾部 Percentile。分母下降通常是告警，不是自动改善。

## 5. 证据数据契约

每个证据项建议至少包含：

```yaml
evidence_id: EVID-...
control_id: NCS-...
assertion: 可验证的人类可读断言
scope:
  service: ...
  profile: ...
  environment: production
  tenants: [all | sampled identifiers]
  regions: [...]
  assets: [...]
  software_firmware_versions: [...]
observation:
  collected_at: RFC3339 timestamp
  collector_identity: ...
  source_system: ...
  method_or_query_version: ...
  result: ...
integrity:
  hash_or_signature: ...
  protected_location: ...
validity:
  expires_at: ...
  invalidation_triggers: [...]
verification:
  validator: ...
  test_id: ...
  result: PASS | FAIL | INCONCLUSIVE | NOT_TESTED
  findings: [...]
```

关键证据应导出到具有与风险相匹配的管理和观察分离的受保护边界，并使用稳定标识关联 Service、Tenant、Subject、Workload、Host、GPU、Fabric、Data/Model、Artifact、Request 和 Policy；这并不普遍要求物理隔离。

## 6. 核心指标目录

下列目标是本项目定义的参考起点，不是经外部验证的行业 Benchmark。组织应根据服务承诺、实际技术栈、威胁模型和风险调整目标，但不得削弱适用的 T0 硬门槛。

### 6.1 治理、Owner 与保证

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-GOV-01 | 适用 T0 验证率 | 已验证适用 T0 / 适用 T0 | 100%；硬门 |
| NCSM-GOV-02 | 关键服务责任完整度 | 同时具备业务、技术、安全、数据、事件 Owner 的关键服务 / 关键服务 | 100% |
| NCSM-GOV-03 | 超期关键例外 | 已过期或超期的 P0/P1 Exception 数 | 0；硬升级 |
| NCSM-GOV-04 | 客户承诺漂移 | 部署状态或证据不符合承诺的项目 / 有效承诺 | 重大漂移为 0 |
| NCSM-GOV-05 | 独立验证覆盖 | 周期内已独立验证控制 / 周期内应验证控制 | 应验证 T0/T1 为 100% |
| NCSM-GOV-06 | 证据新鲜度 | 未过期必需证据 / 必需证据 | T0 为 100%；其他高优先级至少 95% |

### 6.2 清单与范围完整性

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ASM-01 | 关键资产 Owner 覆盖 | 有当前 Owner 的关键资产 / 关键资产 | 第 90 天至少 95%，长期 100% |
| NCSM-ASM-02 | 特权身份 Owner 覆盖 | 有 Owner 和生命周期记录的特权身份 / 特权身份 | 100% |
| NCSM-ASM-03 | Desired/Actual 漂移发现延迟 | 重大状态偏差到被发现的时间 | 租户/隔离 Root 的 p95 不超过 15 分钟 |
| NCSM-ASM-04 | 未知生产资源 | 未映射到服务、租户和 Owner 的生产资源数 | 关键资源为 0，其他持续下降 |
| NCSM-ASM-05 | 依赖可观测覆盖 | 有 Owner、健康、失败模式和恢复路径的关键依赖 / 关键依赖 | 100% |

### 6.3 人员、工作负载与 Agent 身份

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-IAM-01 | 特权抗钓鱼 MFA 覆盖 | 已覆盖特权人员身份 / 特权人员身份 | 100%；适用时为硬门 |
| NCSM-IAM-02 | Standing Privilege | 持久高权限身份 / 特权身份总体 | 最小化；未审批为 0 |
| NCSM-IAM-03 | 特权授予时长 | JIT Elevation 持续时间 | p95 不超过已批准任务窗口 |
| NCSM-IAM-04 | 紧急撤销时间 | 撤销请求到所有执行点实际拒绝的时间 | 按 SLO 测试，报告 p50/p95/max |
| NCSM-IAM-05 | 短期工作负载凭据覆盖 | 使用短期/Brokered Identity 的生产工作负载 / 生产工作负载 | 第 6 个月至少 80%，成熟目标至少 95% |
| NCSM-IAM-06 | 孤儿身份按时关闭 | SLA 内关闭的孤儿身份 / 发现的孤儿身份 | 关键身份 100%，总体至少 98% |
| NCSM-IAM-07 | Agent 委托完整度 | 具备 Identity、Delegator、Goal、Scope、Tool、Budget、Expiry 的 Agent / 生产 Agent | 100% |

### 6.4 API 与控制面正确性

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-API-01 | 租户授权负向测试通过率 | 通过的 Object/Action/Tenant 测试 / 应执行测试 | 关键 API 为 100% |
| NCSM-API-02 | 公网服务商管理面暴露 | 可从公网或租户数据面直达的服务商管理接口数 | 除非显式设计并通过 T0 审批，否则为 0 |
| NCSM-API-03 | 缺失租户上下文拒绝率 | 被拒绝的缺失/冲突 Tenant Context 请求 / 生成测试 | 100% |
| NCSM-API-04 | 控制状态 Trace 完整度 | 含 Request、Policy、Desired、Actual、Actor、Result 的高影响变更 / 高影响变更 | 100% |
| NCSM-API-05 | 部分供应安全收口 | 已回滚或隔离的重大失败工作流 / 重大失败工作流 | 100% |

### 6.5 网络、Fabric、计算与加速器隔离

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ISO-01 | SKU 隔离声明覆盖 | 有当前 Host/GPU/Cache/NVLink/Network/RDMA/Storage/Support 声明的商业 SKU / 商业 SKU | 100%；硬门 |
| NCSM-ISO-02 | 跨租户负向测试通过率 | 通过的必需隔离测试 / 已执行必需测试 | 100%；任一失败即事件/准入失败 |
| NCSM-ISO-03 | Placement Policy 一致率 | 符合批准策略的实际 Host/GPU/Fabric/Storage 分配 / 活动分配 | 关键路径 100%，重大偏差立即隔离 |
| NCSM-ISO-04 | 加速器重分配清理率 | 具有成功 Reset/Error/Cleanup 证据的跨租户重分配 / 跨租户重分配 | 100% |
| NCSM-ISO-05 | Fabric 分配对账率 | 符合租户意图的 VRF/VLAN/VXLAN/P_Key/DPU 分配 / 活动分配 | 100% |
| NCSM-ISO-06 | BMC/OOB 未授权可达路径 | 授权测试中成功的未授权可达路径数 | 0 |
| NCSM-ISO-07 | 隔离证据年龄 | 按 SKU/Region/Version 的最近负向测试距今天数 | 不超过 Policy，有重大变更立即重验 |

### 6.6 Kubernetes、Slurm、Runtime 与数据/模型生命周期

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ORC-01 | 加固控制面覆盖 | 满足批准基线的生产 Cluster/Controller / 生产 Cluster/Controller | 100% |
| NCSM-ORC-02 | 特权工作负载/作业策略有效性 | 被拒绝的禁止提交 / 生成的禁止提交 | 100% |
| NCSM-ORC-03 | 编排恢复成功率 | 满足完整性、隔离和 RTO 的恢复/已知可信重建 / 演练 | 100% |
| NCSM-DAT-01 | Crown Jewel 分类覆盖 | 有 Owner 和生命周期的 Crown Jewel Data/Model/Key/Artifact / 已识别 Crown Jewel | 100% |
| NCSM-DAT-02 | 数据/模型血缘完整度 | 具有 Source-to-Use 血缘的重大制品 / 重大制品 | 至少 95%；发布关键制品 100% |
| NCSM-DAT-03 | 删除与退租验证率 | 在承诺内完成且独立留证的请求 / 到期请求 | 100% |
| NCSM-DAT-04 | 不安全制品拒绝率 | 被拒绝的恶意/不支持 Model 或 Checkpoint Format / 生成测试 | 100% |

### 6.7 密钥、Secret 与供应链

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-KMS-01 | 未知关键密钥 | 缺少 Owner、用途、位置、轮换和恢复记录的关键密钥数 | 0 |
| NCSM-KMS-02 | 静态 Secret 暴露 | 批准例外之外仍活动的静态生产 Secret 数 | 关键为 0，其他持续下降 |
| NCSM-KMS-03 | Key/Certificate 轮换成功率 | 未产生未授权访问或重大中断的轮换 / 计划与紧急轮换 | 100% |
| NCSM-SSC-01 | 高影响制品清单覆盖 | 有 Identity/Version/Owner/Source 的已部署高影响制品 / 已部署高影响制品 | 100% |
| NCSM-SSC-02 | Provenance 与签名覆盖 | 具有已验证 Provenance/Signature 的发布关键制品 / 发布关键制品 | 目标 100% |
| NCSM-SSC-03 | Admission Policy 有效性 | 被拒绝的未知/未签名/已吊销制品 / 生成测试 | 100% |
| NCSM-SSC-04 | 制品召回时间 | 决策到 Registry/Runtime 完成隔离或拒绝的时间 | 按目标测试，报告 p50/p95/max |

### 6.8 漏洞、暴露、遥测与检测

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-VEM-01 | 公网/Root 暴露 SLA | SLA 内已修复或隔离的到期关键暴露 / 到期关键暴露 | 100% |
| NCSM-VEM-02 | 已验证修复率 | 经部署状态 Rescan/Retest 的 Finding / 已关闭 Finding | 关键 100%，总体至少 95% |
| NCSM-VEM-03 | Firmware/Driver 可见度 | 已映射当前 Firmware/Driver 状态的生产设备 / 生产设备 | 至少 95%，关键 Root 100% |
| NCSM-TEL-01 | 关键遥测覆盖 | 健康且可查询的必需关键日志源 / 必需关键日志源 | 第 90 天至少 95%，Root Source 100% |
| NCSM-TEL-02 | 遥测新鲜度 | 在预期延迟内交付的日志源 / 必需日志源 | 关键至少 99% |
| NCSM-TEL-03 | Detection 验证通过率 | 通过授权行为重放的优先检测 / 到期优先检测 | 至少 95%，灾难性场景 100% |
| NCSM-TEL-04 | 告警决策 Precision | 真实可行动告警 / 已复核告警 | 按 Use Case 跟踪并匹配响应容量 |
| NCSM-TEL-05 | 证据篡改发现率 | 被发现的模拟未授权证据修改 / 测试 | 100% |

### 6.9 AI Agent 与自动化防御

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-AIR-01 | 生产 Agent 清单覆盖 | 有 Owner、Identity、Impact Assessment、Model/Prompt/Skill/Tool Version 的 Agent / 生产 Agent | 100% |
| NCSM-AIR-02 | Tool 仲裁覆盖 | 经过 Typed Schema 与 Policy Enforcement 的重大 Tool Call / 重大 Tool Call | 100% |
| NCSM-AIR-03 | 审批绕过率 | 未获得必需确定性审批却执行的高影响动作 / 高影响动作 | 0 |
| NCSM-AIR-04 | Scope 违规率 | 超出不可变 Goal/Scope/Tenant/Data/Cost Boundary 的动作 / Agent 动作 | 重大违规为 0 |
| NCSM-AIR-05 | 确定性停止有效率 | 在 Success/Budget/Time/Repetition/Policy/Uncertainty Boundary 正确停止的场景 / 生成场景 | 优先场景 100% |
| NCSM-AIR-06 | 错误完成率 | 缺少充分证据却被标记完成/验证的任务 / 抽样已完成任务 | Verifier Gate 声明为 0 |
| NCSM-AIR-07 | Verifier 否决率 | 被独立验证者推翻的重大 Owner/Agent 声明 / Candidate | 按类别趋势分析并查因 |
| NCSM-AIR-08 | 自动回滚成功率 | 安全恢复的失败自动变更 / 需要回滚的自动变更 | 已测试可逆类别 100% |

### 6.10 滥用、事件响应、韧性与物理 Root

| ID | 指标 | 计算方法 | 参考目标 |
|---|---|---|---|
| NCSM-ABU-01 | Quota/Rate/Cost Control 绕过 | 授权测试中成功绕过次数 | 0 |
| NCSM-ABU-02 | 紧急滥用隔离时间 | 已确认紧急滥用到实际隔离的时间 | 服务 SLO，报告 p50/p95/max |
| NCSM-IRR-01 | 建立指挥时间 | 符合条件的告警/报告到明确 IC 与安全频道的时间 | 按严重性目标 |
| NCSM-IRR-02 | 可靠范围确定时间 | 宣告事件到获得证据支撑的受影响 Service/Tenant/Resource 集合 | 按场景目标，并报告不确定性 |
| NCSM-IRR-03 | 实际隔离时间 | 宣告事件到在可靠边界完成并验证隔离/撤销的时间 | 按场景目标 |
| NCSM-IRR-04 | 验证关闭质量 | 具有证据、根因、恢复检查、行动项和独立复核的事件 / 已关闭重大事件 | 100% |
| NCSM-RES-01 | 恢复目标成功率 | 同时满足 RTO/RPO、完整性和隔离的演练 / 演练 | 关键服务 100% |
| NCSM-RES-02 | 不可变备份覆盖 | 具有受保护不可变备份的关键服务商管理状态 / 需要备份的关键状态 | 100% |
| NCSM-RES-03 | Known-good Rebuild 成功率 | 满足版本、身份、隔离、数据与监控标准的重建 / 演练 | 100% |
| NCSM-PHY-01 | BMC/Root 基线覆盖 | 有 Owner、清单、加固、补丁和受保护访问的 BMC/OOB / BMC/OOB | 100% |
| NCSM-PHY-02 | 清除验证率 | 具有成功清除记录的租户重分配/退役 / 适用事件 | 100%；重分配前硬门 |

## 7. 证据强度等级

该等级用于确定优先级，不能替代硬门判断。

| 等级 | 证据类型 | 典型用途 |
|---:|---|---|
| 0 | 无证据或无支持声明 | 失败/未知 |
| 1 | Policy、设计说明、访谈 | 只证明意图 |
| 2 | Screenshot 或人工报告 | 方向性复核 |
| 3 | 与范围关联的可重复 API/Query/Export | 实施与覆盖 |
| 4 | 受保护 Runtime Event、Signed Attestation 或自动对账 | 当前运营断言 |
| 5 | 经授权的负向/故障/恢复测试，并被独立复现 | 高置信有效性 |

T0 必须具有当前、范围明确的证据及与断言匹配的独立测试；单一数字等级不能自动证明充分。

## 8. 抽样规则

Identity、Configuration、Assignment、Public Endpoint、Deployed Artifact、Exception 和 Evidence Freshness 应优先进行全量评估。只有在对抗、破坏性或物理测试成本过高时才允许抽样，并且必须满足：

- 总体和选择方法有记录；
- 覆盖所有重大 Service/SKU/Region/Version 变体；
- 高风险和近期变更对象获得更高抽样概率；
- 报告置信度与盲点；
- 任一失败会扩大样本并触发事件或整改；
- 灾难性边界不得仅依赖便利样本推断。

代表性的 GPU Reset 测试必须区分 Hardware Model、Firmware、Driver、Virtualization/Sharing Mode、Scheduler Path、Region 和 Reassignment Workflow。

## 9. 持续证明管道

```text
发现实际状态
  → 规范化身份与资产
  → 评估策略与控制断言
  → 采集受保护证据
  → 执行安全的正向/负向测试
  → 比较 Desired 与 Actual State
  → 独立 Verifier 判定
  → Gate、Alert、Quarantine 或 Risk Acceptance
  → 跟踪整改并重测
  → 发布范围明确的 Assurance
```

管道必须自监控：Collector 缺失、Source 延迟、Schema 错误、Identifier 冲突、权限丢失、测试部分执行、Verifier 不可用和 Evidence Store 完整性问题均是一等失败。

## 10. Dashboard 设计

不要只做一个混合总分，应至少分为四类视图。

### 高管视图

- 每个 Service/Profile 的生产决策；
- 失败、未知或过期 T0；
- 关键例外和客户承诺漂移；
- 信任根、跨租户、数据/模型和韧性 Top Risk；
- 事件与恢复目标失败；
- 决策 Owner 与期限。

### 服务 Owner 视图

- 控制状态和证据到期；
- 资产/身份/依赖范围缺口；
- Desired/Actual Drift；
- 测试失败及整改路径；
- 客户责任与承诺；
- Release、Change 和 Revalidation Trigger。

### 安全运营视图

- 关键遥测健康；
- 活动暴露与可利用性；
- Identity/Root/Fabric/GPU/Agent 异常；
- Detection Quality 与 Missed Behavior；
- Containment Readiness 和 Automation Health。

### 保证与审计视图

- 证据强度、新鲜度、完整性和可复现性；
- 验证到期和独立性；
- 抽样、局限、例外和失败测试；
- 哪些声明可以安全地向客户或审计方展示。

## 11. 报告语言

使用精确陈述：

- 好：“截至 2026-09-04，GPU-IaaS 服务 X 在 Region A/B、Release 2026.09 的 14 项适用 T0 已全部独立验证；另有两项 T1 证据将在 14 天内到期。”
- 差：“安全建设完成度 96%。”
- 好：“Dedicated SKU Y 专属 Host、GPU、NVLink Domain、租户数据网络和本地存储；Provider Telemetry 与 BMC 仍为共享服务商服务，并通过 JIT 访问。”
- 差：“完全专属、全面零信任。”

每个外部保证声明必须标识 Scope、Date、Version、Limitation、Exception 和 Verifier。

## 12. 保证节奏

| 周期 | 最低复核内容 |
|---|---|
| 持续 | T0、身份/策略、公网暴露、分配漂移、关键遥测、Root 使用、备份健康、Agent 高影响动作 |
| 每日 | 失败 Collector/Test、未知或无 Owner 关键状态、紧急暴露、隔离积压 |
| 每周 | 漏洞 SLA、Privilege、Release、Exception、Detection Failure、事件行动项 |
| 每月 | 高管风险与 Gate、客户承诺漂移、Metric Denominator/Source Quality |
| 每季度 | T0/T1 重验证、Access Review、Isolation Test、Revocation/Restore、Detection Replay、Agent Adversarial Evaluation |
| 每半年 | 重大事件、控制面恢复、Root 泄露、客户通知、破坏性自动化演练 |
| 每年 | 独立架构/渗透/隔离、Region DR/Known-good Rebuild、供应商与密码恢复 |
| 重大变更 | 立即重新确定范围并验证受影响断言 |

## 13. Assurance Package 模板

服务保证包至少包含：

1. 服务描述、画像、边界、Region、Version 与共享责任矩阵；
2. 适用控制集与生产准入结论；
3. Host、GPU/Cache/NVLink、Network/RDMA、Storage、Telemetry、BMC 和 Support 隔离声明；
4. Identity、Key、Artifact、Data/Model、Logging、Incident、Backup、Deletion 和 Residency 摘要；
5. 包含 Freshness、Strength、Source 和 Validator 的证据索引；
6. 负向路径、恢复、撤销、清除与事件演练摘要；
7. 当前重大 Finding、Exception、Compensating Control、Customer Impact 和 Remediation Date；
8. 独立复核声明和局限；
9. 下次验证日期和失效触发条件。

## 14. 常见度量失败

- 统计控制数量却不检查适用性和范围；
- T0 失败时仍报告综合完成百分比；
- 用 Scan、Alert、Policy 或 Ticket 数量证明风险下降；
- 不披露地把难覆盖资产从分母排除；
- 把缺失遥测解释为“没有事件”；
- 只报告平均响应时间，不报告 p95/max 和严重性分层；
- 把厂商 Dashboard 当成唯一观察路径；
- 允许 Control Owner 或 Agent 自我验证；
- 证据过期后继续计为 Pass；
- 通过修改定义或分母改善趋势；
- 只度量自动化速度，不度量审批绕过、错误完成、回滚和 Policy Violation；
- 恢复后没有独立 Identity、Integrity、Isolation 和 Data Check 就重新开服。

## 15. 可度量安全的最低定义

一个 NeoCloud 控制只有在范围和 Owner 已知、机制存在于真实部署路径、必需证据当前且受保护、相关禁止路径已测试、独立验证者能够复现断言、失败会触发明确运营响应，并在证据过期或重大变更后重新验证时，才能称为“可度量且有效”。
