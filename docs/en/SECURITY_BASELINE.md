# NeoCloud Cyber Security Baseline

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented project draft  
**Normative machine-readable catalog:** [`controls/neocloud-security-baseline.v1.json`](../../controls/neocloud-security-baseline.v1.json)

## 1. Purpose, scope, and normative language

This baseline defines project-authored minimum cybersecurity outcomes for GPU IaaS, bare-metal GPU, managed Kubernetes, managed Slurm/HPC, model-training, model-serving, agent-platform, and sovereign/regulated NeoCloud services.

- **MUST** identifies a mandatory requirement for an applicable service scope.
- **SHOULD** identifies a strong recommendation whose omission requires documented rationale and residual-risk ownership.
- **MAY** identifies an implementation option.
- An applicability decision must identify the exact service boundary, asset/tenant scope, reason, owner, reviewer, evidence, and revalidation trigger. “Not implemented” is not the same as “not applicable.”
- External-framework alignments are informative. They do not establish certification, legal compliance, deployed effectiveness, or exact control equivalence.

The baseline contains **90 controls across 18 domains**. The JSON catalog is authoritative for stable control IDs, bilingual normative requirements, tiers, default verification frequency, evidence and verification profiles, and metric associations. This document explains assessment, production gates, domain outcomes, and service overlays. If explanatory prose conflicts with the catalog, the catalog and [governance rules](../../GOVERNANCE.md) control until the conflict is corrected.

“NeoCloud” is used as a working industry term for specialized cloud providers serving accelerator-intensive AI and HPC workloads. It is not treated as a formally standardized or regulatory service category.

## 2. Assessment lifecycle

Each service selects one or more service profiles and evaluates every control. An assessment record must contain:

- service, profile, environment, region, version, asset/tenant and data scope;
- applicability and rationale;
- accountable provider, customer, or shared owner;
- implementation state and dependencies;
- evidence IDs, evidence source, collection method, validity period, and integrity protection;
- test method, including a prohibited path or failure behavior where relevant;
- independent validator and verification result;
- exception or business-risk decision, residual risk, customer impact, and target date.

The only normal completion lifecycle is:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

- `READY` requires a defined scope, accountable owner, requirement, dependencies, target date, failure behavior, evidence contract, and test method.
- `IMPLEMENTED` means the mechanism is deployed in the stated scope; it does not prove effectiveness.
- `CANDIDATE_DONE` means the owner has supplied current evidence and asserts completion.
- Only an independent validator returning `PASS` for the exact scope may assign `VERIFIED`.
- `FAIL`, `INCONCLUSIVE`, `NOT_TESTED`, stale evidence, a material change, or inability to reproduce the assertion invalidates `VERIFIED` and returns the control to the appropriate earlier state.

A policy, interview, screenshot, scanner result, vendor dashboard, signature, or attestation may contribute evidence but is not automatically sufficient. Prefer reproducible API/query exports, policy and authorization decisions, protected or tamper-evident runtime events, signed attestations with verified claims and freshness, desired/actual reconciliation, negative-path tests, revocation/restore/rebuild/sanitization traces, hashes, and independent observations from the deployed service.

## 3. Adoption tiers

| Tier | Meaning | Minimum use |
|---|---|---|
| **T0 — Guardrails** | Hard conditions before production capacity or tenant data is exposed | Every applicable T0 must be independently `VERIFIED`; otherwise the service is **NO-GO** and nonconformant under this baseline |
| **T1 — Foundation** | Ownership, inventory, minimum hygiene, visibility, response, and recovery | Establish before material scale; the reference roadmap targets the first 90 days |
| **T2 — Production** | Reusable, policy-enforced, measured controls for sustainable multi-tenant operation | Required for the relevant generally available service boundary |
| **T3 — Assured** | Independently supported higher-assurance controls for sensitive, regulated, sovereign, dedicated, attested, or confidential-computing profiles | Required when the provider makes the corresponding assurance commitment or the threat model requires it |
| **T4 — Adaptive** | Guarded adaptive automation and continuous verification | Adopt only after authority, approval, stop, rollback, trace, and independent-verifier controls are proven |

