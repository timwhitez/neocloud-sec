# Scope and limitations

**Core version:** 1.0.0-draft.1 · **Reviewed:** 2026-09-05

## Project boundary

This is a project-authored, vendor-neutral reference baseline and implementation guide for AI/GPU clouds. It contains documentation, control catalogs, templates and local checks; it is not a deployed security product, formal standard, certification, legal determination or provider rating. “NeoCloud” is a working service category; actual trust boundaries must be documented per service and contract.

The core catalog plus applicable version-bound errata define project requirements. External law, regulation, contracts and qualified applicability decisions determine obligations; a project mapping cannot establish legal compliance or certification.

## Decisions and assurance

Tiers, domain/control counts, roadmap dates, targets and review frequencies are project design choices, not proven industry averages. An applicable T0 that is failed, unknown, expired, inconclusive or untested remains NO_GO_NONCONFORMANT. An authorized business-continuity decision may record continued operation outside conformance but cannot turn the control into PASS or VERIFIED.

Repository validation checks structure and declared relationships, not deployed effectiveness. Evidence must be scoped, current, protected, reproducible where possible and independently evaluated. Different names alone do not establish reviewer independence. Administrative/observational separation may suffice; physical separation depends on the threat model.

## Technology boundaries

GPU dedication, hardware partitioning, mediated vGPU and device-plugin time-slicing have different properties. Test exact hardware, firmware, driver, hypervisor, scheduler, topology, mode and error/lifecycle state. Device dedication to a new tenant is not proof of prior-data cleanup. Media sanitization guidance does not by itself prove volatile accelerator-state erasure.

P_Key, NVLink-domain labels, Kubernetes namespaces, vCluster or Slurm MCS are not universal tenant-isolation proofs. Provider-only controllers, databases and OOB paths need governed private access. Explicitly approved customer-facing API edges are distinct from exposing provider internals. Network, storage, node, GPU, telemetry and support boundaries require separate evidence.

Attestation reports specific measured claims under a root/policy/freshness model; it does not prove safe application behavior, correct end-to-end key release or absence of side channels. Signatures require source, key custody, compatibility, policy and revocation context. Agent goals/scopes cannot be broadened by the agent itself; a separately authorized new envelope may approve a legitimate next stage.

## Shared responsibility

Provider-exclusive roots remain provider-owned. Customer-controlled code, guest configuration, data classification, tenant roles and application policy remain customer duties within the service contract. Higher-assurance SKUs may differ, but their shared resources, exclusions and evidence must be described accurately. No commercial label removes a technical control requirement.

## Source and testing limits

The [current review](../../reviews/2026-09-05-evidence-followup.md) records incomplete full-article access and unresolved differences between ClusterMAX detail/overview pages. Mapping 40 project patterns or 20 dated items does not prove exhaustive coverage, equivalent scoring or provider compliance. Sources change; verify the exact page, date, service scenario and product version before relying on a claim.

This follow-up tests synthetic evidence records and the offline record checker. The earlier mapping regression suite is preserved but not rerun in this follow-up. No production service, GPU memory, fabric, tenant workload or recovery system was actively tested. The [runbooks](VALIDATION_RUNBOOKS.md) describe the authorization, evidence and execution still required.

## Publication and licensing

As observed on 2026-09-05, the repository is public. Earlier private-repository descriptions are historical snapshots, not current status. No explicit reuse license has been selected; do not infer licensing from visibility. GitHub About, topics, reporting and protection settings are administrative state, not automatically applied by documentation. Verify a working confidential reporting route before transmitting sensitive evidence.
