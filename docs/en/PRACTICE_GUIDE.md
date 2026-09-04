# NeoCloud Cyber Security Practice Guide

**Version:** 1.0.0-draft.2  
**Baseline date:** 2026-09-04  
**Audience:** NeoCloud executives, security, platform engineering, SRE, network/fabric, Kubernetes, Slurm/HPC, data/AI, facilities, support, trust and safety, privacy, and assurance teams

This guide turns the [White Paper](WHITEPAPER.md), [Security Baseline](SECURITY_BASELINE.md), [Reference Architecture](REFERENCE_ARCHITECTURE.md), and [Roadmap](ROADMAP.md) into an executable operating model. It is vendor-neutral. Product names are examples, not requirements. Apply the [Scope and Limitations](SCOPE_AND_LIMITATIONS.md) to every implementation claim.

## 1. Start with a service, not a tool

For each production service, create one assessment package containing:

1. service profile and contractual boundary;
2. accountable business, technical, security, data, and incident owners;
3. tenant, identity, data/model, control-plane, compute, GPU, storage, fabric, BMC/OOB, supplier, and support boundaries;
4. applicable controls and explicit not-applicable decisions;
5. threat model and catastrophic failure paths;
6. desired state, enforcement points, failure behavior, and rollback;
7. evidence sources, freshness, independent verifier, and production decision;
8. open risks, exceptions, customer impact, and target dates.

Do not begin by purchasing a SIEM, CNAPP, PAM, or AI security product. Begin by defining the trust decisions the service must make and the evidence needed to prove those decisions.

## 2. Non-negotiable operating rules

- **T0 is a gate, not a score.** One failed applicable T0 is `NO-GO`.
- **Unknown is not safe.** Unknown ownership, tenancy, public exposure, GPU sharing, P_Key assignment, root-key use, or restore state is treated as a failed assertion.
- **The implementer is not the only verifier.** A separate person, team, or qualified assessor must reproduce the evidence and test the control.
- **External content never grants authority.** Tickets, prompts, models, packages, web pages, documents, and tool output are observations, not authorization.
- **Provider-exclusive responsibility stays with the provider.** A customer cannot secure a BMC, fabric controller, host reset, provider control plane, or provider signing root that the customer cannot access.
- **Control failure must be designed.** Every high-impact control defines fail-closed, safe degraded, quarantine, rollback, and manual-recovery behavior.
- **Evidence has a validity period.** A screenshot without scope, identity, collection time, integrity, and reproducible test context is weak evidence.
- **Recovery changes trust state.** Reopening requires verification of identity, artifact integrity, tenant isolation, and data correctness—not merely service availability.

## 3. Minimum team and decision model

Small organizations may combine roles, but not accountability.

| Role | Accountable decisions | Minimum recurring duty |
|---|---|---|
| Executive risk owner | risk appetite, nonconformant emergency deviation, crisis priorities | monthly critical-risk review |
| CISO/security lead | control model, security roadmap, independent challenge | weekly T0/T1 review |
| Service owner | service boundary, customer commitment, residual risk | release and quarterly review |
| Platform owners | reusable identity, policy, compute, fabric, storage, orchestration controls | SLO and incident ownership |
| Data/model owner | classification, allowed use, lineage, retention, export, deletion | quarterly lifecycle review |
| Incident commander | command, containment, evidence, communication, reopening | exercise and on-call readiness |
| Independent validator | test design, evidence reproduction, PASS/FAIL decision | verification by required frequency |
| Customer/support owner | shared responsibility, support access, notification, assurance | customer-facing accuracy review |

A control must have one accountable owner. Multiple implementers are allowed; ambiguous accountability is not.

## 4. First 90 days

### Days 0–7 — Establish command

Deliver:

- named owners for every production service, root/signing key, control plane, fabric, BMC/OOB environment, and incident path;
- one secure incident channel, severity matrix, on-call escalation, and emergency decision log;
- an initial service and crown-jewel inventory;
- a freeze or explicit approval gate for new public admin interfaces, new sharing modes, root changes, fabric topology changes, and unreviewed production artifacts;
- immediate rotation or disablement of unknown, shared, orphaned, or departed-owner privileged credentials.

