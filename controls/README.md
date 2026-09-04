# NeoCloud Security Control Catalog / NeoCloud 安全控制目录

The files in this directory are the machine-readable source of truth for NeoCloud Cyber Security control IDs, tiers, bilingual requirements, evidence profiles, verification profiles, verification frequency, and metric associations.

本目录是 NeoCloud Cyber Security 控制 ID、等级、中英文要求、证据画像、验证画像、验证频率和度量关联的机器可读规范来源。

## Files / 文件

| File | Purpose |
|---|---|
| [`neocloud-security-baseline.v1.json`](neocloud-security-baseline.v1.json) | Normative bilingual catalog containing 18 domains and 90 controls / 包含 18 个安全域与 90 项控制的双语规范目录 |
| [`schema.json`](schema.json) | JSON Schema for structural validation / 用于结构校验的 JSON Schema |
| [`../scripts/validate_repository.py`](../scripts/validate_repository.py) | Standard-library semantic validator for count, IDs, cross-references, versions, baseline parity, and Markdown links / 校验数量、ID、引用、版本、基线一致性与 Markdown 链接的标准库脚本 |

## Normative rule / 规范规则

Every applicable **T0** control must be independently `VERIFIED`. A failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` T0 result is a production **NO-GO**. Aggregate scores cannot compensate for a failed T0.

每个适用 **T0** 控制都必须被独立验证为 `VERIFIED`。任何失败、未知、证据过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的 T0 都会产生生产 **NO-GO**。综合分数不能抵消 T0 失败。

Control completion follows:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

Only an independent validator returning `PASS` may assign `VERIFIED`.

只有独立验证者返回 `PASS`，控制才可进入 `VERIFIED`。

## Catalog structure / 目录结构

The catalog contains:

- version, date, status, languages, and normative rules;
- five adoption tiers and their default revalidation frequencies;
- eight NeoCloud service profiles;
- reusable minimum-evidence and verification profiles;
- metric IDs linked to the bilingual metrics guides;
- 18 bilingual domain definitions;
- exactly 90 controls, each with:
  - stable ID and domain;
  - tier;
  - English and Chinese title;
  - English and Chinese normative requirement;
  - minimum-evidence profile;
  - independent-verification profile;
  - metric associations.

目录包括：

- 版本、日期、状态、语言与规范规则；
- 五级采用模型及默认重验证频率；
- 八类 NeoCloud 服务画像；
- 可复用的最低证据与验证画像；
- 关联中英文度量指南的 Metric ID；
- 18 个双语安全域定义；
- 严格 90 项控制，每项均包含稳定 ID、安全域、等级、中英文标题、中英文规范要求、最低证据画像、独立验证画像和度量关联。

## Validation / 校验

Run from the repository root:

```bash
python3 scripts/validate_repository.py
```

The validator fails when it finds, among other conditions:

- invalid JSON or unsupported version/date syntax;
- a domain count other than 18 or a control count other than 90;
- duplicate, malformed, missing, or unexpected control IDs;
- control/domain prefix mismatch;
- missing bilingual title or requirement;
- missing evidence, verification, tier, or metric reference;
- divergence between the English and Chinese baseline control IDs;
- missing repository deliverables or broken relative Markdown links;
- version inconsistency between `VERSION`, README files, catalogs, and primary documents.

校验器会在以下情况失败：JSON 无效、版本/日期格式错误、安全域或控制数量错误、ID 重复或缺失、Domain Prefix 不一致、双语字段缺失、Evidence/Verification/Tier/Metric 引用悬空、中英文基线 ID 不一致、交付物缺失、相对 Markdown 链接失效，或关键文档版本不一致。

No third-party Python package is required. CI runs the same validator for pull requests and the default branch.

该校验不依赖第三方 Python 包；CI 会在 Pull Request 和默认分支上运行同一脚本。

## Common queries / 常用查询

List all T0 controls:

```bash
jq -r '.controls[] | select(.tier == "T0") | [.id, .title.en, .title["zh-CN"]] | @tsv' \
  controls/neocloud-security-baseline.v1.json
```

List controls in one domain:

```bash
jq -r '.controls[] | select(.domain == "CMP") | [.id, .tier, .title.en] | @tsv' \
  controls/neocloud-security-baseline.v1.json
```

Show a control with its resolved evidence and verification profiles:

```bash
jq --arg id "NCS-CMP-02" '
  . as $root
  | .controls[]
  | select(.id == $id)
  | . + {
      minimum_evidence: $root.evidence_profiles[.evidence_profile],
      verification: $root.verification_profiles[.verification_profile],
      frequency: $root.tiers[.tier]
    }
' controls/neocloud-security-baseline.v1.json
```

Count controls by tier:

```bash
jq -r '.controls | group_by(.tier)[] | "\(.[0].tier)\t\(length)"' \
  controls/neocloud-security-baseline.v1.json
```

Expected distribution for `1.0.0-draft.2`:

```text
T0  32
T1  31
T2  19
T3   7
T4   1
```

## Change rules / 变更规则

Control changes follow [`GOVERNANCE.md`](../GOVERNANCE.md). A control change must update all affected bilingual text, evidence and verification profiles, metrics, primary documentation, templates, tests, version metadata, and changelog. External-framework mappings remain informative and require independent validation for the exact framework version, service, jurisdiction, and audit objective.

控制变更遵循 [`GOVERNANCE.md`](../GOVERNANCE.md)。变更时必须同步中英文内容、证据与验证画像、指标、主文档、模板、校验、版本元数据和 Changelog。外部框架映射仅供参考，正式审计前仍需针对框架版本、具体服务、司法辖区和审计目标独立验证。
