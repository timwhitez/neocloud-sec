# SemiAnalysis / ClusterMAX 覆盖审计与验证指南

**画像版本：** 1.0.1  
**核验日期：** 2026-09-05  
**基础目录：** 1.0.0-draft.1

## 1. 数量究竟说明什么

画像包含 **40/40 项项目自行编写的映射**，以及**有日期的公开 Security 页面快照的 20/20 项映射**。这些是仓库中的记录，不是已经执行的基础设施测试、ClusterMAX 分数、背书，也不意味着访问了 SemiAnalysis 的全部方法与资料。

40 项逐项记录中的历史覆盖分类实际为 **21 项明确覆盖、12 项部分覆盖、7 项缺口**。旧摘要的 17/17/6 与记录矛盾。1.0.1 修正统计，而不是修改逐项分类去凑一个预期数字。历史分类属于本项目判断，不是独立测量的行业统计。“文章五类问题”和本项目的五个分组也不能直接视为作者分类体系的逐项复刻。

以前备用站点显示 21 项的记录仅作为尚未解决的历史观察保留，**不声明 21/21 覆盖**，也不将它描述为本轮再次核实的总数。动态页面可能变化，比较时必须固定日期和准确 URL；不得为了配平数量而编造额外要求。

## 2. 来源与解释边界

