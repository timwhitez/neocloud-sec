# NeoCloud Cyber Security

[简体中文](README.zh-CN.md) | English

Vendor-neutral security baseline, reference architecture, roadmap and practice guides for specialized AI/GPU clouds.

**Base version:** `1.0.0-draft.1`  
**Public-findings profile:** `1.0.1`  
**Last scoped review:** 2026-09-29

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

## Inference and accelerator engineering depth

The existing validation runbooks now make five boundaries explicit: [CPU request budgets and listener coverage](docs/en/VALIDATION_RUNBOOKS.md#inference-resource-budgets), [disaggregated KV leases and reuse](docs/en/VALIDATION_RUNBOOKS.md#disaggregated-kv-lifecycle), [prefix/media/offload cache isolation](docs/en/VALIDATION_RUNBOOKS.md#layer-specific-cache-isolation), [GPU memory faults and recovery](docs/en/VALIDATION_RUNBOOKS.md#gpu-memory-disturbance), and [CPU–GPU–fabric confidential composition](docs/en/VALIDATION_RUNBOOKS.md#confidential-composition).

The same boundaries are stated in the white paper at [inference caches, request cost, KV reuse and confidential composition](docs/en/WHITEPAPER.md#inference-accelerator-boundaries). They are source-backed extensions of that operating model, with paired allow/deny tests, lifecycle, failure behavior and evidence requirements. The 2026-09-29 review is limited to these mechanisms; it is not a complete re-audit of older sources or a deployed-provider assessment. See the [versioned source scope](REFERENCES.md#inference-accelerator-sources). Core control IDs, tiers and conformance semantics are unchanged. Unexecuted GPU, RDMA, serving-runtime and TEE/KMS checks remain `NOT_TESTED`.

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

The runner executes all three repository validators and discovers the unit/negative tests. Missing dependencies or files cause failure, not a skipped green result. The test step records unittest's structured discovered, executed, skipped, failure and error counts. It does not treat a process exit code of 0 as proof that tests ran. No discovered test, or no required test body executed, fails the gate. Tests under `tests/` are required unless the test or its class sets `neocloud_optional = True`. An optional skip is reported and is not execution; a skipped required test fails the gate. The displayed count is the count from that run, not a fixed suite size. Each validator and the test step still runs in a subprocess with a 120-second limit; timeouts and failures to start fail the gate. This does not change `NOT_TESTED`, `VERIFIED` or T0. No infrastructure is probed. Offline environments should pre-stage packages through an approved process. While Actions quota is constrained, the workflow remains manual-dispatch only; do not dispatch or rerun it.

Generate an errata-applied catalog without modifying source files:

```bash
python3 scripts/compile_catalog.py > /tmp/neocloud-effective-catalog.json
```

The bundle includes `catalog` and SHA-256 provenance identifiers; it is not a deployment attestation. Optional offline [evidence and advisory checkers](docs/EVIDENCE_VALIDATION.md) validate metadata, not actual remediation. Historical `--as-of` examples are replay fixtures, not current assessments. Repository examples remain unverified; collect real assets and evidence in a separate private system.

## Governance and sources

[References](REFERENCES.md) · [Governance](GOVERNANCE.md) · [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md) · [Changelog](CHANGELOG.md) · [Repository settings guidance](.github/REPOSITORY_SETTINGS.md)

The settings guide does not itself change GitHub About, topics, visibility or permissions. No open-source license is currently granted. This iteration changes no visibility, license, branch protection or third-party affiliation claim.
