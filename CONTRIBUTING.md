# Contributing / 贡献指南

Contributions are welcome when they make NeoCloud security more accurate, implementable, measurable, or easier to verify.

欢迎能够提高 NeoCloud 安全内容准确性、可落地性、可度量性或可验证性的贡献。

## 1. Choose the right path / 选择正确入口

- Use the **factual-correction issue form** for inaccurate claims, stale references, broken links, unclear terminology, or English/Chinese semantic drift.
- Use the **control-change issue form** for normative controls, tiers, service profiles, evidence, verification, metrics, or compatibility changes.
- Open a pull request for a concrete, reviewable correction or implementation improvement.
- Follow [`SECURITY.md`](SECURITY.md) for live credentials, customer data, private evidence, exploitable repository behavior, or other security-sensitive reports. Never place such material in a public issue or pull request.

普通事实修正、过期引用、失效链接、术语和中英文含义漂移，请使用 factual-correction 表单；控制、等级、服务画像、证据、验证、指标或兼容性变更，请使用 control-change 表单；安全敏感问题遵循 [`SECURITY.md`](SECURITY.md)。

## 2. Requirements for normative changes / 规范性变更要求

A pull request that changes normative content must include:

1. the threat, failure mode, or operating problem;
2. affected control IDs, domains, service profiles, trust boundaries, and provider/customer/shared owners;
3. English and Simplified Chinese text with equivalent normative meaning;
4. implementation guidance that remains vendor-neutral unless explicitly scoped otherwise;
5. the deployed-path assertion, minimum evidence, prohibited-path or failure test, independent validator, validity period, and revalidation triggers;
6. compatibility, migration, control-ID, tier, schema, template, metric, and versioning impact;
7. primary or authoritative sources, including exact version/date and whether each source is final, draft, public review, superseded, or vendor-specific;
8. self-review findings and a separate review of the exact final commit.

规范性 PR 必须说明威胁或运营问题、影响范围与责任、中英文等义文本、落地方法、证据与负向/失败测试、独立验证、有效期、兼容性与版本影响、权威来源，以及针对最终 Commit 的独立复核。

Do not copy proprietary standard text. Summarize the outcome in original language and link to the authoritative source. Framework mappings are informative unless an exact mapping has been independently validated for the named version, service, jurisdiction, contract, and audit objective.

不得复制专有标准正文。应使用原创语言概括安全结果，并链接到权威来源。除非针对明确版本、服务、司法辖区、合同和审计目标完成独立验证，否则框架映射只能作为参考。

## 3. Normative language / 规范语言

- **MUST / 必须** — mandatory for an applicable scope.
- **SHOULD / 应该** — a strong recommendation; omission requires a documented rationale and residual-risk owner.
- **MAY / 可以** — an implementation option.

Requirements must be testable. Avoid marketing language, absolute guarantees, unsupported maturity claims, and terms such as “dedicated,” “isolated,” “zero trust,” “confidential,” “immutable,” or “complete” unless the exact boundary and evidence are stated.

要求必须可测试。避免营销化、绝对保证和无依据成熟度声明；使用“专属”“隔离”“零信任”“机密”“不可变”“完整”等词时，必须同时说明精确边界和证据。

## 4. T0 and assurance invariants / T0 与保证不变量

- Every applicable T0 must be independently `VERIFIED` for the stated service scope and evidence-validity period.
- Failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` T0 evidence remains `NO-GO` and nonconformant.
- A business-risk decision or emergency exception may document why an operator proceeded, but it cannot change the control result, create `VERIFIED` status, or support a conformance claim.
- `IMPLEMENTED` describes deployment; it does not establish effectiveness.
- An implementer, control owner, automated system, or agent cannot be the sole verifier of its own result.

每个适用 T0 都必须被独立验证；风险接受或紧急业务决定不能把失败 T0 变成 `VERIFIED` 或符合项；部署不等于有效；实施者、Owner、自动化或 Agent 不能成为自身结果的唯一验证者。

## 5. Local validation / 本地校验

Run the repository contract validator from the repository root:

```bash
python3 scripts/validate_repository.py
```

The validator checks required deliverables, JSON validity, the exact domain/control/tier contract, control IDs, bilingual baseline parity, evidence/verification/metric references, release-version consistency, and relative Markdown links.

校验器检查必需交付物、JSON、严格的安全域/控制/等级契约、Control ID、中英文基线一致性、证据/验证/指标引用、版本一致性和相对 Markdown 链接。

Include the exact output in the pull request template. The same command runs in GitHub Actions. Passing automation is necessary but not sufficient: reviewers must still check technical truth, source status, service applicability, bilingual meaning, and whether evidence can prove the deployed outcome.

PR 中应粘贴最终 Commit 的校验输出。GitHub Actions 会运行同一命令；自动校验通过只是必要条件，仍需人工复核技术事实、来源状态、服务适用性、中英文含义及证据能否证明真实部署结果。

## 6. Review and versioning / Review 与版本管理

- Review the exact head commit after all requested changes are resolved.
- Normative changes require an independent reviewer or a clearly documented separate review pass.
- Breaking control-ID or schema changes require a major version.
- Backward-compatible normative controls or material semantics normally require a minor version.
- Editorial, factual, reference-status, or non-breaking clarification may use a patch version or remain in `Unreleased` until the next release.
- Update all affected bilingual documents, catalog fields, templates, metrics, references, validation logic, version metadata, and changelog together.

所有整改完成后，应对准确的 Head Commit 重新 Review。破坏性 ID/Schema 变化使用 Major；向后兼容的规范控制或重大语义变化通常使用 Minor；编辑、事实、来源状态与非破坏性澄清可以使用 Patch，或先记录在 `Unreleased`。

## 7. Repository and license status / 仓库与 License 状态

The repository currently grants no open-source license. Do not infer permission to reuse or redistribute content merely from repository access. Before public contribution or release, the owner should adopt an explicit license and contribution policy; options are documented in [`.github/REPOSITORY_SETTINGS.md`](.github/REPOSITORY_SETTINGS.md).

本仓库当前没有授予开源许可证。能够访问仓库不等于自动获得复用或再分发授权。对外开放贡献或发布前，Owner 应明确 License 与贡献许可；建议方案见 [`.github/REPOSITORY_SETTINGS.md`](.github/REPOSITORY_SETTINGS.md)。
