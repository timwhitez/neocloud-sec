# SemiAnalysis / ClusterMAX coverage and validation guide

**Profile version:** 1.0.1  
**Review date:** 2026-09-05  
**Base catalog:** 1.0.0-draft.1

## 1. What the counts mean

The profile contains **40/40 project-authored mappings** and **20/20 mappings of the dated public Security-page snapshot**. These are records in this project, not executed infrastructure tests, a ClusterMAX score, an endorsement, or proof of complete access to SemiAnalysis's methodology.

The prior-coverage classification actually stored in the 40 records is **21 explicit, 12 partial, 7 gaps**. The previous 17/17/6 summary contradicted those records. Version 1.0.1 corrects the arithmetic rather than relabelling findings to fit a preferred total. These historical labels are project judgments, not independently measured industry statistics. Five article-level patterns and our five grouping labels are not a claim that every grouping reproduces the author's taxonomy exactly.

The earlier alternate-host count of 21 is retained as an unresolved historical observation, **not 21/21 coverage** or a newly verified total. The live public page can change. Scope every comparison to a retrieval date and exact URL; do not manufacture an extra requirement to reconcile counts.

## 2. Source and interpretation boundary

The article locator is [Most Neoclouds Suck At Security](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security). This review used publicly indexed excerpts; it did not retrieve the complete paid article. The Security requirements were checked at the [canonical criteria page](https://www.clustermax.ai/criteria/security), not the previously recorded `/security` path. The [public site](https://www.clustermax.ai/) identifies 2.1 as the current published rating and advertises 3.0 as coming soon at this review date.

Every mapped finding now has source IDs. A reference identifies the technical basis for a project interpretation; it does not assert that the source contains the exact project wording or demonstrates a provider implementation. Pricing, commercial partnerships, proprietary scoring and non-public criteria remain outside scope. An equivalent internal ISMS is not a substitute for a source criterion that specifically requests ISO/IEC 27001 certification; check the actual certificate, scope, expiry and exclusions.

## 3. Three views, not three automatic passes

Use three distinct views: **tenant black-box**, **provider white-box**, and **independent failure/recovery**. The first checks the customer-visible path; the second inspects configuration, ownership and operating processes; the third challenges failure and restoration behavior. Do not mark an unavailable view PASS. Where a view is genuinely inapplicable, preserve a separate justified applicability decision and review; do not invent a successful test result.

Repository CSVs are blank templates. Their state is `PROPOSED`, applicability is `UNKNOWN`, and results are `NOT_TESTED`. Copy them into a private assessment system before collecting real evidence. The repository validator rejects passed or verified template rows; it is not a production conformance engine.

## 4. Rules before any technical drill

Use written authorization, two synthetic tenants and non-sensitive canary data. Record exact service, environment, cluster, region, SKU, hardware, firmware, runtime, driver and policy versions. Establish an out-of-band recovery route and stop conditions before testing. Start with read-only inspection. Changes to a fabric, DPU or shared node require an approved maintenance window or isolated lab. Never submit exploit payloads, rotate live fabric keys, power-cycle production devices or probe a third-party tenant merely to complete this guide.

Evidence must identify the assertion, test ID, collector, independent reviewer, timestamps, validity, deployment scope, integrity method, result and limitations. Keep real credentials and key values out of reports. A hash identifies bytes; it does not prove collector trust or test truth. Missing evidence is `NOT_TESTED` or `INCONCLUSIVE`, not success. An applicable failed T0 remains `NO_GO_NONCONFORMANT` regardless of risk acceptance.

## 5. Priority drills

### A. InfiniBand data and management paths — SA-NC-015..022

NVIDIA documents distinct management-key classes, including **C_Key, CC_Key, PM_Key and N2N_Key**; these must not be collapsed into aliases. It also documents that P_Key partition checks do not apply to SMP MADs and that M_Key lease/recovery behavior matters when the manager stops responding. See [NVIDIA's security guide](https://networking-docs.nvidia.com/nvidiainfinibandsecurityoverviewandguidelines/security-in-infiniband).

Inspect a redacted key-class inventory, manager privileges, protected configuration, membership types, topology and endpoint enforcement. In an authorized test fabric, test allowed traffic, prohibited tenant traffic, manager failover, stale assignments and controlled reallocation independently. Validate management-message restrictions separately from data-plane partitions; include SR-IOV VF and supported SHARP paths.

**Pass:** all required prohibited paths are denied, intended traffic remains available, and policy is preserved or safely restricted during failover. **Stop:** unexpected shared-fabric instability or any non-test tenant impact. **Recovery:** restore approved manager state and keys through the established recovery route, quarantine uncertain assignments and independently retest before reopening. Do not treat a successful ping test as proof of RDMA or management isolation.

### B. BlueField RShim and host trust — SA-NC-012..014

[BlueField modes documentation](https://networking-docs.nvidia.com/bsp/480/modes-of-operation) distinguishes host-trusted and restricted operating boundaries. Record the actual product and mode instead of assuming that the presence of a DPU creates isolation.

Map host, ARM-side, RShim/tmfifo and OOB access, administration identities, firmware privileges and reassignment state. Use only provider-approved negative checks from the synthetic tenant's scope. Verify the documented transition and recovery requirements for the exact release before attempting a mode change; do not disable the sole management path.

**Pass:** tenant authority cannot administer the DPU or alter the protected fabric policy; legitimate recovery still works. **Stop:** management access becomes uncertain. **Recovery:** follow the approved vendor-specific recovery procedure, then verify identity, firmware, policy and reassignment cleanup. Lack of a safe recovery test is inconclusive, not proof of isolation.

### C. vCluster, kubelet and shared nodes — SA-NC-005..010

[Kubernetes multi-tenancy guidance](https://kubernetes.io/docs/concepts/security/multi-tenancy/) separates virtual control-plane isolation from data-plane isolation and requires a network plugin that actually enforces NetworkPolicy.

Inspect host-cluster and syncer privileges, node API access, admission exemptions, service accounts, CNI/CSI behavior and volume/snapshot authorization. With two test tenants, verify namespace/API denial, direct supported network paths, storage access and privileged workload rejection separately. A customer-facing managed API may use a protected public edge; do not confuse that with permission to expose provider-only databases or node administration.

**Pass:** every asserted boundary is demonstrated at its enforcement point. **Stop:** a test can reach a provider-only management capability or another tenant's volume. **Recovery:** revoke the test identities, quarantine affected allocations and review synchronization and admission state before retesting. A namespace, vCluster or Slurm label alone is not complete host/GPU/storage/fabric isolation.

### D. Grafana and Prometheus backends — SA-NC-035

[Grafana's data-source documentation](https://grafana.com/docs/grafana/latest/datasources/) describes default organization-wide query access and edition-specific data-source permissions. [Prometheus's security model](https://prometheus.io/docs/operating/security/) must be considered separately. Dashboard or folder access is not sufficient evidence of backend authorization.

Plant distinct synthetic metrics for tenants A and B. Test supported direct query, label/series and dashboard paths using each tenant's own identity. Inspect whether a trusted gateway enforces the tenant context and whether the backend is reachable around it. Test service credentials, alert routing, remote-read/write and support access where enabled. Record the actual Grafana edition and features; do not prescribe Enterprise-only permissions as though every edition has them.

**Pass:** neither tenant can retrieve the other's canary data through any in-scope enabled path. **Stop:** real data becomes visible; retain minimal redacted evidence. **Recovery:** revoke the overbroad credential, restrict backend access, correct server-side authorization and retest every path, not just the dashboard.

### E. GPU sharing and telemetry attribution — NCS-CMP-02

[NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html) states that its time-slicing replicas lack memory/fault isolation and notes a DCGM exporter attribution limitation with time-slicing. Do not infer per-container security coverage from node-level metrics. Hypervisor-mediated vGPU is a separate product-specific mechanism; see the [vGPU overview](https://docs.nvidia.com/ai-enterprise/release-8/latest/infra-software/vgpu/overview.html).

Verify the sold SKU against actual allocation mode, device and software versions. Use authorized benign memory/fault/reset/reassignment procedures on a representative lab device; record unavailable tests explicitly. Preserve per-allocation identity even where telemetry attribution is limited.

**Pass:** every advertised isolation and cleanup property is supported by the exact mechanism and test evidence. **Stop:** a reset could affect an unapproved workload. **Recovery:** quarantine uncertain devices or allocations and use supported known-good provisioning. Load the normative erratum before interpreting the raw catalog requirement.

### F. Agent scope, model output and revocation — SA-NC-031..034

This is a project-designed test, not a claim of an external certification requirement. Treat the goal, tenant, tool, data, egress and cost limits as a versioned authorization envelope. An agent cannot expand that envelope; an independently authorized delegator can approve a new one, with fresh scope and an audit trail.

Use benign injected instructions and canary data to test that external content cannot change tool grants, approval authority or completion evidence. Test credential revocation, budget exhaustion, repeated failure and verifier unavailability. Test cache/session isolation separately from prompt filtering.

**Pass:** prohibited actions are blocked by enforcement outside the model, and high-impact completion requires independent evidence. **Stop:** an action would leave the test scope. **Recovery:** revoke grants, stop queued actions, restore approved state and independently verify. A model saying “done” is not completion evidence.

## 6. Local checks and effective catalog

Install the explicitly declared validation dependencies once, then run locally:

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/check_local.py
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

The first two legacy checks remain standard-library scripts. Strict profile validation now uses jsonschema, actually evaluates all three document/schema pairs, checks date formats, rejects external schema references, verifies CSV mappings and requires unassessed templates. It fails when required files or dependencies are absent. It does not fetch websites or test cloud infrastructure.

The compiler emits a bundle containing `catalog` and input/output digests. It applies the named CMP-02 correction to a copy without changing IDs or tiers. Unknown targets, duplicate/conflicting corrections and base-version mismatches fail instead of being ignored. Digests are provenance identifiers, not signatures or attestations.

## 7. Related artifacts

Use the [profile](../../controls/semianalysis-public-findings-profile.v1.json), [schema](../../controls/semianalysis-public-findings-profile.v1.schema.json), [errata](../../controls/neocloud-security-baseline.v1.errata.json), [40-pattern template](../../templates/semianalysis-public-findings-assessment.csv), [20-item template](../../templates/clustermax-public-security-requirements-assessment.csv), and [review record](../../reviews/2026-09-05-validation-audit.md). This guide adds priority procedures; it does not claim that all 40 mappings are implemented automation or that any provider passed.
