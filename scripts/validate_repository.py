#!/usr/bin/env python3
"""Validate the NeoCloud Cyber Security repository contract.

This validator intentionally uses only the Python standard library so the same
checks can run locally and in a minimal CI environment. It validates semantic
invariants that JSON Schema alone cannot express: exact catalog cardinality,
control-ID sets, cross-references, tier distribution, bilingual baseline parity,
version consistency, required deliverables, and relative Markdown links.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "controls" / "neocloud-security-baseline.v1.json"
SCHEMA_PATH = ROOT / "controls" / "schema.json"
VERSION_PATH = ROOT / "VERSION"

EXPECTED_DOMAINS = (
    "GOV",
    "ASM",
    "IAM",
    "API",
    "NET",
    "CMP",
    "ORC",
    "DAT",
    "KMS",
    "SSC",
    "ENG",
    "VEM",
    "TEL",
    "AIR",
    "ABU",
    "IRR",
    "RES",
    "PHY",
)
EXPECTED_TIER_COUNTS = {"T0": 32, "T1": 31, "T2": 19, "T3": 7, "T4": 1}
EXPECTED_LIFECYCLE = [
    "PROPOSED",
    "READY",
    "IMPLEMENTED",
    "CANDIDATE_DONE",
    "VERIFIED",
]
EXPECTED_RESULTS = ["PASS", "FAIL", "INCONCLUSIVE", "NOT_TESTED"]
EXPECTED_PROFILES = {
    "GPU-IaaS",
    "Bare-Metal-GPU",
    "Managed-Kubernetes",
    "Managed-Slurm-HPC",
    "Model-Training",
    "Model-Serving",
    "Agent-Platform",
    "Sovereign-Regulated",
}
REQUIRED_FILES = (
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "REFERENCES.md",
    "VERSION",
    "docs/en/WHITEPAPER.md",
    "docs/zh-CN/WHITEPAPER.md",
    "docs/en/SECURITY_BASELINE.md",
    "docs/zh-CN/SECURITY_BASELINE.md",
    "docs/en/PRACTICE_GUIDE.md",
    "docs/zh-CN/PRACTICE_GUIDE.md",
    "docs/en/REFERENCE_ARCHITECTURE.md",
    "docs/zh-CN/REFERENCE_ARCHITECTURE.md",
    "docs/en/ROADMAP.md",
    "docs/zh-CN/ROADMAP.md",
    "docs/en/METRICS_AND_ASSURANCE.md",
    "docs/zh-CN/METRICS_AND_ASSURANCE.md",
    "controls/neocloud-security-baseline.v1.json",
    "controls/schema.json",
    "controls/README.md",
    "templates/baseline-assessment.csv",
    "templates/evidence-register.csv",
    "templates/exception-register.csv",
    "templates/risk-register.csv",
    "templates/security-service-catalog.csv",
    "templates/shared-responsibility-matrix.csv",
    "templates/threat-model.md",
    "templates/incident-severity-matrix.md",
)

CONTROL_ID_RE = re.compile(
    r"^NCS-(GOV|ASM|IAM|API|NET|CMP|ORC|DAT|KMS|SSC|ENG|VEM|TEL|AIR|ABU|IRR|RES|PHY)-0[1-5]$"
)
METRIC_ID_RE = re.compile(r"^NCSM-[A-Z]+-[0-9]{2}$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")
BASELINE_ROW_RE = re.compile(
    r"^\|\s*(NCS-[A-Z]+-[0-9]{2})\s*\|\s*(T[0-4])\s*\|\s*(.*?)\s*\|\s*$"
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.error(message)


def load_json(path: Path, validation: Validation) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        validation.error(f"missing JSON file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        validation.error(
            f"invalid JSON in {path.relative_to(ROOT)}: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )
        return {}
    if not isinstance(value, dict):
        validation.error(f"top-level JSON value must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def require_bilingual(
    value: object, label: str, validation: Validation
) -> None:
    if not isinstance(value, dict):
        validation.error(f"{label} must be an object")
        return
    for language in ("en", "zh-CN"):
        text = value.get(language)
        if not isinstance(text, str) or not text.strip():
            validation.error(f"{label}.{language} must be a non-empty string")


def expected_control_ids() -> set[str]:
    return {
        f"NCS-{domain}-{index:02d}"
        for domain in EXPECTED_DOMAINS
        for index in range(1, 6)
    }


def validate_catalog(catalog: dict, validation: Validation) -> tuple[set[str], Counter[str]]:
    validation.require(catalog.get("catalog_id") == "NCS-BASELINE", "catalog_id must be NCS-BASELINE")
    version = catalog.get("version")
    validation.require(
        isinstance(version, str) and VERSION_RE.fullmatch(version) is not None,
        "catalog version must use semantic version syntax",
    )
    validation.require(catalog.get("$schema") == "./schema.json", "catalog $schema must be ./schema.json")
    validation.require(catalog.get("languages") == ["en", "zh-CN"], "catalog languages must be [en, zh-CN]")
    validation.require(catalog.get("control_lifecycle") == EXPECTED_LIFECYCLE, "control lifecycle differs from the normative sequence")
    validation.require(catalog.get("verification_results") == EXPECTED_RESULTS, "verification results differ from the normative set")

    profiles = catalog.get("service_profiles")
    validation.require(isinstance(profiles, list), "service_profiles must be an array")
    if isinstance(profiles, list):
        validation.require(set(profiles) == EXPECTED_PROFILES, "service_profiles must contain the eight normative profiles exactly once")
        validation.require(len(profiles) == len(set(profiles)), "service_profiles contains duplicates")

    tiers = catalog.get("tiers")
    validation.require(isinstance(tiers, dict), "tiers must be an object")
    if not isinstance(tiers, dict):
        tiers = {}
    validation.require(set(tiers) == set(EXPECTED_TIER_COUNTS), "tiers must contain T0 through T4 exactly")

    evidence_profiles = catalog.get("evidence_profiles")
    verification_profiles = catalog.get("verification_profiles")
    metric_ids = catalog.get("metric_ids")
    validation.require(isinstance(evidence_profiles, dict) and bool(evidence_profiles), "evidence_profiles must be a non-empty object")
    validation.require(isinstance(verification_profiles, dict) and bool(verification_profiles), "verification_profiles must be a non-empty object")
    validation.require(isinstance(metric_ids, list) and bool(metric_ids), "metric_ids must be a non-empty array")
    evidence_profiles = evidence_profiles if isinstance(evidence_profiles, dict) else {}
    verification_profiles = verification_profiles if isinstance(verification_profiles, dict) else {}
    metric_id_set = set(metric_ids) if isinstance(metric_ids, list) else set()
    for metric_id in metric_id_set:
        validation.require(isinstance(metric_id, str) and METRIC_ID_RE.fullmatch(metric_id) is not None, f"invalid metric ID: {metric_id!r}")
    if isinstance(metric_ids, list):
        validation.require(len(metric_ids) == len(metric_id_set), "metric_ids contains duplicates")

    domains = catalog.get("domains")
    validation.require(isinstance(domains, list), "domains must be an array")
    domains = domains if isinstance(domains, list) else []
    validation.require(len(domains) == 18, f"expected 18 domains, found {len(domains)}")
    observed_domains: list[str] = []
    for index, domain in enumerate(domains):
        label = f"domains[{index}]"
        if not isinstance(domain, dict):
            validation.error(f"{label} must be an object")
            continue
        domain_id = domain.get("id")
        if isinstance(domain_id, str):
            observed_domains.append(domain_id)
        else:
            validation.error(f"{label}.id must be a string")
        require_bilingual(domain.get("title"), f"{label}.title", validation)
        require_bilingual(domain.get("outcome"), f"{label}.outcome", validation)
    validation.require(tuple(observed_domains) == EXPECTED_DOMAINS, "domain IDs/order must match the normative 18-domain sequence")
    validation.require(len(observed_domains) == len(set(observed_domains)), "domain IDs contain duplicates")

    controls = catalog.get("controls")
    validation.require(isinstance(controls, list), "controls must be an array")
    controls = controls if isinstance(controls, list) else []
    validation.require(len(controls) == 90, f"expected 90 controls, found {len(controls)}")

    observed_ids: list[str] = []
    tier_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    for index, control in enumerate(controls):
        label = f"controls[{index}]"
        if not isinstance(control, dict):
            validation.error(f"{label} must be an object")
            continue
        control_id = control.get("id")
        domain = control.get("domain")
        tier = control.get("tier")
        if not isinstance(control_id, str) or CONTROL_ID_RE.fullmatch(control_id) is None:
            validation.error(f"{label}.id is invalid: {control_id!r}")
        else:
            observed_ids.append(control_id)
        validation.require(domain in EXPECTED_DOMAINS, f"{label}.domain is invalid: {domain!r}")
        if isinstance(control_id, str) and isinstance(domain, str):
            validation.require(control_id.startswith(f"NCS-{domain}-"), f"{control_id} does not match domain {domain}")
        validation.require(tier in EXPECTED_TIER_COUNTS, f"{label}.tier is invalid: {tier!r}")
        if isinstance(tier, str):
            tier_counts[tier] += 1
        if isinstance(domain, str):
            domain_counts[domain] += 1
        require_bilingual(control.get("title"), f"{label}.title", validation)
        require_bilingual(control.get("requirement"), f"{label}.requirement", validation)

        evidence_profile = control.get("evidence_profile")
        verification_profile = control.get("verification_profile")
        validation.require(evidence_profile in evidence_profiles, f"{control_id}: unknown evidence_profile {evidence_profile!r}")
        validation.require(verification_profile in verification_profiles, f"{control_id}: unknown verification_profile {verification_profile!r}")

        control_metrics = control.get("metric_ids")
        validation.require(isinstance(control_metrics, list) and bool(control_metrics), f"{control_id}: metric_ids must be a non-empty array")
        if isinstance(control_metrics, list):
            validation.require(len(control_metrics) == len(set(control_metrics)), f"{control_id}: metric_ids contains duplicates")
            for metric_id in control_metrics:
                validation.require(metric_id in metric_id_set, f"{control_id}: unknown metric ID {metric_id!r}")

    observed_id_set = set(observed_ids)
    validation.require(len(observed_ids) == len(observed_id_set), "control IDs contain duplicates")
    missing = sorted(expected_control_ids() - observed_id_set)
    unexpected = sorted(observed_id_set - expected_control_ids())
    if missing:
        validation.error(f"missing control IDs: {', '.join(missing)}")
    if unexpected:
        validation.error(f"unexpected control IDs: {', '.join(unexpected)}")
    validation.require(dict(tier_counts) == EXPECTED_TIER_COUNTS, f"tier distribution mismatch: expected {EXPECTED_TIER_COUNTS}, found {dict(tier_counts)}")
    validation.require(all(domain_counts.get(domain) == 5 for domain in EXPECTED_DOMAINS), f"each domain must contain five controls; found {dict(domain_counts)}")

    rules = catalog.get("normative_rules")
    validation.require(isinstance(rules, dict), "normative_rules must be an object")
    if isinstance(rules, dict):
        t0_rule = str(rules.get("t0_gate", "")).upper()
        validation.require("NO-GO" in t0_rule and "T0" in t0_rule and "VERIFIED" in t0_rule, "normative T0 rule must state VERIFIED and NO-GO behavior")

    return observed_id_set, tier_counts


def parse_baseline(path: Path, validation: Validation) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        validation.error(f"missing baseline: {path.relative_to(ROOT)}")
        return rows
    for line in lines:
        match = BASELINE_ROW_RE.match(line)
        if not match:
            continue
        control_id, tier, title = match.groups()
        if control_id in rows:
            validation.error(f"duplicate {control_id} in {path.relative_to(ROOT)}")
        rows[control_id] = (tier, title.strip())
    return rows


def validate_baseline_parity(catalog: dict, catalog_ids: set[str], validation: Validation) -> None:
    en_path = ROOT / "docs" / "en" / "SECURITY_BASELINE.md"
    zh_path = ROOT / "docs" / "zh-CN" / "SECURITY_BASELINE.md"
    en_rows = parse_baseline(en_path, validation)
    zh_rows = parse_baseline(zh_path, validation)
    validation.require(set(en_rows) == catalog_ids, "English baseline control-ID set differs from the catalog")
    validation.require(set(zh_rows) == catalog_ids, "Chinese baseline control-ID set differs from the catalog")

    by_id = {
        control["id"]: control
        for control in catalog.get("controls", [])
        if isinstance(control, dict) and isinstance(control.get("id"), str)
    }
    for control_id in sorted(catalog_ids):
        control = by_id.get(control_id)
        if not control:
            continue
        if control_id in en_rows:
            tier, title = en_rows[control_id]
            validation.require(tier == control.get("tier"), f"{control_id}: English baseline tier differs from catalog")
            validation.require(title == control.get("title", {}).get("en"), f"{control_id}: English baseline title differs from catalog")
        if control_id in zh_rows:
            tier, title = zh_rows[control_id]
            validation.require(tier == control.get("tier"), f"{control_id}: Chinese baseline tier differs from catalog")
            validation.require(title == control.get("title", {}).get("zh-CN"), f"{control_id}: Chinese baseline title differs from catalog")


def validate_versions(catalog: dict, validation: Validation) -> None:
    try:
        version = VERSION_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        validation.error("missing VERSION")
        return
    validation.require(VERSION_RE.fullmatch(version) is not None, f"VERSION is invalid: {version!r}")
    validation.require(catalog.get("version") == version, "catalog version differs from VERSION")

    version_files = (
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "docs/en/WHITEPAPER.md",
        ROOT / "docs/zh-CN/WHITEPAPER.md",
        ROOT / "docs/en/SECURITY_BASELINE.md",
        ROOT / "docs/zh-CN/SECURITY_BASELINE.md",
        ROOT / "docs/en/REFERENCE_ARCHITECTURE.md",
        ROOT / "docs/zh-CN/REFERENCE_ARCHITECTURE.md",
        ROOT / "docs/en/PRACTICE_GUIDE.md",
        ROOT / "docs/zh-CN/PRACTICE_GUIDE.md",
        ROOT / "docs/en/METRICS_AND_ASSURANCE.md",
        ROOT / "docs/zh-CN/METRICS_AND_ASSURANCE.md",
    )
    for path in version_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        validation.require(version in text, f"{path.relative_to(ROOT)} does not contain version {version}")


def clean_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target:
        return None
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        # Markdown may append a quoted title after whitespace.
        target = target.split(maxsplit=1)[0]
    target = unquote(target)
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("//") or target.startswith("#"):
        return None
    path = parsed.path
    return path or None


def validate_markdown_links(validation: Validation) -> None:
    for markdown in sorted(ROOT.rglob("*.md")):
        # Git metadata, virtual environments, or generated dependencies are not repository documentation.
        if any(part in {".git", ".venv", "venv", "node_modules"} for part in markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        targets = MARKDOWN_LINK_RE.findall(text) + MARKDOWN_IMAGE_RE.findall(text)
        for raw_target in targets:
            target = clean_link_target(raw_target)
            if target is None:
                continue
            if target.startswith("/"):
                resolved = ROOT / target.lstrip("/")
            else:
                resolved = markdown.parent / target
            if not resolved.exists():
                validation.error(
                    f"broken relative Markdown link in {markdown.relative_to(ROOT)}: {raw_target!r}"
                )


def validate_required_files(validation: Validation) -> None:
    for relative in REQUIRED_FILES:
        validation.require((ROOT / relative).exists(), f"missing required deliverable: {relative}")


def validate_schema_file(validation: Validation) -> None:
    schema = load_json(SCHEMA_PATH, validation)
    if not schema:
        return
    validation.require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema.json must declare JSON Schema 2020-12")
    validation.require(schema.get("type") == "object", "schema.json top-level type must be object")


def main() -> int:
    validation = Validation()
    validate_required_files(validation)
    catalog = load_json(CATALOG_PATH, validation)
    validate_schema_file(validation)

    catalog_ids: set[str] = set()
    tier_counts: Counter[str] = Counter()
    if catalog:
        catalog_ids, tier_counts = validate_catalog(catalog, validation)
        validate_baseline_parity(catalog, catalog_ids, validation)
        validate_versions(catalog, validation)
    validate_markdown_links(validation)

    for warning in validation.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if validation.errors:
        for error in validation.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"NeoCloud repository validation failed with {len(validation.errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    print(
        "NeoCloud repository validation passed: "
        f"{len(EXPECTED_DOMAINS)} domains, {len(catalog_ids)} controls, "
        f"tiers={dict(sorted(tier_counts.items()))}, version={catalog.get('version')}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
