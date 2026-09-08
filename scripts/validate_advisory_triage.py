#!/usr/bin/env python3
"""Check advisory-triage metadata offline, not vulnerabilities or remediation truth."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

FIELDS = {
    "id", "product", "source_url", "source_published_on", "source_accessed_on",
    "scope", "version_and_configuration", "applicability", "disposition", "owner",
    "rationale", "next_review_on", "evidence_ids", "verification_result", "reviewer",
    "verified_on", "valid_until",
}


class TriageError(ValueError):
    """Malformed or inconsistent triage metadata."""


def iso_date(value: object) -> date:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise TriageError("expected YYYY-MM-DD date")
    return date.fromisoformat(value)


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise TriageError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise TriageError(f"non-finite JSON number: {value}")


def load_document(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TriageError(message)


def validate(document: object, as_of: date) -> None:
    """Fail on inconsistent records. Never fetch URLs or infer safe versions."""
    require(type(as_of) is date, "as_of must be a date")
    require(isinstance(document, dict), "document must be an object")
    require(set(document) == {"format_version", "reviewed_on", "records"}, "unexpected document fields")
    require(document["format_version"] == "1", "unsupported format_version")
    reviewed = iso_date(document["reviewed_on"])
    require(reviewed <= as_of, "review is future-dated")
    rows = document["records"]
    require(isinstance(rows, list) and bool(rows), "records must be a non-empty array")
    seen: set[str] = set()
    for index, row in enumerate(rows, 1):
        prefix = f"record {index}: "
        require(isinstance(row, dict) and set(row) == FIELDS, prefix + "unexpected record fields")
        for key in ("id", "product", "source_url", "scope", "version_and_configuration",
                    "applicability", "disposition", "owner", "rationale", "verification_result"):
            value = row[key]
            require(isinstance(value, str) and bool(value.strip()) and value == value.strip(),
                    prefix + f"{key} must be non-empty, unpadded text")
        require(row["id"] not in seen, prefix + "duplicate record id")
        seen.add(row["id"])
        url = urlsplit(row["source_url"])
        require(url.scheme == "https" and bool(url.hostname) and not url.username and not url.password
                and not any(c.isspace() or ord(c) < 32 for c in row["source_url"]),
                prefix + "source_url must be an HTTPS locator without credentials or whitespace")
        accessed = iso_date(row["source_accessed_on"])
        require(accessed <= reviewed, prefix + "source access follows review")
        if row["source_published_on"] is not None:
            require(iso_date(row["source_published_on"]) <= accessed, prefix + "source publication follows access")
        next_review = iso_date(row["next_review_on"])
        require(next_review > as_of, prefix + "next review is due or overdue")
        require(row["applicability"] in {"UNKNOWN", "AFFECTED", "NOT_AFFECTED"}, prefix + "unknown applicability")
        require(row["disposition"] in {"OPEN", "MITIGATED", "REMEDIATED", "NOT_APPLICABLE"}, prefix + "unknown disposition")
        require(row["verification_result"] in {"PASS", "FAIL", "INCONCLUSIVE", "NOT_TESTED"}, prefix + "unknown result")
        evidence = row["evidence_ids"]
        require(isinstance(evidence, list) and all(isinstance(e, str) and bool(e.strip())
                and e == e.strip() for e in evidence), prefix + "evidence_ids must contain non-empty strings")
        require(len(evidence) == len(set(evidence)), prefix + "duplicate evidence id")
        require(isinstance(row["reviewer"], str) and row["reviewer"] == row["reviewer"].strip(), prefix + "invalid reviewer")
        attested = row["verification_result"] == "PASS"
        if attested:
            require(row["applicability"] != "UNKNOWN", prefix + "UNKNOWN cannot have PASS")
            require(bool(evidence) and bool(row["reviewer"]) and row["owner"].casefold() != "unassigned"
                    and row["reviewer"].casefold() != "unassigned",
                    prefix + "PASS requires evidence, assigned owner and reviewer")
            require(row["owner"].casefold() != row["reviewer"].casefold(), prefix + "owner cannot self-review")
            verified = iso_date(row["verified_on"])
            expires = iso_date(row["valid_until"])
            require(verified <= reviewed <= as_of < expires, prefix + "verification is future-dated or expired")
            require(next_review <= expires, prefix + "next review exceeds evidence validity")
        else:
            require(row["verified_on"] is None and row["valid_until"] is None,
                    prefix + "non-PASS records must not carry verification validity dates")
        if row["disposition"] != "OPEN":
            expected = "NOT_AFFECTED" if row["disposition"] == "NOT_APPLICABLE" else "AFFECTED"
            require(row["applicability"] == expected and attested,
                    prefix + "disposition requires matching applicability and current recorded PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json", type=Path)
    parser.add_argument("--as-of", type=iso_date, default=datetime.now(timezone.utc).date(),
                        help="UTC assessment date; a historical date is replay, not a current assessment")
    args = parser.parse_args()
    try:
        validate(load_document(args.json), args.as_of)
    except (ValueError, OSError, UnicodeError, RecursionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Metadata consistent AS OF {args.as_of}; sources, versions, evidence authenticity, reviewer independence and remediation NOT verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
