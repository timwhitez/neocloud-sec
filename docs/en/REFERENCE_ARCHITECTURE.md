# NeoCloud Cyber Security Reference Architecture

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented project draft

## 1. Purpose and architectural contract

This reference architecture describes a target security system for specialized AI/GPU cloud services. It is logical and vendor-neutral: components may be combined or distributed, but the trust decisions, enforcement points, failure behavior, evidence, and recovery boundaries must remain explicit.

The architecture is not deployable software and does not prescribe one product stack. It implements the outcomes in the [Security Baseline](SECURITY_BASELINE.md) through seven cooperating planes:

```text
Governance and assurance
          │
Identity, delegation and policy
          │
Edge, API and provider control plane
          │
Orchestration and workload runtime
          │
Compute, accelerator, fabric, storage and physical roots
          │
Data, model and software/hardware supply chain
          │
Telemetry, response, recovery and continuous assurance
```

Every material action should answer:

```text
who or what is acting?
under whose delegation?
for which tenant and purpose?
on which resource and version?
under which policy and approval?
through which enforcement points?
what actually changed?
what evidence proves the result and failure behavior?
who can independently verify and recover it?
```

## 2. Trust assumptions

- Network location alone is not identity or authorization.
- Public ingress may begin as an unauthenticated, explicitly **anonymous/untrusted principal**. Before any tenant-specific, privileged, state-changing, costly, or sensitive action, the required authentication and authorization must succeed.
- Identity may persist; credentials, sessions, privilege grants and delegated authority should be scoped and short-lived where technically feasible.
- Tenant context is explicit and immutable through the request path. Missing or conflicting context is rejected.
- External content—including prompts, tickets, documents, web pages, packages, models, RAG data, memory and tool output—provides observations, not authority.
- Provider-exclusive roots, such as provider control planes, BMC/OOB, fabric managers, host reset and signing roots, remain provider responsibilities.
- A central policy, identity, evidence or orchestration service can fail. Local enforcement must have explicit fail-closed or safe-degraded behavior rather than silently allowing stale or missing decisions.
- No component proves its own effectiveness solely through its own state or dashboard.
- Recovery must restore trust in identity, artifacts, data, isolation and monitoring, not only process availability.

## 3. Stable identity and correlation model

Use stable, non-reused identifiers for:

- service, service profile, environment, region and release;
- tenant, organization, user, service, workload, device and agent;
- human/service delegator and delegated session;
- request, change, approval, policy version and decision;
- Kubernetes cluster/namespace/service account/pod and Slurm cluster/account/job;
- host, hypervisor, GPU/accelerator, partition/virtual function, DPU/NIC, rack and fabric port;
- VLAN/VXLAN/VRF/P_Key, storage account/volume/object and local media;
- dataset, prompt, output, model, checkpoint, embedding, cache, image/package/driver/firmware/policy/skill;
- key, certificate, secret, attestation and signing/recovery root;
- event, evidence, finding, case, incident, restore, sanitization and verifier result.

Identifiers must be present in API objects, messages, desired and actual controller state, scheduler allocations, enforcement decisions, logs, evidence and cleanup records. Translation between identifiers is itself controlled, logged and reconciled.

## 4. Policy decision model

A reusable authorization request is:

```text
subject identity
+ delegation chain
+ action
+ resource
+ tenant
+ purpose
+ context
+ resource and artifact state
+ policy version
→ allow | deny | require approval | quarantine
+ obligations
```

Context may include device/workload/agent state, authentication strength, service/profile, region, data class, isolation SKU, quota/cost, vulnerability/exposure, artifact provenance, attestation freshness, incident state and risk decision.

Obligations can require dedicated or hardware-partitioned placement, restricted egress, masking, rate/quota/cost limits, JIT session evidence, dual approval, attestation, sandboxing, post-action verification, cleanup, notification or manual review.

Policy decisions should include a reason, decision ID, version, expiry/staleness rule and evidence destination. The protected resource enforces the decision; central evaluation alone is insufficient.

## 5. Seven security planes

### 5.1 Governance and assurance plane

Maintains:

- service catalog and exact boundaries;
- control applicability and shared responsibility;
- legal, regulatory, privacy, safety, sovereignty, contract and customer commitments;
- threat models, risks and catastrophic failure paths;
- business decisions/exceptions without changing control results;
- control lifecycle, evidence validity, independent verification and assurance packages;
- supplier and dependency assurance;
- release and reopening decisions.

This plane must distinguish project conformance, legal obligation, business-risk decisions and external certification. An emergency decision never changes a failed T0 into `VERIFIED`.

### 5.2 Identity, delegation and policy plane

Provides:

- human and tenant federation, authenticator policy and phishing-resistant privileged access;
- JIT/JEA administration, session control, emergency revocation and break-glass;
- workload, service, device and agent identity;
- short-lived certificates/tokens, audience and tenant/resource scope;
- delegation chain, purpose and approval;
- policy evaluation, policy distribution and revocation;
- PKI, KMS/HSM integration, attestation verification and key-release decisions;
- identity/access lifecycle and review.

The plane does not rely on shared provider identities exposed to tenant workloads. A workload or agent cannot broaden its own delegation, policy, credentials, evidence or verifier authority.

### 5.3 Edge, API and provider control plane

Contains public ingress, API gateways, tenant consoles, support entry points, provisioning, quota/billing, provider administration and service controllers.

Required patterns:

- anonymous public traffic remains explicitly untrusted until authentication is required and completed;
- critical APIs enforce server-side object, action, tenant, purpose and context authorization;
- schemas, size, replay, idempotency, rate, quota, concurrency and cost are controlled;
- provider administration, debug, controller/database, fabric and BMC paths use private governed access rather than direct public or tenant-data-plane reachability;
- high-impact changes correlate actor, request, tenant, policy, approval, desired state, actual state, result and rollback;
- partial provisioning is rolled back or quarantined; it does not become an ambiguous active resource;
- API inventory, testing, versioning, deprecation and credential removal are governed.

### 5.4 Orchestration and workload-runtime plane

Includes Kubernetes, Slurm, scheduler services, admission/job policy, node agents, runtimes, sandboxes, CNI/CSI/device plugins, operators, webhooks, prolog/epilog, SPANK, modules and workload telemetry.

Required patterns:

- private, patched and recoverable controllers/databases;
- least-privilege RBAC and service identities;
- restricted privileged workload/job, host, mount, device and network access;
- tenant namespace/account/partition/queue, quota, priority and reservation boundaries;
- topology-aware host/GPU/fabric/storage placement with tenant context;
- artifact and attestation admission where required;
- secrets and workload credentials delivered just in time and revoked on completion;
- runtime detection, node quarantine and known-good rebuild;
- controller, database and accounting backup/restore with tenant and integrity tests.

### 5.5 Compute, accelerator, fabric, storage and physical-root plane

Contains hosts, hypervisors, kernels, runtimes, GPUs/HBM/cache, accelerator partition/virtualization, NVLink topology, DPUs/NICs, Ethernet, InfiniBand/RDMA, storage, local media, BMC/OOB, racks and facilities.

Required patterns:

- every commercial SKU declares host, GPU, memory/cache, fault, reset, DMA, NVLink, Ethernet/RDMA, storage, telemetry and support properties;
- full-device dedication, hardware partitioning, virtualization and time-slicing are separate security products;
- time-slicing is not accepted as memory or fault isolation;
- hardware partitioning is not described as full-device or full-host dedication;
- allocation, reset, error containment, quarantine, local-state cleanup and tenant reassignment are tested on the exact hardware/firmware/driver/hypervisor/scheduler stack;
- packet, storage, management and direct-memory paths are independently isolated and tested;
- P_Key membership/enforcement, fabric-manager authority, DPU/NIC assignment, stale/partial state and cleanup are reconciled;
- BMC/OOB remains isolated from public, tenant and ordinary corporate networks;
- firmware identity, secure configuration, update, detection and recovery are governed;
- facilities, maintenance, custody, environment and emergency response are controlled;
- media and device sanitization uses a method appropriate to data sensitivity and device capability, with verification before reassignment/disposal.

### 5.6 Data, model and supply-chain plane

Governs datasets, prompts, outputs, models, checkpoints, adapters, embeddings, vector stores, caches, snapshots, backups, images, packages, operators, drivers, firmware, IaC, policies, skills, source, builds/training, registries and signing roots.

Required patterns:

- owner, purpose, rights, classification, tenant, jurisdiction, lifecycle and customer ownership are known;
- access is tenant-correct and linked to identity, purpose and policy;
- encryption and key ownership cover transit, storage, snapshots/backups and, where justified, use;
- source-to-use lineage and integrity are preserved;
- unsafe formats and unrestricted deserialization are rejected or isolated;
- release-critical artifacts have applicable inventory/BOM, provenance, signature, scanner, compatibility, policy, revocation and admission evidence;
- signatures are required only where policy says they are required; “unsigned when required,” unknown, revoked, incompatible or unapproved artifacts are rejected;
- build/train identities and environments are protected; approvals are separated; releases are staged and reversible;
- intermediate files, caches, credentials and temporary data are cleaned;
- export, retention, deletion, backup treatment, offboarding and recall are tested.

### 5.7 Telemetry, response, recovery and continuous-assurance plane

Collects and correlates required security-relevant telemetry from identity/policy, API/control plane, Kubernetes/Slurm, host/GPU/fabric/BMC, data/model, keys, artifacts/supply chain, support, agent, abuse, backup and recovery systems.

