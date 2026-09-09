# Evidence and advisory-record validation / 证据与公告记录校验

**Added:** 2026-09-05 · Python 3.10+ · Standard library only / 仅标准库

This checker validates record consistency and freshness, not evidence authenticity, real reviewer independence or service conformance. Exit code 0 is not a provider PASS.

此工具只检查记录一致性和时效，不验证证据真伪、实际人员独立性或服务是否符合基线。退出码 0 不代表服务商通过安全评估。

## Use / 使用

```bash
python3 scripts/validate_evidence_records.py templates/evidence-record.example.csv
python3 -m unittest discover -s tests -p test_evidence_records.py -v
```

Run from the repository root. The supplied example is explicitly unassessed. Keep real records in a private evidence system and pass their local path to the same command. It does not follow evidence URLs, read referenced secret files, install packages or contact the network.

在仓库根目录运行。示例明确为未评估状态。真实记录放在私有证据系统中，以本地文件路径输入。工具不访问证据 URL、不读取引用的秘密文件、不安装软件、不联网。

## Record contract / 字段要求

Every row requires a unique nonempty `evidence_id`, valid `state` and `verification_result`. CSV headers must be unique, without empty or padded names; each row must have exactly the header width. A missing or empty file is an error.

每行要求唯一且非空的 `evidence_id`、合法 `state` 和 `verification_result`。表头不得重名、空白或带首尾空格，行宽必须与表头一致；缺失或空文件报错。

PASS additionally requires `control_id`, `service`, `service_profile`, `environment`, `region_scope`, `asset_scope`, `tenant_scope`, `version_scope`, `assertion`, `test_id`, `collector`, `verifier`, `independence_basis`, `storage_uri`, `integrity_hash` and `invalidation_triggers`.

PASS 还要求上述范围、断言、测试、采集与验证身份、独立性依据、证据位置、摘要和失效触发条件。控制 ID 按当前 18 域、每域 5 项的稳定 ID 格式校验；工具不检查服务真实总体是否完整。

Dates must be timezone-aware RFC3339 and satisfy:

```text
observed_at <= verified_at <= current_time < valid_until
```

过期、未来时间、倒置顺序和不含时区的日期均不能支持 PASS。`VERIFIED` 必须对应 `PASS`；`NOT_TESTED` 不能标记为已验证。非 PASS 记录可以保留未完成字段，不因此获得任何有效性声明。

## Limits / 局限

A hash is syntax-checked as `sha256:<64 lowercase hex>`; the evidence is not fetched and the digest is not recomputed against it. Different reviewer names alone do not establish independence. The checker rejects identical collector/verifier names but cannot discover aliases, collusion or shared administration. Recorded invalidation triggers are not evaluated automatically; a real configuration change can invalidate otherwise unexpired evidence.

摘要只验证语法，不拉取证据并重新计算。姓名不同不能证明独立性；相同采集／验证姓名会被拒绝，但工具不能发现别名、串通或共同管理权。失效触发条件只检查记录是否存在，不自动判断事件是否发生；配置变化可令未到期证据失效。

The old `evidence-register.csv` format is unchanged. This expanded record format is opt-in and includes lifecycle state and additional fields; migrate explicitly rather than silently treating the old file as equivalent. A metadata error never changes the underlying service or authorizes remediation.

旧 `evidence-register.csv` 不变。新格式增加生命周期和额外字段，应显式迁移，不能默认为两者等价。元数据错误不会修改真实服务或授权任何修复动作。

Exit codes: **0** consistent metadata; **1** invalid record assertions; **2** input/parse failure. None certifies a service.

See [English runbooks](en/VALIDATION_RUNBOOKS.md), [中文验证手册](zh-CN/VALIDATION_RUNBOOKS.md) and the [follow-up review](../reviews/2026-09-05-evidence-followup.md).

<a id="advisory-records"></a>
## Optional advisory records / 可选公告记录

Use the existing [synthetic JSON example](../templates/advisory-triage.example.json) and [offline checker](../scripts/validate_advisory_triage.py) when a small private advisory register is useful. This is a separate opt-in format, not a replacement for evidence CSVs, the control catalog, a vulnerability scanner or an attestation system. No new mandatory platform is needed.

需要小型私有公告台账时，可使用已有 JSON 示例与离线校验器。此格式独立且可选，不替代证据 CSV、控制目录、漏洞扫描器或安全证明系统，也不要求新增平台。

```bash
# Current UTC-date metadata check against a private local register:
python3 scripts/validate_advisory_triage.py /private/path/advisory-triage.json
# Deterministic historical replay of an unassessed synthetic fixture:
python3 scripts/validate_advisory_triage.py templates/advisory-triage.example.json --as-of 2026-09-08
python3 -m unittest discover -s tests -p test_advisory_triage.py -v
# Complete repository gate, including advisory tests, from a full checkout:
python3 scripts/check_local.py
```

