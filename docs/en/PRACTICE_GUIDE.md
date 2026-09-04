# NeoCloud Cyber Security Practice Guide

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented project draft  
**Audience:** executives, security, platform engineering, SRE, network/fabric, Kubernetes, Slurm/HPC, data/AI, facilities, support, trust and safety, privacy, risk, and assurance teams

This guide turns the [White Paper](WHITEPAPER.md), [Security Baseline](SECURITY_BASELINE.md), [Reference Architecture](REFERENCE_ARCHITECTURE.md), and [Roadmap](ROADMAP.md) into an executable operating model. It is vendor-neutral; product names and technologies are examples, not proof of effectiveness.

## 1. Begin with a service and a trust decision

For each production service, create one versioned assessment package containing:

1. service profiles, exact contractual boundary, environments, regions, versions, and customer commitments;
2. accountable business, technical, security, data, and incident owners;
3. tenant, identity, data/model, API/control-plane, orchestration, host/GPU, storage, Ethernet/RDMA, DPU, BMC/OOB, supplier, support, evidence, and recovery boundaries;
4. all applicable controls and every reviewed not-applicable decision;
5. threat model, attacker assumptions, catastrophic failure paths, and shared responsibility;
6. desired state, policy decision, enforcement points, failure behavior, containment, rollback, and recovery;
7. evidence sources, integrity, freshness, negative/failure tests, and independent validator;
8. production decision, unresolved risk, business decisions/exceptions, customer impact, owner, and target date.

Do not start by purchasing a SIEM, CNAPP, PAM, or AI-security product. First define the trust decisions the service must make, where they are enforced, how they fail, and what evidence can prove the outcome on the deployed path.

## 2. Non-negotiable operating rules

- **T0 is a hard gate.** A failed, unknown, stale, inconclusive, or untested applicable T0 remains `NO_GO_NONCONFORMANT`.
- **A business decision is not a pass.** An emergency decision may explain temporary operation but cannot create `VERIFIED` or a conformance claim.
- **Unknown critical scope is failure.** Unknown owner, tenant, public exposure, GPU sharing, P_Key/DPU assignment, root-key use, required telemetry, backup, or restore state stays in the denominator and blocks the relevant gate.
- **Deployment is not effectiveness.** `IMPLEMENTED` and `VERIFIED` are different states.
- **The implementer is not the sole verifier.** Use a separate person/team, observation path, test harness, or qualified assessor able to challenge the owner.
- **External content never grants authority.** Prompts, tickets, documents, models, packages, RAG data, memory, web pages, and tool output are observations, not authorization.
- **Provider-exclusive responsibility stays with the provider.** Customers cannot secure provider control planes, hosts, reset paths, fabric managers, BMC/OOB, or signing roots they cannot access.
- **Control failure is designed.** High-impact controls specify fail-closed or safe degraded behavior, quarantine, rollback, manual recovery, and evidence when a dependency is unavailable.
- **Evidence is time-bound.** Scope, identity, collection time, integrity, method, limitations, validity, and independent test context are required.
- **Recovery changes trust state.** Reopening verifies identity, artifacts, tenant isolation, data integrity, monitoring, and objectives—not merely process availability.

## 3. Minimum accountability model

Small organizations may combine roles, but not final accountability or independent challenge.

| Role | Accountable decisions | Minimum recurring duty |
|---|---|---|
| Executive risk owner | risk appetite, exceptional business decisions, crisis priorities | monthly critical-risk and gate review |
| CISO/security lead | baseline, security roadmap, challenge and assurance | weekly T0/T1 and failed-control review |
| Service owner | service boundary, claims, customer commitments, residual risk | release and quarterly review |
| Platform owners | reusable identity, policy, compute, fabric, storage, orchestration and evidence controls | SLO, change and incident ownership |
| Data/model owner | purpose, classification, rights, lineage, retention, export, deletion | quarterly lifecycle review |
| Incident commander | command, scope, evidence, containment, communication and reopening | exercise and on-call readiness |
| Independent validator | test design, evidence reproduction, `PASS/FAIL` decision | verification at required cadence |
| Customer/support owner | shared responsibility, support access, notification and assurance | customer-facing accuracy review |

