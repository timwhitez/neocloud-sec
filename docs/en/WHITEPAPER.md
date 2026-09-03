# NeoCloud Cyber Security White Paper

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** Implementation-oriented public draft

## Executive summary

NeoClouds are specialized, AI-first cloud platforms optimized for accelerator-heavy training, inference, high-performance computing, and agentic workloads. They combine cloud APIs with physical GPU fleets, bare metal, Kubernetes, Slurm, high-throughput storage, Ethernet, InfiniBand/RDMA, NVLink domains, DPUs, firmware, model registries, data services, and increasingly autonomous AI systems. This concentration of expensive capacity and high-value data creates a security problem that is materially different from conventional enterprise IT and cannot be solved by adding a generic cloud checklist to a GPU platform.

NeoCloud Cyber Security defines a unified cybersecurity control plane for this environment. Identity is the root of trust; policy is the decision core; people, tenants, workloads, devices, and AI agents are first-class security subjects. Controls span endpoint and administrative access, control planes, cloud-native runtime, GPU and fabric isolation, data and model protection, software and model supply chains, security operations, resilience, and physical infrastructure. The desired outcome is a closed loop from visibility, to policy decision, to preventive or responsive enforcement, to durable evidence and independent verification.

The baseline is designed around five adoption tiers and eighteen security domains. T0 controls are hard production guardrails. T1 establishes complete ownership and minimum viable visibility. T2 turns controls into scalable platform capabilities. T3 provides higher assurance for regulated, sovereign, sensitive, or dedicated services. T4 introduces continuous verification, confidential-computing patterns, and guarded automation. No aggregate score may compensate for a failed T0 control.

This document is intentionally implementation oriented. It defines the security problem, architecture, operating model, threat model, baseline, roadmap, evidence model, and provider/customer responsibilities. The companion [Security Baseline](SECURITY_BASELINE.md), [Practice Guide](PRACTICE_GUIDE.md), [Reference Architecture](REFERENCE_ARCHITECTURE.md), [Roadmap](ROADMAP.md), and [Metrics and Assurance Guide](METRICS_AND_ASSURANCE.md) convert the model into deployable work.

## 1. Definition and objective

**NeoCloud Cyber Security is a unified cybersecurity control plane for AI-native organizations and specialized AI clouds. It treats identity as the root of trust, policy as the decision core, and agents plus workloads as first-class security subjects. It coordinates endpoint, cloud-native runtime, network and fabric, data, software/model supply chain, and security operations controls to close the loop from visibility to real-time enforcement and continuous assurance.**

The objective is not to build one more security product. It is to establish a coherent set of trust decisions and verifiable outcomes across the complete service lifecycle:

`design → source → build → provision → authenticate → schedule → execute → observe → respond → recover → delete → decommission`

A NeoCloud is secure only when these decisions remain consistent across layers. Strong API authentication cannot compensate for weak GPU reset. A hardened Kubernetes cluster cannot compensate for a shared InfiniBand partition. Signed images cannot compensate for a compromised signing key. An incident-response policy cannot compensate for absent control-plane logs. Security is therefore treated as a system property rather than a collection of disconnected tools.

## 2. Why NeoCloud security is distinct

### 2.1 Shared accelerators create nontraditional tenant boundaries

A GPU may be dedicated, partitioned through hardware mechanisms, virtualized, or shared through scheduler time slicing. These modes are not equivalent. Isolation claims must cover device memory, caches, DMA, driver state, error containment, reset behavior, telemetry, and placement topology—not merely process or container separation. Sensitive workloads must never be placed on a sharing mode whose isolation properties do not meet the declared service commitment.

### 2.2 High-performance fabrics can bypass ordinary controls

Training clusters use high-bandwidth, low-latency fabrics whose operational goal is to remove bottlenecks. Ethernet overlays, storage networks, InfiniBand P_Keys, RDMA, NVLink domains, DPUs, and out-of-band management may each form a distinct trust boundary. A correct VPC policy does not prove that an RDMA path, fabric manager, or DPU assignment is isolated. Security validation must exercise the actual data paths.

### 2.3 Cloud and HPC control models coexist

Kubernetes and Slurm express identity, tenancy, scheduling, quotas, and isolation differently. A single service may involve a public API, an internal provisioning system, Kubernetes operators, Slurm controllers, image factories, node agents, and vendor management components. Authorization must remain tenant-correct across every translation and reconciliation step.

