# GitHub Project Metadata / GitHub 项目元数据

**Version / 版本:** 1.0.0-draft.2  
**Synchronization / 同步方式:** manual / 手工同步

The canonical intended metadata is [`.github/repository-metadata.json`](.github/repository-metadata.json). GitHub does not automatically consume that file. It records the reviewed intent and enables drift checks; an owner must apply the values in repository settings or with GitHub CLI/API.

规范元数据保存在 [`.github/repository-metadata.json`](.github/repository-metadata.json)。GitHub 不会自动读取该文件；它用于记录已审阅意图和检查漂移，仍需 Owner 在仓库设置或 GitHub CLI/API 中应用。

## Recommended description / 推荐描述

> Vendor-neutral bilingual security baseline and implementation guide for NeoCloud/GPU clouds: GPU/RDMA isolation, Kubernetes/Slurm, AI agents, and continuous assurance.

This wording is deliberately short enough for the GitHub About area and describes a bilingual baseline and guide—not a deployed product, adopted standard, or certification.

## Recommended topics / 推荐 Topics

```text
neocloud, gpu-cloud, cloud-security, cybersecurity, ai-security, agent-security, kubernetes-security, slurm, hpc-security, gpu-security, rdma, infiniband, zero-trust, security-baseline, security-architecture, supply-chain-security, incident-response, threat-modeling, continuous-assurance, devsecops
```

The list uses GitHub's maximum of 20 topics. Topic names are always public, including topics attached to a private repository. Apply them only after confirming that this taxonomy itself is safe to disclose.

该列表使用 GitHub 允许的最多 20 个 Topics。Topic 名称即使添加到 Private Repository 也始终公开，因此只有在确认这组分类本身可以披露后才应应用。

## Homepage / 主页

Leave the homepage empty until a maintained documentation site or versioned release page exists. Do not point it at an unrelated personal site.

在存在持续维护的文档站或版本化 Release 页面前保持为空，不要指向无关个人站点。

## License and visibility / License 与可见性

The repository is currently private and no license has been selected. Do not describe it as open source or openly licensed. Before changing visibility to public, select an owner-approved license that addresses documentation, JSON control data, scripts, contributions, third-party quotation, and trademarks.

当前仓库为 Private 且尚未选择 License，不应描述为 Open Source 或 Openly Licensed。转为 Public 前应选择由 Owner 批准、覆盖文档、JSON 控制数据、脚本、贡献、第三方引用与 Trademark 的 License。

## Recommended repository settings / 推荐设置

- Keep `main` protected; require Pull Request and repository validation.
- Require review-conversation resolution and block force pushes.
- Prefer squash merge; delete branches after merge.
- While the repository is private, use an existing trusted private maintainer channel for sensitive reports.
- When the repository becomes public, enable GitHub Private Vulnerability Reporting if supported and document the resulting `Report a vulnerability` path.
- Keep Wiki and Discussions disabled until there is a clear moderation and maintenance owner.
- Do not enable Pages until the generated site has versioning, link validation, and release ownership.

## Apply with GitHub CLI/API / 使用 GitHub CLI/API 应用

Run only after reviewing the intended values and confirming that the public topic taxonomy is acceptable:

```bash
gh repo edit timwhitez/neocloud-sec \
  --description 'Vendor-neutral bilingual security baseline and implementation guide for NeoCloud/GPU clouds: GPU/RDMA isolation, Kubernetes/Slurm, AI agents, and continuous assurance.'

gh api --method PUT repos/timwhitez/neocloud-sec/topics --input - <<'JSON'
{
  "names": [
    "neocloud",
    "gpu-cloud",
    "cloud-security",
    "cybersecurity",
    "ai-security",
    "agent-security",
    "kubernetes-security",
    "slurm",
    "hpc-security",
    "gpu-security",
    "rdma",
    "infiniband",
    "zero-trust",
    "security-baseline",
    "security-architecture",
    "supply-chain-security",
    "incident-response",
    "threat-modeling",
    "continuous-assurance",
    "devsecops"
  ]
}
JSON
```

The topics call replaces the complete topic set rather than only appending values. Keep `homepage` unset until a documentation URL is ready. A metadata file does not prove that the GitHub sidebar settings were applied; compare actual repository metadata during each release.
