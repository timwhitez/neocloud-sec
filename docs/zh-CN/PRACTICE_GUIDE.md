# NeoCloud 网络安全实践指南

**版本：** 1.0.0-draft.2  
**基线日期：** 2026-09-04  
**适用读者：** NeoCloud 管理层、安全、平台工程、SRE、网络与 Fabric、Kubernetes、Slurm/HPC、数据与 AI、机房、支持、Trust & Safety、隐私、风险与审计团队

本指南将[白皮书](WHITEPAPER.md)、[安全基线](SECURITY_BASELINE.md)、[参考架构](REFERENCE_ARCHITECTURE.md)和[发展路线图](ROADMAP.md)转化为可执行的建设与运营方法。本文保持厂商中立；出现的产品类别仅作能力示例，不构成采购建议。所有实施声明都应同时应用[范围与局限](SCOPE_AND_LIMITATIONS.md)。

## 1. 从服务与信任决策出发，而不是从工具出发

每个生产服务应建立一个独立、可审计的安全评估包，至少包含：

1. 服务画像、合同边界和客户承诺；
2. 业务、技术、安全、数据和事件响应的唯一可追责 Owner；
3. 租户、身份、数据/模型、控制面、计算、GPU、存储、Fabric、BMC/OOB、供应商和支持运维边界；
4. 全量适用控制，以及每个“不适用”结论的理由和复核人；
5. 威胁模型、灾难性失败路径和共享责任；
6. 期望状态、策略决策点、执行点、失败模式、降级方式和回滚方式；
7. 证据来源、有效期、独立验证者及生产准入结论；
8. 未关闭风险、例外、客户影响、补偿控制和目标日期。

不要从购买 SIEM、CNAPP、PAM 或 AI 安全产品开始。先定义服务必须做出的信任决策，以及证明这些决策始终正确所需要的证据。

## 2. 不可妥协的运营规则

- **T0 是硬门槛，不是分数。** 任一适用 T0 未通过，即为 `NO-GO`。
- **未知不等于安全。** Owner、租户归属、互联网暴露、GPU 共享、P_Key/DPU 分配、Root Key 使用或恢复状态未知时，应视为断言失败。
- **实施者不能是唯一验证者。** 必须由不同人员、不同团队或合格的外部评估方复现实证并测试控制。
- **外部内容不能授予权限。** Ticket、Prompt、模型、Package、网页、文档和 Tool 输出只能作为观察，不得成为授权来源。
- **服务商独占能力不能转嫁给客户。** 客户无法控制的 BMC、Fabric Controller、Host Reset、服务商控制面与签名根，仍由服务商负责。
- **控制失效必须被设计。** 高影响控制应定义 Fail-closed、安全降级、隔离、回滚和人工恢复行为。
- **证据必须有有效期。** 缺少范围、身份、采集时间、完整性保护和可复现测试上下文的截图，只能作为弱证据。
- **恢复会改变信任状态。** 恢复上线前必须重新验证身份、制品完整性、租户隔离与数据正确性，而不能只验证“服务已启动”。

## 3. 最小团队与决策模型

小型组织可以一人兼任多个角色，但不能省略责任和独立复核。

| 角色 | 可追责决策 | 最低固定职责 |
|---|---|---|
| 高管风险 Owner | 风险偏好、不符合基线的紧急偏离、危机优先级 | 每月审阅关键风险 |
| CISO/安全负责人 | 控制模型、安全路线图、独立挑战 | 每周审阅 T0/T1 |
| 服务 Owner | 服务边界、客户承诺、残余风险 | 发布前和季度复核 |
| 平台能力 Owner | 身份、策略、计算、Fabric、存储、编排等共享控制 | SLO、变更和事件责任 |
| 数据/模型 Owner | 分类、允许用途、血缘、保留、导出、删除 | 每季度生命周期复核 |
| Incident Commander | 指挥、隔离、取证、沟通、恢复开服 | On-call 和演练就绪 |
| 独立验证者 | 测试设计、证据复现、PASS/FAIL 判定 | 按规定频率验证 |
| 客户/支持 Owner | 共享责任、支持访问、通知、保证材料 | 面向客户的准确性复核 |

