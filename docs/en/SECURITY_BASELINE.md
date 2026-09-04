# NeoCloud Cyber Security Baseline

**Version:** 1.0.0-draft.2  
**Baseline date:** 2026-09-04  
**Normative machine-readable catalog:** [`controls/neocloud-security-baseline.v1.json`](../../controls/neocloud-security-baseline.v1.json)

## 1. Purpose and normative language

This baseline defines minimum cybersecurity outcomes for GPU IaaS, bare-metal GPU, managed Kubernetes, managed Slurm/HPC, model-training, model-serving, agent-platform, and sovereign/regulated NeoCloud services.

- **Must** identifies a mandatory requirement unless a reviewed applicability decision proves it is outside the service boundary.
- **Should** identifies a strong recommendation whose omission requires documented rationale and residual-risk ownership.
- **May** identifies an implementation option.
- External-framework alignments are informative. They do not establish certification, compliance, or exact control equivalence.

The baseline contains **90 controls across 18 domains**. The JSON catalog is the authoritative record for bilingual requirements, minimum evidence, verification frequency, metrics, tiers, and control IDs. This document explains how to assess and apply it. The tiers, gates, counts, and targets are project-defined normative rules for this repository, not claims of universal industry consensus; see [Scope and Limitations](SCOPE_AND_LIMITATIONS.md).

## 2. Assessment lifecycle

Each service selects one or more service profiles and evaluates every control. An assessment record must contain service/profile, applicability, asset and tenant scope, provider and customer owner, implementation state, evidence IDs, test method, independent validator, last verification, evidence expiration, exception, residual risk, and target date.

The only allowed completion lifecycle is:

`PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`

- `READY` requires a defined scope, owner, target date, dependencies, evidence, and test method.
- `IMPLEMENTED` means the mechanism is deployed but its effectiveness is not independently proven.
- `CANDIDATE_DONE` means the owner has supplied completion evidence.
- Only an independent validator returning `PASS` may assign `VERIFIED`.
- Failed, incomplete, contradicted, or stale evidence moves the control back to an earlier state.

A screenshot or policy document alone is normally insufficient. Prefer API exports, signed attestations, policy-evaluation results, immutable audit events, reproducible queries, negative tests, restore/rebuild traces, hashes, and independent observations from the deployed service.

## 3. Adoption tiers

| Tier | Meaning | Minimum use |
|---|---|---|
| **T0 — Guardrails** | Non-negotiable conditions before production capacity or tenant data is exposed | Every applicable T0 must be independently `VERIFIED`; otherwise production is **NO-GO** |
| **T1 — Foundation** | Ownership, inventory, minimum hygiene, visibility, response, and recovery | Complete in the first 90 days or before material scale |
| **T2 — Production** | Reusable, policy-enforced, measured controls for multi-tenant general availability | Required for sustainable GA operation |
| **T3 — Assured** | Independent and higher-assurance controls for sensitive, regulated, sovereign, or dedicated services | Required when the service makes a corresponding assurance commitment |
| **T4 — Adaptive** | Continuous verification and guarded automation | Adopt only after authority, failure modes, rollback, and verifier controls are proven |

A score never compensates for a failed T0. An accountable executive and security owner may authorize a time-bounded emergency deviation to continue a service, but the failed or unknown T0 remains `NO-GO` for conformity: it cannot be marked `PASS` or `VERIFIED`, cannot be represented as baseline-compliant, and must retain explicit customer/legal impact, compensating controls, rollback conditions, and a remediation deadline.

## 4. Production hard gates

A service must not enter or remain in general production when any applicable condition below is unknown or unverified:

