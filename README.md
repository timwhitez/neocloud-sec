# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

Vendor-neutral security baseline, reference architecture, roadmap and practice guides for specialized AI/GPU clouds.

**Base version:** `1.0.0-draft.1`  
**Public-findings profile:** `1.0.1`  
**Last scoped review:** 2026-09-09

This is a documentation and validation project, not a deployable security control plane, certification or proof that a provider is secure. “NeoCloud” is a working industry term; define the actual service and trust boundaries rather than inferring them from a label.

## Start here

| Goal | English | 简体中文 |
|---|---|---|
| Understand risks and the operating model | [White paper](docs/en/WHITEPAPER.md) | [白皮书](docs/zh-CN/WHITEPAPER.md) |
| Assess the 18-domain / 90-control baseline | [Baseline](docs/en/SECURITY_BASELINE.md) | [安全基线](docs/zh-CN/SECURITY_BASELINE.md) |
| Implement and operate controls | [Practice guide](docs/en/PRACTICE_GUIDE.md) | [实践指南](docs/zh-CN/PRACTICE_GUIDE.md) |
| Design identity, tenant and enforcement boundaries | [Architecture](docs/en/REFERENCE_ARCHITECTURE.md) | [参考架构](docs/zh-CN/REFERENCE_ARCHITECTURE.md) |
| Plan phased delivery | [Roadmap](docs/en/ROADMAP.md) | [路线图](docs/zh-CN/ROADMAP.md) |
| Define evidence, metrics and verification | [Assurance](docs/en/METRICS_AND_ASSURANCE.md) | [度量与持续证明](docs/zh-CN/METRICS_AND_ASSURANCE.md) |
| Review public findings and authorized priority drills | [SemiAnalysis coverage](docs/en/SEMIANALYSIS_COVERAGE.md) | [覆盖审计与验证指南](docs/zh-CN/SEMIANALYSIS_COVERAGE.md) |
| Validate runtime, revocation, storage and telemetry boundaries | [Validation runbooks](docs/en/VALIDATION_RUNBOOKS.md) | [验证手册](docs/zh-CN/VALIDATION_RUNBOOKS.md) |
| Check evidence and advisory-record consistency | [Evidence validation](docs/EVIDENCE_VALIDATION.md) | [证据与公告记录校验](docs/EVIDENCE_VALIDATION.md) |
| Understand limits | [Scope](docs/en/SCOPE_AND_LIMITATIONS.md) | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) |

Research improves these documents and tools in place. The [contribution process](CONTRIBUTING.md#recurring-research) defines source review, gap assessment and PR-before-merge; [CHANGELOG.md](CHANGELOG.md) records normal project changes. Dated decisions and test evidence belong in the relevant PR/Issue, not a parallel weekly-document series. No background job or scheduler is installed.

## What is included

The base catalog retains 90 stable control IDs: T0=32, T1=31, T2=19, T3=7, T4=1. Service profiles cover GPU IaaS, bare metal, managed Kubernetes, Slurm/HPC, model training, model serving, agents and sovereign/regulated deployments.

The independent SemiAnalysis/ClusterMAX overlay contains **40 atomic project-authored mappings** and **20/20 mappings of a dated public Security-page snapshot**. Mapping is not implementation, test execution, certification, endorsement or exact proprietary-framework parity. Its stored prior-coverage classification is **21 explicit / 12 partial / 7 gaps**, not the earlier incorrect summary; see the [scoped audit](reviews/2026-09-05-validation-audit.md).

Use [core controls](controls/neocloud-security-baseline.v1.json), [normative errata](controls/neocloud-security-baseline.v1.errata.json), the [public-findings profile](controls/semianalysis-public-findings-profile.v1.json) and [templates](templates/README.md) together. Do not import the raw catalog while silently ignoring applicable errata.

## Operating rules

Every applicable T0 must be independently `VERIFIED`. Failed, unknown, stale, inconclusive or untested T0 remains `NO_GO_NONCONFORMANT`; a business-risk decision cannot change the result. Implementation is distinct from verification:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

Provider-exclusive control planes, host/GPU reset, fabric managers, BMC/OOB and signing/key roots remain provider responsibilities. Test compute, storage, fabric, observability and support paths separately. Agent output never grants authority. Recovery must re-establish identity, integrity and tenant isolation, not only availability.

## Local verification — no Actions required

Use a full checkout and Python 3.10+. The first two legacy repository validators use the standard library; strict schema validation requires the declared packages. Installation is a separate setup step, not hidden network activity inside validation.

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/check_local.py
```

The runner executes all three repository validators and discovers the unit/negative tests. Missing dependencies or files cause failure, not a skipped green result. No infrastructure is probed. Offline environments should pre-stage packages through an approved process. While Actions quota is constrained, the workflow remains manual-dispatch only; do not dispatch or rerun it.

Generate an errata-applied catalog without modifying source files:

```bash
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

The bundle includes `catalog` and SHA-256 provenance identifiers; it is not a deployment attestation. Optional offline [evidence and advisory checkers](docs/EVIDENCE_VALIDATION.md) validate metadata, not actual remediation. Historical `--as-of` examples are replay fixtures, not current assessments. Repository examples remain unverified; collect real assets and evidence in a separate private system.

## Governance and sources

[References](REFERENCES.md) · [Governance](GOVERNANCE.md) · [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md) · [Changelog](CHANGELOG.md) · [Repository settings guidance](.github/REPOSITORY_SETTINGS.md)

The settings guide does not itself change GitHub About, topics, visibility or permissions. No open-source license is currently granted. This iteration changes no visibility, license, branch protection or third-party affiliation claim.