A score, compensating control, risk acceptance, or emergency business decision never changes a failed applicable T0 into `VERIFIED` or conformant status. A legally authorized executive may document a time-bounded decision to continue or restore service for exceptional business-continuity reasons, but the service remains `NO-GO` under this baseline until every applicable T0 passes independent verification. The decision must be explicit, scoped, expiring, monitored, and recorded with customer/legal/privacy/safety impact, alternatives, containment, rollback, notification, and remediation.

## 4. Production hard gates

A service must not enter or remain conformant production when any applicable gate below is failed, unknown, stale, inconclusive, or untested:

1. **Accountability:** every production service, critical dependency, root/signing key, provider control plane, fabric-management plane, BMC/OOB environment, and incident path has an accountable owner.
2. **Responsibility:** provider, customer, and shared duties are explicit for identity, guest/workload, GPU/fabric, data/model, logging, incident, backup, deletion, support, and assurance.
3. **Inventory and scope:** in-scope critical services, assets, identities, public endpoints, GPU/fabric/OOB state, data/models, high-impact artifacts, suppliers, and dependencies are known and reconciled; unknown critical scope is a failure, not an omitted denominator.
4. **Privileged identity:** applicable provider privilege and high-impact tenant-owner access use approved phishing-resistant MFA; shared administrators are prohibited; emergency revocation and break-glass are tested across enforcement points.
5. **API correctness:** every critical public and internal API authenticates the subject and enforces server-side object, action, tenant, purpose, and context authorization; missing or contradictory tenant context is rejected.
6. **Private administration:** provider control planes, orchestrator controllers/databases, fabric management, BMC/OOB, debug, and support paths are not directly reachable from public or tenant data planes; access uses a governed privileged path.
7. **End-to-end isolation:** tenant identity and policy are preserved across API, controller, scheduler, host, accelerator, storage, Ethernet, InfiniBand/RDMA, DPU/NIC, telemetry, and support operations, and prohibited paths are tested on the real data path.
8. **Declared compute SKU:** every commercial SKU states and tests host, hypervisor/container, GPU/HBM/cache, NVLink topology, network/RDMA, storage, telemetry, and support sharing, isolation properties, and limitations.
9. **Safe accelerator handling:** full-device dedication, hardware partitioning, virtualization, and time-slicing are treated as different products; time-slicing is not accepted as a memory- or fault-isolation boundary; reset, error containment, quarantine, memory handling, and inter-tenant cleanup are validated on the deployed hardware/firmware/driver/scheduler stack.
10. **Secure orchestration:** Kubernetes/Slurm controllers and databases are private, strongly authenticated, patched, separated from tenant authority, backed up, and recoverable; privileged workloads/jobs, plugins, and node/device access are controlled.
11. **Protected data/models:** crown-jewel data, prompts, outputs, models, checkpoints, embeddings, caches, snapshots, and backups have owners, classification, purpose, tenant-correct access, approved encryption/key ownership, lineage, retention, export, deletion, and sanitization rules.
12. **Protected roots and secrets:** critical encryption, signing, identity, attestation, and recovery roots are inventoried, access-controlled, audited, separated, and recoverable; static and embedded production secrets are eliminated or governed as explicit expiring exceptions.
13. **Known artifacts:** production images, packages, drivers, firmware, operators, infrastructure bundles, models, checkpoints, prompts, policies, and skills come from approved, attributable, inventoried sources; release-critical artifacts undergo the required provenance, signature, scan, admission, revocation, and rollback checks.
14. **Threat-informed engineering:** material services and releases have current threat models, security acceptance criteria, safe defaults, tested rollback, observability/evidence requirements, and explicit unresolved-risk decisions.
15. **Exposure remediation:** internet-facing, root-of-trust, control-plane, isolation, and high-impact vulnerabilities or unsafe configurations are continuously discovered and remediated or isolated within risk-based SLAs, with deployed-state retesting.
16. **Protected audit:** every security-relevant use or change of privileged identity, root/key, policy, API/control plane, orchestrator, host/GPU/fabric/BMC, sensitive data/model, artifact admission, support access, and high-impact agent action produces attributable, correlated, protected evidence; required-source loss is detected.
17. **Agent authority:** every production AI system/agent is inventoried and bounded by owner, identity, delegator, use case, data/tenant scope, model/prompt/RAG/memory/skill/tool versions, authority, impact assessment, monitoring, and incident path. Tool-using and high-impact systems receive proportionate typed interfaces, policy mediation, least privilege, approval, stop, trace, and independent-verification controls.
18. **Abuse and capacity:** acceptable use, prohibited activity, urgent-abuse intake, tenant-aware quotas/rates/cost/concurrency/queue/capacity, egress controls, safe enforcement, and appeal paths exist and are tested against bypass and denial-of-wallet scenarios.
19. **Incident command:** a 24×7 path can establish command, preserve evidence, reliably scope affected tenants/resources, revoke identities/roots, isolate at a reliable boundary, assess notification, recover, and independently decide reopening.
20. **Recovery:** critical provider-managed state and required customer data have protected, access-separated backups or known-good rebuild sources; restore/rebuild exercises verify RTO/RPO, identity, integrity, tenant isolation, monitoring, and reopening.
21. **Physical roots:** facilities and BMC/OOB paths are controlled; hardware/firmware identity and lifecycle are governed; GPU/accelerator state, local disks/media, credentials, network/fabric assignments, and host state are verifiably sanitized or reprovisioned before reassignment or disposal.

