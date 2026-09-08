# Weekly security review and advisory disposition

[简体中文](../zh-CN/WEEKLY_SECURITY_REVIEW.md) · [2026-09-08 research](../../reviews/2026-09-08-weekly-security-review.md)

This is an operational supplement, not a new control catalog, vulnerability scanner, scheduler or attestation system. Use the existing [runbooks](VALIDATION_RUNBOOKS.md), [governance](../../GOVERNANCE.md) and [evidence checker](../EVIDENCE_VALIDATION.md). No background job is installed by these documents.

## 1. Repeatable weekly decision

Record the exact base commit, timezone, calendar-week boundaries and evidence cutoff. Separate this week's publications from a rolling lookback, older carryovers and future deadlines. For each important claim record the primary URL, publication/revision date, access date, affected product/configuration and retrieval limitations. Record conflicting timestamps instead of guessing which is correct. Cross-check an advisory with its product release/changelog or a second primary source; a second syndication is not independent confirmation.

Review supply chain, IAM/API, networking/fabric, host/GPU/virtualization, Kubernetes/Slurm, data/keys, telemetry/detection, governance/compliance, abuse and response/recovery. For each area choose: actionable repository change, already covered, watch pending evidence, or out of scope. A category without a confirmed new event is not proof that no vulnerabilities exist.

Read the current catalog, errata and relevant implementation before labelling a gap. Prefer a missing example, evidence contract or bounded negative check to a new platform. Prioritize exposed or actively exploited paths, tenant-boundary failures and root/control-plane risks using actual applicability, not CVSS alone. Retain unresolved exposure and review dates in a private operational register.

Create a focused Issue when tracking is useful, then a PR. Run local checks, review the exact head and merge only the tested, justified change. No remote Actions dispatch or rerun while quota is constrained; preserve the manual-only workflow, use `[skip ci]`, and do not bypass branch rules. Recheck the base/head before merging. A partial checkout or failed check must be disclosed; it is not a full-suite green result.

Every run reports new practices, repository gaps, Issues/PRs, exact tests, merged changes, unmerged changes with reasons and next watch items. A repository documentation fix never means that a customer's environment was remediated.

## 2. Minimal advisory register

Use [the synthetic example](../../templates/advisory-triage.example.json) as a format reference, not as an assessment. Keep actual assets, credentials, evidence and customer identifiers outside this public repository. The optional format is independent of the core catalog and existing CSVs.

| Fields | Meaning |
|---|---|
| `format_version`, `reviewed_on`, `records` | Exact top-level fields; version is the string `1`; non-empty array of records. |
| `id`, `product`, `source_url` | Unique assessment-row ID, precise product and HTTPS primary-source locator. Separate products/scopes can share an advisory ID. URLs are never fetched by the checker. |
| `source_published_on`, `source_accessed_on` | ISO dates. Publication can be `null` for undated or unresolved source chronology; explain that in `rationale`. Access cannot follow review. |
| `scope`, `version_and_configuration` | Service/region/tenant/asset boundary and installed plus running versions, active configuration and supported backport evidence. These are human assertions, not machine-discovered inventory. |
| `applicability`, `disposition` | `UNKNOWN / AFFECTED / NOT_AFFECTED`; separately `OPEN / MITIGATED / REMEDIATED / NOT_APPLICABLE`. |
| `owner`, `rationale`, `next_review_on` | Responsible owner, reasoning/residual risk and next review date. `UNASSIGNED` is allowed only for unverified intake, not a recorded PASS. |
| `evidence_ids`, `verification_result` | Private evidence references and `PASS / FAIL / INCONCLUSIVE / NOT_TESTED`. No secret values or real evidence are included in the example. |
| `reviewer`, `verified_on`, `valid_until` | Reviewer and evidence dates. A different name is necessary for this metadata check, but does not prove independence. |

The checker rejects missing/unknown fields, duplicate JSON keys/IDs, non-finite numbers, malformed dates, invalid enums, future reviews and overdue review dates. Dates use `YYYY-MM-DD`; validity ends at the start of `valid_until`. A PASS requires known applicability, evidence references, an assigned owner, a distinct assigned reviewer and current verification dates. The next review cannot exceed evidence validity. Non-PASS records carry `null` verification/validity dates.

`MITIGATED` and `REMEDIATED` require `AFFECTED` and a recorded PASS. `NOT_APPLICABLE` requires evidence-backed `NOT_AFFECTED` and a recorded PASS for that applicability assertion. This does not mark the underlying control inapplicable. Unknown scope cannot close. Temporary mitigation is not a patch; residual risk and expiry remain explicit. Risk acceptance belongs in the existing exception/risk process and does not create PASS, VERIFIED or conformance.

