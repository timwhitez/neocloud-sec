# NeoCloud Cyber Security Metrics and Continuous Assurance Guide

**Version:** 1.0.0-draft.1  
**Baseline date:** 2026-09-04  
**Status:** implementation-oriented project draft  
**Purpose:** measure whether security outcomes are true for the deployed service, not merely whether security activity occurred

Use this guide with the [Security Baseline](SECURITY_BASELINE.md), machine-readable [control catalog](../../controls/neocloud-security-baseline.v1.json), [Practice Guide](PRACTICE_GUIDE.md), and repository templates.

## 1. Assurance principles

1. **Gates precede scores.** Any failed, unknown, stale, `INCONCLUSIVE`, or `NOT_TESTED` applicable T0 produces `NO_GO_NONCONFORMANT`.
2. **Risk acceptance is not control verification.** A business decision may authorize temporary operation but cannot change a failed control result or support a conformance claim.
3. **Measure the deployed boundary.** Service, profile, environment, region, version, tenant/asset/data scope, and observation time are part of every material assertion.
4. **Separate deployment from effectiveness.** Implementation state, population coverage, evidence freshness, negative-test success, failure behavior, and independent verification are different facts.
5. **Unknown scope stays in view.** Unknown or unowned critical resources are failures; they are not silently removed from a denominator.
6. **Use independent observation.** High-impact claims require a verifier able to challenge the implementer and, where practical, a separate observation or test path.
7. **Prefer outcomes over activity.** Measure denied unsafe access, corrected drift, effective revocation, safe cleanup, successful recovery, and reliable scope—not only policies, scans, alerts, or tickets.
8. **Reproducibility is evidence quality.** A qualified reviewer should be able to execute the stated query/test and reproduce the result for the stated scope.
9. **Metrics resist gaming.** Define numerator, denominator, exclusions, data owner, source, latency, sampling, target, gate, and change control before reporting a trend.
10. **The assurance plane is sensitive.** Apply tenant partitioning, minimization, access control, integrity protection, retention, legal/privacy treatment, and source-health monitoring.
11. **Automation earns trust.** Measure approval bypass, scope violation, false completion, rollback, stop behavior, evidence integrity, and verifier independence—not just speed.

## 2. Control and verification state

The only normal completion path is:

```text
PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED
```

| State | Meaning | Allowed claim |
|---|---|---|
| `PROPOSED` | desired outcome identified; scope or owner may be incomplete | no implementation claim |
| `READY` | scope, owner, dependencies, requirement, test, evidence, failure behavior and target date defined | implementation may begin |
| `IMPLEMENTED` | mechanism deployed in the stated scope | deployment only; effectiveness not proven |
| `CANDIDATE_DONE` | owner supplied current evidence and asserts completion | awaiting independent validation |
| `VERIFIED` | independent validator returned `PASS` for the exact scope and validity period | may be represented as effective until invalidated |

Verification results are `PASS`, `FAIL`, `INCONCLUSIVE`, and `NOT_TESTED`. Only `PASS` may create `VERIFIED`. Evidence expiry, material change, incident, control failure, scope conflict, or inability to reproduce invalidates the result.

## 3. Production decision gates

Compute hard gates before maturity or progress scores:

```text
if applicable_T0_failed_or_unknown_or_stale_or_inconclusive_or_untested > 0:
    decision = NO_GO_NONCONFORMANT
elif critical_scope_unknown > 0:
    decision = NO_GO_NONCONFORMANT
elif required_isolation_revocation_restore_incident_or_sanitization_test_failed:
    decision = NO_GO_NONCONFORMANT
elif unresolved_high_risk_without_accountable_decision > 0:
    decision = NO_GO
else:
    decision = GO_WITH_RECORDED_RESIDUAL_RISK
```

An emergency business decision is recorded separately and does not alter `NO_GO_NONCONFORMANT` or create `VERIFIED` status.

A gate record must state service/profile, environment, regions, versions, tenant/asset/data scope, assessment time, control/evidence versions, decision owner, validator, failed or unknown assertions, business-risk decisions, customer impact, and next revalidation.

