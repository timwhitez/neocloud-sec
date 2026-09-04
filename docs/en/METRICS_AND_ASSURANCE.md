# NeoCloud Cyber Security Metrics and Continuous Assurance Guide

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Purpose:** measure whether security outcomes are true for the deployed NeoCloud service, not whether security activity occurred

This guide defines the measurement, evidence, verification, and reporting model for the [Security Baseline](SECURITY_BASELINE.md). It should be used with the machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json), the [Practice Guide](PRACTICE_GUIDE.md), and the repository templates.

## 1. Assurance principles

1. **Gates precede scores.** Any failed or unknown applicable T0 produces `NO-GO`; an aggregate percentage cannot override it.
2. **Measure the deployed boundary.** A metric without service, tenant, region, version, asset, and time scope is not decision quality.
3. **Separate implementation from effectiveness.** Deployment status, coverage, freshness, negative-test success, and independent verification are distinct facts.
4. **Use independent observation.** High-impact claims require evidence from a boundary or method not controlled solely by the implementer.
5. **Prefer outcomes over activity.** Count whether unsafe access was denied and recovery succeeded, not only policies written, scans run, or tickets closed.
6. **Unknown, stale, and inconclusive are visible states.** They must never be silently converted to pass.
7. **Reproducibility is part of quality.** A reviewer should be able to run the query or test and obtain the same result for the stated scope.
8. **Metrics must resist gaming.** Define denominator, exclusions, ownership, source, latency, sampling, and change controls before setting a target.
9. **Security data is sensitive.** Tenant partitioning, minimization, access control, integrity, retention, and legal/privacy requirements apply to the assurance plane itself.
10. **Automation earns trust.** Automated evidence and remediation require precision, rollback, failure-mode, and independent-verifier measurements.

## 2. Required control-state model

The only normal completion path is:

`PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`

| State | Meaning | Allowed evidence claim |
|---|---|---|
| `PROPOSED` | desired outcome identified; scope or owner may be incomplete | no implementation claim |
| `READY` | scope, owner, dependencies, requirement, test, evidence, and target date defined | implementation may begin |
| `IMPLEMENTED` | mechanism deployed in stated scope | deployment only; effectiveness not proven |
| `CANDIDATE_DONE` | owner supplied evidence and claims completion | awaiting independent validation |
| `VERIFIED` | independent validator returned `PASS` for current scope and evidence | control may be represented as effective until expiry or invalidation |

Verification results are:

- `PASS`: assertion reproduced; required positive and negative tests passed.
- `FAIL`: assertion contradicted or a required test failed.
- `INCONCLUSIVE`: evidence or test cannot support a reliable decision.
- `NOT_TESTED`: no current test result.

`INCONCLUSIVE`, `NOT_TESTED`, expired evidence, missing scope, or missing validator cannot be counted as verified.

## 3. Production decision gates

For each service profile, compute gates before any maturity score.

```text
if applicable_T0_failed > 0:
    decision = NO_GO
elif applicable_T0_unknown_or_stale > 0:
    decision = NO_GO
elif critical_scope_unknown > 0:
    decision = NO_GO
elif required_isolation_revocation_restore_or_sanitization_test_failed:
    decision = NO_GO
elif unresolved_critical_risk_without_authorized_acceptance > 0:
    decision = NO_GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

A gate record must state service, profile, environment, regions, versions, assessment time, decision owner, validator, failed assertions, exceptions, and next revalidation.

## 4. Metric contract

Every metric definition must contain:

| Field | Requirement |
|---|---|
| ID and name | stable, versioned identifier and unambiguous title |
| Security question | decision the metric supports |
| Numerator/denominator | exact population and counting rule |
| Scope dimensions | service, tenant, region, environment, asset class, version, data class, isolation SKU |
| Data sources | authoritative systems and observation paths |
| Collection | owner, frequency, query/test, latency, integrity protection |
| Target and gate | desired range, warning threshold, hard failure where applicable |
| Exclusions | explicit, justified, expiring, and separately reported |
| Failure behavior | alert, block, quarantine, escalation, or manual review |
| Validator | who independently reviews the definition and samples results |
| Limitations | blind spots, sampling error, ambiguity, and expected false signals |
| Change control | owner and approval for definition, source, or target changes |

Percentages must publish both numerator and denominator. Medians must be accompanied by tail percentiles where catastrophic delay matters. A falling denominator is a warning, not an improvement.

## 5. Evidence data contract

Every evidence item should include:

```yaml
evidence_id: EVID-...
control_id: NCS-...
assertion: human-readable statement
scope:
  service: ...
  profile: ...
  environment: production
  tenants: [all | sampled identifiers]
  regions: [...]
  assets: [...]
  software_firmware_versions: [...]