Exit only when the provider can convene incident command, revoke privileged access, identify active tenant resources, and isolate a service.

### Days 8–30 — Stop critical exposure

Prioritize:

- phishing-resistant MFA for provider privilege and high-impact tenant administrative roles according to service risk;
- private provider administration and isolated BMC/OOB paths;
- highest-risk object/action/tenant authorization tests;
- declared isolation for every commercial compute SKU;
- quarantine of ambiguous GPU sharing, RDMA/P_Key, DPU, storage, or support boundaries;
- protection of KMS/HSM, signing roots, secrets, and break-glass;
- centralized protected logs for identity, API, control plane, Kubernetes/Slurm, fabric/BMC, keys, and support;
- playbooks for cross-tenant access, root compromise, control-plane takeover, destructive automation, and unrecoverable data risk.

Exit only when every T0 has scope, owner, implementation state, evidence, verifier, and dated remediation.

### Days 31–60 — Build authoritative state

Implement:

- service, asset, identity, dependency, data-flow, model, artifact, and supplier inventories;
- shared-responsibility matrices and customer security contacts;
- joiner/mover/leaver and service-account lifecycle;
- vulnerability/exposure discovery linked to real assets;
- data/model classification, residency, retention, export, and deletion requirements;
- backup inventories and restore dependencies;
- desired-versus-actual reconciliation for tenant, scheduler, host, GPU, network/fabric, storage, and quota state.

Exit only when unknown and unowned critical assets are visible as defects rather than hidden by reporting.

### Days 61–90 — Verify the foundation

Perform:

- independent T0 verification;
- privileged-access revocation and break-glass tests;
- cross-tenant negative tests through API, scheduler, host/GPU, storage, Ethernet, InfiniBand/RDMA, and telemetry;
- representative accelerator/local-disk cleanup tests;
- Kubernetes/Slurm control-plane restore or known-good rebuild;
- one full incident exercise with customer and legal/privacy notification analysis;
- one critical data/model restore and one tenant offboarding/deletion exercise;
- publication of the shared-responsibility and assurance package.

Exit only when every applicable T0 is `VERIFIED`, critical inventory/log coverage is at least 95%, privileged identity ownership is 100%, and failed exercises have accountable remediation.

## 5. Control implementation lifecycle

Use the same sequence for every control.

### 5.1 Scope

Record the service, profile, tenants, regions, versions, assets, identities, data classes, suppliers, and excluded components. “Global” without a real asset list is not a scope.

### 5.2 Threat and failure analysis

Describe:

- attacker and compromised-subject assumptions;
- positive path and prohibited negative paths;
- cross-tenant, root-of-trust, destructive, privacy, sovereignty, and availability failures;
- dependency outage, stale controller state, partial provisioning, rollback, and recovery behavior;
- evidence tampering and verifier failure.

### 5.3 Control contract

Define:

`subject + delegation + action + resource + tenant + purpose + context + policy version → decision + obligations`

Obligations may include dedicated placement, restricted egress, masking, dual approval, session recording, quota, evidence generation, or post-action verification.

### 5.4 Enforcement

Place preventive enforcement close to the protected resource. A central policy engine may distribute decisions, but a network, scheduler, node, KMS, registry, or tool boundary must not silently fail open when the central service is unavailable.

### 5.5 Evidence

Generate evidence from the deployed path: API exports, policy decisions, signed attestations, controller reconciliation, negative tests, restore traces, hashes, event samples, and independent observations.

### 5.6 Verification

A validator must reproduce the claim, test at least one prohibited path, confirm evidence freshness and scope, and return `PASS`, `FAIL`, `INCONCLUSIVE`, or `NOT_TESTED`. Only `PASS` can produce `VERIFIED`.

### 5.7 Operate and revalidate

Revalidate after material changes, incidents, failed controls, new service/SKU/region, controller or firmware upgrade, identity/key hierarchy change, supplier change, agent authority change, restore/rebuild, or evidence expiry.

## 6. Implementation patterns by security domain

