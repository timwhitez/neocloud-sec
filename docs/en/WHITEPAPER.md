# NeoCloud Cyber Security White Paper

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented project draft

## Executive summary

“NeoCloud” is used in this project as a working industry term for specialized cloud providers that primarily serve accelerator-intensive artificial-intelligence and high-performance-computing workloads. The term is useful, but it does not yet have one formal, regulatory, or universally accepted definition. This white paper therefore defines its service boundary explicitly rather than relying on the label.

A NeoCloud commonly combines cloud APIs, physical GPU fleets, bare metal, hypervisors, Kubernetes, Slurm, high-throughput storage, Ethernet, InfiniBand/RDMA, NVLink-aware topology, DPUs, firmware, BMC/OOB management, model and artifact registries, data services, and increasingly capable AI agents. Expensive shared capacity, high-value data/models, multiple schedulers, direct-memory data paths, deep firmware/software supply chains, and machine-speed delegated action create failure modes that a generic enterprise or cloud checklist does not fully express.

NeoCloud Cyber Security is a **vendor-neutral security baseline, reference architecture, roadmap, and implementation guide** for this environment. It describes how an operator can design and run a coherent security control system in which identity and delegated authority establish the acting subject, policy governs trust decisions, enforcement occurs close to protected resources, and evidence plus independent verification determine whether an outcome is actually true.

This repository is not a deployable security product, formal standard, certification scheme, legal opinion, or proof that any provider is secure. It is a project-authored draft intended to make service boundaries, risks, controls, evidence, verification, responsibility, and development priorities explicit and testable.

The baseline contains 90 controls across 18 domains and five adoption tiers. T0 controls are hard production gates; every applicable T0 must be independently `VERIFIED`. T1 establishes ownership, scope, hygiene, visibility, response, and recovery foundations. T2 turns controls into scalable platform capabilities. T3 adds independently supportable higher assurance for sensitive, regulated, sovereign, dedicated, attested, or confidential-computing profiles where justified. T4 is reserved for guarded adaptive automation and continuous verification after authority, approval, stop, rollback, trace, and verifier controls have been proven.

No score, compensating control, risk acceptance, or executive decision can turn a failed applicable T0 into a conformant result. An authorized executive may record a time-bounded emergency business-continuity decision, but the control remains failed and the service remains nonconformant under this baseline until the gate is independently verified.

## 1. Objective and system boundary

The objective is to preserve trustworthy decisions throughout the service lifecycle:

```text
design → source → build/train → provision → authenticate/delegate
→ schedule → execute → observe → respond → recover
→ export/delete → sanitize → decommission
```

Security is a system property across this chain. Strong API authentication cannot compensate for incorrect object/tenant authorization. A hardened Kubernetes cluster cannot prove Slurm, RDMA, storage, or GPU isolation. An artifact signature cannot prove safe source, build, review, key custody, policy, or runtime behavior. An available backup cannot prove identity, integrity, tenant isolation, or recoverability. A model-generated success statement cannot prove that an agent completed an authorized task safely.

The project covers provider-operated and customer-facing components that materially affect confidentiality, integrity, availability, privacy, tenant isolation, abuse resistance, sovereignty, safety, recoverability, or customer assurance. A service may select multiple profiles:

| Service profile | Typical boundary | Principal security emphasis |
|---|---|---|
| **GPU-IaaS** | Tenant VM/container on a provider accelerator fleet | API authorization, host/GPU/fabric/storage isolation, image provenance, allocation and reset |
| **Bare-Metal-GPU** | Tenant receives one or more physical hosts | provisioning/deprovisioning, BMC/OOB, firmware, dedicated/shared boundaries, sanitization |
| **Managed-Kubernetes** | Provider manages the control plane and often nodes | tenant RBAC, admission, plugins/operators, workload identity, node/GPU isolation, recovery |
| **Managed-Slurm-HPC** | Provider manages scheduler, partitions, nodes, accounting | controller/authentication, account/job isolation, queue/fabric/storage, accounting and recovery |
| **Model-Training** | Managed datasets, jobs, checkpoints, experiment services | rights/purpose, lineage, poisoning/integrity, safe formats, temporary data, export/deletion |
| **Model-Serving** | Managed model endpoints, routing, cache and runtime | endpoint/model authorization, tenant routing/cache, extraction/abuse, quota and resilience |
| **Agent-Platform** | Managed agents, tools, memory, skills and connectors | delegation, external-content boundaries, tool policy, approval, stop, trace and verification |
| **Sovereign-Regulated** | Jurisdiction-bounded people, data, keys and operations | complete jurisdiction boundary, support, telemetry, suppliers, recovery and assurance |

