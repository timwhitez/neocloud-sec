# Governance / 治理规则

## 1. Purpose / 目的

NeoCloud Cyber Security is maintained as a project-authored, evidence-driven security baseline and reference framework. Changes must improve a defined security outcome, remain implementable, preserve bilingual meaning, and avoid turning documents, dashboards, or risk acceptance into unsupported proof of effectiveness.

NeoCloud Cyber Security 是一套由项目维护者编制、以证据为核心的安全基线与参考框架。任何变更都必须改善明确安全结果、能够落地、保持中英文含义一致，并避免把制度、Dashboard 或风险接受误当作控制有效的证明。

This project is not a standards-development organization, certification scheme, legal authority, or deployable security product. External-framework mappings and implementation examples are informative unless explicitly identified otherwise.

本项目不是标准制定组织、认证体系、法律权威或可直接部署的安全产品。除非明确说明，外部框架映射和实施示例均为参考性内容。

## 2. Applicability and authority / 适用性与权威关系

Applicable law, regulation, contract, privacy/safety obligations, and customer commitments determine external obligations. This baseline may be stricter than those obligations. Where an external obligation conflicts with this baseline, the organization must obtain qualified advice, document the conflict, and must not claim conformance to an unmet project requirement.

适用法律法规、合同、隐私/安全义务和客户承诺决定外部责任。本基线可能比外部最低要求更严格。若二者冲突，组织必须获取合格专业意见、记录冲突，并且不能把未满足的本项目要求声明为符合。

Within this project, use the following order when project materials conflict:

1. the normative machine-readable control catalog and its explicit invariants;
2. the English and Simplified Chinese security baselines, which must remain semantically aligned with the catalog;
3. service-specific applicability, threat models, shared-responsibility decisions, and evidence contracts;
4. the white paper, practice guide, reference architecture, roadmap, templates, and informative mappings.

项目内部发生冲突时，以机器可读规范控制目录及其明确不变量为最高依据；中英文安全基线必须与目录保持等义；随后是服务适用性、威胁模型、共享责任与证据契约；最后是白皮书、实践指南、参考架构、路线图、模板与参考映射。

## 3. T0 production gates and risk decisions / T0 生产硬门与风险决定

Every applicable T0 must be independently `VERIFIED` for a stated service, profile, environment, region, version, tenant/asset scope, test method, and evidence-validity period.