## 4. Metric contract

Every metric must define:

| Field | Requirement |
|---|---|
| ID and name | stable, versioned, unambiguous identifier |
| Security question | decision the metric supports |
| Numerator and denominator | exact population, counting rule, treatment of unknowns and duplicates |
| Scope | service, profile, tenant, region, environment, asset/data class, version, isolation SKU |
| Sources | authoritative systems and independent observation paths |
| Collection | owner, method/query/test version, frequency, latency, integrity and failure detection |
| Target and gate | desired range, warning threshold and hard failure where applicable |
| Exclusions | explicit, justified, approved, expiring and separately reported |
| Failure response | alert, block, quarantine, escalation, risk decision or manual review |
| Validator | independent reviewer and sampling/reproduction method |
| Limitations | blind spots, error, ambiguity, false signals and unsupported populations |
| Change control | approval for definition, source, target or denominator changes |

Report numerator and denominator with every percentage. When catastrophic delay matters, report p50, p95 and maximum or a justified tail measure. A shrinking denominator, missing source, or suddenly unscoped population is an alert, not an improvement.

## 5. Evidence data contract

```yaml
evidence_id: EVID-...
control_id: NCS-...
assertion: human-readable, testable statement
scope:
  service: ...
  profile: ...
  environment: production
  tenants: [all | sampled identifiers]
  regions: [...]
  assets: [...]
  data_classes: [...]
  software_firmware_versions: [...]
observation:
  collected_at: RFC3339 timestamp
  collector_identity: ...
  source_system: ...
  method_or_query_version: ...
  result: ...
  population_and_sample: ...
integrity:
  protection: hash | signature | tamper-evident store | other
  protected_location: ...
validity:
  expires_at: ...
  invalidation_triggers: [...]
verification:
  validator: ...
  test_id: ...
  result: PASS | FAIL | INCONCLUSIVE | NOT_TESTED
  limitations: [...]
  findings: [...]
  retest_due: ...
```

Critical evidence should be exported to a protected boundary and linked through stable service, tenant, subject, request, workload/job, host, GPU, fabric, storage, data/model, artifact, policy, action and result identifiers.

## 6. Core metric catalog

Targets below are project reference points. They do not replace threat modeling, service commitments, legal obligations or control gates.

### 6.1 Governance, ownership and assurance

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-GOV-01 | Applicable T0 verified | independently verified applicable T0 / applicable T0 | 100%; hard gate |
| NCSM-GOV-02 | Critical service ownership | critical services with accountable business, technical, security, data and incident owners / critical services | 100% |
| NCSM-GOV-03 | Overdue critical decisions/exceptions | expired or overdue P0/P1 risk and exception records | 0; hard escalation |
| NCSM-GOV-04 | Customer commitment drift | commitments contradicted by deployed state or current evidence / active commitments | 0 material drift |
| NCSM-GOV-05 | Independent-verification completion | controls independently verified in period / controls due in period | 100% of due T0/T1 and committed T3 populations |
| NCSM-GOV-06 | Evidence freshness | non-expired required evidence / required evidence | 100% T0; target ≥95% for other priority evidence, with gaps visible |

### 6.2 Inventory and scope integrity

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ASM-01 | In-scope critical asset ownership | in-scope critical assets with service, tenant where applicable, lifecycle and accountable owner / all in-scope critical assets including discovered unknowns | 100%; unknown critical resources fail the gate |
| NCSM-ASM-02 | Privileged identity ownership | privileged identities with owner and lifecycle / privileged identities | 100% |
| NCSM-ASM-03 | Desired/actual drift detection latency | material state divergence to detection | service objective; reference p95 ≤15 minutes for tenant/isolation roots |
| NCSM-ASM-04 | Unknown production resources | discovered production resources not mapped to service, tenant where applicable and owner | 0 critical; explicit downward trend otherwise |
| NCSM-ASM-05 | Independent discovery coverage | production scope observed by at least one independent discovery/reconciliation path / expected production scope | reference ≥95% by day 90; exclusions explicit; critical unknowns still fail |