Customer-controlled systems outside the contracted boundary are out of direct provider scope, but may remain dependencies or shared responsibilities. Legal conclusions, model-quality evaluation unrelated to security, and claims of certification are also outside this document.

## 2. Why NeoCloud security is distinct

### 2.1 Accelerator sharing creates several different products

A GPU may be assigned as a full dedicated device, partitioned by supported hardware mechanisms, virtualized, or shared through scheduler time-slicing. These are not interchangeable security boundaries.

- **Full-device dedication** can reduce co-residency, but still depends on host, reset, local storage, network/fabric, telemetry, support, and reassignment controls.
- **Hardware partitioning**, such as supported MIG configurations, may provide dedicated compute and memory resources within a device; it is not the same as full-device or full-host dedication and remains dependent on the exact GPU, firmware, driver, virtualization, topology, scheduler, and operational workflow.
- **Virtualization** depends on the specific mediated/passthrough architecture and its host, IOMMU, driver, management, and reset path.
- **Time-slicing** shares a GPU through scheduling and does not provide memory or fault isolation between replicas; it must not be marketed or accepted as a hardware tenant-isolation boundary.

Every commercial SKU must state and test host, GPU/HBM/cache, DMA, fault, reset, NVLink topology, network/RDMA, storage, telemetry, support, and cleanup properties. Sensitive workloads must use a mode justified by the threat model and customer commitment.

### 2.2 High-performance paths can bypass ordinary assumptions

Training clusters optimize away overhead. Ethernet overlays, storage networks, InfiniBand P_Keys, RDMA, DPUs/NICs, NVLink domains, BMC/OOB, and vendor controllers may each form a trust boundary. A correct VPC or Kubernetes NetworkPolicy does not prove the RDMA, DPU, storage, or management path.

P_Key membership is one relevant InfiniBand isolation control, but it relies on correctly governed fabric-management components, membership configuration, endpoint behavior, and actual enforcement. The provider must protect the subnet/fabric manager, reconcile intended and actual assignments, test prohibited paths, detect stale/partial state, and verify cleanup during tenant reallocation.

### 2.3 Cloud and HPC control models coexist

A tenant request may cross an API gateway, identity and policy systems, provisioning databases, Kubernetes operators, Slurm controllers, image factories, node agents, network/fabric controllers, storage systems, and billing/quota services. Each translation creates risk of object, action, tenant, purpose, or state confusion. Stable request, tenant, workload, job, node, device, data, artifact, policy, and evidence identifiers are therefore core security controls.

### 2.4 Data, models, and intermediate state are both assets and attack surfaces

Datasets, prompts, outputs, model weights, checkpoints, adapters, embeddings, vector stores, KV caches, agent memory, experiment metadata, logs, snapshots, and backups may contain intellectual property, personal data, credentials, or operational secrets. Models and checkpoints may also include unsafe serialization or poisoned behavior.

Protection must address purpose and rights, tenant-correct access, encryption and key ownership, lineage and integrity, safe formats/loaders, temporary state, output/export, privacy, residency, retention, deletion, backup treatment, and offboarding—not only storage encryption.

### 2.5 The trusted supply chain is deep and privileged

The trusted computing base can include firmware, BMCs, DPUs, NICs, GPU drivers, kernels, hypervisors, runtimes, Kubernetes/Slurm components, device plugins, operators, images, packages, infrastructure code, model-serving frameworks, model/checkpoint formats, prompts, policies, skills, build systems, registries, and signing roots.

