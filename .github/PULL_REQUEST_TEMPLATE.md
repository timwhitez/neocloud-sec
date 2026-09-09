## Summary

Describe the problem and outcome, not activity alone. Link the existing Issue; create a new Issue only when separate tracking is useful.

## Change type

- [ ] Factual or editorial correction
- [ ] Translation/parity correction
- [ ] Normative control change
- [ ] Evidence, verification, or metric change
- [ ] Template or tooling change
- [ ] Repository governance or release change

## Scope and impact

- Affected control IDs/domains:
- Affected service profiles and provider/customer/shared responsibilities:
- Canonical documents, implementation and tests changed:
- Compatibility or migration impact:
- T0 gate, control-ID, tier, schema or version impact (state unchanged where applicable):

## Evidence and sources

List primary sources with publication/revision/access dates, exact product/version/configuration, status and retrieval limitations. Distinguish final, draft, public review, superseded and vendor-specific sources. Identify corroborating primary evidence and unresolved conflicts. Separate project-authored recommendations from source requirements and deployed evidence.

For recurring research, follow [CONTRIBUTING](../CONTRIBUTING.md#recurring-research) and complete this section in the PR, not in a separate weekly report:

- Base commit; timezone; calendar-week boundaries; evidence cutoff:
- New publications/revisions versus older lookback findings and future deadlines:
- Cross-domain dispositions: actionable change / already covered / watch / out of scope, with reasons:
- Useful gap and smallest practical fix; unnecessary complexity deliberately avoided:
- Sources/decisions preserved when removing redundant material:
- Next watch items and revalidation triggers:

## Verification

- [ ] I ran `python3 scripts/check_local.py` from a complete checkout of the final candidate.
- [ ] Relevant additional checks passed; exact commands, input scope, output and omissions are recorded below.
- [ ] English and Chinese normative meaning remain aligned.
- [ ] Catalog, baseline tables, templates, metrics, references, versions and changelog are consistent where affected.
- [ ] Changed relative links resolve; retired documents have no active navigation links.
- [ ] Claims distinguish documentation, valid metadata, implementation and independent verification.
- [ ] T0 failures cannot be hidden by exceptions or aggregate scores; high-impact automation cannot approve or verify itself.
- [ ] No Actions dispatch/rerun, force push or branch-rule bypass occurred; commit/merge messages retain `[skip ci]` while quota is constrained.

Exact tested head and environment:

```text
paste commands, exit codes and outputs; identify unavailable or failed checks
```

A partial checkout, historical test result or metadata PASS is not a full-suite pass or infrastructure security assessment. Leave the PR unmerged when a required gate is unavailable or fails.

## Review and delivery

- Reviewer or separate review method (do not imply independent assurance from self-review):
- Exact commit reviewed; findings and resolutions:
- Remaining uncertainty/residual risk:
- Issue/PR status; merged changes or unmerged reasons:
- Base/head rechecked before merge; resulting main commit verified afterward:

## Security and disclosure

- [ ] No live credentials, customer data, private evidence, exploitable production detail or uncoordinated third-party vulnerability is included.
- [ ] Sensitive issues follow `SECURITY.md`, not a public Issue or PR.