| Domain | Minimum implementation | Mandatory test | Strong evidence |
|---|---|---|---|
| GOV | charter, named service/control owners, obligation/risk/exception registers, independent assurance | expired exception and unowned service are blocked from healthy status | approved decisions and current service-scoped assurance |
| ASM | API-driven asset/identity/data/model/dependency inventory and reconciliation | introduce a controlled unknown asset or stale assignment and verify detection | desired/actual diff with owner and tenant context |
| IAM | federation, phishing-resistant MFA, JIT/JEA, short-lived workload/agent identity, break-glass | denial, expiry, emergency revocation, and orphan cleanup | IdP/PAM/IAM exports and revocation traces |
| API | tenant-correct authorization, private admin, schema, replay, quota/rate, change audit | object/action/tenant confusion and partial-provisioning rollback | correlated request, policy, desired state, actual state, and rollback events |
| NET | plane separation, default deny, tenant-aware Ethernet/storage/fabric/DPU/OOB policy | cross-tenant and management reachability including stale VRF/P_Key/DPU state | topology, controller state, packet/path test, and reconciliation |
| CMP | declared SKU isolation, hardened host, safe GPU assignment/reset, attestation where justified | memory/reset/error/quarantine and cross-allocation cleanup | allocation and reset records tied to hardware/version/tenant |
| ORC | private hardened K8s/Slurm controllers, RBAC, admission/job policy, quotas, node/plugin security | privileged workload/job, scheduler escape, controller loss, backup restore | policy exports, audit, negative tests, restore/rebuild traces |
| DAT | classification, tenant authorization, encryption, lineage, safe formats, retention/deletion | unauthorized model/checkpoint access, malicious format, deletion/offboarding | object lineage, key/access records, cleanup and restore proof |
| KMS | central KMS/HSM, root hierarchy, short-lived secrets, PKI rotation, recovery | root/credential revocation, failed attestation, key recovery | key inventory, ceremonies, audit, rotation/recovery traces |
| SSC | approved sources, BOM, provenance, signatures, isolated build, admission, recall | unsigned/unknown artifact rejection and compromised-artifact recall | source-to-deploy provenance and rollback |
| ENG | threat model, secure defaults, IaC/policy review, test gate, canary, rollback | unsafe configuration and failed rollout rollback | review, test, deployment, drift, and post-deploy verification |
| VEM | asset-linked discovery, exploitability/exposure priority, patch SLA, firmware coverage | emergency patch/canary and deployed-version verification | finding-to-asset-to-remediation-to-rescan chain |
| TEL | protected correlated telemetry, coverage inventory, detection-as-code, tenant-safe retention | log-source failure, tamper attempt, ATT&CK/ATLAS behavior replay | event samples, coverage/freshness, test results, alert quality |
| AIR | inventory, impact assessment, immutable scope, typed tools, approval, budget, stop, verifier | prompt injection, confused deputy, tool abuse, memory/skill poisoning | signed configuration, full trace, policy decision, verifier result |
| ABU | tenant trust tiers, AUP, quota/rate/cost/capacity, egress, cases and appeal | quota bypass, unauthorized cryptomining or other policy-prohibited workload, denial-of-wallet, prohibited egress | onboarding decision, enforcement reason, case and restoration |
| IRR | command, playbooks, forensic readiness, notification, reopening gate | cross-tenant/root/agent/availability exercise | timeline, evidence chain, decisions, recovery and independent closure |
| RES | dependency/SLO/RTO/RPO, immutable backup, safe degradation, rebuild/failover | restore with unavailable primary identity/key service and region/fabric failure | objective result, integrity/isolation checks, reopening approval |
| PHY | facility controls, isolated BMC/OOB, firmware/hardware inventory, sanitization and custody | unauthorized OOB path and tenant reassignment sanitation | access logs, config, firmware state, sanitation and destruction records |

## 7. Service-profile launch checklists

### 7.1 GPU IaaS

Before launch, verify:

- tenant-correct API and image authorization;
- VM/container, host, GPU/HBM/cache, NVLink, storage, Ethernet, InfiniBand/RDMA, telemetry, and support isolation claims;
- allowed sharing modes by data sensitivity and customer commitment;
- allocation lineage, reset/error/quarantine, local storage cleanup, and reassignment evidence;
- host and driver/firmware lifecycle, node isolation, and rapid rebuild;
- quota, billing, denial-of-wallet, abuse, and egress controls.

