#!/usr/bin/env python3
"""Validate the SemiAnalysis/ClusterMAX public-findings interoperability overlay.

The validator is deliberately standard-library only. It proves repository
consistency, not provider security, ClusterMAX equivalence, or certification.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "controls" / "semianalysis-public-findings-profile.v1.json"
PROFILE_SCHEMA = ROOT / "controls" / "semianalysis-public-findings-profile.v1.schema.json"
ERRATA = ROOT / "controls" / "neocloud-security-baseline.v1.errata.json"
ERRATA_SCHEMA = ROOT / "controls" / "neocloud-security-baseline.v1.errata.schema.json"
CORE = ROOT / "controls" / "neocloud-security-baseline.v1.json"
ARTICLE_CSV = ROOT / "templates" / "semianalysis-public-findings-assessment.csv"
SECURITY_CSV = ROOT / "templates" / "clustermax-public-security-requirements-assessment.csv"

EXPECTED_VIEWS = [
    "tenant-black-box",
    "provider-white-box",
    "independent-failure-recovery",
]
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
EXPECTED_DIMENSIONS = [
    "Security",
    "Lifecycle",
    "Orchestration",
    "Storage",
    "Networking",
    "Reliability",
    "Monitoring",
    "Pricing",
    "Partnerships",
    "Availability",
]
ALLOWED_RESULTS = {"PASS", "FAIL", "INCONCLUSIVE", "NOT_TESTED"}
CONTROL_RE = re.compile(r"^NCS-[A-Z]+-[0-9]{2}$")


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def load_json(path: Path, v: Validation) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        v.errors.append(f"missing file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        v.errors.append(
            f"invalid JSON in {path.relative_to(ROOT)} at "
            f"{exc.lineno}:{exc.colno}: {exc.msg}"
        )
        return {}
    if not isinstance(value, dict):
        v.errors.append(f"top-level value must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def read_csv(path: Path, v: Validation) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            return reader.fieldnames or [], list(reader)
    except FileNotFoundError:
        v.errors.append(f"missing file: {path.relative_to(ROOT)}")
        return [], []


def validate_profile(profile: dict, core: dict, v: Validation) -> None:
    v.require(profile.get("profile_id") == "NCS-PROFILE-SEMIANALYSIS-PUBLIC-2026", "unexpected profile_id")
    v.require(profile.get("version") == "1.0.0", "profile version must be 1.0.0")
    v.require(profile.get("baseline_version") == core.get("version"), "profile baseline_version differs from core catalog")
    v.require(profile.get("assurance_views") == EXPECTED_VIEWS, "assurance views differ from the three-view model")
    v.require(set(profile.get("service_profiles", [])) == EXPECTED_PROFILES, "service profile set is incomplete")
    dimensions = [item.get("name") for item in profile.get("dimensions", []) if isinstance(item, dict)]
    v.require(dimensions == EXPECTED_DIMENSIONS, "ClusterMAX dimension names/order changed")

    coverage = profile.get("coverage_summary", {})
    v.require(coverage.get("article_reported_macro_patterns") == 5, "article macro-pattern count must be 5")
    v.require(coverage.get("project_authored_atomic_patterns") == 40, "project atomic-pattern count must be 40")
    v.require(coverage.get("before") == {"explicit": 17, "partial": 17, "gap": 6}, "before-state distribution changed")
    v.require(coverage.get("after") == {"explicit_mapped": 40}, "after-state mapping must be 40")
    v.require(coverage.get("exact_clustermax_parity_claimed") is False, "profile must not claim exact ClusterMAX parity")

    core_ids = {
        item.get("id")
        for item in core.get("controls", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    findings = profile.get("findings", [])
    v.require(len(findings) == 40, f"expected 40 findings, found {len(findings)}")
    expected_finding_ids = [f"SA-NC-{i:03d}" for i in range(1, 41)]
    observed_finding_ids = [item.get("id") for item in findings if isinstance(item, dict)]
    v.require(observed_finding_ids == expected_finding_ids, "finding IDs must be contiguous SA-NC-001..040")
    prior = Counter(item.get("prior_coverage") for item in findings if isinstance(item, dict))
    v.require(prior == Counter({"covered": 17, "partial": 17, "gap": 6}), f"prior coverage distribution changed: {dict(prior)}")

    for finding in findings:
        if not isinstance(finding, dict):
            v.errors.append("finding must be an object")
            continue
        finding_id = finding.get("id")
        v.require(finding.get("assurance_views") == EXPECTED_VIEWS, f"{finding_id}: three assurance views missing")
        controls = finding.get("mapped_controls", [])
        v.require(bool(controls), f"{finding_id}: no mapped controls")
        v.require(len(controls) == len(set(controls)), f"{finding_id}: duplicate mapped controls")
        for control_id in controls:
            v.require(isinstance(control_id, str) and CONTROL_RE.fullmatch(control_id) is not None, f"{finding_id}: invalid control ID {control_id!r}")
            v.require(control_id in core_ids, f"{finding_id}: unknown core control {control_id!r}")
        v.require(len(finding.get("minimum_evidence", [])) >= 4, f"{finding_id}: minimum evidence is incomplete")

    public = profile.get("public_security_page_coverage", {})
    v.require(public.get("canonical_enumerated") == 20, "canonical public Security-page count must be 20")
    v.require(public.get("mapped") == 20, "canonical public Security-page mapped count must be 20")
    v.require(public.get("alternate_host_reported") == 21, "alternate-host observed count must remain 21")
    v.require(public.get("unresolved_delta") == 1, "unresolved public count delta must remain 1")
    v.require(public.get("exact_parity_claimed") is False, "public-page mapping must not claim exact parity")
    items = public.get("items", [])
    v.require(len(items) == 20, f"expected 20 public Security-page items, found {len(items)}")
    expected_public_ids = [f"CMX-SEC-PUB-{i:03d}" for i in range(1, 21)]
    observed_public_ids = [item.get("id") for item in items if isinstance(item, dict)]
    v.require(observed_public_ids == expected_public_ids, "public Security-page IDs must be contiguous 001..020")
    for item in items:
        item_id = item.get("id")
        v.require(item.get("coverage") == "mapped-not-verified", f"{item_id}: coverage must remain mapped-not-verified")
        for control_id in item.get("mapped_controls", []):
            v.require(control_id in core_ids, f"{item_id}: unknown core control {control_id!r}")

    errata_ref = profile.get("normative_errata", {})
    v.require(errata_ref.get("id") == "NCS-BASELINE-V1-ERRATA", "profile errata ID mismatch")
    v.require(errata_ref.get("applies_to") == ["NCS-CMP-02"], "profile errata scope mismatch")


def validate_errata(errata: dict, core: dict, v: Validation) -> None:
    v.require(errata.get("errata_id") == "NCS-BASELINE-V1-ERRATA", "unexpected errata_id")
    v.require(errata.get("base_catalog_version") == core.get("version"), "errata base catalog version mismatch")
    corrections = errata.get("corrections", [])
    v.require(len(corrections) == 1, "v1 errata must currently contain exactly one correction")
    if not corrections:
        return
    correction = corrections[0]
    v.require(correction.get("control_id") == "NCS-CMP-02", "errata must apply to NCS-CMP-02")
    replacement = correction.get("replacement", {})
    en = replacement.get("en", "")
    zh = replacement.get("zh-CN", "")
    for token in (
        "full-device dedication",
        "hardware partitioning",
        "hypervisor-mediated vGPU",
        "scheduler-level bare-device-plugin time-slicing",
    ):
        v.require(token in en, f"errata English replacement omits {token}")
    v.require("never represent scheduler-level time-slicing as memory or fault isolation" in en, "errata does not preserve device-plugin limitation")
    v.require("不得把调度器级 Time-slicing 表述为显存或故障隔离" in zh, "Chinese errata does not preserve device-plugin limitation")


def validate_article_csv(profile: dict, v: Validation) -> None:
    fields, rows = read_csv(ARTICLE_CSV, v)
    required = {
        "assessment_id",
        "finding_id",
        "service",
        "service_profile",
        "region",
        "cluster",
        "sku",
        "hardware",
        "firmware_driver_orchestrator_versions",
        "tenant_blackbox_result",
        "provider_whitebox_result",
        "independent_failure_recovery_result",
        "evidence_ids",
        "validator",
        "last_verified_at",
        "valid_until",
    }
    v.require(required.issubset(fields), "40-pattern assessment CSV is missing required columns")
    v.require(len(rows) == 40, f"40-pattern assessment CSV has {len(rows)} rows")
    expected = [f"SA-NC-{i:03d}" for i in range(1, 41)]
    v.require([row.get("finding_id") for row in rows] == expected, "40-pattern assessment CSV IDs changed")
    for line, row in enumerate(rows, start=2):
        for field in (
            "tenant_blackbox_result",
            "provider_whitebox_result",
            "independent_failure_recovery_result",
        ):
            result = (row.get(field) or "").strip()
            v.require(result in ALLOWED_RESULTS, f"{ARTICLE_CSV.name}:{line}: invalid {field}={result!r}")


def validate_security_csv(v: Validation) -> None:
    fields, rows = read_csv(SECURITY_CSV, v)
    required = {
        "assessment_id",
        "criterion_id",
        "criterion_title",
        "service",
        "service_profile",
        "region",
        "cluster",
        "sku",
        "core_controls",
        "verification_method",
        "validator",
        "verification_result",
        "last_verified_at",
        "valid_until",
    }
    v.require(required.issubset(fields), "20-item Security-page assessment CSV is missing required columns")
    v.require(len(rows) == 20, f"20-item Security-page assessment CSV has {len(rows)} rows")
    expected = [f"CMX-SEC-PUB-{i:03d}" for i in range(1, 21)]
    v.require([row.get("criterion_id") for row in rows] == expected, "20-item Security-page assessment IDs changed")
    for line, row in enumerate(rows, start=2):
        result = (row.get("verification_result") or "").strip()
        v.require(result in ALLOWED_RESULTS, f"{SECURITY_CSV.name}:{line}: invalid verification_result={result!r}")


def validate_docs(v: Validation) -> None:
    required_tokens = {
        "SEMIANALYSIS_COVERAGE.md": ["20/20", "40", "not a ClusterMAX score"],
        "docs/en/SEMIANALYSIS_COVERAGE.md": ["20/20", "40/40", "three distinct views", "not 21/21"],
        "docs/zh-CN/SEMIANALYSIS_COVERAGE.md": ["20/20", "40/40", "三类视角", "不声明 21/21"],
        "README.md": ["SEMIANALYSIS_COVERAGE", "20/20", "40 atomic"],
        "README.zh-CN.md": ["SEMIANALYSIS_COVERAGE", "20/20", "40 项"],
        "templates/README.md": ["tenant_blackbox_result", "mapped row is not proof"],
        "controls/README.md": ["semianalysis-public-findings-profile.v1.json", "neocloud-security-baseline.v1.errata.json"],
    }
    for relative, tokens in required_tokens.items():
        text = ""
        try:
            text = (ROOT / relative).read_text(encoding="utf-8")
        except FileNotFoundError:
            v.errors.append(f"missing file: {relative}")
            continue
        for token in tokens:
            v.require(token in text, f"{relative} omits required token {token!r}")


def main() -> int:
    v = Validation()
    core = load_json(CORE, v)
    profile = load_json(PROFILE, v)
    errata = load_json(ERRATA, v)
    load_json(PROFILE_SCHEMA, v)
    load_json(ERRATA_SCHEMA, v)

    if core and profile:
        validate_profile(profile, core, v)
    if core and errata:
        validate_errata(errata, core, v)
    validate_article_csv(profile, v)
    validate_security_csv(v)
    validate_docs(v)

    if v.errors:
        for error in v.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"SemiAnalysis profile validation failed with {len(v.errors)} error(s).", file=sys.stderr)
        return 1

    print(
        "SemiAnalysis public-findings profile validation passed: "
        "5 article patterns, 40 project atomic patterns, "
        "20/20 canonical public Security-page mappings, "
        "three assurance views, no exact-parity claim."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
