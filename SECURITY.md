# Security Policy / 安全问题报告

## Supported content / 支持范围

The current `main` branch is the only supported version of this repository. The project primarily contains documentation, structured control data, templates, a Python validator, and GitHub Actions configuration.

本仓库仅支持当前 `main` 分支。项目主要包含文档、结构化控制数据、模板、Python 校验器和 GitHub Actions 配置。

Security-sensitive reports may include:

- code execution, command injection, path traversal, or unsafe parsing in repository scripts;
- workflow or dependency behavior that could compromise repository contents, credentials, or contributors;
- a committed live credential, customer data, private evidence, or other sensitive information;
- a method to bypass integrity, validation, or review controls in a way that would materially mislead users;
- an implementation instruction that could predictably create serious unsafe production behavior when followed as written.

The following are normally **not** confidential vulnerability reports and should use a regular issue or pull request:

- factual corrections, terminology improvements, missing references, broken links, translation drift, control-design debate, and non-sensitive implementation suggestions;
- vulnerabilities in third-party products or NeoCloud providers that are not caused by this repository;
- requests for legal, compliance, certification, or product-security guarantees.

## How to report privately / 如何私密报告

Do **not** open an issue containing a live secret, customer information, exploitable production detail, private topology, or an uncoordinated third-party vulnerability.

This repository is currently private. Use an **already established trusted private channel** to the repository owner or maintainers. This policy intentionally does not invent an email address, contact mechanism, safe-harbor promise, or response SLA.

If the repository is later made public and GitHub Private Vulnerability Reporting is supported and enabled, use the repository's **Report a vulnerability** path.

Include only what is necessary:

- affected path, control ID, revision, or version;
- impact and realistic prerequisites;
- safe minimal reproduction or evidence;
- whether a live service or third party is affected;
- suggested containment and disclosure constraints.

Use synthetic data and redact credentials, personal information, customer data, and private infrastructure details. Do not actively test systems, tenants, data, or infrastructure without explicit authorization.

当前仓库是 Private。敏感问题应通过已经建立的可信私密渠道联系 Owner 或 Maintainer；本文不会虚构 Email、联系方式、安全港承诺或响应 SLA。仓库未来转为 Public 且启用 GitHub Private Vulnerability Reporting 后，再使用 **Report a vulnerability** 路径。禁止在 Issue 中提交真实 Secret、客户数据、生产拓扑、可直接利用细节或未协调披露的第三方漏洞。

## Handling expectations / 处理原则

The maintainer will triage reports according to impact and available capacity. A report may be closed or redirected when it concerns a third-party system, duplicates a known issue, lacks enough information to reproduce, or is better treated as a normal factual correction. No response-time, remediation-time, bounty, safe-harbor, or disclosure guarantee is made by this draft policy.

维护者会按影响与可用资源分诊。若问题属于第三方系统、与已知问题重复、信息不足以复现，或更适合作为普通事实修正，报告可能被关闭或转移。本草案不承诺响应时限、修复时限、奖金、安全港或披露时间。

## Coordinated disclosure / 协调披露

The existence of this repository does not authorize testing of any provider or customer environment. Public disclosure should occur only after sensitive material is removed and affected parties have had a reasonable opportunity to assess and contain the issue. A repository edit or passing structural CI does not itself prove that a production vulnerability has been remediated.

本仓库的存在不构成对任何服务商或客户环境进行主动测试的授权。公开披露前应移除敏感材料，并给受影响方合理的评估与隔离机会。仓库修改或结构校验通过本身不能证明生产漏洞已经修复。
