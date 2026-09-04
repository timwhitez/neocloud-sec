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

Recommended states are `PROPOSED`, `READY`, `IMPLEMENTED`, `CANDIDATE_DONE`, and `VERIFIED`. Only independent validation should assign `VERIFIED`.
