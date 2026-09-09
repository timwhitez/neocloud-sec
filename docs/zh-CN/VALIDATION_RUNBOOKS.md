# NeoCloud 验证手册

**复核日期：** 2026-09-09 · **画像版本：** 1.0.1 · **核心目录：** 1.0.0-draft.1

本手册是项目自行设计的测试方案，不是已经执行的基础设施测试、厂商认证或 SemiAnalysis 评分规则。这十类运营验证手册补充[公开问题画像](../../controls/semianalysis-public-findings-profile.v1.json)，不修改其 Schema，也不声称已建立机器校验的逐项关联。实施时使用包含版本绑定勘误的[目录编译器](../../scripts/compile_catalog.py)。

## 授权与证据要求

测试前记录服务、区域、集群、SKU、租户标识、实际运行版本、获批目标与动作、窗口、操作人、独立复核人、恢复负责人和中止条件。使用两个带有不同无害标记的模拟租户，仅测试明确授权的资源。不得将真实客户数据、管理密钥、原始显存或保密厂商公告写入本仓库。

每个测试同时包含允许路径与禁止路径。由于无关系统故障造成的访问失败，不能作为授权控制通过的证据。记录判定、目标侧实际影响、请求标识、生效策略和时间。租户黑盒、服务商白盒、独立故障／恢复三个视角分别记录；不适用需要范围理由和批准记录，不能把未执行视角填成 PASS。任何适用 T0 缺少当前充分证据时，仍为 NO_GO_NONCONFORMANT。可选[证据与公告记录校验](../EVIDENCE_VALIDATION.md)只检查元数据，不证明这些结果。

<a id="rb-01"></a>
## RB-01 — API、调度、vCluster 与节点边界

**准备：** 为模拟租户 A/B 创建资源、工作负载身份与获批凭据，导出生效 RBAC、准入规则、同步器／Operator 权限、CNI 与节点 API 配置。

**测试：** A 能访问自己的资源，但不能读取、挂载、修改或冒充 B 的资源。覆盖 kubelet、宿主集群对象和服务账户令牌。vCluster 必须检查同步组件的宿主集群权限以及共享节点组件；虚拟控制面本身不证明节点隔离。使用安全的中断分配和凭据过期场景，不提交破坏性工作负载。

针对 NCS-IAM-04、NCS-KMS-02 和 NCS-ORC-04，还要把撤权沿 Operator 追踪到后端：撤销模拟资源之间此前允许的跨命名空间关联，观察协调及凭据删除／轮换，验证旧的一次性后端凭据被拒绝，而独立获授权身份仍可正常访问 [S9]。Kubernetes 拒绝不等于已撤销现有数据库凭据。检查服务账户实际权限和所有已启用授权路径；控制器选择器、本地缓存不能替代资源侧授权 [S10]。保存脱敏判定／请求标识，不保存凭据值。

**验收／留证：** 租户上下文贯穿控制器转换，禁止请求在目标侧无实际影响，部分分配被回滚或隔离。保存脱敏配置、两类请求轨迹和实际状态对账。出现异租户数据或意外特权立即中止；先控制影响，必要时轮换凭据，经独立复测后才能重新开放。

<a id="rb-02"></a>
## RB-02 — 运行时漏洞与安全发布

**准备：** 按资产盘点已安装及实际运行的 Toolkit、Runtime、Driver、Firmware、Kernel 和编排版本，关联受影响配置、厂商修复／回移补丁、兼容性与客户影响。版本号更大不等于安全。

**测试：** 在隔离金丝雀环境按批准方案更新，按需重启组件并验证实际加载版本及范围内回归；模拟更新失败和节点清单过期。建立公告接收与升级路径。Embargo／预发布资格依赖厂商安排，不是所有服务商天然具备的能力。

针对 NCS-ASM-01、NCS-ORC-04 和 NCS-CMP-03，区分上游修复、发行版回移、云厂商镜像发布和真实节点替换。记录镜像／构建标识、替换或启动证据，再验证作业完成、策略执行和恢复。修改镜像族指针不会更新已有节点 [S11]。启用热补丁不取消具体公告的重启要求，应看本次更新而非仅按长期日历推断 [S12]。只有服务商能够提供的证据仍由服务商负责。

功能门开启、配置用户命名空间与节点真实无根运行是不同状态。可选迁移前检查 CNI／CSI／设备／GPU 组合的支持与恢复；不强制采用 Beta 功能，也不将其视为所有内核漏洞的防护 [S17]。

