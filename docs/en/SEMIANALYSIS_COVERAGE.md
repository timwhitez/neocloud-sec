# SemiAnalysis / ClusterMAX Public Security Coverage

**Profile version:** 1.0.0  
**Review date:** 2026-09-05  
**Base NeoCloud catalog:** 1.0.0-draft.1  
**Status:** project-authored public-findings interoperability overlay

## 1. Answer

The original 90-control NeoCloud catalog covered the main categories raised in the publicly accessible SemiAnalysis NeoCloud security material—tenant escape, weak shared control planes, vulnerable container/GPU software, BMC/OOB and DPU paths, InfiniBand/RDMA isolation, patching, monitoring and assurance—but several requirements were only implicit.

This update makes the publicly observable coverage explicit:

- **5** high-level public article patterns are decomposed by this project into **40 atomic, test-oriented patterns**.
- Before this update, the audit classified **17 as explicit, 17 as partial and 6 as material gaps**.
- After this update, all **40/40 are mapped** to stable NeoCloud controls, evidence expectations and three assurance views.
- The **20/20 requirements currently enumerable on the canonical public ClusterMAX Security page** are mapped to the same stable controls and an assessment template.

“Mapped” does **not** mean implemented, passed, certified or endorsed. A real provider must still scope each row to a concrete service, region, cluster, SKU, hardware, firmware, driver, orchestrator and date, then produce current evidence and an independent result.

## 2. What was already strong

The base catalog already addressed:

- API object/action/tenant authorization and private provider administration;
- tenant separation across compute, storage, Ethernet, InfiniBand/RDMA, DPU and OOB paths;
- Kubernetes and Slurm controller, admission, scheduler, plugin and node controls;
- host, runtime, driver, firmware and accelerator lifecycle;
- data/model/artifact provenance, admission, revocation and deletion;
- agent identity, tool mediation, approval, stop, trace and verifier controls;
- vulnerability discovery, staged remediation and deployed-state verification;
- protected telemetry, incident command, recovery, sanitization and independent testing.

These controls remain the stable normative core. The new profile does not add a second competing baseline.

## 3. Material gaps that were made explicit

| Gap before this update | Added treatment |
|---|---|
| InfiniBand control was centered on P_Key and did not explicitly enumerate management/service keys | Added M_Key, SM_Key, SA_Key, C_Key/CC_Key, VS_Key, SHARP AM_Key, service-key and per-job-key checks |
| DPU coverage did not name BlueField RShim/tmfifo_net0 and privileged adapter paths | Added RShim/tmfifo_net0, DPU identity/firmware, SR-IOV VF, QP0, MAD and privileged-operation tests |
| Shared Kubernetes and observability risks were implicit | Added vCluster/shared-control-plane, kubelet/node API, Prometheus/Grafana data-source, credential and tenant-isolation tests |
| Patch management did not explicitly model vendor embargo and a dynamic minimum-safe version | Added prerelease advisory intake, exploitability-based minimum-safe version, canary, deployed-state verification, recall and rollback |
| Customer-visible testing was not separated from provider and independent assurance | Added tenant black-box, provider white-box and independent failure/recovery result fields |
| Vulnerability disclosure and future-criteria drift were not explicit enough | Added trusted reporting/remediation, periodic retest and source/criterion change tracking |

## 4. Important technical correction: “time-slicing” is not one mechanism

The base catalog used the generic term **time-slicing** too broadly. The normative erratum now separates:

1. full-device dedication;
2. hardware partitioning;
3. hypervisor-mediated vGPU;
4. scheduler-level bare-device-plugin time-slicing.

Kubernetes GPU Operator/device-plugin time-slicing does not itself provide memory or fault isolation between replicas. A mediated vGPU may have product-, GPU-, hypervisor-, manager/driver-, firmware-, topology- and configuration-specific isolation properties. No isolation claim may be inferred from the label “time-sliced”; it must be stated and tested for the deployed mechanism.

See [`NCS-BASELINE-V1-ERRATA`](../../controls/neocloud-security-baseline.v1.errata.json).

## 5. Coverage model

Each atomic pattern is evaluated through three distinct views:

