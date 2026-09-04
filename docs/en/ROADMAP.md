# NeoCloud Cyber Security Development Roadmap

**Horizon:** 0–24 months  
**Planning model:** gate-based, risk-prioritized, evidence-driven

## 1. How to use this roadmap

This roadmap is a reference sequence, not a calendar promise. A young provider with public APIs and multi-tenant GPUs may need to complete T0 guardrails in days. A dedicated internal cluster may legitimately mark some controls not applicable. Progress is measured by independently verified outcomes and reduced exposure, not documents produced or tools purchased. Dates, percentages, and phase targets are project-defined planning defaults—not externally validated industry benchmarks—and must be adapted using [Scope and Limitations](SCOPE_AND_LIMITATIONS.md).

Start by selecting service profiles, defining the production boundary, identifying accountable owners, and assessing every T0/T1 control. Use the risk register for service-specific threats, but do not let a numeric score override a failed cross-tenant, root-key, public-admin, secure-erase, logging, response or recovery guardrail.

Each phase below has an **exit gate**. Work may overlap across phases, but the program should not claim the next maturity level until the prior gate is satisfied.

## 2. Target state after 24 months

A mature NeoCloud security program should be able to demonstrate:

- one authoritative graph linking services, tenants, identities, workloads, nodes, GPUs, fabrics, data/models, artifacts, controls, risks and evidence;
- phishing-resistant and just-in-time human access plus short-lived workload/agent identity, bound to attestation where supported and justified;
- tenant-correct policy enforced at API, controller, scheduler, host, GPU, fabric, storage, registry, KMS and tool boundaries;
- declared and continuously validated isolation properties for every commercial SKU;
- trusted software/model/firmware supply chains with inventory, provenance, signatures, staged rollout and recall;
- protected data/model lifecycle, customer-visible responsibility, residency, retention, deletion and export;
- complete, tenant-safe telemetry and evidence with tested detection and incident playbooks;
- tested credential revocation, containment, rebuild, restore, failover, sanitization and customer coordination;
- bounded AI-assisted defense whose authority, approval, cost, rollback and verifier are explicit;
- current assurance material that states scope and exceptions precisely.

## 3. Phase 0 — Days 0–7: establish command

### Objectives

- Name accountable owners and create a single security decision channel.
- Identify immediate conditions that could cause cross-tenant, fleet-wide or unrecoverable harm.
- Preserve evidence and prevent uncontrolled change while the baseline is established.

### Deliverables

- Executive risk owner, CISO/security lead, service owners and incident commander rotation.
- Initial list of customer-facing services, production regions, orchestrators, GPU sharing modes, fabrics, BMC/OOB systems, identity providers, signing roots, registries, key stores and critical suppliers.
- Emergency contact tree, secure incident channel and SEV-0/SEV-1 criteria.
- Freeze or approval requirement for new public administrative interfaces, root/signing-key changes, new GPU-sharing modes, fabric topology changes and unreviewed production images.
- Immediate credential rotation for unknown, shared or departed-owner privileged accounts.

### Exit gate

- Every production service and critical root has a named owner.
- No known public provider-management interface lacks strong authentication and an explicit necessity decision.
- A 24×7 path exists to revoke privileged access, isolate a service and convene incident command.

## 4. Phase 1 — Days 8–30: stop critical exposure

### Objectives

- Meet the most urgent T0 guardrails.
- Establish minimum visibility into identities, control planes, tenancy and physical allocation.
- Make incident containment possible without improvisation.

### Work packages

**Identity and roots**

- Enforce phishing-resistant MFA for provider privileged access and tenant owners where supported.
- Remove shared accounts; inventory service/automation credentials; protect break-glass.
- Centralize KMS/secret storage for critical services; restrict and log signing/root-key use.

**Control plane and network**

- Move provider administration behind a privileged gateway or private path.
- Validate object-level tenant authorization on highest-risk APIs.
- Separate public, tenant, provider-management and BMC/OOB networks.
- Identify InfiniBand/RDMA/NVLink and DPU boundaries; quarantine ambiguous assignments.

**Compute and data**

- Publish an interim isolation matrix for each SKU: host, GPU, memory, fabric, storage and support.
- Disable or restrict sharing modes that cannot meet the claimed isolation.
- Define and test minimum GPU/local-disk cleanup between tenants.
- Classify signing keys, customer models/checkpoints and provider control-plane data as crown jewels.

**Telemetry and response**

