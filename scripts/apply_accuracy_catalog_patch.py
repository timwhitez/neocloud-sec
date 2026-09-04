#!/usr/bin/env python3
"""Apply exact, asserted non-breaking accuracy corrections to the draft catalog.

This one-shot script is committed only long enough for an authenticated branch
workflow to apply deterministic replacements to a file too large for the
repository connector's whole-file update interface. The workflow removes both
itself and this script in the same patch commit.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one occurrence in {path.relative_to(ROOT)}; found {count}: {old[:120]!r}"
        )
    path.write_text(text.replace(old, new), encoding="utf-8")


catalog = ROOT / "controls" / "neocloud-security-baseline.v1.json"

catalog_replacements = [
    (
        '  "status": "implementation-oriented public draft",',
        '  "status": "implementation-oriented project draft",',
    ),
    (
        '    "t0_gate": "Every applicable T0 control must be independently VERIFIED. Failed, unknown, inconclusive, untested, or stale T0 evidence produces NO-GO.",',
        '    "t0_gate": "Every applicable T0 control must be independently VERIFIED. Failed, unknown, inconclusive, untested, or stale T0 evidence produces NO_GO_NONCONFORMANT; a business-risk decision cannot change the control result.",',
    ),
    (
        '    "t0_gate_zh_CN": "每个适用 T0 控制都必须被独立验证为 VERIFIED；失败、未知、无法判定、未测试或证据过期均产生 NO-GO。",',
        '    "t0_gate_zh_CN": "每个适用 T0 控制都必须被独立验证为 VERIFIED；失败、未知、无法判定、未测试或证据过期均产生 NO_GO_NONCONFORMANT，业务风险决定不能改变控制结果。",',
    ),
    (
        '    "EP-AGENT": {"minimum_evidence_en": ["agent identity, delegator, immutable goal/scope, model/prompt/skill/tool versions", "typed tool, policy, approval, budget, stop, and trace records", "prompt-injection, confused-deputy, scope, stop, and independent-verifier tests"], "minimum_evidence_zh_CN": ["Agent 身份、委托方、不可变 Goal/Scope 以及 Model/Prompt/Skill/Tool 版本", "Typed Tool、策略、审批、预算、停止与 Trace 记录", "Prompt Injection、Confused Deputy、Scope、Stop 与独立 Verifier 测试"]},',
        '    "EP-AGENT": {"minimum_evidence_en": ["agent owner, identity, delegator, use case, impact, data/tenant/authority scope, and versioned model/prompt/RAG/memory/skill/tool inventory", "for tool-using systems: typed tool, policy, credential, egress/data/cost, revocation, and security-relevant trace records", "for high-impact or adaptive systems: deterministic approval/stop, protected replayable trace, rollback/manual recovery, and independent-verifier test results"], "minimum_evidence_zh_CN": ["Agent Owner、Identity、Delegator、Use Case、Impact、Data/Tenant/Authority Scope，以及版本化 Model/Prompt/RAG/Memory/Skill/Tool Inventory", "对 Tool-using System：Typed Tool、Policy、Credential、Egress/Data/Cost、Revocation 与安全相关 Trace Record", "对高影响或自适应系统：Deterministic Approval/Stop、受保护可重放 Trace、Rollback/Manual Recovery 与 Independent-verifier Test Result"]},',
    ),
    (
        '    "VP-DATA-SUPPLY": {"steps_en": ["trace a representative object from source to use and disposal", "attempt unauthorized, unsigned, malicious, revoked, or expired handling", "verify recall, rollback, deletion, or recovery"], "steps_zh_CN": ["跟踪代表性对象从来源到使用与处置", "尝试未授权、未签名、恶意、已吊销或过期处理", "验证召回、回滚、删除或恢复"]},',
        '    "VP-DATA-SUPPLY": {"steps_en": ["trace a representative object from source to use and disposal", "attempt unauthorized, unsigned-when-required, malicious, revoked, incompatible, or expired handling", "verify recall, rollback, deletion, or recovery"], "steps_zh_CN": ["跟踪代表性对象从来源到使用与处置", "尝试未授权、在要求签名时未签名、恶意、已吊销、不兼容或过期处理", "验证召回、回滚、删除或恢复"]},',
    ),
    (
        '    "VP-AGENT": {"steps_en": ["freeze identity, delegation, goal, scope, tools, budget, and verifier", "test untrusted-content, approval, scope, cost, repetition, and destructive-action boundaries", "confirm deterministic stop, complete trace, and independent verdict"], "steps_zh_CN": ["冻结身份、委托、Goal、Scope、Tool、Budget 与 Verifier", "测试不可信内容、审批、范围、成本、重复和破坏性动作边界", "确认确定性停止、完整 Trace 与独立结论"]},',
        '    "VP-AGENT": {"steps_en": ["confirm owner, identity, delegation, use case, impact, components, data/tenant/authority scope, monitoring, and incident path", "for tool-using or high-impact systems, test untrusted content, approval, scope, egress/data/cost, credential revocation, repeated failure, and destructive-action boundaries", "where applicable, confirm deterministic stop, rollback/manual recovery, protected trace, and independent verdict"], "steps_zh_CN": ["确认 Owner、Identity、Delegation、Use Case、Impact、Component、Data/Tenant/Authority Scope、Monitoring 与 Incident Path", "对 Tool-using 或高影响系统，测试不可信内容、Approval、Scope、Egress/Data/Cost、Credential Revocation、Repeated Failure 与 Destructive-action Boundary", "在适用时确认 Deterministic Stop、Rollback/Manual Recovery、Protected Trace 与 Independent Verdict"]},',
    ),
    (
        '    {"id": "IAM", "title": {"en": "Human, tenant, workload, and agent identity", "zh-CN": "人员、租户、工作负载与 Agent 身份"}, "outcome": {"en": "Every acting subject has a strong, scoped, short-lived, and reviewable identity.", "zh-CN": "每个行动主体都具有强、受限、短期且可复核的身份。"}},',
        '    {"id": "IAM", "title": {"en": "Human, tenant, workload, and agent identity", "zh-CN": "人员、租户、工作负载与 Agent 身份"}, "outcome": {"en": "Every acting subject has a strong, scoped, and reviewable identity; credentials, sessions, privilege grants, and delegated authority are short-lived where technically feasible.", "zh-CN": "每个行动主体都具有强、受限且可复核的身份；在技术可行时，Credential、Session、Privilege Grant 与 Delegated Authority 应短期化。"}},',
    ),
    (
        '    {"id": "TEL", "title": {"en": "Telemetry, detection engineering, threat intelligence, and audit", "zh-CN": "遥测、检测工程、威胁情报与审计"}, "outcome": {"en": "Complete, tenant-safe, tamper-resistant evidence and detections tested against relevant threats.", "zh-CN": "证据完整、租户安全、抗篡改，检测经过相关威胁验证。"}},',
        '    {"id": "TEL", "title": {"en": "Telemetry, detection engineering, threat intelligence, and audit", "zh-CN": "遥测、检测工程、威胁情报与审计"}, "outcome": {"en": "Required, tenant-safe, tamper-evident evidence and detections tested against relevant threats and failure modes.", "zh-CN": "必需证据租户安全且可发现篡改，检测针对相关威胁与失败模式经过测试。"}},',
    ),
    (
        '    {"id": "AIR", "title": {"en": "AI application, agent, tool, skill, and prompt security", "zh-CN": "AI 应用、Agent、Tool、Skill 与 Prompt 安全"}, "outcome": {"en": "Constrained authority, protected context, policy-mediated tools, deterministic stops, and independent verification.", "zh-CN": "权限受限、上下文受保护、工具经策略仲裁、停止确定且结果独立验证。"}},',
        '    {"id": "AIR", "title": {"en": "AI application, agent, tool, skill, and prompt security", "zh-CN": "AI 应用、Agent、Tool、Skill 与 Prompt 安全"}, "outcome": {"en": "Risk-proportionate control of authority, context, components, tools, approvals, stops, traces, recovery, and independent verification.", "zh-CN": "按风险治理 Authority、Context、Component、Tool、Approval、Stop、Trace、Recovery 与 Independent Verification。"}},',
    ),
    (
        '    {"id":"NCS-IAM-03","domain":"IAM","tier":"T2","title":{"en":"Attested workload and service identity","zh-CN":"经过证明的工作负载与服务身份"},"requirement":{"en":"The provider MUST issue scoped, audience-restricted, short-lived workload and service identities and bind them to attested state where justified.","zh-CN":"服务商必须签发范围受限、Audience 受限、短期的工作负载和服务身份，并在合理场景绑定证明状态。"},"evidence_profile":"EP-IDENTITY-POLICY","verification_profile":"VP-IDENTITY-POLICY","metric_ids":["NCSM-IAM-01","NCSM-IAM-04"]},',
        '    {"id":"NCS-IAM-03","domain":"IAM","tier":"T2","title":{"en":"Attested workload and service identity","zh-CN":"经过证明的工作负载与服务身份"},"requirement":{"en":"The provider MUST issue scoped, audience-restricted, short-lived credentials for workload and service identities and bind identity or credential release to attested state where justified.","zh-CN":"服务商必须为 Workload 与 Service Identity 签发范围受限、Audience 受限的 Short-lived Credential，并在合理场景将 Identity 或 Credential Release 绑定到 Attested State。"},"evidence_profile":"EP-IDENTITY-POLICY","verification_profile":"VP-IDENTITY-POLICY","metric_ids":["NCSM-IAM-01","NCSM-IAM-04"]},',
    ),
    (
        '    {"id":"NCS-IAM-05","domain":"IAM","tier":"T2","title":{"en":"Agent identity, delegation, and action scope","zh-CN":"Agent 身份、委托与动作范围"},"requirement":{"en":"The provider MUST assign each production agent a unique identity, explicit delegator, immutable goal/scope, bounded authority, expiry, and attributable actions.","zh-CN":"服务商必须为每个生产 Agent 分配唯一身份、明确委托方、不可变 Goal/Scope、受限权限、有效期和可归因动作。"},"evidence_profile":"EP-AGENT","verification_profile":"VP-AGENT","metric_ids":["NCSM-AIR-02","NCSM-AIR-06"]},',
        '    {"id":"NCS-IAM-05","domain":"IAM","tier":"T2","title":{"en":"Agent identity, delegation, and action scope","zh-CN":"Agent 身份、委托与动作范围"},"requirement":{"en":"The provider MUST assign each production agent an accountable owner, unique identity, explicit delegator and use case, bounded data/tenant/tool authority, review or expiry, monitoring, incident path, and attributable actions; high-impact workflows MUST additionally bind immutable goal and scope.","zh-CN":"服务商必须为每个生产 Agent 指定 Accountable Owner、Unique Identity、Explicit Delegator/Use Case、受限 Data/Tenant/Tool Authority、Review 或 Expiry、Monitoring、Incident Path 与可归因 Action；高影响 Workflow 还必须绑定不可变 Goal 与 Scope。"},"evidence_profile":"EP-AGENT","verification_profile":"VP-AGENT","metric_ids":["NCSM-AIR-02","NCSM-AIR-06"]},',
    ),
    (
        '    {"id":"NCS-API-01","domain":"API","tier":"T0","title":{"en":"Tenant-correct API authentication and authorization","zh-CN":"租户正确的 API 认证与授权"},"requirement":{"en":"Every critical public and internal API MUST authenticate the subject and enforce server-side object, action, tenant, purpose, and context authorization.","zh-CN":"每个关键公网与内部 API 都必须认证主体，并在服务端执行对象、动作、租户、目的和上下文授权。"},"evidence_profile":"EP-IDENTITY-POLICY","verification_profile":"VP-IDENTITY-POLICY","metric_ids":["NCSM-API-01","NCSM-API-04"]},',
        '    {"id":"NCS-API-01","domain":"API","tier":"T0","title":{"en":"Tenant-correct API authentication and authorization","zh-CN":"租户正确的 API 认证与授权"},"requirement":{"en":"Every critical public and internal API MUST identify the subject, including explicit anonymous/untrusted status where permitted; before tenant-specific, privileged, state-changing, costly, or sensitive actions, it MUST authenticate as required and enforce server-side object, action, tenant, purpose, and context authorization.","zh-CN":"每个关键公网与内部 API 都必须识别 Subject，并在允许匿名时显式标记为 Anonymous/Untrusted；在执行 Tenant-specific、Privileged、State-changing、高成本或敏感动作前，必须按要求完成 Authentication，并在服务端执行 Object、Action、Tenant、Purpose 与 Context Authorization。"},"evidence_profile":"EP-IDENTITY-POLICY","verification_profile":"VP-IDENTITY-POLICY","metric_ids":["NCSM-API-01","NCSM-API-04"]},',
    ),
    (
        '    {"id":"NCS-CMP-02","domain":"CMP","tier":"T0","title":{"en":"Safe accelerator sharing, reset, and memory handling","zh-CN":"安全加速器共享、重置与显存处理"},"requirement":{"en":"The provider MUST select sharing modes by threat model, prevent sensitive placement on insufficient boundaries, and verify reset, error containment, quarantine, memory handling, and inter-tenant cleanup.","zh-CN":"服务商必须按威胁模型选择共享模式，禁止敏感任务使用不足边界，并验证 Reset、Error Containment、Quarantine、显存处理与跨租户清理。"},"evidence_profile":"EP-ISOLATION-RUNTIME","verification_profile":"VP-ISOLATION","metric_ids":["NCSM-ISO-01","NCSM-ISO-04"]},',
        '    {"id":"NCS-CMP-02","domain":"CMP","tier":"T0","title":{"en":"Safe accelerator sharing, reset, and memory handling","zh-CN":"安全加速器共享、重置与显存处理"},"requirement":{"en":"The provider MUST distinguish full-device dedication, hardware partitioning, virtualization, and time-slicing; select modes by threat model; never treat time-slicing as memory or fault isolation; prevent sensitive placement on insufficient boundaries; and verify reset, error containment, quarantine, memory handling, and inter-tenant cleanup on the deployed stack.","zh-CN":"服务商必须区分整卡独占、硬件分区、虚拟化与 Time-slicing，按 Threat Model 选择模式，不得把 Time-slicing 当作 Memory/Fault Isolation，禁止敏感任务使用不足边界，并在真实部署 Stack 上验证 Reset、Error Containment、Quarantine、Memory Handling 与跨租户 Cleanup。"},"evidence_profile":"EP-ISOLATION-RUNTIME","verification_profile":"VP-ISOLATION","metric_ids":["NCSM-ISO-01","NCSM-ISO-04"]},',
    ),
    (
        '    {"id":"NCS-SSC-02","domain":"SSC","tier":"T1","title":{"en":"Provenance, signature, and admission verification","zh-CN":"来源证明、签名与准入验证"},"requirement":{"en":"Release-critical artifacts MUST produce and verify suitable BOM, provenance, signature, scanner, policy, revocation, and admission evidence before use.","zh-CN":"发布关键制品必须在使用前生成并验证合适的 BOM、Provenance、Signature、Scanner、Policy、Revocation 与 Admission 证据。"},"evidence_profile":"EP-DATA-SUPPLY","verification_profile":"VP-DATA-SUPPLY","metric_ids":["NCSM-SSC-01","NCSM-SSC-03"]},',
        '    {"id":"NCS-SSC-02","domain":"SSC","tier":"T1","title":{"en":"Provenance, signature, and admission verification","zh-CN":"来源证明、签名与准入验证"},"requirement":{"en":"Release-critical artifacts MUST produce and verify applicable inventory/BOM, provenance, signature where required, scanner, compatibility, policy, revocation, and admission evidence before use.","zh-CN":"发布关键制品必须在使用前生成并验证适用的 Inventory/BOM、Provenance、按要求提供的 Signature、Scanner、Compatibility、Policy、Revocation 与 Admission Evidence。"},"evidence_profile":"EP-DATA-SUPPLY","verification_profile":"VP-DATA-SUPPLY","metric_ids":["NCSM-SSC-01","NCSM-SSC-03"]},',
    ),
    (
        '    {"id":"NCS-AIR-05","domain":"AIR","tier":"T4","title":{"en":"Agent trace, deterministic stop, and independent verifier","zh-CN":"Agent Trace、确定性停止与独立验证"},"requirement":{"en":"After prerequisites are proven, adaptive workflows SHOULD preserve a tamper-resistant action trace, deterministic success/budget/time/repetition/policy/uncertainty stops, and an independent verifier that the agent cannot alter.","zh-CN":"在前置能力被证明后，自适应工作流应保留抗篡改动作 Trace，具备针对成功、预算、时间、重复、策略和不确定性的确定性停止，以及 Agent 无法修改的独立 Verifier。"},"evidence_profile":"EP-AGENT","verification_profile":"VP-AGENT","metric_ids":["NCSM-AIR-02","NCSM-AIR-06"]},',
        '    {"id":"NCS-AIR-05","domain":"AIR","tier":"T4","title":{"en":"Agent trace, deterministic stop, and independent verifier","zh-CN":"Agent Trace、确定性停止与独立验证"},"requirement":{"en":"After prerequisites are proven, adaptive workflows SHOULD preserve a protected, replayable, tamper-evident action trace, deterministic success/budget/time/repetition/policy/uncertainty stops, rollback or manual recovery, and an independent verifier that the agent cannot alter.","zh-CN":"在前置能力被证明后，自适应工作流应保留受保护、可重放且可发现篡改的 Action Trace，具备针对 Success、Budget、Time、Repetition、Policy 与 Uncertainty 的 Deterministic Stop、Rollback 或 Manual Recovery，以及 Agent 无法修改的 Independent Verifier。"},"evidence_profile":"EP-AGENT","verification_profile":"VP-AGENT","metric_ids":["NCSM-AIR-02","NCSM-AIR-06"]},',
    ),
    (
        '    {"id":"NCS-RES-02","domain":"RES","tier":"T0","title":{"en":"Immutable backup and verified restore","zh-CN":"不可变备份与验证恢复"},',
        '    {"id":"NCS-RES-02","domain":"RES","tier":"T0","title":{"en":"Protected backup and verified restore","zh-CN":"受保护备份与验证恢复"},',
    ),
]

for old, new in catalog_replacements:
    replace_once(catalog, old, new)

for relative in (
    "docs/en/SECURITY_BASELINE.md",
    "docs/zh-CN/SECURITY_BASELINE.md",
):
    path = ROOT / relative
    if relative.startswith("docs/en"):
        replace_once(
            path,
            "| NCS-RES-02 | T0 | Immutable backup and verified restore |",
            "| NCS-RES-02 | T0 | Protected backup and verified restore |",
        )
    else:
        replace_once(
            path,
            "| NCS-RES-02 | T0 | 不可变备份与验证恢复 |",
            "| NCS-RES-02 | T0 | 受保护备份与验证恢复 |",
        )

english_metrics = ROOT / "docs" / "en" / "METRICS_AND_ASSURANCE.md"
replace_once(
    english_metrics,
    """| NCSM-TEL-01 | Required T0 telemetry coverage | healthy, queryable required T0 sources / required T0 sources | 100%; hard gate; missing telemetry is not zero activity |
