# NeoCloud validation runbooks

**Review date:** 2026-09-09 · **Profile:** 1.0.1 · **Core catalog:** 1.0.0-draft.1

These are project-authored test plans, not executed infrastructure tests, vendor certifications, or SemiAnalysis scoring criteria. These ten operational runbooks complement the [public-findings profile](../../controls/semianalysis-public-findings-profile.v1.json); they do not modify its schema or claim a machine-validated per-pattern join. Use the [effective-catalog compiler](../../scripts/compile_catalog.py), including version-bound errata.

## Test authorization and evidence contract

Before testing, record service, region, cluster, SKU, tenant IDs, exact running versions, approved targets/actions, test window, operator, independent reviewer, recovery owner and abort criteria. Use two synthetic tenants with distinct harmless markers. Test only explicitly authorized resources. Do not copy real tenant data, management keys, raw GPU memory or confidential vendor advisories into this repository.

Every runbook needs an allowed-path control and a prohibited-path check. A denial caused only by an unrelated outage is not a successful authorization test. Record the observed decision, actual target effect, request ID, effective policy and time. Report each applicable view separately: tenant black-box, provider white-box and independent failure/recovery. Record justified non-applicability outside the four-result enum; never convert an unexecuted view to PASS. Any applicable T0 without current sufficient evidence remains NO_GO_NONCONFORMANT. Use the optional [evidence and advisory record checks](../EVIDENCE_VALIDATION.md) for metadata, not as proof of these outcomes.

<a id="rb-01"></a>
## RB-01 — API, scheduler, vCluster and node boundaries

**Arrange:** Create tenant A/B test resources, unique workload identities and approved API credentials. Export effective RBAC, admission, syncer/operator permissions, CNI and node API configuration.

**Exercise:** Show A can access its own resource but cannot read, attach, mutate or impersonate B's resource. Include kubelet, host-cluster objects and service-account tokens. For vCluster, examine the host-cluster permissions of syncers and shared-node components; a virtual control plane alone does not prove node isolation. Test an interrupted allocation and expired credentials without submitting destructive workloads. After revoking a previously permitted cross-namespace association or operator-granted permission, use disposable identities and harmless records to check that the operator's reconciliation removes or rotates the backend credentials it generated [S9], and that the old disposable credential is denied at the backend (for example the datastore) while an independently authorized identity still succeeds. A Kubernetes API denial alone does not establish revocation of an existing backend credential; key-lifecycle requirements still apply to the rotated material. For NCS-IAM-04, NCS-KMS-02 and NCS-ORC-04, also inspect actual service-account grants and every enabled authorization path; controller selectors and local caches are not substitutes for resource-side authorization [S10].

**Accept/evidence:** Tenant context survives every controller transition; unauthorized requests have no target-side effect; partial allocation is rolled back or quarantined. Save redacted policy exports, both request traces and actual-state reconciliation. Redact credentials and retain only decision and request identifiers. Abort on foreign data visibility, unexpected privilege or any unexpected post-revocation access; complete containment, rotation and an independent retest before reopening the path.

<a id="rb-02"></a>
## RB-02 — Runtime vulnerabilities and safe rollout

**Arrange:** Inventory installed AND running toolkit, runtime, driver, firmware, kernel and orchestrator versions by asset. Identify the exact managed service, OS image/build, controller and running processes rather than only a package label or image family. Associate advisories with affected configuration, vendor-supported fix/backport, compatibility and customer impact, distinguishing four propagation stages: upstream fix, distribution backport, provider image publication and actual node replacement. A numerically newer version alone is not a safe-version proof.

**Exercise:** In an isolated canary, apply the approved update, restart affected components where required, verify loaded versions and run the scoped regression. Record both the permitted workload's success and the reviewed denied boundary. Simulate a failed update and stale node inventory. Establish advisory intake and escalation; prerelease/embargo access depends on vendor eligibility and is not universally available. An optional offline advisory-triage register for this metadata is documented with the [evidence checkers](../EVIDENCE_VALIDATION.md).

For NCS-ASM-01, NCS-ORC-04 and NCS-CMP-03, record image/build identity and replacement or boot evidence, then verify workload completion, policy enforcement and recovery. A changed image-family pointer does not update existing nodes [S11]. Hotpatch enrollment does not remove a bulletin's reboot requirement; check the specific update rather than inferring its behavior from a standing calendar [S12]. Provider-only evidence remains a provider responsibility.

Treat a rootless feature gate, a configured user namespace and an actually rootless node as different states. Evaluate supported CNI/CSI/device/GPU combinations and recovery before an optional migration; do not mandate a beta feature or treat it as protection against every kernel flaw [S17].

