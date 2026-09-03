# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

**Version:** `1.0.0-draft.1`  
**Baseline date:** 2026-09-04

NeoCloud Cyber Security is an open, evidence-driven security architecture and operating model for AI-first cloud infrastructure.

> **NeoCloud Cyber Security is a unified cybersecurity control plane for AI-native organizations and specialized AI clouds. It treats identity as the root of trust, policy as the decision core, and agents plus workloads as first-class security subjects. It coordinates endpoint, cloud-native runtime, network and fabric, data, software/model supply chain, and security operations controls to close the loop from visibility to real-time enforcement and continuous assurance.**

The project covers the full NeoCloud trust surface: people, tenants, AI agents, workload identities, APIs, control planes, Kubernetes and Slurm, bare-metal hosts, hypervisors, GPUs and accelerators, Ethernet and InfiniBand/RDMA fabrics, datasets, models, checkpoints, secrets, firmware, BMCs, facilities, and third-party dependencies.

## What this repository delivers

| Deliverable | English | 中文 |
|---|---|---|
| Full white paper | [White Paper](docs/en/WHITEPAPER.md) | [白皮书](docs/zh-CN/WHITEPAPER.md) |
| Security baseline | [Security Baseline](docs/en/SECURITY_BASELINE.md) | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) |
| Practice guide | [Practice Guide](docs/en/PRACTICE_GUIDE.md) | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) |
| Reference architecture | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| Development roadmap | [Roadmap](docs/en/ROADMAP.md) | [发展路线图](docs/zh-CN/ROADMAP.md) |
| Metrics and assurance | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| Machine-readable controls | [Control catalog](controls/neocloud-security-baseline.v1.json) | [控制目录说明](controls/README.md) |
| Assessment templates | [Templates](templates/) | [模板](templates/) |
| Normative references | [References](REFERENCES.md) | [参考资料](REFERENCES.md) |

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
- **T3 — Assured:** higher-assurance controls for sensitive, regulated, sovereign, or dedicated environments.
- **T4 — Adaptive:** continuous verification, high-confidence automation, confidential computing, and guarded AI-assisted defense.

A numeric score never compensates for a failed T0 control. Production readiness is gate-based and evidence-based.

## Core design principles

- **Identity before network location.** Human, service, workload, device, tenant, and agent identities are authenticated, scoped, short-lived, and continuously evaluated.
- **Isolation by construction.** Tenant boundaries extend across API, compute, storage, Ethernet, InfiniBand/RDMA, NVLink, schedulers, observability, and support operations.
- **Shared responsibility must be explicit.** Every control has a provider, customer, or shared owner and an escalation path.
- **Evidence is part of the control.** A control is not complete until its implementation, coverage, freshness, owner, exceptions, and independent verification are recorded.
- **Agents are privileged software subjects.** Agent actions are mediated by policy, least privilege, approval boundaries, immutable audit, and deterministic stop conditions.
- **Recovery is a security capability.** Backups, rebuilds, tenant offboarding, secure erasure, and crisis communications are tested rather than assumed.
- **Secure by design, not by tenant expertise.** Safe defaults, MFA, logging, isolation, and update mechanisms are provider responsibilities, not paid add-ons.

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

## Status and scope

This is an implementation-oriented community baseline, not a certification, legal opinion, or substitute for jurisdiction-specific obligations. Mappings to external frameworks are informative. Organizations remain responsible for determining applicability and obtaining qualified legal, privacy, safety, and audit advice.

See [GOVERNANCE.md](GOVERNANCE.md) for change control and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules.