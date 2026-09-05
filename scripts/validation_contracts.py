#!/usr/bin/env python3
"""Strict, offline validation helpers; no infrastructure or network actions."""
from __future__ import annotations

import copy
import csv
import io
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    """Input is invalid or insufficient to support a repository claim."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def load_json(path: Path) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise ContractError(f"non-finite JSON number: {value}")

    try:
        require(path.stat().st_size <= 4 * 1024 * 1024, "JSON exceeds 4 MiB repository limit")
        result = json.loads(path.read_text(encoding="utf-8"),
                            object_pairs_hook=pairs, parse_constant=constant)
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ContractError(f"cannot read JSON {path.name}: {type(exc).__name__}") from exc
    require(isinstance(result, dict), f"{path.name}: expected an object")
    return result


def check_schema(instance: Any, schema: dict[str, Any]) -> None:
    """Validate Draft 2020-12 with date formats, without remote reference retrieval."""
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry
        from referencing.exceptions import NoSuchResource
    except ImportError as exc:
        raise ContractError("install requirements-validation.txt; schema validation was NOT run") from exc

    def offline(uri: str) -> Any:
        raise NoSuchResource(ref=uri)

    def local_refs(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"$ref", "$dynamicRef"}:
                    require(isinstance(value, str) and value.startswith("#"),
                            "only same-document schema references are permitted")
                local_refs(value)
        elif isinstance(node, list):
            for value in node:
                local_refs(value)

    local_refs(schema)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
            "unsupported schema dialect")
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker(),
                                        registry=Registry(retrieve=offline))
        error = next(validator.iter_errors(instance), None)
        if error is not None:
            # Do not echo arbitrary input values, which may contain private evidence.
            where = "/".join(map(str, error.absolute_path)) or "<root>"
            raise ContractError(f"schema violation at {where}: {error.validator}")
    except ContractError:
        raise
    except Exception as exc:
        raise ContractError(f"schema evaluation failed: {type(exc).__name__}") from exc


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            records = list(csv.reader(handle, strict=True))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ContractError(f"cannot read CSV {path.name}: {type(exc).__name__}") from exc
    require(bool(records) and bool(records[0]), f"{path.name}: missing header")
    fields = records[0]
    require(all(fields) and len(set(fields)) == len(fields), f"{path.name}: duplicate/empty header")
    rows = []
    for number, record in enumerate(records[1:], 2):
        require(len(record) == len(fields), f"{path.name}:{number}: wrong field count")
        rows.append(dict(zip(fields, record)))
    return fields, rows


def csv_text(fields: list[str], rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def summary(findings: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(item["prior_coverage"] for item in findings)
    require(set(counts) <= {"covered", "partial", "gap"}, "invalid prior coverage value")
    return {"explicit": counts["covered"], "partial": counts["partial"], "gap": counts["gap"]}


def unique_index(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result = {}
    require(isinstance(items, list), "expected a record array")
    for item in items:
        require(isinstance(item, dict), "expected an object record")
        ident = item.get(key)
        require(isinstance(ident, str) and bool(ident), f"missing {key}")
        require(ident not in result, f"duplicate {key}: {ident}")
        result[ident] = item
    return result


def validate_profile(profile: dict[str, Any], core_ids: set[str]) -> None:
    """Semantic checks after schema validation; all counts derive from records."""
    findings = unique_index(profile["findings"], "id")
    require(set(findings) == {f"SA-NC-{n:03d}" for n in range(1, 41)}, "40 finding IDs must be complete")
    stats = profile["coverage_summary"]
    require(stats["before"] == summary(list(findings.values())), "coverage totals contradict per-item records")
    require(stats["project_authored_atomic_patterns"] == len(findings), "atomic total mismatch")
    require(stats["after"] == {"explicit_mapped": len(findings)}, "mapped total mismatch")
    require(stats["exact_clustermax_parity_claimed"] is False, "exact parity must not be claimed")
    sources = unique_index(profile["sources"], "id")
    review = date.fromisoformat(profile["review_date"])
    for source in sources.values():
        require(date.fromisoformat(source["observed_at"]) <= review, "source observation postdates review")
    require(len(set(profile["service_profiles"])) == 8, "duplicate service profile")
    require(len({x["name"] for x in profile["dimensions"]}) == 10, "duplicate dimension")
    public = profile["public_security_page_coverage"]
    items = unique_index(public["items"], "id")
    require(set(items) == {f"CMX-SEC-PUB-{n:03d}" for n in range(1, 21)}, "20 public item IDs must be complete")
    require(public["canonical_source_id"] in sources, "unknown canonical source")
    require(public["canonical_enumerated"] == public["mapped"] == len(items), "public mapping count mismatch")
    require(public["alternate_host_reported"] - public["canonical_enumerated"] == public["unresolved_delta"],
            "historical alternate-host count delta mismatch")
    require(public["exact_parity_claimed"] is False, "public mapping cannot imply parity")
    require(stats["canonical_public_security_page"] == {"enumerable": len(items), "mapped": len(items)},
            "public summary mismatch")
    require(stats["alternate_host_reported_security_count"] == public["alternate_host_reported"] and
            stats["unresolved_live_delta"] == public["unresolved_delta"], "duplicate count summaries disagree")
    for item in list(findings.values()) + list(items.values()):
        refs = item["mapped_controls"]
        require(bool(refs) and len(refs) == len(set(refs)), f"{item['id']}: empty/duplicate control mapping")
        require(set(refs) <= core_ids, f"{item['id']}: unknown core control")
        require(set(item["source_ids"]) <= set(sources), f"{item['id']}: unknown source")
    for item in findings.values():
        require(item["assurance_views"] == profile["assurance_views"], f"{item['id']}: assurance views drift")


def validate_templates(profile: dict[str, Any], article: Path, security: Path) -> None:
    """Repository templates are unassessed; this is NOT a production gate evaluator."""
    for path, key, data in [(article, "finding_id", profile["findings"]),
                            (security, "criterion_id", profile["public_security_page_coverage"]["items"])]:
        fields, rows = read_csv(path)
        expected = unique_index(data, "id")
        observed = unique_index(rows, key)
        require(set(expected) == set(observed), f"{path.name}: template IDs differ from profile")
        unique_index(rows, "assessment_id")
        require("core_controls" in fields, f"{path.name}: missing core_controls")
        for ident, row in observed.items():
            item = expected[ident]
            require(row["core_controls"].split(";") == item["mapped_controls"], f"{ident}: CSV mapping drift")
            require(row.get("applicability") == "UNKNOWN" and row.get("state") == "PROPOSED",
                    f"{ident}: repository template must be unassessed")
            result_fields = (["tenant_blackbox_result", "provider_whitebox_result", "independent_failure_recovery_result"]
                             if key == "finding_id" else ["verification_result"])
            require(all(row.get(f) == "NOT_TESTED" for f in result_fields), f"{ident}: template cannot claim a test passed")
            require(all(not row.get(f, "").strip() for f in ["evidence_ids", "validator", "last_verified_at", "valid_until"]),
                    f"{ident}: template cannot contain live verification evidence")
            if key == "finding_id":
                require(row.get("severity") == item["severity"], f"{ident}: severity drift")
            else:
                require(row.get("criterion_title") == item["title"]["en"], f"{ident}: title drift")


def effective_catalog(core: dict[str, Any], errata: dict[str, Any]) -> dict[str, Any]:
    """Apply validated errata to a copy; never silently ignore unknown targets."""
    require(isinstance(core.get("catalog_id"), str) and bool(core["catalog_id"]), "missing catalog ID")
    require(isinstance(core.get("version"), str) and bool(core["version"]), "missing catalog version")
    require(errata.get("base_catalog_id") == core.get("catalog_id"), "errata catalog ID mismatch")
    require(errata.get("base_catalog_version") == core.get("version"), "errata catalog version mismatch")
    result = copy.deepcopy(core)
    controls = unique_index(result["controls"], "id")
    corrections = errata["corrections"]
    unique_index(corrections, "erratum_id")
    seen = set()
    for correction in corrections:
        ident, field = correction["control_id"], correction["field"]
        require(ident in controls and field == "requirement", "unknown or unsupported errata target")
        require((ident, field) not in seen, "conflicting repeated errata target")
        seen.add((ident, field))
        text = correction["replacement"]
        require(isinstance(text, dict) and set(text) == {"en", "zh-CN"} and
                all(isinstance(v, str) and v.strip() for v in text.values()), "invalid bilingual errata replacement")
        controls[ident][field] = copy.deepcopy(text)
    return result
