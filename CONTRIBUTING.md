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

Run the complete local entry point from a full checkout with the declared dependencies installed:

```bash
python3 scripts/check_local.py
```

The runner executes the three repository validators and discovers unit tests, including advisory and documentation regressions. The core validator checks required deliverables, JSON validity, the exact domain/control/tier contract, control IDs, bilingual baseline parity, evidence/verification/metric references, release-version consistency, and relative Markdown links.

本地入口运行三项仓库校验并发现单元测试，包含公告与文档回归；核心校验器检查必需交付物、JSON、严格的安全域/控制/等级契约、Control ID、中英文基线一致性、证据/验证/指标引用、版本一致性和相对 Markdown 链接。

Include the exact tested head, commands, output and omissions in the PR. The workflow is manual-dispatch only while Actions quota is constrained: do not dispatch or rerun it. Keep `[skip ci]` in commit/merge messages. A partial checkout is not a full-suite pass. Passing automation is necessary but not sufficient: reviewers must still check technical truth, source status, service applicability, bilingual meaning, and whether evidence can prove the deployed outcome.

PR 应记录准确测试 Head、命令、输出及未执行项目。额度受限期间工作流仅手动触发，本轮不得调度或重跑；Commit/合并信息保留 `[skip ci]`。部分检出不等于全套测试通过；自动校验通过只是必要条件，仍需人工复核技术事实、来源状态、服务适用性、中英文含义及证据能否证明真实部署结果。

<a id="recurring-research"></a>
## 6. Recurring research is project maintenance / 持续研究就是项目迭代

Record the base commit, timezone, calendar-week start/end and evidence cutoff in the normal PR or Issue. Separate this week's publications, revisions, older lookback findings and future deadlines. For consequential claims, record the primary URL, publication/revision/access dates, product/version/configuration, source status and retrieval limitations. Cross-check with a product release, upstream advisory or another primary authority. Syndication is not independent corroboration; retain unresolved chronology or applicability instead of guessing.

在普通 PR／Issue 中记录基准提交、时区、自然周起止与证据截止；区分本周发布、本周修订、历史回溯及未来期限。关键结论记录一手链接、发布／修订／访问日期、产品版本配置、来源状态和读取局限，使用产品发布、上游公告或另一一手权威交叉验证；转载不是独立证据，时间或适用性冲突应保留。

Review supply chain, IAM/API, network/fabric, host/GPU/virtualization, containers/Kubernetes/Slurm, data/keys, telemetry/detection, governance/compliance, abuse and response/recovery. Compare each area with the actual catalog, errata and implementation before declaring a gap. Record one disposition per area: actionable change, already covered, watch pending evidence, or out of scope. No confirmed new event does not prove that no vulnerability exists.

逐域检查供应链、IAM/API、网络/Fabric、Host/GPU/虚拟化、容器/Kubernetes/Slurm、数据/密钥、监控检测、治理合规、滥用与应急恢复。先对照真实目录、勘误和实现，再判定缺口；记录可执行改动、已有覆盖、待证据跟踪或不适用，不能把“未发现新公告”写成“没有漏洞”。

Put durable guidance into the existing bilingual practice guide, architecture or [validation runbooks](docs/en/VALIDATION_RUNBOOKS.md); update affected controls, templates and tests only when needed. Keep references inline and in [REFERENCES.md](REFERENCES.md), and record user-facing changes in [CHANGELOG.md](CHANGELOG.md). Keep the optional advisory format in [evidence validation](docs/EVIDENCE_VALIDATION.md). The PR/Issue carries the dated research and decision trail; do not create a parallel weekly guide, addendum, report series or control catalog. Preserve useful sources and decisions before removing redundant material; use Git history and the original PR for historical provenance.

