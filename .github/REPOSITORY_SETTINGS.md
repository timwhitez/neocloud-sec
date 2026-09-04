# Recommended GitHub Repository Settings / GitHub 仓库设置建议

**Audit snapshot:** 2026-09-04  
**Repository:** `timwhitez/neocloud-sec`

This file records reviewed metadata and repository safeguards. It is documentation only: GitHub **About**, visibility, topics, rulesets, security settings, merge settings, and license status must be configured by an authorized repository administrator.

本文件记录经审阅的项目元数据与仓库防护建议。它不会自动修改 GitHub **About**、可见性、Topics、Ruleset、安全设置、Merge 设置或 License；这些项目必须由有权限的仓库管理员应用。

## 1. About description / 项目描述

Recommended description:

> Vendor-neutral bilingual security baseline and implementation guide for NeoCloud/GPU clouds: GPU/RDMA isolation, Kubernetes/Slurm, AI agents, and continuous assurance.

The wording is intentionally compact and describes a baseline and implementation guide—not a deployed product, adopted standard, certification, or guarantee.

建议中文释义：

> 面向 NeoCloud/GPU 云的厂商中立中英双语安全基线与实施指南，覆盖 GPU/RDMA 隔离、Kubernetes/Slurm、AI Agent 与持续证明。

## 2. Topics / Topics 建议

Use a focused set:

```text
neocloud
gpu-cloud
cloud-security
ai-security
agent-security
hpc-security
gpu-security
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

GitHub permits at most 20 topics. **Topic names are always public, even when attached to a private repository.** Apply this taxonomy only after confirming it is safe to disclose. Avoid product-vendor topics unless the project becomes implementation-specific, and avoid standalone `compliance`, `certification`, or `standard` claims while this remains a project-authored draft.

GitHub 最多允许 20 个 Topics。**即使仓库是 Private，Topic 名称仍始终公开。** 因此只有在确认该分类信息可披露后才应应用。

## 3. Homepage and social preview / 主页与社交预览

- Leave **Homepage** empty until a maintained documentation site or versioned release page exists.
- Do not point it at an unrelated personal site.
- Consider a restrained social preview only after the project name, license, and publication status are final; use “security baseline and implementation guide,” not “certified” or “complete protection.”

## 4. Visibility and publication / 可见性与发布

At the audit snapshot the repository is private. Before making it public:

1. choose and add an explicit license;
2. remove private evidence, credentials, customer names, internal topology, and non-redistributable material;
3. verify README, scope, security policy, contribution policy, references, and release status;
4. run `python3 scripts/validate_repository.py` on the exact publication commit;
5. obtain independent review of material normative changes;
6. create an attributable release/tag and retain its review result;
7. after public release, enable GitHub Private Vulnerability Reporting if supported and document the resulting `Report a vulnerability` path.

Researcher-facing GitHub Private Vulnerability Reporting is not a substitute for a reporting path while this repository is private. Until public release, use an already established trusted private maintainer channel and do not invent an email address or SLA.

## 5. License decision / License 决策

No open-source license is currently granted. A readable or public repository does not itself grant ordinary open-source reuse rights.

Options requiring an explicit owner/legal decision include:

- **Single license:** Apache License 2.0 for the repository, after confirming it is appropriate for both code and documentation.
- **Dual license:** Apache License 2.0 for scripts, schemas, structured catalogs, and templates; Creative Commons Attribution 4.0 for prose and diagrams, with precise file-scope notices.
- **Restricted draft:** retain all rights while private and decide at publication time.

This document does not select a license. Third-party quotation, trademarks, contribution terms, and mixed code/documentation scope must be reviewed before publication.

## 6. Default-branch protection / 默认分支保护

Recommended ruleset for `main`:

- require a pull request before merge;
- require at least one approving review for normative or executable changes;
- require review-conversation resolution;
- require the `Repository contract` status check;
- require the branch to be current before merge where practical;
- block force pushes and branch deletion;
- restrict and audit bypass;
- prefer squash merge and delete merged head branches;
- require signed commits only when the contributor workflow can support it without unsafe workarounds.

For a single-maintainer project, independent review may be supplied by a named external reviewer or a documented separate review pass. Do not weaken protection merely to make a release appear reviewed.

## 7. Repository features / 仓库功能

| Feature | Recommendation | Reason |
|---|---|---|
| Issues | Enabled | factual corrections, control proposals, implementation feedback |
| Pull requests | Enabled | attributable and reviewable change |
| Projects | Enable only when actively used | avoid empty process surfaces |
| Discussions | Optional after public release | longer design discussions with a moderation owner |
| Wiki | Disabled unless actively maintained | preserve one source of truth |
| Private vulnerability reporting | Enable after public release if supported | confidential researcher intake on a public repository |
| Dependabot/security updates | Enable if executable dependencies are added | the current validator uses only the Python standard library |
| Auto-delete head branches | Enabled | reduce stale branches after squash merge |

## 8. Apply metadata / 应用元数据

Run only after reviewing the values and confirming that public topic names are acceptable:

```bash
gh repo edit timwhitez/neocloud-sec \
  --description 'Vendor-neutral bilingual security baseline and implementation guide for NeoCloud/GPU clouds: GPU/RDMA isolation, Kubernetes/Slurm, AI agents, and continuous assurance.'

gh api --method PUT repos/timwhitez/neocloud-sec/topics --input - <<'JSON'
{
  "names": [
    "neocloud",
    "gpu-cloud",
    "cloud-security",
    "ai-security",
    "agent-security",
    "hpc-security",
    "gpu-security",
    "kubernetes-security",
    "slurm",
    "rdma",
    "infiniband",
    "zero-trust",
    "confidential-computing",
    "software-supply-chain",
    "security-baseline",
    "reference-architecture",
    "continuous-assurance",
    "bilingual"
  ]
}
JSON
```

The topics call replaces the complete topic set. Keep `homepage` unset until a maintained documentation URL exists.

## 9. Release checklist / 发布检查

A release is ready only when:

- the exact catalog and both baseline documents pass repository validation;
- source status distinguishes final, draft, public-review, living-project, vendor, and research material;
- externally stated counts, versions, dates, and guarantees are reproducible;
- the release does not claim deployed-product, formal-standard, certification, community-consensus, open-license, or public status unless true;
- material normative changes received independent review;
- limitations and unresolved uncertainty are explicit;
- actual GitHub About, topics, visibility, license, security reporting, merge settings, and branch protection match the release documentation.