Never market “dedicated” unless every relevant resource boundary is precisely stated.

### 7.2 Bare-metal GPU

Add:

- provider credential removal before handoff;
- BMC/OOB isolation and JIT support access;
- measured firmware and approved provisioning image;
- dedicated or explicitly shared network/fabric/storage boundaries;
- full deprovisioning ceremony covering GPU, local disk, TPM, NIC/DPU, BMC users, certificates, and fabric assignments;
- chain-of-custody and sanitation evidence before reassignment.

### 7.3 Managed Kubernetes

Verify:

- provider-only controllers and etcd are private; a customer-facing API endpoint is private by default or explicitly approved, strongly authenticated, source/rate restricted, DDoS-protected, and audited; strong administrator and workload identity;
- restricted Pod Security Standards and default-deny admission;
- RBAC isolation, tenant namespaces/accounts, quotas, network policy, and secret boundaries;
- CNI, CSI, GPU device plugin, operator, webhook, and node privilege review;
- signed/admitted images and deployment policy;
- audit, runtime detection, node quarantine, etcd backup, restore, and known-good rebuild.

### 7.4 Managed Slurm/HPC

Verify:

- private, patched controller/database/REST endpoints and strong authentication;
- account, association, partition, QOS, reservation, and job ownership;
- prolog/epilog, SPANK plugins, modules, container runtimes, shared storage, and node credential controls;
- queue and priority abuse protections;
- node/GPU/fabric placement and cleanup linked to job and tenant identity;
- controller/database backup, accounting integrity, failover, and recovery.
- Slurm accounts, associations, partitions, QOS, and MCS labels support scheduling and information controls but are not a complete tenant-isolation boundary without OS/runtime, storage, network/fabric, and credential enforcement.

### 7.5 Model training

Add:

- dataset purpose, rights, provenance, integrity, poisoning checks, and access;
- experiment identity, code/image/config/data/model lineage;
- safe checkpoint/model formats and restricted deserialization;
- intermediate artifact, cache, secret, and temporary-data cleanup;
- evaluation integrity and separation from training influence;
- output, export, retention, deletion, privacy, and customer ownership.

### 7.6 Model serving

Add:

- endpoint and model-level authorization;
- tenant-safe routing, KV/cache/session isolation, prompt/output handling, and logging minimization;
- model provenance and runtime integrity;
- extraction, enumeration, adversarial-input, quota, rate, cost, and capacity controls;
- safe fallback/degraded behavior and rollback;
- privacy-safe incident evidence.

### 7.7 Agent platform

Before any high-impact tool is enabled, require:

- unique agent identity, explicit human/service delegator, immutable goal and scope;
- approved and versioned models, prompts, skills, MCP/tool servers, connectors, memory, and RAG sources;
- typed tool schemas, least privilege, short-lived credentials, tenant/data/egress/cost policy;
- deterministic approval for destructive, external, customer-impacting, high-cost, or irreversible actions;
- deterministic stops for success, budget, time, repeated failure, policy violation, and uncertainty;
- tamper-resistant trace and independent verifier;
- no ability for an agent to modify its own policy, credentials, approval authority, evidence, or verifier.

### 7.8 Sovereign or regulated service

Verify the complete jurisdictional boundary across people, identity, data, keys, support, telemetry, backup, suppliers, incident response, and recovery. Residency of storage alone is insufficient.

## 8. Critical technical patterns

### 8.1 Preserve tenant context end to end

Use immutable tenant and request identifiers at every API object, message, controller record, Kubernetes/Slurm object, node allocation, GPU assignment, fabric/storage rule, log, and evidence item. Reject missing or contradictory tenant context. Reconciliation must compare intent with actual state.

### 8.2 Choose accelerator sharing deliberately

Treat dedication, hardware partitioning, mediated virtualization, and scheduler-level sharing as different products. Scheduler-level Kubernetes GPU time-slicing/oversubscription does not by itself provide memory or fault isolation; a supported hypervisor-mediated vGPU mode can have different properties. Never infer isolation from the phrase ‘time-sliced.’ Document and test memory, cache, DMA/IOMMU, fault, reset, telemetry, topology, performance-interference, hardware, hypervisor, driver, firmware, and configuration properties against the service threat model.