Required patterns:

- defined required-source inventory, event fields, source identity, time integrity, coverage, freshness and failure detection;
- tenant-safe collection, minimization, redaction, access, retention and legal hold;
- critical evidence exported to a boundary ordinary source administrators cannot silently alter;
- detections derived from current threat models and tested through authorized behavior replay;
- case and incident management linked to stable service/tenant/resource/evidence IDs;
- rapid command, reliable scope, identity/key revocation and containment at a trusted boundary;
- protected backup, restore, failover and known-good rebuild;
- independent verification and evidence-expiry/invalidation processing;
- self-monitoring of collectors, schemas, permissions, clocks, tests, evidence storage and verifier availability.

## 6. Trust zones and allowed communication

A typical deployment separates at least:

1. public edge;
2. tenant API and service front door;
3. provider privileged-access zone;
4. provider control-plane zone;
5. orchestrator-controller zone;
6. tenant workload/data plane;
7. storage plane;
8. Ethernet/fabric/RDMA plane;
9. BMC/OOB and hardware-management plane;
10. build/train/registry and supply-chain zone;
11. security evidence and response zone;
12. backup/recovery zone;
13. corporate IT and support environment.

Cross-zone flows require an explicit source principal or anonymous/untrusted classification, destination, protocol/interface, action, tenant/purpose where applicable, authentication requirement, authorization decision, rate/cost rule, encryption/integrity, telemetry, owner, failure behavior and expiry. “Any-to-any internal” is not an acceptable default.

Provider management, fabric, BMC/OOB, evidence and backup zones should not be directly reachable from tenant or public data planes. Corporate IT must not become an uncontrolled bridge into production roots.

## 7. End-to-end workflows

### 7.1 Tenant workload or training job

```text
1. Authenticate tenant subject and resolve organization/role.
2. Validate request schema, replay/idempotency, quota, cost and data classification.
3. Authorize object, action, tenant, purpose and context; issue request/decision IDs.
4. Verify image/code/model/checkpoint policy and required provenance/signature/scan.
5. Select permitted host/GPU/sharing/fabric/storage topology.
6. Write tenant-linked desired state.
7. Controllers reconcile actual state and report mismatch.
8. Issue scoped short-lived workload identity and secrets.
9. Admission/node enforcement revalidates artifact, identity and placement.
10. Correlate job, node, GPU, fabric, storage, data/model and policy events.
11. On completion/failure, revoke credentials and clean accelerator/local/fabric state.
12. Independently sample or test the resulting assertion and evidence.
```

A failed step must roll back, quarantine or leave an explicit recoverable state; ambiguous partial provisioning is a control failure.

### 7.2 Privileged provider operation

```text
identity + phishing-resistant MFA
→ ticket/purpose and risk context
→ JIT least-privilege grant
→ approved private access path
→ command/action policy
→ protected session and target evidence
→ post-action desired/actual verification
→ expiry/revocation
→ independent review for high-impact change
```

Break-glass is separate, tightly held, monitored, tested and reviewed after every use.

### 7.3 Agent tool execution

```text
agent identity + human/service delegator
→ approved use case and versioned components
→ goal, tenant/data/tool/egress/cost scope
→ typed tool request
→ policy and required deterministic approval
→ sandbox/resource enforcement where applicable
→ execution through scoped short-lived credential
→ protected security-relevant trace
→ output and post-condition validation
→ deterministic stop/rollback/manual recovery where risk requires
→ independent verifier for high-impact/adaptive claims
```

Low-impact assistive systems do not need every T4 mechanism, but every production agent remains inventoried, owned, scoped, monitored and attributable. High-impact systems cannot modify their own policy, approval authority, credentials, evidence or verifier.

### 7.4 Incident and recovery

```text
qualifying alert/report
→ establish command and secure communication
→ preserve evidence and establish reliable scope
→ revoke identity/key and contain at trusted boundary
→ assess tenant, privacy, legal and customer impact
→ quarantine compromised artifact/path/node/device/service
→ restore or rebuild from known-good state
→ verify identity, artifact, tenant isolation, data and monitoring
→ authorize reopening independently
→ notify as required and track remediation/retest
```

## 8. Failure-mode matrix