1. **Accountability:** every production service, critical dependency, root/signing key, control plane, fabric, and incident path has an owner.
2. **Responsibility:** provider, customer, and shared duties are explicit for identity, guest/workload, GPU/fabric, data/model, logging, incident, backup, deletion, and support.
3. **Inventory:** critical services, assets, identities, public endpoints, GPU/fabric/OOB state, data/models, and high-impact artifacts are known and reconciled.
4. **Privileged identity:** provider privilege and tenant owners use approved strong MFA; shared admin accounts are prohibited; emergency revocation and break-glass are tested.
5. **API correctness:** every critical public and internal API authenticates the caller and verifies object/action/tenant authorization server-side.
6. **Private administration:** provider control planes, orchestrator databases/controllers, fabric management, BMC/OOB, debug, and support paths are not directly exposed to public or tenant data planes.
7. **End-to-end isolation:** tenant and authorization context is preserved across control-plane translations and enforced through authoritative bindings at scheduler, host, GPU, storage, Ethernet, InfiniBand/RDMA, DPU, telemetry, and support boundaries.
8. **Declared compute SKU:** host, GPU/HBM/cache, NVLink, fabric, storage, telemetry, and support isolation properties and limitations are documented and tested.
9. **Safe accelerator handling:** sensitive workloads do not use a sharing mode lacking required memory/fault isolation; reset, error, quarantine, and inter-tenant cleanup are verified.
10. **Secure orchestration:** provider-only Kubernetes/Slurm controllers and databases are private, patched, strongly authenticated, separated from tenants, backed up, and recoverable. Any customer-facing management API is private by default or explicitly approved, hardened, restricted, protected from abuse, and fully audited.
11. **Protected data/models:** crown-jewel data and models are owned, classified, tenant-authorized, encrypted, retained, exported, deleted, and sanitized according to policy.
12. **Protected roots and secrets:** critical keys are centrally governed; static secrets are minimized; signing/root use is restricted, audited, and recoverable.
13. **Known artifacts:** production images, drivers, firmware, operators, infrastructure bundles, models, checkpoints, and skills come from approved and inventoried sources.
14. **Threat-informed engineering:** material releases have a current threat model, security acceptance criteria, safe rollback, and explicit unresolved-risk decision.
15. **Exposure remediation:** internet/root vulnerabilities and exposure are continuously discovered and remediated or isolated within risk-based SLAs.
16. **Protected audit:** identity, policy, API, control-plane, root/key, orchestrator, host/GPU/fabric/BMC, data/model, build, support, and agent actions produce protected, correlated evidence.
17. **Agent authority:** every production agent is inventoried; all tools/connectors are policy mediated; high-impact actions cannot self-approve; goal/scope/permissions cannot be changed by untrusted content.
18. **Abuse and capacity:** acceptable use, urgent-abuse response, quotas, rates, costs, queue, and GPU capacity controls exist and are testable.
19. **Incident command:** a 24×7 path can establish command, preserve evidence, revoke roots/identities, isolate at a reliable boundary, assess notification, and decide reopening.
20. **Recovery:** critical control planes and provider-managed data have protected backups and tested restore or known-good rebuild within declared RTO/RPO.
21. **Physical roots:** facilities and BMC/OOB are controlled; tenant/direct corporate access is denied; device and local-storage sanitization is verified before reassignment.

## 5. Control catalog by domain

### GOV — Governance, risk, compliance, and shared responsibility

**Outcome:** accountable decisions, explicit responsibility, expiring exceptions, and independently supportable assurance.

| ID | Tier | Control |
|---|---:|---|
| NCS-GOV-01 | T0 | Security mandate and accountable ownership |
| NCS-GOV-02 | T0 | Shared responsibility and security commitments |
| NCS-GOV-03 | T1 | Risk and threat-model governance |
| NCS-GOV-04 | T2 | Compliance, privacy, and sovereignty governance |
| NCS-GOV-05 | T2 | Exception, assurance, and independent-verification governance |

### ASM — Asset, service, dependency, and data-flow inventory

**Outcome:** know what exists, who owns it, how it relates, which tenant it affects, and whether actual state matches intent.

| ID | Tier | Control |
|---|---:|---|
| NCS-ASM-01 | T0 | Authoritative production service and asset inventory |
| NCS-ASM-02 | T1 | Identity, software, data, and model inventory |
| NCS-ASM-03 | T1 | Data flows and trust boundaries |
| NCS-ASM-04 | T2 | Dependency and service relationship graph |
| NCS-ASM-05 | T3 | Continuous discovery and control-scope reconciliation |

### IAM — Human, tenant, workload, and agent identity

**Outcome:** every acting subject has a strong, scoped, short-lived, and reviewable identity.

