# NeoCloud Cyber Security 安全基线

**版本：** 1.0.0-draft.2  
**基线日期：** 2026-09-04  
**规范性机器可读目录：** [`controls/neocloud-security-baseline.v1.json`](../../controls/neocloud-security-baseline.v1.json)

## 1. 目的与规范性语言

本基线定义 GPU IaaS、裸金属 GPU、托管 Kubernetes、托管 Slurm/HPC、模型训练、模型服务、Agent 平台以及主权/监管 NeoCloud 服务的最低网络安全结果。

- **必须**表示强制要求，除非经过 Review 的适用性决定证明其不在服务边界内。
- **应该**表示强建议，省略时必须记录理由和剩余风险 Owner。
- **可以**表示可选实现。
- 外部框架映射仅供参考，不构成认证、合规或精确等价声明。

本基线包含 **18 个域、90 项控制**。JSON 目录是中英文要求、最小证据、验证频率、指标、等级和 Control ID 的权威记录；本文解释如何评估和应用。等级、硬门、数量和目标值是本仓库定义的规范规则，并不代表普遍行业共识；详见[范围与局限](SCOPE_AND_LIMITATIONS.md)。

## 2. 评估生命周期

每个服务选择一个或多个 Service Profile，并评估所有控制。评估记录必须包含 Service/Profile、Applicability、Asset/Tenant Scope、Provider/Customer Owner、Implementation State、Evidence ID、Test Method、Independent Validator、Last Verification、Evidence Expiration、Exception、Residual Risk 和 Target Date。

唯一允许的完成生命周期是：

`PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`

- `READY` 要求范围、Owner、目标日期、依赖、证据和测试方法完整。
- `IMPLEMENTED` 表示机制已部署，但有效性尚未独立证明。
- `CANDIDATE_DONE` 表示责任人已经提交完成证据。
- 只有独立验证者返回 `PASS` 才能进入 `VERIFIED`。
- 证据失败、不完整、相互矛盾或过期时必须退回更早状态。

Screenshot 或制度文档通常不能单独作为充分证据。优先使用 API Export、Signed Attestation、Policy Evaluation、Immutable Audit Event、Reproducible Query、Negative Test、Restore/Rebuild Trace、Hash 和来自实际部署服务的独立观察。

## 3. 采用等级

| 等级 | 含义 | 最低要求 |
|---|---|---|
| **T0—硬门槛** | 在开放生产算力或处理租户数据前不可妥协的条件 | 每个适用 T0 必须独立 `VERIFIED`，否则生产 **NO-GO** |
| **T1—基础级** | 责任、清单、最低安全卫生、可见性、响应与恢复 | 前 90 天或规模化前完成 |
| **T2—生产级** | 支撑多租户正式商用的可复用、策略化、可度量控制 | 可持续 GA 运营所需 |
| **T3—可信级** | 面向敏感、受监管、主权或专属服务的独立和高保证控制 | 服务作出相应保证承诺时必须采用 |
| **T4—自适应级** | 持续验证和受控自动化 | 只有在权限、失败模式、回滚和 Verifier 均已证明后采用 |

任何分数都不能抵消 T0 失败。可追责高管和安全 Owner 可以批准限时紧急偏离以维持服务，但失败或未知 T0 在符合性判定上仍然是 `NO-GO`：不得标记为 `PASS` 或 `VERIFIED`，不得对外声称符合本基线，并必须明确客户/法律影响、补偿控制、回滚条件和整改截止时间。

## 4. 生产硬门槛

下列任一适用条件未知或未验证时，服务不得进入或继续保持正式生产：

