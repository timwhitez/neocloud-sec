# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

A vendor-neutral security baseline, reference architecture, roadmap, and implementation guide for specialized AI and GPU clouds.

**Version:** `1.0.0-draft.1`  
**Baseline date:** 2026-09-04  
**Latest public-findings review:** 2026-09-05  
**Status:** implementation-oriented project draft

> NeoCloud Cyber Security is a reference framework for designing and operating security controls across AI infrastructure. It treats identity and delegated authority as trust roots, policy as the decision mechanism, and people, tenants, workloads, devices, models, and agents as explicit security subjects. It connects preventive controls, telemetry, response, recovery, evidence, and independent verification across the service boundary.

This repository contains documentation, machine-readable control catalogs and profiles, local validation logic, and implementation templates. **It is not a deployable security product, an adopted industry standard, a certification scheme, a ClusterMAX rating, or proof that any provider is secure.**

“NeoCloud” is used here as a working industry term for specialized cloud providers serving accelerator-intensive AI and HPC workloads. The project does not assume one formal or regulatory definition.

## Start here

| Goal | Entry point |
|---|---|
| Understand the security problem and operating model | [White Paper](docs/en/WHITEPAPER.md) |
| Assess minimum security outcomes | [Security Baseline](docs/en/SECURITY_BASELINE.md) and [baseline template](templates/baseline-assessment.csv) |
| Turn requirements into engineering and operations | [Practice Guide](docs/en/PRACTICE_GUIDE.md) |
| Design trust zones, policy, evidence and recovery boundaries | [Reference Architecture](docs/en/REFERENCE_ARCHITECTURE.md) |
| Plan a 0–24-month program | [Roadmap](docs/en/ROADMAP.md) |
| Define gates, metrics and independent assurance | [Metrics & Assurance](docs/en/METRICS_AND_ASSURANCE.md) |
| Review SemiAnalysis / ClusterMAX public security findings | [Coverage audit](docs/en/SEMIANALYSIS_COVERAGE.md), [40-pattern assessment](templates/semianalysis-public-findings-assessment.csv), and [20-item public Security-page assessment](templates/clustermax-public-security-requirements-assessment.csv) |
| Integrate controls with tooling | [Core catalog](controls/neocloud-security-baseline.v1.json), [public-findings profile](controls/semianalysis-public-findings-profile.v1.json), [normative errata](controls/neocloud-security-baseline.v1.errata.json), and schemas |

A practical first pass:

1. Define the exact service, region, cluster, SKU, hardware and deployed version boundary.
2. Assign provider, customer and shared responsibility without transferring provider-exclusive roots to the customer.
3. Evaluate every applicable T0/T1 with current, scoped evidence.
4. Run customer black-box, provider white-box and independent failure/recovery tests for material isolation claims.
5. Treat every failed, unknown, stale, `INCONCLUSIVE` or `NOT_TESTED` applicable T0 as `NO_GO_NONCONFORMANT`.
6. Productize T2, add T3 where commitments require it, and adopt T4 only after approval, stop, rollback, trace and verifier behavior are proven.

## Deliverables

