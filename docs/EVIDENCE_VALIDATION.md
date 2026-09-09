# Evidence and advisory-record validation / 证据与公告处置记录校验

**Added:** 2026-09-05 (evidence records) · 2026-09-08 (advisory triage) · Python 3.10+ · Standard library only / 仅标准库

These two offline checkers validate record consistency and freshness, not evidence authenticity, real reviewer independence or service conformance. Exit code 0 is not a provider PASS. Neither checker fetches URLs, reads referenced secrets, installs packages or contacts the network.

两个离线校验器只检查记录一致性和时效，不验证证据真伪、实际人员独立性或服务是否符合基线。退出码 0 不代表服务商通过安全评估。两个工具都不访问 URL、不读取引用的秘密文件、不安装软件、不联网。

## Evidence-record validation / 证据记录校验

```bash
python3 scripts/validate_evidence_records.py templates/evidence-record.example.csv
python3 -m unittest discover -s tests -p test_evidence_records.py -v
```

Run from the repository root. The supplied example is explicitly unassessed. Keep real records in a private evidence system and pass their local path to the same command.

在仓库根目录运行。示例明确为未评估状态。真实记录放在私有证据系统中，以本地文件路径输入。

### Record contract / 字段要求

Every row requires a unique nonempty `evidence_id`, valid `state` and `verification_result`. CSV headers must be unique, without empty or padded names; each row must have exactly the header width. A missing or empty file is an error.

每行要求唯一且非空的 `evidence_id`、合法 `state` 和 `verification_result`。表头不得重名、空白或带首尾空格，行宽必须与表头一致；缺失或空文件报错。

PASS additionally requires `control_id`, `service`, `service_profile`, `environment`, `region_scope`, `asset_scope`, `tenant_scope`, `version_scope`, `assertion`, `test_id`, `collector`, `verifier`, `independence_basis`, `storage_uri`, `integrity_hash` and `invalidation_triggers`.

PASS 还要求上述范围、断言、测试、采集与验证身份、独立性依据、证据位置、摘要和失效触发条件。控制 ID 按当前 18 域、每域 5 项的稳定 ID 格式校验；工具不检查服务真实总体是否完整。

Dates must be timezone-aware RFC3339 and satisfy:

```text
observed_at <= verified_at <= current_time < valid_until
```

过期、未来时间、倒置顺序和不含时区的日期均不能支持 PASS。`VERIFIED` 必须对应 `PASS`；`NOT_TESTED` 不能标记为已验证。非 PASS 记录可以保留未完成字段，不因此获得任何有效性声明。

### Limits / 局限

A hash is syntax-checked as `sha256:<64 lowercase hex>`; the evidence is not fetched and the digest is not recomputed against it. Different reviewer names alone do not establish independence. The checker rejects identical collector/verifier names but cannot discover aliases, collusion or shared administration. Recorded invalidation triggers are not evaluated automatically; a real configuration change can invalidate otherwise unexpired evidence.

摘要只验证语法，不拉取证据并重新计算。姓名不同不能证明独立性；相同采集／验证姓名会被拒绝，但工具不能发现别名、串通或共同管理权。失效触发条件只检查记录是否存在，不自动判断事件是否发生；配置变化可令未到期证据失效。

The old `evidence-register.csv` format is unchanged. This expanded record format is opt-in and includes lifecycle state and additional fields; migrate explicitly rather than silently treating the old file as equivalent. A metadata error never changes the underlying service or authorizes remediation.

旧 `evidence-register.csv` 不变。新格式增加生命周期和额外字段，应显式迁移，不能默认为两者等价。元数据错误不会修改真实服务或授权任何修复动作。

Exit codes: **0** consistent metadata; **1** invalid record assertions; **2** input/parse failure. None certifies a service.

## Advisory-triage validation / 公告处置校验

An optional offline format for tracking the disposition of security advisories against services you operate: which advisory applies to which product/configuration, who owns the decision, what was decided, and when it must be reviewed. It is independent of the control catalog and the CSV templates; keep actual assets, credentials, evidence and customer identifiers outside this public repository. [RB-02](en/VALIDATION_RUNBOOKS.md) references it as an ordinary optional tool for advisory intake.

可选的离线格式，用于跟踪所运营服务对安全公告的处置：哪条公告适用于哪个产品/配置、责任归属、处置决定和复核时间。它与控制目录及既有 CSV 模板相互独立；真实资产、凭据、证据和客户标识保留在本公开仓库之外。[RB-02](en/VALIDATION_RUNBOOKS.md) 将其作为公告接收的普通可选工具引用。

Advisory disposition state and control evidence state are different concepts. "This advisory is dispositioned" does not mean "the related control is independently verified". A recorded PASS here covers only the evidence chain behind the applicability/disposition assertion; it creates no `VERIFIED` control state and no conformance claim.