每项控制只能有一个最终可追责 Owner；可以有多个实施者，但不允许“大家共同负责、无人最终负责”。

## 4. 前 90 天落地计划

### 第 0–7 天：建立指挥体系

交付：

- 为每个生产服务、Root/Signing Key、控制面、Fabric、BMC/OOB 环境和事件路径指定 Owner；
- 建立一个安全事件通信频道、严重性矩阵、On-call 升级链和紧急决策日志；
- 建立第一版服务与 Crown Jewel 清单；
- 对新增公网管理接口、新共享模式、Root 变更、Fabric 拓扑变更和未经审查的生产制品设置冻结或显式审批；
- 立即轮换或禁用来源未知、多人共用、无人认领或离职人员遗留的特权凭据。

退出条件：服务商能够随时建立事件指挥、撤销特权访问、定位某租户的活动资源并隔离一个服务。

### 第 8–30 天：停止关键暴露

优先完成：

- 服务商特权身份及按服务风险判定的高影响租户管理角色使用抗钓鱼 MFA；
- 服务商管理面私有化，BMC/OOB 走独立受控路径；
- 对最高风险 API 执行对象、动作和租户授权测试；
- 为每种对外销售的计算 SKU 声明精确隔离属性；
- 隔离或停止边界不清晰的 GPU 共享、RDMA/P_Key、DPU、存储或支持运维模式；
- 保护 KMS/HSM、签名根、Secret 与 Break-glass；
- 集中并保护身份、API、控制面、Kubernetes/Slurm、Fabric/BMC、密钥与支持访问日志；
- 建立跨租户访问、Root 泄露、控制面接管、破坏性自动化和不可恢复数据风险 Playbook。

退出条件：每个 T0 都有明确范围、Owner、状态、证据要求、验证者和有日期的整改计划。

### 第 31–60 天：形成权威状态

建设：

- 服务、资产、身份、依赖、数据流、模型、制品与供应商清单；
- 共享责任矩阵和客户安全联系人；
- 人员 Joiner/Mover/Leaver 与服务账户生命周期；
- 与真实资产关联的漏洞和暴露面发现；
- 数据/模型分类、驻留、保留、导出与删除要求；
- 备份清单、依赖关系和恢复前置条件；
- 对租户、调度器、Host、GPU、网络/Fabric、存储和配额进行期望状态与实际状态对账。

退出条件：未知资产和无 Owner 资产会被系统明确显示为缺陷，而不是在报表中被隐藏。

### 第 61–90 天：验证基础能力

执行：

- 独立 T0 验证；
- 特权撤销和 Break-glass 演练；
- 跨 API、调度、Host/GPU、存储、以太网、InfiniBand/RDMA 和遥测的负向隔离测试；
- 代表性的加速器与本地盘跨租户清理测试；
- Kubernetes/Slurm 控制面的恢复或已知可信重建；
- 一次包含客户、法务和隐私通知判断的完整事件演练；
- 一次关键数据/模型恢复，以及一次租户退租/删除演练；
- 发布共享责任矩阵和客户保证包。

退出条件：所有适用 T0 均为 `VERIFIED`；关键资产与日志覆盖率达到至少 95%；特权身份 Owner 覆盖率为 100%；所有失败演练均有可追责整改项。

## 5. 单项控制的实施生命周期

### 5.1 确定范围

记录服务、画像、租户、Region、版本、资产、身份、数据分类、供应商和排除项。“全局生效”但没有真实资产清单，不构成有效范围。

### 5.2 分析威胁与失败模式

至少描述：

- 攻击者和被攻陷主体假设；
- 正常路径和必须被拒绝的负向路径；
- 跨租户、信任根、破坏性、隐私、主权和可用性失败；
- 依赖不可用、Controller 状态过期、部分供应、回滚和恢复；
- 证据被篡改以及验证者失效。

### 5.3 定义控制契约

使用统一决策模型：

