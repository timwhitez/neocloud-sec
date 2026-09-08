"""Synthetic metadata regressions; no vulnerability or infrastructure execution."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_advisory_triage as triage

AS_OF = date(2026, 9, 8)
EXAMPLE = ROOT / "templates/advisory-triage.example.json"


def document() -> dict:
    return copy.deepcopy(json.loads(EXAMPLE.read_text(encoding="utf-8")))


def assessed(disposition: str = "REMEDIATED") -> dict:
    doc = document()
    doc["records"][0].update(
        applicability="NOT_AFFECTED" if disposition == "NOT_APPLICABLE" else "AFFECTED",
        disposition=disposition, owner="synthetic-owner", reviewer="synthetic-reviewer",
        verification_result="PASS", evidence_ids=["synthetic-evidence-1"],
        verified_on="2026-09-08", valid_until="2026-09-16",
        version_and_configuration="Synthetic fixture; not an actual version assessment",
    )
    return doc


class TriageTests(unittest.TestCase):
    def test_example_is_unassessed(self):
        doc = document()
        triage.validate(doc, AS_OF)
        self.assertEqual(doc["records"][0]["applicability"], "UNKNOWN")
        self.assertEqual(doc["records"][0]["verification_result"], "NOT_TESTED")
        self.assertEqual(doc["records"][0]["evidence_ids"], [])

    def test_recorded_remediation(self):
        triage.validate(assessed(), AS_OF)

    def test_recorded_mitigation(self):
        triage.validate(assessed("MITIGATED"), AS_OF)

    def test_recorded_nonapplicability(self):
        triage.validate(assessed("NOT_APPLICABLE"), AS_OF)

    def test_open_failed_assessment(self):
        doc = document()
        doc["records"][0].update(applicability="AFFECTED", verification_result="FAIL")
        triage.validate(doc, AS_OF)

    def test_living_source_unknown_publication(self):
        doc = document()
        doc["records"][0]["source_published_on"] = None
        triage.validate(doc, AS_OF)

    def test_duplicate_json_keys_nested(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.json"
            path.write_text('{"records":[{"id":"one","id":"two"}]}')
            with self.assertRaises(triage.TriageError):
                triage.load_document(path)

    def test_nonfinite_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nan.json"
            for constant in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(constant=constant):
                    path.write_text('{"number":' + constant + '}')
                    with self.assertRaises(triage.TriageError):
                        triage.load_document(path)

    def test_duplicate_record_ids(self):
        doc = document()
        doc["records"].append(copy.deepcopy(doc["records"][0]))
        with self.assertRaises(triage.TriageError):
            triage.validate(doc, AS_OF)

    def test_missing_record_field(self):
        doc = document()
        del doc["records"][0]["scope"]
        with self.assertRaises(triage.TriageError):
            triage.validate(doc, AS_OF)

    def test_unknown_record_field(self):
        doc = document()
        doc["records"][0]["automatically_verified"] = True
        with self.assertRaises(triage.TriageError):
            triage.validate(doc, AS_OF)

    def test_invalid_top_level(self):
        for value in (None, [], {}, {"format_version": "2", "reviewed_on": "2026-09-08", "records": []}):
            with self.subTest(value=value), self.assertRaises(triage.TriageError):
                triage.validate(value, AS_OF)

    def test_empty_records(self):
        doc = document()
        doc["records"] = []
        with self.assertRaises(triage.TriageError):
            triage.validate(doc, AS_OF)

    def test_future_review(self):
        doc = document()
        doc["reviewed_on"] = "2026-09-09"
        with self.assertRaises(triage.TriageError):
            triage.validate(doc, AS_OF)

    def test_invalid_date_formats(self):
        for value in ("20260908", "2026-09-08T00:00:00Z", "2026-02-30", None, 20260908):
            with self.subTest(value=value), self.assertRaises(ValueError):
                triage.iso_date(value)

    def run_cli(self, path: Path, as_of: str = "2026-09-08"):
        return subprocess.run([sys.executable, str(ROOT / "scripts/validate_advisory_triage.py"),
                               str(path), "--as-of", as_of], capture_output=True, text=True,
                              timeout=10, check=False)

    def test_cli_example_replay(self):
        result = self.run_cli(EXAMPLE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("AS OF 2026-09-08", result.stdout)
        self.assertIn("remediation NOT verified", result.stdout)

    def test_cli_overdue_replay_fails(self):
        result = self.run_cli(EXAMPLE, "2026-09-15")
        self.assertEqual(result.returncode, 1)
        self.assertIn("due or overdue", result.stderr)

    def test_cli_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli(Path(folder) / "missing.json")
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)

    def test_cli_malformed_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text("{")
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)

    def test_cli_invalid_encoding(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_bytes(b"\xff\xfe")
            self.assertEqual(self.run_cli(path).returncode, 1)


# Each independent mutation is a separately counted unittest test.
CASES = {
    "unknown_cannot_be_remediated": {"applicability": "UNKNOWN"},
    "remediation_requires_pass": {"verification_result": "FAIL"},
    "missing_evidence": {"evidence_ids": []},
    "malformed_evidence": {"evidence_ids": [None]},
    "duplicate_evidence": {"evidence_ids": ["e1", "e1"]},
    "missing_reviewer": {"reviewer": ""},
    "self_review": {"reviewer": "SYNTHETIC-OWNER"},
    "unassigned_owner": {"owner": "UNASSIGNED"},
    "unassigned_reviewer": {"reviewer": "UNASSIGNED"},
    "future_verification": {"verified_on": "2026-09-09"},
    "expired_verification": {"valid_until": "2026-09-08"},
    "review_after_expiry": {"next_review_on": "2026-09-17"},
    "overdue_review": {"next_review_on": "2026-09-08"},
    "future_source_access": {"source_accessed_on": "2026-09-09"},
    "publication_after_access": {"source_published_on": "2026-09-09"},
    "blank_scope": {"scope": " "},
    "padded_id": {"id": " padded "},
    "missing_configuration": {"version_and_configuration": ""},
    "nonapplicability_mismatch": {"disposition": "NOT_APPLICABLE"},
    "unknown_disposition": {"disposition": "ACCEPTED_RISK"},
    "unknown_result": {"verification_result": "GREEN"},
    "unknown_applicability": {"applicability": "PROBABLY"},
    "http_source": {"source_url": "http://example.com/advisory"},
    "local_source": {"source_url": "file:///etc/passwd"},
    "credentialed_source": {"source_url": "https://user:secret@example.com/advisory"},
    "whitespace_source": {"source_url": "https://example.com/a b"},
    "nonpass_validity_claim": {"disposition": "OPEN", "verification_result": "NOT_TESTED"},
}


def negative_case(changes: dict):
    def test(self):
        doc = assessed()
        doc["records"][0].update(copy.deepcopy(changes))
        with self.assertRaises(ValueError):
            triage.validate(doc, AS_OF)
    return test


for name, changes in CASES.items():
    setattr(TriageTests, "test_reject_" + name, negative_case(changes))


if __name__ == "__main__":
    unittest.main()