- Centralize identity, privileged access, API/control-plane, Kubernetes/Slurm and BMC/fabric change logs for critical systems.
- Protect logs from ordinary source administrators.
- Create playbooks for credential/root compromise, control-plane takeover, cross-tenant exposure and destructive automation.

### Exit gate

- All applicable T0 controls have owners, scope, implementation state, evidence requirement and target date.
- No critical root, privileged identity or production management path is unknown.
- Provider can identify a tenant's active resources and revoke access in an emergency.
- Known cross-tenant isolation uncertainty is blocked, dedicated or explicitly escalated—not silently accepted.

## 5. Phase 2 — Days 31–90: build the foundation

### Objectives

- Complete T0 and establish T1 across production.
- Replace tribal knowledge with authoritative inventories, responsibilities and tested procedures.
- Build the telemetry and evidence needed for later automation.

### Deliverables by workstream

| Workstream | 90-day deliverables |
|---|---|
| Governance | approved security charter, service profiles, risk/exception process, shared-responsibility matrices, customer commitment register |
| Inventory | authoritative service/asset/identity/data/model/dependency inventory with owners and reconciliation |
| Identity | federation, MFA, joiner/mover/leaver, privileged JIT roadmap, break-glass test, service-account lifecycle |
| API/control plane | inventory, authentication/authorization standards, rate/quotas, private admin, audit and change traceability |
| Compute/fabric | documented SKU isolation, host baselines, placement records, reset/sanitization tests, network/P_Key ownership |
| Kubernetes/Slurm | hardened control-plane baselines, RBAC/account review, admission/job controls, private management and backups |
| Data/model | classification, encryption/key ownership, residency/retention/deletion requirements, access and lineage minimums |
| Supply chain | approved sources, image/model registries, SBOM inventory, signature/provenance pilot, emergency rollback |
| Vulnerability | asset-linked scanning, severity/exploitability SLAs, emergency patch path, firmware/driver coverage |
| Detection/IR | log coverage dashboard, core detections, incident severity, on-call, evidence handling, tabletop exercise |
| Resilience | service dependency maps, SLO/RTO/RPO, immutable backup for critical control planes, restore and revocation tests |
| Abuse | AUP, tenant risk tiers, quotas, rate controls, prohibited-use and escalation process |

### Exit gate

- Every applicable T0 is independently `VERIFIED` or service launch is blocked.
- At least 95% of critical assets and 100% of privileged identities have owners and current inventory records.
- Critical log-source coverage is at least 95%, with known gaps assigned and dated.
- Restore, privileged revocation and one cross-tenant incident scenario have been exercised.
- Shared responsibility and security contact paths are customer accessible.

## 6. Phase 3 — Months 3–6: productize controls

### Objectives

- Turn manual controls into reusable, paved-road platform services.
- Push policy decisions and evidence generation into normal provisioning and deployment paths.
- Reduce static secrets, configuration drift and service-by-service exceptions.

### Major initiatives

1. **Workload identity:** issue short-lived identities to services, jobs, nodes and agents; bind them to attested state where supported and justified; remove embedded cloud/API credentials.
2. **Policy-as-code:** define reusable policies for tenant authorization, isolation SKU, region, data class, artifact admission, egress, tool use and approvals.
3. **Trusted artifact pipeline:** protected source, isolated build, SBOM, provenance, signature, registry policy and admission verification for high-impact components.
4. **Desired/actual reconciliation:** continuously compare API intent with Kubernetes/Slurm, host, GPU, storage, network, DPU and P_Key state.
5. **Runtime and node response:** establish host/runtime telemetry, quarantine workflow, immutable-node or rapid-rebuild approach.
6. **Evidence automation:** generate evidence IDs, hashes, scope and freshness directly from policy and infrastructure systems.
7. **Tenant trust and abuse:** integrate onboarding risk, quotas, egress, behavior and appeals with service operation.
8. **Secure engineering:** make threat model, security tests, rollback and observability release criteria.

### Exit gate

- New tier-1 services use standard identity, logging, secrets, policy, artifact and incident capabilities.
- An organization-defined target for production workloads using short-lived or brokered credentials is met; 80% by month six is an illustrative planning target, not an industry benchmark.
- High-impact artifacts are inventoried; critical build paths produce SBOM and provenance.
- Tenant/fabric/GPU assignment reconciliation detects and pages on material mismatch.
- Security evidence for priority controls is generated automatically and reviewed for correctness.

## 7. Phase 4 — Months 6–12: production maturity

### Objectives

- Close T2 gaps and demonstrate effectiveness under attack, failure and recovery.
- Make customer assurance accurate and repeatable.
- Establish a sustainable operating cadence.

