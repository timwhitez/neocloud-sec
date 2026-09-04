# NeoCloud Cyber Security Scope and Limitations

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** project-authored implementation draft

## 1. What this project is

NeoCloud Cyber Security is a vendor-neutral reference baseline and implementation guide for specialized AI/GPU cloud services. It provides a bilingual control catalog, evidence and verification model, reference architecture, roadmap, metrics, governance, and implementation templates.

It is **not** a deployed security product, an adopted industry standard, a certification scheme, a formally accredited control framework, or evidence that any provider is secure. “NeoCloud” is used as a working term for specialized cloud services supporting accelerator-intensive AI and HPC workloads; providers may use different commercial and technical definitions.

## 2. Normative scope

Within this repository, the machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json) is authoritative for stable control IDs, tiers, bilingual requirements, evidence profiles, verification profiles, and metric associations. The security-baseline documents explain production gates and service overlays; other documents operationalize the catalog.

For a real service, applicable law, regulatory direction, contracts, customer commitments, documented service boundaries, and qualified applicability decisions determine external obligations. This project cannot make legal, privacy, safety, contractual, or certification determinations for an adopter.

## 3. Project-defined gates and targets

The five tiers, 18 domains, 90 controls, T0 production gates, default verification frequencies, roadmap dates, and numerical targets are design choices of this project. They are conservative planning defaults and testable operating rules—not claims that an external standards body or the industry has endorsed those exact values.

A failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` applicable T0 remains `NO_GO_NONCONFORMANT`. A legally authorized emergency business-continuity decision may permit time-bounded operation outside the baseline’s conformity result, but it cannot create `PASS`, `VERIFIED`, or a conformance claim.

## 4. Technology-specific limitations

Security properties must be validated on the exact deployed stack.

- **GPU sharing:** full-device dedication, hardware partitioning, hypervisor-mediated vGPU, and scheduler-level time-slicing/oversubscription are different mechanisms. Scheduler-level Kubernetes GPU time-slicing does not itself provide memory or fault isolation. Supported mediated vGPU and hardware-partitioned modes can have different, product-specific properties. Names alone do not prove isolation.
- **Accelerator cleanup:** GPU/HBM/cache/reset behavior is device-, mode-, firmware-, driver-, hypervisor-, error-state-, and workload-specific. Conventional media-sanitization guidance does not automatically prove volatile accelerator-state cleanup. When a defensible cross-tenant cleanup claim cannot be established, quarantine, retirement, or dedicated allocation may be required.
- **InfiniBand/RDMA:** P_Keys provide partition-membership semantics, not complete isolation proof. Effectiveness also depends on membership type, default partition, fabric-manager authority, DPU/NIC and storage configuration, topology, endpoint behavior, controller reconciliation, stale-state handling, and deployed-path negative tests.
- **NVLink/NVSwitch:** topology-aware placement and domain assignment are implementation inputs; an “NVLink domain” label is not, by itself, a tenant-security boundary.
- **Kubernetes:** provider-only controllers and databases should be private. A customer-facing managed API endpoint may be reachable through a public edge when explicitly approved, strongly authenticated, source/rate restricted, DDoS-protected, abuse-resistant, and fully audited.
- **Slurm:** accounts, associations, partitions, QOS, reservations, and MCS labels govern scheduling and visibility but do not replace OS/runtime, credential, storage, network/fabric, and node enforcement.
- **Attestation and confidential computing:** attestation reports measured claims under a specific product, root, policy, nonce/freshness model, and configuration. It does not by itself prove application behavior, end-to-end confidentiality, correct key release, or absence of side channels.
- **Supply-chain signatures:** a valid signature proves that a key signed an artifact. Safety still depends on source, build/training lineage, key custody, compatibility, policy, review, vulnerability state, admission, revocation, and recall.
- **Evidence independence:** independent assurance requires sufficient organizational and observational separation to challenge the implementer. It does not universally require a physically separate platform.

## 5. Shared responsibility and commercial boundaries

A provider remains accountable for controls over infrastructure it exclusively operates. Customers remain accountable for customer-controlled code, data classification, tenant-role assignment, guest configuration, and other contracted duties. Exact responsibility must be stated per service, service tier, and incident phase.

Secure defaults do not imply identical assurance across all SKUs. A provider may offer dedicated, sovereign, attested, or confidential-computing services, but it must accurately describe what each baseline and higher-assurance tier protects, shares, excludes, and requires from the customer.

## 6. Evidence and assurance limitations

A passing repository validator proves structural consistency, not deployed security. A policy, screenshot, vendor dashboard, scanner result, signature, or attestation is not sufficient on its own. Evidence must be current, scoped, protected, reproducible where possible, linked to the deployed path, and independently evaluated against relevant allowed, prohibited, failure, revocation, recovery, and cleanup paths.

Framework references and mappings are informative. Formal compliance or certification requires the exact framework version, jurisdiction, audit objective, service scope, evidence, and qualified assessor.

## 7. Publication and licensing

At this version the GitHub repository is private and no license has been selected. The content therefore must not be described as open source or openly licensed. Before public release, the owner should select an appropriate license for documentation, structured control data, scripts, schemas, and contributions; review third-party quotation and trademark constraints; remove sensitive material; and establish a supported private reporting path.

Repository topics are public even when attached to a private repository. The intended description, topics, publication checklist, and administrative safeguards are documented in [Repository Settings](../../.github/REPOSITORY_SETTINGS.md).

See [Accuracy Review](../../ACCURACY_REVIEW.md), [Security Policy](../../SECURITY.md), and [References](../../REFERENCES.md).
