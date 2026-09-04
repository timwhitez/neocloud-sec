# SemiAnalysis / ClusterMAX 公开安全问题覆盖审计

**画像版本：** 1.0.0  
**审计日期：** 2026-09-05  
**基础 NeoCloud 目录：** 1.0.0-draft.1  
**状态：** 项目独立编写的公开问题互操作覆盖层

## 1. 结论

原有 90 项 NeoCloud 控制已经覆盖 SemiAnalysis 公开 NeoCloud 安全资料提出的大类问题，包括租户逃逸、共享控制面薄弱、Container/GPU 软件漏洞、BMC/OOB 与 DPU 路径、InfiniBand/RDMA 隔离、补丁、监控和保证，但其中一部分只在原则层面隐含存在。

本轮更新将公开可核验的覆盖显式化：

- 将公开文章的 **5 类高层问题**由本项目拆解为 **40 项原子、面向测试的问题模式**；
- 更新前审计结果为：**17 项明确覆盖、17 项部分覆盖、6 项实质缺口**；
- 更新后，**40/40 均已映射**到稳定 NeoCloud 控制、最低证据与三类保证视角；
- 将当前主站公开 ClusterMAX Security 页面可独立枚举的 **20/20 项要求**映射到稳定控制和评估模板。

“已映射”不等于已经实施、通过、认证或获得 SemiAnalysis/ClusterMAX 背书。真实服务商仍须把每一行限定到具体 Service、Region、Cluster、SKU、Hardware、Firmware、Driver、Orchestrator 与日期，并提供当前证据和独立结论。

## 2. 原有基线已经较强的部分

原有目录已覆盖：

- API 对象/动作/租户授权与服务商管理面私有化；
- Compute、Storage、Ethernet、InfiniBand/RDMA、DPU 与 OOB 的租户分离；
- Kubernetes/Slurm Controller、Admission、Scheduler、Plugin 与 Node 安全；
- Host、Runtime、Driver、Firmware 与 Accelerator 生命周期；
- Data/Model/Artifact 的 Provenance、Admission、Revocation 与删除；
- Agent Identity、Tool Mediation、Approval、Stop、Trace 与 Verifier；
- 漏洞发现、分阶段修复与部署状态复验；
- 受保护遥测、事件指挥、恢复、清除与独立测试。

这些 90 项控制仍是稳定规范核心；新画像不会形成第二套竞争基线。

## 3. 本轮显式补齐的实质缺口

| 更新前缺口 | 本轮补强 |
|---|---|
| InfiniBand 主要围绕 P_Key，未显式枚举管理/服务密钥 | 增加 M_Key、SM_Key、SA_Key、C_Key/CC_Key、VS_Key、SHARP AM_Key、服务密钥与作业级密钥 |
| DPU 控制未点名 BlueField RShim/tmfifo_net0 与特权适配器路径 | 增加 RShim/tmfifo_net0、DPU Identity/Firmware、SR-IOV VF、QP0、MAD 与特权操作测试 |
| 共享 Kubernetes 与可观测性风险主要为隐含覆盖 | 增加 vCluster/共享控制面、Kubelet/Node API、Prometheus/Grafana Data Source、Credential 与租户隔离测试 |
| 补丁治理未显式建模 Vendor Embargo 和动态最低安全版本 | 增加预发布公告接入、基于真实可利用性的 Minimum-safe Version、Canary、部署复验、召回与回滚 |
| 未清晰分离客户可见测试、服务商验证与独立保证 | 增加 Tenant Black-box、Provider White-box、Independent Failure/Recovery 三类结果字段 |
| 漏洞披露与未来条目漂移不够显式 | 增加可信报告/整改、周期复测及来源/条目变化跟踪 |

## 4. 重要技术勘误：“Time-slicing”不是单一机制

原目录对通用术语 **Time-slicing** 的表述过宽。规范勘误现在明确区分：

1. 整卡独占；
2. 硬件分区；
3. 由 Hypervisor 仲裁的 vGPU；
4. 基于裸 Device Plugin 的调度器级 Time-slicing。

Kubernetes GPU Operator/Device Plugin 的调度器级 Time-slicing 本身不提供 Replica 间显存或故障隔离。受仲裁 vGPU 可能具有与 Product、GPU、Hypervisor、Manager/Driver、Firmware、Topology 和 Configuration 相关的隔离属性。不得根据 “Time-sliced” 标签推断隔离，必须声明并测试真实部署机制。

见 [`NCS-BASELINE-V1-ERRATA`](../../controls/neocloud-security-baseline.v1.errata.json)。

## 5. 三视角覆盖模型

每项原子问题分别从三类视角评估：

