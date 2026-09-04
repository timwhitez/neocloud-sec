# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

A vendor-neutral security baseline, reference architecture, roadmap, and implementation guide for specialized AI and GPU clouds.

**Version:** `1.0.0-draft.1`  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented draft

> NeoCloud Cyber Security is a **reference framework for designing and operating** a coherent security control plane across AI infrastructure. It treats identity and delegated authority as trust roots, policy as the decision mechanism, and people, tenants, workloads, devices, models, and agents as explicit security subjects. It connects preventive controls, telemetry, response, recovery, evidence, and independent verification across the full service boundary.

This repository contains documentation, a machine-readable control catalog, validation logic, and implementation templates. **It is not a deployable security product, a certification scheme, or evidence that any provider is secure.**

“NeoCloud” is used here as a working industry term for specialized cloud providers serving accelerator-intensive AI and HPC workloads. The project does not assume that the term has a single formal, regulatory, or universally accepted definition.

## Start here

| Goal | Recommended entry point |
|---|---|
| Understand the security problem and operating model | [White Paper](docs/en/WHITEPAPER.md) |
| Assess a service against minimum outcomes | [Security Baseline](docs/en/SECURITY_BASELINE.md) and [assessment template](templates/baseline-assessment.csv) |
| Turn requirements into engineering and operations work | [Practice Guide](docs/en/PRACTICE_GUIDE.md) |
| Design trust zones, policy points, evidence flows, and recovery boundaries | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) |
| Plan a 0–24-month program | [Roadmap](docs/en/ROADMAP.md) |
| Define gates, evidence, metrics, and independent assurance | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) |
| Integrate controls with tooling | [Machine-readable catalog](controls/neocloud-security-baseline.v1.json) and [schema](controls/schema.json) |

A practical first pass is:

1. Select one or more service profiles and define the exact production boundary.
2. Assign provider, customer, and shared responsibility.
3. Evaluate every applicable T0 and T1 control using current, scoped evidence.
4. Block or remove exposure for every failed, unknown, stale, inconclusive, or untested applicable T0.
5. Productize T2 controls, add T3 assurance where commitments require it, and introduce T4 adaptive automation only after authority and failure modes are proven.

## What this repository delivers

| Deliverable | English | 中文 |
|---|---|---|
| Full white paper | [White Paper](docs/en/WHITEPAPER.md) | [白皮书](docs/zh-CN/WHITEPAPER.md) |
| Security baseline | [Security Baseline](docs/en/SECURITY_BASELINE.md) | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) |
| Practice guide | [Practice Guide](docs/en/PRACTICE_GUIDE.md) | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) |
| Reference architecture | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| Development roadmap | [Roadmap](docs/en/ROADMAP.md) | [发展路线图](docs/zh-CN/ROADMAP.md) |
| Metrics and assurance | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| Machine-readable controls | [Control catalog](controls/neocloud-security-baseline.v1.json), [schema](controls/schema.json), and [catalog guide](controls/README.md) | [控制目录说明](controls/README.md) |
| Assessment templates | [Templates](templates/) | [模板](templates/) |
| Standards and research basis | [References](REFERENCES.md) | [参考资料](REFERENCES.md) |

## Scope

The project covers provider-operated and customer-facing trust boundaries involving:

- GPU IaaS and bare-metal GPU services;
- managed Kubernetes and managed Slurm/HPC;
- model training, model serving, and agent platforms;
- sovereign or regulated service profiles;
- human, tenant, workload, device, service, and agent identity;
- APIs, control planes, schedulers, hosts, accelerators, storage, Ethernet, InfiniBand/RDMA, NVLink-aware placement, DPUs, BMC/OOB, facilities, and suppliers;
- datasets, prompts, outputs, models, checkpoints, embeddings, caches, keys, software, firmware, and security evidence.

The baseline does not replace service-specific threat modeling, deployed-path testing, contractual responsibility, applicable law, privacy or safety assessment, or qualified independent audit.

## Security model

The baseline contains **90 controls across 18 domains**:

| Governance and visibility | Platform and workload protection | Operations and assurance |
|---|---|---|
| Governance, risk, compliance, and shared responsibility | Network, fabric, RDMA/InfiniBand, and DPU isolation | Secure engineering, IaC, change, and configuration |
| Asset, service, dependency, and data-flow inventory | Compute, hypervisor, bare-metal, GPU, and accelerator isolation | Vulnerability, exposure, patch, and firmware management |
| Human, tenant, workload, and agent identity | Kubernetes, containers, Slurm, and scheduler security | Telemetry, detection engineering, threat intelligence, and audit |
| Control-plane, API, and administrative-interface security | Data, dataset, model, artifact, and privacy protection | Abuse prevention, tenant trust, egress, and acceptable use |
| Secrets, keys, PKI, attestation, and confidential computing | Software, model, and infrastructure supply-chain security | Incident response, resilience, recovery, physical and hardware lifecycle |
| AI application, agent, tool, skill, and prompt security |  |  |

Controls are prioritized through five adoption tiers:

- **T0 — Guardrails:** hard production gates. Every applicable T0 must be independently `VERIFIED`; no exception or aggregate score can make an unmet T0 conformant.
- **T1 — Foundation:** ownership, inventory, hygiene, visibility, response, and recovery foundations.
- **T2 — Production:** reusable, policy-enforced, measured controls for sustainable multi-tenant operation.
- **T3 — Assured:** independently supported, higher-assurance controls for sensitive, regulated, sovereign, dedicated, attested, or confidential-computing profiles where justified.
- **T4 — Adaptive:** guarded adaptive automation and continuous verification after authority, approval, stop, rollback, trace, and verifier controls have been proven.

An executive may authorize a time-bounded emergency business decision, but that decision does **not** convert a failed T0 into `VERIFIED` or permit the service to be represented as conformant.

## Core design principles

- **Identity before network location.** Subjects have strong, scoped, reviewable identities; credentials, sessions, and delegated authority are short-lived where technically feasible.
- **Isolation by construction.** Tenant boundaries extend across API, compute, accelerator memory and faults, storage, Ethernet, InfiniBand/RDMA, NVLink topology, schedulers, telemetry, and support operations.
- **Sharing modes are not equivalent.** Full-device dedication, hardware partitioning, virtualization, and time-slicing must be described and tested separately. Time-slicing is not a memory- or fault-isolation boundary.
- **Shared responsibility is explicit.** Every control has a provider, customer, or shared owner and an escalation path.
- **Evidence is part of the control.** Deployment alone is not effectiveness; current scope, negative tests, failure behavior, recovery, and independent verification matter.
- **Agent authority is risk based.** Every production agent is inventoried and bounded; high-impact or adaptive workflows additionally require deterministic approval/stop conditions, protected traces, and independent verification.
- **Recovery restores trust, not only availability.** Reopening requires identity, artifact, tenant-isolation, data-integrity, and monitoring checks.
- **Secure defaults are provider responsibilities.** Capabilities exclusively controlled by the provider cannot be transferred to the customer through documentation.

## Control state and evidence

The only normal completion path is:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

Only an independent validator returning `PASS` for the stated service, version, region, tenant/asset scope, test, and evidence validity period may assign `VERIFIED`.

## Repository validation

Run the dependency-free validator from the repository root:

```bash
python3 scripts/validate_repository.py
```

It verifies:

- exactly 18 domains and 90 controls;
- the expected `T0=32`, `T1=31`, `T2=19`, `T3=7`, `T4=1` distribution;
- valid, unique, and complete control IDs;
- bilingual titles and normative requirements;
- evidence, verification, tier, and metric cross-references;
- parity between the JSON catalog and both security-baseline documents;
- consistent release versions and required deliverables;
- valid relative Markdown links.

The same check runs for pull requests and `main` through [GitHub Actions](.github/workflows/validate.yml).

## Project governance and status

- Contribution rules: [CONTRIBUTING.md](CONTRIBUTING.md)
- Control and evidence governance: [GOVERNANCE.md](GOVERNANCE.md)
- Security reporting: [SECURITY.md](SECURITY.md)
- Recommended GitHub About text, topics, and repository settings: [.github/REPOSITORY_SETTINGS.md](.github/REPOSITORY_SETTINGS.md)
- Change history: [CHANGELOG.md](CHANGELOG.md)

No open-source license is currently granted by this repository. Before public release or external reuse, the owner should select and add an explicit license; the recommended decision options are recorded in the repository-settings guide.
