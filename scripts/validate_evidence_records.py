#!/usr/bin/env python3
"""Offline evidence-record checks, not authentication or service certification."""
from __future__ import annotations
import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RESULTS = {"PASS", "FAIL", "INCONCLUSIVE", "NOT_TESTED"}
STATES = {"PROPOSED", "READY", "IMPLEMENTED", "CANDIDATE_DONE", "VERIFIED"}
DOMAINS = "GOV ASM IAM API NET CMP ORC DAT KMS SSC ENG VEM TEL AIR ABU IRR RES PHY".split()
CONTROL = re.compile(r"NCS-(?:" + "|".join(DOMAINS) + r")-0[1-5]\Z")


class EvidenceInputError(ValueError):
    """Invalid CSV structure or required record fields."""


def read_records(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        fields = next(reader, [])
        if not fields or any(not f or f != f.strip() for f in fields):
            raise EvidenceInputError("empty or whitespace-padded CSV header")
        if len(fields) != len(set(fields)):
            raise EvidenceInputError("duplicate CSV header")
        if not {"evidence_id", "state", "verification_result"}.issubset(fields):
            raise EvidenceInputError("missing evidence_id, state or verification_result")
        rows = []
        seen = set()
        for values in reader:
            if len(values) != len(fields):
                raise EvidenceInputError(f"line {reader.line_num}: expected {len(fields)} fields, got {len(values)}")
            row = dict(zip(fields, values, strict=True))
            key = row["evidence_id"].strip()
            if not key or key in seen:
                raise EvidenceInputError(f"line {reader.line_num}: empty or duplicate evidence ID")
            seen.add(key)
            rows.append(row)
        if not rows:
            raise EvidenceInputError("no evidence records")
        return rows


def evidence_record_errors(record: dict[str, str], now: datetime) -> list[str]:
    """Validate a live evidence *record*, not the truth or completeness of its evidence.

    PASS results need timezone-aware observation/expiry as well as
    a scoped assertion and recorded verification; no network or file URLs are followed.
    """
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    errors: list[str] = []
    if record.get("verification_result") not in RESULTS:
        errors.append("unknown verification result")
    if record.get("state") not in STATES:
        errors.append("unknown lifecycle state")
    if record.get("state") == "VERIFIED" and record.get("verification_result") != "PASS":
        errors.append("VERIFIED requires PASS")
    if record.get("verification_result") != "PASS":
        return errors
    for key in ("control_id", "service", "service_profile", "environment", "region_scope", "asset_scope",
                "tenant_scope", "version_scope", "assertion", "test_id", "collector", "verifier",
                "independence_basis", "storage_uri", "integrity_hash", "invalidation_triggers"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            errors.append(f"PASS requires {key}")
    if not CONTROL.fullmatch(record.get("control_id", "")):
        errors.append("invalid control_id")
    if record.get("collector", "").casefold().strip() == record.get("verifier", "").casefold().strip():
        errors.append("collector and verifier must differ; distinct names alone do not prove independence")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", record.get("integrity_hash", "")):
        errors.append("integrity_hash must be sha256:<64 lowercase hex>; hash is not a signature")
    times = {}
    for key in ("observed_at", "verified_at", "valid_until"):
        try:
            value = record.get(key, "")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
                raise ValueError("expected RFC3339 timestamp")
            times[key] = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
        except (ValueError, TypeError):
            errors.append(f"{key}: invalid timezone-aware timestamp")
    if len(times) == 3 and not (times["observed_at"] <= times["verified_at"] <= now < times["valid_until"]):
        errors.append("PASS evidence is future-dated, reversed, or expired")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    try:
        rows = read_records(args.csv)
        now = datetime.now(timezone.utc)
        errors = [f"record {row['evidence_id']}: {error}" for row in rows
                  for error in evidence_record_errors(row, now)]
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("Record structure and dates consistent; evidence authenticity, reviewer independence and service conformance NOT verified.")
        return 0
    except (EvidenceInputError, OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
