# NeoCloud Cyber Security Development Roadmap

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented project draft  
**Reference horizon:** 0–24 months

## 1. How to use the roadmap

This roadmap sequences security capabilities for a specialized AI/GPU cloud. It is not permission to defer a currently failed T0 control. Dates are planning references; each phase exits through evidence gates.

The program follows three rules:

1. **T0 first:** every applicable T0 must be independently `VERIFIED`; failed, unknown, stale, inconclusive or untested T0 remains `NO_GO_NONCONFORMANT`.
2. **Build reusable mechanisms:** identity, delegated authority, policy, isolation, provenance, evidence, response and recovery should become shared platform capabilities rather than service-specific tickets.
3. **Add automation last:** adaptive defense is introduced only after approval, stop, rollback, trace, evidence and independent-verifier behavior are measured.

An executive may authorize a time-bounded emergency business-continuity decision, but the decision does not change the failed control result or allow the service to be described as conformant.

## 2. Target state at 24 months

A mature NeoCloud security program should be able to:

- identify every in-scope critical service, asset, tenant relationship, privileged identity, root, accelerator/fabric/OOB state, data/model, deployed artifact, supplier and dependency;
- preserve tenant and request context from API authorization through scheduler, host/GPU, network/RDMA/DPU, storage, telemetry, cleanup and deletion;
- state and test the exact isolation properties of every commercial compute SKU;
- govern people, workloads, services, devices and agents through strong identity, scoped delegated authority and revocation;
- admit, recall and rebuild software, firmware, infrastructure, model, checkpoint, prompt, policy and skill artifacts from attributable sources;
- collect all required T0 telemetry and measure priority-source coverage, freshness and failure separately;
- establish incident command, reliable scope, containment, notification, known-good recovery and independently verified reopening;
- produce service-scoped, time-bound assurance rather than one aggregate compliance score;
- operate high-assurance dedicated, sovereign, attested or confidential-computing profiles where justified by threat model and customer commitment;
- use guarded adaptive automation only where false completion, scope violation, approval bypass, stop, rollback and verifier independence are measurable.

## 3. Program workstreams

| Workstream | Accountable outcome | Typical owners |
|---|---|---|
| Governance and assurance | service boundaries, responsibility, risks, decisions, evidence, independent review | executive risk owner, CISO, service owners, privacy/legal, assurance |
| Inventory and exposure | authoritative services/assets/identities/data/models/dependencies; independent discovery and drift | platform security, SRE, asset/configuration owners |
| Identity and policy | human/tenant/workload/device/agent identity, JIT privilege, delegation, policy and revocation | IAM, platform identity, security architecture |
| API and control plane | tenant-correct authorization, private administration, safe change and failure | product/platform engineering, SRE, security |
| Compute and orchestration | Kubernetes/Slurm, host/runtime, GPU sharing/reset, node response | compute, Kubernetes, HPC/Slurm, accelerator teams |
| Network, fabric and OOB | plane separation, Ethernet/RDMA/P_Key/DPU, BMC/OOB and path validation | network/fabric, hardware platform, facilities security |
| Data, model and privacy | purpose, rights, access, lineage, safe formats, retention/export/deletion | data/AI platform, privacy, security |
| Keys and supply chain | KMS/HSM/PKI/secrets, source/build/train, provenance, admission, recall | cryptography, DevSecOps, release, model platform |
| Telemetry and detection | required-source health, evidence integrity, detections, threat hunting, assurance pipeline | security engineering, SOC, platform observability |
| Abuse and resilience | tenant trust, quotas/cost, egress, capacity, backup, failover and recovery | trust and safety, fraud, SRE, capacity, billing |
| Incident and crisis | command, forensics, notification, containment, recovery and lessons | incident response, legal/privacy, customer/support |
| Physical and lifecycle | facility, BMC, firmware, custody, sanitization and decommissioning | data-center, hardware, facilities, security |