**验收／留证：** 有漏洞或状态未知的节点不能静默回到健康资源池。回滚若恢复已知可利用配置，必须隔离并明确保持不符合基线状态。保留公告标识、可用时的签名来源证据、金丝雀结果、部署状态和复测结果。违反服务目标或丢失恢复通道立即停止。

<a id="rb-03"></a>
## RB-03 — BlueField、RShim 与服务商恢复路径

**准备：** 记录 DPU 型号、BSP／DOCA／固件、NIC／DPU 模式、宿主权限、Arm 侧控制权与服务商 BMC 恢复方式。DPU 模式并非自动防御恶意宿主；NVIDIA 文档说明了信任宿主的默认设置及额外的限制宿主控制 [S3]。

**测试：** 从获批模拟租户宿主检查 RShim／TMFIFO、固件写入、Tracer／Counter 和端口控制权的预期拒绝边界。验证配置与访问判定，不读取密钥、不刷写真实生产硬件。确认服务商恢复路径独立于租户宿主。模式切换和复位仅在获批实验环境按支持矩阵执行。

**验收／留证：** 生命周期转换后被禁止能力仍被禁止，服务商恢复可用，重用前清除过期分配。保留权限状态、脱敏路径测试和恢复结果。管理访问丢失即中止，不跨 DPU 代际套用统一复位命令。

<a id="rb-04"></a>
## RB-04 — InfiniBand、RoCE 与管理密钥

**准备：** 区分 P_Key 分区成员关系、管理认证和载荷加密。逐项盘点适用的 M_Key、SM_Key、SA_Key、VS_Key、PM_Key、拥塞控制密钥、Class C／N2N 和 SHARP AM／Job／Service Key。不能将 Class C／N2N 静默等同于名称相近的拥塞控制密钥。记录密钥标识和 Owner，不记录密钥值。参数名称须匹配真实 UFM／OpenSM 版本 [S4、S5]。

**测试：** 验证允许数据路径与禁止跨租户路径；独立核查默认分区、成员类型、PF／VF 权限、QP0／MAD 限制和获准管理器 GUID。检查适用 SA 信任、限速和 SHARP 作业隔离。控制台安全检查属于配置证据，并非端到端证明。在实验环境以受限流量验证过期控制器状态和重新分配；不得洪泛生产 Fabric，也不得在发现阶段轮换全网密钥。

对于 CNI 或云网络迁移，默认拒绝上线前盘点 OS／CNI 兼容性以及 DNS、服务、存储依赖；同时测试允许的业务流量与禁止的跨租户路径，保留独立 OOB 通道。厂商退役通知是范围内迁移触发条件，不应因此把所有云统一到同一 CNI。Kubernetes NetworkPolicy 不替代 Fabric、DPU 或存储隔离 [S18]，仍需 RB-03、RB-06 和 RB-09。

**验收／留证：** 非授权管理操作和跨租户通信失败，正常控制流量不因策略变更失效。保存拓扑、脱敏生效配置、路径结果和回滚／恢复轨迹。出现互联不稳定、异常可达或管理仲裁丢失立即中止。

<a id="rb-05"></a>
## RB-05 — Prometheus、Grafana 与遥测

**准备：** 为 A/B 注入不同无害时序数据，记录 Grafana 版本／版本类别、组织、数据源凭据以及直连后端、代理和 Remote Read 路径。Prometheus 默认安全模型允许 HTTP 用户访问其时序数据；标签不是授权 [S6]。Grafana Viewer 可能查询数据源，而不只读取可见看板 [S7、S8]。

**测试：** 绕过看板导航直接查询，尝试异租户查询和伪造租户选择器。确认上下文由可信代理／后端绑定，而不是由调用者自报。验证告警路由、保留和支持访问。使用数据源权限前核实具体产品版本是否支持该功能。

威胁模型还应覆盖共享看板创建／导入和可视化渲染，而非只有查询；分离写入与查看权限，检查实际部署的看板组件及托管服务补丁状态 [S13]。只用厂商支持的无害样本和授权检查，不复现浏览器执行载荷。自建版本已修复不证明托管服务完成了自己的修复。

以租户安全的标识关联策略变化、Operator 协调、凭据生命周期、后端拒绝与存储判定。逐个云审计来源记录支持的服务／动作、启用状态、投递和保留，验证预期无害事件实际送达且缺失来源能够被发现。提供审计功能或采集器成功退出不等于覆盖有效 [S14]；不得将真实租户记录导出到本仓库。