| View | Question |
|---|---|
| **Tenant black-box** | Can a customer reproduce prohibited reachability, isolation, privilege, data, version or disclosure behavior using only supported interfaces? |
| **Provider white-box** | Do architecture, configuration, key hierarchy, controller state, ownership, operational process and evidence support the claim? |
| **Independent failure/recovery** | Does a qualified independent party reproduce the control under misconfiguration, stale state, revocation, failure, recovery and reassignment conditions? |

The public customer-perspective CLI/audit path is useful but is only a subset of full assurance. Architecture/process review and controlled failure/recovery testing remain necessary for high-impact claims.

## 6. High-priority explicit checks

### InfiniBand/RDMA and fabric management

Verify, where applicable:

- P_Key membership, type, default partition, endpoint enforcement and stale-state cleanup;
- M_Key, SM_Key, SA_Key, C_Key/CC_Key and VS_Key ownership, uniqueness, rotation, revocation and audit;
- SHARP AM_Key, service-key and per-job key separation;
- Fabric Manager identity, least privilege, allowed GUID policy and protected administrative paths;
- SAETM/MAD abuse controls, QP0 restrictions and SR-IOV VF limitations;
- RoCE VLAN/VXLAN and storage-path tenant separation;
- DPU/NIC assignment, firmware, certificates, controller state and reassignment cleanup.

### Kubernetes, shared nodes and observability

Verify:

- provider-only API server, etcd, kubelet and node-management paths;
- vCluster/shared-control-plane host-cluster and synchronization boundaries;
- admission, RBAC, privileged workloads, hostPath, host network/PID/IPC and device-plugin/operator privileges;
- CNI/CSI and storage/snapshot authorization;
- Prometheus/Grafana tenant labels, data-source authorization, dashboard/query isolation, shared service credentials, alert routing, retention and support access.

### Vulnerability and patch intelligence

Maintain:

- exact deployed version inventory for container toolkit, runtime, kubelet, kernel, GPU driver, firmware, DPU, fabric manager and orchestrator;
- a dynamic minimum-safe version based on the actual exploit path and deployed configuration—not a permanently hard-coded version;
- trusted vendor embargo/prerelease advisory intake where contractually available;
- canary/staged rollout, rollback, quarantine and post-deployment verification;
- customer notification, vulnerability disclosure and remediation-retest paths.

### Hostile artifacts and AI workloads

Treat images, renderers, models, checkpoints, prompts, RAG sources, memory, skills, plugins, responses and caches as untrusted inputs until admitted by policy. Test deserialization, executable formats, tenant cache/session isolation, model output handling, tool invocation and egress.

## 7. ClusterMAX boundary

ClusterMAX is broader than cybersecurity. Its public framework includes dimensions such as lifecycle, orchestration, storage, networking, reliability, monitoring, pricing, partnerships and availability in addition to security. This project maps:

- the Security dimension directly;
- security-relevant portions of lifecycle, orchestration, storage, networking, reliability, monitoring and availability;
- no price, commercial-partnership, proprietary weighting or overall rating logic.

At the review cut-off, the canonical public Security page exposed **20 independently enumerable requirements**. An alternate ClusterMAX host reported **21 Security criteria**, but the additional item could not be independently enumerated. The repository therefore claims **20/20 mapping of the canonical public page**, not 21/21, exact criteria parity, a rating or certification.

## 8. Artifacts

- [Machine-readable public-findings profile](../../controls/semianalysis-public-findings-profile.v1.json)
- [Profile JSON Schema](../../controls/semianalysis-public-findings-profile.v1.schema.json)
- [Normative v1 errata](../../controls/neocloud-security-baseline.v1.errata.json)
- [40-pattern assessment template](../../templates/semianalysis-public-findings-assessment.csv)
- [20-item canonical public Security-page assessment](../../templates/clustermax-public-security-requirements-assessment.csv)
- [Local profile validator](../../scripts/validate_semianalysis_profile.py)

## 9. Definition of coverage

A row is **mapped** when a stable NeoCloud control, minimum evidence and test path exist. It is **verified** only when a scoped provider implementation produces current evidence and a qualified independent validator returns `PASS`.

A failed, unknown, stale, `INCONCLUSIVE` or `NOT_TESTED` applicable T0 remains `NO_GO_NONCONFORMANT`.
