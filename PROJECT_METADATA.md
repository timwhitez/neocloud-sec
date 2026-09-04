# GitHub Project Metadata / GitHub 项目元数据

**Version / 版本:** 1.0.0-draft.2  
**Synchronization / 同步方式:** manual / 手工同步

The canonical intended metadata is [`.github/repository-metadata.json`](.github/repository-metadata.json). GitHub does not automatically consume that file. It records the reviewed intent and enables drift checks; an owner must apply the values in repository settings or with GitHub CLI/API.

规范元数据保存在 [`.github/repository-metadata.json`](.github/repository-metadata.json)。GitHub 不会自动读取该文件；它用于记录已审阅意图和检查漂移，仍需 Owner 在仓库设置或 GitHub CLI/API 中应用。

## Recommended description / 推荐描述

> Vendor-neutral bilingual cybersecurity baseline and implementation guide for NeoCloud and GPU cloud platforms, covering GPU/RDMA isolation, Kubernetes/Slurm, AI agents, evidence, assurance, and a 0–24 month roadmap.

This wording deliberately describes a bilingual baseline and guide, not a deployed product, adopted standard, or certification.

## Recommended topics / 推荐 Topics

```text
neocloud, gpu-cloud, cloud-security, cybersecurity, ai-security, agent-security, kubernetes-security, slurm, hpc-security, gpu-security, rdma, infiniband, zero-trust, security-baseline, security-architecture, supply-chain-security, incident-response, threat-modeling, continuous-assurance, devsecops
```

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
- Enable private vulnerability reporting or another documented private channel.
- Keep Wiki and Discussions disabled until there is a clear moderation/maintenance owner.
- Do not enable Pages until the generated site has versioning, link validation, and release ownership.

## Apply with GitHub CLI / 使用 GitHub CLI 应用

Run only after reviewing the intended values:

```bash
gh repo edit timwhitez/neocloud-sec \
  --description 'Vendor-neutral bilingual cybersecurity baseline and implementation guide for NeoCloud and GPU cloud platforms, covering GPU/RDMA isolation, Kubernetes/Slurm, AI agents, evidence, assurance, and a 0–24 month roadmap.' \
  --add-topic neocloud \
  --add-topic gpu-cloud \
  --add-topic cloud-security \
  --add-topic cybersecurity \
  --add-topic ai-security \
  --add-topic agent-security \
  --add-topic kubernetes-security \
  --add-topic slurm \
  --add-topic hpc-security \
  --add-topic gpu-security \
  --add-topic rdma \
  --add-topic infiniband \
  --add-topic zero-trust \
  --add-topic security-baseline \
  --add-topic security-architecture \
  --add-topic supply-chain-security \
  --add-topic incident-response \
  --add-topic threat-modeling \
  --add-topic continuous-assurance \
  --add-topic devsecops
```

Keep `homepage` unset until a documentation URL is ready. A metadata file does not prove that the GitHub sidebar settings were applied; compare them during each release.
