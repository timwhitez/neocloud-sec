#!/usr/bin/env python3
"""Emit an effective catalog bundle after validating and applying project errata.

No file is modified. Redirect stdout to a private output location. Digests
identify input bytes; they do not authenticate a publisher or attest a service.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from validation_contracts import ContractError, check_schema, effective_catalog, load_json, require

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        folder = ROOT / "controls"
        base_path = folder / "neocloud-security-baseline.v1.json"
        errata_path = folder / "neocloud-security-baseline.v1.errata.json"
        base_bytes, errata_bytes = base_path.read_bytes(), errata_path.read_bytes()
        base, errata = load_json(base_path), load_json(errata_path)
        require(base_path.read_bytes() == base_bytes and errata_path.read_bytes() == errata_bytes,
                "catalog inputs changed during compilation")
        schema = load_json(folder / "schema.json")
        check_schema(base, schema)
        check_schema(errata, load_json(folder / "neocloud-security-baseline.v1.errata.schema.json"))
        effective = effective_catalog(base, errata)
        check_schema(effective, schema)
        canonical = json.dumps(effective, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":"), allow_nan=False).encode("utf-8")
        bundle = {
            "artifact_type": "effective-catalog-bundle",
            "catalog": effective,
            "provenance": {
                "base_sha256": hashlib.sha256(base_bytes).hexdigest(),
                "errata_sha256": hashlib.sha256(errata_bytes).hexdigest(),
                "effective_canonical_sha256": hashlib.sha256(canonical).hexdigest(),
                "applied_errata": [x["erratum_id"] for x in errata["corrections"]],
                "canonicalization": "UTF-8; sorted keys; compact JSON; ensure_ascii=False; no newline",
                "provider_security_tested": False,
            },
        }
        print(json.dumps(bundle, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ContractError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