`主体 + 委托链 + 动作 + 资源 + 租户 + 目的 + 上下文 + 策略版本 → 允许/拒绝/审批 + 附加义务`

附加义务可以包括专属放置、限制出网、脱敏、双人审批、会话记录、配额、强制留证或动作后复验。

### 5.4 落实执行点

将预防性执行尽量放在受保护资源附近。中央策略服务可以下发决策，但网络、调度器、Node、KMS、Registry 或 Tool 边界不能在中央服务故障时静默 Fail-open。

### 5.5 生成证据

证据应来自真实部署路径，例如 API 导出、策略判定、签名证明、Controller 对账、负向测试、恢复轨迹、Hash、事件样本和独立观察。

### 5.6 独立验证

验证者必须复现断言、至少测试一条禁止路径、确认范围与时效，并返回 `PASS`、`FAIL`、`INCONCLUSIVE` 或 `NOT_TESTED`。只有 `PASS` 才能进入 `VERIFIED`。

### 5.7 持续运营与重新验证

发生重大变更、事件、控制失败、新服务/SKU/Region、Controller 或固件升级、身份/密钥层级变化、供应商变化、Agent 权限扩大、恢复/重建或证据过期后，必须重新确定范围并验证。

## 6. 十八个安全域的实施模式

| 安全域 | 最低实施要求 | 必做测试 | 强证据 |
|---|---|---|---|
| GOV | Charter、服务/控制 Owner、义务/风险/例外台账、独立保证 | 过期例外和无 Owner 服务不得显示为健康 | 已批准决策与当前服务范围保证材料 |
| ASM | API 驱动的资产/身份/数据/模型/依赖清单及对账 | 注入受控未知资产或过期分配并验证检测 | 带 Owner、租户上下文的期望/实际差异 |
| IAM | Federation、抗钓鱼 MFA、JIT/JEA、短期工作负载/Agent 身份、Break-glass | 拒绝、过期、紧急撤销与孤儿身份清理 | IdP/PAM/IAM 导出及撤销轨迹 |
| API | 租户正确授权、私有管理、Schema、Replay、配额/限速、变更审计 | 对象/动作/租户混淆与部分供应回滚 | 关联 Request、Policy、Desired/Actual State 与回滚事件 |
| NET | 平面分离、默认拒绝、租户感知的以太网/存储/Fabric/DPU/OOB 策略 | 跨租户与管理面可达性，含过期 VRF/P_Key/DPU 状态 | 拓扑、Controller 状态、Path Test 和对账结果 |
| CMP | SKU 隔离声明、Host 加固、安全 GPU 分配/重置、必要时证明 | 显存/重置/错误/隔离及跨分配清理 | 与硬件、版本、租户关联的分配与重置记录 |
| ORC | 私有且加固的 K8s/Slurm 控制面、RBAC、准入/作业策略、配额、Node/插件安全 | 特权工作负载/作业、调度逃逸、Controller 丢失、备份恢复 | Policy 导出、Audit、负向测试和重建轨迹 |
| DAT | 分类、租户授权、加密、血缘、安全格式、保留/删除 | 未授权模型/Checkpoint 访问、恶意格式、删除/退租 | 对象血缘、密钥/访问、清理与恢复证明 |
| KMS | 集中 KMS/HSM、Root 层级、短期 Secret、PKI 轮换、恢复 | Root/凭据撤销、证明失败、密钥恢复 | 密钥清单、Ceremony、审计、轮换与恢复轨迹 |
| SSC | 批准来源、BOM、Provenance、签名、隔离构建、准入、召回 | 拒绝未签名/未知制品，以及受污染制品召回 | Source-to-Deploy Provenance 与回滚证据 |
| ENG | 威胁模型、安全默认、IaC/Policy Review、测试门、Canary、回滚 | 不安全配置和失败发布回滚 | Review、测试、部署、漂移与部署后验证 |
| VEM | 资产关联发现、按可利用性/暴露优先、补丁 SLA、固件覆盖 | 紧急补丁/Canary 与部署版本复核 | Finding→Asset→Remediation→Rescan 链路 |
| TEL | 受保护关联遥测、覆盖清单、Detection-as-Code、租户安全保留 | 日志源失效、篡改尝试、ATT&CK/ATLAS 行为重放 | 事件样本、覆盖/新鲜度、测试结果、告警质量 |
| AIR | 清单、影响评估、不可变范围、Typed Tool、审批、预算、Stop、Verifier | Prompt Injection、Confused Deputy、Tool Abuse、Memory/Skill Poisoning | 签名配置、完整 Trace、策略判定和验证结果 |
| ABU | 租户信任分级、AUP、配额/速率/成本/容量、出网、Case 与申诉 | 配额绕过、未经授权的挖矿或其他 Policy 禁止工作负载、Denial-of-wallet、禁止出网 | 准入判定、执行原因、Case 和恢复记录 |
| IRR | 指挥、Playbook、取证就绪、通知、开服门 | 跨租户/Root/Agent/可用性演练 | Timeline、证据链、决策、恢复与独立关闭 |
| RES | 依赖/SLO/RTO/RPO、不可变备份、安全降级、重建/切换 | 主身份/密钥服务不可用时恢复，以及 Region/Fabric 故障 | 目标结果、完整性/隔离检查与开服审批 |
| PHY | 机房控制、BMC/OOB 隔离、固件/硬件清单、清除与保管链 | 未授权 OOB 路径和租户重分配清除 | 门禁、配置、固件状态、清除与销毁记录 |