The operator must know what is running, where it came from, which identity produced and approved it, what evidence supports it, what can revoke it, and how to recall, quarantine, roll back, or rebuild it. A valid signature proves that a key signed bytes; it does not prove the source, review, key policy, runtime behavior, or safety of those bytes.

### 2.6 Agents change authorization and failure speed

Agents may read data, execute code, call infrastructure or business tools, change resources, communicate externally, and make repeated decisions at machine speed. Controls must scale with authority and impact rather than applying the same heavyweight mechanism to every AI feature.

Every production AI system or agent requires an owner, identity, use case, model/prompt/RAG/memory/skill/tool inventory, data and tenant scope, delegated authority, impact assessment, monitoring, and incident path. Tool-using systems additionally require typed interfaces, policy mediation, least privilege, short-lived credentials where feasible, egress/data/cost controls, and revocation. High-impact, destructive, external, customer-affecting, expensive, or irreversible actions require deterministic approval and explicit stop/containment behavior. Adaptive or autonomous security workflows further require immutable goals/scope, protected replayable traces, budget/time/repetition/uncertainty stops, rollback or manual recovery, and an independent verifier that the agent cannot modify.

External content—including prompts, documents, tickets, web pages, packages, models, RAG data, memory, and tool output—provides observations, not authority. It cannot expand identity, goal, scope, tools, credentials, policy, approval, budget, evidence, or verifier authority.

### 2.7 Scarce capacity attracts abuse and availability attacks

Fraudulent onboarding, credential resale, cryptomining, prohibited workloads, quota bypass, queue manipulation, capacity hoarding, model extraction, denial of wallet, DDoS, dependency failure, and destructive automation can affect security, safety, customers, and economics simultaneously. Tenant trust, acceptable use, quotas/rates/cost/concurrency, egress, capacity engineering, fair enforcement, incident response, and appeal therefore belong in the baseline.

## 3. Assets, roots of trust, and threat actors

A complete inventory must cover:

- tenant organizations, users, owners, federation, quotas, billing, support and emergency contacts;
- human administrators, service/workload/device/agent identities, API keys, certificates, break-glass and signing/recovery roots;
- APIs, controllers, schedulers, databases, operators, policy engines, CI/CD, support systems and evidence pipelines;
- hosts, hypervisors, kernels, runtimes, BMCs, DPUs/NICs, GPUs/HBM, local media, networks/fabrics, racks, regions and utilities;
- images, packages, firmware, drivers, operators, IaC, SBOMs, provenance, signatures, models, checkpoints, prompts, skills and policies;
- customer data/model artifacts, caches, outputs, logs, snapshots, backups, deletion and sanitization state;
- suppliers, SaaS, IdPs, registries, repositories, remote support and critical facilities.

Each critical object needs an accountable owner, service and tenant relationship, identity, location, lifecycle, expected state, classification, dependencies, telemetry, recovery, and disposal method. Unknown critical scope is a failed assertion, not an item to omit from the denominator.

Threat actors include external attackers, malicious or compromised tenants, fraudulent customers, compromised workloads/models/agents, insiders, support personnel, compromised provider identities, supply-chain actors, malicious or failed automation, jurisdictional actors, and physical attackers. Baseline failure classes include:

| Failure class | Examples | Principal consequences |
|---|---|---|
| Identity/API | stolen credential, federation error, broken object or tenant authorization | takeover, cross-tenant access, fraudulent consumption |
| Provider control plane | public admin path, vulnerable controller/operator, leaked automation identity | fleet-wide compromise, persistence, destructive change |
| Compute/runtime | VM/container escape, privileged job, host compromise | access to host, peers, credentials or devices |
| Accelerator | memory remanence, unsafe sharing, reset/error failure, side channel | data/model exposure and cross-allocation impact |
| Fabric/storage | incorrect VRF/VXLAN/P_Key/DPU/storage assignment, RDMA bypass | direct cross-tenant reachability or corruption |
| Data/model | theft, poisoning, unsafe format/deserialization, deletion failure | IP/privacy loss, code execution, model compromise |
| Supply chain | poisoned package/image/operator/driver/firmware/model/skill | privileged compromise at scale |
| Agent/tool | prompt injection, confused deputy, excessive authority, false completion | exfiltration, unauthorized action, destruction |
| Abuse/capacity | fraud, quota/cost bypass, hoarding, DDoS | financial loss, service degradation, legal/safety harm |
| Insider/support | standing privilege, covert access, evidence tampering | high-confidence access and loss of assurance |
| Recovery/availability | ransomware, regional/fabric failure, bad automation, unusable backup | prolonged outage, data loss, unsafe reopening |
| Physical/firmware | BMC compromise, rogue component, malicious maintenance | persistent control below the OS |

Threat modeling must cover normal and prohibited flows, dependency and controller failure, stale or partial state, operator error, malicious configuration, recovery, and evidence integrity. Catastrophic cross-tenant, root-of-trust, destructive, or irrecoverable failures must not be averaged away by an aggregate risk score.

## 4. Security principles

1. **Identity and delegation before location.** Authenticate and authorize people, tenants, services, workloads, devices, agents, and automation independently of network location.
2. **Least privilege is time-, task-, tenant-, purpose-, and resource-bound.** Prefer short-lived credentials, sessions, and delegated authority where technically feasible.
3. **Tenant isolation is end to end.** Test API, control plane, scheduler, host, GPU, storage, cache, telemetry, Ethernet, RDMA, DPU, OOB, and support paths.
4. **Sharing modes are explicit products.** Do not collapse full-device, hardware-partitioned, virtualized, and time-sliced services into one “isolated GPU” claim.
5. **Provider-exclusive controls remain provider responsibilities.** A customer cannot secure infrastructure it cannot access or govern.
6. **External content is untrusted data, not authority.** Authorization comes from identities, delegation, policy, and approved decisions.
7. **Evidence belongs to the control.** A deployed mechanism is not effective until scope, failure behavior, negative tests, freshness, and independent verification support the claim.
8. **Assume compromise and constrain blast radius.** Design rapid revocation, isolation, quarantine, rebuild, recall, and customer-safe evidence collection.
9. **Recovery restores trust, not only availability.** Verify identity, artifacts, data, tenant isolation, monitoring, and objectives before reopening.
10. **Automation earns authority.** Add autonomy only when approval, stop, rollback, trace, budget, and verifier behavior are demonstrated.
11. **Complexity must earn its cost.** Prefer general mechanisms—identity, policy, isolation, provenance, evidence, recovery, feedback, and verification—over brittle exceptions.
12. **State uncertainty precisely.** Avoid unsupported terms such as “complete,” “immutable,” “dedicated,” “confidential,” or “zero trust” without a scope and evidence contract.

## 5. Operating model and shared responsibility

The executive risk owner sets risk appetite and makes exceptional business decisions. A CISO or equivalent owns the program. Each customer-facing service has accountable business, technical, security, data, and incident owners. Platform teams own reusable capabilities; service teams remain responsible for correct adoption and service claims.

Three functions must remain distinct even in a small organization:

- **Implementation and operation:** product, platform, infrastructure, SRE, network, facilities, data and AI teams.
- **Policy, risk, privacy and challenge:** security, privacy, legal/risk and compliance functions.
- **Independent verification:** a separate person/team, observation path, test harness, or qualified assessor able to challenge the implementer.

The provider cannot transfer responsibility for BMC/OOB, fabric managers, host reset, provider control planes, signing roots, or other exclusively controlled infrastructure to customers. Customers remain responsible for their code, data classification, role assignment, guest/workload configuration, and use unless the contract assigns those duties to the provider. Every service must publish normal-operation and incident responsibilities for identity, workload, data/model, GPU/fabric, logging, support, backup/restore, export/deletion, evidence, and end of service.

## 6. Reference architecture

The target security system consists of seven cooperating planes:

1. **Governance and assurance:** services, scope, obligations, responsibility, risks, decisions, exceptions, control state, evidence and assurance.
2. **Identity and policy:** human/tenant/service/workload/device/agent identity, federation, PKI, JIT privilege, delegation, policy decisions and approval.
3. **Edge and control plane:** public APIs, support and privileged access, provisioning, quota/billing, controllers and administrative interfaces.
4. **Orchestration and runtime:** Kubernetes, Slurm, admission/job policy, scheduler, runtime, node agents, sandboxing and workload controls.
5. **Compute, fabric, storage and physical roots:** hosts, hypervisors, accelerators, DPUs/NICs, Ethernet, InfiniBand/RDMA, NVLink topology, storage, BMC/OOB, facilities, reset and sanitization.
6. **Data, model and supply chain:** source, build/train, registries, SBOM/provenance/signing, datasets, models, checkpoints, prompts, skills, policies, safe loading and release.
7. **Telemetry, response and recovery:** required logs/traces, inventory and reconciliation, detections, cases, protected evidence, revocation, containment, backup, restore and known-good rebuild.

Policy enforcement should remain close to the protected resource; a central decision or evidence service must not create a silent fail-open path. Stable identifiers correlate the subject, delegation, tenant, request, policy version, desired state, actual state, workload/job, host/GPU/fabric/storage assignment, data/model access, result, cleanup, and evidence.

No component is trusted to prove its own effectiveness solely through its own dashboard. Critical evidence should be exported to a boundary that ordinary source administrators cannot silently alter, while preserving tenant partitioning, minimization, privacy, retention, legal hold, time integrity, and access audit.

## 7. Security domains

The 18 domains cover:

1. governance, risk, compliance and shared responsibility;
2. asset, service, dependency and data-flow inventory;
3. human, tenant, workload and agent identity;
4. control plane, API and administrative interfaces;
5. network, fabric, RDMA/InfiniBand and DPU isolation;
6. compute, hypervisor, bare metal, GPU and accelerator isolation;
7. Kubernetes, containers, Slurm and schedulers;
8. data, datasets, models, artifacts and privacy;
9. secrets, keys, PKI, attestation and confidential computing;
10. software, model and infrastructure supply chain;
11. secure engineering, IaC, change and configuration;
12. vulnerability, exposure, patch and firmware management;
13. telemetry, detection engineering, threat intelligence and audit;
14. AI application, agent, tool, skill and prompt security;
15. abuse prevention, tenant trust, egress and acceptable use;
16. incident response, forensics, crisis management and recovery;
17. resilience, availability, capacity, backup and disaster recovery;
18. physical, facility, BMC, hardware lifecycle and media sanitization.

The [Security Baseline](SECURITY_BASELINE.md) defines the stable IDs and production gates. The machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json) supplies bilingual requirements, evidence and verification profiles, tier frequency, and metric associations.

## 8. Tiers, verification, and exceptions

| Tier | Purpose | Default verification model |
|---|---|---|
| **T0 Guardrails** | hard production gates | continuous monitoring where feasible; independent verification at least quarterly and after material change |
| **T1 Foundation** | ownership, scope, hygiene, visibility, response and recovery | at least quarterly and after material change |
| **T2 Production** | reusable, enforced and measured controls | at least semi-annually and after material change |
| **T3 Assured** | service-specific higher assurance | at least annually, independently, and after material change |
| **T4 Adaptive** | guarded adaptive automation | continuous metrics plus quarterly adversarial and failure-mode review |

The control lifecycle is:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

`IMPLEMENTED` establishes deployment, not effectiveness. Only an independent validator returning `PASS` for the exact service, version, region, asset/tenant scope, test, evidence and validity period may assign `VERIFIED`. `FAIL`, `INCONCLUSIVE`, `NOT_TESTED`, stale evidence, material change, or inability to reproduce the assertion invalidates the prior result.

An exception record may document operation outside a requirement, but it cannot change the requirement or result. An applicable T0 exception remains a failed/nonconformant gate. External assurance must state the scope, date, version, limitations, failed tests, exceptions, and verifier rather than presenting one blended score.