| Deliverable | English | 中文 |
|---|---|---|
| White paper | [English](docs/en/WHITEPAPER.md) | [中文](docs/zh-CN/WHITEPAPER.md) |
| Security baseline | [English](docs/en/SECURITY_BASELINE.md) | [中文](docs/zh-CN/SECURITY_BASELINE.md) |
| Practice guide | [English](docs/en/PRACTICE_GUIDE.md) | [中文](docs/zh-CN/PRACTICE_GUIDE.md) |
| Reference architecture | [English](docs/en/REFERENCE_ARCHITECTURE.md) | [中文](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| Roadmap | [English](docs/en/ROADMAP.md) | [中文](docs/zh-CN/ROADMAP.md) |
| Metrics and assurance | [English](docs/en/METRICS_AND_ASSURANCE.md) | [中文](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| SemiAnalysis public-findings coverage | [English](docs/en/SEMIANALYSIS_COVERAGE.md) | [中文](docs/zh-CN/SEMIANALYSIS_COVERAGE.md) |
| Machine-readable controls | [Core catalog](controls/neocloud-security-baseline.v1.json) and [normative errata](controls/neocloud-security-baseline.v1.errata.json) | [Catalog guide](controls/README.md) |
| Interoperability overlay | [Public-findings profile](controls/semianalysis-public-findings-profile.v1.json) | [Landing page](SEMIANALYSIS_COVERAGE.md) |
| Templates | [Templates](templates/) | [模板](templates/) |
| Sources and limitations | [References](REFERENCES.md) and [scope](docs/en/SCOPE_AND_LIMITATIONS.md) | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) |

## Security model

The stable core contains **90 controls across 18 domains** and five adoption tiers:

- **T0 — Guardrails:** hard production gates; every applicable T0 must be independently `VERIFIED`.
- **T1 — Foundation:** ownership, inventory, hygiene, visibility, response and recovery foundations.
- **T2 — Production:** reusable, policy-enforced and measured controls for sustainable multi-tenant operation.
- **T3 — Assured:** higher assurance for sensitive, regulated, sovereign, dedicated, attested or confidential-computing profiles.
- **T4 — Adaptive:** guarded adaptive automation and continuous verification after authority and failure modes are proven.

The control state is:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

Only an independent validator returning `PASS` for the exact service, environment, version, scope and evidence-validity period may assign `VERIFIED`.

## SemiAnalysis / ClusterMAX public coverage

The independent interoperability profile maps:

- **five public article-level patterns decomposed by this project into 40 atomic test patterns**;
- **20/20 currently enumerable requirements on the canonical public ClusterMAX Security page**;
- explicit checks for InfiniBand management and service keys, SR-IOV QP0/MAD restrictions, BlueField/RShim, vCluster/shared nodes, kubelet, Prometheus/Grafana tenant isolation, provider-wide root keys, dynamic minimum-safe versions, vulnerability disclosure, hostile renderers/caches, inference-response supply-chain risk, and three-view assurance.

An alternate ClusterMAX host reported 21 Security criteria at the review cut-off, but the extra item could not be independently enumerated. The project therefore does **not** claim 21/21, exact ClusterMAX parity, a score, certification or endorsement. ClusterMAX also includes non-security rating dimensions that this cybersecurity project intentionally does not reproduce.

The [v1 normative errata](controls/neocloud-security-baseline.v1.errata.json) refines `NCS-CMP-02`: full-device dedication, hardware partitioning, hypervisor-mediated vGPU and scheduler-level bare-device-plugin time-slicing are different mechanisms. Kubernetes GPU Operator time-slicing has no memory/fault isolation between replicas; mediated-vGPU claims are product/version/configuration specific and must be tested.

## Core principles

- **Identity before location.** Keep credentials, sessions, privilege grants and delegated authority short-lived where feasible.
- **Isolation requires path-by-path evidence.** Test API, compute, accelerator memory/faults, storage, Ethernet, RDMA/InfiniBand, DPU, scheduler, telemetry, support and OOB paths independently.
- **Sharing modes are not equivalent.** Full-device dedication, hardware partitioning, mediated vGPU and scheduler-level time-slicing are different products.
- **Provider-exclusive roots remain provider-owned.** Control planes, host/GPU reset, fabric managers, BMC/OOB and provider signing/key roots cannot be transferred through documentation.
- **Evidence is part of the control.** Deployment is not effectiveness; prohibited paths, failure behavior, recovery and independent reproduction matter.
- **Model output is not authority.** External content and inference responses are untrusted proposals; typed tools and local policy govern actions.
- **Recovery restores trust, not only availability.** Reopening verifies identity, artifacts, tenant isolation, data integrity and monitoring.

## Local validation

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_accuracy_invariants.py
python3 scripts/validate_semianalysis_profile.py
```

The validators check the stable 18-domain/90-control contract, bilingual parity, cross-references, versions, links, template semantics, the 10-dimension/40-pattern public-findings profile, the 20-item canonical public Security-page mapping and the active normative errata.

## Governance and license

- [Contribution rules](CONTRIBUTING.md)
- [Control and evidence governance](GOVERNANCE.md)
- [Security reporting](SECURITY.md)
- [Accuracy review](ACCURACY_REVIEW.md)
- [Recommended GitHub settings](.github/REPOSITORY_SETTINGS.md)
- [Change history](CHANGELOG.md)

No open-source license is currently granted. Before public release or external reuse, the owner should select and add an explicit license.