Each control has one accountable owner. Multiple implementers are acceptable; ambiguous ownership is not.

## 4. First 90 days

The calendar is a planning aid. A currently failed T0 is addressed immediately rather than deferred to its nominal phase.

### Days 0–7 — Establish command

Deliver:

- owners for every production service, critical dependency, root/signing key, provider control plane, fabric manager, BMC/OOB environment, and incident path;
- a secure incident channel, severity matrix, on-call escalation, emergency-decision record, and authority to revoke or isolate;
- an initial service, critical-asset, critical-identity, public-exposure, and crown-jewel inventory;
- a freeze or explicit approval gate for new public admin interfaces, new sharing modes, root/fabric changes, and unreviewed production artifacts;
- rotation or disablement of unknown, shared, orphaned, or departed-owner privileged credentials.

Exit only when the provider can establish command, revoke privilege, identify active tenant resources, and isolate a service at a reliable boundary.

### Days 8–30 — Remove critical exposure

Prioritize:

- approved phishing-resistant MFA for applicable provider privilege and high-impact tenant-owner access;
- private provider administration and isolated BMC/OOB paths;
- critical object/action/tenant/purpose/context authorization tests;
- explicit isolation statements for every commercial compute SKU;
- quarantine of ambiguous GPU-sharing, RDMA/P_Key, DPU, storage, support, or reassignment boundaries;
- protection and recovery of KMS/HSM, signing roots, secrets, PKI, and break-glass;
- protected required telemetry for identity, API/control plane, Kubernetes/Slurm, host/GPU/fabric/BMC, keys, artifacts, support, and high-impact agents;
- playbooks for cross-tenant access, root compromise, control-plane takeover, destructive automation, and irrecoverable data risk.

Exit only when every applicable T0 has scope, owner, current state, evidence requirement, validator, and dated containment/remediation, and no failed gate is represented as healthy.

### Days 31–60 — Create authoritative state

Implement:

- service, asset, identity, dependency, data-flow, model, artifact, key, supplier, and support inventories;
- shared-responsibility matrices and customer security contacts;
- joiner/mover/leaver, service-account, workload-identity, agent, certificate, and secret lifecycle;
- vulnerability and exposure discovery linked to real assets and tenant/service context;
- data/model purpose, rights, classification, residency, retention, export, deletion, and backup requirements;
- backup/rebuild-source inventories and dependency mapping;
- desired-versus-actual reconciliation for tenant, scheduler, host, accelerator, network/fabric, DPU, storage, quota, artifact, and policy state.

Exit only when independent discovery coverage is measured, unknown/unowned resources are visible as defects, and critical unknowns cannot disappear from reporting.

### Days 61–90 — Verify the foundation

Perform:

- independent verification of every applicable T0;
- privileged-access denial, expiry, emergency revocation, and break-glass tests;
- cross-tenant prohibited-path tests through API, scheduler, host/GPU, storage, Ethernet, InfiniBand/RDMA, DPU, telemetry, and support paths;
- representative accelerator and local-media reset/sanitization tests across relevant hardware/firmware/driver/sharing variants;
- Kubernetes/Slurm controller restore or known-good rebuild;
- one full incident exercise including reliable scope, customer and legal/privacy notification analysis, containment, recovery, and reopening;
- one critical data/model restore and one tenant offboarding/export/deletion exercise;
- a service-scoped shared-responsibility and assurance package.

Exit only when every applicable T0 is independently `VERIFIED`; in-scope critical asset and privileged-identity ownership is 100%; required T0 telemetry sources are 100% healthy and queryable; priority discovery and non-gate telemetry coverage has a stated denominator and reference target of at least 95%; and failed exercises have accountable containment and remediation.

## 5. Implement every control through the same lifecycle

### 5.1 Scope