## 9. Lifecycle integration

### Design

Define service profiles, tenant and trust boundaries, isolation SKU, data classes and purpose, jurisdiction, responsibility, abuse cases, SLO/RTO/RPO, evidence contract, failure behavior, recovery, deletion, and decommissioning before implementation. Security requirements are release acceptance criteria.

### Source, build, train and release

Protect source and build identities; review infrastructure and policy as code; isolate high-impact builds; inventory direct and transitive dependencies; produce appropriate BOM/provenance/signatures; govern datasets, models, prompts, skills, drivers and firmware; admit only artifacts meeting policy; stage deployments; observe declared signals; and test recall and rollback.

### Provision, schedule and execute

Authenticate subject and tenant; evaluate action, object, purpose, context, isolation and cost policy; issue an immutable request/correlation ID; assign network/fabric/storage/host/accelerator resources with tenant identity; compare desired and actual state; issue scoped short-lived workload credentials; revalidate artifact and placement at admission/node boundaries; correlate runtime events; and clean credentials, accelerator/local state and assignments on completion.

### Observe and respond

Collect defined security-relevant telemetry; monitor source coverage and freshness; preserve evidence; establish incident command; determine reliable scope; contain at the strongest trusted boundary; revoke identities/keys; quarantine artifacts, nodes, devices, paths, data or tenants; assess customer/regulatory impact; and record decisions.

### Recover, delete and decommission

Prefer revocation and known-good rebuild when a root cannot be trusted. Restore or rebuild against RTO/RPO while verifying identity, artifact integrity, tenant isolation, data correctness and monitoring. Execute authorized export/deletion, apply backup retention policy, sanitize media and accelerator/host state according to risk and device capability, remove network/fabric assignments and credentials, and preserve chain-of-custody evidence.

## 10. Evidence and continuous assurance

A useful evidence item identifies:

- control and human-readable assertion;
- service/profile, environment, region, version, tenant/asset/data scope;
- collector identity, source system, method/query/test version and time;
- result, limitations, sampling and blind spots;
- integrity protection and protected location;
- validity period and invalidation triggers;
- validator, test result, findings and retest date.

Evidence strength generally increases from statement, to screenshot/manual report, to reproducible query/export, to protected runtime event or verified attestation, to authorized negative/failure/recovery test, to independent reproduction through a separate observation path. The exact evidence must match the assertion; a numeric evidence score never replaces judgment or a hard gate.

Continuous assurance combines inventory reconciliation, policy evaluation, exposure discovery, required-source health, isolation tests, revocation and restore exercises, detection replay, artifact recall, sanitization evidence, agent adversarial evaluation, exception expiry, and independent sampling. The system must detect failures of its own collectors, schemas, permissions, clocks, evidence store, tests and verifier.

## 11. Development roadmap

A typical program progresses through evidence gates rather than dates alone:

1. **Days 0–7:** establish owners, incident command, critical inventory, change freezes and emergency revocation.
2. **Days 8–30:** remove critical public/admin exposure; implement phishing-resistant privileged access, private management, explicit SKU isolation, root protection, required telemetry and core playbooks.
3. **Days 31–90:** establish authoritative service/asset/identity/data/model/dependency inventories, shared responsibility, lifecycle processes, vulnerability/exposure management, backup dependencies and desired/actual reconciliation; independently verify every applicable T0.
4. **Months 3–6:** productize workload identity, policy as code, trusted artifacts, reconciliation, node/runtime response, evidence automation, tenant trust and secure engineering.
5. **Months 6–12:** close T2 gaps; perform cross-tenant, accelerator, fabric, recovery, detection, incident and customer-notification exercises.
6. **Months 12–18:** add T3 controls justified by dedicated, sensitive, regulated, sovereign, attested or confidential-computing commitments; independently test roots, isolation, suppliers and recovery.
7. **Months 18–24:** add T4 guarded adaptive automation only when precision, approval bypass, scope violation, false completion, rollback, kill switch and independent-verifier behavior are measurable.