1. **责任：** 每项生产服务、关键依赖、Root/Signing Key、Control Plane、Fabric 和 Incident Path 都有 Owner。
2. **共享责任：** Provider/Customer/Shared 对 Identity、Guest/Workload、GPU/Fabric、Data/Model、Logging、Incident、Backup、Deletion 和 Support 的责任明确。
3. **清单：** 关键 Service、Asset、Identity、Public Endpoint、GPU/Fabric/OOB、Data/Model 和高影响 Artifact 已知并持续对账。
4. **高权限身份：** 服务商高权限与租户 Owner 使用批准的强 MFA；禁止共享 Admin；紧急 Revocation 和 Break-glass 已测试。
5. **API 正确性：** 每个关键公网/内部 API 认证调用者，并由服务端验证 Object/Action/Tenant Authorization。
6. **私有管理：** Provider Control Plane、Orchestrator DB/Controller、Fabric Management、BMC/OOB、Debug 和 Support Path 不得直接暴露给公网或 Tenant Data Plane。
7. **端到端隔离：** Tenant/Authorization Context 在控制面对象转换中保持，并通过权威绑定在 Scheduler、Host、GPU、Storage、Ethernet、InfiniBand/RDMA、DPU、Telemetry 和 Support 边界执行。
8. **计算 SKU 声明：** 每种 SKU 的 Host、GPU/HBM/Cache、NVLink、Fabric、Storage、Telemetry 和 Support 隔离性质/限制已记录并测试。
9. **加速器安全：** 敏感工作负载不使用缺乏所需 Memory/Fault Isolation 的共享模式；Reset、Error、Quarantine 和 Tenant 间 Cleanup 已验证。
10. **编排安全：** 服务商专用 Kubernetes/Slurm Controller 与 Database 私有、补丁及时、强认证、与租户分离、可备份和恢复。任何面向客户的管理 API 默认私有，或经过显式批准并实施加固、来源/权限限制、抗滥用保护和完整审计。
11. **数据/模型保护：** Crown-jewel Data/Model 有 Owner 和 Classification，并按策略实施租户授权、加密、保留、导出、删除和清除。
12. **信任根/Secret：** 关键 Key 集中治理，静态 Secret 最小化，Signing/Root 使用受限、审计且可恢复。
13. **制品已知：** 生产 Image、Driver、Firmware、Operator、IaC Bundle、Model、Checkpoint 和 Skill 均来自批准且已盘点的来源。
14. **威胁驱动工程：** 重大发布具备当前 Threat Model、安全验收、可靠 Rollback 和未解决风险决定。
15. **暴露修复：** 持续发现 Internet/Root 漏洞和暴露，并在风险 SLA 内修复或隔离。
16. **受保护审计：** Identity、Policy、API、Control Plane、Root/Key、Orchestrator、Host/GPU/Fabric/BMC、Data/Model、Build、Support 和 Agent 行为产生受保护关联证据。
17. **Agent 权限：** 生产 Agent 全量盘点；Tool/Connector 均经 Policy Broker；高影响行为不能自我批准；非可信内容不能改变 Goal/Scope/Permission。
18. **滥用与容量：** AUP、紧急 Abuse Response、Quota、Rate、Cost、Queue 和 GPU Capacity 控制存在且可测试。
19. **事件指挥：** 24×7 可建立指挥、保全证据、吊销 Root/Identity、在可靠边界隔离、评估通知并决定重新开服。
20. **恢复：** 关键 Control Plane 和 Provider-managed Data 具有受保护备份，并在声明 RTO/RPO 内完成过 Restore 或 Known-good Rebuild。
21. **物理信任根：** Facility/BMC/OOB 受控，Tenant/普通 Corporate 直接访问被拒；Device/Local Storage 在重新分配前完成可验证清除。

## 5. 按安全域划分的控制目录

### GOV—治理、风险、合规与共享责任

**结果：** 决策可追责、责任明确、例外到期、保证可由独立证据支持。

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

**结果：** 每个行动主体都具备强、受限、短期且可复核的身份。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-IAM-01 | T0 | 集中联邦与抗钓鱼 MFA |
| NCS-IAM-02 | T0 | 最小权限、JIT 管理与 Break-glass |
| NCS-IAM-03 | T2 | 短期工作负载与服务身份 |
| NCS-IAM-04 | T1 | 租户、服务账户与访问生命周期 |
| NCS-IAM-05 | T2 | Agent 身份、委托与动作范围 |

### API—控制面、API 与管理接口

**结果：** 租户正确授权、私有服务商管理、抗滥用、变更可追踪和 API 生命周期安全。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-API-01 | T0 | 租户正确的 API 认证与授权 |
| NCS-API-02 | T0 | 私有且受治理的管理接口 |
| NCS-API-03 | T1 | API 抗滥用与资源控制 |
| NCS-API-04 | T1 | 控制面变更完整性与审计 |
| NCS-API-05 | T2 | 安全 API 生命周期、测试与退役 |

### NET—网络、高性能互联、RDMA/InfiniBand 与 DPU 隔离

**结果：** 每条报文、存储、管理和直接内存路径均经过证明隔离。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-NET-01 | T0 | 安全平面分离与默认拒绝 |
| NCS-NET-02 | T0 | 端到端租户网络、存储与 Fabric 隔离 |
| NCS-NET-03 | T1 | InfiniBand P_Key 与 RDMA 隔离验证 |
| NCS-NET-04 | T1 | 出网、DPU/NIC 与带外隔离 |
| NCS-NET-05 | T3 | 持续路径与隔离保证 |