## 5. Control catalog by domain

### GOV — Governance, risk, compliance, and shared responsibility

**Outcome:** accountable decisions, explicit responsibility, controlled and expiring exceptions, and independently supportable assurance.

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

**Outcome:** every acting subject has a strong, scoped, reviewable identity, with short-lived credentials, sessions, and delegated authority where technically feasible.

| ID | Tier | Control |
|---|---:|---|
| NCS-IAM-01 | T0 | Central federation and phishing-resistant MFA |
| NCS-IAM-02 | T0 | Least privilege, JIT administration, and break-glass |
| NCS-IAM-03 | T2 | Attested workload and service identity |
| NCS-IAM-04 | T1 | Tenant, service-account, and access lifecycle |
| NCS-IAM-05 | T2 | Agent identity, delegation, and action scope |

### API — Control plane, API, and administrative interfaces

**Outcome:** tenant-correct authorization, private provider administration, abuse resistance, traceable change, safe failure, and secure API lifecycle.

| ID | Tier | Control |
|---|---:|---|
| NCS-API-01 | T0 | Tenant-correct API authentication and authorization |
| NCS-API-02 | T0 | Private and governed administrative interfaces |
| NCS-API-03 | T1 | API abuse resistance and resource controls |
| NCS-API-04 | T1 | Control-plane change integrity and audit |
| NCS-API-05 | T2 | Secure API lifecycle, testing, and deprecation |

### NET — Network, fabric, RDMA/InfiniBand, and DPU isolation

**Outcome:** tested separation across packet, storage, management, and direct-memory paths, including controller and stale-state failure modes.

| ID | Tier | Control |
|---|---:|---|
| NCS-NET-01 | T0 | Security-plane separation and default deny |
| NCS-NET-02 | T0 | End-to-end per-tenant network, storage, and fabric isolation |
| NCS-NET-03 | T1 | InfiniBand P_Key and RDMA isolation validation |
| NCS-NET-04 | T1 | Egress, DPU/NIC, and out-of-band isolation |
| NCS-NET-05 | T3 | Continuous path and isolation assurance |

### CMP — Compute, hypervisor, bare metal, GPU, and accelerator isolation

**Outcome:** declared isolation, safe allocation and reset, hardened hosts, trusted provisioning, and service-specific higher-assurance options.

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
| NCS-ORC-01 | T0 | Hardened and private orchestrator control planes |
| NCS-ORC-02 | T1 | RBAC, admission, job, and privileged-workload controls |
| NCS-ORC-03 | T1 | Tenant scheduling, quotas, and placement boundaries |
| NCS-ORC-04 | T2 | Runtime, node, secret, and plugin security |
| NCS-ORC-05 | T2 | Orchestrator backup, recovery, and adversarial validation |

### DAT — Data, dataset, model, artifact, and privacy protection

**Outcome:** controlled classification, purpose, access, use, lineage, output, retention, export, deletion, and offboarding.

