# Weekly NeoCloud security review / 每周安全研究 — 2026-09-08

**Status:** dated research and repository implementation review; not a provider assessment.  
**Timezone:** Asia/Singapore. **Calendar week:** 2026-09-07–2026-09-13, observed only through September 8.  
**Rolling discovery window:** September 2–8; September 1 carryovers are labelled separately.  
**Reviewed base commit:** `030b67eb6a0930910ecb70e555861ac882926535`.  
**Base tree:** `f76489b70245af956cc4ef2db2c2be3ff00c57cd`.  
**Implementation tracking:** [Issue #7](https://github.com/timwhitez/neocloud-sec/issues/7).  
**Full-checkout evidence follow-up:** [Issue #8](https://github.com/timwhitez/neocloud-sec/issues/8).

## Executive finding / 核心结论

The current 90-control baseline already covers the essential mechanisms. This week's useful delta is operational precision: bind advisories to exact products and running configurations; verify derived-credential revocation at the backend; constrain storage-controller authority; enforce agent permissions at the resource; distinguish publication from deployment and future legal deadlines. No new control IDs, cloud integrations, CNI mandate or security platform is justified by these findings.

现有基线并不缺少“补丁、IAM、隔离、供应链、应急”等大类。真正值得落地的是把最新公告接入既有机制，补足**适用性、运行态证据、撤权后残留凭据、控制器权限、日期与来源状态**的操作闭环。不得把本次发现的第三方产品问题称为本仓库的漏洞，也不得把本仓库 PR 合并称为服务商已修复。

交付为双语[周审流程](../docs/zh-CN/WEEKLY_SECURITY_REVIEW.md)、[English procedure](../docs/en/WEEKLY_SECURITY_REVIEW.md)、[合成台账](../templates/advisory-triage.example.json)、[离线元数据校验](../scripts/validate_advisory_triage.py)及[负向测试](../tests/test_advisory_triage.py)。90 个控制、等级、核心 `1.0.0-draft.1`、画像 `1.0.1`、既有 Schema、验证器和手动工作流均不改动。

## 1. Research method and limits / 方法与限制

先检查仓库树、main、Issue/PR 历史、双语入口、基线及十类验证手册，再核对证据校验器、本地入口、核心校验器相关契约、准确性校验、贡献与治理要求、已有参考资料。当前实现是文档与离线验证工具，不是云安全控制平面；因此不新增部署服务或扫描程序。

外部调研按“发现 → 原厂公告 → 产品发布/变更或其他一手来源 → 现有控制 → 可执行差距 → 反证/范围收敛”进行。正文每条产品或法规判断均指向下方来源。关键交叉核验包括 Google 产品页与 SchedMD 发布线、AWS 公告与 EFS CSI 固定提交的变更日志、NVIDIA 公告内部不同 CVE 修复边界、Microsoft 的 OS/CNI 限制，以及欧委会 reporting 与总览页面。

部分动态官网直接打开返回缓存/访问错误，但搜索工具可返回原厂索引正文，已在台账标识为 `indexed-primary`。这不等于取得原始响应、签名快照或无遗漏的实时 feed。新闻聚合和扫描器数据库仅用于发现线索，不作为本报告技术结论的唯一依据。未取得可靠一手说明的分支不写入最低安全版本表；未检索到新公告不代表无漏洞。

容器直接克隆 GitHub 遇到 DNS/网络限制；通过已连接 GitHub 读取固定提交。修改的四个既有文档先重建并比对原始 Git blob SHA；本轮没有完整检出全部历史文件，没有逐字重审全部白皮书或完整重跑旧目录/编译器套件。这里的“范围内审查”不应扩展为全仓库或全行业无遗漏证明。没有生产、GPU/Fabric、跨租户、恢复或漏洞利用测试，没有独立人员/sub-agent 保证。文档和代码分别进行了作者复核；其性质仍是 self-review。

## 2. 本周及近期新增到项目的实践

### W01 — Slurm：镜像已修复不等于节点已修复

**本周事件：** Google Cluster Toolkit 的 GCP-2026-060 发布于 **9 月 7 日**，针对 CVE-2026-65107，明确要求处理尚未自该日期起重新创建的节点。[S01] SchedMD 的 9 月安全发布线包括 **26.05.4、25.11.8、25.05.9**；上游修复不能直接充当发行版回补或云托管构建的证明。[S02]

**动作：** 对准确服务、镜像构建、运行进程及节点替换时间建立记录；采用受支持修复和维护计划，验证金丝雀作业、隔离、重启/替换后的运行态及恢复。公告编号相同也需保留产品 URL：Google 总览将 9 月 4 日条目指向 Cluster Director，而 Toolkit 页面为 9 月 7 日，不能把两个日期拼成统一规则。[S01,S08]

**仓库差距：** RB-02 已要求安装/运行版本、回补、金丝雀及隔离。本轮增加的是公告处置台账和产品/日期区分，不重复添加“补丁管理”控制。

### W02 — Triton：按各 CVE 的修复边界处理

**本轮最新核验：** NVIDIA 5875 号公告建议 **r26.07 或后续版本**；表中 CVE-2026-16497 的修复版本是 **26.07**，CVE-2026-47625 则是 **26.04**。不能说两个问题都始于或都在 26.07 首次修复，也不能把该建议当作所有后续漏洞的永久安全下限。[S03]

**日期冲突：** 页面头为 9 月 4 日更新，Revision History 写 9 月 8 日 Initial Release；两者原样记录。选用受支持兼容构建、固定制品摘要并核对实际运行服务，不凭“最新版”字符串关闭。保留 API 授权、资源预算、异常请求/资源耗尽监控；本轮不构造攻击请求。[S03]

### W03 — EFS CSI：判断真实配置及控制器所有权

**回溯窗口：** AWS 9 月 4 日公告 CVE-2026-85781 涉及驱动 **<=3.4.0**，修复为 **3.4.1**；受影响条件包括非默认 `--delete-access-point-root-dir=true`，且涉及 PV 创建权限。AWS 明确区分驱动问题与 EFS 服务本身。[S04]

**交叉核验：** 官方 3.4.1 Release 的发布日期实际为 **7 月 23 日**，其固定提交变更日志记录 DeleteVolume 所有权检查；公告日期不是补丁首次发布日期。[S05]

**动作：** 审查 PV 创建权限、真实选项、CSI IAM、资源策略及对象归属。不能即时升级时遵循原厂缓解，记录业务影响及复验；只采用惰性夹具或非破坏性检查，不提供/执行破坏性 Volume Handle。映射既有 NCS-API-01、NCS-DAT-04、NCS-ORC-02。[S04,S05]

### W04 — ECK：撤销 RBAC 后检查后端派生凭据

**旧事项延续：** Elastic 原厂页面发布日期为 **9 月 1 日**。CVE-2026-78600 涉及 **2.6.0–3.4.1** 的特定跨 Namespace 关联及后续 RBAC 执行/撤销场景，修复为 **3.5.0**。原厂指出，关联被拒绝后保留的凭据仍可能产生后端读取权限；不能只看 Kubernetes 返回拒绝就关闭事件。[S06]

**动作：** 在授权合成环境检查 Operator 状态收敛、派生凭据清理/轮换及旧凭据在后端被拒绝，同时验证合法身份仍正常。风险排序应考虑租户边界，不单凭该公告的低 CVSS 排到末尾。原厂写明不能升级时没有 workaround；本报告不把自行轮换冒充厂商保证的完整修复。[S06]

### W05 — Agent/MCP：资源侧权限才是执行边界

**回溯窗口：** AWS 9 月 4 日 CVE-2026-85787 公告涉及 postgres MCP server **<1.1.7**；SQL 禁止列表并不能单独保证只读。原厂修复为 **1.1.7**，并强调专用最小权限数据库角色。[S07]

**动作：** 沿用 NCS-AIR-03，把资源身份权限作为独立于模型和工具过滤器的边界，验证正常读取与不允许副作用。只读描述、提示词、客户端声明和工具参数不能替代数据库授权。本轮只补充操作流程，不引入新的 Agent 框架或生产执行器。[S07]

### W06 — IAM：区分注册权限、联合身份及已修复托管服务

Google 9 月 2 日 GCP-2026-058 涉及 GKE Multi-Cloud 集群创建/注册时的项目权限校验和目标项目 Workload Identity Federation。研究启示是联合身份信任链需包含“谁能注册身份来源”，不只是检查最终 token。[S08]

同一官方总览的 GCP-2026-059 虽在 9 月 4 日发布，却明确标注 **2025 年 12 月 11 日已修复且无需客户操作**。这类情况记录 provider-fixed/customer-action-none，而不是要求用户安装不存在的补丁。对 058 的具体服务修复状态，本轮未完成产品详情核验，不宣称客户无需动作或给出猜测的安全版本。[S08]

### W07 — AKS 网络：OS 兼容性与真实迁移窗口

Microsoft 当前文档注明 **Windows NPM 支持截至 2026 年 9 月 30 日，Linux 为 2028 年 9 月 30 日**，且 Azure CNI powered by Cilium 仅支持 Linux。不能把“推荐 Cilium”改成所有 NeoCloud、所有 Windows 工作负载的强制要求。[S09]

**动作：** 对实际使用 Windows NPM 的服务提前评估受支持路径；默认拒绝前确认 DNS/业务依赖，做允许和拒绝配对测试及回滚。对不使用该组件的环境保留有证据的适用性判断，不进行无收益重构。[S09]

### W08 — 虚拟化与 NeoCloud：声明必须绑定产品和边界

Broadcom 9 月 3 日 VMSA-2026-0007 的列明产品是 **Workstation 与 Fusion**；本轮不把它写成所有 ESXi/GPU 云均受影响。是否进入处置队列取决于构建/运维工作站是否实际使用该产品。[S19]

CoreWeave 公开架构与 Nebius IAM 文档可作为产品实现参照，不是独立租户隔离证明。Nebius 的 `viewers` 包含部分数据访问能力，角色名称不能自动等同元数据审计角色；需要按真实权限区分。[S10,S11] 保留现有 GPU sharing、Fabric、BMC/OOB、节点与存储的分层责任，不复制某供应商的整个技术栈。

### W09 — 合规与应急：明确尚未到来的日期

截至 **9 月 8 日**，欧盟 CRA 的相关报告义务开始日 **9 月 11 日** 尚未到来；欧委会页面针对含数字元素产品的制造商，涉及被积极利用漏洞及严重产品安全事件。先由法务核定产品、市场、供应商角色和服务组成，不推定每家 NeoCloud 自动适用。[S16,S17]

**动作：** 在适用范围内确认收件人、事件发现时点、证据保全、审批和通知演练；关注官方早期预警/后续报告流程。不能据本轮资料宣称 SRP 平台已投产，也不把通用控制合规映射当成法律意见。NIST SP 800-239 仍为 Initial Public Draft，公开评论截至 **9 月 25 日**；维持草案标识，不变成新的硬性基线。[S16,S18]

## 3. Cross-domain coverage and gap decision / 领域覆盖与取舍

| 领域与现有控制域 | 原有机制及本轮依据 | 本轮处置 |
|---|---|---|
| 治理/合规 GOV | 已有责任、例外、框架状态；CRA 与 NIST 草案 [S16–S18] | 增加日期和产品/司法辖区核定；不新增认证或法律保证 |
| 资产与暴露 ASM、VEM | RB-02 已区分安装与运行版本；Slurm、Triton [S01–S03] | 处置台账连接配置、责任、复核与证据；实际资产未知保留 UNKNOWN |
| 身份/API IAM、API | 现有 RBAC、委托和租户边界；ECK、GCP、Nebius [S06,S08,S11] | 补充派生凭据失效及身份来源注册权限核对 |
| 网络/硬件 NET、PHY | RB-03/04 已有 DPU、P_Key、OOB；AKS、CoreWeave [S09,S10] | 范围化迁移、允许/拒绝与恢复；不强制 CNI，不降低 Fabric/物理边界 |
| 虚拟化/GPU/调度 CMP、ORC | RB-01/02/09 已有 GPU 模式、运行态及调度；[S01–S03,S13,S14,S19] | 补充产品适用性；time-slicing 仍不是内存/故障隔离证明 |
| 数据/密钥 DAT、KMS | RB-06/07 已有租户数据、删除、恢复及安全加载；[S04–S06] | 存储所有权、控制器最小权限及派生凭据撤销；不发布密钥或客户证据 |
| 供应链/工程 SSC、ENG | RB-07 已有签名、来源和召回；SLSA 验证预期 [S12] | 明确制品摘要、构建者、来源与预期输入的绑定；不增加制品平台 |
| 监控检测 TEL | RB-05 已明确 Prometheus/Grafana 后端边界；[S06,S15] | 串联 Operator/凭据/后端/存储事件，保留采集缺失与归因限制 |
| AI 与滥用 AIR、ABU | RB-08 和配额已有覆盖；MCP/Triton [S03,S07] | 资源侧授权、预算和停止条件；不新增任意自主攻防流程 |
| 应急/恢复 IRR、RES | RB-02/06/10 已有遏制、回滚、恢复和独立验证；[S01,S04,S16] | 日期、通知责任、隔离和恢复后身份验证补充；未执行恢复不能标记 PASS |

以上是来源与操作机制的对照，不是标准精确等价映射或服务商评分。没有新增证据支持的问题不强行转成 Issue；重复控制不重新编号。没有要求安装 SBOM/SIEM/CSPM 等新平台。原有 REFERENCES.md 的 9 月 4 日基础资料截止不被整体改成 9 月 8 日，以免暗示所有历史来源均被重核；本报告是有范围的增量台账。

## 4. Implementation, tests and merge boundary / 落地与验收边界

**Issue #7 的实现：** 一份日期化研究、两份等义运营指南、一份合成 JSON 台账、一份标准库校验器及其测试，更新双语入口、贡献指南和 Changelog。新格式仅服务公告处置元数据，不修改原有证据/控制状态模型，不被核心编译器导入。

**校验负向覆盖：** UNKNOWN 不能获得 PASS 或标为修复；缓解/修复/不适用需要匹配的适用性和当前已记录 PASS；证据、Owner/Reviewer、到期及下次复核的关系；重复键/记录/证据；非法字段/枚举/日期；带凭据或非 HTTPS 来源；错误编码、缺文件与坏 JSON；历史回放和到期失败。仍不能验证证据真伪、实际配置/修复、真实独立性或事件触发失效。

实际执行环境为 **Python 3.13.5**。本轮独立测试命令：

```text
python3 -m unittest discover -s tests -p test_advisory_triage.py -v
Ran 47 tests
OK

python3 scripts/validate_advisory_triage.py templates/advisory-triage.example.json --as-of 2026-09-08
Metadata consistent AS OF 2026-09-08; ... remediation NOT verified.

python3 -m py_compile scripts/validate_advisory_triage.py tests/test_advisory_triage.py
```

四个被修改既有文档在编辑前已与固定 Base 的 Git blob SHA 一致。最终候选的内容哈希、相对链接/结构检查、精确 Head、再次执行结果及合并决定以 PR 留存为准，避免在报告中自引用尚未产生的 Commit。

**未执行：** 完整历史套件和真实核心目录的端到端编译、Python 多版本运行矩阵、真实集群补丁/凭据/存储/网络/恢复测试、独立人工评估。47 不是把既往 70 与 18 相加后的结果。完整检出回归证据保留在 **Issue #8**，不会随 #7 的文档/独立工具 PR 自动关闭。没有触发远端 Actions、修改工作流/分支规则或安排后台任务。

**合并原则：** 本轮增量模块及文档在范围内测试、内容核对和独立于编写步骤的作者复核通过后，才可合并精确 Head；完整旧套件没有被声称为绿色。任何会修改核心 Schema、编译器或既有验证语义的改动，都不应借此有限验证范围合并。本轮未包含这类改动。

## 5. 下一轮继续跟踪；本轮不伪造完成

| 事项 | 继续跟踪的判断点 | 本轮未做或未合并的原因 |
|---|---|---|
| 完整检出本地回归 | Issue #8；真实核心目录编译与全部现存测试 | 当前克隆/网络限制；不是已经复现的代码故障 |
| Slurm 跨产品补丁传播 | 发行版回补、托管镜像、运行进程及节点实际替换 | 本仓库没有客户资产；不能凭厂商公告关闭运营记录 |
| NVIDIA Triton | 公告日期冲突是否修订、各受支持产品分支及实际构建 | 不锁死永久“最低安全版本”，不执行攻击复现 |
| ECK 派生身份 | 升级后跨 Namespace 收敛及旧凭据失效证据 | 无授权实验集群；不把自拟轮换流程称为完整原厂修复 |
| GKE Multi-Cloud / AWS ParallelCluster / MSRC | 进一步取得具体产品的最新官方处置状态 | 本轮未完整核定这些分支的修复/客户动作；不写猜测版本 |
| CRA / NIST / AKS | 9 月 11 日报告义务、9 月 25 日草案评论、9 月 30 日 Windows NPM 期限 | 均为范围化未来节点，不提前声称生效、完成或普遍适用 |
| 实际检测与恢复 | 租户安全的关联 ID、来源丢失、后端拒绝、恢复后身份检查 | 本轮补充的是验证方案，没有运行生产检测或恢复演练 |

## 6. Primary-source ledger / 一手来源台账

All sources were retrieved or inspected through available tools on **2026-09-08**. `indexed-primary` means the publisher's indexed text was available but a direct page response was not reliably obtained. `direct` means readable primary-page text; it does not mean independent verification of the publisher's operational claims. Living documentation is not automatically a publication from this week.

| ID | 一手来源与状态 | 日期/核验范围与限制 |
|---|---|---|
| S01 | [Google Cluster Toolkit security bulletins](https://docs.cloud.google.com/cluster-toolkit/docs/security-bulletins) — vendor bulletin, indexed-primary | GCP-2026-060 published 2026-09-07; Toolkit 节点和镜像处置，不外推其他服务 |
| S02 | [SchedMD September 2026 announcements](https://lists.schedmd.com/mailman3/hyperkitty/list/slurm-users%40lists.schedmd.com/2026/9/) — upstream, indexed-primary | September 2 security release announcement; 26.05.4 / 25.11.8 / 25.05.9；不是发行版回补证明 |
| S03 | [NVIDIA Triton bulletin 5875](https://nvidia.custhelp.com/app/answers/detail/a_id/5875) — vendor bulletin, indexed-primary | Header 2026-09-04 versus initial revision 2026-09-08；各 CVE 修复边界分别记录 |
| S04 | [AWS 2026-099](https://aws.amazon.com/security/security-bulletins/2026-099-aws/) — vendor bulletin, indexed-primary | 2026-09-04; CVE-2026-85781；驱动、非默认选项、权限前提及 EFS 服务范围 |
| S05 | [EFS CSI v3.4.1 release](https://github.com/kubernetes-sigs/aws-efs-csi-driver/releases/tag/v3.4.1) and [fixed-commit changelog](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/3fcc6bdd7533a4cfd15643b31593f7ff154584c9/CHANGELOG-3.x.md) — GitHub connector | Release published 2026-07-23；变更日志确认 DeleteVolume 所有权检查；未分析或执行利用代码 |
| S06 | [Elastic ESA-2026-146](https://discuss.elastic.co/t/elastic-cloud-on-kubernetes-3-5-0-security-update-esa-2026-146/390106) — vendor bulletin, indexed-primary | Vendor page September 1；2.6.0–3.4.1 / 3.5.0；特定跨 Namespace 生命周期；旧事项延续 |
| S07 | [AWS 2026-101](https://aws.amazon.com/security/security-bulletins/2026-101-aws/) — vendor bulletin, indexed-primary | September 4；postgres MCP <1.1.7 / 1.1.7；原厂资源侧权限建议 |
| S08 | [Google Cloud security bulletins](https://docs.cloud.google.com/support/bulletins) — vendor bulletin, indexed-primary | 058: September 2；059: September 4，但 2025-12-11 已修复；060 总览指向 Director，不能替代 Toolkit 页 |
| S09 | [Microsoft AKS network-policy best practices](https://learn.microsoft.com/en-us/azure/aks/network-policy-best-practices) — living vendor guidance, direct | Windows/Linux NPM 期限与 Cilium Linux-only；不宣称本周首次发布 |
| S10 | [CoreWeave security architecture](https://docs.coreweave.com/security/architecture) — living vendor guidance, direct | 产品架构声明，用于边界对照；不是独立隔离或不可变日志证明 |
| S11 | [Nebius IAM overview](https://docs.nebius.com/iam/overview) and [service-account authentication](https://docs.nebius.com/iam/service-accounts/authentication) — living vendor guidance, indexed-primary | 角色/组和不同服务凭据；角色名称不等同实际数据权限 |
| S12 | [SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) — approved project specification, indexed-primary | 核对摘要、构建者/信任根、来源与预期输入；已在基础 REFERENCES 引用 SLSA，非本周新标准 |
| S13 | [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/) — upstream living documentation, direct | 复核命名空间/控制面与节点边界区分；未对具体集群执行测试 |
| S14 | [NVIDIA GPU Operator sharing](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html) — living vendor guidance, direct | 保留 time-slicing 内存/故障隔离与归因局限；不增改硬件证明声明 |
| S15 | [Prometheus security model](https://prometheus.io/docs/operating/security/) — upstream living documentation, direct | HTTP/查询边界和 RB-05 对照；标签不是授权 |
| S16 | [European Commission CRA reporting](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting) — official guidance, direct | 2026-09-11 是未来适用日期；平台状态不作已上线保证 |
| S17 | [European Commission CRA overview](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) — official guidance, direct | 产品/制造商范围与一般适用时间区分；非法律意见 |
| S18 | [NIST SP 800-239](https://csrc.nist.gov/pubs/sp/800/239/ipd) and [NIST announcement](https://csrc.nist.gov/News/2026/ai-data-center-security-analysis-draft-sp-800-239) — initial public draft, indexed-primary | Published 2026-07-27；comment deadline 2026-09-25；仅核验发布状态/范围，未重新全文分析 PDF |
| S19 | [Broadcom VMSA-2026-0007](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38288) — vendor advisory, indexed-primary | Published September 3；Workstation/Fusion，不外推 ESXi 或全部 NeoCloud |

No exploit payloads, production identities, secrets, proprietary framework text or fabricated deployment results are included. 本报告没有创建外部订阅或定时执行；后续每周运行需由有权限的执行环境实际触发并重新核验来源。