| ID | Tier | Control |
|---|---:|---|
| NCS-IAM-01 | T0 | Central federation and phishing-resistant MFA |
| NCS-IAM-02 | T0 | Least privilege, JIT administration, and break-glass |
| NCS-IAM-03 | T2 | Short-lived workload and service identity |
| NCS-IAM-04 | T1 | Tenant, service-account, and access lifecycle |
| NCS-IAM-05 | T2 | Agent identity, delegation, and action scope |

### API — Control plane, API, and administrative interfaces

**Outcome:** tenant-correct authorization, private provider administration, abuse resistance, traceable change, and secure API lifecycle.

| ID | Tier | Control |
|---|---:|---|
| NCS-API-01 | T0 | Tenant-correct API authentication and authorization |
| NCS-API-02 | T0 | Private and governed administrative interfaces |
| NCS-API-03 | T1 | API abuse resistance and resource controls |
| NCS-API-04 | T1 | Control-plane change integrity and audit |
| NCS-API-05 | T2 | Secure API lifecycle, testing, and deprecation |

### NET — Network, fabric, RDMA/InfiniBand, and DPU isolation

**Outcome:** proven separation across every packet, storage, management, and direct-memory path.

| ID | Tier | Control |
|---|---:|---|
| NCS-NET-01 | T0 | Security-plane separation and default deny |
| NCS-NET-02 | T0 | End-to-end per-tenant network, storage, and fabric isolation |
| NCS-NET-03 | T1 | InfiniBand P_Key and RDMA isolation validation |
| NCS-NET-04 | T1 | Egress, DPU/NIC, and out-of-band isolation |
| NCS-NET-05 | T3 | Continuous path and isolation assurance |

### CMP — Compute, hypervisor, bare metal, GPU, and accelerator isolation

**Outcome:** declared isolation, safe allocation and reset, hardened hosts, trusted provisioning, and higher-assurance options.

| ID | Tier | Control |
|---|---:|---|
| NCS-CMP-01 | T0 | Declared isolation model for every compute SKU |
| NCS-CMP-02 | T0 | Safe accelerator sharing, reset, and memory handling |
| NCS-CMP-03 | T1 | Host, hypervisor, and container hardening |
| NCS-CMP-04 | T2 | Secure provisioning, measured state, and attestation |
| NCS-CMP-05 | T3 | High-assurance compute and side-channel controls |

### ORC — Kubernetes, containers, Slurm, and scheduler security

**Outcome:** secure controllers, authorization, admission, scheduling, runtime, cleanup, backup, and recovery.

| ID | Tier | Control |
|---|---:|---|
| NCS-ORC-01 | T0 | Hardened and access-restricted orchestrator control planes |
| NCS-ORC-02 | T1 | RBAC, admission, job, and privileged-workload controls |
| NCS-ORC-03 | T1 | Tenant scheduling, quotas, and placement boundaries |
| NCS-ORC-04 | T2 | Runtime, node, secret, and plugin security |
| NCS-ORC-05 | T2 | Orchestrator backup, recovery, and adversarial validation |

### DAT — Data, dataset, model, artifact, and privacy protection

**Outcome:** controlled classification, access, use, lineage, output, retention, deletion, and offboarding.

| ID | Tier | Control |
|---|---:|---|
| NCS-DAT-01 | T0 | Data and model classification, ownership, and lifecycle |
| NCS-DAT-02 | T0 | Encryption, tenant separation, and access control |
| NCS-DAT-03 | T1 | Lineage, integrity, and safe artifact handling |
| NCS-DAT-04 | T1 | Deletion, export, tenant offboarding, and sanitization |
| NCS-DAT-05 | T2 | Privacy, DLP, and sensitive telemetry/output protection |

### KMS — Secrets, keys, PKI, attestation, and confidential computing

**Outcome:** protected cryptographic roots, short-lived secrets, governed identity/key release, and tested root recovery.

| ID | Tier | Control |
|---|---:|---|
| NCS-KMS-01 | T0 | Central KMS/HSM, key hierarchy, and root protection |
| NCS-KMS-02 | T0 | Secret lifecycle and elimination of static credentials |
| NCS-KMS-03 | T1 | PKI, certificate, and service-identity rotation |
| NCS-KMS-04 | T3 | Attestation-governed admission and key release |
| NCS-KMS-05 | T2 | Cryptographic agility and trust-root recovery |

### SSC — Software, model, and infrastructure supply-chain security