### 6.3 Human, workload and agent identity

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-IAM-01 | Phishing-resistant privileged MFA | covered applicable privileged/high-impact human identities / applicable population | 100%; hard gate |
| NCSM-IAM-02 | Standing privileged access | persistent high-privilege identities / privileged population | 0 unapproved; minimize approved cases |
| NCSM-IAM-03 | JIT privilege duration | grant-to-expiry duration | p95 within approved task window |
| NCSM-IAM-04 | Emergency revocation time | request to verified denial across required enforcement points | scenario-specific SLO; report p50/p95/max |
| NCSM-IAM-05 | Short-lived workload credentials | production workloads using short-lived/brokered credentials / production workloads | reference ≥80% by month 6; mature target ≥95% |
| NCSM-IAM-06 | Orphan identity closure | orphan identities closed within SLA / discovered orphan identities | 100% critical; reference ≥98% overall |
| NCSM-IAM-07 | Agent delegation completeness | production agents with owner, identity, delegator, use case, scope, tools, authority and expiry/review / production agents | 100% |

### 6.4 API and control-plane correctness

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-API-01 | Tenant-authorization negative-test pass rate | passed object/action/tenant/purpose/context tests / required executed tests | 100% critical APIs |
| NCSM-API-02 | Direct provider-admin exposure | provider administration reachable directly from public or tenant data planes outside the governed privileged path | 0; hard gate |
| NCSM-API-03 | Missing/conflicting tenant-context rejection | correctly rejected generated requests / generated requests | 100% |
| NCSM-API-04 | Control-state trace completeness | high-impact changes correlated across request, actor, tenant, policy, approval, desired/actual state and result / high-impact changes | 100% |
| NCSM-API-05 | Partial-provisioning safe closure | failed material workflows rolled back or quarantined and verified / failed material workflows | 100% |

### 6.5 Network, fabric, compute and accelerator isolation

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ISO-01 | Declared SKU isolation coverage | commercial SKUs with current host/GPU/cache/NVLink/network/RDMA/storage/telemetry/support declaration / commercial SKUs | 100%; hard gate |
| NCSM-ISO-02 | Cross-tenant negative-test pass rate | passed required prohibited-path tests / required executed tests | 100%; any failure is an incident/gate failure |
| NCSM-ISO-03 | Placement-policy conformance | actual host/GPU/fabric/storage assignments matching policy / active assignments | 100% critical; quarantine material mismatch |
| NCSM-ISO-04 | Accelerator reassignment cleanup | tenant-to-tenant reassignments with verified reset/error/cleanup evidence / applicable reassignments | 100% |
| NCSM-ISO-05 | Fabric assignment reconciliation | current VRF/VLAN/VXLAN/P_Key/DPU assignments matching approved tenant intent / active assignments | 100% |
| NCSM-ISO-06 | BMC/OOB unauthorized reachability | successful unauthorized paths in representative tests | 0 |
| NCSM-ISO-07 | Isolation evidence age | time since representative test by service/SKU/region/hardware/firmware/driver/mode | within policy; invalidated by material change |

### 6.6 Orchestration and data/model lifecycle

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ORC-01 | Hardened control-plane coverage | production clusters/controllers meeting the applicable baseline / production population | 100% |
| NCSM-ORC-02 | Privileged workload/job policy effectiveness | prohibited submissions denied / generated prohibited submissions | 100% |
| NCSM-ORC-03 | Orchestrator recovery success | restore or known-good rebuilds meeting identity, integrity, isolation and RTO checks / exercises | 100% |
| NCSM-DAT-01 | Crown-jewel lifecycle coverage | identified crown-jewel data/models/keys/artifacts with owner, classification, purpose and lifecycle / identified population | 100% |
| NCSM-DAT-02 | Data/model lineage completeness | release/material artifacts with required source-to-use lineage / applicable artifacts | 100% release-critical; reference ≥95% other material artifacts |
| NCSM-DAT-03 | Deletion/offboarding verification | due requests completed and independently evidenced within commitment / due requests | 100% |
| NCSM-DAT-04 | Unsafe artifact rejection | generated malicious/unsupported/revoked model/checkpoint cases rejected / generated cases | 100% |

