# NeoCloud Security Control Catalog / NeoCloud 安全控制目录

The files in this directory are the machine-readable source of truth for NeoCloud Cyber Security control IDs, tiers, bilingual requirements, evidence profiles, verification profiles, default revalidation frequency, and metric associations.

本目录是 NeoCloud Cyber Security 控制 ID、等级、中英文要求、证据画像、验证画像、默认重验证频率和度量关联的机器可读规范来源。

## Files / 文件

| File | Purpose |
|---|---|
| [`neocloud-security-baseline.v1.json`](neocloud-security-baseline.v1.json) | Normative bilingual catalog containing 18 domains and 90 controls / 包含 18 个安全域与 90 项控制的双语规范目录 |
| [`schema.json`](schema.json) | JSON Schema for structural validation / 用于结构校验的 JSON Schema |
| [`../scripts/validate_repository.py`](../scripts/validate_repository.py) | Standard-library validator for catalog semantics, exact IDs and counts, cross-references, bilingual baseline/metric parity, release versions, required deliverables, and Markdown links / 校验目录语义、精确 ID/数量、交叉引用、中英文基线与指标一致性、版本、必需交付物和 Markdown 链接 |

## Normative rule / 规范规则

Every applicable **T0** control must be independently `VERIFIED`. A failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` T0 result is **NO-GO (`NO_GO_NONCONFORMANT`)**. An aggregate score, compensating control, exception, risk acceptance, or emergency business decision cannot change the control result or support a conformance claim.

每个适用 **T0** 控制都必须被独立验证为 `VERIFIED`。任何失败、未知、证据过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的 T0 均为 **NO-GO（`NO_GO_NONCONFORMANT`）**。综合分数、补偿控制、例外、风险接受或紧急业务决定都不能改变控制结果，也不能支持符合性声明。

Control completion follows:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

`IMPLEMENTED` establishes deployment only. Only an independent validator returning `PASS` for the exact service/profile, environment, version, tenant/asset scope, test, evidence, and validity period may assign `VERIFIED`.

`IMPLEMENTED` 只证明已经部署。只有独立验证者针对准确的 Service/Profile、Environment、Version、Tenant/Asset Scope、Test、Evidence 与 Validity Period 返回 `PASS`，才能进入 `VERIFIED`。

## Catalog structure / 目录结构

The catalog contains:

- version, evidence cut-off, status, languages, and normative rules;
- five adoption tiers and their default revalidation frequencies;
- eight NeoCloud service profiles;
- reusable minimum-evidence and independent-verification profiles;
- stable metric IDs linked to the bilingual metrics guides;
- 18 bilingual domain definitions;
- exactly 90 controls, each with:
  - stable ID and domain;
  - tier;
  - English and Chinese title;
  - English and Chinese normative requirement;
  - minimum-evidence profile;
  - independent-verification profile;
  - metric associations.

目录包括版本、资料核验截止日期、状态、语言与规范规则，五级采用模型及默认复核频率，八类服务画像，可复用证据/独立验证画像，稳定 Metric ID，18 个双语安全域，以及严格 90 项控制。

## Validation / 校验

Run from the repository root:

```bash
python3 scripts/validate_repository.py
```

The validator fails when it finds, among other conditions:

- invalid JSON or unsupported version/date syntax;
- an unexpected project status or incomplete T0 decision invariant;
- a domain count other than 18, a control count other than 90, or an altered tier distribution;
- duplicate, malformed, missing, unexpected, or domain-mismatched control IDs;
- missing bilingual title or normative requirement;
- missing evidence, verification, tier, or metric references;
- divergence between the catalog and either language baseline;
- missing or duplicate catalog-linked metric IDs in either language metrics guide;
- missing required repository deliverables or broken relative Markdown links;
- version inconsistency between `VERSION`, README files, catalog, and primary documents.

校验器会在 JSON/版本/日期无效、项目状态或 T0 不变量不完整、安全域/控制/Tier 数量变化、Control ID 错误、双语字段缺失、引用悬空、目录与双语基线不一致、中英文指标缺失或重复、交付物/链接缺失、版本不一致时失败。

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

Show a control with resolved evidence, verification, and tier frequency:

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

Expected distribution for `1.0.0-draft.1`:

```text
T0  32
T1  31
T2  19
T3   7
T4   1
```

## Interpretation safeguards / 解释边界

- Full-device dedication, hardware partitioning, virtualization, and time-slicing are separate products. Time-slicing is not a memory- or fault-isolation boundary; hardware partitioning is not full-device or full-host dedication.
- Identity may persist; credentials, sessions, privilege grants, and delegated authority should be short-lived where technically feasible.
- Signatures and attestations support specific claims. They do not automatically establish safe source, runtime behavior, deployed effectiveness, or complete isolation.
- Every production AI system or agent requires ownership, identity, scope, component inventory, monitoring, and incident handling. Stronger tool, approval, stop, trace, rollback, and verifier controls apply according to authority and impact.
- Unknown critical scope remains a failed assertion and must not disappear from a denominator.

- 整卡、硬件分区、虚拟化与 Time-slicing 是不同产品；Time-slicing 不提供显存/故障隔离，硬件分区也不等于整卡/整机专属。
- Identity 可以长期存在；在技术可行时，Credential、Session、Privilege Grant 与 Delegated Authority 应短期化。
- Signature 与 Attestation 只能支持具体 Claim，不能自动证明来源、Runtime、安全效果或完整隔离。
- 每个生产 AI System/Agent 都必须具备 Owner、Identity、Scope、Component Inventory、Monitoring 与 Incident Handling；更强 Tool/Approval/Stop/Trace/Rollback/Verifier 控制随权限和影响增加。
- 未知关键范围仍然属于失败，不能从指标分母中消失。

## Change rules / 变更规则

Control changes follow [`GOVERNANCE.md`](../GOVERNANCE.md). A change must update all affected bilingual text, evidence and verification profiles, metrics, primary documentation, templates, tests, version metadata, and changelog. External-framework mappings remain informative and require independent validation for the exact framework version, service, jurisdiction, contract, deployment, and audit objective.

控制变更遵循 [`GOVERNANCE.md`](../GOVERNANCE.md)。变更时必须同步中英文内容、证据/验证画像、指标、主文档、模板、校验、版本元数据和 Changelog。外部框架映射仅供参考，正式采用前仍需针对准确框架版本、服务、司法辖区、合同、部署与审计目标独立验证。