Record service/profile, environment, region, version, tenants, assets, identities, data classes, suppliers, dependencies, and excluded components. “Global” without a real population is not a scope.

### 5.2 Threat and failure analysis

Describe attacker/compromised-subject assumptions; allowed and prohibited paths; cross-tenant, root, destructive, privacy, sovereignty and availability failures; dependency outage; stale/partial controller state; rollback and recovery; evidence tampering; and verifier failure.

### 5.3 Control contract

A reusable decision contract is:

```text
subject + delegation + action + resource + tenant + purpose
+ context + policy version
→ allow | deny | approve | quarantine + obligations
```

Obligations may require dedicated placement, restricted egress, masking, dual approval, session evidence, quota, attestation, post-action verification, or cleanup.

### 5.4 Enforcement and failure behavior

Place preventive enforcement close to the resource. A central policy service may distribute decisions, but API gateways, schedulers, nodes, KMS, registries, fabrics, storage, and tool boundaries must not silently fail open when it is unavailable. Define stale-decision limits, local cache behavior, safe degradation, quarantine, rollback, and manual recovery.

### 5.5 Evidence and verification

Generate evidence from the deployed path: API/configuration exports, authorization decisions, protected runtime events, verified attestations, desired/actual reconciliation, prohibited-path and failure tests, revocation/restore/rebuild/sanitization traces, hashes, and independent observations.

A validator confirms scope and freshness, reproduces the assertion, exercises a relevant prohibited path or failure, and returns `PASS`, `FAIL`, `INCONCLUSIVE`, or `NOT_TESTED`. Only `PASS` creates `VERIFIED`.

### 5.6 Operate and revalidate

Revalidate on evidence expiry, material release, new service/SKU/region, sharing or isolation change, controller/orchestrator/firmware/driver update, identity/key/policy change, supplier/data-flow/support change, agent-authority expansion, incident, failed control, restore/rebuild, or inability to reproduce the prior result.

## 6. Implementation patterns by domain

| Domain | Minimum implementation | Mandatory effectiveness test | Strong evidence |
|---|---|---|---|
| GOV | charter, service/control owners, obligations, risks, decisions/exceptions, independent assurance | expired decision and unowned service cannot appear healthy | approved scoped decisions and current independent review |
| ASM | API-driven service/asset/identity/data/model/dependency inventory and reconciliation | detect a controlled unknown or stale assignment | desired/actual diff with owner, tenant and service context |
| IAM | federation, phishing-resistant privileged MFA, JIT/JEA, workload identity, lifecycle, break-glass | deny, expire and revoke at every required enforcement point | IdP/PAM/IAM exports and correlated revocation trace |
| API | tenant-correct authorization, private admin, schema/replay/idempotency/rate/quota, change trace | object/action/tenant confusion and partial-provisioning failure | request, policy, approval, desired/actual state and rollback correlation |
| NET | plane separation, default deny, tenant-aware Ethernet/storage/RDMA/DPU/OOB policy | cross-tenant/management path including stale VRF/P_Key/DPU state | topology, controller state, path test and reconciliation |
| CMP | explicit SKU model, hardened host, safe allocation/reset/error handling | memory, fault, reset, quarantine and cross-allocation cleanup | allocation/cleanup tied to tenant, hardware, firmware and driver |
| ORC | private hardened K8s/Slurm controllers, RBAC, admission/job policy, quotas, node/plugin security | prohibited privileged workload/job and controller-loss recovery | policy exports, audit, negative tests and restore/rebuild trace |
| DAT | purpose/classification, tenant access, encryption/key ownership, lineage, safe formats, deletion | unauthorized access, malicious format, export/deletion/offboarding | object lineage, access/key records, cleanup and restore proof |
| KMS | KMS/HSM, root hierarchy, short-lived secrets, PKI, recovery | root/credential revocation, failed attestation, key recovery | key inventory, ceremony, audit, rotation and recovery trace |
| SSC | approved sources, inventory, BOM, provenance/signature where required, isolated build, admission, recall | reject unknown, revoked, incompatible, or unsigned-when-required artifact | source-to-deploy provenance, policy decision and rollback |
| ENG | threat model, safe defaults, IaC/policy review, tests, canary, rollback | unsafe configuration and failed rollout | review, tests, deployment, drift and post-deploy verification |
| VEM | asset-linked discovery, exposure/exploitability priority, patch/firmware lifecycle | emergency patch/canary and deployed-state retest | finding-to-asset-to-remediation-to-retest chain |
| TEL | protected required telemetry, coverage/freshness inventory, detections as code | source loss, evidence tamper, ATT&CK/ATLAS behavior replay | event samples, health, tests, limitations and alert quality |
| AIR | inventory, identity, delegation, impact, component integrity, typed tools, policy | prompt injection, confused deputy, tool abuse, memory/skill poisoning | versioned configuration, policy/approval, trace and verifier result proportional to risk |
| ABU | trust tiers, AUP, quota/rate/cost/capacity, egress, cases and appeal | quota bypass, cryptomining, denial of wallet, prohibited egress | onboarding decision, enforcement reason, case and restoration |
| IRR | command, playbooks, forensic readiness, notification and reopening gate | cross-tenant/root/agent/availability exercise | timeline, evidence chain, decisions, recovery and independent closure |
| RES | dependency/SLO/RTO/RPO, protected backup, safe degradation, rebuild/failover | restore with unavailable primary identity/key dependency and regional/fabric failure | objective, integrity/isolation checks and reopening decision |
| PHY | facility, BMC/OOB isolation, hardware/firmware lifecycle and sanitization | unauthorized OOB path and representative reassignment/decommission | access, firmware, maintenance, sanitization and custody evidence |