## 7. 各服务画像上线检查

### 7.1 GPU IaaS

上线前验证：

- API 和镜像授权具备正确租户语义；
- VM/容器、Host、GPU/HBM/Cache、NVLink、存储、以太网、InfiniBand/RDMA、遥测和支持运维的隔离声明；
- 不同数据敏感级别和客户承诺允许使用的共享模式；
- 分配血缘、Reset/Error/Quarantine、本地存储清理和重分配证据；
- Host、Driver、Firmware 生命周期、Node 隔离与快速重建；
- 配额、计费、Denial-of-wallet、滥用和出网控制。

除非明确指出每个相关资源边界，否则不得使用“Dedicated”作为笼统营销声明。

### 7.2 裸金属 GPU

额外要求：

- 交付前删除服务商凭据；
- BMC/OOB 隔离与 JIT 支持访问；
- 已度量固件与批准的供应镜像；
- 专属或明确声明共享的网络/Fabric/存储边界；
- 完整退供流程，覆盖 GPU、本地盘、TPM、NIC/DPU、BMC 用户、证书和 Fabric 分配；
- 重分配前生成保管链和清除证明。

### 7.3 托管 Kubernetes

验证：

- 服务商专用 Controller 与 etcd 私有；面向客户的 API Endpoint 默认私有，或经过显式批准并实施强认证、来源/速率限制、DDoS 防护与完整审计；使用强管理员及工作负载身份；
- Restricted Pod Security Standards 与默认拒绝准入；
- RBAC 隔离、租户 Namespace/Account、Quota、Network Policy 与 Secret 边界；
- CNI、CSI、GPU Device Plugin、Operator、Webhook 与 Node 权限；
- 已签名并通过策略准入的镜像；
- Audit、Runtime Detection、Node Quarantine、etcd Backup、Restore 和 Known-good Rebuild。

### 7.4 托管 Slurm/HPC

验证：

- 私有、已修补的 Controller、Database、REST Endpoint 和强认证；
- Account、Association、Partition、QOS、Reservation 和 Job 所属关系；
- Prolog/Epilog、SPANK Plugin、Module、Container Runtime、共享存储和 Node 凭据；
- Queue/Priority 滥用防护；
- Node/GPU/Fabric 放置与清理能关联到 Job 和 Tenant Identity；
- Controller/Database Backup、Accounting Integrity、Failover 与 Recovery。
- Slurm Account、Association、Partition、QOS 和 MCS Label 可约束调度和信息可见性，但如果缺少 OS/Runtime、Storage、Network/Fabric 与 Credential Enforcement，就不是完整租户隔离边界。

### 7.5 模型训练平台