### 2.4 AI data and models are crown jewels and attack surfaces

Training datasets, private prompts, model weights, checkpoints, adapters, embeddings, vector stores, inference inputs and outputs, agent memory, KV caches, and evaluation data may contain intellectual property, personal data, credentials, or operational secrets. Models and checkpoints may also contain malicious serialized objects or poisoned behavior. NeoCloud security must protect confidentiality, integrity, provenance, retention, deletion, and safe loading—not only storage encryption.

### 2.5 The infrastructure supply chain is deep and privileged

The trusted computing base includes firmware, BMCs, DPUs, NICs, GPU drivers, kernels, hypervisors, container runtimes, Kubernetes and Slurm components, device plugins, operators, images, packages, infrastructure code, model-serving frameworks, model formats, and build/signing systems. A provider must know what is running, where it came from, who approved it, and how compromise can be contained or rolled back.

### 2.6 AI agents change the unit of authorization

An agent can read data, call tools, execute code, modify infrastructure, communicate externally, and make decisions at machine speed. The traditional distinction between “application” and “administrator” becomes insufficient. Each agent requires an identity, declared goal, immutable scope, authorized tools, short-lived credentials, approval boundaries, budgets, deterministic stop conditions, complete action traces, and an independent verifier. External content must never silently alter its goal, permissions, hooks, skills, or policy.

### 2.7 Scarce capacity invites abuse and availability attacks

GPU capacity can be stolen, hoarded, resold, used for prohibited workloads, or exhausted through denial-of-wallet attacks. Queue manipulation, fraudulent accounts, credential resale, cryptomining, malicious model serving, DDoS, and dependency failures can harm both safety and economics. Abuse prevention, tenant trust, rate limits, quotas, egress controls, capacity engineering, and incident response therefore belong in the cyber baseline.

## 3. Scope and service profiles

The baseline applies to provider-operated and customer-facing components that materially affect confidentiality, integrity, availability, privacy, tenant isolation, safety, sovereignty, or recoverability.

| Service profile | Typical boundary | Principal security emphasis |
|---|---|---|
| **GPU-IaaS** | Tenant VM/container on provider accelerator fleet | identity, API correctness, host/GPU/fabric isolation, image provenance, secure reset |
| **Bare-Metal-GPU** | Tenant receives one or more physical hosts | provisioning, BMC isolation, firmware state, network/fabric segmentation, sanitization |
| **Managed-Kubernetes** | Provider manages control plane and often nodes | tenant RBAC, admission, runtime security, secret handling, node/GPU isolation |
| **Managed-Slurm-HPC** | Provider manages scheduler, partitions, nodes, accounting | controller security, user/job isolation, modules, shared storage, queue/fabric controls |
| **Model-Training** | Managed data, jobs, checkpoints and experiment services | data/model lineage, poisoning resistance, workload identity, artifact integrity, privacy |
| **Model-Serving** | Managed endpoints, routing, cache and model runtime | API abuse, model authorization, prompt/output handling, cache isolation, availability |
| **Agent-Platform** | Managed agents, tools, memory, skills and connectors | delegated authority, prompt injection, tool policy, approval, audit, stop and verification |
| **Sovereign-Regulated** | Jurisdiction-bounded people, data, keys and operations | residency, personnel, cryptographic control, support boundaries, evidence and assurance |

A service may select more than one profile. Applicability must be recorded explicitly; “not applicable” requires a rationale and reviewer.

Out of scope are customer-controlled systems beyond the contracted boundary, legal conclusions, model-quality assurance unrelated to security, and claims that a mapping alone establishes certification. These may still be dependencies or shared responsibilities.

## 4. Assets and crown jewels

A NeoCloud asset model must include logical, physical, human, and informational assets. At minimum:

- tenant accounts, organizations, quotas, billing state, support identities, and federation mappings;
- human administrators, break-glass accounts, service accounts, workload identities, agent identities, API keys, certificates, and signing roots;
- public APIs, administrative interfaces, provisioning systems, schedulers, controllers, operators, admission systems, policy engines, and CI/CD;
- hosts, hypervisors, kernels, containers, BMCs, DPUs, NICs, GPUs, HBM, local disks, fabrics, racks, regions, and availability zones;
- images, packages, firmware, drivers, operators, infrastructure code, SBOMs, provenance records, signatures, and transparency evidence;
- customer datasets, prompts, outputs, models, adapters, checkpoints, embeddings, caches, experiment metadata, logs, snapshots, and backups;
- security telemetry, incident evidence, detection content, vulnerability state, exception records, and assurance reports;
- third-party SaaS, identity providers, package registries, source repositories, hardware suppliers, remote support paths, and critical utilities.

Asset inventory is not a spreadsheet exercise. Each critical asset must have an owner, service relationship, tenant scope, identity, location, lifecycle state, data classification, dependency edges, expected configuration, telemetry source, and recovery or disposal method.

## 5. Threat model

NeoClouds must consider external attackers, malicious or compromised tenants, insiders, compromised provider identities, supply-chain actors, fraudulent customers, compromised workloads, models and agents, and jurisdictional or physical threats. The following failure classes are baseline design inputs.

| Threat class | Representative failure | Potential impact | First-line controls |
|---|---|---|---|
| Account and API compromise | stolen credential, broken object-level authorization, support impersonation | tenant takeover, cross-tenant access, fraudulent consumption | phishing-resistant MFA, federation, tenant-correct authorization, JIT access, immutable audit |
| Control-plane takeover | exposed admin interface, vulnerable operator, leaked automation token | fleet-wide compromise and persistence | private management plane, workload identity, policy gates, hardened controllers, rapid revocation |
| Compute escape | container/VM escape, privileged workload, host compromise | access to host, peer workloads, credentials or devices | hardened isolation, admission policy, patched runtime, EDR/runtime detection, placement controls |
| Accelerator leakage | memory remanence, unsafe sharing, weak reset, side channel | model/data exposure across jobs or tenants | documented SKU isolation, dedicated/MIG-class options, reset verification, adversarial testing |
| Fabric boundary failure | wrong VRF/VXLAN/P_Key/DPU assignment or RDMA bypass | direct cross-tenant network or storage reachability | default deny, plane separation, controller reconciliation, end-to-end path tests |
| Data/model compromise | theft, poisoning, malicious format, unsafe deserialization | privacy/IP loss, model sabotage, code execution | classification, encryption, lineage, signed artifacts, safe loaders, access and integrity monitoring |
| Supply-chain compromise | poisoned package/image/operator/driver/firmware/model | privileged code execution at scale | approved sources, SBOM, provenance, signatures, isolated builds, staged rollout and rollback |
| Agent/tool abuse | prompt injection, confused deputy, excessive agency, poisoned skill/memory | unauthorized actions, exfiltration, destruction | agent identity, policy-mediated tools, schema validation, approvals, budgets, trace and verifier |
| Abuse and denial of wallet | fraudulent tenant, quota bypass, capacity hoarding, prohibited use | financial loss, service degradation, legal/safety harm | tenant trust tiers, quotas, rate limits, egress policy, behavioral detection, response workflow |
| Insider and support abuse | standing privilege, covert access, log tampering | high-confidence access to sensitive assets | separation of duties, JIT/JEA, session recording, dual control, evidence immutability |
| Availability and destructive events | DDoS, ransomware, automation error, regional/fabric failure | prolonged outage, data loss, unsafe recovery | capacity controls, immutable backups, tested rebuild, regional strategy, kill switches and exercises |
| Physical/firmware compromise | BMC takeover, rogue component, theft, malicious maintenance | persistent control below the OS | isolated OOB, measured state, supply controls, facility access, tamper and lifecycle evidence |

Threat modeling must include positive and negative flows, trust-boundary crossings, failure of dependencies, unsafe defaults, operator error, malicious configuration, recovery behavior, and evidence integrity. Catastrophic cross-tenant and root-of-trust failures must not be averaged away by a low probability score.

## 6. Security principles

