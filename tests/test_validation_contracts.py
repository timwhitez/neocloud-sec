"""Offline contract tests. Synthetic catalog fixtures are NOT provider evidence."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validation_contracts import (ContractError, check_schema, csv_text, effective_catalog,
                                  load_json, read_csv, summary, validate_profile, validate_templates)

DOMAINS = 'GOV ASM IAM API NET CMP ORC DAT KMS SSC ENG VEM TEL AIR ABU IRR RES PHY'.split()
CORE_IDS = {f'NCS-{domain}-{n:02d}' for domain in DOMAINS for n in range(1, 6)}


class ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_json(ROOT / 'controls/semianalysis-public-findings-profile.v1.json')
        cls.schema = load_json(ROOT / 'controls/semianalysis-public-findings-profile.v1.schema.json')

    def valid(self, value):
        check_schema(value, self.schema)
        validate_profile(value, CORE_IDS)

    def mutate(self, change):
        value = copy.deepcopy(self.profile)
        change(value)
        with self.assertRaises(ContractError):
            self.valid(value)

    def test_current_profile(self):
        self.valid(self.profile)

    def test_actual_counts(self):
        self.assertEqual(summary(self.profile['findings']), {'explicit': 21, 'partial': 12, 'gap': 7})

    def test_regression_original_false_totals(self):
        self.mutate(lambda p: p['coverage_summary'].update(before={'explicit': 17, 'partial': 17, 'gap': 6}))

    def test_missing_finding(self):
        self.mutate(lambda p: p['findings'].pop())

    def test_duplicate_finding(self):
        self.mutate(lambda p: p['findings'][1].update(id='SA-NC-001'))

    def test_unknown_control(self):
        self.mutate(lambda p: p['findings'][0]['mapped_controls'].append('NCS-GOV-99'))

    def test_empty_mapping(self):
        self.mutate(lambda p: p['findings'][0].update(mapped_controls=[]))

    def test_duplicate_mapping(self):
        self.mutate(lambda p: p['findings'][0]['mapped_controls'].append('NCS-ENG-01'))

    def test_missing_translation(self):
        self.mutate(lambda p: p['findings'][0]['title'].pop('zh-CN'))

    def test_empty_translation(self):
        self.mutate(lambda p: p['findings'][0]['title'].update(en=''))

    def test_bad_nested_type(self):
        self.mutate(lambda p: p['findings'].__setitem__(0, []))

    def test_unknown_field(self):
        self.mutate(lambda p: p.update(certified=True))

    def test_boolean_is_not_count(self):
        self.mutate(lambda p: p['coverage_summary']['before'].update(gap=True))

    def test_invalid_date(self):
        self.mutate(lambda p: p.update(review_date='2026-02-30'))

    def test_source_postdates_review(self):
        self.mutate(lambda p: p['sources'][0].update(observed_at='2027-01-01'))

    def test_unknown_source(self):
        self.mutate(lambda p: p['findings'][0].update(source_ids=['UNRESOLVED']))

    def test_duplicate_source(self):
        self.mutate(lambda p: p['sources'][1].update(id=p['sources'][0]['id']))

    def test_no_source(self):
        self.mutate(lambda p: p['findings'][0].update(source_ids=[]))

    def test_bad_source_url(self):
        self.mutate(lambda p: p['sources'][0].update(url='file:///etc/passwd'))

    def test_empty_evidence_text(self):
        self.mutate(lambda p: p['findings'][0]['minimum_evidence'].__setitem__(0, ''))

    def test_evidence_wrong_type(self):
        self.mutate(lambda p: p['findings'][0]['minimum_evidence'].__setitem__(0, {}))

    def test_duplicate_profile(self):
        self.mutate(lambda p: p['service_profiles'].__setitem__(1, p['service_profiles'][0]))

    def test_duplicate_dimension(self):
        self.mutate(lambda p: p['dimensions'][1].update(name='Security'))

    def test_assurance_view_drift(self):
        self.mutate(lambda p: p['findings'][0]['assurance_views'].pop())

    def test_parity_overclaim(self):
        self.mutate(lambda p: p['coverage_summary'].update(exact_clustermax_parity_claimed=True))

    def test_public_count_drift(self):
        self.mutate(lambda p: p['public_security_page_coverage'].update(mapped=21))

    def test_public_duplicate_id(self):
        self.mutate(lambda p: p['public_security_page_coverage']['items'][1].update(id='CMX-SEC-PUB-001'))

    def test_public_false_pass(self):
        self.mutate(lambda p: p['public_security_page_coverage']['items'][0].update(coverage='verified'))

    def test_unresolved_delta_drift(self):
        self.mutate(lambda p: p['public_security_page_coverage'].update(unresolved_delta=0))

    def test_duplicate_summary_drift(self):
        self.mutate(lambda p: p['coverage_summary'].update(unresolved_live_delta=0))


class InputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'input.json'

    def rejects_json(self, text):
        self.path.write_text(text)
        with self.assertRaises(ContractError):
            load_json(self.path)

    def test_duplicate_json_key(self): self.rejects_json('{"x":1,"x":2}')
    def test_nested_duplicate_key(self): self.rejects_json('{"a":{"x":1,"x":2}}')
    def test_nan(self): self.rejects_json('{"a":NaN}')
    def test_infinity(self): self.rejects_json('{"a":Infinity}')
    def test_json_array_root(self): self.rejects_json('[]')
    def test_invalid_json(self): self.rejects_json('{')

    def test_missing_input(self):
        with self.assertRaises(ContractError): load_json(self.path)

    def test_invalid_utf8(self):
        self.path.write_bytes(b'\xff')
        with self.assertRaises(ContractError): load_json(self.path)

    def test_remote_schema_ref_denied(self):
        with self.assertRaises(ContractError):
            check_schema({}, {'$schema':'https://json-schema.org/draft/2020-12/schema', '$ref':'https://example.invalid/schema'})

    def test_file_schema_ref_denied(self):
        with self.assertRaises(ContractError):
            check_schema({}, {'$schema':'https://json-schema.org/draft/2020-12/schema', '$ref':'file:///etc/passwd'})

    def test_missing_schema_reference(self):
        with self.assertRaises(ContractError):
            check_schema({}, {'$schema':'https://json-schema.org/draft/2020-12/schema', '$ref':'#/$defs/missing'})

    def test_wrong_schema_dialect(self):
        with self.assertRaises(ContractError): check_schema({}, {'type':'object'})

    def test_missing_dependency_is_not_success(self):
        import builtins
        original = builtins.__import__
        def unavailable(name, *args, **kwargs):
            if name == "jsonschema":
                raise ImportError("test fixture")
            return original(name, *args, **kwargs)
        with patch("builtins.__import__", side_effect=unavailable):
            with self.assertRaises(ContractError):
                check_schema({}, {"$schema":"https://json-schema.org/draft/2020-12/schema"})

    def test_schema_type_enforced(self):
        with self.assertRaises(ContractError):
            check_schema('not an object', {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object'})

    def rejects_csv(self, text):
        self.path.write_text(text)
        with self.assertRaises(ContractError): read_csv(self.path)

    def test_duplicate_csv_header(self): self.rejects_csv('a,a\n1,2\n')
    def test_empty_csv_header(self): self.rejects_csv('a,\n1,2\n')
    def test_long_csv_row(self): self.rejects_csv('a,b\n1,2,3\n')
    def test_short_csv_row(self): self.rejects_csv('a,b\n1\n')
    def test_bad_csv_quote(self): self.rejects_csv('a,b\n"unfinished\n')


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_json(ROOT / 'controls/semianalysis-public-findings-profile.v1.json')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.article = Path(self.temp.name)/'article.csv'
        self.public = Path(self.temp.name)/'public.csv'
        self.article.write_bytes((ROOT/'templates/semianalysis-public-findings-assessment.csv').read_bytes())
        self.public.write_bytes((ROOT/'templates/clustermax-public-security-requirements-assessment.csv').read_bytes())

    def mutate(self, path, change):
        fields, rows = read_csv(path)
        change(rows)
        path.write_text(csv_text(fields, rows))
        with self.assertRaises(ContractError): validate_templates(self.profile, self.article, self.public)

    def test_real_templates(self): validate_templates(self.profile, self.article, self.public)
    def test_mapping_drift(self): self.mutate(self.article, lambda r:r[0].update(core_controls='NCS-GOV-01'))
    def test_public_mapping_drift(self): self.mutate(self.public, lambda r:r[0].update(core_controls='NCS-GOV-01'))
    def test_severity_drift(self): self.mutate(self.article, lambda r:r[0].update(severity='low'))
    def test_public_title_drift(self): self.mutate(self.public, lambda r:r[0].update(criterion_title='Wrong'))
    def test_false_pass(self): self.mutate(self.article, lambda r:r[0].update(tenant_blackbox_result='PASS'))
    def test_false_verified(self): self.mutate(self.article, lambda r:r[0].update(state='VERIFIED'))
    def test_public_false_pass(self): self.mutate(self.public, lambda r:r[0].update(verification_result='PASS'))
    def test_live_evidence_in_template(self): self.mutate(self.article, lambda r:r[0].update(evidence_ids='PRIVATE-123'))
    def test_duplicate_assessment(self): self.mutate(self.article, lambda r:r[1].update(assessment_id=r[0]['assessment_id']))
    def test_missing_row(self): self.mutate(self.article, lambda r:r.pop())


class ErrataTests(unittest.TestCase):
    def setUp(self):
        # Deliberately small synthetic unit fixture; not the deployed or full repository catalog.
        self.core = {'catalog_id':'NCS-BASELINE','version':'1.0.0-draft.1','controls':[
            {'id':'NCS-CMP-02','tier':'T0','requirement':{'en':'original','zh-CN':'原文'}}]}
        self.errata = {'base_catalog_id':'NCS-BASELINE','base_catalog_version':'1.0.0-draft.1','corrections':[
            {'erratum_id':'E-1','control_id':'NCS-CMP-02','field':'requirement','replacement':{'en':'corrected','zh-CN':'修正'}}]}

    def rejects(self, change):
        change(self.errata)
        with self.assertRaises(ContractError): effective_catalog(self.core, self.errata)

    def test_applies_without_mutating_inputs(self):
        original = copy.deepcopy(self.core)
        result = effective_catalog(self.core, self.errata)
        self.assertEqual(result['controls'][0]['requirement']['en'],'corrected')
        self.assertEqual(result['controls'][0]['tier'],'T0')
        self.assertEqual(self.core,original)
        self.assertEqual(result,effective_catalog(self.core,self.errata))

    def test_actual_errata_schema_and_replacement(self):
        errata = load_json(ROOT / "controls/neocloud-security-baseline.v1.errata.json")
        schema = load_json(ROOT / "controls/neocloud-security-baseline.v1.errata.schema.json")
        check_schema(errata, schema)
        result = effective_catalog(self.core, errata)
        self.assertIn("never represent scheduler-level time-slicing", result["controls"][0]["requirement"]["en"])

    def test_version_mismatch(self): self.rejects(lambda e:e.update(base_catalog_version='2.0.0'))
    def test_catalog_id_mismatch(self): self.rejects(lambda e:e.update(base_catalog_id='OTHER'))
    def test_unknown_target(self): self.rejects(lambda e:e['corrections'][0].update(control_id='NCS-FAKE-01'))
    def test_tier_change_rejected(self): self.rejects(lambda e:e['corrections'][0].update(field='tier'))
    def test_missing_translation(self): self.rejects(lambda e:e['corrections'][0]['replacement'].pop('zh-CN'))
    def test_blank_translation(self): self.rejects(lambda e:e['corrections'][0]['replacement'].update(en=' '))
    def test_duplicate_erratum(self): self.rejects(lambda e:e['corrections'].append(copy.deepcopy(e['corrections'][0])))
    def test_conflicting_target(self):
        self.rejects(lambda e:e['corrections'].append(dict(e['corrections'][0],erratum_id='E-2')))


if __name__ == '__main__':
    unittest.main()
