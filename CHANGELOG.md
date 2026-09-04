# Changelog

All notable changes to NeoCloud Cyber Security are recorded here.

## 1.0.0-draft.2 — 2026-09-04

### Corrected

- Reframed the repository as a project-defined, vendor-neutral reference baseline rather than an open project, deployed product, adopted industry standard, or universal security control plane.
- Reconciled T0 emergency handling with the hard `NO-GO` algorithm: a time-bounded emergency deviation remains explicitly nonconformant and cannot become `PASS` or `VERIFIED`.
- Reconciled T3 cadence as semi-annual control-owner review plus annual independent verification and material-change review.
- Distinguished scheduler-level Kubernetes GPU time-slicing from mediated vGPU, hardware partitioning, and full-GPU dedication; made isolation and cleanup claims deployment specific.
- Clarified that InfiniBand P_Keys, Slurm scheduling constructs, Kubernetes namespaces, attestation, confidential computing, and signatures are partial mechanisms rather than complete proof.
- Replaced universally private customer API wording with a provider-private/customer-endpoint risk model.
- Corrected `CONTRIBUTING.md` to describe the actual local and GitHub Actions validation workflow.

### Added

- Bilingual scope and limitations documents, a source-backed accuracy review, intended GitHub metadata, and a security-reporting policy.

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
- Refreshed the standards and research basis through 2026-09-04, including current NIST HPC/AI data-center/API/storage publications, CSA CCM/AICM/AISMM, OWASP GenAI and agent-control material, Kubernetes, Slurm, NVIDIA, SLSA, Sigstore, and MITRE ATT&CK/ATLAS.

### Validation contract

- Domains: **18**.
- Controls: **90**, exactly five per domain.
- Tier distribution: **T0=32, T1=31, T2=19, T3=7, T4=1**.
- Languages: **English and Simplified Chinese**.
- Every control includes a stable ID, tier, bilingual title and normative requirement, evidence profile, independent-verification profile, and metric associations.

### Status

This release is an implementation-oriented public draft. It is not a certification, legal opinion, or guarantee. External-framework mappings and draft publications are informative inputs and require independent validation for the exact framework version, service, jurisdiction, contractual scope, and audit objective.