1. **Identity before location.** Authenticate and authorize people, tenants, workloads, devices, agents, and automation independently of network location.
2. **Least privilege is dynamic.** Prefer short-lived, just-in-time, task-bound authority over standing roles or static secrets.
3. **Tenant isolation is end to end.** Verify boundaries across API, identity, control plane, compute, GPU, storage, cache, telemetry, Ethernet, RDMA, and support operations.
4. **Secure defaults are provider responsibilities.** MFA, audit, safe isolation modes, encryption, updates, and secure deletion cannot be optional premium features.
5. **Policy and evidence are code.** Important decisions should be testable, versioned, reproducible, and attributable.
6. **External content is untrusted data.** Prompts, models, packages, skills, documents, images, tickets, and web content never grant authority.
7. **Assume compromise and constrain blast radius.** Design for rapid isolation, revocation, rebuild, and customer-safe evidence collection.
8. **Recovery is continuously proven.** Backups, restores, failover, secure erase, key recovery, and tenant offboarding are exercised.
9. **Automation earns autonomy.** Automated actions must be bounded, observable, reversible where possible, and independently verified.
10. **Complexity must earn its cost.** Prefer general mechanisms—identity, isolation, policy, evidence, feedback, and verification—over brittle exceptions.

## 7. Operating model

### 7.1 Accountability

The governing body or executive risk owner sets risk appetite and approves material residual risk. A CISO or equivalent owns the security program. Every customer-facing service has a business owner, technical owner, security owner, data owner, and incident escalation path. Platform teams own reusable controls; service teams remain accountable for correct adoption.

### 7.2 Three complementary lines

- **First line:** product, platform, infrastructure, SRE, network, data, and AI teams implement and operate controls.
- **Second line:** security, privacy, risk, and compliance define policy, challenge design, monitor risk, and coordinate assurance.
- **Third line:** independent audit or validation tests whether assertions and evidence are reliable.

Independence is about decision authority, not organizational size. A small NeoCloud may use cross-team review or a qualified external assessor, but the implementer must not be the only verifier.

### 7.3 Security capability model

Security should be delivered as shared platform capabilities: identity and federation, workload identity, policy decision and enforcement, secrets and keys, trusted build and artifact verification, asset/dependency graph, vulnerability and exposure management, telemetry and evidence plane, incident command, tenant trust and abuse prevention, recovery and sanitization, and customer assurance.

Each capability needs an owner, service-level objective, supported tiers, consumers, dependencies, evidence outputs, on-call path, and roadmap state. The [security service catalog template](../../templates/security-service-catalog.csv) provides the minimum fields.

### 7.4 Shared responsibility

The provider cannot transfer responsibility for infrastructure it exclusively controls. Customers cannot assume the provider will secure customer code, data classification, role assignments, or guest operating systems unless contracted. Every service must publish a responsibility matrix that covers normal operation, incident response, evidence, backup/restore, deletion, and end-of-service actions. Ambiguity is itself a control failure.

## 8. Reference architecture

The security architecture has seven cooperating planes:

1. **Governance and assurance plane:** service catalog, risk, obligations, exceptions, evidence, control status, customer assurance.
2. **Identity and policy plane:** human/tenant/workload/agent identity, federation, PKI, authorization, JIT privilege, policy decision and approval.
3. **Edge and control plane:** API gateway, management interfaces, provisioning, billing/quota, support tooling, orchestrator controllers.
4. **Orchestration and runtime plane:** Kubernetes, Slurm, admission, scheduler, runtime, node agents, sandboxing, workload policy.
5. **Compute, fabric and storage plane:** hosts, hypervisors, GPUs, DPUs, BMCs, Ethernet, InfiniBand/RDMA, NVLink, storage, snapshots and reset/sanitization.
6. **Data, model and supply-chain plane:** source, build, registry, SBOM, provenance, signing, datasets, model registry, safe loading and release.
7. **Telemetry, response and recovery plane:** logs, traces, detections, case management, evidence store, revocation, containment, backup, restore and rebuild.

Policy enforcement must occur close to the resource being protected, while decisions and evidence remain correlated through stable identities and asset relationships. No single plane is trusted to attest to its own effectiveness. See the [Reference Architecture](REFERENCE_ARCHITECTURE.md) for trust zones, flows, components, and service-profile variants.

## 9. Security-domain model