| ID | Tier | Control |
|---|---:|---|
| NCS-DAT-01 | T0 | Data and model classification, ownership, and lifecycle |
| NCS-DAT-02 | T0 | Encryption, tenant separation, and access control |
| NCS-DAT-03 | T1 | Lineage, integrity, and safe artifact handling |
| NCS-DAT-04 | T1 | Deletion, export, tenant offboarding, and sanitization |
| NCS-DAT-05 | T2 | Privacy, DLP, and sensitive telemetry/output protection |

### KMS — Secrets, keys, PKI, attestation, and confidential computing

**Outcome:** protected cryptographic roots, short-lived secrets and credentials, governed identity/key release, and tested root recovery.

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

**Outcome:** threat-informed design, safe defaults, reviewable change, test gates, drift control, observability, and reliable rollback.

| ID | Tier | Control |
|---|---:|---|
| NCS-ENG-01 | T0 | Secure development lifecycle and threat-informed design |
| NCS-ENG-02 | T1 | Infrastructure and policy as code with secure defaults |
| NCS-ENG-03 | T1 | Protected change, peer review, and separation of duties |
| NCS-ENG-04 | T2 | Security test gates, canary, and rollback |
| NCS-ENG-05 | T2 | Engineering privacy, secrets, and observability requirements |

### VEM — Vulnerability, exposure, patch, and firmware management

**Outcome:** continuous discovery and risk-based, deployment-verified remediation across every in-scope layer.

| ID | Tier | Control |
|---|---:|---|
| NCS-VEM-01 | T0 | Continuous vulnerability and exposure discovery |
| NCS-VEM-02 | T0 | Risk-based remediation and emergency patching |
| NCS-VEM-03 | T1 | Firmware, driver, and platform patch lifecycle |
| NCS-VEM-04 | T1 | External attack surface and configuration drift |
| NCS-VEM-05 | T3 | Independent penetration, isolation, and adversarial testing |

### TEL — Telemetry, detection engineering, threat intelligence, and audit

**Outcome:** required, tenant-safe, tamper-evident evidence and detections tested against relevant threats and failure modes.

| ID | Tier | Control |
|---|---:|---|
| NCS-TEL-01 | T0 | Centralized, protected, and tenant-safe telemetry |
| NCS-TEL-02 | T0 | Mandatory audit for roots and control boundaries |
| NCS-TEL-03 | T1 | Detection engineering mapped to threats |
| NCS-TEL-04 | T1 | Evidence retention, time integrity, and customer-safe access |
| NCS-TEL-05 | T3 | Continuous control monitoring, hunting, and purple-team validation |

### AIR — AI application, agent, tool, skill, and prompt security

**Outcome:** risk-proportionate control of authority, context, artifacts, tools, approvals, stops, traces, and independent verification.

| ID | Tier | Control |
|---|---:|---|
| NCS-AIR-01 | T0 | AI system and agent inventory with security risk assessment |
| NCS-AIR-02 | T1 | Input, prompt, output, and schema enforcement |
| NCS-AIR-03 | T0 | Tool, skill, and connector least privilege with approval gates |
| NCS-AIR-04 | T2 | Model, RAG, memory, and skill integrity |
| NCS-AIR-05 | T4 | Agent trace, deterministic stop, and independent verifier |

### ABU — Abuse prevention, tenant trust, egress, and acceptable use

**Outcome:** proportionate onboarding, resource and external-interaction controls, misuse detection, safe enforcement, restoration, and appeal.

| ID | Tier | Control |
|---|---:|---|
| NCS-ABU-01 | T1 | Risk-based tenant identity and trust tiers |
| NCS-ABU-02 | T0 | Acceptable use, prohibited activity, and abuse response |
| NCS-ABU-03 | T0 | Quota, rate, cost, and capacity protection |
| NCS-ABU-04 | T1 | Egress and external-interaction controls |
| NCS-ABU-05 | T2 | Abuse detection, coordination, and appeal quality |

### IRR — Incident response, forensics, crisis management, and recovery

**Outcome:** fast command, reliable scoping, evidence preservation, safe containment, defensible notification, recovery, and independently verified closure.

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

**Outcome:** controlled facilities and hardware roots, isolated OOB, trustworthy device state, and verifiable sanitization and decommissioning.