An applicable T0 that is failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` remains:

- `NO-GO` under this baseline;
- nonconformant;
- ineligible to be represented as `VERIFIED` or offset by an aggregate score.

A legally authorized executive may make a time-bounded emergency business-continuity or risk decision outside this baseline's conformance result. Such a decision must record the affected service and tenants, rationale, alternatives considered, customer/legal/privacy/safety impact, compensating controls, exposure window, monitoring, rollback/containment, notification decision, owner, expiry, and remediation deadline. It **does not** change the failed control result, create conformance, or permit a claim that the T0 gate passed.

每个适用 T0 都必须针对明确的服务、画像、环境、Region、版本、租户/资产范围、测试方法和证据有效期独立验证。失败、未知、过期、`INCONCLUSIVE` 或 `NOT_TESTED` 的适用 T0 始终保持 `NO-GO` 和不符合状态，不能被综合分数抵消。

高管可以在本基线符合性结论之外作出限时的紧急业务连续性或风险决定，但必须记录范围、理由、替代方案、客户/法律/隐私/安全影响、补偿控制、暴露窗口、监控、回滚/隔离、通知决定、Owner、到期和整改期限。该决定不会改变控制失败结果、不会形成符合状态，也不能支持“T0 已通过”的声明。

## 4. Change process / 变更流程

Every material change should be proposed through an issue or pull request containing:

- the threat, failure mode, factual error, or operating problem;
- affected control IDs, domains, service profiles, trust boundaries, and responsibility owners;
- proposed English and Simplified Chinese text;
- implementation guidance and provider/customer/shared responsibility;
- deployed-path assertion, minimum evidence, negative/failure test, independent validator, validity period, and revalidation trigger;
- migration, backward-compatibility, identifier, tier, schema, metric, template, and versioning impact;
- primary or authoritative sources with exact version/date and publication status;
- known limitations, uncertainty, and independent-review findings.

重大变更必须说明问题、影响范围、双语文本、责任、实施、证据、负向/失败测试、独立验证、有效期、迁移与版本影响、权威来源、局限和复核结论。

Do not copy proprietary standard text. A reference to an external framework does not prove compliance, exact equivalence, or deployed effectiveness.

不得复制专有标准正文。引用外部框架不能自动证明合规、精确等价或真实部署有效。

## 5. Versioning and identifiers / 版本与标识符

- Removing, renaming, or changing the meaning of a stable control ID or introducing an incompatible schema requires a major version.
- Adding backward-compatible normative controls or materially changing normative semantics normally requires a minor version.
- Non-breaking factual corrections, source-status updates, translation alignment, implementation clarification, repository metadata, and tooling fixes may use a patch version or remain under `Unreleased` until the next release.
- A release must state its exact catalog version, baseline date, publication status, scope, and known limitations.

删除、重命名或改变稳定 Control ID 含义，以及不兼容 Schema 变化，需要 Major；向后兼容的新规范控制或重大规范语义变化通常需要 Minor；非破坏性事实修正、来源状态、翻译校准、实施澄清、项目元数据和工具修复可以使用 Patch，或先记录在 `Unreleased`。

## 6. Control and assessment states / 控制与评估状态

Assessment work follows:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

- **PROPOSED:** the desired outcome exists, but scope, ownership, dependencies, evidence, or test requirements may be incomplete.
- **READY:** scope, accountable owner, dependencies, requirement, test, evidence contract, target date, and failure behavior are defined.
- **IMPLEMENTED:** the mechanism is deployed in the stated scope; effectiveness has not been independently established.
- **CANDIDATE_DONE:** the owner has supplied current evidence and asserts completion.
- **VERIFIED:** an independent validator returned `PASS` for the exact scope and evidence-validity period.

Verification results are `PASS`, `FAIL`, `INCONCLUSIVE`, and `NOT_TESTED`. Only `PASS` can create `VERIFIED`. A material change, incident, control failure, evidence expiry, scope conflict, or inability to reproduce the assertion invalidates the prior result and returns the control to the appropriate earlier state.

验证结果只有 `PASS`、`FAIL`、`INCONCLUSIVE` 和 `NOT_TESTED`；只有 `PASS` 能形成 `VERIFIED`。重大变更、事件、控制失效、证据到期、范围冲突或无法复现会使原结论失效。

## 7. Evidence and independence / 证据与独立性

Evidence must be:

- attributable to a control, assertion, service/profile, environment, version, asset/tenant scope, owner, collector, and observation time;
- derived from or demonstrably linked to the deployed path;
- reproducible or independently inspectable;
- protected against unauthorized alteration, with tamper evidence where appropriate;
- current under the control's validity period and invalidation triggers;
- explicit about sampling, exclusions, blind spots, assumptions, and exceptions;
- retained and shared according to security, privacy, contractual, forensic, and legal requirements.

A policy, interview, screenshot, scanner result, vendor dashboard, signature, or attestation may contribute evidence but is not automatically sufficient. High-impact assertions normally require a prohibited-path, failure, revocation, restore, rebuild, sanitization, or adversarial test appropriate to the claim.

证据必须可归因、关联真实部署、可复现或独立检查、受完整性保护、处于有效期内，并明确抽样、排除、盲点、假设和例外。Policy、访谈、截图、Scanner、厂商 Dashboard、签名或 Attestation 都可能构成证据，但不会自动充分；高影响断言通常还需要与声明匹配的负向、故障、撤销、恢复、重建、清除或对抗测试。

Independence means the validator can challenge the owner and does not rely solely on evidence or conclusions controlled by the implementer. A separate person, team, observation path, test harness, or qualified assessor may provide independence. An agent or automated control cannot be the sole verifier of its own work.

独立性意味着验证者能够挑战 Owner，并且不只依赖实施者控制的证据或结论。可以通过不同人员、团队、观察路径、测试 Harness 或合格评估方实现。Agent 或自动化控制不能成为自身工作的唯一验证者。

## 8. Agent and automation safety / Agent 与自动化安全

Every production AI system or agent must have an accountable owner, identity, declared use case, model/prompt/RAG/memory/skill/tool inventory, data and tenant scope, delegated authority, impact assessment, monitoring, and incident path.

Controls increase with authority and impact:

- low-impact assistive systems require inventory, data handling, output validation, and security-relevant audit;
- tool-using systems require typed interfaces, policy mediation, least privilege, short-lived credentials where feasible, egress/data/cost controls, and revocation;
- high-impact, destructive, external, customer-affecting, expensive, or irreversible actions require deterministic approval and explicit stop/containment behavior;
- adaptive or autonomous security workflows additionally require immutable goal/scope, protected and replayable action traces, budget/time/repetition/uncertainty stops, rollback or manual recovery, and an independent verifier the agent cannot alter.

每个生产 AI 系统或 Agent 都必须具备 Owner、Identity、Use Case、Model/Prompt/RAG/Memory/Skill/Tool 清单、Data/Tenant Scope、Delegated Authority、Impact Assessment、Monitoring 与 Incident Path。控制强度随权限和影响增加；只有高影响或自适应工作流才需要完整的确定性审批/停止、受保护可重放 Trace、回滚/人工恢复和 Agent 无法修改的独立 Verifier。

External content—including prompts, documents, tickets, web pages, packages, models, tool output, RAG data, and memory—provides observations, not authority. It cannot directly expand goal, scope, identity, credentials, policy, tools, approvals, budgets, evidence, or verifier authority.

外部 Prompt、文档、Ticket、网页、Package、Model、Tool Output、RAG Data 与 Memory 只能提供观察，不能直接扩大 Goal、Scope、Identity、Credential、Policy、Tool、Approval、Budget、Evidence 或 Verifier 权限。

Active testing requires explicit authorization, approved targets and methods, least privilege, bounded time and resources, isolation where practical, evidence handling, stop conditions, and an incident/rollback path.

## 9. Review and revalidation cadence / Review 与重验证频率

The default catalog cadence is:

| Tier | Default minimum |
|---|---|
| T0 | Continuous monitoring where feasible; independent verification at least quarterly and after material change |
| T1 | At least quarterly and after material change |
| T2 | At least semi-annually and after material change |
| T3 | At least annually, independently, and after material change |
| T4 | Continuous metrics plus quarterly adversarial and failure-mode review |

These are maximum default intervals, not a reason to delay verification. A shorter contractual, legal, threat-driven, evidence-expiry, release, or incident-triggered interval takes precedence.

默认频率为：T0 在技术可行时持续监控，至少每季度及重大变更后独立验证；T1 至少每季度；T2 至少每半年；T3 至少每年独立验证；T4 持续度量并至少每季度进行对抗与失败模式复核。合同、法律、威胁、证据到期、发布或事件要求更短时，以更短频率为准。

A material change includes a new service/SKU/region; isolation or sharing-mode change; controller, orchestrator, firmware, driver, model, agent, tool, policy, identity, key, data-flow, supplier, support, recovery, or evidence-pipeline change; control failure; incident; restore/rebuild; or inability to reproduce the prior assertion.

## 10. Maintainer and release principles / 维护与发布原则

- Prefer general mechanisms—identity, delegated authority, policy, isolation, provenance, evidence, recovery, feedback, and verification—over brittle one-off rules.
- Complexity must earn its operational and assurance cost.
- Distinguish project-authored requirements from externally mandated obligations.
- Distinguish final standards from drafts, public-review material, vendor guidance, and research.
- Distinguish deployment from effectiveness and risk acceptance from conformance.
- State uncertainty rather than manufacturing precision.
- Review the exact final commit after all requested changes are resolved.
- A release should not claim community consensus, formal-standard status, certification, public availability, or a deployable product unless those facts are true.

项目维护应优先采用通用机制，控制复杂度，区分项目要求与外部义务、正式标准与草案、部署与有效、风险接受与符合性；不确定时应明确表达，不得制造精确感。所有整改完成后必须复核准确的最终 Commit；只有事实成立时才能声明社区共识、正式标准、认证、公开发布或可部署产品。