`--as-of` is explicitly historical replay, not a way to make expired evidence current. The synthetic example is `UNKNOWN / OPEN / NOT_TESTED`; its successful metadata check does not mean any deployed product was assessed. The ordinary local runner discovers these tests; no remote workflow or scheduler is invoked.

`--as-of` 明确用于历史回放，不能使过期证据重新有效。示例为 `UNKNOWN / OPEN / NOT_TESTED`，元数据校验成功不表示评估过实际产品。普通本地入口发现这些测试，不调用远端工作流或调度器。

### JSON contract / JSON 契约

All fields shown below are required, including nullable fields; unknown fields, duplicate JSON keys, duplicate record/evidence IDs and non-finite JSON constants are rejected. Dates are real `YYYY-MM-DD` calendar dates. Keep publication/revision ambiguity in the rationale and PR source trail rather than inventing a date.

下列字段全部必需，含允许 null 的字段；未知字段、重复 JSON 键、重复记录／证据 ID 和非有限 JSON 常量均被拒绝。日期必须是有效的 `YYYY-MM-DD`。发布／修订日期不明确时，保留理由及 PR 来源轨迹，不编造日期。

| Level / 层级 | Fields / 字段 | Meaning / 含义 |
|---|---|---|
| Document / 文档 | `format_version`, `reviewed_on`, `records` | Version string `"1"`; review date; nonempty record array / 版本字符串、复核日期、非空记录数组 |
| Record / 记录 | `id`, `product`, `source_url` | Unique ID, named product, HTTPS locator without embedded credentials / 唯一标识、产品、不含凭据的 HTTPS 来源 |
| Source / 来源 | `source_published_on`, `source_accessed_on` | Publication date or null with human explanation; access date / 发布日期或附人工说明的 null、访问日期 |
| Scope / 范围 | `scope`, `version_and_configuration` | Human-authored deployed-scope assertion, not automated discovery or version comparison / 人工范围断言，不自动发现资产或比较版本 |
| Decision / 判定 | `applicability`, `disposition` | Applicability `UNKNOWN`, `AFFECTED`, `NOT_AFFECTED`; disposition `OPEN`, `MITIGATED`, `REMEDIATED`, `NOT_APPLICABLE` |
| Ownership / 责任 | `owner`, `rationale`, `next_review_on` | Owner, documented reason, next review date / 责任人、理由、下一复核日期 |
| Evidence / 证据 | `evidence_ids`, `verification_result` | Evidence ID array; `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_TESTED` |
| Review / 验证 | `reviewer`, `verified_on`, `valid_until` | Reviewer and nullable verification/expiry dates / 验证人及可为空的验证、到期日期 |

Source access cannot follow review, and a known publication date cannot follow access. Review cannot be in the future; every next review must be strictly after the assessment date. A recorded PASS additionally requires known applicability, evidence IDs, an assigned owner and a distinct assigned reviewer, with:

```text
verified_on <= reviewed_on <= assessment_date < valid_until
assessment_date < next_review_on <= valid_until
```

来源访问不能晚于复核，已知发布日期不能晚于访问；复核不能在未来，每条记录的下一复核必须晚于评估日。记录 PASS 还要求已知适用性、证据 ID、已分配 Owner 和不同的已分配验证人，并满足以上日期关系。`valid_until` 是排除式边界：到该 UTC 日期开始即不再有效。

Non-PASS records must keep `verified_on` and `valid_until` null. `MITIGATED` and `REMEDIATED` require `AFFECTED` plus a current recorded PASS; `NOT_APPLICABLE` requires `NOT_AFFECTED` plus such a PASS. The latter concerns only the named advisory, not a control exemption. A missing publication date's explanation is a human review obligation; the checker cannot judge whether rationale text is adequate.

非 PASS 的验证／到期日期必须为 null；`MITIGATED`、`REMEDIATED` 要求 `AFFECTED` 与当前记录 PASS，`NOT_APPLICABLE` 要求 `NOT_AFFECTED` 与当前记录 PASS。后者只针对该公告，不产生控制豁免。缺失发布日期的解释须人工复核；工具不能判断理由文字是否充分。

The checker never fetches sources, validates evidence bytes, compares vendor versions, discovers exposure, proves reviewer independence or evaluates invalidation events. Reopen a decision after a relevant configuration, identity, artifact, advisory or scope change and independently retest. Even consistent, unexpired metadata can be false. Any applicable T0 without sufficient independent current evidence remains `NO_GO_NONCONFORMANT`.

校验器不拉取来源、不验证证据内容、不比较厂商版本、不发现暴露面、不证明人员独立性，也不判断失效事件。相关配置、身份、制品、公告或范围变化后，应重新开启判定并独立复测；一致且未到期的元数据仍可能不真实。适用 T0 缺乏充分、独立、当前证据时仍为 `NO_GO_NONCONFORMANT`。

Keep durable operating guidance in the [runbooks](en/VALIDATION_RUNBOOKS.md) / [验证手册](zh-CN/VALIDATION_RUNBOOKS.md), and follow [CONTRIBUTING](../CONTRIBUTING.md#recurring-research) for research and PR provenance.