| Dependency failure | Unsafe behavior | Required design |
|---|---|---|
| Identity/federation unavailable | fail open or reuse unlimited stale sessions | bounded cached decisions only where justified; deny privilege/state-changing access; emergency path tested |
| Policy service unavailable | local components allow by default | signed/versioned policy cache with expiry; safe default deny/quarantine; explicit degradation |
| Controller/scheduler stale or partitioned | desired and actual tenant state diverge | versioned state, leases/epochs, reconciliation, mismatch quarantine and manual recovery |
| Fabric/DPU manager unavailable | stale P_Key/VRF/DPU assignment persists silently | freeze risky reallocation, independent path tests, recovery authority and cleanup evidence |
| KMS/HSM/PKI unavailable | bypass key policy or use embedded secrets | controlled degradation, protected recovery keys, short-lived cache where justified and tested recovery |
| Registry/build/provenance unavailable | unverified artifact admitted | trusted cached set with expiry or block admission; emergency decision remains nonconformant if T0 fails |
| Telemetry/evidence pipeline unavailable | activity interpreted as safe | detect source loss, preserve local buffer where safe, restrict high-impact action, reconcile after recovery |
| Backup/recovery dependency unavailable | restore begins from untrusted or incomplete state | dependency-aware plans, alternate roots/sources and tested manual path |
| Agent verifier unavailable | agent self-approves completion | high-impact/adaptive claim remains unverified; stop, queue or require qualified human verification |

## 9. Service-profile deltas

| Profile | Required architectural emphasis |
|---|---|
| GPU-IaaS | tenant-correct API, explicit sharing model, allocation lineage, host/GPU/fabric/storage cleanup and abuse/capacity control |
| Bare metal | BMC/OOB, firmware, provider-credential removal, dedicated/shared path statement, sanitization and custody |
| Managed Kubernetes | private API/etcd, RBAC/admission, CNI/CSI/device plugins/operators, workload identity, node response and restore |
| Managed Slurm/HPC | controller/database/auth, account/partition/QOS, prolog/epilog/SPANK/modules, shared storage/fabric, accounting/recovery |
| Model training | purpose/rights, data/experiment/model lineage, poisoning/integrity, safe checkpoint handling, temp/cache cleanup and export/deletion |
| Model serving | endpoint/model auth, tenant routing and cache/session isolation, extraction/abuse, rate/cost/capacity, fallback and rollback |
| Agent platform | delegation, component provenance, context separation, typed tools, policy, approval/stop, trace, revocation and independent verification proportional to impact |
| Sovereign/regulated | jurisdiction-bounded people, identity, keys, data, support, telemetry, backup, suppliers, response, recovery and evidence |

## 10. Implementation sequence

1. Define service profiles, boundaries, responsibility, identities and stable IDs.
2. Remove direct public/tenant reachability to provider administration, fabric and BMC/OOB.
3. Establish critical inventory, root protection, required telemetry, incident command and recovery sources.
4. Implement tenant-correct API authorization and desired/actual reconciliation.
5. Declare and test accelerator, fabric, storage and support isolation for every SKU.
6. Harden Kubernetes/Slurm, workload identity, artifact admission, node response and cleanup.
7. Establish data/model lifecycle, source-to-deploy provenance, revocation and recall.
8. Productize evidence, negative/failure tests, restore/rebuild/sanitization and assurance.
9. Add service-specific T3 dedicated, attested, confidential or sovereign assurance where justified.
10. Add T4 adaptive automation only after approval, stop, rollback, trace and verifier behavior are measured.

## 11. Architectural anti-patterns

- calling documentation or a dashboard a “unified control plane” without deployable enforcement and evidence;
- treating network location or Kubernetes namespace as identity or full tenant isolation;
- treating time-sliced GPUs as memory/fault-isolated tenants;
- treating MIG or other hardware partitioning as full-device/full-host dedication;
- relying on a VPC or NetworkPolicy to prove RDMA, DPU, storage or BMC isolation;
- shared provider identities or broad metadata credentials in tenant workloads;
- central policy/evidence services that cause silent fail-open;
- accepting every signed artifact without source, key-policy, compatibility and admission context, or rejecting every unsigned artifact without an explicit requirement;
- unbounded agent authority or an agent that approves/verifies itself;
- evidence stored only in the system being evaluated;
- backup without restore, sanitization without verification, or recovery without a reopening gate;
- a risk decision that overwrites the failed control result.

## 12. Definition of architectural readiness

The architecture is ready for a service only when:

- exact boundaries, profiles, versions, identities and responsibility are documented;
- every applicable T0 is independently `VERIFIED`;
- policy and tenant context reach each required enforcement point;
- prohibited API, host/GPU, fabric/RDMA/DPU, storage, support and OOB paths are tested;
- required telemetry and evidence sources are healthy, protected and independently inspectable;
- control-plane, identity/key, artifact, node, regional and evidence-pipeline failure behavior is known;
- restore/rebuild, revocation, incident, cleanup and sanitization exercises pass;
- customer claims describe exact dedicated/shared and provider/customer boundaries;
- high-impact agents have bounded authority, deterministic approval/stop, protected trace, recovery and independent verification.

Use the [Practice Guide](PRACTICE_GUIDE.md) for implementation sequencing and the [Metrics and Assurance Guide](METRICS_AND_ASSURANCE.md) for gates, evidence and measurements.
