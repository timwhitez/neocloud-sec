# Implementation templates / 实施模板

These templates turn the white paper and security profiles into an operating system for security work. Copy them into a controlled system of record or GRC platform; do not store live secrets or sensitive customer evidence in a public repository.

这些模板用于把白皮书和安全画像转化为可运营工作。请复制到受控的 System of Record 或 GRC 平台中；不要在公开仓库保存真实 Secret、客户数据或敏感证据。

| Template | Purpose |
|---|---|
| `baseline-assessment.csv` | Control-by-control implementation and verification tracker |
| `semianalysis-public-findings-assessment.csv` | Service/region/SKU/version-scoped assessment of 40 project-authored atomic test patterns derived from five high-level public article patterns |
| `clustermax-public-security-requirements-assessment.csv` | Assessment of the 20 currently enumerable requirements on the canonical public ClusterMAX Security page; not a score or exact-parity claim |
| `risk-register.csv` | Cyber, AI, tenant, and infrastructure risk register |
| `exception-register.csv` | Time-bounded control exceptions and compensating controls |
| `shared-responsibility-matrix.csv` | Provider/customer/shared ownership |
| `evidence-register.csv` | Evidence provenance, freshness, integrity, and verifier status |
| `security-service-catalog.csv` | Security capability owners, consumers, SLOs, and dependencies |
| `threat-model.md` | Service threat-model and trust-boundary template |
| `incident-severity-matrix.md` | NeoCloud-specific severity classification and response targets |

Recommended control states are `PROPOSED`, `READY`, `IMPLEMENTED`, `CANDIDATE_DONE`, and `VERIFIED`. Verification results are `PASS`, `FAIL`, `INCONCLUSIVE`, and `NOT_TESTED`. Only an independent validator returning `PASS` should assign `VERIFIED`.

For the 40 project-authored atomic patterns, fill all three result views independently:

- `tenant_blackbox_result`
- `provider_whitebox_result`
- `independent_failure_recovery_result`

A mapped row is not proof of effectiveness. Scope every row to a concrete service, profile, region, cluster, SKU, hardware and deployed software/firmware/orchestrator version. A failed, unknown, stale, inconclusive or untested applicable T0 remains `NO_GO_NONCONFORMANT`.

For the canonical public Security-page template, assess all 20 rows against the exact service and deployed environment. An alternate ClusterMAX host reported 21 Security criteria at the review cut-off; because its extra item could not be independently enumerated, do not present the template as 21/21 coverage or as a ClusterMAX rating.