Each workstream needs one accountable owner, dependencies, milestones, service coverage, metrics, evidence, tests and exit criteria. “Security owns it” is not an acceptable final ownership model.

## 4. Phase 0 — Immediate command and exposure control (days 0–7)

### Outcomes

- name owners for production services, critical dependencies, control planes, roots/signing keys, fabric managers, BMC/OOB and incident command;
- establish a secure incident channel, severity model, on-call escalation and emergency decision record;
- create an initial inventory of services, critical assets/identities, public exposure and crown-jewel data/models;
- freeze or explicitly approve new public provider administration, new accelerator-sharing modes, root/fabric changes and unreviewed production artifacts;
- rotate or disable shared, unknown, orphaned or departed-owner privileged credentials;
- define authority to revoke, quarantine, isolate and stop a risky deployment.

### Exit gate

The provider can establish command, identify the service/tenant/resource under investigation, revoke privilege and isolate a service through a known trusted path. Unknown critical roots or provider-admin paths are not represented as healthy.

## 5. Phase 1 — T0 containment and minimum visibility (days 8–30)

### Outcomes

- phishing-resistant MFA for applicable provider privilege and high-impact tenant-owner access;
- private governed access to provider control planes, Kubernetes/Slurm controllers, fabric management and BMC/OOB;
- critical API object/action/tenant/purpose/context tests;
- exact host/GPU/cache/NVLink/network/RDMA/storage/telemetry/support declarations for every commercial SKU;
- quarantine or removal of ambiguous time-slicing, hardware-partition, virtualization, P_Key/DPU, storage, support or cleanup boundaries;
- central protection and recovery of roots, secrets, PKI and break-glass;
- protected required telemetry and source-health monitoring for critical trust boundaries;
- core playbooks for cross-tenant, root/key, control-plane, accelerator/fabric/BMC, destructive-agent and irrecoverable-data scenarios.

### Exit gate

Every applicable T0 has scope, owner, current implementation state, evidence requirement, validator, and dated containment/remediation. No failed or unknown T0 is counted as complete or covered by a score.

## 6. Phase 2 — Authoritative state and independent verification (days 31–90)

### Outcomes

- service, asset, identity, dependency, data-flow, model, artifact, key and supplier inventories;
- shared-responsibility matrices and customer security contacts;
- joiner/mover/leaver, service account, workload identity, agent, certificate and secret lifecycle;
- asset-linked vulnerability and external-exposure discovery;
- data/model purpose, rights, classification, residency, retention, export, deletion and backup requirements;
- backup/rebuild-source inventory and dependency mapping;
- desired/actual reconciliation for tenant, scheduler, host/GPU, network/fabric/DPU, storage, quota, policy and artifact state;
- independent prohibited-path tests across API, host/GPU, storage, Ethernet/RDMA, DPU, telemetry and support;
- privileged revocation/break-glass, orchestrator restore/rebuild, critical data/model restore, tenant offboarding/deletion and end-to-end incident exercises;
- initial service-scoped assurance package.

### Exit gate

- every applicable T0 is independently `VERIFIED`;
- in-scope critical asset and privileged-identity ownership is 100%;
- required T0 telemetry-source health is 100%;
- priority independent discovery and non-gate telemetry coverage has a declared denominator and reaches the agreed target, with 95% as a reference starting point rather than a hard-gate substitute;
- failed tests have accountable containment and remediation;
- service claims match current deployed evidence.

## 7. Phase 3 — Productize the foundation (months 3–6)

### Outcomes

- workload/service identity and short-lived credentials integrated into Kubernetes, Slurm, storage, registry and internal APIs;
- policy-as-code for authorization, sharing modes, placement, egress, quota/cost, artifact admission and agent tools;
- reconciled desired/actual state and quarantine for material tenant/isolation drift;
- hardened, versioned host/node/controller images with rapid rebuild;
- inventory/BOM, provenance/signature where required, scan, compatibility, admission and recall for high-impact artifacts;
- protected evidence pipelines with stable service/tenant/request/resource identifiers;
- defined secure engineering gates, canary, rollback and post-deployment verification;
- tenant trust tiers, urgent abuse path and quota/rate/cost/capacity controls;
- customer-facing responsibility and isolation statements.

