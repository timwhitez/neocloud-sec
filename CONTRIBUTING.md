# Contributing / 贡献指南

Contributions are welcome when they make NeoCloud security more accurate, implementable, measurable, or easier to verify.

## Contribution requirements

A pull request that changes normative content should include:

1. The threat, failure mode, or operating problem being addressed.
2. Affected domains, controls, service profiles, and responsibility owners.
3. Implementation guidance that does not depend on a single vendor unless the control is explicitly vendor-specific.
4. Minimum evidence, a verification method, and expected evidence freshness.
5. Compatibility impact and migration notes.
6. Primary or authoritative sources.
7. A self-review and an independent review summary.

Do not copy proprietary standard text. Summarize outcomes and link to the authoritative source.

## Local and CI validation

Run the repository contract locally before review:

```bash
python3 scripts/validate_repository.py
```

The validator checks catalog structure, exact control IDs/counts/tier distribution, bilingual baseline parity, cross-references, release versions, required deliverables—including the intended repository-metadata file—and relative Markdown links. GitHub Actions runs the same validator for pull requests and `main`; local success does not replace independent review, and CI success does not prove the substantive correctness of a security claim. Mermaid diagrams should also be visually reviewed in GitHub Markdown.

## Writing style

- Use direct, testable language: **must** for requirements, **should** for strong recommendations, and **may** for options.
- Separate provider, customer, and shared responsibilities.
- State assumptions and applicability.
- Avoid product marketing, fear-based language, unsupported maturity claims, and absolute guarantees.
- Keep English and Chinese normative meaning aligned; literal translation is less important than semantic equivalence.

## Security-sensitive contributions

Do not open an issue containing a live credential, customer data, exploitable production detail, or uncoordinated vulnerability. Follow [`SECURITY.md`](SECURITY.md), use an existing trusted private maintainer channel while this repository is private, and redact evidence before committing it.

## 中文摘要

规范性修改必须说明威胁、适用范围、责任方、实现方式、最小证据、验证方法、兼容性与权威来源。禁止把专有标准正文直接复制进仓库；禁止在 Issue 中提交真实密钥、客户数据和未协调披露的生产漏洞。提交前运行 `python3 scripts/validate_repository.py`，Pull Request 还会执行相同 CI；只有独立验证返回 `PASS` 后才能宣称控制已完成。当前 Private 状态下，敏感问题应通过已有的可信私密渠道报告。