### Major initiatives

- Expand policy enforcement and workload identity to all production service classes.
- Validate GPU memory reset, partitioning/dedication, device errors and placement transitions through authorized tests.
- Exercise Ethernet, storage and InfiniBand/RDMA isolation end to end, including controller misconfiguration and stale assignment.
- Establish detection engineering mapped to relevant ATT&CK/ATLAS behaviors; run purple-team tests and measure coverage.
- Implement provider-support JIT/JEA, session evidence and tenant-safe access.
- Integrate vulnerability, exploitability, exposure and asset criticality; include firmware, BMC, DPU, driver and operators.
- Conduct full incident simulations for cross-tenant data, signing/root compromise, scheduler/control-plane takeover and malicious/destructive agent.
- Conduct region or major dependency DR, immutable-backup restore and known-good rebuild exercises.
- Produce a customer assurance package with service scope, control status, testing, exceptions and responsibility.

### Exit gate

- T2 verified completion reaches the organization target, with zero failed T0 and no overdue critical exception.
- Cross-tenant negative tests and restore/rebuild exercises pass for every production service profile.
- Priority detection coverage and alert-quality targets are met and independently sampled.
- Customer notification, evidence exchange and support-access processes are exercised.
- Mean time to revoke privileged/workload access and isolate a tenant/resource meets defined SLOs.

## 8. Phase 5 — Months 12–18: high assurance

### Objectives

- Add controls justified by sensitive, regulated, dedicated or sovereign workloads.
- Increase confidence in roots, isolation, supply chain and insider resistance.

### Major initiatives

- Independent penetration and architecture testing with explicit GPU/fabric/control-plane scope.
- Dedicated-host/fabric/storage and regulated-service profiles with precise customer commitments.
- Measured boot, node/device attestation and policy-governed key release where supported.
- Confidential-computing options for suitable workload and threat models.
- Region/jurisdiction-specific key custody, support personnel, telemetry and recovery boundaries.
- Two-person control for root/signing, high-impact release, destructive fleet action and sensitive support operations.
- Supplier assurance for hardware, firmware, drivers, operators, remote support and critical dependencies.
- Advanced insider-risk detections that preserve workforce privacy and due process.
- Cryptographic agility, signing-root rotation and compromise recovery exercise.

### Exit gate

- T3 claims are backed by service-specific, independent evidence.
- Sovereign/regulated boundaries are verified across data, identity, key, support, telemetry, backup and supplier flows.
- Root/key compromise and confidential-workload recovery are exercised.
- Dedicated/isolation statements use precise resource boundaries rather than marketing language.

## 9. Phase 6 — Months 18–24: guarded adaptive security

### Objectives

- Introduce continuous controls monitoring and carefully bounded AI-assisted defense.
- Shorten detection, evidence, triage and safe-remediation loops without allowing automation to become an uncontrolled root of trust.

### Major initiatives

- Continuous evaluation of identity, policy, asset, vulnerability, artifact, GPU/fabric and evidence state.
- Security-agent workflows represented as `Goal → State Summary → Evidence → Reasoning → Action → Observation → Verifier → State Update`.
- Separate planner from executor; require explicit authorization and sandboxing for active testing.
- Typed tools with least privilege, short-lived credentials, immutable scope, budgets and deterministic stops.
- Human approval for destructive, external, customer-impacting, high-cost or irreversible actions.
- Independent verifier gates before controls, incidents or remediation tasks become `VERIFIED`/closed.
- Replayable environments and signed traces for regression, evaluation, SFT/RL data and failure analysis.
- Gradual autonomy levels: recommend → draft → execute reversible low-risk action → execute bounded containment → never autonomous for prohibited classes.

### Exit gate

- Automation has measurable precision, rollback success, approval-bypass rate, policy-violation rate and false-completion rate.
- No agent can alter its own goal, scope, tools, credentials, policy, approval authority, evidence or verifier.
- Every automated containment/remediation path has a tested kill switch and manual recovery path.
- Adaptive controls reduce verified time-to-containment or cost without increasing material incidents or unsupported claims.

## 10. Parallel workstreams and accountable owners

