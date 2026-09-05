# Changelog

All notable changes to NeoCloud Cyber Security are recorded here.

## Unreleased — 2026-09-05 validation and source correction

- Fix a reproduced count contradiction: the 40 stored prior classifications are 21 explicit / 12 partial / 7 gaps, not 17/17/6. Derive summary counts instead of forcing rows to match a headline.
- Advance only the public-findings profile to 1.0.1. Preserve the base version, all 90 core IDs, tiers, 40 finding IDs and 20 public snapshot IDs.
- Actually evaluate JSON Schema with explicit date checks; reject duplicate JSON keys, non-finite numbers, external schema references, malformed CSV rows, mapping/severity/title drift and fabricated assessed template states.
- Correct source URLs, attach source IDs to findings, distinguish C_Key from CC_Key, add PM_Key/N2N_Key to the existing key group and preserve actual ISO/IEC 27001 certificate wording.
- Add a non-mutating errata compiler, local all-check runner, explicit validation dependencies and offline negative regression tests. The strict check is no longer dependency-free; existing stdlib checks remain separate.
- Replace broad coverage claims with scoped mapping claims and bilingual authorized drill procedures for fabric, DPU, shared Kubernetes, observability, GPU sharing and agent authority.
- Restore template guidance required by the legacy accuracy check. Record test scope, source retrieval limitations and the absence of live infrastructure assessment in reviews/2026-09-05-validation-audit.md.
- Keep remote CI skipped for this change. Do not change repository visibility, license or branch protections.

## Unreleased — SemiAnalysis / ClusterMAX public-findings coverage

### Added

- Independent bilingual coverage audit for publicly accessible SemiAnalysis NeoCloud security issue patterns and the currently enumerable canonical public ClusterMAX Security requirements.
- Project-authored decomposition of five public article-level patterns into 40 atomic, test-oriented patterns with stable `SA-NC-*` IDs.
- Mapping of the 20/20 requirements currently enumerable on the canonical public ClusterMAX Security page to stable NeoCloud controls, without claiming a score, endorsement, certification or exact criteria parity.
- Machine-readable interoperability profile and JSON Schema:
  - `controls/semianalysis-public-findings-profile.v1.json`
  - `controls/semianalysis-public-findings-profile.v1.schema.json`
- Normative v1 errata and Schema:
  - `controls/neocloud-security-baseline.v1.errata.json`
  - `controls/neocloud-security-baseline.v1.errata.schema.json`
- Service/region/cluster/SKU/version-scoped assessment templates for the 40 atomic patterns and 20 canonical public Security-page requirements.
- Standard-library validator checking pattern counts and IDs, control references, source/count caveats, three assurance views, assessment result enums and normative errata.

### Corrected

- Distinguished full-device dedication, hardware partitioning, hypervisor-mediated vGPU and scheduler-level bare-device-plugin time-slicing. Scheduler-level Kubernetes GPU time-slicing must not be represented as memory or fault isolation; mediated-vGPU claims are product-, GPU-, hypervisor-, driver/manager-, firmware-, topology- and configuration-specific.
- Made InfiniBand management and service controls explicit: M_Key, SM_Key, SA_Key, C_Key/CC_Key, VS_Key, SHARP AM_Key, service/per-job keys, Fabric Manager authority, allowed GUID policy, SAETM/MAD/QP0 and SR-IOV VF restrictions.
- Made BlueField RShim/tmfifo_net0, DPU identity/firmware/reassignment, vCluster/shared-control-plane, kubelet/node API and Prometheus/Grafana tenant-boundary checks explicit.
- Added dynamic minimum-safe-version handling, vendor embargo/prerelease advisory intake, staged rollout, deployed-state verification, vulnerability disclosure and remediation retest.
- Separated tenant black-box, provider white-box and independent failure/recovery assurance instead of treating one public audit path as complete proof.
- Recorded that an alternate ClusterMAX host reported 21 Security criteria while only 20 were independently enumerable on the canonical page at the review cut-off; no 21/21 or exact-parity claim is made.

### Preserved

- Stable set of 18 domains and 90 core control IDs.
- Tier distribution `T0=32`, `T1=31`, `T2=19`, `T3=7`, `T4=1`.
- Base catalog version `1.0.0-draft.1`; the mechanism-specific correction is carried as explicit normative errata until a later catalog version incorporates it.

## Unreleased — accuracy audit and repository hardening

### Corrected

- Repositioned the repository as a vendor-neutral security baseline, reference architecture, roadmap and implementation guide rather than a deployable “unified security control plane.”
- Defined “NeoCloud” as a working industry term rather than a formal, regulatory or universally accepted service category.
- Resolved the T0 exception conflict: a failed, unknown, stale, inconclusive or untested applicable T0 remains `NO_GO_NONCONFORMANT`; a time-bounded business-risk decision cannot create `VERIFIED` or a conformance claim.
- Aligned the default revalidation cadence across governance, baseline, white paper, practice guide, roadmap, reference architecture, metrics and the machine-readable catalog.
- Distinguished persistent identity from short-lived credentials, sessions, privilege grants and delegated authority where technically feasible.
- Replaced uniform agent controls with risk-proportionate requirements.
- Corrected GPU-sharing, InfiniBand/RDMA, artifact-signature, public-ingress, central-service failure, metric-denominator, evidence, recovery and source-status semantics.
- Added current primary references for digital identity, media sanitization, firmware resilience, API security, accelerator sharing and fabric isolation.

### Added

- Bilingual project positioning and “Start here” navigation on both README files.
- `SECURITY.md`, evidence-aware pull-request template, focused issue forms and `CODEOWNERS`.
- `.github/REPOSITORY_SETTINGS.md` with recommended About descriptions, topics, publication checklist, license options, default-branch rules, feature settings and release requirements.
- Explicit no-license warning pending an owner decision before public reuse or release.

### Preserved

- Stable set of 18 domains and 90 control IDs.
- Tier distribution `T0=32`, `T1=31`, `T2=19`, `T3=7`, `T4=1`.
- Version `1.0.0-draft.1`.

## 1.0.0-draft.1 — 2026-09-04

### Added

- Complete English and Simplified Chinese NeoCloud Cyber Security white papers.
- Bilingual security baseline with 18 security domains and 90 stable controls.
- Five-tier adoption model: T0 Guardrails, T1 Foundation, T2 Production, T3 Assured and T4 Adaptive.
- Bilingual practice guides, reference architecture, 0–24-month roadmap and metrics/continuous-assurance guides.
- Normative machine-readable bilingual control catalog and JSON Schema.
- Repository validator and pinned GitHub Actions validation workflow.
- Assessment, evidence, exception, risk, shared-responsibility, security-service-catalog, threat-model and incident-severity templates.
- Governance, contribution, versioning and change-control documents.

### Validation contract

- Domains: **18**.
- Controls: **90**, exactly five per domain.
- Tier distribution: **T0=32, T1=31, T2=19, T3=7, T4=1**.
- Languages: **English and Simplified Chinese**.
- Every control includes a stable ID, tier, bilingual title and normative requirement, evidence profile, independent-verification profile and metric associations.

### Status

This release is an implementation-oriented project draft. It is not a deployable product, certification, legal opinion, formal standard or guarantee. External-framework mappings and draft/vendor sources are informative inputs and require independent validation for the exact framework version, service, jurisdiction, contractual scope, deployment and audit objective.
