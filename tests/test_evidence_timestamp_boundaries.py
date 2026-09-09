"""Offline timestamp regressions; all records and identities are synthetic."""
from __future__ import annotations
import csv
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Do not import TestCase classes: unittest would count those tests a second time.
from test_evidence_records import NOW, ROOT, record
from validate_evidence_records import evidence_record_errors

FIELDS = ('observed_at', 'verified_at', 'valid_until')


class TimestampBoundaryTests(unittest.TestCase):
    def assert_bad_time(self, field, value):
        r = record()
        r[field] = value
        self.assertIn(f'{field}: invalid timezone-aware timestamp', evidence_record_errors(r, NOW))

    def test_offset_minutes_must_not_be_normalized(self):
        for field in FIELDS:
            for offset in ('+00:60', '+00:99', '-00:60', '-00:99', '+12:60', '-12:99'):
                with self.subTest(field=field, offset=offset):
                    self.assert_bad_time(field, '2026-09-05T12:00:00' + offset)

    def test_offset_hours_out_of_range(self):
        for offset in ('+24:00', '-24:00', '+99:00', '-99:00'):
            with self.subTest(offset=offset):
                self.assert_bad_time('verified_at', '2026-09-05T11:00:00' + offset)

    def test_all_legal_numeric_offsets_preserve_the_instant(self):
        instant = datetime(2026, 9, 5, 11, tzinfo=timezone.utc)
        for sign in (-1, 1):
            for hours in range(24):
                for minutes in range(60):
                    offset = timezone(sign * timedelta(hours=hours, minutes=minutes))
                    r = record()
                    r['verified_at'] = instant.astimezone(offset).isoformat()
                    with self.subTest(timestamp=r['verified_at']):
                        self.assertEqual(evidence_record_errors(r, NOW), [])

    def test_microsecond_precision_is_preserved(self):
        r = record()
        r['observed_at'] = '2026-09-05T11:00:00.000002Z'
        r['verified_at'] = '2026-09-05T11:00:00.000001Z'
        self.assertIn('PASS evidence is future-dated, reversed, or expired', evidence_record_errors(r, NOW))

    def test_valid_fractional_precision_one_through_six(self):
        for digits in range(1, 7):
            r = record()
            r['verified_at'] = '2026-09-05T11:00:00.' + '1' * digits + 'Z'
            with self.subTest(digits=digits):
                self.assertEqual(evidence_record_errors(r, NOW), [])

    def test_submicrosecond_reversal_cannot_be_truncated_to_equal(self):
        r = record()
        r['observed_at'] = '2026-09-05T11:00:00.0000009Z'
        r['verified_at'] = '2026-09-05T11:00:00.0000001Z'
        errors = evidence_record_errors(r, NOW)
        for field in ('observed_at', 'verified_at'):
            self.assertIn(f'{field}: invalid timezone-aware timestamp', errors)

    def test_overprecision_is_explicitly_unsupported_even_for_trailing_zeros(self):
        for field in FIELDS:
            for fraction in ('0000000', '123456789'):
                with self.subTest(field=field, fraction=fraction):
                    self.assert_bad_time(field, '2026-09-05T11:00:00.' + fraction + 'Z')

    def test_utc_conversion_underflow_is_a_record_error(self):
        for field in FIELDS:
            with self.subTest(field=field):
                self.assert_bad_time(field, '0001-01-01T00:00:00+01:00')

    def test_utc_conversion_overflow_is_a_record_error(self):
        for field in FIELDS:
            with self.subTest(field=field):
                self.assert_bad_time(field, '9999-12-31T23:59:59-01:00')

    def test_representable_year_extremes_remain_supported(self):
        r = record()
        r['observed_at'] = '0001-01-01T00:00:00Z'
        r['valid_until'] = '9999-12-31T23:59:59Z'
        self.assertEqual(evidence_record_errors(r, NOW), [])

    def test_minus_zero_still_denotes_a_known_utc_instant(self):
        # RFC 3339 4.3: UTC is known even if the local offset is unknown.
        # RFC 9557 2.2 updates the preferred spelling; it does not invalidate UTC.
        for offset in ('Z', '+00:00', '-00:00'):
            r = record()
            r['verified_at'] = '2026-09-05T11:00:00' + offset
            with self.subTest(offset=offset):
                self.assertEqual(evidence_record_errors(r, NOW), [])

    def test_invalid_calendar_dates(self):
        for date in ('2026-02-29', '2026-13-01', '0000-01-01', '2026-04-31'):
            with self.subTest(date=date):
                self.assert_bad_time('verified_at', date + 'T11:00:00Z')

    def test_unsupported_clock_and_offset_syntax(self):
        for value in ('2026-09-05T24:00:00Z', '2026-09-05T11:60:00Z',
                      '2026-09-05T11:00:60Z', '2026-09-05T11:00:00+0100',
                      '2026-09-05T11:00:00+01:00:30', '2026-09-05T11:00:00,1Z',
                      '2026-09-05 11:00:00Z', '2026-09-05T11:00:00.Z',
                      '2026-09-05T11:00:00Z\n'):
            with self.subTest(value=value):
                self.assert_bad_time('verified_at', value)

    def test_non_pass_records_keep_the_existing_partial_metadata_contract(self):
        for result in ('NOT_TESTED', 'FAIL', 'INCONCLUSIVE'):
            r = {'state': 'PROPOSED', 'verification_result': result, 'observed_at': 'not collected'}
            with self.subTest(result=result):
                self.assertEqual(evidence_record_errors(r, NOW), [])

    def test_non_utc_now_keeps_the_same_ordering(self):
        local_now = NOW.astimezone(timezone(timedelta(hours=8)))
        self.assertEqual(evidence_record_errors(record(), local_now), [])


class TimestampCliTests(unittest.TestCase):
    def check_cli_error(self, field, timestamp):
        r = record()
        r[field] = timestamp
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.csv'
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(r))
                writer.writeheader()
                writer.writerow(r)
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts/validate_evidence_records.py'), str(path)],
                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(f'{field}: invalid timezone-aware timestamp', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertNotIn('Record structure and dates consistent', result.stdout)

    def test_invalid_offset_cli(self):
        self.check_cli_error('verified_at', '2026-09-05T12:00:00+00:60')

    def test_underflow_cli(self):
        self.check_cli_error('observed_at', '0001-01-01T00:00:00+01:00')

    def test_overflow_cli(self):
        self.check_cli_error('valid_until', '9999-12-31T23:59:59-01:00')

    def test_overprecision_cli(self):
        self.check_cli_error('verified_at', '2026-09-05T11:00:00.0000001Z')


if __name__ == '__main__':
    unittest.main()