### 8.3 Validate InfiniBand/RDMA and DPU boundaries

A VPC or Kubernetes NetworkPolicy does not prove the high-performance data path. InfiniBand P_Key membership is one partitioning mechanism—not evidence of complete tenant isolation by itself. Test membership type and enforcement, default-partition policy, RDMA reachability, fabric-manager authority, DPU assignment, storage access, stale-controller state, and reallocation cleanup on the deployed topology. Protect fabric and DPU controllers as provider roots.

### 8.4 Eliminate static workload credentials

Use workload identity, short-lived certificates/tokens, audience restriction, tenant/resource scope, attested node/workload state where justified, and immediate revocation. Metadata services and default provider service identities must not grant broad project or fleet authority to tenant workloads.

### 8.5 Make artifact trust an admission decision

For images, packages, models, checkpoints, drivers, firmware, operators, IaC, and agent skills, preserve source, build/train lineage, BOM, provenance, signature, scanner result, policy decision, and deployed version. A valid signature is necessary evidence, not proof of safety.

### 8.6 Separate evidence from the evaluated system

Critical logs and evidence must be exported to a boundary with administrative and observational separation sufficient to prevent ordinary source administrators from silently altering the record; this does not universally require a separate physical system. Preserve stable IDs, time synchronization, integrity, tenant partitioning, access audit, redaction, retention, and legal hold. Monitor missing evidence as a control failure.

### 8.7 Use safe recovery, not optimistic cleanup

When roots, hosts, controllers, or build systems are uncertain, prefer revocation and known-good rebuild over attempting to “clean” them. Reopening requires independent tests of identity, artifact integrity, tenant isolation, data integrity, and monitoring.

## 9. Operating cadence

| Cadence | Required activities |
|---|---|
| Continuous | identity/policy decisions, asset reconciliation, public exposure, critical logs, root use, vulnerability signals, GPU/fabric assignments, quota/capacity, backup health, agent actions |
| Daily | critical exposure and failed-control triage; unknown/unowned assets; overdue containment; evidence pipeline health |
| Weekly | vulnerability SLA, privileged changes, risky tenant/egress activity, release and exception review, unresolved incident actions |
| Monthly | executive critical-risk review, T0/T1 status, customer commitment drift, supplier and capacity risk, metric quality |
| Quarterly | access review, T0/T1 revalidation, cross-tenant tests, restore/revocation exercise, detection replay, evidence sampling, agent adversarial review |
| Semi-annual | major incident simulation, orchestrator recovery, destructive-agent scenario, root compromise, customer notification exercise |
| Annual | independent architecture/penetration/isolation assessment, regional DR or known-good rebuild, supplier assurance, cryptographic recovery, roadmap reset |
| Material change | re-scope and revalidate affected controls before or immediately after controlled deployment |

## 10. Incident playbook minimums

Every playbook must define detection, command, scope queries, preservation, containment boundary, identity/key actions, tenant/customer impact, legal/privacy assessment, recovery, reopening criteria, and independent closure.

Required NeoCloud scenarios:

1. cross-tenant API, storage, GPU, cache, telemetry, or fabric access;
2. provider root, signing key, KMS/HSM, IdP, PAM, or break-glass compromise;
3. Kubernetes/Slurm/controller/operator or provisioning takeover;
4. BMC/OOB, DPU, fabric manager, firmware, or supply-chain compromise;
5. accelerator memory/remanence, unsafe sharing, reset, or error-domain failure;
6. malicious model/checkpoint/image/package/driver/operator/skill;
7. destructive or exfiltrating agent/tool workflow;
8. ransomware, region/fabric/storage outage, capacity exhaustion, or backup failure;
9. tenant fraud, unauthorized cryptomining or another policy-prohibited workload, quota bypass, or denial of wallet;
10. data/model deletion failure, residency breach, or unsupported customer notification.

A playbook is not ready until at least one technical exercise proves that the required isolation, revocation, and evidence paths work.

## 11. Evidence quality and independent verification

An evidence item should contain:

