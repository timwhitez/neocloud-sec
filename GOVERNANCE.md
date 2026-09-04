# Governance / 治理规则

## 1. Purpose

NeoCloud Cyber Security is maintained as an evidence-driven security baseline. Changes must improve a defined security outcome, remain implementable, and avoid creating compliance theatre.

NeoCloud Cyber Security 以可验证结果为核心。任何变更都必须改善明确的安全结果、能够落地，并避免把“写了制度”误当作“控制有效”。

## 2. Authority hierarchy

When requirements conflict, use the following order:

1. Applicable law, regulator, contract, or customer commitment.
2. Explicit service boundary and applicability decisions approved by accountable owners.
3. T0 production guardrails for the in-scope service.
4. Service-specific threat models and shared-responsibility decisions.
5. Explicit residual-risk decisions for T1–T4 and explicitly nonconformant emergency deviations.
6. Informative framework mappings.

A risk decision may authorize a time-bounded operational deviation, but it cannot relabel a failed or unknown T0 as `PASS`, `VERIFIED`, or baseline-conformant. A mapping to an external framework never proves compliance by itself.

## 3. Change process

Every material control change should be proposed through a pull request containing:

- problem statement and affected threat;
- affected service profiles and trust boundaries;
- proposed control text and implementation guidance;
- minimum evidence and verification method;
- migration and backward-compatibility impact;
- source references and known limitations;
- independent reviewer findings.

Breaking control-ID changes require a major version. New backward-compatible controls require a minor version. Editorial clarification uses a patch version.

## 4. Control and assessment states

Assessment work follows an explicit state machine:

`PROPOSED → READY → IMPLEMENTED → CANDIDATE_DONE → VERIFIED`

- **PROPOSED:** the item exists but scope, owner, or evidence requirements may be incomplete.
- **READY:** scope, owner, target date, test method, and dependencies are defined.
- **IMPLEMENTED:** the control is deployed, but effectiveness has not yet been independently established.
- **CANDIDATE_DONE:** implementation evidence is collected and the owner asserts completion.
- **VERIFIED:** an independent validator has returned `PASS` against the defined scope and evidence.

Only an independent validator `PASS` may promote `CANDIDATE_DONE` to `VERIFIED`. Failed or stale evidence returns the item to the appropriate earlier state. “Configured” is not synonymous with “effective.”

## 5. Evidence rules

Evidence must be:

- attributable to a control, asset scope, tenant/service boundary, owner, and observation time;
- reproducible or independently inspectable;
- protected from unauthorized alteration;
- no older than the control's evidence-freshness requirement;
- explicit about sampling, exclusions, blind spots, and exceptions;
- retained according to contractual, privacy, forensic, and legal requirements.

Screenshots alone are weak evidence. Prefer API exports, signed attestations, immutable audit events, policy evaluation results, test records, and configuration snapshots with cryptographic hashes.

## 6. Risk acceptance and exceptions

A T0 failure or unknown state cannot receive a conforming exception. An accountable executive and security owner may approve a time-bounded **emergency deviation** with compensating controls, customer/legal impact analysis, explicit nonconformant status, rollback conditions, and a remediation deadline. The affected control remains failed or unverified until an independent validator returns `PASS`.

All deviations and other exceptions require an owner, reason, affected assets/tenants, residual risk, compensating controls, approval, expiration date, customer-facing claim treatment, and verification after closure. They must never silently become permanent architecture.

## 7. Agent and automation safety

AI or automated security actions must satisfy all of the following:

- a declared goal, a policy-controlled authorization envelope that the agent or untrusted content cannot expand, and an authorized tool set;
- least privilege and short-lived credentials;
- policy gates for destructive, external, customer-impacting, or irreversible actions;
- complete action/observation/evidence audit trails;
- deterministic stop conditions and budget limits;
- rollback or containment plans;
- independent validation before declaring success.

Active security testing requires explicit authorization, least privilege, an approved target scope, isolation/sandboxing where possible, and an approval path. External or untrusted content must not directly change goals, scope, hooks, skills, policy, or tool permissions. A planning component may create or revise a roadmap but must not silently execute active tests.

## 8. Review cadence

- T0: continuous monitoring where feasible, independent verification at least quarterly, and review after material architecture or threat change.
- T1: at least quarterly and after material change.
- T2: at least semi-annually and after material change.
- T3: control-owner review at least semi-annually, independent assessment at least annually, and review after material change.
- T4 automation: continuous telemetry plus quarterly adversarial/failure-mode review and review after material change.
- Full baseline: annual version review or earlier when a major standard, platform, accelerator, isolation mechanism, or threat class changes.

## 9. Maintainer principles

The project follows first-principles security and the “bitter lesson” for automation: favor general, scalable mechanisms—identity, policy, evidence, isolation, feedback, and verification—over brittle one-off rules. Complexity must earn its operational cost.