**Accept/evidence:** Vulnerable or unverified nodes cannot silently return to the healthy pool. Quarantine unverified capacity; provider image publication alone is not proof that any specific node was recreated or patched, and provider-only evidence stays a provider responsibility. Rollback must not restore a known exploitable configuration without isolation and an explicit nonconformance decision. Keep advisory IDs, signed package provenance where available, canary results, deployed-state evidence and retest outcome. Stop on service SLO breach or loss of recovery access.

<a id="rb-03"></a>
## RB-03 — BlueField, RShim and provider recovery

**Arrange:** Record DPU model, BSP/DOCA/firmware, NIC/DPU mode, host privilege setting, Arm-side ownership and provider BMC recovery. DPU mode is not automatically a hostile-host boundary: NVIDIA documents trusted-host defaults and additional restricted-host controls [S3].

**Exercise:** From an authorized synthetic tenant host, check the intended deny boundary for RShim/TMFIFO, flash, tracer/counters and port ownership. Inspect configuration and access decisions rather than reading secrets or reflashing hardware. Confirm the provider recovery path remains available independently of the tenant host. Validate supported mode transitions and resets only in an approved maintenance lab.

**Accept/evidence:** Denied host capabilities remain denied after the documented lifecycle transition; provider recovery is tested; stale assignments are removed before reuse. Save privilege-state exports, redacted path checks and recovery results. Abort if management access is lost. Do not use a generic reset command across DPU generations.

<a id="rb-04"></a>
## RB-04 — InfiniBand, RoCE and management keys

**Arrange:** Distinguish P_Key partition membership from management authentication and payload encryption. Inventory applicable M_Key, SM_Key, SA_Key, VS_Key, PM_Key, congestion-control keys, Class C/N2N and SHARP AM/job/service key roles. Class C/N2N must not be silently collapsed into a similarly named congestion-control key. Record key IDs/owners, never values. Match parameter names to the installed UFM/OpenSM release [S4, S5].

**Exercise:** Test authorized tenant data paths and prohibited cross-tenant paths. Independently inspect default partition, membership type, PF/VF authority, QP0/MAD restrictions and allowed manager GUIDs. Examine relevant SA trust, rate limiting and SHARP job separation. A dashboard's security check is configuration evidence, not end-to-end proof. In a lab, test stale-controller state and reassignment cleanup with bounded traffic; never flood a production fabric or rotate fleet keys during discovery.

For CNI or provider-network migrations, inventory OS/CNI compatibility, DNS, service and storage dependencies before default-deny rollout. Pair allowed workload traffic with denied cross-tenant paths and preserve independent OOB access. A provider retirement is a scoped migration trigger, not a reason to standardize every cloud on one CNI. Kubernetes NetworkPolicy does not replace fabric, DPU or storage isolation [S18]; keep RB-03, RB-06 and RB-09.

**Accept/evidence:** No unauthorized management or cross-tenant traffic succeeds; authorized control traffic survives policy changes. Capture topology, redacted effective configuration, path results and rollback/recovery. Abort on fabric instability, unexpected reachability or loss of management quorum.

<a id="rb-05"></a>
## RB-05 — Prometheus, Grafana and telemetry

**Arrange:** Seed distinct harmless time series for A/B. Identify Grafana edition, organizations, data-source credentials and every direct backend/proxy/remote-read route. Prometheus assumes HTTP users can access its time series; labels are not authorization [S6]. Grafana Viewer access can permit arbitrary data-source queries, not just the visible dashboards [S7, S8].

**Exercise:** Query outside dashboard navigation; attempt a foreign-tenant query and a forged tenant selector through each supported path. Verify whether tenant context is bound by a trusted proxy or backend rather than supplied by the caller. Confirm alert routing, retention and support access. Check edition-specific data-source permission features before relying on them. Correlate policy changes, operator reconciliation, credential lifecycle, denied backend use and storage decisions through tenant-safe correlation identifiers, and alert when a required audit source is missing; a dashboard, a metric label or a successful collector exit is not evidence of tenant authorization.

Include shared dashboard creation/import and visualization rendering in the trust model, not only queries. Separate writer and viewer privileges and inspect the exact deployed dashboard component and managed-service patch status [S13]. Use vendor-supported harmless fixtures and authorization checks; do not reproduce browser-execution payloads. A self-managed fixed version is not evidence that a managed service has completed its own remediation.

For each provider audit source, record supported services/actions, enablement, delivery and retention; verify that a harmless expected event arrives and that a missing source is detected. An offered audit feature or a successful collector exit does not prove coverage [S14]. Never export real tenant records to this repository.