- evidence ID and control ID;
- service, profile, environment, tenant, region, asset, identity, and version scope;
- assertion and collection method;
- collector identity and observation time;
- source, hash/signature or integrity protection, and storage location;
- limitations, sampling method, and expiry;
- validator, test procedure, result, findings, and retest date.

Evidence strength, from weakest to strongest:

1. statement or policy;
2. screenshot or manually curated report;
3. repeatable API/query output;
4. protected runtime event or signed attestation;
5. authorized negative-path, restore, failure-injection, or adversarial test;
6. independent reproduction using a separate observation path.

Use the [evidence register](../../templates/evidence-register.csv) and [Metrics and Assurance Guide](METRICS_AND_ASSURANCE.md).

## 12. Build, buy, and integrate

Build or deeply integrate controls that encode NeoCloud-specific tenancy and topology:

- tenant-aware authorization and desired/actual reconciliation;
- GPU, NVLink, fabric, DPU, storage, and scheduler placement evidence;
- reset/sanitization and reassignment workflow;
- model/checkpoint lifecycle and safe loading;
- agent identity, delegation, tool mediation, approval, stop, and verifier;
- service-specific containment and reopening.

Buy or use mature managed/open components where interfaces and evidence are strong:

- IdP/MFA, PAM, KMS/HSM, secret manager, PKI;
- vulnerability and attack-surface management;
- SIEM/data lake, EDR/runtime security, case management;
- backup, DDoS/WAF/API gateway, signing/transparency infrastructure.

Require exportable logs and APIs, tenant-safe behavior, HA and safe degraded mode, secure update, incident notification, data handling, independent testing, migration/exit, and stable identity integration. A vendor dashboard alone is not proof of service-wide coverage.

## 13. Customer and supplier due diligence

Ask for precise answers:

- Which host, GPU, memory/cache, NVLink, network, RDMA, storage, telemetry, and support resources are dedicated or shared?
- How is tenant context preserved from API request to physical allocation and deletion?
- Which GPU sharing modes are used, and what memory/fault/reset guarantees are tested?
- How are P_Keys, RDMA, DPUs, BMC/OOB, and fabric controllers isolated?
- Who can access customer data/models, through which JIT workflow, and with what evidence?
- Where do plaintext and keys exist, who controls them, and how are roots recovered?
- Which artifacts require BOM, provenance, signature, admission, and recall?
- What are notification, evidence exchange, restore, deletion, residency, and offboarding commitments?
- Which controls are provider, customer, or shared, including during incidents?
- Which assurance claims are independently tested, when, against which exact service/version, and what exceptions remain?

## 14. Anti-patterns

Reject these patterns:

- one aggregate compliance score that hides failed T0 controls;
- “dedicated,” “zero trust,” “encrypted,” or “confidential” claims without exact boundaries;
- Kubernetes namespace or VPC isolation asserted as proof of RDMA/GPU/storage isolation;
- scheduler-level shared GPU replicas—or any sharing mode lacking deployment-specific evidence—marketed as hardware-separated tenants;
- shared provider service identities or broad metadata credentials exposed to workloads;
- standing admin privilege and unrecorded support sessions;
- signed artifacts accepted without source/build/key-policy context;
- screenshots used as the only evidence;
- restore plans that have never restored;
- AI agents allowed to approve their own high-impact actions or mark their own work verified;
- exceptions without owner, compensating control, expiry, customer impact, and remediation;
- security products purchased without a service owner, integration contract, evidence output, or failure mode.

## 15. Definition of done

A service is ready for production only when:

- the boundary, service profiles, responsibility, and customer commitments are explicit;
- every applicable T0 is independently `VERIFIED`;
- critical asset, identity, public exposure, root, GPU/fabric/OOB, data/model, and artifact state is known;
- negative-path isolation, revocation, restore/rebuild, incident, and sanitization tests pass;
- evidence is fresh, scoped, protected, reproducible, and independently reviewed;
- unresolved material risks have accountable, authorized, time-bounded decisions;
- monitoring detects drift and the team can contain and recover without improvisation.

Use the machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json) as the source of control IDs, tiers, bilingual requirements, evidence profiles, verification profiles, and metrics.