### 6.7 Keys, secrets and supply chain

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-KMS-01 | Unknown critical keys | critical keys missing owner, purpose, location, access, rotation or recovery record | 0 |
| NCSM-KMS-02 | Static production secret exposure | active static/embedded secrets outside approved expiring exception | 0 critical; continuous reduction otherwise |
| NCSM-KMS-03 | Key/certificate rotation and recovery success | exercises completed without unauthorized access or unplanned material outage / planned and emergency exercises | 100% |
| NCSM-SSC-01 | High-impact artifact inventory | deployed high-impact artifacts with identity, owner, source and version / deployed high-impact artifacts | 100% |
| NCSM-SSC-02 | Required provenance/signature coverage | release-critical artifacts meeting applicable provenance/signature policy / applicable release-critical artifacts | 100% |
| NCSM-SSC-03 | Admission-policy effectiveness | generated unknown/unsigned-when-required/revoked/incompatible artifacts denied / generated cases | 100% |
| NCSM-SSC-04 | Artifact recall time | decision to verified deny/quarantine across required registries/runtime | tested SLO; report p50/p95/max |

### 6.8 Vulnerability, exposure, telemetry and detection

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-VEM-01 | Internet/root exposure SLA | due critical exposures remediated or reliably isolated within SLA / due critical exposures | 100% |
| NCSM-VEM-02 | Verified remediation | closed findings retested against deployed state / closed findings | 100% critical; reference ≥95% overall |
| NCSM-VEM-03 | Firmware/driver state visibility | production devices with current, attributable firmware/driver state / production devices | 100% critical roots; reference ≥95% overall |
| NCSM-TEL-01 | Required T0 telemetry coverage | healthy, queryable required T0 sources / required T0 sources | 100%; hard gate; missing telemetry is not zero activity |
| NCSM-TEL-02 | Priority telemetry coverage | healthy, queryable priority sources / defined priority sources | reference ≥95% by day 90, with gaps and risk explicit |
| NCSM-TEL-03 | Telemetry freshness | sources delivering within expected latency / required sources | target set per source; reference ≥99% critical |
| NCSM-TEL-04 | Detection validation pass rate | priority detections passing authorized behavior replay / due priority detections | 100% catastrophic scenarios; reference ≥95% other priority detections |
| NCSM-TEL-05 | Evidence tamper detection | simulated unauthorized evidence changes or source-health failures detected / tests | 100% priority tests |
| NCSM-TEL-06 | Alert decision precision and recall proxy | actionable outcomes and known missed test behaviors / reviewed alerts and test corpus | track by use case; publish limitations and sampling |

### 6.9 AI agent and automated-defense safety

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-AIR-01 | Production agent inventory | agents with owner, identity, use case, impact assessment and versioned components / production agents | 100% |
| NCSM-AIR-02 | Tool mediation coverage | material tool calls passing typed validation and policy enforcement / material tool calls | 100% |
| NCSM-AIR-03 | Required approval bypass | high-impact actions executed without required deterministic approval / high-impact actions | 0 |
| NCSM-AIR-04 | Material scope violation | actions outside immutable or approved goal/tenant/data/tool/egress/cost boundary / agent actions | 0 |
| NCSM-AIR-05 | Deterministic-stop effectiveness | priority scenarios stopped at success/budget/time/repetition/policy/uncertainty boundary / generated scenarios | 100% applicable priority scenarios |
| NCSM-AIR-06 | False completion | tasks represented complete/verified without sufficient evidence / sampled completed tasks | 0 verifier-gated claims |
| NCSM-AIR-07 | Verifier disagreement | material candidate claims overturned by independent verifier / candidates | trend by failure class; investigate all material disagreements |
| NCSM-AIR-08 | Automated rollback/manual recovery success | failed automated changes safely reversed or contained / applicable exercises | 100% tested classes |