**Accept/evidence:** Isolation holds at the backend credential/query boundary and cannot be bypassed by direct access or editable labels. Use separate appropriately scoped organizations/backends where needed. Record query results and effective backend grants. For GPU Operator time-slicing, record NVIDIA's DCGM-Exporter container-attribution limitation [S1]; do not invent per-container accountability from unavailable metrics. Abort on a foreign series or secret disclosure.

<a id="rb-06"></a>
## RB-06 — Storage, snapshots, deletion and restore

**Arrange:** Create synthetic objects, volumes and snapshots for A/B. Record CSI/controller identities, KMS ownership, immutable backup retention and contractual deletion scope. For NCS-API-01, NCS-DAT-04 and NCS-ORC-02, review PV-creation authority, the deletion options actually enabled, CSI identity, filesystem/access-point ownership and the cloud resource policy together [S15], preferring patched vendor software and least privilege for the controller.

**Exercise:** Reject foreign attach, export and restore requests at the actual storage boundary. Validate object/tenant ownership with inert unit fixtures or vendor-supported non-destructive checks; never construct destructive volume handles or delete real data. Verify that authorized storage use still succeeds after a policy change. Restore a test backup while a primary dependency is unavailable. Check replicas, caches, snapshots, local media and retention-delayed backup deletion. A deletion request must not be described as immediate physical erasure of every retained immutable backup. A driver defect is not automatically a storage-service breach; disabling an affected configuration is an applicability claim that requires evidence and revalidation.

**Accept/evidence:** Recovery meets the declared integrity/isolation/RTO/RPO objectives; deletion reports identify delayed or excluded copies and their expiry. Preserve object lineage, access decisions, restore checks and key dependencies. Abort on access outside the approved synthetic set or evidence that the restore crosses tenant boundaries.

<a id="rb-07"></a>
## RB-07 — Hostile artifacts and parsers

**Arrange:** Use synthetic unsupported or intentionally invalid input fixtures, an isolated loader and no production credentials. Record accepted formats, deserialization permissions, artifact digests, provenance, signature policy and runtime boundaries. For NCS-SSC-02 and NCS-DAT-03, bind the digest in artifact admission to the approved signer/builder identity, the canonical source repository, the build type and the expected build inputs; a valid signature alone is insufficient [S16].

**Exercise:** Reject unapproved executable serialization and unauthorized artifact sources. Verify that a valid signature from an unapproved signer is not treated as safety. Revoke a test artifact and verify registry, deployment, renderer and cache invalidation. Unknown or unauthorized inputs need an explicit decision rather than silent acceptance. Keep the controls applicable to the actual format: scanning is not proof that arbitrary model code is safe. Retain loader isolation rather than introducing a mandatory agent framework.

**Accept/evidence:** Denial is enforced before privileged execution; recall reaches cached/deployed copies; known-good rebuild is reproducible. Capture loader decisions, provenance and recall evidence. Abort on unexpected execution, persistence, credential access or out-of-scope network traffic. No real malicious payload is required for this runbook.

<a id="rb-08"></a>
## RB-08 — Agent authorization envelopes

**Arrange:** An external authorized delegator defines the goal, tenant, resources, tools, parameters, destinations, budget, expiry and policy version. “Immutable” means the agent cannot enlarge that authorization envelope, not that a legitimate human can never approve a new stage.

**Exercise:** Use benign injection text to request broader access, change approval state or treat tool/model output as authorization. Test a changed tool argument after approval, credential expiry, repeated failure, timeout and budget exhaustion. A new goal or broader scope requires a newly approved envelope, bound to the changed parameters; old approvals cannot be replayed against new actions. For data-accessing agents, enforce read-only and least-privilege permissions at the database or resource identity, not only in tool descriptions, prompts or SQL filtering; a tool declaration is not authorization. Exercise an unauthorized synthetic request and a harmless unsupported format, verify the allowed path still functions and the denied side effects did not occur, and record rollback/recall and the identities used.

For NCS-AIR-03, review the inherited role memberships and executable functions behind the database/resource identity [S19]. With disposable records and identities, verify an allowed read and a denied unauthorized side effect at the backend, follow RB-01 for credential revocation, and apply vendor fixes as well; least privilege does not establish that vulnerable software is remediated.

**Accept/evidence:** The resource-side decision denies unauthorized action even if the model proposes it. Record approval binding, action/result traces, stop decisions and independent post-condition checks. Budget/time/retry rules can be deterministic; semantic success and uncertainty are not guaranteed to be perfectly decidable. On ambiguity, leave the result unverified and escalate instead of allowing self-certification.

<a id="rb-09"></a>
## RB-09 — GPU, serving caches and reassignment