公告处置状态和控制证据状态是不同概念。“该公告已处置”不等于“相关控制已独立验证”。此处记录的 PASS 只针对适用性/处置断言背后的证据链，不产生任何 `VERIFIED` 控制状态或符合性声明。

### Use / 使用

```bash
# Current metadata check; defaults to the current UTC date.
python3 scripts/validate_advisory_triage.py /private/path/advisory-triage.json

# Reproduce the dated synthetic fixture, not a current operational assessment.
python3 scripts/validate_advisory_triage.py templates/advisory-triage.example.json --as-of 2026-09-08
python3 -m unittest discover -s tests -p test_advisory_triage.py -v

# Full checkout and declared dependencies required; do not claim this passed if unavailable.
python3 scripts/check_local.py
```

### Record semantics / 记录语义

| Fields | Meaning |
|---|---|
| `format_version`, `reviewed_on`, `records` | Exact top-level fields; version is the string `1`; non-empty array of records. |
| `id`, `product`, `source_url` | Unique assessment-row ID, precise product and HTTPS primary-source locator. Separate products/scopes can share an advisory ID. URLs are never fetched by the checker. |
| `source_published_on`, `source_accessed_on` | ISO dates. Publication can be `null` for undated or unresolved source chronology; explain that in `rationale`. Access cannot follow review. |
| `scope`, `version_and_configuration` | Service/region/tenant/asset boundary and installed plus running versions, active configuration and supported backport evidence. These are human assertions, not machine-discovered inventory. |
| `applicability`, `disposition` | `UNKNOWN / AFFECTED / NOT_AFFECTED`; separately `OPEN / MITIGATED / REMEDIATED / NOT_APPLICABLE`. |
| `owner`, `rationale`, `next_review_on` | Responsible owner, reasoning/residual risk and next review date. `UNASSIGNED` is allowed only for unverified intake, not a recorded PASS. |
| `evidence_ids`, `verification_result` | Private evidence references and `PASS / FAIL / INCONCLUSIVE / NOT_TESTED`. The example contains no secret values or real evidence. |
| `reviewer`, `verified_on`, `valid_until` | Reviewer and evidence dates. A different name is necessary for this metadata check, but does not prove independence. |

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

The checker rejects missing/unknown fields, duplicate JSON keys/IDs, non-finite numbers, malformed dates, invalid enums, future reviews and overdue review dates. Dates use `YYYY-MM-DD`; validity ends at the start of `valid_until`. A PASS requires known applicability, evidence references, an assigned owner, a distinct assigned reviewer and current verification dates. The next review cannot exceed evidence validity. Non-PASS records carry `null` verification/validity dates.

校验器拒绝缺失/未知字段、重复 JSON 键及 ID、非有限数、错误日期、未知枚举、未来复核及到期未复核。日期采用 `YYYY-MM-DD`；有效性在 `valid_until` 当日开始时结束。PASS 要求已知适用性、证据引用、已分配 Owner、不同且已分配的复核人及当前有效验证日期；下次复核不能晚于证据到期。非 PASS 记录的验证及有效期日期为 `null`。

`MITIGATED` and `REMEDIATED` require `AFFECTED` and a recorded PASS. `NOT_APPLICABLE` requires evidence-backed `NOT_AFFECTED` and a recorded PASS for that applicability assertion; it does not mark the underlying control inapplicable. Unknown scope cannot close. Temporary mitigation is not a patch; residual risk and expiry remain explicit. Risk acceptance belongs to the existing exception/risk process and does not create PASS, VERIFIED or conformance.

`MITIGATED`、`REMEDIATED` 要求 `AFFECTED` 和已记录 PASS；`NOT_APPLICABLE` 要求有证据支持的 `NOT_AFFECTED`，以及针对该适用性判断的已记录 PASS，且不表示底层控制项不适用。范围未知不能关闭。临时缓解不等于补丁，剩余风险和到期时间仍需明确。风险接受进入既有例外/风险流程，不能制造 PASS、VERIFIED 或符合性。

### Limits / 局限

Exit 0 means consistent metadata as of the printed date. It does **not** authenticate sources/evidence, compare package versions, evaluate configuration, establish reviewer independence, evaluate invalidation events or verify remediation. Historical `--as-of` is replay only. Reopen the operational record after a relevant material change even before its time-based expiry. Every applicable unverified T0 remains **NO_GO_NONCONFORMANT**.

退出码 0 仅表示打印日期下的元数据一致性，不验证来源/证据真伪，不比较包版本，不评估配置，不证明复核独立性，不判断失效事件，也不证明修复。历史 `--as-of` 仅供回放；即使未到期，相关重大变更后仍应重新打开运营记录。每个适用且未验证的 T0 继续保持 **NO_GO_NONCONFORMANT**。

See [English runbooks](en/VALIDATION_RUNBOOKS.md), [中文验证手册](zh-CN/VALIDATION_RUNBOOKS.md) and the [follow-up review](../reviews/2026-09-05-evidence-followup.md).