## 7. Service-profile launch checks

### GPU IaaS

Verify tenant-correct API/image authorization; explicit full-device, hardware-partitioned, virtualized, or time-sliced semantics; host, GPU/HBM/cache, NVLink, storage, Ethernet/RDMA, telemetry and support boundaries; allocation lineage; reset/error/quarantine; local-state cleanup; driver/firmware lifecycle; node isolation/rebuild; quota, billing, abuse and egress. Never use “dedicated” without stating each dedicated and shared resource.

### Bare-metal GPU

Add provider-credential removal; isolated BMC/OOB with JIT support; approved/measured firmware and provisioning image; dedicated or precisely declared network/fabric/storage; deprovisioning across GPU, local media, TPM, NIC/DPU, BMC users/certificates and fabric assignments; chain of custody; and method-appropriate sanitization before reassignment.

### Managed Kubernetes

Verify private API server/etcd; strong administrator and workload identity; restricted Pod Security Standards; least-privilege RBAC; default-deny admission/network policy where applicable; tenant namespaces/accounts and quotas; CNI/CSI/device plugin/operator/webhook/node privilege; artifact admission; audit/runtime detection; node quarantine; etcd backup and known-good restore/rebuild.

### Managed Slurm/HPC

Verify private, patched controller/database/REST endpoints; strong authentication; accounts/associations/partitions/QOS/reservations/job ownership; prolog/epilog, SPANK, modules, container runtime, shared storage and node credentials; queue/priority abuse; node/GPU/fabric placement and cleanup tied to job/tenant identity; accounting integrity; backup, failover and recovery.

### Model training

Verify dataset purpose, rights, provenance, integrity and poisoning controls; experiment identity; code/image/config/data/model lineage; safe checkpoint/model formats and restricted deserialization; intermediate/cache/secret/temp cleanup; evaluation integrity; output/export; retention/deletion; privacy and customer ownership.

### Model serving

Verify endpoint/model authorization; tenant-safe routing and KV/cache/session isolation; prompt/output handling and telemetry minimization; model provenance/runtime integrity; extraction/enumeration/adversarial input; quota/rate/cost/capacity; safe fallback/degradation; rollback and privacy-safe incident evidence.

### Agent platform