**Outcome:** known, approved, attributable, verifiable, recallable, and reversible production inputs.

| ID | Tier | Control |
|---|---:|---|
| NCS-SSC-01 | T0 | Approved sources and complete artifact inventory |
| NCS-SSC-02 | T1 | Provenance, signature, and admission verification |
| NCS-SSC-03 | T2 | Isolated build, release approvals, and rollback |
| NCS-SSC-04 | T1 | Dependency vulnerability, VEX, and open-source risk |
| NCS-SSC-05 | T2 | Firmware, driver, operator, and model supply assurance |

### ENG — Secure engineering, IaC, change, and configuration

**Outcome:** threat-informed design, safe defaults, reviewable change, test gates, drift control, and reliable rollback.

| ID | Tier | Control |
|---|---:|---|
| NCS-ENG-01 | T0 | Secure development lifecycle and threat-informed design |
| NCS-ENG-02 | T1 | Infrastructure and policy as code with secure defaults |
| NCS-ENG-03 | T1 | Protected change, peer review, and separation of duties |
| NCS-ENG-04 | T2 | Security test gates, canary, and rollback |
| NCS-ENG-05 | T2 | Engineering privacy, secrets, and observability requirements |

### VEM — Vulnerability, exposure, patch, and firmware management

**Outcome:** continuous discovery and risk-based, deployment-verified remediation across every layer.

| ID | Tier | Control |
|---|---:|---|
| NCS-VEM-01 | T0 | Continuous vulnerability and exposure discovery |
| NCS-VEM-02 | T0 | Risk-based remediation and emergency patching |
| NCS-VEM-03 | T1 | Firmware, driver, and platform patch lifecycle |
| NCS-VEM-04 | T1 | External attack surface and configuration drift |
| NCS-VEM-05 | T3 | Independent penetration, isolation, and adversarial testing |

### TEL — Telemetry, detection engineering, threat intelligence, and audit

**Outcome:** complete, tenant-safe, tamper-resistant evidence and detections tested against actual threats.

| ID | Tier | Control |
|---|---:|---|
| NCS-TEL-01 | T0 | Centralized, protected, and tenant-safe telemetry |
| NCS-TEL-02 | T0 | Mandatory audit for roots and control boundaries |
| NCS-TEL-03 | T1 | Detection engineering mapped to threats |
| NCS-TEL-04 | T1 | Evidence retention, time integrity, and customer-safe access |
| NCS-TEL-05 | T3 | Continuous control monitoring, hunting, and purple-team validation |

### AIR — AI application, agent, tool, skill, and prompt security

**Outcome:** constrained authority, protected context and artifacts, policy-mediated tools, deterministic stops, and independent verification.

| ID | Tier | Control |
|---|---:|---|
| NCS-AIR-01 | T0 | AI system and agent inventory with security risk assessment |
| NCS-AIR-02 | T1 | Input, prompt, output, and schema enforcement |
| NCS-AIR-03 | T0 | Tool, skill, and connector least privilege with approval gates |
| NCS-AIR-04 | T2 | Model, RAG, memory, and skill integrity |
| NCS-AIR-05 | T4 | Agent trace, deterministic stop, and independent verifier |

### ABU — Abuse prevention, tenant trust, egress, and acceptable use

**Outcome:** proportional onboarding, resource and external-interaction controls, misuse detection, safe enforcement, and appeal.

| ID | Tier | Control |
|---|---:|---|
| NCS-ABU-01 | T1 | Risk-based tenant identity and trust tiers |
| NCS-ABU-02 | T0 | Acceptable use, prohibited activity, and abuse response |
| NCS-ABU-03 | T0 | Quota, rate, cost, and capacity protection |
| NCS-ABU-04 | T1 | Egress and external-interaction controls |
| NCS-ABU-05 | T2 | Abuse detection, coordination, and appeal quality |

### IRR — Incident response, forensics, crisis management, and recovery

**Outcome:** fast command, evidence preservation, safe containment, defensible notification, recovery, and verified closure.

| ID | Tier | Control |
|---|---:|---|
| NCS-IRR-01 | T0 | Incident command, roles, and secure communications |
| NCS-IRR-02 | T1 | NeoCloud-specific incident playbooks |
| NCS-IRR-03 | T1 | Forensic readiness and evidence preservation |
| NCS-IRR-04 | T1 | Customer, regulator, and ecosystem notification |
| NCS-IRR-05 | T2 | Exercises, lessons learned, and verified closure |

