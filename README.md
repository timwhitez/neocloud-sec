# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

Vendor-neutral security baseline, reference architecture, roadmap and practice guides for specialized AI/GPU clouds.

**Base version:** `1.0.0-draft.1`  
**Public-findings profile:** `1.0.1`  
**Last scoped review:** 2026-09-05

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
| Review public findings and run authorized priority drills | [SemiAnalysis coverage](docs/en/SEMIANALYSIS_COVERAGE.md) | [覆盖审计与验证指南](docs/zh-CN/SEMIANALYSIS_COVERAGE.md) |
| Understand limits | [Scope](docs/en/SCOPE_AND_LIMITATIONS.md) | [范围与局限](docs/zh-CN/SCOPE_AND_LIMITATIONS.md) |

## What is included

The base catalog retains 90 stable control IDs: T0=32, T1=31, T2=19, T3=7, T4=1. Service profiles cover GPU IaaS, bare metal, managed Kubernetes, Slurm/HPC, model training, model serving, agents and sovereign/regulated deployments.

The independent SemiAnalysis/ClusterMAX overlay contains **40 atomic project-authored mappings** and **20/20 mappings of a dated public Security-page snapshot**. Mapping is not implementation, test execution, certification, endorsement or exact proprietary-framework parity. Its earlier prior-coverage summary was wrong; the actual stored classification is **21 explicit / 12 partial / 7 gaps**, now checked against the records. See the [scoped review](reviews/2026-09-05-validation-audit.md) for evidence and limitations.

Use [core controls](controls/neocloud-security-baseline.v1.json), [normative errata](controls/neocloud-security-baseline.v1.errata.json), the [public-findings profile](controls/semianalysis-public-findings-profile.v1.json) and [templates](templates/README.md) together. Do not import the raw core catalog while silently ignoring applicable errata.

## Operating rules

Every applicable T0 must be independently `VERIFIED`. Failed, unknown, stale, inconclusive or untested T0 remains `NO_GO_NONCONFORMANT`; a business-risk decision cannot change the result. Implementation is distinct from verification:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

Provider-exclusive control planes, host/GPU reset, fabric managers, BMC/OOB and signing/key roots remain provider responsibilities. Test compute, storage, fabric, observability and support paths separately. Agent output never grants authority. Recovery must re-establish identity, integrity and tenant isolation, not only availability.

## Local verification — no Actions required

Python 3.10+ is required for the strict checker. The first two legacy scripts use the standard library; strict schema validation explicitly requires the packages below. Dependency installation is a separate setup step, not hidden network activity inside validation.

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/check_local.py
```

The runner executes all three repository validators and the unit/negative tests locally. Missing dependencies or files cause failure, not a skipped green result. No infrastructure is probed. For an offline machine, pre-stage the required packages through your approved package process.

Generate a derived, errata-applied catalog bundle without modifying source files:

```bash
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

The bundle includes `catalog` and SHA-256 provenance identifiers. It is not a deployment attestation. Repository CSVs deliberately remain `UNKNOWN / PROPOSED / NOT_TESTED`; collect real assessments in a separate private system.

## Governance and sources

[References](REFERENCES.md) · [Governance](GOVERNANCE.md) · [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md) · [Changelog](CHANGELOG.md) · [Repository settings guidance](.github/REPOSITORY_SETTINGS.md)

The settings guide does not itself change GitHub About, topics, visibility or permissions. No open-source license is currently granted. This update does not change visibility, license, branch protections or third-party affiliation claims.
