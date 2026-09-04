#!/usr/bin/env python3
"""Apply exact, asserted improvements to the repository validator."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "validate_repository.py"


def replace_once(old: str, new: str) -> None:
    text = TARGET.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one occurrence, found {count}: {old[:120]!r}")
    TARGET.write_text(text.replace(old, new), encoding="utf-8")


replace_once(
    """invariants that JSON Schema alone cannot express: exact catalog cardinality,
control-ID sets, cross-references, tier distribution, bilingual baseline parity,
version consistency, required deliverables, and relative Markdown links.""",
    """invariants that JSON Schema alone cannot express: project status and T0
semantics, exact catalog cardinality, control-ID sets, cross-references, tier
distribution, bilingual baseline and metric parity, version consistency,
required deliverables, and relative Markdown links.""",
)

replace_once(
    '    "VERSION",\n',
    '''    "VERSION",\n    "SECURITY.md",\n    ".github/CODEOWNERS",\n    ".github/PULL_REQUEST_TEMPLATE.md",\n    ".github/REPOSITORY_SETTINGS.md",\n    ".github/ISSUE_TEMPLATE/config.yml",\n    ".github/ISSUE_TEMPLATE/control-change.yml",\n    ".github/ISSUE_TEMPLATE/factual-correction.yml",\n''',
)

replace_once(
    '''BASELINE_ROW_RE = re.compile(
    r"^\\|\\s*(NCS-[A-Z]+-[0-9]{2})\\s*\\|\\s*(T[0-4])\\s*\\|\\s*(.*?)\\s*\\|\\s*$"
)
''',
    '''BASELINE_ROW_RE = re.compile(
    r"^\\|\\s*(NCS-[A-Z]+-[0-9]{2})\\s*\\|\\s*(T[0-4])\\s*\\|\\s*(.*?)\\s*\\|\\s*$"
)
METRIC_ROW_RE = re.compile(r"^\\|\\s*(NCSM-[A-Z]+-[0-9]{2})\\s*\\|")
''',
)

replace_once(
    '''def validate_catalog(catalog: dict, validation: Validation) -> tuple[set[str], Counter[str]]:
    validation.require(catalog.get("catalog_id") == "NCS-BASELINE", "catalog_id must be NCS-BASELINE")
''',
    '''def validate_catalog(catalog: dict, validation: Validation) -> tuple[set[str], Counter[str]]:
    validation.require(catalog.get("catalog_id") == "NCS-BASELINE", "catalog_id must be NCS-BASELINE")
    validation.require(
        catalog.get("status") == "implementation-oriented project draft",
        "catalog status must be implementation-oriented project draft",
    )
''',
)

replace_once(
    '''        validation.require("NO-GO" in t0_rule and "T0" in t0_rule and "VERIFIED" in t0_rule, "normative T0 rule must state VERIFIED and NO-GO behavior")
''',
    '''        validation.require(
            all(
                token in t0_rule
                for token in (
                    "NO-GO",
                    "NO_GO_NONCONFORMANT",
                    "T0",
                    "VERIFIED",
                    "BUSINESS-RISK DECISION",
                    "CANNOT CHANGE",
                )
            ),
            "normative T0 rule must preserve NO-GO, machine state, verification, and business-decision semantics",
        )
        t0_rule_zh = str(rules.get("t0_gate_zh_CN", ""))
        validation.require(
            "NO-GO" in t0_rule_zh
            and "NO_GO_NONCONFORMANT" in t0_rule_zh
            and "VERIFIED" in t0_rule_zh
            and "业务风险决定" in t0_rule_zh
            and "不能改变" in t0_rule_zh,
            "Chinese normative T0 rule must preserve the same decision semantics",
        )
''',
)

replace_once(
    '''def validate_versions(catalog: dict, validation: Validation) -> None:
''',
    '''def parse_metric_rows(path: Path, validation: Validation) -> dict[str, int]:
    rows: dict[str, int] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        validation.error(f"missing metrics guide: {path.relative_to(ROOT)}")
        return rows
    for line_number, line in enumerate(lines, start=1):
        match = METRIC_ROW_RE.match(line)
        if not match:
            continue
        metric_id = match.group(1)
        if metric_id in rows:
            validation.error(
                f"duplicate {metric_id} in {path.relative_to(ROOT)} at lines "
                f"{rows[metric_id]} and {line_number}"
            )
        rows[metric_id] = line_number
    return rows


def validate_metric_docs(catalog: dict, validation: Validation) -> None:
    en_path = ROOT / "docs" / "en" / "METRICS_AND_ASSURANCE.md"
    zh_path = ROOT / "docs" / "zh-CN" / "METRICS_AND_ASSURANCE.md"
    en_rows = parse_metric_rows(en_path, validation)
    zh_rows = parse_metric_rows(zh_path, validation)
    en_ids = set(en_rows)
    zh_ids = set(zh_rows)
    validation.require(en_ids == zh_ids, "English and Chinese metric-ID sets differ")

    catalog_ids = set(catalog.get("metric_ids", []))
    missing_en = sorted(catalog_ids - en_ids)
    missing_zh = sorted(catalog_ids - zh_ids)
    if missing_en:
        validation.error(
            "catalog-linked metric IDs missing from English metrics guide: "
            + ", ".join(missing_en)
        )
    if missing_zh:
        validation.error(
            "catalog-linked metric IDs missing from Chinese metrics guide: "
            + ", ".join(missing_zh)
        )


def validate_versions(catalog: dict, validation: Validation) -> None:
''',
)

replace_once(
    '''        validate_baseline_parity(catalog, catalog_ids, validation)
        validate_versions(catalog, validation)
''',
    '''        validate_baseline_parity(catalog, catalog_ids, validation)
        validate_metric_docs(catalog, validation)
        validate_versions(catalog, validation)
''',
)

print("Applied repository-validator semantic and metric invariants.")
