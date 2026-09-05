"""Synthetic evidence-metadata tests only; no live service or network access."""
from __future__ import annotations
import csv
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_evidence_records import EvidenceInputError, evidence_record_errors, read_records

NOW = datetime(2026, 9, 5, 12, tzinfo=timezone.utc)


def record() -> dict[str, str]:
    return dict(evidence_id='SYNTHETIC-001', control_id='NCS-CMP-02', service='synthetic-service',
                service_profile='GPU-IaaS', environment='test', region_scope='synthetic-region',
                asset_scope='synthetic-node', tenant_scope='synthetic-tenants', version_scope='fixture',
                assertion='synthetic marker denied', test_id='fixture-test', collector='fixture-operator',
                verifier='fixture-reviewer', independence_basis='synthetic separate reviewer',
                storage_uri='urn:synthetic:evidence', integrity_hash='sha256:' + '0' * 64,
                invalidation_triggers='configuration change', verification_result='PASS', state='VERIFIED',
                observed_at='2026-09-05T10:00:00Z', verified_at='2026-09-05T11:00:00Z',
                valid_until='2026-09-06T10:00:00Z')


class RecordTests(unittest.TestCase):
    def test_complete_synthetic_metadata(self):
        self.assertEqual(evidence_record_errors(record(), NOW), [])

    def test_unassessed_is_not_verified(self):
        r = {'state': 'PROPOSED', 'verification_result': 'NOT_TESTED'}
        self.assertEqual(evidence_record_errors(r, NOW), [])
        r['state'] = 'VERIFIED'
        self.assertTrue(evidence_record_errors(r, NOW))

    def test_invalid_verdict_and_lifecycle(self):
        for key, value in [('state', 'DONE'), ('verification_result', 'NOT_REVIEWED')]:
            r = record(); r[key] = value
            with self.subTest(key=key): self.assertTrue(evidence_record_errors(r, NOW))

    def test_expiry_boundary(self):
        r = record(); r['valid_until'] = NOW.isoformat()
        self.assertTrue(evidence_record_errors(r, NOW))

    def test_future_and_reversed_times(self):
        for key, value in [('observed_at', '2026-09-07T00:00:00Z'),
                           ('verified_at', '2026-09-05T09:00:00Z')]:
            r = record(); r[key] = value
            with self.subTest(key=key): self.assertTrue(evidence_record_errors(r, NOW))

    def test_invalid_or_naive_timestamps(self):
        for value in ('2026-09-05', '2026-09-05T11:00:00', '2026-02-30T11:00:00Z'):
            r = record(); r['verified_at'] = value
            with self.subTest(value=value): self.assertTrue(evidence_record_errors(r, NOW))
        with self.assertRaises(ValueError): evidence_record_errors(record(), datetime(2026, 9, 5))

    def test_timezone_offsets(self):
        r = record(); r['verified_at'] = '2026-09-05T20:00:00+09:00'
        self.assertEqual(evidence_record_errors(r, NOW), [])

    def test_self_verification(self):
        r = record(); r['verifier'] = ' FIXTURE-OPERATOR '
        self.assertTrue(evidence_record_errors(r, NOW))

    def test_missing_required_scope(self):
        for key in ('environment', 'region_scope', 'test_id', 'independence_basis', 'version_scope',
                    'service_profile', 'asset_scope', 'assertion', 'invalidation_triggers'):
            r = record(); del r[key]
            with self.subTest(key=key): self.assertTrue(evidence_record_errors(r, NOW))

    def test_hash_and_control_contract(self):
        for key, value in [('integrity_hash', 'not-a-hash'), ('control_id', 'NCS-FAKE-01'),
                           ('control_id', 'NCS-CMP-99')]:
            r = record(); r[key] = value
            with self.subTest(key=key, value=value): self.assertTrue(evidence_record_errors(r, NOW))


class CsvTests(unittest.TestCase):
    def test_malformed_widths_headers_quotes_and_empty(self):
        cases = ['', 'evidence_id,state,verification_result\n',
                 'evidence_id,state,verification_result\nx,PROPOSED\n',
                 'evidence_id,state,verification_result\nx,PROPOSED,NOT_TESTED,extra\n',
                 'evidence_id,state,verification_result,state\nx,PROPOSED,NOT_TESTED,PROPOSED\n',
                 'evidence_id, state,verification_result\nx,PROPOSED,NOT_TESTED\n',
                 'evidence_id,state,verification_result\n"unfinished']
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'fixture.csv'
            for text in cases:
                path.write_text(text)
                with self.subTest(text=text), self.assertRaises((EvidenceInputError, csv.Error)):
                    read_records(path)

    def test_empty_and_duplicate_evidence_ids(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'fixture.csv'
            for body in (' ,PROPOSED,NOT_TESTED\n', 'same,PROPOSED,NOT_TESTED\n same ,PROPOSED,NOT_TESTED\n'):
                path.write_text('evidence_id,state,verification_result\n' + body)
                with self.subTest(body=body), self.assertRaises(EvidenceInputError):
                    read_records(path)

    def test_bom_quotes_and_multiline(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'fixture.csv'
            path.write_text('\ufeffevidence_id,state,verification_result,notes\nx,PROPOSED,NOT_TESTED,"a,b\nc"\n')
            self.assertEqual(read_records(path)[0]['notes'], 'a,b\nc')

    def test_distributed_template_stays_unassessed(self):
        rows = read_records(ROOT / 'templates/evidence-record.example.csv')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['state'], 'PROPOSED')
        self.assertEqual(rows[0]['verification_result'], 'NOT_TESTED')


class CliTests(unittest.TestCase):
    def run_cli(self, path: Path):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/validate_evidence_records.py'), str(path)],
                              capture_output=True, text=True, timeout=10)

    def test_example_success_is_not_provider_pass(self):
        result = self.run_cli(ROOT / 'templates/evidence-record.example.csv')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('NOT verified', result.stdout)

    def test_missing_file_is_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            result = self.run_cli(Path(d) / 'missing.csv')
            self.assertEqual(result.returncode, 2)
            self.assertIn('ERROR:', result.stderr)

    def test_invalid_utf8_is_diagnostic(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'fixture.csv'; path.write_bytes(b'\xff')
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)

    def test_fake_verified_record_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'fixture.csv'
            path.write_text('evidence_id,state,verification_result\nx,VERIFIED,PASS\n')
            result = self.run_cli(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn('PASS requires', result.stderr)


if __name__ == '__main__':
    unittest.main()