### 6.10 Abuse, incident response, resilience and physical roots

| ID | Metric | Calculation | Reference target |
|---|---|---|---|
| NCSM-ABU-01 | Quota/rate/cost control bypass | successful bypasses in authorized tests | 0 |
| NCSM-ABU-02 | Urgent abuse containment time | validated urgent abuse to verified effective containment | service SLO; report p50/p95/max |
| NCSM-IRR-01 | Time to establish command | qualifying alert/report to named incident commander and secure channel | severity-specific objective |
| NCSM-IRR-02 | Time to reliable scope | incident declaration to evidence-backed affected service/tenant/resource set | scenario objective; report uncertainty |
| NCSM-IRR-03 | Time to effective containment | incident declaration to verified isolation/revocation at a reliable boundary | scenario objective |
| NCSM-IRR-04 | Verified closure quality | material incidents closed with evidence, cause, recovery checks, actions and independent review / closed material incidents | 100% |
| NCSM-RES-01 | Restore objective success | exercises meeting RTO/RPO plus identity, integrity and isolation / exercises | 100% critical services |
| NCSM-RES-02 | Protected backup/rebuild-source coverage | critical provider-managed state with required protected backup or known-good source / applicable critical state | 100% |
| NCSM-RES-03 | Known-good rebuild success | rebuilds meeting version, identity, integrity, isolation, data and monitoring criteria / exercises | 100% |
| NCSM-PHY-01 | BMC/root baseline coverage | BMC/OOB devices with owner, inventory, hardened state, patch, access and recovery / devices | 100% |
| NCSM-PHY-02 | Sanitization verification | reassignments/decommissions with successful, method-appropriate sanitation evidence / applicable events | 100%; hard gate before reassignment/disposal |

The machine-readable catalog currently references a stable subset of these metric IDs. Additional IDs in this guide are informative until they are added to a future catalog revision through the governed change process.

## 7. Evidence strength

A strength level helps prioritize review but never replaces a control gate:

| Level | Evidence type | Typical conclusion |
|---:|---|---|
| 0 | no evidence or unsupported assertion | fail or unknown |
| 1 | policy, design statement or interview | intent only |
| 2 | screenshot or manually curated report | directional implementation indication |
| 3 | reproducible API/query/export tied to scope | current implementation and population coverage |
| 4 | protected runtime event, verified attestation or automated reconciliation | operational assertion with integrity/freshness |
| 5 | authorized negative/failure/recovery test independently reproduced | high-confidence effectiveness for the tested scope |

T0 requires evidence appropriate to the exact assertion plus independent verification; “level 5” does not make an incomplete scope conformant.

## 8. Sampling

Use full-population evaluation where feasible for identities, configurations, assignments, public endpoints, deployed artifacts, exceptions, ownership and evidence freshness. Sampling expensive adversarial, destructive or physical tests is acceptable only when:

- the population, strata and selection method are documented;
- all material service/SKU/region/hardware/firmware/driver/mode variants are represented;
- high-risk and recently changed items receive higher probability;
- confidence, blind spots and unsupported populations are reported;
- any failure expands scope and triggers incident or remediation;
- catastrophic boundaries are not inferred solely from convenience samples.

A representative accelerator reset/cleanup test must distinguish hardware model, firmware, driver, virtualization/sharing mode, scheduler path, region, error state and tenant-reassignment workflow.

## 9. Continuous-assurance pipeline

```text
Discover actual state
  → normalize identities, scope and relationships
  → evaluate policy/control assertions
  → collect protected evidence
  → run authorized positive, prohibited-path and failure tests
  → compare desired and actual state
  → independent verifier decision
  → gate, alert, quarantine, contain or record risk decision
  → remediate and re-test
  → publish scoped, time-bound assurance
```

