# Implementation templates / 实施模板

Copy templates into a private system of record before collecting real assessments. Do not commit credentials, customer data or production evidence to this repository.

请先将模板复制到私有台账，再收集真实评估。不要向本仓库提交凭据、客户数据或生产证据。

| Template | Purpose |
|---|---|
| [Baseline assessment](baseline-assessment.csv) | Core control implementation tracker |
| [Public-findings assessment](semianalysis-public-findings-assessment.csv) | 40 project-authored mappings, with three assurance views |
| [Public Security-page assessment](clustermax-public-security-requirements-assessment.csv) | 20 dated public-page mappings, not a rating |
| [Evidence register](evidence-register.csv) | Provenance, scope, validity and reviewer |
| [Shared responsibility](shared-responsibility-matrix.csv) | Explicit provider/customer duties |
| [Risk register](risk-register.csv) | Residual risks and owners |
| [Exception register](exception-register.csv) | Time-bounded decisions, never a fabricated PASS |
| [Service catalog](security-service-catalog.csv) | Capability owners and dependencies |
| [Threat model](threat-model.md) | Trust boundaries and test scope |
| [Incident severity](incident-severity-matrix.md) | Incident classification and response objectives |

Control states: `PROPOSED`, `READY`, `IMPLEMENTED`, `CANDIDATE_DONE`, `VERIFIED`.
Verification results: `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_TESTED`.
`NOT_REVIEWED` is not a valid result. Only a qualified independent PASS can support VERIFIED. An applicable failed, stale or untested T0 remains `NO_GO_NONCONFORMANT`.

Provider-exclusive roots remain provider-owned: provider control planes, host/GPU reset, fabric management, BMC/OOB and provider signing/key roots. Customer configuration responsibilities do not transfer these responsibilities.

A mapped row is not proof of effectiveness. Preserve the three fields `tenant_blackbox_result`, `provider_whitebox_result`, and `independent_failure_recovery_result` independently. The live assessment system must track scope, applicability rationale, evidence validity, reviewer independence and failure handling; the repository linter does not implement that system.

The two public-findings templates deliberately use `UNKNOWN / PROPOSED / NOT_TESTED` and contain no real verification evidence. The strict repository checker rejects changed mappings, altered severity/title, malformed CSV rows and fabricated template PASS states. Generate operational results only in your private copy.

See the [English validation guide](../docs/en/SEMIANALYSIS_COVERAGE.md) / [中文验证指南](../docs/zh-CN/SEMIANALYSIS_COVERAGE.md).
