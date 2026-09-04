# Changelog

All notable changes to NeoCloud Cyber Security are recorded here.

## Unreleased — accuracy audit and repository hardening

### Corrected

- Repositioned the repository as a vendor-neutral security baseline, reference architecture, roadmap, and implementation guide rather than a deployable “unified security control plane.”
- Defined “NeoCloud” as a working industry term rather than a formal, regulatory, or universally accepted service category.
- Resolved the T0 exception conflict: a failed, unknown, stale, inconclusive, or untested applicable T0 remains `NO_GO_NONCONFORMANT`; a time-bounded business-risk decision cannot create `VERIFIED` or a conformance claim.
- Aligned the default revalidation cadence across governance, baseline, white paper, practice guide, roadmap, reference architecture, metrics, and the machine-readable catalog: T0/T1 quarterly, T2 semi-annually, T3 annually and independently, T4 continuously measured with quarterly adversarial/failure-mode review, plus material-change triggers.
- Distinguished persistent identity from short-lived credentials, sessions, privilege grants, and delegated authority where technically feasible.
- Replaced uniform agent controls with risk-proportionate requirements: all production agents require ownership, identity, scope, component inventory, monitoring, and incident handling; tool-using, high-impact, destructive, external, irreversible, or adaptive systems receive progressively stronger policy, approval, stop, trace, rollback, and independent-verifier controls.
- Corrected GPU-sharing language: full-device dedication, hardware partitioning, virtualization, and time-slicing are separate products; time-slicing is not memory or fault isolation, and hardware partitioning is not full-device/full-host dedication.
- Corrected InfiniBand/RDMA language so P_Key membership is treated as one control whose effectiveness depends on governed fabric managers, endpoint behavior, actual enforcement, reconciliation, stale-state handling, and deployed-path testing.
- Clarified that signatures and attestations support specific claims but do not automatically prove artifact safety, source trust, deployed effectiveness, or complete isolation.
- Corrected metric denominators and thresholds: unknown critical assets remain failures; in-scope critical ownership and required T0 telemetry health target 100%; 95% remains a reference target only for priority discovery or non-gate coverage.
- Corrected public-ingress semantics: unauthenticated traffic is an explicit anonymous/untrusted principal until authentication is required and succeeds, rather than assuming every initial subject is already authenticated.
- Clarified central-service failure behavior, evidence tamper detection, safe degradation, known-good recovery, media/device sanitization, and independent reopening.
- Marked final, draft, public-review, living-project, vendor, and research references distinctly; corrected OWASP Agentic Skills Top 10 to a public-review draft/project at the 2026-09-04 evidence cut-off.
- Added current primary references for NIST Digital Identity Guidelines, media sanitization, platform firmware resiliency, OWASP API Security, accelerator sharing, and fabric isolation.

### Added

- Bilingual project positioning and “Start here” navigation on both README files.
- `SECURITY.md` for confidential vulnerability and sensitive-data reporting.
- `.github/REPOSITORY_SETTINGS.md` with recommended GitHub About descriptions, focused topics, publication checklist, license decision options, default-branch rules, feature settings, and release requirements.
- Evidence-aware pull-request template.
- Issue forms for factual/documentation corrections and normative control/assurance changes.
- `CODEOWNERS` for default ownership of normative controls, documentation, validation scripts, and workflows.
- Explicit no-license warning pending an owner decision before public reuse or release.

### Preserved

- Stable set of 18 domains and 90 control IDs.
- Tier distribution `T0=32`, `T1=31`, `T2=19`, `T3=7`, `T4=1`.
- Version `1.0.0-draft.1`; the audit is a non-breaking factual, semantic, governance, and repository-hardening correction pending the next release decision.

## 1.0.0-draft.1 — 2026-09-04

### Added

- Complete English and Simplified Chinese NeoCloud Cyber Security white papers.
- Bilingual security baseline with 18 security domains and 90 stable controls.
- Five-tier adoption model: T0 Guardrails, T1 Foundation, T2 Production, T3 Assured, and T4 Adaptive.
- Bilingual implementation-oriented practice guides with a first-90-days plan, domain implementation patterns, service-profile launch checks, operating cadence, incident scenarios, evidence requirements, and build/buy guidance.
- Bilingual reference architecture covering governance, identity and policy, edge and control plane, orchestration and runtime, compute/fabric/storage, data/model/supply chain, and telemetry/response/recovery planes.
- Bilingual 0–24-month development roadmap with phase gates, accountable workstreams, target-state outcomes, build/buy guidance, and program risks.
- Bilingual metrics and continuous-assurance guides with production gates, evidence contracts, independent-verification states, metric definitions, sampling rules, dashboards, and assurance-package guidance.
- Normative machine-readable bilingual control catalog at `controls/neocloud-security-baseline.v1.json`.
- JSON Schema for structural validation and reusable evidence, verification, tier, service-profile, and metric references.
- Standard-library repository validator checking exact control IDs and counts, tier distribution, cross-references, bilingual baseline parity, release versions, required deliverables, and relative Markdown links.
- GitHub Actions validation for pull requests and the default branch.
- Assessment, evidence, exception, risk, shared-responsibility, security-service-catalog, threat-model, and incident-severity templates.
- Governance, contribution, versioning, and change-control documents.

### Changed

- Reworked English and Chinese repository landing pages into complete delivery indexes with local validation instructions.
- Made `T0` a hard production gate: failed, unknown, inconclusive, untested, or stale applicable T0 evidence cannot be offset by an aggregate score.
- Separated `IMPLEMENTED` from independently `VERIFIED` and standardized the lifecycle `PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`.
- Expanded the evidence model to include scope, freshness, integrity, negative testing, recovery testing, and independent reproduction.
- Established a standards and research basis through the 2026-09-04 evidence cut-off.

### Validation contract

- Domains: **18**.
- Controls: **90**, exactly five per domain.
- Tier distribution: **T0=32, T1=31, T2=19, T3=7, T4=1**.
- Languages: **English and Simplified Chinese**.
- Every control includes a stable ID, tier, bilingual title and normative requirement, evidence profile, independent-verification profile, and metric associations.

### Status

This release is an implementation-oriented project draft. It is not a deployable product, certification, legal opinion, formal standard, or guarantee. External-framework mappings and draft/vendor sources are informative inputs and require independent validation for the exact framework version, service, jurisdiction, contractual scope, deployment, and audit objective.
