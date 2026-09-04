# Security Policy / 安全问题报告

## Supported content / 支持范围

The current `main` branch is the only supported version of this repository. The project primarily contains documentation, structured control data, templates, a Python validator, and GitHub Actions configuration.

本仓库仅支持当前 `main` 分支。项目主要包含文档、结构化控制数据、模板、Python 校验器和 GitHub Actions 配置。

Security-sensitive reports may include:

- code execution, command injection, path traversal, or unsafe parsing in repository scripts;
- workflow or dependency behavior that could compromise repository contents, credentials, or contributors;
- a committed live credential, customer data, private evidence, or other sensitive information;
- a method to bypass integrity, validation, or review controls in a way that would materially mislead users;
- a vulnerability in an implementation example that could create unsafe production behavior when followed as written.

The following are normally **not** confidential vulnerability reports and should use a regular issue or pull request:

- factual corrections, terminology improvements, missing references, broken links, translation drift, control-design debate, and non-sensitive implementation suggestions;
- vulnerabilities in third-party products or NeoCloud providers that are not caused by this repository;
- requests for legal, compliance, certification, or product-security guarantees.

安全敏感报告可以包括：仓库脚本中的代码执行、命令注入、路径穿越或不安全解析；可能危害仓库、凭据或贡献者的 Workflow/Dependency 行为；误提交的真实密钥、客户数据或私密证据；能够实质绕过完整性、校验或 Review 的方法；以及按文档实施会直接形成高风险生产漏洞的错误示例。

普通事实修正、术语、缺失引用、失效链接、翻译漂移、控制设计讨论和非敏感实施建议，应通过普通 Issue 或 Pull Request 提交。

## How to report privately / 如何私密报告

1. Use GitHub's private vulnerability-reporting or Security Advisory function for this repository when it is available.
2. If that function is unavailable, contact repository owner [`@timwhitez`](https://github.com/timwhitez) through a private channel listed on the GitHub profile.
3. Do **not** open a public issue containing a live secret, customer information, exploitable production detail, or uncoordinated third-party vulnerability.
4. Include the affected path and revision, impact, prerequisites, minimal reproduction, evidence, and any suggested containment. Use synthetic data and redact secrets.

优先使用仓库的 GitHub Private Vulnerability Reporting 或 Security Advisory。若该能力不可用，请通过 [`@timwhitez`](https://github.com/timwhitez) GitHub 主页列出的私密渠道联系。不要在公开 Issue 中提交真实 Secret、客户信息、可直接利用的生产细节或未经协调的第三方漏洞。报告应包含受影响路径与版本、影响、前置条件、最小复现、证据和建议隔离措施，并使用合成数据、删除敏感信息。

## Handling expectations / 处理原则

The maintainer will triage reports according to impact and available capacity. A report may be closed or redirected when it concerns a third-party system, duplicates a known issue, lacks enough information to reproduce, or is better treated as a normal factual correction. No response-time, remediation-time, bounty, safe-harbor, or disclosure guarantee is made by this draft policy.

维护者会按影响与可用资源分诊。若问题属于第三方系统、与已知问题重复、信息不足以复现，或更适合作为普通事实修正，报告可能被关闭或转移。本草案不承诺响应时限、修复时限、奖金、安全港或披露时间。

## Coordinated disclosure / 协调披露

Do not test systems, tenants, data, or infrastructure without explicit authorization. The existence of this repository does not authorize active testing of any provider or customer environment. Public disclosure should occur only after sensitive material is removed and affected parties have had a reasonable opportunity to assess and contain the issue.

未经明确授权，不得测试任何系统、租户、数据或基础设施。本仓库的存在不构成对任何服务商或客户环境进行主动测试的授权。公开披露前应移除敏感材料，并给受影响方合理的评估与隔离机会。