额外要求：

- 数据集目的、权利、来源、完整性、投毒检查和访问；
- 实验身份，以及 Code/Image/Config/Data/Model 全链路血缘；
- 安全 Checkpoint/Model 格式与受限反序列化；
- 中间制品、Cache、Secret 和临时数据清理；
- 评测完整性及其与训练影响的分离；
- 输出、导出、保留、删除、隐私和客户所有权。

### 7.6 模型服务平台

额外要求：

- Endpoint 和 Model 级授权；
- 租户安全路由、KV/Cache/Session 隔离、Prompt/Output 处理和日志最小化；
- 模型 Provenance 与 Runtime Integrity；
- 模型抽取、枚举、对抗输入、配额、速率、成本和容量控制；
- 安全 Fallback/Degraded Mode 与回滚；
- 隐私安全的事件证据。

### 7.7 Agent 平台

启用任何高影响 Tool 前必须具备：

- 唯一 Agent Identity、明确的人或服务委托方，以及不可变 Goal 和 Scope；
- 已批准且版本化的 Model、Prompt、Skill、MCP/Tool Server、Connector、Memory 与 RAG Source；
- Typed Tool Schema、最小权限、短期凭据，以及 Tenant/Data/Egress/Cost Policy；
- 对破坏性、外部、客户影响、高成本或不可逆动作采用确定性审批；
- 针对成功、预算、时间、重复失败、策略违规和不确定性的确定性停止；
- 抗篡改 Trace 与独立 Verifier；
- Agent 无权修改自身 Policy、Credential、Approval Authority、Evidence 或 Verifier。

### 7.8 主权或受监管服务

必须验证完整司法辖区边界，覆盖人员、身份、数据、密钥、支持、遥测、备份、供应商、事件响应和恢复。仅证明数据存储位置不等于满足主权要求。

## 8. 关键技术实践

### 8.1 端到端保留租户上下文

在每个 API Object、Message、Controller Record、Kubernetes/Slurm Object、Node Allocation、GPU Assignment、Fabric/Storage Rule、Log 和 Evidence 中使用不可变 Tenant ID 与 Request ID。缺失或冲突时拒绝请求；对账系统持续比较意图和实际状态。

### 8.2 有意识地选择加速器共享方式

将专属、硬件分区、受 Hypervisor 仲裁的虚拟化和调度器级共享视为不同产品。Kubernetes GPU 调度器级 Time-slicing/超卖本身不提供显存或故障隔离；受支持的 vGPU 模式可能具有不同属性。绝不能仅根据 ‘Time-sliced’ 名称推断隔离。应针对服务威胁模型，逐项声明并测试显存、Cache、DMA/IOMMU、Fault、Reset、Telemetry、Topology、性能干扰、Hardware、Hypervisor、Driver、Firmware 与 Configuration。

### 8.3 独立验证 InfiniBand/RDMA 与 DPU 边界

VPC 或 Kubernetes NetworkPolicy 不能证明高性能数据路径已经隔离。InfiniBand P_Key Membership 只是分区机制之一，不能单独证明完整租户隔离。必须在真实拓扑上测试 Membership Type/Enforcement、Default Partition Policy、RDMA Reachability、Fabric Manager Authority、DPU Assignment、Storage Access、Controller Stale State 和重新分配清理。Fabric 和 DPU Controller 应按服务商 Root 保护。

### 8.4 消除静态工作负载凭据

采用 Workload Identity、短期 Certificate/Token、Audience Restriction、Tenant/Resource Scope，并在合理场景下绑定 Node/Workload Attestation。Metadata Service 与默认服务身份不得向租户工作负载提供宽泛 Project/Fleet 权限。

### 8.5 将制品信任变成准入决策

对 Image、Package、Model、Checkpoint、Driver、Firmware、Operator、IaC 和 Agent Skill 保留 Source、Build/Train Lineage、BOM、Provenance、Signature、Scan Result、Policy Decision 与 Deployed Version。签名只证明某密钥执行了签名，不代表制品天然安全。

### 8.6 将证据与被评估系统隔离

