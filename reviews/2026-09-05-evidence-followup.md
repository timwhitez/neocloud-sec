# Evidence and operational-validation follow-up — 2026-09-05

**Integration base:** `9a0988331f978170ec7499ae0db4521509ec8480` (PR #5).
**Core:** 1.0.0-draft.1 · **Public-findings profile:** 1.0.1.

## Concurrent update preserved

The initial review used `2bd7dd6241919226623f02b735f049449849535d` and reproduced the count, schema, CSV parity and source-locator defects. Before publication, PR #5 landed on main with overlapping fixes. This follow-up is based on that new commit and preserves its profile, schemas, compiler, dependencies, existing tests and both legacy validators. The earlier alternative mapping/tool implementation was not overlaid on the newer main.

PR #5 records 70 local tests. This follow-up does not claim to rerun those tests or combine them with the new tests into a single executed result. Its [separate review](2026-09-05-validation-audit.md) retains its own scope and limitations.

## Additions

- An offline evidence-record checker distinguishes record consistency from evidence authenticity and service conformance. It checks CSV widths/headers/IDs, control ID format, lifecycle/verdict relationships, required PASS scope, timezone-aware observation/verification/expiry ordering, digest syntax and obvious self-verification.
- Eighteen local tests cover valid synthetic records, expiry, future/reversed dates, missing fields, malformed CSV/UTF-8, duplicates and CLI exit behavior. The distributed example remains PROPOSED / NOT_TESTED.
- Ten bilingual operational runbooks complement existing coverage guidance with allowed/prohibited paths, evidence, abort and recovery conditions. They are project-authored plans, not executed provider tests or a new machine-validated join to the profile.
- Current scope documents distinguish public repository visibility from licensing and assurance. The repository is public as observed on 2026-09-05; older private-repository notes are historical snapshots.
- The existing workflow's commands and pinned actions are preserved, but its automatic PR/push triggers are removed while Actions quota is constrained. It now requires explicit manual dispatch; this work does not dispatch it.

## Source observations and limits

- [SemiAnalysis article](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security): only indexed public excerpts were available in this review. No complete full-text or proprietary-framework coverage claim is made.
- [ClusterMAX Security detail](https://www.clustermax.ai/criteria/security) and [overview](https://clustermax.semianalysis.com/criteria): retrieved detail and overview counts differ (20 versus 21, with scenario-specific counts). This does not prove exactly one unique missing requirement; item-level/version reconciliation remains unresolved.
- [BlueField modes](https://networking-docs.nvidia.com/bsp/latest/modes-of-operation): DPU mode and restricted-host privilege are distinct; bind assertions to model/BSP/firmware and lifecycle.
- [UFM configuration](https://docs.nvidia.com/networking/display/ufmenterpriseumv62320/Optional-Configurations) and [Security tab](https://networking-docs.nvidia.com/ufmenterpriseum/6.26.1/security-tab): key classes, manager GUID policy and abuse controls are version-specific. Configuration checks are not end-to-end isolation proof.
- [Prometheus](https://prometheus.io/docs/operating/security/) and [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/): backend access and query credentials matter; tenant labels/dashboard visibility are not authorization boundaries. Grafana permissions are edition-dependent.
- [GPU Operator sharing](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html): device-plugin time-slicing lacks replica memory/fault isolation and limits DCGM-Exporter container attribution. This is not a universal claim about mediated vGPU.

These sources support specific technical mechanisms, not every project-authored recommendation. No raw article or private evidence is redistributed.

## Executed locally

```text
python3 -m unittest discover -s tests -p test_evidence_records.py -v
Ran 18 tests
OK

python3 -m py_compile scripts/validate_evidence_records.py tests/test_evidence_records.py
PASS
```

The tests use synthetic records and the exact new checker/example bytes. No cloud, GPU, tenant, fabric or penetration tests were performed. Network restrictions prevented a complete local checkout, so the full existing repository suite was not run. The existing `scripts/check_local.py` will discover the new test file in a normal complete checkout; no skipped or absent test group is reported as green here.

Local UTF-8, changed-document relative-path checks and published Git blob identity are checked separately. No external reviewer or independent assessor is claimed. No remote CI status, About/topics mutation, license choice, visibility change or branch-protection bypass is asserted. Commits and merge messages use `[skip ci]`.
