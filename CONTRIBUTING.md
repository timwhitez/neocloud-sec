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

## Local validation

This repository intentionally does not require a GitHub Actions workflow. Run the checks locally before review:

```bash
python -m json.tool controls/neocloud-security-baseline.v1.json >/dev/null
python - <<'PY'
import json
from pathlib import Path
p = Path('controls/neocloud-security-baseline.v1.json')
data = json.loads(p.read_text())
ids = [c['id'] for c in data['controls']]
assert len(ids) == len(set(ids)), 'duplicate control IDs'
assert all(c['tier'] in {'T0','T1','T2','T3','T4'} for c in data['controls'])
print(f"validated {len(ids)} controls")
PY

grep -RInE 'TODO|TBD|FIXME|PLACEHOLDER' README* docs controls templates GOVERNANCE.md CONTRIBUTING.md REFERENCES.md && exit 1 || true
```

Review all relative Markdown links manually or with a local link checker. Mermaid diagrams must render in GitHub Markdown.

## Writing style

- Use direct, testable language: **must** for requirements, **should** for strong recommendations, and **may** for options.
- Separate provider, customer, and shared responsibilities.
- State assumptions and applicability.
- Avoid product marketing, fear-based language, unsupported maturity claims, and absolute guarantees.
- Keep English and Chinese normative meaning aligned; literal translation is less important than semantic equivalence.

## Security-sensitive contributions

Do not open a public issue containing a live credential, customer data, exploitable production detail, or uncoordinated vulnerability. Use the repository owner's private disclosure channel. Redact evidence before committing it.

## 中文摘要

规范性修改必须说明威胁、适用范围、责任方、实现方式、最小证据、验证方法、兼容性与权威来源。禁止把专有标准正文直接复制进仓库；禁止提交真实密钥、客户数据和未协调披露的生产漏洞。所有校验和 Review 应在本地完成，只有独立验证通过后才能宣称控制已完成。