| ID | Tier | Control |
|---|---:|---|
| NCS-PHY-01 | T0 | Facility, physical access, and environmental security |
| NCS-PHY-02 | T0 | BMC and out-of-band root security |
| NCS-PHY-03 | T1 | Secure hardware supply, firmware inventory, and lockdown |
| NCS-PHY-04 | T0 | Verified accelerator, local-disk, and host sanitization |
| NCS-PHY-05 | T1 | Decommission, media destruction, and chain of custody |

## 6. Service-profile overlays

- **GPU-IaaS:** API correctness; VM/container boundary; explicit full-device, hardware-partition, virtualized, or time-sliced GPU semantics; accelerator reset/error/cleanup; fabric/storage isolation; image provenance; host/GPU lineage; quota, billing, and egress.
- **Bare-Metal-GPU:** provisioning and deprovisioning ceremony; BMC/OOB; firmware and measured state; provider-credential removal; dedicated or precisely declared shared network/fabric/storage; complete sanitization and chain of custody.
- **Managed-Kubernetes:** private/hardened control plane; tenant RBAC; restricted admission and Pod Security Standards; CNI/CSI/device-plugin/operator/webhook privilege; workload identity; etcd backup; node quarantine and known-good rebuild.
- **Managed-Slurm-HPC:** controller/database/authentication; accounts/associations/QOS/partitions/reservations; prolog/epilog/SPANK/modules/container runtime; shared storage; queue/fabric isolation; job/accounting integrity and recovery.
- **Model-Training:** dataset purpose/rights/provenance; experiment and source-to-model lineage; poisoning and integrity controls; safe formats and restricted deserialization; checkpoint and temporary/cache handling; evaluation integrity; export, retention, deletion, and ownership.
- **Model-Serving:** endpoint/model authorization; tenant-safe routing and KV/cache/session isolation; prompt/output and telemetry minimization; model provenance/runtime integrity; extraction, adversarial input, quota, rate, cost, capacity, fallback, and rollback.
- **Agent-Platform:** inventory, identity, delegation, immutable scope for high-impact workflows, model/prompt/RAG/memory/skill/tool provenance, typed interfaces, policy mediation, least privilege, egress/data/cost controls, deterministic approval/stop where risk requires, protected trace, revocation, and independent verification.
- **Sovereign-Regulated:** jurisdiction-bounded people, identity, data, keys, support, telemetry, backup, suppliers, incident response, recovery, deletion, and independently supportable assurance. Storage residency alone is insufficient.

## 7. Evidence freshness and revalidation

Evidence is invalid when it exceeds its required validity period or when a material change affects the assertion. Material triggers include a new service/SKU/region/fabric; sharing or isolation change; orchestrator/controller/firmware/driver update; identity/key/policy change; data flow, supplier, support, model, agent, tool, recovery, or evidence-pipeline change; control failure; incident; restore/rebuild; or inability to reproduce the prior result.

Default maximum intervals from the normative catalog are:

| Tier | Default minimum verification cadence |
|---|---|
| T0 | Continuous monitoring where feasible; independent verification at least quarterly and after material change |
| T1 | At least quarterly and after material change |
| T2 | At least semi-annually and after material change |
| T3 | At least annually, independently, and after material change |
| T4 | Continuous metrics plus quarterly adversarial and failure-mode review |

A shorter contractual, legal, threat-driven, evidence-expiry, release, or incident-triggered interval takes precedence.

## 8. Production decision algorithm

```text
if any applicable T0 is FAIL, UNKNOWN, STALE, INCONCLUSIVE, or NOT_TESTED:
    decision = NO_GO_NONCONFORMANT
elif any critical service or asset scope is unknown:
    decision = NO_GO_NONCONFORMANT
elif any required isolation, revocation, restore, incident, or sanitization test failed:
    decision = NO_GO_NONCONFORMANT
elif any unresolved high risk lacks an accountable decision:
    decision = NO_GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

An emergency business decision may be recorded separately; it does not alter `NO_GO_NONCONFORMANT` or produce `VERIFIED` status.

Use the [assessment template](../../templates/baseline-assessment.csv), [practice guide](PRACTICE_GUIDE.md), and [metrics guide](METRICS_AND_ASSURANCE.md). Control and evidence changes follow [GOVERNANCE.md](../../GOVERNANCE.md).