持久建议直接进入已有中英文实践指南、架构或[验证手册](docs/zh-CN/VALIDATION_RUNBOOKS.md)，按需同步控制、模板和测试；来源保留在正文与 REFERENCES，用户可见变化记入普通 CHANGELOG，公告格式归入已有证据校验文档。日期化研究及决策过程留在 PR／Issue，不另建周更指南、补充文档、报告系列或平行控制目录。移除重复内容前保留有效来源与决策，历史追溯使用 Git 历史及原 PR。

Prefer the smallest enforceable improvement: a corrected boundary, example, evidence contract or safe allow/deny test. Prioritize actual exposure, affected configuration, active exploitation when supported, tenant-boundary failures and privileged control planes rather than CVSS or novelty alone. Do not require a vendor, new platform, CNI, beta feature or agent framework merely because it is recent. A no-change result is valid when evidence supports it.

优先补齐最小可执行改进：边界、示例、证据契约或安全的允许／拒绝测试。依据实际暴露、受影响配置、有证据的在野利用、租户边界及特权控制面排序，而非只看 CVSS 或热度；不能仅因新发布就要求引入厂商、平台、CNI、Beta 功能或 Agent 框架。有依据的“无需改动”也是有效结果。

Reuse an existing Issue; create one only when distinct tracking is useful. Open a focused PR, review/test the final head and recheck base/head before merging. Do not merge when required validation fails or cannot be completed; explain the remaining gate without weakening it. Never force-push or bypass branch rules. Every run reports new practices, gaps, Issue/PR links, actual tests, merged content, unmerged reasons and next watch items. Keep real assets, credentials and evidence private. A documentation change is not infrastructure remediation, and these instructions install no scheduler or background job.

Distinguish vendor capabilities, single vulnerability events, draft standards and final generally applicable requirements before promoting any of them into normative text; a new normative requirement follows section 2. Follow section 5 for local validation of every research-driven change.

优先复用 Issue，确有独立跟踪价值才新建。通过聚焦 PR 变更，对最终 Head 审查测试，合并前复查 Base/Head；必需验证失败或无法完成时不合并，明确剩余门槛而非降低门槛。不强推、不绕过分支规则。每轮报告新增实践、缺口、Issue/PR、真实测试、已合并内容、未合并原因与后续关注点。真实资产、凭据和证据留在私有系统；文档变更不代表基础设施已修复，本流程不安装调度器或后台任务。

把厂商能力、单个漏洞事件、标准草案与正式通用要求区分开，再决定是否写入规范文本；新增规范要求遵循第 2 节。每轮研究产生的改动均按第 5 节执行本地校验。

## 7. Review and versioning / Review 与版本管理

- Review the exact head commit after all requested changes are resolved.
- Normative changes require an independent reviewer or a clearly documented separate review pass.
- Breaking control-ID or schema changes require a major version.
- Backward-compatible normative controls or material semantics normally require a minor version.
- Editorial, factual, reference-status, or non-breaking clarification may use a patch version or remain in `Unreleased` until the next release.
- Update all affected bilingual documents, catalog fields, templates, metrics, references, validation logic, version metadata, and changelog together.

所有整改完成后，应对准确的 Head Commit 重新 Review。破坏性 ID/Schema 变化使用 Major；向后兼容的规范控制或重大语义变化通常使用 Minor；编辑、事实、来源状态与非破坏性澄清可以使用 Patch，或先记录在 `Unreleased`。

## 8. Repository and license status / 仓库与 License 状态

The repository currently grants no open-source license. Do not infer permission to reuse or redistribute content merely from repository access. Before public contribution or release, the owner should adopt an explicit license and contribution policy; options are documented in [`.github/REPOSITORY_SETTINGS.md`](.github/REPOSITORY_SETTINGS.md).

本仓库当前没有授予开源许可证。能够访问仓库不等于自动获得复用或再分发授权。对外开放贡献或发布前，Owner 应明确 License 与贡献许可；建议方案见 [`.github/REPOSITORY_SETTINGS.md`](.github/REPOSITORY_SETTINGS.md)。
