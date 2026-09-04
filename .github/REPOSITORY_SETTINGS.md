# Recommended GitHub Repository Settings / GitHub 仓库设置建议

**Audit snapshot:** 2026-09-04  
**Repository:** `timwhitez/neocloud-sec`

This file records the intended public-facing metadata and repository safeguards. It is documentation only: GitHub's **About**, visibility, topics, rulesets, security settings, and license status must be configured in repository settings or by an authorized repository-administration API.

本文件记录建议的项目展示信息与仓库防护。它本身不会自动修改 GitHub 的 **About**、可见性、Topics、Ruleset、安全设置或 License；这些内容需要由具备仓库管理权限的人员在 Settings 中配置。

## 1. About description / 项目描述

Recommended primary description:

> Vendor-neutral NeoCloud/GPU-cloud security baseline, reference architecture, roadmap, and implementation guide for multi-tenant accelerators, Kubernetes/Slurm, RDMA/InfiniBand, AI models and agents, supply chain, resilience, and continuous assurance. English / 简体中文.

More compact alternative:

> Vendor-neutral security baseline, reference architecture, roadmap, and practice guide for NeoCloud/GPU-cloud infrastructure, AI models, and agents. English / 简体中文.

The description deliberately calls the repository a **baseline and reference framework**, not a deployable “security control plane.”

建议主描述：

> 面向 NeoCloud/GPU 云的厂商中立安全基线、参考架构、路线图与实践指南，覆盖多租户加速器、Kubernetes/Slurm、RDMA/InfiniBand、AI 模型与 Agent、供应链、韧性和持续证明。中英双语。

## 2. Topics / Topics 建议

Use a focused set rather than the maximum number of tags:

```text
neocloud
gpu-cloud
cloud-security
ai-security
agent-security
hpc-security
kubernetes-security
slurm
rdma
infiniband
zero-trust
confidential-computing
software-supply-chain
security-baseline
reference-architecture
continuous-assurance
bilingual
```

Avoid product-vendor topics unless the repository becomes implementation-specific. Avoid `compliance`, `certification`, or `standard` as standalone claims while this remains a project-authored draft.

## 3. Homepage and social preview / 主页与社交预览

- Leave **Homepage** empty until a maintained documentation site or release page exists; do not point it at an unrelated personal site.
- After the repository is public, consider a small static documentation site generated from the bilingual Markdown.
- Add a restrained social-preview image only after the project name, license, and publication status are final. It should say “Security baseline and reference architecture,” not “certified” or “complete protection.”

## 4. Visibility and publication status / 可见性与发布状态

At the audit snapshot, the repository is private while earlier content described itself as a “public draft.” The documents now use **implementation-oriented draft** so the statement remains true regardless of visibility.

Before changing visibility to public:

1. choose and add an explicit license;
2. remove any private evidence, credentials, customer names, internal topology, or non-redistributable source material;
3. enable private vulnerability reporting where available;
4. verify README, security policy, contribution policy, references, and release status;
5. run `python3 scripts/validate_repository.py` on the exact publication commit;
6. create a signed or otherwise attributable release/tag and retain the review result.

## 5. License decision / License 决策

No open-source license is currently granted. Until a `LICENSE` file is added, external users do not receive normal open-source reuse rights merely because they can read the repository.

Recommended options for an explicit owner decision:

- **Simple:** Apache License 2.0 for the entire repository.
- **Dual license:** Apache License 2.0 for scripts, schemas, structured catalogs, and templates; Creative Commons Attribution 4.0 for prose documentation and diagrams.
- **Restricted draft:** keep all rights reserved while the repository remains private, then make a release-time license decision.

Dual licensing is often clearer for mixed code/documentation repositories, but it requires precise file-scope notices. The repository owner should make this legal decision; contributors and automation must not infer a license.

## 6. Default-branch protection / 默认分支保护

Recommended ruleset for `main`:

- require a pull request before merge;
- require at least one approving review for normative or executable changes;
- require conversation resolution;
- require the `Repository contract` status check;
- require the branch to be up to date before merge where practical;
- block force pushes and branch deletion;
- restrict bypass to an explicit emergency role and audit every bypass;
- use squash merge for ordinary changes and delete merged head branches;
- require signed commits only if the contributor workflow can support it without encouraging unsafe workarounds.

For a single-maintainer repository, independent review may be supplied by a named external reviewer or a documented, separate review pass; branch protection should not be weakened silently to make a release appear reviewed.

## 7. Repository features / 仓库功能

Recommended state:

| Feature | Recommendation | Reason |
|---|---|---|
| Issues | Enabled | factual corrections, control proposals, and implementation feedback |
| Pull requests | Enabled | reviewable, attributable changes |
| Discussions | Optional after public release | longer design debate that should not block concrete fixes |
| Wiki | Disabled unless actively maintained | avoid two competing sources of truth |
| Projects | Enable only when used | avoid empty process surfaces |
| Private vulnerability reporting | Enable before public release | confidential intake for repository vulnerabilities or leaked secrets |
| Dependabot/security updates | Enable if executable dependencies are added | current validator is standard-library only |
| Auto-delete head branches | Enabled | reduce stale branches after squash merge |

## 8. Pull-request and issue governance / PR 与 Issue 治理

The repository includes:

- [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) for normative, bilingual, evidence-aware review;
- issue forms for factual corrections and control changes;
- [`CODEOWNERS`](CODEOWNERS) for explicit default ownership;
- [`../SECURITY.md`](../SECURITY.md) for confidential reporting;
- [`../GOVERNANCE.md`](../GOVERNANCE.md) for control state, evidence, exceptions, and release decisions.

## 9. Release checklist / 发布检查

A release is ready only when:

- the exact catalog and both baseline documents pass repository validation;
- current references distinguish final, draft, public-review, and superseded sources;
- every externally stated count, version, status, and guarantee is reproducible;
- the release does not call itself a deployable product, formal standard, certification, community consensus, or public artifact unless that claim is actually true;
- material normative changes received independent review;
- the release notes state limitations and any unresolved factual uncertainty;
- GitHub About, topics, visibility, license, and branch protection match the release documentation.