关键日志与证据必须导出到具有足够管理与观察分离的边界，使普通源系统管理员无法静默修改记录；这并不普遍要求单独的物理系统。保留稳定 ID、时间同步、完整性、租户分区、访问审计、脱敏、保留和 Legal Hold。证据缺失本身应触发控制失败。

### 8.7 使用可信重建，而不是乐观清理

当 Root、Host、Controller 或 Build System 的可信状态不确定时，优先撤销并从已知可信源重建，而不是尝试“清理”。重新开服前需独立验证身份、制品完整性、租户隔离、数据完整性和监控。

## 9. 固定运营节奏

| 周期 | 必须执行的活动 |
|---|---|
| 持续 | 身份/策略判定、资产对账、公网暴露、关键日志、Root 使用、漏洞信号、GPU/Fabric 分配、配额/容量、备份健康、Agent 动作 |
| 每日 | 关键暴露和失败控制分诊；未知/无 Owner 资产；超期隔离；证据管道健康 |
| 每周 | 漏洞 SLA、特权变更、高风险租户/出网活动、发布、例外和未关闭事件行动项 |
| 每月 | 高管关键风险、T0/T1 状态、客户承诺漂移、供应商/容量风险、指标质量 |
| 每季度 | 权限复核、T0/T1 重验证、跨租户测试、恢复/撤销演练、检测重放、证据抽样、Agent 对抗复核 |
| 每半年 | 重大事件模拟、编排恢复、破坏性 Agent 场景、Root 泄露和客户通知演练 |
| 每年 | 独立架构/渗透/隔离评估、Region DR 或 Known-good Rebuild、供应商保证、密码恢复、路线图重置 |
| 重大变更 | 在受控发布前，或紧接发布后重新确定并验证受影响控制 |

## 10. 事件 Playbook 最低集合

每个 Playbook 必须包含：检测、指挥、范围查询、证据保全、隔离边界、身份/密钥动作、租户/客户影响、法务/隐私判断、恢复、重新开服条件和独立关闭。

NeoCloud 至少需要覆盖：

1. 跨租户 API、存储、GPU、Cache、Telemetry 或 Fabric 访问；
2. 服务商 Root、Signing Key、KMS/HSM、IdP、PAM 或 Break-glass 泄露；
3. Kubernetes/Slurm/Controller/Operator 或 Provisioning 接管；
4. BMC/OOB、DPU、Fabric Manager、Firmware 或供应链泄露；
5. 加速器显存残留、不安全共享、Reset 或 Error Domain 失败；
6. 恶意 Model/Checkpoint/Image/Package/Driver/Operator/Skill；
7. 破坏性或外传型 Agent/Tool 工作流；
8. Ransomware、Region/Fabric/Storage 故障、容量耗尽或备份失败；
9. 租户欺诈、未经授权的挖矿或其他 Policy 禁止工作负载、配额绕过或 Denial-of-wallet；
10. 数据/模型删除失败、Residency 违约或客户通知失效。

只有技术演练证明隔离、撤销与留证路径真正可用后，Playbook 才能标记为 Ready。

## 11. 证据质量与独立验证

一个证据项至少包含：

- Evidence ID 与 Control ID；
- Service、Profile、Environment、Tenant、Region、Asset、Identity 和 Version Scope；
- Assertion 与 Collection Method；
- Collector Identity 与 Observation Time；
- Source、Hash/Signature 或其他完整性保护及存储位置；
- Limitation、Sampling Method 与 Expiry；
- Validator、Test Procedure、Result、Finding 和 Retest Date。

证据强度由弱到强：

1. 声明或 Policy；
2. Screenshot 或人工整理报告；
3. 可重复 API/Query 输出；
4. 受保护 Runtime Event 或 Signed Attestation；
5. 授权的负向、恢复、故障注入或对抗测试；
6. 使用独立观察路径进行复现。

使用[证据登记表](../../templates/evidence-register.csv)和[度量与持续证明指南](METRICS_AND_ASSURANCE.md)。

## 12. Build、Buy 与深度集成