文章准确入口为 [Most Neoclouds Suck At Security](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security)。本轮使用公开索引中的摘录，没有取得完整付费文章。Security 要求核对的是[正式 criteria 页面](https://www.clustermax.ai/criteria/security)，不是之前记录的 `/security` 路径。[公开站点](https://www.clustermax.ai/)在本次核验时把 2.1 标为当前已发布评级，3.0 仍标为即将推出。

每项问题现在都有来源 ID。引用表示本项目解释的技术依据，并不表示来源包含完全相同的措辞，或来源已证明某服务商部署安全。价格、商业合作、专有评分和未公开条目仍不在范围内。若外部条目明确要求 ISO/IEC 27001 认证，内部“等效 ISMS”不能被当成该认证的替代证据；应核对真实证书、服务范围、有效期和排除项。

## 3. 三类视角不是三个自动通过

保留**租户黑盒、服务商白盒、独立故障/恢复**三类视角。第一类验证客户可见路径，第二类检查配置、责任与运营流程，第三类挑战故障和恢复行为。某个视角无法执行时不能标为 PASS。确实不适用时，应另外记录带理由和复核人的适用性决定，不能伪造成功测试。

仓库 CSV 是空白模板：状态为 `PROPOSED`、适用性为 `UNKNOWN`、结果为 `NOT_TESTED`。先复制到私有评估系统，再采集真实证据。仓库校验会拒绝带“已通过/已验证”结果的模板行；它不是生产准入判定引擎。

## 4. 开始技术验证前的规则

取得书面授权，使用两个合成租户及非敏感标记数据。记录准确服务、环境、集群、地域、SKU、硬件、固件、运行时、驱动和策略版本。先确定带外恢复路径和停止条件，再开始测试。优先只读检查；Fabric、DPU、共享节点变更只能在批准的维护窗口或隔离实验环境中进行。不得为完成本指南而向生产系统提交利用载荷、轮换线上 Fabric 密钥、重启设备或探测第三方租户。

证据应包含断言、测试 ID、采集者、独立复核者、时间、有效期、部署范围、完整性方法、结果和局限。真实凭据和密钥值不得进入报告。Hash 只能标识字节，不能证明采集者可信或测试真实。证据缺失应为 `NOT_TESTED` 或 `INCONCLUSIVE`，不是成功。适用 T0 失败时仍是 `NO_GO_NONCONFORMANT`，风险接受不能改变结果。

## 5. 优先验证场景

### A. InfiniBand 数据与管理路径——SA-NC-015..022

NVIDIA 分别定义了多种管理密钥，包括 **C_Key、CC_Key、PM_Key 和 N2N_Key**，不能合并成别名。其文档还指出，P_Key 分区检查不适用于 SMP MAD，管理器无响应时的 M_Key 租期和恢复行为也会影响保护状态。依据见 [NVIDIA 安全指南](https://networking-docs.nvidia.com/nvidiainfinibandsecurityoverviewandguidelines/security-in-infiniband)。

检查脱敏的密钥类别清单、管理器权限、受保护配置、成员类型、拓扑与端点执行。在授权测试 Fabric 中，分别验证允许流量、禁止的跨租户流量、管理器切换、陈旧分配和受控重分配。管理消息限制必须与数据分区分开验证，同时覆盖适用的 SR-IOV VF 和 SHARP 路径。

**通过：** 所有必测禁止路径均被拒绝，合法流量仍可用，切换期间策略被保留或进入安全限制状态。**停止：** 共享 Fabric 出现非预期不稳定或影响非测试租户。**恢复：** 使用既定恢复路径还原已批准的管理器状态与密钥，隔离不确定分配，独立复测后开服。Ping 测试不能证明 RDMA 或管理面隔离。

### B. BlueField RShim 与主机信任——SA-NC-012..014

[BlueField 模式文档](https://networking-docs.nvidia.com/bsp/480/modes-of-operation)区分信任主机与限制主机权限的运行边界。必须记录具体产品和模式，不能认为“部署了 DPU”就自然完成隔离。

梳理 Host、ARM 侧、RShim/tmfifo、OOB 的访问路径、管理身份、固件权限和重分配状态。只在合成租户范围内进行获批的负向检查。切换模式前，先核对该版本的变更生效与恢复要求，禁止直接关闭唯一管理路径。

**通过：** 租户权限无法管理 DPU，也不能修改受保护的 Fabric 策略，合法恢复仍可行。**停止：** 管理访问变得不确定。**恢复：** 按批准的厂商特定流程恢复，再检查身份、固件、策略和重分配清理。缺少安全恢复测试时应判为无法确定，不能当成隔离证明。

### C. vCluster、Kubelet 与共享节点——SA-NC-005..010

[Kubernetes 多租户指南](https://kubernetes.io/docs/concepts/security/multi-tenancy/)把虚拟控制面与数据面隔离区分开来；NetworkPolicy 还需要网络插件真正执行。

检查 Host Cluster 与 Syncer 权限、节点 API、准入豁免、服务账户、CNI/CSI 行为及卷/快照授权。用两个测试租户分别验证 Namespace/API 拒绝、直接受支持网络路径、存储访问和特权工作负载拒绝。客户使用的托管 API 可以有受保护的公网入口，但这不意味着可以暴露服务商专用数据库或节点管理接口。

**通过：** 每项声明在真实执行点得到验证。**停止：** 测试可以访问服务商专用管理能力或其他租户卷。**恢复：** 撤销测试身份、隔离受影响分配，复核同步和准入状态后重测。Namespace、vCluster 或 Slurm 标签都不能单独证明 Host/GPU/Storage/Fabric 完整隔离。

### D. Grafana 与 Prometheus 后端——SA-NC-035

[Grafana 数据源文档](https://grafana.com/docs/grafana/latest/datasources/)说明了组织内默认查询权限及分版本提供的数据源权限能力；[Prometheus 安全模型](https://prometheus.io/docs/operating/security/)也需要独立考虑。Dashboard 或 Folder 权限不足以证明后端授权正确。

为租户 A、B 放入不同的合成指标，用各自身份测试受支持的直接查询、Label/Series 和 Dashboard 路径。检查租户上下文是否由可信网关强制执行、是否能绕过网关直达后端。对启用的共享服务凭据、告警路由、Remote Read/Write 和支持访问分别检查。记录 Grafana 实际版本及功能，不要把 Enterprise 专有控制写成所有版本都有。

**通过：** 任一租户都不能经范围内的已启用路径读取另一方标记数据。**停止：** 真实数据可见，仅保留必要脱敏证据。**恢复：** 撤销过宽凭据、限制后端访问、修正服务端授权，并复测全部路径，而不只是 Dashboard。

### E. GPU 共享与遥测归因——NCS-CMP-02

[NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html)指出其 Time-slicing Replica 不提供显存/故障隔离，还说明了该模式下 DCGM Exporter 的归因局限。不能根据节点指标宣称已经具备逐容器安全可见性。Hypervisor 仲裁的 vGPU 是不同的产品特定机制，参见 [vGPU 说明](https://docs.nvidia.com/ai-enterprise/release-8/latest/infra-software/vgpu/overview.html)。

对照所售 SKU 与实际分配模式、设备和软件版本。在代表性实验设备上执行授权、无害的显存、故障、重置和重分配验证；不能执行的项目必须明确记录。即使遥测归因有限，也要保留逐分配身份信息。

**通过：** 每项对外隔离和清理承诺都有对应机制及测试证据。**停止：** 重置可能影响未批准的工作负载。**恢复：** 隔离不确定设备或分配，使用受支持的已知可信供应流程。解释原始 Catalog 前必须应用规范勘误。

### F. Agent 范围、模型输出与撤销——SA-NC-031..034

这是本项目设计的验证场景，不是外部认证要求。将 Goal、Tenant、Tool、Data、Egress 和 Cost 范围视为版本化授权约束。Agent 不能自行扩大范围；具备独立授权资格的委托方可以批准新的范围，并保留新的授权和审计记录。

使用无害注入指令和标记数据，验证外部内容不能修改工具授权、审批权限或完成证据。测试凭据撤销、预算耗尽、重复失败和验证者不可用。Cache/Session 隔离必须与 Prompt 过滤分开测试。

**通过：** 禁止动作由模型之外的执行点阻断，高影响完成声明有独立证据。**停止：** 动作即将超出测试范围。**恢复：** 撤销授权、停止排队动作、还原批准状态并独立验证。模型说“完成”不是完成证据。

## 6. 本地校验与有效目录

显式安装校验依赖后，在本地运行：

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/check_local.py
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

前两项旧校验仍是标准库脚本。新的严格画像校验使用 jsonschema，真正评估三组文档/Schema、检查日期、拒绝外部 Schema 引用、核对 CSV 映射，并要求仓库模板保持未评估。缺文件或缺依赖时失败退出，不会偷偷跳过。它不会访问网站，也不会测试云基础设施。

编译器输出包含 `catalog` 和输入/输出摘要的 Bundle，将 CMP-02 勘误应用到副本，不改变 ID 或等级。未知目标、重复/冲突勘误和基础版本不匹配都会失败，而不是静默忽略。摘要是来源标识，不是数字签名或安全证明。

## 7. 相关文件

使用[画像](../../controls/semianalysis-public-findings-profile.v1.json)、[Schema](../../controls/semianalysis-public-findings-profile.v1.schema.json)、[勘误](../../controls/neocloud-security-baseline.v1.errata.json)、[40 项模板](../../templates/semianalysis-public-findings-assessment.csv)、[20 项模板](../../templates/clustermax-public-security-requirements-assessment.csv)和[本次审计记录](../../reviews/2026-09-05-validation-audit.md)。本指南增加优先验证流程，不宣称 40 项映射均已实现自动化，更不代表任何服务商已经通过。
