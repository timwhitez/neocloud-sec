# Implementation templates / 实施模板

These templates turn the white paper into an operating system for security work. Copy them into a controlled system of record or GRC platform; do not store live secrets or sensitive customer evidence in a public repository.

| Template | Purpose |
|---|---|
| `baseline-assessment.csv` | Control-by-control implementation and verification tracker |
| `risk-register.csv` | Cyber, AI, tenant, and infrastructure risk register |
| `exception-register.csv` | Time-bounded control exceptions and compensating controls |
| `shared-responsibility-matrix.csv` | Provider/customer/shared ownership |
| `evidence-register.csv` | Evidence provenance, freshness, integrity, and verifier status |
| `security-service-catalog.csv` | Security capability owners, consumers, SLOs, and dependencies |
| `threat-model.md` | Service threat-model and trust-boundary template |
| `incident-severity-matrix.md` | NeoCloud-specific severity classification and response targets |

Recommended control states are `PROPOSED`, `READY`, `IMPLEMENTED`, `CANDIDATE_DONE`, and `VERIFIED`. Verification results are `PASS`, `FAIL`, `INCONCLUSIVE`, and `NOT_TESTED`; `NOT_REVIEWED` is not a valid result. Only an independent validator returning `PASS` may assign `VERIFIED`. A failed, unknown, stale, inconclusive, or untested applicable T0 remains `NO_GO_NONCONFORMANT`, regardless of a business-risk decision.

In the shared-responsibility template, split adjacent provider and customer duties rather than labelling an entire capability `shared`. Provider-exclusive roots—including provider control planes, managed scheduler/control-plane internals, host/GPU reset, fabric managers, P_Key/RDMA/DPU enforcement, BMC/OOB, and provider signing/key roots—remain provider-owned.