| Domain | Required outcome |
|---|---|
| Governance, risk, compliance and shared responsibility | accountable decisions, explicit obligations, controlled exceptions, customer-transparent responsibility |
| Asset, service, dependency and data-flow inventory | authoritative knowledge of what exists, who owns it, how it connects, and what evidence is missing |
| Human, tenant, workload and agent identity | strong, short-lived, scoped and reviewable identity for every acting subject |
| Control-plane, API and administrative interfaces | tenant-correct authorization, private administration, abuse resistance, traceable change |
| Network, fabric, RDMA/InfiniBand and DPU isolation | proven separation across every packet and direct-memory path |
| Compute, hypervisor, bare metal, GPU and accelerator | declared isolation properties, hardened hosts, safe allocation, reset and attestation |
| Kubernetes, containers, Slurm and scheduler | secure controllers, admission, jobs, quotas, runtime and recovery |
| Data, dataset, model, artifact and privacy | controlled lifecycle, provenance, integrity, confidentiality, retention and deletion |
| Secrets, keys, PKI, attestation and confidential computing | protected roots of trust, short-lived secrets, governed key release and cryptographic agility |
| Software, model and infrastructure supply chain | known, approved, signed and reproducible inputs with rapid revocation and rollback |
| Secure engineering, IaC, change and configuration | threat-informed design, reviewable change, safe defaults, policy gates and drift control |
| Vulnerability, exposure, patch and firmware | continuous discovery, risk-based remediation and verified closure across all layers |
| Telemetry, detection, intelligence and audit | complete, tenant-safe, tamper-resistant evidence and tested detections |
| AI application, agent, tool, skill and prompt | constrained authority, protected memory/context, safe tool use, traceability and independent verification |
| Abuse prevention, tenant trust, egress and acceptable use | proportional onboarding, resource controls, misuse detection, fair response and appeal |
| Incident response, forensics, crisis and recovery | fast command, safe containment, evidence preservation, notification and verified reopening |
| Resilience, availability, capacity, backup and DR | survivable control planes, tested restore/rebuild and resistance to capacity exhaustion |
| Physical, facility, BMC, hardware lifecycle and media | controlled facilities and OOB systems, trustworthy hardware state and verifiable sanitization |

The complete normative outcomes and evidence expectations are in the baseline and machine-readable control catalog.

## 10. Adoption tiers and production gates

| Tier | Meaning | Typical decision |
|---|---|---|
| **T0 Guardrails** | non-negotiable conditions before tenant data or production capacity is exposed | release blocked until passed or an exceptional executive emergency process is invoked |
| **T1 Foundation** | ownership, inventory, basic hygiene, visibility, response and recovery foundations | complete in the first 90 days or before material scale |
| **T2 Production** | reusable, policy-enforced and measured controls for multi-tenant general availability | required for sustainable production operation |
| **T3 Assured** | independent testing and higher-assurance isolation, sovereignty and resilience | required for high-impact, regulated or explicitly assured services |
| **T4 Adaptive** | continuous verification, guarded automation, advanced attestation/confidentiality | adopted only where failure modes and rollback are understood |

A production-readiness decision requires:

- all applicable T0 controls independently `VERIFIED`;
- no unowned critical asset, privileged identity, public administrative path, or unknown tenant-isolation mode;
- a current threat model and shared-responsibility matrix;
- tested credential revocation, incident escalation, restore/rebuild and tenant offboarding;
- evidence that the deployed service—not a reference design—satisfies the claim;
- explicit residual-risk acceptance for all unresolved high risks.

## 11. Lifecycle integration

### Design and product definition

Define service profile, tenant boundary, data classes, jurisdictions, isolation SKU, responsibility split, abuse cases, SLO/RTO/RPO, evidence obligations, and decommission behavior before implementation. Security requirements are acceptance criteria, not post-launch findings.

### Source, build and release

Use protected source control, reviewed infrastructure code, isolated builds, pinned dependencies, SBOMs, provenance, artifact signatures, trusted registries, policy verification, staged rollout, canaries, and tested rollback. Treat models, checkpoints, skills, prompts, policies, and firmware as governed artifacts.

### Provision and operate

Issue short-lived identities, enforce policy at API/orchestrator/host/fabric/storage boundaries, record allocation topology, validate isolation, continuously reconcile desired and actual state, and route security telemetry to a protected evidence plane. Administrative support uses JIT access, approved purpose, session evidence, and tenant-safe handling.

### Respond and recover

Contain at the strongest reliable boundary; preserve evidence; rotate roots and delegated credentials as needed; communicate by tenant and jurisdiction; rebuild from known-good sources; independently verify isolation, integrity, and recovery before reopening.

### Delete and decommission