| NCSM-TEL-02 | Priority telemetry coverage | healthy, queryable priority sources / defined priority sources | reference ≥95% by day 90, with gaps and risk explicit |
| NCSM-TEL-03 | Telemetry freshness | sources delivering within expected latency / required sources | target set per source; reference ≥99% critical |
| NCSM-TEL-04 | Detection validation pass rate | priority detections passing authorized behavior replay / due priority detections | 100% catastrophic scenarios; reference ≥95% other priority detections |
| NCSM-TEL-05 | Evidence tamper detection | simulated unauthorized evidence changes or source-health failures detected / tests | 100% priority tests |
| NCSM-TEL-06 | Alert decision precision and recall proxy | actionable outcomes and known missed test behaviors / reviewed alerts and test corpus | track by use case; publish limitations and sampling |""",
    """| NCSM-TEL-01 | Required T0 telemetry coverage | healthy, queryable required T0 sources / required T0 sources | 100%; hard gate; missing telemetry is not zero activity |
| NCSM-TEL-02 | Telemetry freshness | sources delivering within expected latency / required sources | target set per source; reference ≥99% critical |
| NCSM-TEL-03 | Detection validation pass rate | priority detections passing authorized behavior replay / due priority detections | 100% catastrophic scenarios; reference ≥95% other priority detections |
| NCSM-TEL-04 | Alert decision precision and recall proxy | actionable outcomes and known missed test behaviors / reviewed alerts and test corpus | track by use case; publish limitations and sampling |
| NCSM-TEL-05 | Evidence tamper and source-failure detection | simulated unauthorized evidence changes or source-health failures detected / tests | 100% priority tests |
| NCSM-TEL-06 | Priority non-gate telemetry coverage | healthy, queryable priority sources outside the T0 required set / defined priority non-gate sources | reference ≥95% by day 90, with gaps and risk explicit |""",
)

chinese_metrics = ROOT / "docs" / "zh-CN" / "METRICS_AND_ASSURANCE.md"
replace_once(
    chinese_metrics,
    """| NCSM-TEL-01 | T0 必需遥测覆盖 | 健康且可查询的 T0 必需 Source / T0 必需 Source | 100%；硬门；缺失遥测不能解释为没有活动 |