The pipeline must monitor itself: collector/source loss, delay, schema error, conflicting identifiers, permission loss, clock problems, partial test execution, evidence-store integrity, verifier unavailability and denominator change are first-class failures.

## 10. Dashboards and reporting

Do not publish one blended “security percentage.” Use separate views:

- **Executive:** service/profile production decision; failed/unknown/stale T0; critical decisions; customer commitment drift; root/cross-tenant/data/recovery risks; owner and due date.
- **Service owner:** control state, evidence expiry, scope gaps, desired/actual drift, test failures, customer responsibilities and revalidation triggers.
- **Security operations:** required-source health, active exposure, identity/root/fabric/GPU/agent anomalies, detection tests, containment and automation health.
- **Assurance:** evidence scope/strength/freshness/integrity/reproducibility, validator independence, samples, exceptions, failed tests and externally supportable claims.

Use precise statements:

- Good: “All applicable T0 controls for GPU-IaaS service X, regions A/B, release 2026.09, were independently verified as of 2026-09-04; two T1 evidence items expire within 14 days.”
- Bad: “Security is 96% complete.”
- Good: “SKU Y dedicates the host, full GPU, tenant data network and local storage; provider BMC and security telemetry remain shared provider services accessed through JIT controls.”
- Bad: “Fully dedicated and zero trust.”

Every external assurance statement identifies scope, date, version, limitations, failed or untested areas, business-risk decisions and verifier.

## 11. Assurance cadence

| Frequency | Minimum review |
|---|---|
| Continuous | T0 state where feasible, identity/policy, public exposure, allocation drift, required telemetry, root use, backup health, high-impact agent action |
| Daily | failed collectors/tests, unknown/unowned critical state, urgent exposure and containment backlog |
| Weekly | vulnerability SLA, privilege, releases, decisions/exceptions, detection failures and incident actions |
| Monthly | executive gate/risk review, customer commitment drift, denominator/source quality and overdue remediation |
| Quarterly | T0/T1 verification, access review, isolation, revocation/restore, detection replay and applicable agent adversarial tests |
| Semi-annual | T2 verification and major incident/control-plane/recovery exercises |
| Annual | independent T3 architecture/isolation review, regional recovery/rebuild, supplier and cryptographic recovery |
| Material change | immediate re-scope and revalidation of affected assertions |

## 12. Assurance package

A service assurance package includes:

1. service description, profiles, boundary, regions, versions and shared responsibility;
2. applicable controls and production-gate decision;
3. precise host/GPU/cache/NVLink/network/RDMA/storage/telemetry/BMC/support sharing and isolation statement;
4. identity, key, artifact, data/model, logging, incident, backup, deletion and residency summaries;
5. evidence index with scope, freshness, strength, source, integrity and validator;
6. negative-path, failure, revocation, restore/rebuild, sanitization and incident test summary;
7. material findings, unknowns, risk decisions/exceptions, compensating controls, customer impact and remediation dates;
8. independent-review statement and limitations;
9. next verification and invalidation triggers.

## 13. Common measurement failures

- reporting a percentage while an applicable T0 fails;
- turning a business-risk decision into a “pass”;
- dropping unknown or hard-to-measure assets from the denominator;
- treating missing telemetry as zero malicious activity;
- counting scans, policies, tickets or alerts as proof of reduced risk;
- accepting a vendor dashboard, signature or attestation without validating its claim and scope;
- measuring only average response time rather than severity and tail delay;
- allowing the owner, control or agent to self-verify;
- continuing to count stale evidence;
- changing a definition or denominator to improve a trend;
- measuring automation speed without approval, scope, false-completion, stop and rollback outcomes;
- reopening after recovery without independent identity, artifact, data, tenant-isolation and monitoring checks.

## 14. Minimum definition of measurable security

A NeoCloud control is measurably effective only when its applicable scope and owner are known; the mechanism exists in the deployed path; required evidence is current, protected and reproducible; prohibited paths and failure behavior are tested where relevant; an independent validator can reproduce the assertion; failure produces an explicit operational response; and the control is revalidated after expiry or material change.
