# 每周安全研究与公告处置

[English](../en/WEEKLY_SECURITY_REVIEW.md) · [2026-09-08 调研记录](../../reviews/2026-09-08-weekly-security-review.md)

这是运营补充，不是新的控制目录、漏洞扫描器、调度器或证明系统。结合现有[验证手册](VALIDATION_RUNBOOKS.md)、[治理要求](../../GOVERNANCE.md)和[证据校验器](../EVIDENCE_VALIDATION.md)使用。本文不会安装或启动后台定时任务。

## 1. 每周重复执行的决策流程

记录准确的基线 Commit、时区、自然周起止和资料截止时间，区分本周发布、滚动回溯、旧事项延续及未来截止日期。重要判断记录一手 URL、发布/修订日期、访问日期、产品与配置适用性、访问限制。日期冲突应保留，不猜测哪个正确。使用产品发布记录、变更日志或第二个一手来源交叉核验；转载不构成独立证据。

覆盖供应链、IAM/API、网络/Fabric、Host/GPU/虚拟化、Kubernetes/Slurm、数据/密钥、可观测性/检测、治理/合规、滥用防护与应急恢复。各领域分别决定：可执行仓库改动、已覆盖、证据不足待跟踪或不适用。未确认某类新事件，不等于该类没有漏洞。

先读当前目录、勘误和相关实现，再判定 gap。优先补充缺失示例、证据约定和有边界的负向检查，而不是新增平台。结合真实适用性，优先处理已暴露或已被利用的路径、租户边界、信任根和控制面风险，不能仅按 CVSS 排序。未解决暴露及复核日期保留在私有运营台账。

有跟踪价值时创建集中 Issue，再提交 PR；执行本地检查，复核准确 Head，仅合并已测试且合理的改动。额度受限期间不调度或重跑远端 Actions；保留手动工作流并使用 `[skip ci]`，不绕过分支规则。合并前再次检查 Base/Head。部分检出或检查失败必须披露，不能描述为完整测试通过。

每次输出新增实践、仓库 gap、Issue/PR、准确测试、已合并内容、未合并及原因和后续跟踪方向。修正文档不表示客户环境已经修复。

## 2. 最小公告台账

[合成示例](../../templates/advisory-triage.example.json)仅说明格式，不是评估结果。真实资产、凭据、证据和客户标识保留在本公开仓库之外。该可选格式与核心目录及既有 CSV 独立。

| 字段 | 含义 |
|---|---|
| `format_version`、`reviewed_on`、`records` | 顶层仅这些字段；版本为字符串 `1`；记录数组不能为空。 |
| `id`、`product`、`source_url` | 唯一评估行 ID、准确产品及 HTTPS 一手来源。不同产品/范围可以引用相同公告 ID；校验器不会访问 URL。 |
| `source_published_on`、`source_accessed_on` | ISO 日期。持续更新或日期冲突未解决的来源可把发布日期设为 `null`，在 `rationale` 解释；访问不得晚于复核。 |
| `scope`、`version_and_configuration` | 服务/区域/租户/资产边界，安装及运行版本、生效配置与受支持回补证据。属于人工声明，不是自动发现的资产清单。 |
| `applicability`、`disposition` | 分别为 `UNKNOWN / AFFECTED / NOT_AFFECTED` 和 `OPEN / MITIGATED / REMEDIATED / NOT_APPLICABLE`。 |
| `owner`、`rationale`、`next_review_on` | 责任人、判断/剩余风险及下次复核日期。`UNASSIGNED` 仅允许用于尚未验证的收件记录，不得用于已记录 PASS。 |
| `evidence_ids`、`verification_result` | 私有证据引用，以及 `PASS / FAIL / INCONCLUSIVE / NOT_TESTED`；示例不包含真实证据或密钥值。 |
| `reviewer`、`verified_on`、`valid_until` | 复核人及证据日期。不同姓名是此元数据检查的必要条件，但不能证明真实独立性。 |

校验器拒绝缺失/未知字段、重复 JSON 键及 ID、非有限数、错误日期、未知枚举、未来复核及到期未复核。日期采用 `YYYY-MM-DD`；有效性在 `valid_until` 当日开始时结束。PASS 要求已知适用性、证据引用、已分配 Owner、不同且已分配的复核人及当前有效验证日期；下次复核不能晚于证据到期。非 PASS 记录的验证及有效期日期为 `null`。

`MITIGATED`、`REMEDIATED` 要求 `AFFECTED` 和已记录 PASS；`NOT_APPLICABLE` 要求有证据支持的 `NOT_AFFECTED`，以及针对该适用性判断的已记录 PASS，不表示底层控制项不适用。范围未知不能关闭。临时缓解不等于补丁，剩余风险和到期时间仍需明确。风险接受进入既有例外/风险流程，不能制造 PASS、VERIFIED 或符合性。