**验收／留证：** 隔离落实到后端凭据／查询边界，直连或编辑标签不能绕过；必要时采用分离组织和权限受限的后端。保留查询结果和后端授权。GPU Operator 时间切片下，须记录 DCGM-Exporter 的容器归因限制 [S1]，不能从不存在的指标推导容器责任。出现异租户时序或密钥暴露立即中止。

<a id="rb-06"></a>
## RB-06 — 存储、快照、删除与恢复

**准备：** 创建 A/B 模拟对象、卷和快照，记录 CSI／控制器身份、KMS 归属、不可变备份保留期和合同删除范围。

**测试：** 在实际存储边界拒绝异租户挂载、导出和恢复。在主依赖不可用时恢复测试备份。检查副本、缓存、快照、本地介质和受保留期限制的延后删除。删除请求不能被描述为所有不可变备份立即完成物理擦除。

针对 NCS-API-01、NCS-DAT-04 和 NCS-ORC-02，联合检查 PV 创建权限、实际删除选项、CSI 身份、文件系统／接入点归属与云资源策略 [S15]。优先采用厂商修复和最小权限；使用惰性单元样本或厂商支持的非破坏检查验证归属，不能构造破坏性卷句柄或删除真实数据。策略变化后正常存储使用应保持可用。驱动受影响不自动等于存储服务被攻破；关闭受影响配置只是有明确范围的适用性声明，仍需证据与复验。

**验收／留证：** 恢复满足声明的完整性、隔离、RTO／RPO；删除结果明确延迟／排除副本及其到期时间。保留血缘、访问判定、恢复检查和密钥依赖。访问超出模拟资源范围或恢复跨越租户边界时立即停止。

<a id="rb-07"></a>
## RB-07 — 不可信制品与解析器

**准备：** 使用模拟的不支持格式／无效输入、隔离加载器，不授予生产凭据。记录可接受格式、反序列化权限、制品摘要、来源、签名策略和运行边界。

**测试：** 拒绝未经批准的可执行序列化和制品来源。未批准签名者的有效签名不能直接视为安全。针对 NCS-SSC-02 与 NCS-DAT-03，将实际制品摘要绑定至获准签名者／构建者、规范源码仓库、构建类型和预期外部参数 [S16]；仅签名有效仍不足，未知或未授权输入必须明确判定而非静默接受。吊销测试制品并检查 Registry、部署、渲染器和缓存失效。措施须对应实际格式；扫描不能证明任意模型代码安全。保留加载器隔离，不引入强制 Agent 框架。

**验收／留证：** 在特权执行前拒绝，召回覆盖部署和缓存，可信重建可复现。保存加载决策、来源和召回证据。意外执行、持久化、凭据访问或越界出网即中止。本手册不需要真实恶意载荷。

<a id="rb-08"></a>
## RB-08 — Agent 授权范围

**准备：** 由外部授权委托方定义目标、租户、资源、工具、参数、目的地、预算、到期时间和策略版本。“不可变”指 Agent 不能自行扩大当前授权，不意味着合法用户永远不能批准下一阶段。

**测试：** 以无害注入文本请求越权、改变审批状态或把模型／工具输出当作授权；测试审批后参数变化、凭据过期、重复失败、超时和预算耗尽。新目标或更大范围需要新的授权包，绑定变化后的参数；旧审批不能重放到新动作。

针对 NCS-AIR-03，以数据库／资源身份的实际权限落实只读，而非仅依靠工具描述、SQL 禁止列表或默认事务设置 [S19]。使用一次性记录和身份，在后端验证正常读取及禁止的未授权副作用；检查继承角色和可执行函数，保留脱敏判定，并按 RB-01 验证凭据撤销。同样需要应用厂商修复；最小权限不能证明有漏洞的软件已被修复。

**验收／留证：** 即使模型提出越权动作，资源侧仍拒绝执行。保存审批绑定、动作结果、停止判定和独立后置条件检查。预算、时间、重试可以有确定性限制，但语义成功与不确定性不保证总能准确判定。模糊时保持未验证并升级，不允许自行认证完成。

<a id="rb-09"></a>
## RB-09 — GPU、服务缓存与重新分配

**准备：** 声明准确的整机／整卡独占、MIG／硬件分区、受仲裁 vGPU 或 Device Plugin 时间切片模式。后者不提供 Replica 间显存／故障隔离；vGPU 属性取决于具体产品、版本和配置 [S1、S2]。