Delete logical data, snapshots, caches, model artifacts and backups according to policy; reset/sanitize accelerators, local disks and media; revoke identities and certificates; remove fabric and network assignments; retire BMC/DPU access; produce deletion and chain-of-custody evidence.

## 12. Evidence and continuous assurance

A control is not complete because a policy exists or a console shows a green state. Each assessment follows:

`PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`

Only an independent validator `PASS` may promote a control to `VERIFIED`. Evidence must identify the control, service, asset and tenant scope, collector, observation time, integrity protection, limitations, valid-until time, storage location, and verifier. Evidence freshness is part of the requirement.

Continuous assurance combines:

- configuration and policy evaluation;
- asset/identity/dependency reconciliation;
- authorized isolation and negative-path tests;
- restore, revocation, failover and sanitization exercises;
- detection validation mapped to relevant ATT&CK and ATLAS behaviors;
- sample-based human review of high-impact actions;
- customer-facing assurance packages with clearly stated scope and exceptions.

The goal is not a dashboard score. It is the ability to answer, with current evidence: **What do we protect? Who or what can act? Which policy allowed it? What happened? Was the boundary preserved? Can we contain and recover? Who independently verified the claim?**

## 13. Development roadmap

A typical program proceeds through six gates:

1. **0–30 days: establish command and stop critical exposure.** Name owners, freeze unsafe public administration, enforce MFA, protect roots, inventory critical services, define severity and incident command, identify sharing/isolation modes.
2. **31–90 days: build the foundation.** Complete T0/T1 assessment, centralize identity/logging/secrets, document data flows, publish shared responsibility, test backup and revocation, create patch and vulnerability SLAs.
3. **3–6 months: productize controls.** Introduce workload identity, policy-as-code, trusted build/provenance, fabric validation, admission/runtime controls, evidence collection, tenant trust and abuse workflows.
4. **6–12 months: reach production maturity.** Close T2 gaps, establish detection engineering and purple-team cadence, validate GPU/fabric isolation, integrate customer assurance, conduct full incident and DR exercises.
5. **12–18 months: add high assurance.** Independent testing, dedicated/regulated profiles, stronger attestation and key release, sovereign operations, advanced insider and supply-chain controls.
6. **18–24 months: adopt guarded adaptivity.** Continuous controls monitoring, bounded security agents, automated evidence, safe containment and remediation with approval, rollback and verifier gates.

Detailed dependencies, milestones, metrics, team model, and build/buy guidance appear in the [Roadmap](ROADMAP.md).

## 14. Customer and ecosystem transparency

A trustworthy provider should make the following available under appropriate confidentiality:

- service boundary and current shared-responsibility matrix;
- supported isolation modes and limitations for each SKU;
- encryption, key ownership, data residency, retention and deletion behavior;
- security event, vulnerability and customer-notification commitments;
- independent assurance reports and material exceptions;
- subprocessor and critical dependency information;
- API, identity, logging, export, backup and offboarding capabilities;
- secure development and artifact-provenance approach;
- incident coordination and evidence-exchange process.

Security claims must be precise. “Dedicated” must identify which host, GPU, network, fabric, storage, support, and telemetry resources are dedicated. “Encrypted” must identify where plaintext exists and who controls keys. “Zero trust” must identify the identities, policies, enforcement points, and verification process.

## 15. Conclusion

NeoCloud security is the discipline of preserving trustworthy decisions across AI infrastructure that is physically dense, highly shared, software defined, supply-chain dependent, and increasingly autonomous. The minimum viable program is not a certificate or a collection of appliances. It is an explicit service boundary, strong identities, end-to-end tenant isolation, secure artifacts, protected data and models, complete telemetry, tested response and recovery, controlled automation, and evidence that survives independent challenge.

Organizations should begin with T0 production gates, build T1 visibility and ownership, convert T2 controls into shared platform services, apply T3 where the consequences justify higher assurance, and introduce T4 automation only when its authority and failure modes are constrained. This creates a security architecture that can scale with compute, models, agents, customers, and regulation without turning every new risk into another brittle exception.

## Disclaimer

This white paper is an implementation-oriented industry baseline. It is not a certification, legal opinion, guarantee, or substitute for applicable law, regulation, contract, privacy assessment, safety assessment, or qualified independent audit. External-framework mappings are informative and must be validated for the organization, service, jurisdiction, and version in use.