Every production system requires inventory, owner, identity, delegator, use case, component versions, data/tenant/authority scope, impact assessment, monitoring and incident path. Tool-using systems add typed interfaces, policy mediation, least privilege, short-lived credentials where feasible, egress/data/cost controls and revocation. High-impact or adaptive systems add immutable scope, deterministic approval/stop, protected replayable trace, rollback/manual recovery and an independent verifier the agent cannot change.

### Sovereign or regulated service

Verify the complete jurisdictional boundary across people, identity, data, key release, support, telemetry, backup, suppliers, incident response, recovery, deletion and evidence. Storage residency alone is insufficient.

## 8. Critical engineering patterns

### Preserve tenant and request context end to end

Use stable tenant/request identifiers at every API object, message, controller record, Kubernetes/Slurm object, allocation, GPU/fabric/storage rule, log and evidence item. Reject missing or contradictory context. Compare intended and actual state continuously.

### Treat sharing modes separately

Document memory, cache, DMA, fault, reset, telemetry, topology and operational properties for full-device, hardware partition, virtualization and time-slicing modes. Time-slicing is not memory or fault isolation. Hardware partitioning is not full-device or full-host dedication. Test the exact deployed hardware/firmware/driver/hypervisor/scheduler combination.

### Validate InfiniBand/RDMA and DPU on the real path

Test P_Key membership/enforcement, RDMA reachability, fabric-manager authority, DPU/NIC assignment, storage access, stale/partial controller state and reallocation cleanup. Protect fabric/DPU controllers as provider roots. A VPC or Kubernetes NetworkPolicy is not sufficient evidence.

### Eliminate static workload credentials

Use workload identity, scoped short-lived certificates/tokens, audience restriction, tenant/resource scope, revocation and, where justified, attested state. Metadata and default service identities must not grant broad provider/project authority to tenant workloads.

### Make artifact trust an admission decision

For images, packages, models, checkpoints, drivers, firmware, operators, IaC, prompts, policies and skills, preserve source, build/train lineage, inventory/BOM, provenance/signature where required, scans, policy, revocation and deployed version. A valid signature is evidence of signing, not proof of safety.

### Separate evidence from the evaluated system

Export critical evidence to a boundary ordinary source administrators cannot silently modify. Preserve stable IDs, time integrity, tenant partitioning, access audit, minimization/redaction, retention and legal hold. Missing evidence is a control failure.

### Recover from known-good state

When a root, host, controller, fabric manager or build system is uncertain, prefer revocation and known-good rebuild over optimistic cleanup. Reopening requires independent identity, artifact, data, isolation and monitoring checks.

## 9. Operating cadence

| Cadence | Required activity |
|---|---|
| Continuous | feasible T0 state, identity/policy, public exposure, critical source health, root use, assignment drift, capacity/abuse, backup and high-impact agent action |
| Daily | failed controls/collectors/tests, unknown/unowned critical state, urgent exposure and containment backlog |
| Weekly | vulnerability SLA, privilege, release, risk decisions, detection failure and incident actions |
| Monthly | executive gates/risks, customer commitment drift, supplier/capacity risk and metric quality |
| Quarterly | T0/T1 verification, access review, isolation, revocation/restore, detection replay and applicable agent tests |
| Semi-annual | T2 verification and major incident/control-plane/recovery exercises |
| Annual | independent T3 architecture/isolation, regional recovery/rebuild, supplier and cryptographic recovery |
| Material change | immediate re-scope and revalidation of affected assertions |

## 10. Minimum incident playbooks

Every playbook defines detection, command, reliable scope queries, evidence preservation, containment boundary, identity/key actions, tenant/customer impact, legal/privacy assessment, communication, recovery, reopening and independently verified closure.

At minimum cover:

1. cross-tenant API, storage, GPU/cache, telemetry, fabric or support access;
2. provider root, signing key, KMS/HSM, IdP, PAM or break-glass compromise;
3. Kubernetes/Slurm/controller/operator/provisioning takeover;
4. BMC/OOB, DPU, fabric manager, firmware or supply-chain compromise;
5. accelerator remanence, unsafe sharing, reset or error-domain failure;
6. malicious model/checkpoint/image/package/driver/operator/prompt/policy/skill;
7. destructive or exfiltrating agent/tool workflow and false completion;
8. ransomware, regional/fabric/storage outage, capacity exhaustion or backup failure;
9. tenant fraud, cryptomining, prohibited workload, quota bypass or denial of wallet;
10. data/model deletion failure, residency breach or customer-notification failure.

A playbook is ready only after a technical exercise proves its isolation, revocation, evidence and recovery paths.

## 11. Build, buy and integrate

Build or deeply integrate controls that encode service-specific tenancy and topology: tenant-correct authorization; desired/actual reconciliation; GPU/NVLink/fabric/DPU/storage/scheduler evidence; reset/sanitization; model/checkpoint safe loading and lifecycle; agent delegation/tool mediation; containment and reopening.

Buy or adopt mature components where interfaces and evidence are strong: IdP/MFA, PAM, KMS/HSM, secrets/PKI, vulnerability and attack-surface management, SIEM/data lake, EDR/runtime security, case management, backup, DDoS/WAF/API gateway, signing and transparency.

Require exportable APIs/events, stable identities, tenant-safe behavior, secure update, high availability and safe degradation, incident notification, data handling, independent test support, migration/exit and correlated evidence. A product dashboard alone is not proof of service-wide coverage.

## 12. Due diligence questions

Ask providers and suppliers:

- Which host, GPU/HBM/cache, NVLink, network/RDMA, storage, telemetry, BMC and support resources are dedicated or shared?
- How is tenant/request context preserved from API through physical allocation, cleanup and deletion?
- Which accelerator modes are used, and what memory, fault, reset and reassignment guarantees are tested?
- How are P_Keys, RDMA, DPUs/NICs, BMC/OOB and fabric controllers governed and independently tested?
- Who can access customer data/models, through which JIT workflow, with which evidence and notification?
- Where do plaintext and keys exist, who controls release, and how are roots revoked/recovered?
- Which artifacts require inventory, provenance, signature, admission, revocation and recall?
- What are notification, evidence exchange, restore, export, deletion, residency and offboarding commitments?
- Which controls remain provider, customer or shared during an incident?
- Which claims were independently tested, when, against which exact service/version, and with what limitations?

## 13. Anti-patterns

Reject:

- one aggregate score that hides a failed T0;
- a risk decision recorded as `PASS`;
- “dedicated,” “isolated,” “zero trust,” “encrypted,” “confidential,” “immutable,” or “complete” without exact scope and evidence;
- VPC/namespace isolation asserted as proof of GPU/RDMA/storage isolation;
- time-sliced GPUs represented as memory/fault-isolated tenants;
- shared provider identities or broad metadata credentials exposed to tenant workloads;
- standing administration and unrecorded support access;
- accepting signed artifacts without source/build/key-policy/admission context;
- screenshots or vendor dashboards as the only evidence;
- backups never restored or sanitization never tested;
- agents allowed to approve or verify their own high-impact actions;
- exceptions without owner, customer impact, containment, expiry and remediation;
- security products without a service owner, integration contract, evidence output and failure mode.

## 14. Definition of done

A service is ready to be represented as conformant only when:

- its boundary, profiles, versions, responsibility and customer commitments are explicit;
- every applicable T0 is independently `VERIFIED`;
- critical service/asset/identity/root/GPU/fabric/OOB/data/model/artifact scope is known;
- required telemetry sources are healthy and missing-source behavior is tested;
- prohibited-path isolation, revocation, restore/rebuild, incident and sanitization tests pass;
- evidence is current, scoped, protected, reproducible and independently reviewed;
- unresolved risks have accountable decisions that do not alter control results;
- monitoring detects drift and the team can contain and recover without improvisation.

Use the machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json) as the normative source for stable control IDs, tiers, bilingual requirements, evidence/verification profiles and metric associations.