| Workstream | Accountable owner | Essential partners | Primary outcome |
|---|---|---|---|
| Governance and assurance | CISO / risk executive | legal, privacy, audit, product | explicit decisions, obligations, evidence and exceptions |
| Identity and policy | identity/platform leader | security architecture, product, IT | one trust model for human, workload, tenant and agent subjects |
| API and control plane | product/platform engineering | AppSec, SRE, IAM | tenant-correct, private, resilient and auditable control paths |
| Compute/GPU/runtime | compute platform | virtualization, kernel, SRE, vendor | declared and proven isolation, reset, hardening and rebuild |
| Network/fabric/OOB | network/platform security | HPC, facilities, hardware vendor | end-to-end tenant and management-plane separation |
| Kubernetes/Slurm | orchestration platform | service teams, SRE, security | secure scheduling, admission, jobs and controller lifecycle |
| Data/model/privacy | data/AI platform | privacy, product, customer teams | protected lifecycle and provenance for data and models |
| Supply chain/engineering | engineering productivity | AppSec, build, procurement | trusted source-to-deployment path and recall |
| Detection/response | SecOps / incident response | all platform teams, legal, support | complete telemetry, tested detections, fast safe recovery |
| Abuse and customer trust | trust and safety / product | fraud, legal, support, SRE | safe onboarding, capacity protection and fair enforcement |
| Resilience and facilities | SRE/infrastructure | network, facilities, security | tested continuity, rebuild, backup and physical roots |

Small organizations may combine roles, but accountability and independent verification must remain explicit.

## 11. Build, buy and shared-platform guidance

**Build or deeply integrate** capabilities that encode NeoCloud-specific tenancy or topology: tenant-aware authorization, provisioning reconciliation, GPU/fabric placement evidence, secure reset/sanitization, scheduler policy, model/checkpoint lifecycle, agent-tool mediation and service-specific containment.

**Buy or use managed/open components** where the problem is mature and interoperability is strong: IdP/MFA, PAM, KMS/HSM, secret manager, vulnerability scanners, SIEM/data lake, EDR/runtime detection, ticketing, PKI, backup, DDoS/WAF and artifact signing infrastructure.

**Do not outsource accountability.** A vendor dashboard is not evidence that the complete service boundary is covered. Require exportable logs, APIs, tenant-safe operation, HA/degraded-mode design, documented data handling, independent testing, secure update, incident notification, exit/migration and integration with stable identities.

## 12. Prioritization method

Prioritize work in this order:

1. T0 production gate failure.
2. Confirmed active compromise or cross-tenant path.
3. Root of trust, fleet-wide blast radius or irrecoverable data loss.
4. Externally reachable and exploitable path.
5. High-value data/model exposure or destructive authority.
6. Control/evidence blind spot that prevents scope determination.
7. Repeated operational failure or overdue exception.
8. Scalable platform control that removes many manual risks.
9. T3/T4 improvements justified by service commitment or measured value.

Estimate effort and dependency, but do not let a low-effort hygiene task displace a difficult T0 isolation failure.

## 13. Program risks and countermeasures

| Program risk | Countermeasure |
|---|---|
| Tool-first procurement without ownership | define service/control/evidence outcome and integration owner before buying |
| Compliance theatre | require deployed-scope evidence, negative tests and independent verification |
| Hidden shared responsibility | publish per-service matrix and test incident/offboarding handoffs |
| Security blocks product through late review | make paved-road identity, policy, artifact, logging and isolation services available early |
| Excessive exceptions become architecture | expiration, owner, customer impact, compensating control and executive visibility |
| Central policy/logging becomes single point of failure | distributed enforcement, bounded cache, protected buffering and tested degraded mode |
| AI automation overclaims completion | state machine, immutable evidence, independent verifier and false-completion metric |
| Sensitive logs create new data risk | minimization, tenant partitioning, masking, role separation, retention and access audit |
| GPU/fabric assumptions remain untested | service-specific isolation matrix and authorized end-to-end negative tests |
| Fast growth outruns inventory | event-driven registration, reconciliation and launch gates tied to asset/service IDs |

## 14. First executive decisions

Within the first month, leadership should explicitly decide:

- which services and regions are in production scope;
- which isolation modes may carry which data classes;
- whether any provider administration may be public;
- who owns root/signing/KMS/BMC/fabric authority;
- authority, maximum lifetime, rollback criteria, and explicitly nonconformant status for any T0 emergency deviation;
- notification commitments and decision makers;
- support-access model and customer visibility;
- default tenant identity, MFA, egress and quota posture;
- evidence retention and customer assurance commitments;
- RTO/RPO and whether the business can rebuild from known-good sources;
- prohibited autonomous-agent action classes;
- resources and accountable owners for the first 90 days.

Without these decisions, security teams cannot reliably implement technical controls because the trust boundary and acceptable failure are undefined.
