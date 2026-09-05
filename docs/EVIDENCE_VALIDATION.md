# Evidence-record validation / 证据记录校验

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