observation:
  collected_at: RFC3339 timestamp
  collector_identity: ...
  source_system: ...
  method_or_query_version: ...
  result: ...
integrity:
  hash_or_signature: ...
  protected_location: ...
validity:
  expires_at: ...
  invalidation_triggers: [...]
verification:
  validator: ...
  test_id: ...
  result: PASS | FAIL | INCONCLUSIVE | NOT_TESTED
  findings: [...]
```

Critical evidence should be exported to a protected boundary and linked to stable service, tenant, subject, workload, host, GPU, fabric, data/model, artifact, request, and policy identifiers.

## 6. Core metric catalog

Targets below are reference starting points. Each organization must set targets based on service commitments and risk, while preserving all T0 hard gates.

### 6.1 Governance, ownership, and assurance

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-GOV-01 | Applicable T0 verified | verified applicable T0 / applicable T0 | 100%; hard gate |
| NCSM-GOV-02 | Critical service ownership | critical services with business, technical, security, data, and incident owners / critical services | 100% |
| NCSM-GOV-03 | Overdue critical exceptions | count of expired or overdue P0/P1 exceptions | 0; hard escalation |
| NCSM-GOV-04 | Customer commitment drift | commitments whose deployed state or evidence does not match / active commitments | 0 material drift |
| NCSM-GOV-05 | Independent-verification coverage | controls independently verified in period / controls due in period | 100% T0/T1 due population |
| NCSM-GOV-06 | Evidence freshness | non-expired required evidence / required evidence | 100% T0; ≥95% other priority controls |

### 6.2 Inventory and scope integrity

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ASM-01 | Critical asset ownership | critical assets with current owner / critical assets | ≥95% by day 90; 100% target |
| NCSM-ASM-02 | Privileged identity ownership | privileged identities with accountable owner and lifecycle / privileged identities | 100% |
| NCSM-ASM-03 | Desired/actual reconciliation latency | time from material state divergence to detection | p95 ≤15 minutes for tenant/isolation roots |
| NCSM-ASM-04 | Unknown production resources | production resources not mapped to service, tenant, and owner | 0 critical; downward trend otherwise |
| NCSM-ASM-05 | Dependency observability | critical dependencies with owner, health, failure mode, and recovery path / critical dependencies | 100% |

### 6.3 Human, workload, and agent identity

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-IAM-01 | Phishing-resistant privileged MFA | covered privileged human identities / privileged human identities | 100%; hard gate where applicable |
| NCSM-IAM-02 | Standing privileged access | identities with persistent high privilege / privileged population | minimize; 0 unapproved |
| NCSM-IAM-03 | Privilege grant duration | duration of JIT elevation | p95 within approved task window |
| NCSM-IAM-04 | Emergency revocation time | request-to-effective denial across all enforcement points | tested objective; report p50/p95/max |
| NCSM-IAM-05 | Short-lived workload credentials | production workloads using short-lived/brokered identity / production workloads | ≥80% by month 6; ≥95% mature target |
| NCSM-IAM-06 | Orphan identity closure | orphaned identities closed within SLA / discovered orphan identities | 100% critical; ≥98% overall |
| NCSM-IAM-07 | Agent delegation completeness | agents with identity, delegator, goal, scope, tools, budget, and expiry / production agents | 100% |

### 6.4 API and control-plane correctness

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-API-01 | Tenant-authorization negative-test pass rate | passed object/action/tenant tests / executed required tests | 100% critical APIs |
| NCSM-API-02 | Public provider-admin exposure | provider administrative interfaces directly reachable from public/tenant data planes | 0 unless explicitly designed and T0-approved |
| NCSM-API-03 | Missing tenant-context rejection | requests with missing/conflicting tenant context denied / generated tests | 100% |
| NCSM-API-04 | Control-state trace completeness | high-impact changes with request, policy, desired, actual, actor, and result correlation / high-impact changes | 100% |
| NCSM-API-05 | Partial-provisioning safe closure | failed workflows rolled back or quarantined / failed material workflows | 100% |

### 6.5 Network, fabric, compute, and accelerator isolation

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ISO-01 | Declared SKU isolation coverage | commercial SKUs with current host/GPU/cache/NVLink/network/RDMA/storage/support declaration / commercial SKUs | 100%; hard gate |
| NCSM-ISO-02 | Cross-tenant negative-test pass rate | passed required isolation tests / executed required tests | 100%; any failure is incident/gate failure |
| NCSM-ISO-03 | Placement-policy conformance | actual host/GPU/fabric/storage assignments matching approved policy / active assignments | 100% critical; immediate quarantine on material mismatch |
| NCSM-ISO-04 | Accelerator reassignment cleanup | reassignments with successful reset/error/cleanup evidence / tenant-to-tenant reassignments | 100% |
| NCSM-ISO-05 | Fabric assignment reconciliation | current VRF/VLAN/VXLAN/P_Key/DPU assignments matching tenant intent / active assignments | 100% |
| NCSM-ISO-06 | BMC/OOB unauthorized reachability | successful unauthorized reachability paths in tests | 0 |
| NCSM-ISO-07 | Isolation evidence age | age of last representative negative test by SKU/region/version | within policy; revalidate after material change |

### 6.6 Kubernetes, Slurm, runtime, and data/model lifecycle

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ORC-01 | Hardened-control-plane coverage | clusters/controllers meeting approved baseline / production clusters/controllers | 100% |
| NCSM-ORC-02 | Privileged workload/job policy effectiveness | prohibited privileged submissions denied / generated prohibited submissions | 100% |
| NCSM-ORC-03 | Orchestrator recovery success | representative restore or known-good rebuilds meeting integrity/isolation/RTO checks / exercises | 100% |
| NCSM-DAT-01 | Crown-jewel classification | crown-jewel datasets/models/keys/artifacts with owner and lifecycle / identified crown jewels | 100% |
| NCSM-DAT-02 | Data/model lineage completeness | material artifacts with source-to-use lineage / material artifacts | ≥95%; 100% release-critical |
| NCSM-DAT-03 | Deletion and offboarding verification | requests completed and independently evidenced within commitment / due requests | 100% |
| NCSM-DAT-04 | Unsafe artifact rejection | malicious/unsupported model or checkpoint formats rejected / generated tests | 100% |

### 6.7 Keys, secrets, and supply chain

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-KMS-01 | Unknown critical keys | critical keys without owner, purpose, location, rotation, and recovery record | 0 |
| NCSM-KMS-02 | Static secret exposure | active static production secrets outside approved exception | 0 critical; continuous reduction |
| NCSM-KMS-03 | Key/certificate rotation success | rotations completed without unauthorized access or material outage / planned and emergency rotations | 100% |
| NCSM-SSC-01 | High-impact artifact inventory | deployed high-impact artifacts with identity/version/owner/source / deployed high-impact artifacts | 100% |
| NCSM-SSC-02 | Provenance and signature coverage | release-critical artifacts with verified provenance/signature / release-critical artifacts | 100% target |
| NCSM-SSC-03 | Admission-policy effectiveness | unknown/unsigned/revoked artifacts denied / generated tests | 100% |
| NCSM-SSC-04 | Artifact recall time | decision-to-quarantine/deny across registries and runtime | tested objective; report p50/p95/max |

### 6.8 Vulnerability, exposure, telemetry, and detection

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-VEM-01 | Internet/root exposure SLA | due critical exposures remediated or isolated within SLA / due critical exposures | 100% |
| NCSM-VEM-02 | Verified remediation | findings whose deployed state was rescanned/retested / closed findings | 100% critical; ≥95% overall |
| NCSM-VEM-03 | Firmware/driver coverage | production devices mapped to current firmware/driver state / production devices | ≥95%; 100% critical roots |
| NCSM-TEL-01 | Critical telemetry coverage | required critical log sources healthy and queryable / required critical log sources | ≥95% by day 90; 100% hard-root sources |
| NCSM-TEL-02 | Telemetry freshness | sources delivering within expected latency / required sources | ≥99% critical |
| NCSM-TEL-03 | Detection validation pass rate | priority detections passing authorized behavior replay / due priority detections | ≥95%; 100% for catastrophic scenarios |
| NCSM-TEL-04 | Alert decision precision | true actionable alerts / reviewed alerts | track by use case; target based on response capacity |
| NCSM-TEL-05 | Evidence tamper detection | simulated unauthorized evidence changes detected / tests | 100% |

### 6.9 AI agent safety and automated defense

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-AIR-01 | Production agent inventory | agents with owner, identity, impact assessment, model/prompt/skill/tool versions / production agents | 100% |
| NCSM-AIR-02 | Tool mediation coverage | material tool calls passing typed schema and policy enforcement / material tool calls | 100% |
| NCSM-AIR-03 | Approval bypass rate | high-impact actions executed without required deterministic approval / high-impact actions | 0 |
| NCSM-AIR-04 | Scope-violation rate | actions outside immutable goal/scope/tenant/data/cost boundary / agent actions | 0 material violations |
| NCSM-AIR-05 | Deterministic-stop effectiveness | scenarios stopped at success/budget/time/repetition/policy/uncertainty boundary / generated scenarios | 100% priority scenarios |
| NCSM-AIR-06 | False-completion rate | tasks marked complete/verified without sufficient evidence / completed tasks sampled | 0 for verifier-gated claims |
| NCSM-AIR-07 | Verifier disagreement | material owner/agent claims overturned by independent verifier / verified candidates | trend and investigate by class |
| NCSM-AIR-08 | Automated rollback success | failed automated changes safely reverted / changes requiring rollback | 100% tested reversible class |

### 6.10 Abuse, incident response, resilience, and physical roots

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ABU-01 | Quota/rate/cost control bypass | successful bypasses in authorized tests | 0 |
| NCSM-ABU-02 | Urgent abuse containment time | validated urgent abuse to effective containment | service SLO; report p50/p95/max |
| NCSM-IRR-01 | Time to establish command | qualifying alert/report to named incident commander and secure channel | objective by severity |
| NCSM-IRR-02 | Time to reliable scope | incident declaration to evidence-backed affected service/tenant/resource set | objective by scenario; report uncertainty |
| NCSM-IRR-03 | Time to effective containment | incident declaration to verified isolation/revocation at reliable boundary | objective by scenario |
| NCSM-IRR-04 | Verified closure quality | incidents closed with evidence, root cause, recovery checks, actions, and independent review / closed material incidents | 100% |
| NCSM-RES-01 | Restore objective success | exercises meeting declared RTO/RPO plus integrity and isolation / exercises | 100% critical services |
| NCSM-RES-02 | Immutable backup coverage | critical provider-managed state with protected immutable backup / critical state | 100% where backup is required |
| NCSM-RES-03 | Known-good rebuild success | rebuilds meeting version, identity, isolation, data, and monitoring criteria / exercises | 100% |
| NCSM-PHY-01 | BMC/root baseline coverage | BMC/OOB devices with owner, inventory, hardened state, patch, and protected access / devices | 100% |
| NCSM-PHY-02 | Sanitization verification | tenant reassignments/decommissions with successful documented sanitation / applicable events | 100%; hard gate before reassignment |

## 7. Evidence strength score

A strength score helps prioritization but never replaces a gate.

| Level | Evidence type | Typical use |
|---:|---|---|
| 0 | no evidence or unsupported assertion | fail/unknown |
| 1 | policy, design statement, interview | intent only |
| 2 | screenshot or manually curated report | directional review |
| 3 | repeatable API/query/export tied to scope | implementation and coverage |
| 4 | protected runtime event, signed attestation, or automated reconciliation | current operational assertion |
| 5 | authorized negative/failure/restore test independently reproduced | high-confidence effectiveness |

For T0, require current scope-specific evidence plus independent testing appropriate to the assertion; a numeric level alone does not guarantee sufficiency.

## 8. Sampling rules

Full-population evaluation is preferred for identities, configurations, assignments, public endpoints, deployed artifacts, exceptions, and evidence freshness. Sampling may be used for expensive adversarial, destructive, or physical tests only when:

- the population and selection method are documented;
- all material service/SKU/region/version variants are represented;
- high-risk and recently changed items receive higher probability;
- confidence and blind spots are reported;
- any failure expands the sample and triggers incident or remediation;
- catastrophic boundaries are never inferred solely from convenience samples.

A representative GPU reset test must account for hardware model, firmware, driver, virtualization/sharing mode, scheduler path, region, and reassignment workflow.

## 9. Continuous-assurance pipeline

```text
Discover actual state
  → normalize identities and assets
  → evaluate policy and control assertions
  → collect protected evidence
  → run safe positive/negative tests
  → compare desired and actual state
  → independent verifier decision
  → gate, alert, quarantine, or accept risk
  → track remediation and re-test
  → publish scoped assurance
