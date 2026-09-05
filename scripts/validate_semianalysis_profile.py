#!/usr/bin/env python3
"""Offline schema, mapping and unassessed-template validation. Not certification.

Install requirements-validation.txt first. The two earlier stdlib validators
remain separate; this check now actually enforces JSON Schema.
"""
from __future__ import annotations
import sys
from pathlib import Path
from validation_contracts import (ContractError, check_schema, effective_catalog,
                                  load_json, require, summary, unique_index,
                                  validate_profile, validate_templates)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        controls = ROOT / "controls"
        core = load_json(controls / "neocloud-security-baseline.v1.json")
        profile = load_json(controls / "semianalysis-public-findings-profile.v1.json")
        errata = load_json(controls / "neocloud-security-baseline.v1.errata.json")
        for value, name in [(core, "schema.json"),
                            (profile, "semianalysis-public-findings-profile.v1.schema.json"),
                            (errata, "neocloud-security-baseline.v1.errata.schema.json")]:
            check_schema(value, load_json(controls / name))
        core_ids = set(unique_index(core["controls"], "id"))
        require(len(core_ids) == 90, "expected 90 core controls")
        require(profile["baseline_version"] == core["version"], "profile/core version drift")
        require((ROOT / "VERSION").read_text(encoding="utf-8").strip() == core["version"], "VERSION drift")
        validate_profile(profile, core_ids)
        require(profile["normative_errata"]["id"] == errata["errata_id"], "errata reference mismatch")
        require(profile["normative_errata"]["applies_to"] == [x["control_id"] for x in errata["corrections"]],
                "errata scope mismatch")
        effective = effective_catalog(core, errata)
        check_schema(effective, load_json(controls / "schema.json"))
        validate_templates(profile,
            ROOT / "templates/semianalysis-public-findings-assessment.csv",
            ROOT / "templates/clustermax-public-security-requirements-assessment.csv")
        print("PASS: schemas, 90 control references, 40 patterns, 20 public mappings, "
              "errata application and unassessed templates; prior classification="
              + str(summary(profile["findings"])))
        print("NOT_TESTED: any provider deployment, live source freshness, or ClusterMAX conformance.")
        return 0
    except (ContractError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