### Exit gate

New production services inherit identity, policy, telemetry, evidence, response and recovery defaults from platform services rather than implementing them manually. Material drift creates an alert, block or quarantine with an owner and evidence.

## 8. Phase 4 — Sustainable multi-tenant production (months 6–12)

### Outcomes

- close applicable T2 gaps across engineering, data/model lifecycle, supply chain, keys, orchestration, vulnerability management, evidence, incident and resilience;
- continuous or frequent service/asset/identity/artifact/fabric reconciliation;
- vulnerability prioritization based on real exposure, exploitability, privilege, tenant impact and blast radius;
- tested GPU reset/error/quarantine and tenant-reassignment workflow across representative hardware/firmware/driver/mode variants;
- regular API, Kubernetes/Slurm, fabric/RDMA/DPU, storage, support and OOB prohibited-path tests;
- detection engineering linked to current ATT&CK/ATLAS-informed threat scenarios and authorized behavior replay;
- customer, legal/privacy and ecosystem notification exercises;
- backup, restore, regional/fabric failure and known-good rebuild exercises;
- evidence-quality, freshness, false-positive/false-negative proxy and remediation metrics.

### Exit gate

Applicable T2 controls operate as owned services with SLOs, change control, failure behavior, current evidence and repeatable tests. Recovery and isolation results meet service commitments, not just tabletop expectations.

## 9. Phase 5 — Higher-assurance services (months 12–18)

### Outcomes

Apply only where threat model, regulation, sovereignty, data sensitivity or customer commitment justifies the cost:

- dedicated host/full-device or precisely stated hardware-partitioned services;
- measured boot/firmware and attestation-bound admission or key release;
- confidential-computing profiles with explicit hardware/software/attestation boundary and unsupported components;
- jurisdiction-bounded people, identity, key, data, support, telemetry, backup, suppliers and recovery;
- stronger build/train isolation, reproducibility, root separation and cryptographic recovery;
- independent architecture, penetration, isolation, supplier and recovery assessments;
- customer assurance packages with exact scope, versions, limitations, findings and evidence validity.

### Exit gate

Every T3 claim is linked to a named service/profile and exact deployed boundary, independently tested at least annually and after material change, and removed or downgraded when evidence expires or assumptions change.

## 10. Phase 6 — Guarded adaptive security (months 18–24)

### Preconditions

Do not begin until identity/delegation, typed tools, least privilege, deterministic approval, stop/containment, rollback/manual recovery, protected traces, independent verification, evidence quality and incident ownership are proven for the relevant action class.

### Candidate uses

- evidence collection and scope reconciliation;
- detection triage and investigation planning;
- reversible low-risk configuration correction;
- artifact/vulnerability prioritization;
- guided containment preparation;
- controlled red-team, validation and recovery exercises in authorized environments.

### Prohibited default uses

- unrestricted destructive action;
- self-expanding credentials, tools, scope or budget;
- self-approval of customer-impacting action;
- self-modification of policy, evidence or verifier;
- autonomous irreversible customer communication, legal conclusion or production deletion;
- declaring its own task `VERIFIED` without independent evidence.

### Exit gate

For each automated action class, measure and meet targets for approval bypass, policy/scope violation, false completion, rollback/manual recovery, stop effectiveness, evidence integrity, customer impact and independent-verifier disagreement. A kill switch and human incident path are tested.

## 11. Metrics and executive scorecard

Do not use one blended completion percentage. Report:

- production decision by service/profile;
- failed, unknown, stale, inconclusive or untested T0;
- critical unknown/unowned scope;
- exact commercial-SKU isolation declarations and latest prohibited-path tests;
- required T0 telemetry health and separately measured priority-source coverage;
- privileged MFA/JIT/revocation and root/secret state;
- vulnerability/exposure SLA and deployed-state retest;
- artifact inventory, provenance/admission and recall;
- incident command, reliable-scope and effective-containment time;
- restore/rebuild, tenant offboarding/deletion and sanitization results;
- agent approval bypass, scope violation, false completion, stop and rollback;
- customer commitment drift, evidence expiry and unresolved business decisions.

