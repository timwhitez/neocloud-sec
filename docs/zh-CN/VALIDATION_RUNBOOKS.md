# NeoCloud 验证手册

**复核日期：** 2026-09-09 · **画像版本：** 1.0.1 · **核心目录：** 1.0.0-draft.1

本手册是项目自行设计的测试方案，不是已经执行的基础设施测试、厂商认证或 SemiAnalysis 评分规则。这十类运营验证手册补充[公开问题画像](../../controls/semianalysis-public-findings-profile.v1.json)，不修改其 Schema，也不声称已建立机器校验的逐项关联。实施时使用包含版本绑定勘误的[目录编译器](../../scripts/compile_catalog.py)。

**技术扩展复核：** 2026-09-29，仅覆盖下文的推理入口、KV 传输／缓存生命周期、GPU 内存故障与机密计算组合边界；早期来源截止日期保持不变。这些是既有控制的工程深化，不是新增控制或已经执行的安全测试。发布日期、资料状态和适用性见[范围内来源索引](../../REFERENCES.md#inference-accelerator-sources)。

| 工程问题 | 既有手册中的位置 |
|---|---|
| 经过认证的请求会不会在 GPU Token 限额生效前耗尽 CPU？ | [推理入口与资源预算](#inference-resource-budgets) |
| 已取消的 Decode 能否持续占用或重新访问被复用的 KV 内存？ | [分离式 KV 生命周期](#disaggregated-kv-lifecycle) |
| Prefix 隔离是否同样覆盖媒体、Encoder 与 Offload 缓存？ | [逐层缓存隔离](#layer-specific-cache-isolation) |
| ECC 已启用或计数器没有异常时，仍有哪些风险？ | [内存扰动与恢复](#gpu-memory-disturbance) |
| 哪些 CPU、GPU 与 Fabric 状态真正约束密钥释放？ | [机密计算组合边界](#confidential-composition) |

## 授权与证据要求

测试前记录服务、区域、集群、SKU、租户标识、实际运行版本、获批目标与动作、窗口、操作人、独立复核人、恢复负责人和中止条件。使用两个带有不同无害标记的模拟租户，仅测试明确授权的资源。不得将真实客户数据、管理密钥、原始显存或保密厂商公告写入本仓库。

每个测试同时包含允许路径与禁止路径。由于无关系统故障造成的访问失败，不能作为授权控制通过的证据。记录判定、目标侧实际影响、请求标识、生效策略和时间。租户黑盒、服务商白盒、独立故障／恢复三个视角分别记录；不适用需要范围理由和批准记录，不能把未执行视角填成 PASS。任何适用 T0 缺少当前充分证据时，仍为 NO_GO_NONCONFORMANT。元数据可选用[证据与公告记录校验](../EVIDENCE_VALIDATION.md)，但不能当作上述结果成立的证明。

<a id="rb-01"></a>
## RB-01 — API、调度、vCluster 与节点边界

**准备：** 为模拟租户 A/B 创建资源、工作负载身份与获批凭据，导出生效 RBAC、准入规则、同步器／Operator 权限、CNI 与节点 API 配置。

**测试：** A 能访问自己的资源，但不能读取、挂载、修改或冒充 B 的资源。覆盖 kubelet、宿主集群对象和服务账户令牌。vCluster 必须检查同步组件的宿主集群权限以及共享节点组件；虚拟控制面本身不证明节点隔离。使用安全的中断分配和凭据过期场景，不提交破坏性工作负载。撤销此前允许的跨 Namespace 关联或 Operator 授权后，使用一次性身份和无害记录，检查 Operator 收敛时是否清理或轮换其生成的后端凭据 [S9]，并核对旧的一次性凭据在后端（如数据库）被拒绝，同时另一独立授权身份仍可成功。Kubernetes API 拒绝本身不证明现存后端凭据已失效；轮换出的密钥材料仍须满足密钥生命周期要求。针对 NCS-IAM-04、NCS-KMS-02 和 NCS-ORC-04，还要检查服务账户实际权限和所有已启用授权路径；控制器选择器、本地缓存不能替代资源侧授权 [S10]。

**验收／留证：** 租户上下文贯穿控制器转换，禁止请求在目标侧无实际影响，部分分配被回滚或隔离。保存脱敏配置、两类请求轨迹和实际状态对账。凭据脱敏，仅保留判定与请求标识。出现异租户数据、意外特权或撤权后任何异常访问立即中止；先完成隔离、轮换和独立复验，再重新开放该路径。

<a id="rb-02"></a>
## RB-02 — 运行时漏洞与安全发布

**准备：** 按资产盘点已安装及实际运行的 Toolkit、Runtime、Driver、Firmware、Kernel 和编排版本，识别准确的托管服务、OS 镜像/构建、控制器及运行进程，而不只看包名或镜像族。将公告关联到受影响配置、厂商修复／回移补丁、兼容性与客户影响，并区分四个传播阶段：上游修复、发行版回补、云镜像发布和实际节点替换。版本号更大不等于安全。

**测试：** 在隔离金丝雀环境更新，按需重启组件并验证实际加载版本；同时记录合法作业成功和经审查的禁止边界结果。模拟更新失败和节点清单过期。建立公告接收与升级路径；Embargo／预发布资格依赖厂商安排，不是所有服务商天然具备的能力。此类元数据可选用离线公告处置台账记录，与[证据校验工具](../EVIDENCE_VALIDATION.md)一同说明。

针对 NCS-ASM-01、NCS-ORC-04 和 NCS-CMP-03，记录镜像／构建标识、替换或启动证据，再验证作业完成、策略执行和恢复。修改镜像族指针不会更新已有节点 [S11]。启用热补丁不取消具体公告的重启要求，应看本次更新而非仅按长期日历推断 [S12]。只有服务商能够提供的证据仍由服务商负责。

功能门开启、配置用户命名空间与节点真实无根运行是不同状态。可选迁移前检查 CNI／CSI／设备／GPU 组合的支持与恢复；不强制采用 Beta 功能，也不将其视为所有内核漏洞的防护 [S17]。

**验收／留证：** 有漏洞或状态未知的节点不能静默回到健康资源池；未验证容量保持隔离。云镜像发布本身不证明任何具体节点已重建或修复，服务商独占的证据仍由服务商负责。回滚若恢复已知可利用版本，必须隔离并明确保持不符合基线状态。保留公告标识、可用时的签名来源证据、金丝雀结果、部署复验和复测结果。违反服务目标或丢失恢复通道立即停止。

<a id="inference-resource-budgets"></a>
### 推理入口与资源预算

**范围：** NCS-API-01、NCS-API-02、NCS-API-03、NCS-API-05、NCS-ORC-03 和 NCS-VEM-02。按真实服务版本、监听器与已启用插件实施。vLLM 上游公告 [S22] 展示了 CPU 调度侧资源耗尽；GPU Token 配额不是完整的请求成本边界。公告修复范围不等于永久安全版本底线。HTTP API Key 覆盖不能证明另外启用的 gRPC、内部 Worker 或插件路由已受保护 [S21]。

**设计：** 导出运行中的监听器／路由清单：地址、端口、协议、Path/Method、插件来源、认证、授权与资源成本。除公开推理外，覆盖管理、Health/Metrics、模型／Adapter 操作与内部入口。可信入口默认拒绝，并阻止绕过网关直达 Worker。解析前限制整体字节数；进入昂贵 Engine 工作前限制字段、媒体解码、序列化／哈希、序列数量、上下文／输出、并发、队列长度／等待时间与重试。由授权边界注入固定长度秘密 Cache Salt，不接受调用者无限长度值。已认证租户同样受限；取消和超时释放预留，重试不能放大已耗尽预算。

**测试／证据：** 使用小型 `limit-1`、`limit`、`limit+1` 夹具，不发送公告中的超大请求或并发耗尽载荷。逐个已启用监听器／路由配对验证合法请求、错误身份／租户及网关绕过。确认拒绝发生在昂贵 Engine 处理之前，取消后 CPU／GPU／队列预留归还。记录实际构建、生效限额、判定／Engine 轨迹、受限资源消耗，以及正常业务的 p95/p99 首 Token 时延（TTFT）。遗漏的监听器保持未验证；达到获批资源／SLO 阈值即停止。入口过滤补充但不替代厂商修复；路由、插件、Engine 或网关变化后重新验证。

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

<a id="disaggregated-kv-lifecycle"></a>
### 分离式 KV 传输、租约与复用

**范围：** NCS-NET-02、NCS-NET-03、NCS-DAT-02、NCS-DAT-04、NCS-CMP-02、NCS-ORC-03 和 NCS-IAM-04。分别检查请求／路由授权、KV 元数据／通知／租约流量，以及 GPU／CPU／RDMA／TCP／Offload 大块数据传输。公开 API TLS 或 Service Mesh 不证明直通内存路径受到保护。检查实际 Backend 与 Fallback，不把某种 vLLM 部署的内部可信网络假设 [S21] 推广为所有 NIXL Backend 的属性。

**设计：** 在可信状态中绑定授权共享域、请求、模型／Adapter 版本、来源／目的 Peer、分配 Generation、Buffer 边界、到期时间和保留预算。Engine ID、地址、rkey 或调用者自报的传输参数不是业务授权。复用受支持的 Peer／网络／Backend 执行机制，不另造传输协议。上游 NIXL Connector 租约设计 [S23] 通过 Heartbeat 为 Decode 保持 Prefill 数据块存活；存活不意味着可以无限续期授权。

```text
分配／注册 → 授权 → 传输／固定内存
→ 完成／取消／到期 → 停止续期 → 排空／隔离在途访问
→ 撤销／注销或隔离 → 必需清理 → 新 Generation 复用
```

超时或完成通知本身不能证明在途 DMA 已停止；迟到 Heartbeat／Completion 不能复活终态分配。无法证明受支持的 Fencing、撤销或清理时，隔离相关分配／Worker／设备，不能乐观复用旧地址。

| 授权实验场景 | 必需的配对观察 |
|---|---|
| 合法 Prefill/Decode | 请求／模型数据正确，保留受限 |
| 错误共享域、Peer 或 Generation | 元数据与实际大块数据访问边界均拒绝 |
| Decode 崩溃、网络分区或长队列 | 保留受限，区分正常排队与失联 |
| 取消／到期后收到迟到 Heartbeat／Completion | 不恢复授权，不复用旧分配 |
| Worker 重启、地址复用或 RDMA→TCP Fallback | 重新核查身份／Generation，不降低声明的保护 |

**证据／中止：** 仅用无害标记。关联分配／请求血缘、实际 Backend、Peer 判定、终态事件、排空／Fencing、清理和重新分配，测量保留字节数、回收延迟与正常业务时延。日志不记录真实 rkey、KV 内容、Token ID 或 Salt。撤销未验证不能填 PASS；出现跨域访问或 Fabric 不稳定即停止并先隔离。按受支持流程恢复及独立复测。本节不宣称发现 NIXL 漏洞，也不要求在生产运行 RDMA 利用。

<a id="rb-05"></a>
## RB-05 — Prometheus、Grafana 与遥测

**准备：** 为 A/B 注入不同无害时序数据，记录 Grafana 版本／版本类别、组织、数据源凭据以及直连后端、代理和 Remote Read 路径。Prometheus 默认安全模型允许 HTTP 用户访问其时序数据；标签不是授权 [S6]。Grafana Viewer 可能查询数据源，而不只读取可见看板 [S7、S8]。

**测试：** 绕过看板导航直接查询，尝试异租户查询和伪造租户选择器。确认上下文由可信代理／后端绑定，而不是由调用者自报。验证告警路由、保留和支持访问。使用数据源权限前核实具体产品版本是否支持该功能。用租户安全的关联 ID 串联策略变更、Operator 收敛、凭据生命周期、后端拒绝和存储决策，并在必需审计来源缺失时告警；Dashboard、指标标签或采集程序退出成功都不等于租户授权。

威胁模型还应覆盖共享看板创建／导入和可视化渲染，而非只有查询；分离写入与查看权限，检查实际部署的看板组件及托管服务补丁状态 [S13]。只用厂商支持的无害样本和授权检查，不复现浏览器执行载荷。自建版本已修复不证明托管服务完成了自己的修复。

逐个云审计来源记录支持的服务／动作、启用状态、投递和保留，验证预期无害事件实际送达且缺失来源能够被发现。提供审计功能或采集器成功退出不等于覆盖有效 [S14]；不得将真实租户记录导出到本仓库。

**验收／留证：** 隔离落实到后端凭据／查询边界，直连或编辑标签不能绕过；必要时采用分离组织和权限受限的后端。保留查询结果和后端授权。GPU Operator 时间切片下，须记录 DCGM-Exporter 的容器归因限制 [S1]，不能从不存在的指标推导容器责任。出现异租户时序或密钥暴露立即中止。

<a id="rb-06"></a>
## RB-06 — 存储、快照、删除与恢复

**准备：** 创建 A/B 模拟对象、卷和快照，记录 CSI／控制器身份、KMS 归属、不可变备份保留期和合同删除范围。针对 NCS-API-01、NCS-DAT-04 和 NCS-ORC-02，联合审查 PV 创建权限、实际启用的删除选项、CSI 身份、Filesystem/Access Point 所有权和云资源策略 [S15]，控制器优先采用厂商修复版本和最小权限。

**测试：** 在实际存储边界拒绝异租户挂载、导出和恢复。用惰性单元夹具或厂商支持的非破坏性检查验证对象/租户归属；不构造破坏性 Volume Handle，不删除真实数据。确认策略变更后合法存储使用仍成功。在主依赖不可用时恢复测试备份。检查副本、缓存、快照、本地介质和受保留期限制的延后删除。删除请求不能被描述为所有不可变备份立即完成物理擦除。驱动缺陷不自动等于存储服务被攻破；停用受影响配置是需要证据和重验证的适用性判断。

**验收／留证：** 恢复满足声明的完整性、隔离、RTO／RPO；删除结果明确延迟／排除副本及其到期时间。保留血缘、访问判定、恢复检查和密钥依赖。访问超出模拟资源范围或恢复跨越租户边界时立即停止。

<a id="rb-07"></a>
## RB-07 — 不可信制品与解析器

**准备：** 使用模拟的不支持格式／无效输入、隔离加载器，不授予生产凭据。记录可接受格式、反序列化权限、制品摘要、来源、签名策略和运行边界。针对 NCS-SSC-02 与 NCS-DAT-03，制品准入须将摘要绑定到批准的签名者/构建者身份、规范源码仓库、构建类型和预期构建输入；仅签名有效并不足够 [S16]。

**测试：** 拒绝未经批准的可执行序列化和制品来源。未批准签名者的有效签名不能直接视为安全。吊销测试制品并检查 Registry、部署、渲染器和缓存失效。未知或未授权输入必须明确判定而非静默接受。措施须对应实际格式；扫描不能证明任意模型代码安全。保留加载器隔离，不引入强制 Agent 框架。

**验收／留证：** 在特权执行前拒绝，召回覆盖部署和缓存，可信重建可复现。保存加载决策、来源和召回证据。意外执行、持久化、凭据访问或越界出网即中止。本手册不需要真实恶意载荷。

<a id="rb-08"></a>
## RB-08 — Agent 授权范围

**准备：** 由外部授权委托方定义目标、租户、资源、工具、参数、目的地、预算、到期时间和策略版本。“不可变”指 Agent 不能自行扩大当前授权，不意味着合法用户永远不能批准下一阶段。

**测试：** 以无害注入文本请求越权、改变审批状态或把模型／工具输出当作授权；测试审批后参数变化、凭据过期、重复失败、超时和预算耗尽。新目标或更大范围需要新的授权包，绑定变化后的参数；旧审批不能重放到新动作。对访问数据的 Agent，在数据库/资源身份处落实只读和最小权限，不能只依赖工具描述、提示词或 SQL 过滤；工具声明不是授权。执行未授权合成请求和无害的不支持格式，验证合法路径仍可用、被拒绝操作无副作用，并记录回滚/召回及所用身份。

针对 NCS-AIR-03，检查数据库／资源身份背后的继承角色和可执行函数 [S19]。使用一次性记录和身份，在后端验证正常读取及禁止的未授权副作用，按 RB-01 验证凭据撤销，并同样应用厂商修复；最小权限不能证明有漏洞的软件已被修复。

**验收／留证：** 即使模型提出越权动作，资源侧仍拒绝执行。保存审批绑定、动作结果、停止判定和独立后置条件检查。预算、时间、重试可以有确定性限制，但语义成功与不确定性不保证总能准确判定。模糊时保持未验证并升级，不允许自行认证完成。

<a id="rb-09"></a>
## RB-09 — GPU、服务缓存与重新分配

**准备：** 声明准确的整机／整卡独占、MIG／硬件分区、受仲裁 vGPU 或 Device Plugin 时间切片模式。后者不提供 Replica 间显存／故障隔离；vGPU 属性取决于具体产品、版本和配置 [S1、S2]。

**测试：** 在获批实验环境验证适用 SKU 的显存、故障、DMA、复位与重新分配声明。模型服务使用模拟标记测试路由、KV Cache、Session 和 Prefix Cache 的租户分区。错误后的设备复用不同于正常退出；普通磁盘清除指引不证明易失加速器状态清理。

**验收／留证：** 声明必须有厂商支持及部署路径证据。清理／复位无法判定时隔离设备；把设备独占分配给新租户并不能擦除旧数据。记录复位范围、故障域、残余共享资源和归因限制。出现跨租户标记或硬件错误立即中止。

<a id="layer-specific-cache-isolation"></a>
### 逐层缓存隔离

**范围：** NCS-DAT-02、NCS-DAT-04、NCS-DAT-05、NCS-CMP-02、NCS-CMP-05、NCS-API-01 和 NCS-TEL-01。vLLM 文档所述机制 [S21] 中，可选 `cache_salt` 分隔 Prefix Cache 复用，客户端多模态 UUID 则可能影响 Processor／Encoder 缓存；Prefix Salting 本身不证明媒体缓存隔离。

| 层次 | 本项目的实施决策 | 无害负向测试 |
|---|---|---|
| Prefix KV | 可信入口为授权共享域注入固定长度、不可预测的秘密 Salt；拒绝／覆盖客户端 Salt 并阻断直达 Worker | A 的授权重复请求可复用；B 不能选择 A 的共享域 |
| 媒体 Processor／Encoder | 移除不可信 UUID 覆盖值并使用内容哈希；必须使用 UUID 时，由可信映射检查授权对象与内容一致性 | A/B 使用相同 UUID 和不同模拟媒体，逐层核验 |
| CPU RAM／NVMe／远端 Offload | 绑定 Namespace、对象 ACL、Peer 与分配 Epoch；无法分区则关闭该层或拆分 Worker | 旧域、错 Epoch 和恢复／重启请求不能取回他域缓存 |
| 索引／事件／遥测 | 认证发布者／读取者并最小化字段，标签不授予权限 | 未授权读取者不能得到缓存对象、媒体、Token ID 或秘密 Salt |

公开 Tenant ID 不是秘密 Salt。授权共享域可以细于租户；组织内用户间共享也要明确授权，不能默认成立。内容哈希解决 UUID 替换问题，不是所有时序侧信道的通用防护。Salt 轮换阻断旧 Namespace 复用，但不擦除旧数据；副本、快照和保留副本还须按 RB-06 处理。模型／Adapter 变更、撤权、取消、崩溃与租户退出均检查生命周期。

**证据：** 正确输出之外还需可信 Cache Hit／Block 归属观察，单次 TTFT 不证明隔离。按声明共享策略配对测量隐私边界、Hit Rate、吞吐和 p50/p95/p99 TTFT。记录清理、残余副本／保留期限与独立观察者。出现异租户标记即停止、隔离相关层并独立复测。不能将不同 Salt 宣称为整栈 ACL，也不必为此次保证工作另造缓存服务。

<a id="gpu-memory-disturbance"></a>
### GPU 内存扰动、ECC 与可信恢复

**范围：** NCS-CMP-01、NCS-CMP-02、NCS-CMP-03、NCS-CMP-05、NCS-ASM-01、NCS-VEM-03、NCS-TEL-01 和 NCS-TEL-03。GPUThor [S24] 与 NVIDIA 更新指南 [S25] 支持纵深防御，而不是关闭 ECC。论文四卡 GDDR6 位翻转实验使用 ECC-disabled；ECC-enabled 实验使用本地 RTX A6000。不能直接推广为 H100／HBM3／Blackwell 受影响，也不能把其他被测内存未观察到翻转写成免疫。

**设计：** 盘点准确 GPU／DRAM、固件／驱动、Host／Hypervisor、SYS-ECC 当前与待生效模式、适用 On-Die ECC、实际 DMA／IOMMU 边界以及共享、故障和复位域。Boot Flag、默认配置或 IOMMU Group 清单本身不是完整部署隔离证明。保留受支持的 ECC、DMA 隔离、租户放置与宿主控制，检查 GPUDirect／P2P 和机密模式兼容性，不直接套用通用启动参数。宿主 DMA 隔离不证明 GPU 内部数据完整性或 NVLink 隔离。

**测试／证据：** 使用合成遥测演练 Corrected／Uncorrectable Error、Row Remap、Reset 和来源缺失，贯穿告警、停止放置、隔离与审批开放。在维护实验环境关联受支持的只读设备状态、正常作业及恢复结果。合成事件只验证响应逻辑，不证明抗物理扰动。异常计数可能来自硬件故障，没有计数异常也不能排除静默损坏；不新增 Hammer Kernel、提权载荷或主动损坏硬件的测试。

**恢复：** 停止向不确定故障域放置新任务，保存脱敏证据，按厂商支持流程复位／重建／更换。异常窗口产生的模型／Checkpoint 在完整性与可信恢复来源评估前保持隔离；成功续跑不等于安全。独立核验身份、设备状态、DMA／租户边界和数据完整性后才能开放。硬件／DRAM、固件／驱动、共享方式变更或异常复位会使相关证据失效。

<a id="confidential-composition"></a>
### CPU–GPU–Fabric 机密计算组合边界

**范围：** NCS-CMP-04、NCS-CMP-05、NCS-IAM-03 和 NCS-KMS-04，适用于选定画像或合同要求证明／机密运行的服务。不把 T3 强制推广至所有服务，也不放宽任何 T0。NVIDIA 部署与运营指南 [S26、S27] 具有平台／版本约束；预印本 [S28] 指出其测试的 Fabric Manager／NVSwitch 栈的证明覆盖限制，不是通用漏洞或未来版本仍有相同边界的证明。

**设计：** 声明 CPU TEE／固件、CVM、准确 GPU 集合／分区、VBIOS／驱动、CC／PPCIe 模式、互连拓扑、Fabric Manager 位置、Verifier／参考值版本及客户密钥 Owner。区分经密码学测量／验证的状态、服务商声明、独立路径测试与仍需信任的管理组件。CPU 和 GPU 报告各自通过，不自动绑定到同一工作负载、Peer 或密钥接收者。复用受支持 Verifier、KMS 和策略系统，不自研证明密码协议。

密钥释放策略须通过受支持协议，将新鲜且真实性已验证的证据绑定到租户／工作负载、获批 GPU 集合与模式、制品策略、密钥用途及真实可信接收者。明确并测试 Challenge、Recipient／Channel Binding、参考值和撤销语义，不能声明部署实际上没有的绑定。缺少 GPU、证据过期／重放、参考值未知／撤销、接收者错误、未批准 Devtools／非保护模式或 Verifier 故障，都不能静默释放密钥或回退到明文 Worker。禁止未来释放不等于擦除已释放密钥，后者须独立隔离、到期／轮换和清理。

**测试／证据：** 配对合法运行与 Replay、错误租户／接收者、缺 GPU、模式降级、依赖丢失的合成 Verifier 夹具。夹具仅测试策略逻辑；真实 CPU／GPU 证据及资源侧密钥释放／拒绝须在受支持部署上由独立观察者核验。Reset、换卡、拓扑／模式／驱动／固件、参考值／策略变化后更新相关证据与会话。未覆盖的宿主 Fabric Manager／NVSwitch 路由信任假设必须披露，不能藏在 GPU Token 后面。

**安全／性能验收：** 保持必需保护开启，测量完整 Prefill／Decode、Collective、CPU↔GPU 拷贝、KV Offload／Restore 和 Checkpoint 路径；远端传输按 RB-04 验证。比较须匹配硬件、模型、精度、上下文、并发与拓扑，报告吞吐、p50/p95/p99 TTFT、每输出 Token 时延和恢复开销。GPU 内部矩阵基准不证明端到端机密推理性能 [S28]；不规定通用损耗比例或实验调参开关。记录准确范围与脱敏策略判定，不在本仓库存客户密钥或租户原始证据；缺硬件／验证条件时保持 NOT_TESTED 或 INCONCLUSIVE。

<a id="rb-10"></a>
## RB-10 — 独立保证与来源变化

**准备：** 明确评估总体、抽样依据、准确来源 URL、发布／读取日期、状态及访问限制。区分来源要求与本项目建议。来源要求认证时，仅实施类似控制并不满足原要求。

**测试：** 逐行将 CSV 控制映射与 JSON 对账。在可丢弃样本中注入缺失控制、过期 PASS、重复来源、畸形 CSV 和 Schema 类型错误，确认校验失败。对详情与总览按条目和场景对账，而非只比较数量。

对于法律或合同通知义务，由责任 Owner 确认产品、供应商角色、司法辖区、合同、触发条件与生效日期后，再声明适用 [S20]。使用无害场景演练事件接收、证据保存、知悉时间记录、授权通知及恢复；区分各项报告时钟，以及未来期限和已生效义务。复查平台可用性和接收方指引；草案或路线图都不证明通报渠道已实际可用。

**验收／留证：** 缺失、未测试、过期、无法判定均显式保留。区分文档映射、有效元数据、已部署控制和独立验证结果。验证人姓名不同不自动证明独立性。记录准确提交和局限；本地 Schema 测试不会授予 ClusterMAX 评级。遵循常规[研究与变更流程](../../CONTRIBUTING.md#recurring-research)，不建立第二套评审目录。

## 一手来源与局限

- [S1 — NVIDIA GPU Operator 共享](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html)
- [S2 — NVIDIA vGPU](https://docs.nvidia.com/ai-enterprise/release-8/latest/infra-software/vgpu/overview.html)
- [S3 — BlueField 运行模式](https://networking-docs.nvidia.com/bsp/latest/modes-of-operation)
- [S4 — UFM 6.23.20 配置](https://docs.nvidia.com/networking/display/ufmenterpriseumv62320/Optional-Configurations)
- [S5 — UFM 6.26.1 Security 页](https://networking-docs.nvidia.com/ufmenterpriseum/6.26.1/security-tab)
- [S6 — Prometheus 安全模型](https://prometheus.io/docs/operating/security/)
- [S7 — Grafana 安全配置](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/)
- [S8 — Grafana 角色与权限](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/)
- [S9 — Elastic ECK ESA-2026-146](https://discuss.elastic.co/t/elastic-cloud-on-kubernetes-3-5-0-security-update-esa-2026-146/390106)
- [S10 — Kubernetes RBAC 良好实践](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [S11 — Google Cluster Toolkit 安全公告](https://docs.cloud.google.com/cluster-toolkit/docs/security-bulletins)
- [S12 — Microsoft Server 2025 Azure Edition 9 月 8 日基线](https://support.microsoft.com/en-us/servicing/os/hotpatch/windows-server-2025/2026/september-8-2026-baseline)
- [S13 — AWS OpenSearch Dashboards 公告 2026-102](https://aws.amazon.com/security/security-bulletins/2026-102-aws/)
- [S14 — Nebius 审计服务/动作覆盖](https://docs.nebius.com/audit-logs/services)
- [S15 — AWS EFS CSI 公告 2026-099](https://aws.amazon.com/security/security-bulletins/2026-099-aws/)
- [S16 — SLSA v1.2 制品验证](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [S17 — Kubernetes v1.37 rootless beta](https://kubernetes.io/blog/2026/09/04/kubernetes-v1-37-rootless-beta/)
- [S18 — Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [S19 — AWS postgres-mcp-server 公告 2026-101](https://aws.amazon.com/security/security-bulletins/2026-101-aws/)
- [S20 — 欧委会 CRA 报告指南](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting)

- [S21 — vLLM security / 安全指南](https://docs.vllm.ai/en/stable/usage/security/)
- [S22 — vLLM GHSA-wpww-v874-ph2p](https://github.com/vllm-project/vllm/security/advisories/GHSA-wpww-v874-ph2p)
- [S23 — vLLM NIXL KV cache lease design](https://docs.vllm.ai/en/latest/design/nixl_kv_cache_lease/)
- [S24 — GPUThor author paper / 作者论文](https://gururaj-s.github.io/assets/pdf/CCS26_GPUThor.pdf)
- [S25 — NVIDIA Rowhammer notice 5873](https://nvidia.custhelp.com/app/answers/detail/a_id/5873)
- [S26 — NVIDIA CC deployment guide](https://docs.nvidia.com/cc-deployment-guide-tdx-snp.pdf)
- [S27 — NVIDIA Secure AI operations guide](https://docs.nvidia.com/nvidia-secure-ai-operations-guide.pdf)
- [S28 — The Serialized Bridge, arXiv:2606.23969v2](https://arxiv.org/html/2606.23969v2)

S21–S28 于 2026-09-29 读取；[范围内来源索引](../../REFERENCES.md#inference-accelerator-sources)区分持续更新／开发文档、公告日期、厂商指南版本与研究状态。早期条目保持原有复核范围。

厂商行为具有版本差异，来源支持具体机制，不代表背书整套测试方案。读取限制和外部框架差异见[本轮来源复核](../../reviews/2026-09-05-evidence-followup.md)。
