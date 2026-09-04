# NeoCloud Cyber Security Scope and Limitations

**Version:** 1.0.0-draft.2  
**Baseline date:** 2026-09-04

## 1. What this project is

NeoCloud Cyber Security is a project-defined, vendor-neutral reference baseline and implementation guide for specialized AI/GPU cloud services. It provides a control catalog, evidence model, verification method, reference architecture, roadmap, metrics, and implementation templates.

It is not a deployed security product, an adopted industry standard, a certification scheme, or a formally accredited control framework. “NeoCloud” is used operationally; service providers may use different commercial and technical definitions.

## 2. Normative scope

Within this repository, the machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json) is authoritative for control IDs, tiers, bilingual requirements, evidence profiles, verification profiles, and metric references. The prose documents explain and operationalize that catalog.

For a real service, the controlling hierarchy is applicable law, regulatory direction, contract and customer commitment, followed by the documented service boundary and applicability decision. This project cannot determine legal or contractual applicability.

## 3. Project-defined gates and targets

The five tiers, 18 domains, 90 controls, T0 production gates, review frequencies, roadmap dates, and numerical targets are design choices of this project. They are intended to be conservative planning defaults and testable operating rules, not claims that an external standards body or the industry has endorsed those exact values.

A failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` applicable T0 cannot be marked conformant. An emergency deviation may be authorized to maintain service, but it remains explicitly nonconformant and cannot become `PASS` or `VERIFIED` without independent validation.

## 4. Technology-specific limitations

Security properties must be validated on the exact deployed stack.

- **GPU sharing:** full-GPU dedication, hardware partitioning, hypervisor-mediated vGPU, and scheduler-level time-slicing are different mechanisms. Scheduler-level Kubernetes GPU time-slicing does not itself provide memory or fault isolation; supported mediated vGPU and hardware-partitioned modes can have different properties. Names alone do not prove isolation.
- **Accelerator cleanup:** GPU/HBM/cache/reset behavior is device-, mode-, driver-, firmware-, hypervisor-, and workload-specific. Conventional media-sanitization guidance does not automatically prove volatile accelerator-state cleanup.
- **InfiniBand/RDMA:** P_Keys provide partition membership semantics, but complete isolation also depends on membership type, default partition, fabric-manager authority, DPU/NIC and storage configuration, controller reconciliation, and real negative-path tests.
- **NVLink/NVSwitch:** topology-aware placement and domain assignment are implementation inputs; the label “NVLink domain” is not, by itself, a tenant-security boundary.
- **Kubernetes:** a managed customer-facing API endpoint need not be universally private, but provider-only controllers and databases must be protected. A public endpoint requires an explicit hardened service profile and abuse-resistant access controls.
- **Slurm:** accounts, partitions, QOS, associations, and MCS labels help govern scheduling and visibility. They do not replace OS/runtime, credential, storage, network/fabric, and node controls.
- **Attestation and confidential computing:** attestation reports measured state under a specific root and policy. It does not by itself prove application behavior, end-to-end confidentiality, correct key release, or absence of side channels.
- **Supply-chain signatures:** a valid signature proves that a key signed an artifact; safety also depends on source, build/training lineage, key custody, policy, vulnerability state, review, and revocation.
- **Evidence separation:** independent protection is a trust and administrative-separation requirement. It does not always require a physically separate platform.

## 5. Shared responsibility and commercial boundaries

A provider remains accountable for controls over infrastructure it exclusively operates. Customers remain accountable for customer-controlled code, data classification, tenant role assignment, guest configuration, and other contracted duties. Exact responsibility must be stated per service and incident phase.

Secure defaults should not be confused with identical service tiers. A provider may offer higher-assurance dedicated, sovereign, attested, or confidential-computing services, but it must accurately state what the baseline SKU does and does not protect.

## 6. Evidence and assurance limitations

A repository validator proves structural consistency, not substantive deployment security. A policy, screenshot, vendor dashboard, attestation, signature, or passing CI job is not sufficient on its own. Evidence must be scoped, current, protected, reproducible where possible, and independently evaluated against positive and prohibited paths.

Framework references and mappings are informative. Formal compliance or certification requires the exact framework version, jurisdiction, audit objective, service scope, evidence, and qualified assessor.

## 7. Publication and licensing

At this version the GitHub repository is private and no license has been selected. The content therefore must not be described as open source or openly licensed. Before public release, the owner should select a license appropriate for documentation, control data, code, and contribution policy; review third-party quotation and trademark constraints; and enable an appropriate private vulnerability-reporting path.

See [Project Metadata](../../PROJECT_METADATA.md), [Security Policy](../../SECURITY.md), [Accuracy Review](../../ACCURACY_REVIEW.md), and [References](../../REFERENCES.md).