| NCSM-TEL-02 | 优先遥测覆盖 | 健康且可查询的 Priority Source / 已定义 Priority Source | 第 90 天参考至少 95%，缺口与风险显式 |
| NCSM-TEL-03 | 遥测新鲜度 | 在期望延迟内交付的 Source / Required Source | 按 Source 设定；关键参考至少 99% |
| NCSM-TEL-04 | Detection 验证通过率 | 通过授权 Behavior Replay 的 Priority Detection / 到期 Priority Detection | 灾难性场景 100%，其他优先项参考至少 95% |
| NCSM-TEL-05 | Evidence Tamper Detection | 被发现的模拟未授权修改或 Source-health Failure / 测试 | 优先测试 100% |
| NCSM-TEL-06 | Alert Decision Precision 与 Recall Proxy | 可行动结果和已知漏检测试行为 / 已复核 Alert 与 Test Corpus | 按 Use Case 跟踪，披露局限和抽样 |""",
    """| NCSM-TEL-01 | T0 必需遥测覆盖 | 健康且可查询的 T0 必需 Source / T0 必需 Source | 100%；硬门；缺失遥测不能解释为没有活动 |
| NCSM-TEL-02 | 遥测新鲜度 | 在期望延迟内交付的 Source / Required Source | 按 Source 设定；关键参考至少 99% |
| NCSM-TEL-03 | Detection 验证通过率 | 通过授权 Behavior Replay 的 Priority Detection / 到期 Priority Detection | 灾难性场景 100%，其他优先项参考至少 95% |
| NCSM-TEL-04 | Alert Decision Precision 与 Recall Proxy | 可行动结果和已知漏检测试行为 / 已复核 Alert 与 Test Corpus | 按 Use Case 跟踪，披露局限和抽样 |
| NCSM-TEL-05 | Evidence Tamper 与 Source-failure Detection | 被发现的模拟未授权修改或 Source-health Failure / 测试 | 优先测试 100% |
| NCSM-TEL-06 | 非硬门优先遥测覆盖 | 健康且可查询的 T0 Required Set 之外 Priority Source / 已定义 Non-gate Priority Source | 第 90 天参考至少 95%，缺口与风险显式 |""",
)

print("Applied deterministic NeoCloud catalog and metric-ID accuracy corrections.")