**测试：** 在获批实验环境验证适用 SKU 的显存、故障、DMA、复位与重新分配声明。模型服务使用模拟标记测试路由、KV Cache、Session 和 Prefix Cache 的租户分区。错误后的设备复用不同于正常退出；普通磁盘清除指引不证明易失加速器状态清理。

**验收／留证：** 声明必须有厂商支持及部署路径证据。清理／复位无法判定时隔离设备；把设备独占分配给新租户并不能擦除旧数据。记录复位范围、故障域、残余共享资源和归因限制。出现跨租户标记或硬件错误立即中止。

<a id="rb-10"></a>
## RB-10 — 独立保证与来源变化

**准备：** 明确评估总体、抽样依据、准确来源 URL、发布／读取日期、状态及访问限制。区分来源要求与本项目建议。来源要求认证时，仅实施类似控制并不满足原要求。

**测试：** 逐行将 CSV 控制映射与 JSON 对账。在可丢弃样本中注入缺失控制、过期 PASS、重复来源、畸形 CSV 和 Schema 类型错误，确认校验失败。对详情与总览按条目和场景对账，而非只比较数量。

对于法律或合同通知义务，由责任 Owner 确认产品、供应商角色、司法辖区、合同、触发条件与生效日期后，再声明适用 [S20]。使用无害场景演练事件接收、证据保存、知悉时间记录、授权通知及恢复；区分各项报告时钟，以及未来期限和已生效义务。复查平台可用性和接收方指引；草案或路线图都不证明通报渠道已实际可用。

**验收／留证：** 缺失、未测试、过期、无法判定均显式保留。区分文档映射、有效元数据、已部署控制和独立验证结果。验证人姓名不同不自动证明独立性。记录准确提交和局限；本地 Schema 测试不会授予 ClusterMAX 评级。遵循普通[研究与变更流程](../../CONTRIBUTING.md#recurring-research)，不另建第二套评审目录。

## 一手来源与局限

- [S1 — NVIDIA GPU Operator sharing](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html)
- [S2 — NVIDIA mediated vGPU overview](https://docs.nvidia.com/ai-enterprise/release-8/latest/infra-software/vgpu/overview.html)
- [S3 — BlueField modes](https://networking-docs.nvidia.com/bsp/latest/modes-of-operation)
- [S4 — UFM 6.23.20 optional configurations](https://docs.nvidia.com/networking/display/ufmenterpriseumv62320/Optional-Configurations)
- [S5 — UFM 6.26.1 Security tab](https://networking-docs.nvidia.com/ufmenterpriseum/6.26.1/security-tab)
- [S6 — Prometheus security model](https://prometheus.io/docs/operating/security/)
- [S7 — Grafana security](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/)
- [S8 — Grafana roles and permissions](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/)
- [S9 — Elastic ECK ESA-2026-146](https://discuss.elastic.co/t/elastic-cloud-on-kubernetes-3-5-0-security-update-esa-2026-146/390106)
- [S10 — Kubernetes RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [S11 — Google Cluster Toolkit security bulletins](https://docs.cloud.google.com/cluster-toolkit/docs/security-bulletins)
- [S12 — Microsoft Server 2025 Azure Edition September 8 baseline](https://support.microsoft.com/en-us/servicing/os/hotpatch/windows-server-2025/2026/september-8-2026-baseline)
- [S13 — AWS OpenSearch Dashboards bulletin 2026-102](https://aws.amazon.com/security/security-bulletins/2026-102-aws/)
- [S14 — Nebius audit service/action coverage](https://docs.nebius.com/audit-logs/services)
- [S15 — AWS EFS CSI bulletin 2026-099](https://aws.amazon.com/security/security-bulletins/2026-099-aws/)
- [S16 — SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [S17 — Kubernetes v1.37 rootless beta](https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/)
- [S18 — Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [S19 — AWS postgres-mcp-server bulletin 2026-101](https://aws.amazon.com/security/security-bulletins/2026-101-aws/)
- [S20 — European Commission CRA reporting guidance](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting)

厂商行为依赖具体版本／产品类别。来源支持特定机制，不自动支持手册中的全部项目建议。[参考资料](../../REFERENCES.md)记录范围内日期与读取局限；[此前来源复核](../../reviews/2026-09-05-evidence-followup.md)保留尚未解决的外部框架差异。新公告触发适用性复核，不自动证明符合基线，也不强制迁移平台。