```bash
# Current metadata check; defaults to the current UTC date.
python3 scripts/validate_advisory_triage.py /private/path/advisory-triage.json

# Reproduce the dated synthetic fixture, not a current operational assessment.
python3 scripts/validate_advisory_triage.py templates/advisory-triage.example.json --as-of 2026-09-08
python3 -m unittest discover -s tests -p test_advisory_triage.py -v

# Full checkout and declared dependencies required; do not claim this passed if unavailable.
python3 scripts/check_local.py
```

Exit 0 means consistent metadata as of the printed date. It does **not** authenticate sources/evidence, compare package versions, evaluate configuration, establish reviewer independence, evaluate invalidation events or verify remediation. Historical `--as-of` is replay only. Reopen the operational record after a relevant material change even before its time-based expiry. Every applicable unverified T0 remains **NO_GO_NONCONFORMANT**.

## 3. Four bounded operational additions

These are project-authored procedures motivated by the [dated primary-source ledger](../../reviews/2026-09-08-weekly-security-review.md). They complement RB-01/02/06/07/08 rather than replace them. Execute only in an explicitly authorized synthetic lab with an owner, approved maintenance window, abort criteria and recovery path. Do not reproduce published exploits or probe third-party tenants.

### A. Patch release to running-state evidence

Map NCS-ASM-01, NCS-ORC-04 and NCS-CMP-03. Identify the exact managed service, OS image/build, controller and running processes, not just a package label or image family. Distinguish upstream fix, distribution backport, provider image publication and actual node replacement. Use an approved canary and verify loaded versions, job completion, policy enforcement and recovery. Quarantine unverified capacity; do not automatically reintroduce a vulnerable image during rollback. Record both permitted workload success and the reviewed denied boundary. Provider-only evidence stays a provider responsibility.

### B. Revocation beyond the Kubernetes API

Map NCS-IAM-04, NCS-KMS-02 and NCS-ORC-04. With disposable identities and harmless records, revoke a previously permitted cross-namespace association. Inspect the operator's reconciliation and removal/rotation of generated backend credentials. Check that the old disposable credential is denied at the backend while an independently authorized identity still succeeds. Redact credentials and retain decision/request IDs. A Kubernetes denial alone does not establish revocation of an existing database credential. Stop on any unexpected access; containment/rotation and independent retest precede reopening.

### C. Storage-controller authority

Map NCS-API-01, NCS-DAT-04 and NCS-ORC-02. Review PV-creation authority, active deletion options, CSI identity, filesystem/access-point ownership and cloud resource policy together. Prefer patched vendor software and least privilege. Validate object/tenant ownership with inert unit fixtures or vendor-supported non-destructive checks; do not construct destructive volume handles or delete real data. Verify that authorized storage use survives the policy change. A driver issue is not automatically a storage-service breach; disabled affected configuration is an applicability claim requiring evidence and revalidation.

### D. Agent and model pipeline permissions

Map NCS-AIR-03, NCS-SSC-02 and NCS-DAT-03. Enforce read-only agent permissions at the database/resource identity, not only in tool descriptions or SQL filtering. For artifact admission, bind the digest to the approved signer/builder, source repository and expected build inputs; a valid signature alone is insufficient. Use harmless unsupported formats and unauthorized synthetic requests, not malicious payloads. Verify allow-path functionality and denied side effects, then record rollback/recall and the identities used. Retain existing loader isolation and provenance controls rather than adding a mandatory agent framework.

## 4. Network migration, monitoring and incident readiness

A provider feature retirement is a scoped migration trigger, not a reason to standardize every cloud on one CNI. Record OS/CNI compatibility, DNS/service dependencies and paired allow/deny tests before default-deny rollout. Preserve OOB/recovery access. Kubernetes NetworkPolicy does not replace fabric/DPU/storage isolation; keep RB-03/04/09.

Correlate policy changes, operator reconciliation, credential lifecycle, denied backend use and storage decisions through tenant-safe IDs. Alert on missing audit sources. Do not treat a dashboard, a Prometheus label or a successful collector exit as tenant authorization. Keep RB-05 and its attribution limitations.

For legal deadlines, first establish the actual product, supplier role, jurisdiction and contractual scope with the responsible legal/compliance owner. Maintain incident intake, evidence preservation, authority, notification and recovery exercises. Future deadlines are not already-effective obligations; a draft is not a final standard. The dated report carries current scoped notices instead of freezing deadlines into the base catalog.