### CMP—计算、虚拟化、裸金属、GPU 与加速器隔离

**结果：** 隔离明确、分配/重置安全、Host 加固、供应可信，并提供高保证选项。

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
| NCS-ORC-01 | T0 | 加固且访问受限的编排控制面 |
| NCS-ORC-02 | T1 | RBAC、准入、作业与特权工作负载控制 |
| NCS-ORC-03 | T1 | 租户调度、配额与放置边界 |
| NCS-ORC-04 | T2 | 运行时、节点、Secret 与插件安全 |
| NCS-ORC-05 | T2 | 编排系统备份、恢复与对抗验证 |

### DAT—数据、数据集、模型、制品与隐私保护

**结果：** 分类、访问、使用、血缘、输出、保留、删除和退租全过程受控。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-DAT-01 | T0 | 数据与模型分类、Owner 和生命周期 |
| NCS-DAT-02 | T0 | 加密、租户分离与访问控制 |
| NCS-DAT-03 | T1 | 血缘、完整性与安全制品处理 |
| NCS-DAT-04 | T1 | 删除、导出、退租与清除 |
| NCS-DAT-05 | T2 | 隐私、DLP 与敏感遥测/输出保护 |

### KMS—Secret、密钥、PKI、证明与机密计算

**结果：** 密码信任根受保护、Secret 短期化、身份/密钥释放受治理、Root 恢复经过测试。

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

**结果：** 威胁驱动设计、安全默认、变更可 Review、测试门、漂移控制和可靠回滚。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-ENG-01 | T0 | 安全开发生命周期与威胁驱动设计 |
| NCS-ENG-02 | T1 | IaC/Policy-as-Code 与安全默认 |
| NCS-ENG-03 | T1 | 受保护变更、同伴 Review 与职责分离 |
| NCS-ENG-04 | T2 | 安全测试门、Canary 与回滚 |
| NCS-ENG-05 | T2 | 工程隐私、Secret 与可观测性要求 |

### VEM—漏洞、暴露面、补丁与固件管理

**结果：** 全层持续发现并按风险修复，且通过部署范围验证闭环。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-VEM-01 | T0 | 持续漏洞与暴露面发现 |
| NCS-VEM-02 | T0 | 风险驱动修复与紧急补丁 |
| NCS-VEM-03 | T1 | 固件、驱动与平台补丁生命周期 |
| NCS-VEM-04 | T1 | 外部攻击面与配置漂移 |
| NCS-VEM-05 | T3 | 独立渗透、隔离与对抗测试 |

### TEL—遥测、检测工程、威胁情报与审计

**结果：** 证据完整、租户安全、抗篡改，检测经过真实威胁验证。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-TEL-01 | T0 | 集中、受保护且租户安全的遥测 |
| NCS-TEL-02 | T0 | 信任根与控制边界强制审计 |
| NCS-TEL-03 | T1 | 映射威胁的检测工程 |
| NCS-TEL-04 | T1 | 证据保留、时间完整性与客户安全访问 |
| NCS-TEL-05 | T3 | 持续控制监控、威胁狩猎与 Purple Team |

### AIR—AI 应用、Agent、Tool、Skill 与 Prompt 安全

**结果：** 权限受限、上下文/制品受保护、工具经策略仲裁、停止确定且结果独立验证。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-AIR-01 | T0 | AI 系统与 Agent 清单及安全风险评估 |
| NCS-AIR-02 | T1 | 输入、Prompt、输出与 Schema 强制 |
| NCS-AIR-03 | T0 | Tool、Skill 与 Connector 最小权限及审批门 |
| NCS-AIR-04 | T2 | 模型、RAG、Memory 与 Skill 完整性 |
| NCS-AIR-05 | T4 | Agent Trace、确定性停止与独立验证 |

### ABU—滥用防护、租户信任、出网与可接受使用

**结果：** 分级准入、资源/外部交互控制、误用检测、安全执行与申诉。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-ABU-01 | T1 | 风险驱动租户身份与信任分级 |
| NCS-ABU-02 | T0 | 可接受使用、禁止活动与滥用响应 |
| NCS-ABU-03 | T0 | 配额、速率、成本与容量保护 |
| NCS-ABU-04 | T1 | 出网与外部交互控制 |
| NCS-ABU-05 | T2 | 滥用检测、协同与申诉质量 |

### IRR—事件响应、取证、危机管理与恢复

