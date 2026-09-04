# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

**Version:** `1.0.0-draft.2`  
**Baseline date:** 2026-09-04

NeoCloud Cyber Security is a vendor-neutral, bilingual, evidence-oriented reference baseline and implementation guide for AI-first cloud infrastructure.

> **This repository defines a security reference model, control catalog, assurance method, and implementation roadmap. It is not a deployed security product or a claim that one universal “control plane” can secure every NeoCloud. The model coordinates identity and authorization, platform and workload integrity, cryptographic roots, policy enforcement, tenant isolation, and independently protected evidence across the service lifecycle.**

The project covers the full NeoCloud trust surface: people, tenants, AI agents, workload identities, APIs, control planes, Kubernetes and Slurm, bare-metal hosts, hypervisors, GPUs and accelerators, Ethernet and InfiniBand/RDMA fabrics, datasets, models, checkpoints, secrets, firmware, BMCs, facilities, and third-party dependencies.

“NeoCloud” is used here as an operational term for specialized AI/GPU cloud services, not as a formally standardized industry category. See [Scope and Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) before adopting or citing the baseline.

## What this repository delivers

| Deliverable | English | 中文 |
|---|---|---|
| Full white paper | [White Paper](docs/en/WHITEPAPER.md) | [白皮书](docs/zh-CN/WHITEPAPER.md) |
| Security baseline | [Security Baseline](docs/en/SECURITY_BASELINE.md) | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) |
| Practice guide | [Practice Guide](docs/en/PRACTICE_GUIDE.md) | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) |
| Reference architecture | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| Development roadmap | [Roadmap](docs/en/ROADMAP.md) | [发展路线图](docs/zh-CN/ROADMAP.md) |
| Metrics and assurance | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| Machine-readable controls | [Control catalog](controls/neocloud-security-baseline.v1.json) and [schema](controls/schema.json) | [控制目录说明](controls/README.md) |
| Assessment templates | [Templates](templates/) | [模板](templates/) |
| Standards and research | [References](REFERENCES.md) | [参考资料](REFERENCES.md) |
| Scope and limitations | [Scope & Limitations](docs/en/SCOPE_AND_LIMITATIONS.md) | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) |
| Accuracy review | [Accuracy Review](ACCURACY_REVIEW.md) | [准确性审计](ACCURACY_REVIEW.md) |
| Repository metadata | [Project Metadata](PROJECT_METADATA.md) | [项目元数据](PROJECT_METADATA.md) |
| Security reporting | [Security Policy](SECURITY.md) | [安全报告](SECURITY.md) |

## Security model

The baseline is organized into 18 NeoCloud Security domains:

1. Governance, risk, compliance, and shared responsibility
2. Asset, service, dependency, and data-flow inventory
3. Human, tenant, workload, and agent identity
4. Control-plane, API, and administrative-interface security
5. Network, fabric, RDMA/InfiniBand, and DPU isolation
6. Compute, hypervisor, bare-metal, GPU, and accelerator isolation
7. Kubernetes, containers, Slurm, and scheduler security
8. Data, dataset, model, artifact, and privacy protection
9. Secrets, keys, PKI, attestation, and confidential computing
10. Software, model, and infrastructure supply-chain security
11. Secure engineering, infrastructure as code, change, and configuration
12. Vulnerability, exposure, patch, and firmware management
13. Telemetry, detection engineering, threat intelligence, and audit
14. AI application, agent, tool, skill, and prompt security
15. Abuse prevention, tenant trust, egress, and acceptable use
16. Incident response, forensics, crisis management, and recovery
17. Resilience, availability, capacity, backup, and disaster recovery
18. Physical, facility, BMC, hardware lifecycle, and media sanitization

Controls are prioritized through five adoption tiers:

- **T0 — Guardrails:** non-negotiable conditions before a service processes tenant data or exposes production capacity.
- **T1 — Foundation:** essential cyber hygiene and complete visibility, normally targeted in the first 90 days.
- **T2 — Production:** scalable, policy-enforced controls for a generally available multi-tenant service.
- **T3 — Assured:** higher-assurance controls for sensitive, regulated, sovereign, or dedicated environments, including independently tested and threat-model-justified attestation or confidential-computing patterns.
- **T4 — Adaptive:** continuous verification and guarded AI-assisted security automation whose authority, rollback, and independent verification are proven.

A numeric score never compensates for a failed T0 control. Production readiness is gate-based and evidence-based.

## Core design principles

- **Identity before network location.** Human, service, workload, device, tenant, and agent identities are authenticated, scoped, short-lived, and continuously evaluated.
- **Isolation by construction.** Tenant boundaries extend across API, compute, storage, Ethernet, InfiniBand/RDMA, NVLink, schedulers, observability, and support operations.
- **Shared responsibility must be explicit.** Every control has a provider, customer, or shared owner and an escalation path.
- **Evidence is part of the control.** A control is not complete until its implementation, coverage, freshness, owner, exceptions, and independent verification are recorded.
- **Agents are privileged software subjects.** Agent actions are mediated by policy, least privilege, approval boundaries, immutable audit, and deterministic stop conditions.
- **Recovery is a security capability.** Backups, rebuilds, tenant offboarding, secure erasure, and crisis communications are tested rather than assumed.
- **Secure by design and accurately scoped.** Provider-controlled baseline safeguards should be secure by default; customer-controlled duties and higher-assurance offerings must be explicit and must not conceal the limitations of baseline service tiers.

## Intended users

This repository is designed for NeoCloud and GPU-cloud providers, AI infrastructure teams, sovereign AI operators, platform engineering teams, security architects, CISOs, auditors, enterprise buyers, and customers performing provider due diligence.

It supports GPU IaaS, bare-metal GPU services, managed Kubernetes, managed Slurm/HPC, model-training platforms, inference and model-serving platforms, agent platforms, and regulated or sovereign deployments.

## Adoption path

1. Select the applicable service profile and establish the shared-responsibility matrix.
2. Inventory assets, identities, data flows, trust boundaries, and critical dependencies.
3. Assess T0 and T1 controls with evidence; remediate all failed production gates.
4. Implement T2 controls as reusable platform capabilities and policy-as-code.
5. Add T3 assurance for high-risk services and customer commitments.
6. Introduce T4 automation only after actions are bounded, reversible, observable, and independently verified.

## Repository validation

Run the standard-library validator from the repository root:

```bash
python3 scripts/validate_repository.py
```

It verifies the repository contract, including:

- exactly 18 domains and 90 controls;
- the expected `T0=32`, `T1=31`, `T2=19`, `T3=7`, `T4=1` distribution;
- valid, unique, and complete control IDs;
- bilingual titles and normative requirements;
- evidence, verification, tier, and metric cross-references;
- parity between the JSON catalog and both security-baseline documents;
- consistent release versions and required deliverables;
- valid relative Markdown links.

The same check runs in GitHub Actions for pull requests and `main`. See the [control-catalog documentation](controls/README.md) for queries and change rules.

## Accuracy and scope

The baseline distinguishes scheduler-level GPU oversubscription from mediated vGPU and hardware-partitioned modes; treats InfiniBand P_Keys and Slurm labels as partial mechanisms rather than complete isolation proofs; and makes attestation, confidential computing, sanitization, and public control-plane claims product-, version-, configuration-, and threat-model specific.

See the [accuracy review](ACCURACY_REVIEW.md), [scope and limitations](docs/en/SCOPE_AND_LIMITATIONS.md), and [source register](REFERENCES.md). Project-defined targets are planning defaults, not externally validated industry benchmarks.

## Status and scope

This is a project-defined implementation draft and reference baseline—not an adopted industry standard, deployed product, certification, legal opinion, or substitute for jurisdiction-specific obligations. External-framework mappings are informative. Organizations remain responsible for applicability decisions and qualified legal, privacy, safety, engineering, and audit review.

See [GOVERNANCE.md](GOVERNANCE.md) for change control and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules.
