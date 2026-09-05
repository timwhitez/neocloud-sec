# Control catalogs / 控制目录

**Base:** 1.0.0-draft.1 · **Public-findings profile:** 1.0.1

| File | Role |
|---|---|
| [neocloud-security-baseline.v1.json](neocloud-security-baseline.v1.json) | 18 domains, 90 stable bilingual controls |
| [schema.json](schema.json) | Base-catalog JSON Schema |
| [neocloud-security-baseline.v1.errata.json](neocloud-security-baseline.v1.errata.json) | Normative correction to CMP-02; apply before use |
| [Errata schema](neocloud-security-baseline.v1.errata.schema.json) | Allowed correction structure |
| [semianalysis-public-findings-profile.v1.json](semianalysis-public-findings-profile.v1.json) | 40 project mappings and 20 dated public-page mappings; not a provider rating |
| [Profile schema](semianalysis-public-findings-profile.v1.schema.json) | Structural requirements; semantic joins also checked in code |

## Effective requirements / 有效要求

The raw base file and applicable errata jointly define requirements. Do not use a raw CMP-02 requirement while ignoring the correction. Generate a derived bundle:

原始目录与适用勘误共同定义要求，不能读取原始 CMP-02 却忽略勘误。生成派生 Bundle：

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

The bundle's `catalog` is a copy with validated replacements. `provenance` contains input digests, applied erratum IDs and an output digest. IDs and tiers do not change. Unknown targets, repeated targets and version mismatches are errors. This is deterministic document transformation, not provider assurance.

`catalog` 是已应用勘误的副本；`provenance` 包含输入摘要、勘误 ID 与输出摘要。ID 和等级不变，未知目标、重复目标和版本不一致会报错。这是确定性文档转换，不是服务商安全证明。

## Queries / 查询

List T0 controls from the effective bundle:

```bash
jq -r '.catalog.controls[] | select(.tier == "T0") | [.id, .title.en, .title["zh-CN"]] | @tsv' /tmp/neocloud-effective-catalog.json
```

Resolve a control's evidence and verification references:

```bash
jq --arg id 'NCS-CMP-02' '.catalog as $c | $c.controls[] | select(.id == $id) | . + {evidence: $c.evidence_profiles[.evidence_profile], verification: $c.verification_profiles[.verification_profile]}' /tmp/neocloud-effective-catalog.json
```

The base tier distribution remains T0=32, T1=31, T2=19, T3=7, T4=1. An applicable failed, unknown, stale, inconclusive or untested T0 remains `NO_GO_NONCONFORMANT`. Only scoped independent `PASS` can support `VERIFIED`; a risk decision cannot fabricate a passing result.

基础等级分布不变。适用 T0 的失败、未知、过期、无法判断或未测试都不能被综合分数或风险接受覆盖。只有范围明确的独立 `PASS` 才能支持 `VERIFIED`。

## Validation / 校验

```bash
python3 scripts/check_local.py
```

The two legacy validators remain standard-library scripts. The strict profile checker uses the declared jsonschema dependency and actually evaluates base, profile and errata schemas. It checks duplicate JSON keys, invalid dates, incomplete source references, record/count disagreement, CSV shape and exact mapping joins. Repository templates remain unassessed. Missing required inputs or dependencies fail rather than being silently skipped.

前两项旧校验使用标准库。严格画像校验显式依赖 jsonschema，实际评估基础目录、画像与勘误 Schema，并检查重复 JSON 字段、无效日期、来源引用、统计矛盾、CSV 列结构与映射。仓库模板保持未评估，缺少输入或依赖时失败退出。

## Interpretation / 解释

Scheduler-level GPU device-plugin time-slicing is not memory/fault isolation. Hypervisor-mediated vGPU, hardware partitioning and full-device dedication are separate mechanisms requiring version-specific evidence. Key values, labels, signatures, attestations and dashboards support limited claims; none alone proves complete tenant isolation.

调度器级 Device Plugin Time-slicing 不等于显存/故障隔离；Hypervisor 仲裁的 vGPU、硬件分区、整卡独占是不同机制，均需版本特定证据。密钥值、标签、签名、证明和 Dashboard 都只能支持有限声明，不能单独证明完整租户隔离。

See [governance](../GOVERNANCE.md), [English drill guide](../docs/en/SEMIANALYSIS_COVERAGE.md), [中文验证指南](../docs/zh-CN/SEMIANALYSIS_COVERAGE.md) and the [scoped audit](../reviews/2026-09-05-validation-audit.md). Keep normative changes, translations, schemas, templates, tests and source/version notes aligned.