```

The pipeline must monitor itself: missing collectors, delayed sources, schema errors, conflicting identifiers, permission loss, partial test execution, verifier unavailability, and evidence-store integrity are first-class failures.

## 10. Dashboard design

Use separate views rather than one blended score.

### Executive view

- production decision by service/profile;
- failed, unknown, or stale T0 controls;
- critical exceptions and customer commitment drift;
- top root-of-trust, cross-tenant, data/model, and resilience risks;
- incident and recovery objective failures;
- decision owner and due date.

### Service-owner view

- control state and evidence expiry;
- asset/identity/dependency scope gaps;
- desired/actual drift;
- test failures and remediation path;
- customer responsibility and commitments;
- release, change, and revalidation triggers.

### Security-operations view

- critical telemetry health;
- active exposure and exploitability;
- identity/root/fabric/GPU/agent anomalies;
- detection quality and missed behaviors;
- containment readiness and automation health.

### Assurance view

- evidence strength, freshness, integrity, and reproducibility;
- validation due dates and independence;
- samples, limitations, exceptions, and failed tests;
- claims safe to present to customers or auditors.

## 11. Reporting language

Use precise statements:

- Good: “All 14 applicable T0 controls for GPU-IaaS service X, regions A/B, release 2026.09, were independently verified as of 2026-09-04; two T1 evidence items expire within 14 days.”
- Bad: “Security is 96% complete.”
- Good: “Dedicated SKU Y dedicates host, GPU, NVLink domain, tenant data network and local storage; provider telemetry and BMC remain shared provider services with JIT access.”
- Bad: “Fully dedicated and zero trust.”

Every external assurance statement must identify scope, date, version, limitations, exceptions, and verifier.

## 12. Assurance cadence

| Frequency | Minimum review |
|---|---|
| Continuous | T0 state, identity/policy, public exposure, assignment drift, critical telemetry, root use, backup health, agent high-impact action |
| Daily | failed collectors/tests, unknown/unowned critical state, urgent exposure, containment backlog |
| Weekly | vulnerability SLA, privilege, release, exceptions, detection failures, incident actions |
| Monthly | executive risk and gate review, customer commitment drift, metric denominator/source quality |
| Quarterly | T0/T1 revalidation, access review, isolation tests, revocation/restore, detection replay, agent adversarial evaluation |
| Semi-annual | major incident, control-plane recovery, root compromise, customer notification, destructive automation exercise |
| Annual | independent architecture/penetration/isolation review, regional DR/known-good rebuild, supplier and cryptographic recovery |
| Material change | immediate re-scope and revalidation of affected assertions |

## 13. Assurance package template

A service assurance package should include:

1. service description, profiles, boundary, regions, versions, and shared-responsibility matrix;
2. applicable control set and production-gate decision;
3. isolation statement by host, GPU/cache/NVLink, network/RDMA, storage, telemetry, BMC, and support;
4. identity, key, artifact, data/model, logging, incident, backup, deletion, and residency summaries;
5. evidence index with freshness, strength, source, and validator;
6. test summary including negative-path, restore, revocation, sanitization, and incident exercises;
7. current material findings, exceptions, compensating controls, customer impact, and remediation dates;
8. independent-review statement and limitations;
9. next verification date and invalidation triggers.

## 14. Common measurement failures

- counting controls without checking applicability and scope;
- reporting percentage complete while T0 is failed;
- using number of scans, alerts, policies, or tickets as proof of reduced risk;
- excluding difficult assets from the denominator without disclosure;
- treating missing telemetry as zero events;
- measuring mean response time without p95/max and severity segmentation;
- accepting a vendor dashboard as the only observation path;
- allowing a control owner or agent to self-verify;
- continuing to count expired evidence as pass;
- changing definitions or denominators to improve a trend;
- measuring automation speed without approval bypass, false completion, rollback, and policy violation;
- reopening after recovery without independent identity, integrity, isolation, and data checks.

## 15. Minimum definition of measurable security

A NeoCloud control is measurably effective only when its scope and owner are known, the implementation exists in the deployed path, required evidence is current and protected, a prohibited path has been tested where relevant, an independent validator can reproduce the assertion, failure creates an explicit operational response, and the control is revalidated after expiry or material change.