**Arrange:** Declare exact host/device dedication, MIG/hardware partition, mediated-vGPU or device-plugin time-slicing mode. NVIDIA's device-plugin time-slicing lacks memory/fault isolation between replicas; mediated vGPU properties are product/version/configuration dependent [S1, S2].

**Exercise:** In an authorized lab, test memory, fault, DMA, reset and reassignment claims appropriate to the SKU. In serving, test routing, KV cache, session and prefix-cache partitioning with synthetic markers. Reuse after failure is a different case from a clean shutdown. Do not treat ordinary disk sanitization guidance as proof of volatile accelerator-state cleanup.

**Accept/evidence:** Claims are backed by vendor-supported behavior and deployed-path evidence. Quarantine when reset/cleanup is inconclusive; dedication to a new tenant does not itself erase old data. Record reset scope, fault domain, remaining shared resources and attribution limits. Stop immediately on a cross-tenant marker or hardware error.

<a id="rb-10"></a>
## RB-10 — Independent assurance and source changes

**Arrange:** Define the assessment population, sampling basis, current source URL, publication/retrieval dates, source status and access limitations. Distinguish source requirements from project recommendations. A certification requirement is not met by merely implementing similar controls.

**Exercise:** Reconcile every CSV control mapping to JSON. Introduce a missing control, stale PASS, duplicated source, malformed CSV and schema type error into a disposable fixture. Confirm the validator fails. Reconcile detailed and overview source pages by item and scenario, not just by count.

For legal or contractual notification duties, have the responsible owner determine product, supplier role, jurisdiction, contract, trigger and effective date before claiming applicability [S20]. Exercise incident intake, evidence preservation, awareness-time recording, authorized notification and recovery with harmless scenarios. Distinguish each reporting clock and a future deadline from an already-effective duty. Recheck platform availability and recipient instructions; neither a draft standard nor a roadmap proves an operational reporting channel.

**Accept/evidence:** Missing, untested, expired and inconclusive evidence stay visible. Separate mapped documentation, valid metadata, implemented controls and independently verified outcomes. A different reviewer name alone does not establish independence. Save the exact reviewed commit and limitations; local schema tests never confer a ClusterMAX rating. Follow the normal [research and change process](../../CONTRIBUTING.md#recurring-research), not a second review catalog.

## Primary sources and limitations

- [S1 — NVIDIA GPU Operator sharing](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html)
- [S2 — NVIDIA mediated vGPU overview](https://docs.nvidia.com/ai-enterprise/release-8/latest/infra-software/vgpu/overview.html)
- [S3 — BlueField modes](https://networking-docs.nvidia.com/bsp/latest/modes-of-operation)
- [S4 — UFM 6.23.20 optional configurations](https://docs.nvidia.com/networking/display/ufmenterpriseumv62320/Optional-Configurations)
- [S5 — UFM 6.26.1 Security tab](https://networking-docs.nvidia.com/ufmenterpriseum/6.26.1/security-tab)
- [S6 — Prometheus security model](https://prometheus.io/docs/operating/security/)
- [S7 — Grafana security](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/)
- [S8 — Grafana roles and permissions](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/)
- [S9 — Elastic ECK ESA-2026-146](https://discuss.elastic.co/t/elastic-cloud-on-kubernetes-3-5-0-security-update-esa-2026-146/390106)
- [S10 — Kubernetes RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [S11 — Google Cluster Toolkit security bulletins](https://docs.cloud.google.com/cluster-toolkit/docs/security-bulletins)
- [S12 — Microsoft Server 2025 Azure Edition September 8 baseline](https://support.microsoft.com/en-us/servicing/os/hotpatch/windows-server-2025/2026/september-8-2026-baseline)
- [S13 — AWS OpenSearch Dashboards bulletin 2026-102](https://aws.amazon.com/security/security-bulletins/2026-102-aws/)
- [S14 — Nebius audit service/action coverage](https://docs.nebius.com/audit-logs/services)
- [S15 — AWS EFS CSI bulletin 2026-099](https://aws.amazon.com/security/security-bulletins/2026-099-aws/)
- [S16 — SLSA v1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [S17 — Kubernetes v1.37 rootless beta](https://kubernetes.io/blog/2026/09/04/kubernetes-v1.37-rootless-beta/)
- [S18 — Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [S19 — AWS postgres-mcp-server bulletin 2026-101](https://aws.amazon.com/security/security-bulletins/2026-101-aws/)
- [S20 — European Commission CRA reporting guidance](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting)

Vendor behavior is version/edition dependent. These sources support specific mechanisms, not all recommendations in a runbook. See the [source-review record](../../reviews/2026-09-05-evidence-followup.md) for retrieval limitations and unresolved external-framework differences.