```bash
# 当前元数据检查：默认使用当前 UTC 日期。
python3 scripts/validate_advisory_triage.py /private/path/advisory-triage.json

# 回放有日期的合成示例，不代表当前运营评估。
python3 scripts/validate_advisory_triage.py templates/advisory-triage.example.json --as-of 2026-09-08
python3 -m unittest discover -s tests -p test_advisory_triage.py -v

# 需要完整检出及已声明依赖；条件不具备时不得宣称此检查通过。
python3 scripts/check_local.py
```

退出码 0 仅表示打印日期下的元数据一致性，不验证来源/证据真伪，不比较包版本，不评估配置，不证明复核独立性，不判断失效事件，也不证明修复。历史 `--as-of` 仅供回放；即使未到期，相关重大变更后仍应重新打开运营记录。每个适用且未验证的 T0 继续保持 **NO_GO_NONCONFORMANT**。

## 3. 四项有边界的运营补充

以下为项目编写的流程，依据见[有日期的一手来源台账](../../reviews/2026-09-08-weekly-security-review.md)，补充而不替代 RB-01/02/06/07/08。仅在明确授权的合成实验环境内执行，并事先确定 Owner、维护窗口、中止条件与恢复路径。不复现公开漏洞利用，不探测第三方租户。

### A. 从补丁发布到运行态证据

映射 NCS-ASM-01、NCS-ORC-04、NCS-CMP-03。识别准确托管服务、OS 镜像/构建、控制器及运行进程，而非只看包名或镜像族。区分上游修复、发行版回补、云镜像发布和实际节点替换。通过批准的金丝雀验证已加载版本、作业完成、策略生效和恢复能力。未验证容量保持隔离，回滚不得自动重新投放脆弱镜像。记录合法作业成功及经审查的禁止边界结果。服务商独占的证据仍由服务商负责。

### B. 撤权不能止于 Kubernetes API

映射 NCS-IAM-04、NCS-KMS-02、NCS-ORC-04。使用一次性身份和无害记录，撤销此前允许的跨 Namespace 关联；检查 Operator 对后端派生凭据的清理/轮换及状态收敛。核对旧测试凭据在后端被拒绝，同时另一已授权身份仍成功。凭据脱敏，只保留决策与请求 ID。Kubernetes 拒绝不代表现存数据库凭据已失效。发现异常访问立即停止，完成遏制/轮换及独立复验后再开放。

### C. 存储控制器权限

映射 NCS-API-01、NCS-DAT-04、NCS-ORC-02。联合审查 PV 创建权限、实际删除选项、CSI 身份、Filesystem/Access Point 所有权及云资源策略。优先采用厂商修复和最小权限。通过惰性单元夹具或厂商支持的非破坏性检查验证对象/租户归属，不构造破坏性 Volume Handle，不删除真实数据；同时确认合法存储使用仍成功。驱动缺陷不自动等于存储服务被攻破；关闭受影响配置是需要证据和重验证的适用性判断。

### D. Agent 与模型流水线权限

映射 NCS-AIR-03、NCS-SSC-02、NCS-DAT-03。在数据库/资源身份处落实只读权限，不仅依赖工具描述或 SQL 过滤。制品准入将摘要绑定到批准的签名者/构建者、源码仓库和预期构建输入；签名有效本身不足。使用无害的不支持格式与未授权合成请求，不使用恶意载荷；验证合法路径和被拒绝操作没有副作用，记录回滚/召回及使用身份。沿用既有加载隔离和来源验证，不强制新增 Agent 框架。

## 4. 网络迁移、检测与应急准备

厂商功能退役是有范围的迁移触发器，不是让所有云统一采用某种 CNI 的理由。默认拒绝上线前记录 OS/CNI 兼容性、DNS/服务依赖及配对的允许/拒绝测试，保留 OOB 和恢复通道。Kubernetes NetworkPolicy 不能替代 Fabric/DPU/存储隔离，继续使用 RB-03/04/09。

使用租户安全的关联 ID 串联策略变更、Operator 收敛、凭据生命周期、后端拒绝和存储决策；对审计来源缺失告警。Dashboard、Prometheus 标签或采集程序退出成功不等于租户授权。保留 RB-05 及其归因局限。

法律截止日期首先由法务/合规责任人确认真实产品、供应商角色、司法辖区和合同范围，再维护事件收件、证据保全、授权、通知和恢复演练。未来截止不是已经生效的义务；草案不是正式标准。具体日期放在本轮报告中，不冻结进通用基线。