### RES — Resilience, availability, capacity, backup, and disaster recovery

**Outcome:** safe degraded behavior, protected backup, tested failover/restore/rebuild, and verified reopening.

| ID | Tier | Control |
|---|---:|---|
| NCS-RES-01 | T0 | Service objectives, dependency, and recovery requirements |
| NCS-RES-02 | T0 | Immutable backup and verified restore |
| NCS-RES-03 | T2 | Control-plane and regional resilience |
| NCS-RES-04 | T1 | Capacity, DDoS, queue, and GPU-exhaustion resilience |
| NCS-RES-05 | T3 | Known-good rebuild, disaster recovery, and exit portability |

### PHY — Physical, facility, BMC, hardware lifecycle, and media sanitization

**Outcome:** controlled facilities and hardware roots, isolated OOB, trustworthy device state, and verifiable sanitization/decommissioning.

| ID | Tier | Control |
|---|---:|---|
| NCS-PHY-01 | T0 | Facility, physical access, and environmental security |
| NCS-PHY-02 | T0 | BMC and out-of-band root security |
| NCS-PHY-03 | T1 | Secure hardware supply, firmware inventory, and lockdown |
| NCS-PHY-04 | T0 | Verified accelerator, local-disk, and host sanitization |
| NCS-PHY-05 | T1 | Decommission, media destruction, and chain of custody |

## 6. Service-profile overlays

- **GPU-IaaS:** API correctness, VM/container boundary, GPU sharing/reset, fabric/storage isolation, image provenance, and host lineage.
- **Bare-Metal-GPU:** provisioning/deprovisioning ceremony, BMC/OOB, firmware state, dedicated network/fabric, provider-credential removal, and sanitization.
- **Managed-Kubernetes:** private/hardened control plane, tenant RBAC, restricted admission/PSS, CNI/CSI/device plugins, workload identity, etcd backup, and node response.
- **Managed-Slurm-HPC:** controller/database/authentication, accounts/associations/QOS/partitions, prolog/epilog/modules, shared storage, queue, and fabric isolation.
- **Model-Training:** dataset/model lineage, poisoning resistance, safe formats, checkpoint access, temporary/cache cleanup, and experiment evidence.
- **Model-Serving:** endpoint and model authorization, prompt/output handling, KV/cache isolation, extraction/abuse resistance, quota, and availability.
- **Agent-Platform:** delegation, tool/skill provenance and least privilege, deterministic approval/stop, trace, verifier, memory integrity, and external-content boundaries.
- **Sovereign-Regulated:** jurisdiction-bounded people, data, keys, support, telemetry, backup, suppliers, notification, and independent assurance.

## 7. Evidence freshness and revalidation triggers

Evidence is stale when it exceeds its required frequency or when a material change affects the assertion. Revalidation triggers include service-SKU or sharing changes, new region/fabric, orchestrator or controller upgrade, identity/key hierarchy change, data flow or supplier change, model/agent/tool capability expansion, control failure, incident, restore/rebuild, or verifier inability to reproduce the result.

Default minimum revalidation is: T0—continuous monitoring where feasible plus independent verification at least quarterly and after material change; T1—at least quarterly and after material change; T2—at least semi-annually and after material change; T3—control-owner review at least semi-annually, independent assessment at least annually, and review after material change; T4—continuous metrics plus quarterly adversarial/failure-mode review and review after material change. A service-specific threat model, contract, incident, or regulator may require a shorter interval.

## 8. Production decision algorithm

```text
if any applicable T0 is not independently VERIFIED:
    decision = NO-GO
elif any critical evidence is stale or service scope is unknown:
    decision = NO-GO
elif any unresolved high risk lacks accountable acceptance:
    decision = NO-GO
elif required restore, revocation, isolation, incident, or sanitization tests failed:
    decision = NO-GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

Use [the assessment template](../../templates/baseline-assessment.csv) and [the metrics guide](METRICS_AND_ASSURANCE.md). Control changes follow [GOVERNANCE.md](../../GOVERNANCE.md).