The [Roadmap](ROADMAP.md) defines workstreams, dependencies, exit gates and build/buy guidance. Calendar targets are references; production exposure must not wait for a future phase when a T0 fails today.

## 12. Customer and ecosystem transparency

A trustworthy provider should be able to supply, under appropriate confidentiality:

- exact service boundary, profile, region and version;
- current provider/customer/shared responsibility;
- host, GPU/HBM/cache, NVLink, network/RDMA, storage, telemetry, BMC and support sharing/isolation statements;
- data/model purpose, access, encryption/key ownership, residency, retention, export and deletion behavior;
- support-access, vulnerability, incident, notification and evidence-exchange commitments;
- artifact and firmware provenance approach;
- backup, restore, rebuild, offboarding and sanitization behavior;
- independent tests, evidence validity, material findings, exceptions and remediation dates;
- suppliers, subprocessors and critical dependencies relevant to the claim.

Claims must be precise. “Dedicated” must identify each dedicated and shared resource. “Encrypted” must identify where plaintext exists and who controls key release. “Confidential” must identify the threat model, hardware/software/attestation boundary, unsupported components, and key-release policy. “Zero trust” must identify subjects, policies, enforcement points, failure behavior and verification. “Compliant” must identify the exact obligation, scope, assessor, date and exceptions.

## 13. Build, buy, and integrate

Build or deeply integrate controls that encode NeoCloud-specific tenancy and topology: tenant-aware authorization; desired/actual reconciliation; GPU/NVLink/fabric/DPU/storage/scheduler placement evidence; reset/sanitization; model/checkpoint lifecycle and safe loading; agent delegation and tool mediation; service-specific containment and reopening.

Mature components may be bought or adopted where interfaces and evidence are strong: IdP/MFA, PAM, KMS/HSM, secret management, PKI, vulnerability and attack-surface management, SIEM/data lake, runtime detection, case management, backup, DDoS/WAF/API gateway, signing and transparency infrastructure.

A vendor dashboard does not prove coverage. Require exportable data and APIs, stable identities, tenant-safe behavior, secure update, HA and safe degraded mode, failure detection, incident notification, data handling, independent testing, migration/exit, and evidence that can be correlated to the service boundary.

## 14. Limitations

This baseline is broad by design and cannot encode every product, jurisdiction, service contract, hardware generation, driver/firmware combination, threat actor, or safety requirement. Some evidence targets are reference starting points rather than universal thresholds. Draft and vendor sources inform the project but are not automatically normative. A control mapping is not certification. A passed baseline does not eliminate risk, and a failed control should not be hidden behind false precision.

Organizations must adapt the controls to a current service threat model, obtain qualified legal/privacy/safety/audit advice, test the actual deployed path, state uncertainty, and keep assurance time-bound.

## 15. Conclusion

NeoCloud security is the discipline of preserving trustworthy, tenant-correct and recoverable decisions across physically dense, highly shared, software-defined, supply-chain-dependent and increasingly autonomous AI infrastructure.

The minimum viable program is an explicit service boundary; accountable responsibility; strong identities and delegation; precise accelerator, fabric and storage isolation; protected data/models and artifacts; required telemetry; tested response, recovery and sanitization; risk-proportionate agent controls; and evidence that survives independent challenge.

Start with T0 production gates. Build T1 ownership and visibility. Convert T2 into reusable platform services. Add T3 only where consequences or commitments justify higher assurance. Introduce T4 adaptive automation only after its authority and failure modes can be measured and constrained. This sequence lets security scale with compute, models, agents, customers and regulation without turning every new risk into another unverifiable exception.

## Disclaimer

This project-authored white paper is an implementation-oriented draft. It is not a certification, formal standard, legal opinion, guarantee, or substitute for applicable law, regulation, contract, privacy assessment, safety assessment, product documentation, or qualified independent audit. External-framework mappings and source references are informative and must be validated for the organization, service, jurisdiction, version and assurance objective in use.