**结果：** 快速指挥、证据保全、安全隔离、可辩护通知、恢复与验证闭环。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-IRR-01 | T0 | 事件指挥、角色与安全通信 |
| NCS-IRR-02 | T1 | NeoCloud 特定事件 Playbook |
| NCS-IRR-03 | T1 | 取证就绪与证据保全 |
| NCS-IRR-04 | T1 | 客户、监管与生态通知 |
| NCS-IRR-05 | T2 | 演练、经验反馈与验证闭环 |

### RES—韧性、可用性、容量、备份与灾难恢复

**结果：** 降级行为安全、备份受保护、切换/恢复/重建经过测试并验证后开服。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-RES-01 | T0 | 服务目标、依赖与恢复要求 |
| NCS-RES-02 | T0 | 不可变备份与验证恢复 |
| NCS-RES-03 | T2 | 控制面与 Region 韧性 |
| NCS-RES-04 | T1 | 容量、DDoS、队列与 GPU 耗尽韧性 |
| NCS-RES-05 | T3 | 已知可信重建、灾备与退出可迁移性 |

### PHY—物理、机房、BMC、硬件生命周期与介质清除

**结果：** 机房/硬件信任根受控、OOB 隔离、设备状态可信、清除/退役可证明。

| ID | 等级 | 控制 |
|---|---:|---|
| NCS-PHY-01 | T0 | 机房、物理访问与环境安全 |
| NCS-PHY-02 | T0 | BMC 与带外信任根安全 |
| NCS-PHY-03 | T1 | 安全硬件供应、固件清单与锁定 |
| NCS-PHY-04 | T0 | 加速器、本地盘与 Host 清除验证 |
| NCS-PHY-05 | T1 | 退役、介质销毁与保管链 |

## 6. 服务画像叠加要求

- **GPU-IaaS：** API 正确性、VM/Container 边界、GPU Sharing/Reset、Fabric/Storage 隔离、镜像来源和 Host Lineage。
- **Bare-Metal-GPU：** Provision/Deprovision 仪式、BMC/OOB、Firmware State、专属 Network/Fabric、Provider Credential Removal 和 Sanitization。
- **Managed-Kubernetes：** 私有/加固控制面、Tenant RBAC、Restricted Admission/PSS、CNI/CSI/Device Plugin、Workload Identity、etcd Backup 和 Node Response。
- **Managed-Slurm-HPC：** Controller/Database/Auth、Account/Association/QOS/Partition、Prolog/Epilog/Module、Shared Storage、Queue/Fabric Isolation。
- **Model-Training：** Dataset/Model Lineage、Poisoning Resistance、Safe Format、Checkpoint Access、Temp/Cache Cleanup 和 Experiment Evidence。
- **Model-Serving：** Endpoint/Model Authorization、Prompt/Output Handling、KV/Cache Isolation、Extraction/Abuse、Quota 和 Availability。
- **Agent-Platform：** Delegation、Tool/Skill Provenance 与 Least Privilege、确定性 Approval/Stop、Trace、Verifier、Memory Integrity 和 External-content Boundary。
- **Sovereign-Regulated：** Jurisdiction-bounded People、Data、Key、Support、Telemetry、Backup、Supplier、Notification 和 Independent Assurance。

## 7. 证据新鲜度与重验证触发器

证据超过要求频率或发生影响声明的重大变化即为过期。触发重验证的变化包括 Service SKU/Sharing、New Region/Fabric、Orchestrator/Controller Upgrade、Identity/Key Hierarchy、Data Flow/Supplier、Model/Agent/Tool Capability Expansion、Control Failure、Incident、Restore/Rebuild 或 Verifier 无法复现。

默认最低重验证频率为：T0 在可行时持续监控、至少每季度独立验证并在重大变更后复验；T1 至少每季度及重大变更后；T2 至少每半年及重大变更后；T3 至少每半年由 Control Owner 复核、至少每年独立评估，并在重大变更后复验；T4 持续度量、每季度对抗/失败模式复核，并在重大变更后复验。服务威胁模型、合同、事件或监管要求可以缩短周期。

## 8. 生产决策算法

```text
if 任一适用 T0 未独立 VERIFIED:
    decision = NO-GO
elif 关键证据过期或服务范围未知:
    decision = NO-GO
elif 未解决高风险缺乏可追责批准:
    decision = NO-GO
elif Restore、Revocation、Isolation、Incident 或 Sanitization 测试失败:
    decision = NO-GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

采用[基线评估模板](../../templates/baseline-assessment.csv)与[度量指南](METRICS_AND_ASSURANCE.md)。Control 变更遵循 [GOVERNANCE.md](../../GOVERNANCE.md)。