Use the [Metrics and Assurance Guide](METRICS_AND_ASSURANCE.md) for definitions and denominators.

## 12. Build, buy and staffing priorities

### Build or deeply integrate

- tenant-correct authorization and desired/actual reconciliation;
- GPU/NVLink/fabric/DPU/storage/scheduler assignment evidence;
- reset, cleanup, sanitization and reassignment workflow;
- model/checkpoint lineage, safe loading and lifecycle;
- agent identity, delegation, tool policy, approval, stop and verifier;
- service-specific containment, recovery and reopening.

### Buy or adopt mature components

- IdP, phishing-resistant MFA, PAM, KMS/HSM, PKI and secret management;
- vulnerability, exposure and attack-surface management;
- SIEM/data lake, runtime detection, case management and evidence storage;
- backup, DDoS/WAF/API gateway, signing and transparency services.

Procurement requires exportable APIs/events, stable identity integration, tenant-safe behavior, secure update, high availability and safe degradation, incident notification, evidence quality, independent testing and migration/exit. A vendor dashboard alone is not coverage.

### Staffing sequence

Early staffing should cover accountable security leadership, platform security architecture, identity/policy, cloud/HPC/GPU/fabric engineering, detection/response, data/model security, vulnerability/exposure, facilities/hardware and assurance/privacy. At small scale, individuals may cover several functions, but implementation and independent verification cannot collapse into one unchecked role.

## 13. Principal program risks

| Risk | Failure pattern | Countermeasure |
|---|---|---|
| compliance theater | policies and dashboards replace deployed tests | T0 gates, negative tests, evidence freshness and independent review |
| platform/security split | service owners assume central security owns correctness | explicit shared responsibility and service acceptance criteria |
| GPU marketing ambiguity | “dedicated” or “isolated” hides sharing | exact SKU statement and versioned deployed-path tests |
| coverage gaming | unknown assets/logs disappear from denominators | unknown critical scope fails; publish numerator, denominator and exclusions |
| control-plane centralization | identity/policy/evidence outage causes fail-open | local safe behavior, bounded cache, expiry, quarantine and recovery tests |
| tool sprawl | products do not share identities, state or evidence | capability contracts, integration architecture and retirement plan |
| agent overreach | automation gains destructive authority before proof | risk tiers, deterministic approval/stop, rollback, trace and verifier |
| recovery optimism | backup exists but roots/data/isolation are not trustworthy | known-good rebuild and independent reopening tests |
| unreviewed standards drift | final, draft and vendor guidance treated equally | reference-status tracking and periodic evidence-cutoff review |

## 14. Executive decisions required

Leadership must decide and document:

1. service profiles, risk appetite and customer assurance commitments;
2. accountable service/control owners and independent-verification authority;
3. which failed T0 exposures are stopped immediately, and who may make a separate time-bounded emergency business decision without changing the conformance result;
4. isolation products the company will sell and the exact meaning of each claim;
5. jurisdictions, data/model classes and workloads accepted;
6. build/buy boundaries and strategic platform investments;
7. recovery objectives, capacity reserve and notification principles;
8. high-impact agent action classes allowed, prohibited or approval-gated;
9. publication, license, vulnerability-reporting and external-assurance strategy;
10. metrics and evidence that will be reviewed monthly.

## 15. Roadmap completion definition

The roadmap is successful when security is no longer a collection of disconnected controls. Service boundaries and identities are authoritative; tenant context survives every translation; isolation claims are precise and tested; data/models/artifacts have lifecycle and provenance; required telemetry is healthy; response and recovery are exercised; evidence is independently reproducible; and automation cannot exceed, approve or verify its own authority.
