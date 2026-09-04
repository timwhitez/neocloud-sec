# Security Policy / 安全报告规则

## Supported content

Security reports may concern:

- a live credential, customer data, private infrastructure detail, or other sensitive material accidentally committed to this repository;
- a repository workflow or script vulnerability;
- a control or implementation recommendation that could predictably create a serious security failure when followed;
- a coordinated vulnerability affecting a referenced NeoCloud implementation, when the repository owner is an appropriate coordination party.

Documentation disagreements, ordinary corrections, and non-sensitive gaps should use an issue or pull request.

## Private reporting

Do **not** open a public issue containing a credential, customer data, exploit details for a live system, private topology, or an uncoordinated third-party vulnerability.

Use GitHub private vulnerability reporting / **Report a vulnerability** when it is enabled for this repository. If it is not enabled, use an existing trusted private channel to the repository owner. This document intentionally does not invent an email address or response SLA.

Include only what is necessary:

- affected repository path, control ID, version, or commit;
- impact and realistic preconditions;
- a safe reproduction or minimal evidence;
- whether a live service or third party is affected;
- suggested containment and disclosure constraints.

Redact secrets and personal/customer data. Do not perform active testing against systems without explicit authorization.

## Response expectations

The project may acknowledge, triage, correct documentation, revoke content, or coordinate disclosure depending on scope. No fixed response or remediation SLA is promised in this draft. A repository change or passing CI does not by itself prove that a production vulnerability is remediated.

## 中文摘要

禁止在 Public Issue 中提交真实 Credential、客户数据、生产拓扑、可直接利用细节或未协调披露的第三方漏洞。优先使用 GitHub Private Vulnerability Reporting；如果仓库未启用该能力，则使用已建立的可信私密渠道联系 Owner。报告应包含受影响 Path/Control/Version、影响、必要前提、安全复现和建议隔离，且必须脱敏。未经明确授权不得对真实系统做主动测试。