| 视角 | 核心问题 |
|---|---|
| **Tenant Black-box** | 客户能否仅通过受支持接口复现禁止可达性、隔离、权限、数据、版本或披露行为？ |
| **Provider White-box** | 架构、配置、密钥层级、Controller State、Owner、运营流程与证据是否支撑声明？ |
| **Independent Failure/Recovery** | 合格独立方能否在误配置、陈旧状态、撤销、故障、恢复和重分配条件下复现控制？ |

公开的客户视角 CLI/Audit 很有价值，但只是完整保证的一部分。高影响声明仍需架构/流程复核与受控故障/恢复测试。

## 6. 高优先级显式检查

### InfiniBand/RDMA 与 Fabric 管理

按适用性验证：

- P_Key Membership、Type、Default Partition、Endpoint Enforcement 与 Stale-state Cleanup；
- M_Key、SM_Key、SA_Key、C_Key/CC_Key、VS_Key 的 Owner、唯一性、轮换、撤销与审计；
- SHARP AM_Key、Service Key 与 Per-job Key 分离；
- Fabric Manager Identity、Least Privilege、Allowed GUID Policy 与受保护管理路径；
- SAETM/MAD 防滥用、QP0 限制及 SR-IOV VF 权限边界；
- RoCE VLAN/VXLAN 与 Storage Path 租户分离；
- DPU/NIC 分配、Firmware、Certificate、Controller State 与重分配清理。

### Kubernetes、共享节点与可观测性

验证：

- 服务商专用 API Server、etcd、Kubelet 与 Node Management Path；
- vCluster/共享控制面的 Host Cluster 与同步边界；
- Admission、RBAC、Privileged Workload、HostPath、Host Network/PID/IPC 及 Device Plugin/Operator 权限；
- CNI/CSI 与 Storage/Snapshot 授权；
- Prometheus/Grafana Tenant Label、Data Source Authorization、Dashboard/Query Isolation、共享服务凭据、Alert Routing、Retention 与 Support Access。

### 漏洞与补丁情报

建立：

- Container Toolkit、Runtime、Kubelet、Kernel、GPU Driver、Firmware、DPU、Fabric Manager 与 Orchestrator 的准确部署版本清单；
- 基于真实 Exploit Path 和部署配置动态计算的最低安全版本，而不是长期硬编码某个版本；
- 在合同可用时接入可信 Vendor Embargo/Prerelease Advisory；
- Canary/分阶段发布、Rollback、Quarantine 与部署后复验；
- 客户通知、漏洞披露和整改复测路径。

### 敌意制品与 AI 工作负载

Image、Renderer、Model、Checkpoint、Prompt、RAG Source、Memory、Skill、Plugin、Response 与 Cache 在通过策略准入前均按不可信输入处理。测试 Deserialization、Executable Format、租户 Cache/Session 隔离、Model Output、Tool Invocation 与 Egress。

## 7. ClusterMAX 边界

ClusterMAX 不只评估网络安全；其公开框架还包含 Lifecycle、Orchestration、Storage、Networking、Reliability、Monitoring、Pricing、Partnerships 与 Availability 等维度。本项目：

- 直接映射 Security；
- 映射 Lifecycle、Orchestration、Storage、Networking、Reliability、Monitoring 与 Availability 中安全相关部分；
- 不复刻 Price、商业合作、专有权重或总评分逻辑。

在审计截止时，主站公开 Security 页面可独立枚举 **20 项要求**。另一个 ClusterMAX Host 报告 **21 项 Security Criteria**，但额外一项无法被独立枚举。因此仓库只声明“主站当前公开页面 20/20 映射”，不声明 21/21、精确条目等价、评级或认证。

## 8. 交付物

- [机器可读公开问题画像](../../controls/semianalysis-public-findings-profile.v1.json)
- [画像 JSON Schema](../../controls/semianalysis-public-findings-profile.v1.schema.json)
- [v1 规范勘误](../../controls/neocloud-security-baseline.v1.errata.json)
- [40 项问题评估模板](../../templates/semianalysis-public-findings-assessment.csv)
- [主站公开 Security 页面 20 项评估模板](../../templates/clustermax-public-security-requirements-assessment.csv)
- [本地画像校验器](../../scripts/validate_semianalysis_profile.py)

## 9. 覆盖的定义

只有当稳定 NeoCloud 控制、最低证据和测试路径存在时，才称为 **Mapped**。只有真实服务商实施被限定到准确范围、产生当前证据，并由合格独立验证者返回 `PASS` 时，才称为 **Verified**。

任何失败、未知、过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的适用 T0 仍为 `NO_GO_NONCONFORMANT`。