应自建或深度集成编码 NeoCloud 特有租户与拓扑语义的能力：

- 租户感知授权和 Desired/Actual Reconciliation；
- GPU、NVLink、Fabric、DPU、Storage 和 Scheduler Placement Evidence；
- Reset/Sanitization 和重新分配流程；
- Model/Checkpoint Lifecycle 与 Safe Loading；
- Agent Identity、Delegation、Tool Mediation、Approval、Stop 与 Verifier；
- 服务特定的 Containment 与 Reopening。

成熟、接口明确且证据可导出的能力可采购或使用托管/开源组件：

- IdP/MFA、PAM、KMS/HSM、Secret Manager、PKI；
- Vulnerability/Attack Surface Management；
- SIEM/Data Lake、EDR/Runtime Security、Case Management；
- Backup、DDoS/WAF/API Gateway、Signing/Transparency Infrastructure。

供应商必须支持可导出日志和 API、租户安全行为、高可用与安全降级、安全更新、事件通知、数据处理、独立测试、迁移/退出和稳定身份集成。厂商控制台“全绿”不能证明服务边界完整覆盖。

## 13. 客户与供应商尽调问题

要求对方精确回答：

- 哪些 Host、GPU、Memory/Cache、NVLink、Network、RDMA、Storage、Telemetry 与 Support Resource 是专属或共享？
- Tenant Context 如何从 API Request 一直保留到物理分配和删除？
- 使用哪些 GPU Sharing Mode，显存、故障和 Reset 保证如何测试？
- P_Key、RDMA、DPU、BMC/OOB 与 Fabric Controller 如何隔离？
- 谁能通过什么 JIT 流程访问客户数据/模型，留下何种证据？
- Plaintext 和 Key 在哪里存在，谁控制，Root 如何恢复？
- 哪些制品必须具备 BOM、Provenance、Signature、Admission 和 Recall？
- 通知、证据交换、恢复、删除、Residency 与 Offboarding 承诺是什么？
- 正常运营和事件期间，哪些控制分别由 Provider、Customer 或双方负责？
- 哪些保证声明由独立方在什么时间、针对哪个具体服务/版本测试，仍存在哪些例外？

## 14. 必须拒绝的反模式

- 用一个综合合规分数隐藏失败的 T0；
- 使用“Dedicated”“Zero Trust”“Encrypted”“Confidential”等词却不说明精确边界；
- 将 Kubernetes Namespace 或 VPC 隔离作为 RDMA/GPU/Storage 隔离证明；
- 将调度器级共享 GPU Replica，或任何缺乏部署特定证据的 Sharing Mode，宣传为硬件级租户隔离；
- 向工作负载暴露共享服务商身份或宽权限 Metadata Credential；
- 长期 Standing Admin Privilege 和无记录 Support Session；
- 只因签名有效就接受制品，而不验证 Source/Build/Key Policy；
- 只用 Screenshot 作为控制证据；
- 从未真实恢复过的 Backup/Restore 计划；
- 允许 AI Agent 自己批准高影响动作或把自己的工作标记为 Verified；
- 缺少 Owner、补偿控制、到期时间、客户影响和整改计划的例外；
- 购买安全产品却没有服务 Owner、集成契约、证据输出和失败模式。

## 15. Definition of Done

生产服务只有同时满足以下条件才可准入：

- 边界、服务画像、共享责任和客户承诺明确；
- 所有适用 T0 均被独立标记为 `VERIFIED`；
- 关键资产、身份、公网暴露、Root、GPU/Fabric/OOB、数据/模型和制品状态已知；
- 负向隔离、撤销、恢复/重建、事件和清除测试通过；
- 证据处于有效期内，范围明确、受保护、可复现并经过独立复核；
- 未关闭重大风险具有可追责、已授权、带期限的决策；
- 监控能发现漂移，团队能在不临时 improvisation 的情况下完成隔离与恢复。

机器可读[控制目录](../../controls/neocloud-security-baseline.v1.json)是控制 ID、等级、中英文要求、证据画像、验证画像和度量关联的规范来源。
