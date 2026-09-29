"""Execution accounting for scripts/check_local.py. These fixtures are not provider tests."""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
VALIDATORS = (
    "validate_repository.py",
    "validate_accuracy_invariants.py",
    "validate_semianalysis_profile.py",
)
PASSING_TEST = textwrap.dedent(
    """\
    import unittest
    class T(unittest.TestCase):
        def test_ok(self):
            self.assertEqual(1 + 1, 2)
    """
)
FAILING_TEST = textwrap.dedent(
    """\
    import unittest
    class T(unittest.TestCase):
        def test_bad(self):
            self.fail("synthetic failure")
    """
)
ALL_SKIP = textwrap.dedent(
    """\
    import unittest
    @unittest.skip("synthetic fixture")
    class T(unittest.TestCase):
        def test_placeholder(self):
            pass
    """
)
MIXED_OPTIONAL = textwrap.dedent(
    """\
    import unittest
    class T(unittest.TestCase):
        def test_required(self):
            self.assertTrue(True)

        @unittest.skip("synthetic optional")
        def test_optional(self):
            self.fail("optional body must not run")
    T.test_optional.neocloud_optional = True
    """
)
REQUIRED_SKIP = textwrap.dedent(
    """\
    import unittest
    class T(unittest.TestCase):
        def test_required(self):
            self.assertTrue(True)

        @unittest.skip("synthetic required skip")
        def test_needed(self):
            pass
    """
)
OPTIONAL_ONLY_PASS = textwrap.dedent(
    """\
    import unittest
    class T(unittest.TestCase):
        neocloud_optional = True
        def test_optional_pass(self):
            self.assertTrue(True)
    """
)
OPTIONAL_ONLY_SKIP = textwrap.dedent(
    """\
    import unittest
    @unittest.skip("synthetic optional group")
    class T(unittest.TestCase):
        neocloud_optional = True
        def test_placeholder(self):
            pass
    """
)


def load_gate():
    spec = importlib.util.spec_from_file_location(
        "neocloud_check_local", ROOT / "scripts" / "check_local.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_validators(root: Path, codes: dict[str, int] | None = None) -> None:
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    selected = codes or {name: 0 for name in VALIDATORS}
    for name in VALIDATORS:
        (scripts / name).write_text(f"raise SystemExit({selected.get(name, 0)})\n", encoding="utf-8")


def write_tests(root: Path, source: str | None) -> None:
    tests = root / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    if source is not None:
        (tests / "test_sample.py").write_text(source, encoding="utf-8")


def base_report(**overrides) -> dict:
    report = {
        "discovered": 1,
        "executed": 1,
        "required_executed": 1,
        "optional_executed": 0,
        "skipped": 0,
        "required_skipped": 0,
        "optional_skipped": 0,
        "failures": 0,
        "errors": 0,
        "unexpected_successes": 0,
        "incomplete": False,
        "error": "",
    }
    report.update(overrides)
    return report


class LocalGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = load_gate()

    def setUp(self):
        self.gate.ROOT = ROOT

    def capture(self, func):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = func()
        return code, stdout.getvalue(), stderr.getvalue()

    def gate_on(self, source: str | None, codes: dict[str, int] | None = None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_validators(root, codes)
            write_tests(root, source)
            return self.capture(lambda: self.gate.run_gate(root))

    def test_assess_policy_matrix(self):
        accepted, reason = self.gate.assess(base_report())
        self.assertTrue(accepted)
        self.assertEqual(reason, "required tests executed")

        accepted, reason = self.gate.assess(base_report(
            discovered=0, executed=0, required_executed=0,
        ))
        self.assertFalse(accepted)
        self.assertEqual(reason, "no tests discovered")

        accepted, reason = self.gate.assess(base_report(
            executed=0, required_executed=0, skipped=1, required_skipped=1,
        ))
        self.assertFalse(accepted)
        self.assertEqual(reason, "no required test body executed")

        accepted, reason = self.gate.assess(base_report(
            discovered=2, executed=1, required_executed=1, skipped=1, required_skipped=1,
        ))
        self.assertFalse(accepted)
        self.assertEqual(reason, "required test skipped")

        accepted, reason = self.gate.assess(base_report(
            discovered=2, executed=1, required_executed=1, skipped=1, optional_skipped=1,
        ))
        self.assertTrue(accepted)
        self.assertIn("optional tests skipped", reason)
        self.assertNotIn("all discovered tests executed", reason)
        self.assertNotIn("all tests executed", reason)

        accepted, reason = self.gate.assess(base_report(
            executed=0, required_executed=0, skipped=1, required_skipped=0, optional_skipped=1,
        ))
        self.assertFalse(accepted)
        self.assertEqual(reason, "no required test body executed")

        for key in ("failures", "errors", "unexpected_successes"):
            accepted, reason = self.gate.assess(base_report(**{key: 1}))
            self.assertFalse(accepted)
            self.assertEqual(reason, "unittest failures or errors")

        accepted, reason = self.gate.assess(base_report(discovered=True))
        self.assertFalse(accepted)
        self.assertEqual(reason, "unittest result is incomplete")

        accepted, reason = self.gate.assess(base_report(executed=2))
        self.assertFalse(accepted)
        self.assertEqual(reason, "unittest result is inconsistent")

        accepted, reason = self.gate.assess({"discovered": 1})
        self.assertFalse(accepted)
        self.assertEqual(reason, "unittest result is incomplete")

        accepted, reason = self.gate.assess(base_report(executed=-1))
        self.assertFalse(accepted)
        self.assertEqual(reason, "unittest result is incomplete")

        accepted, reason = self.gate.assess(base_report(
            discovered=2, executed=1, required_executed=1, not_run=1,
        ))
        self.assertFalse(accepted)
        self.assertEqual(reason, "unittest did not start every discovered test")

        accepted, reason = self.gate.assess(base_report(
            subtests_skipped=1, subtests_optional_skipped=1,
        ))
        self.assertTrue(accepted)
        self.assertIn("optional subtests skipped", reason)
        self.assertNotIn("all tests executed", reason)
        self.assertNotIn("all discovered tests executed", reason)

        accepted, reason = self.gate.assess(base_report(
            subtests_skipped=1, subtests_required_skipped=1,
        ))
        self.assertFalse(accepted)
        self.assertEqual(reason, "required subtest skipped")

    def test_source_keeps_timeout_and_does_not_hardcode_suite_size(self):
        source = (ROOT / "scripts" / "check_local.py").read_text(encoding="utf-8")
        self.assertIn("STEP_TIMEOUT_SECONDS = 120", source)
        self.assertIn('OPTIONAL_ATTRIBUTE = "neocloud_optional"', source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("170", source)
        self.assertNotIn("executed = started - skipped", source)
        self.assertNotIn("max(0", source)

    def test_docs_state_skip_contract(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        for text in (readme, contributing):
            self.assertIn("neocloud_optional", text)
            self.assertIn("no required test body executed", text)
        for text in (readme_zh, contributing):
            self.assertIn("neocloud_optional", text)
            self.assertIn("没有必需测试主体执行", text)
        self.assertIn("`NOT_TESTED`", readme)
        self.assertIn("`NOT_TESTED`", readme_zh)
        self.assertIn("required subtest", readme)
        self.assertIn("required subtest", contributing)
        self.assertIn("必需子测试", readme_zh)
        self.assertIn("必需子测试", contributing)

    def test_empty_directory_fails_and_cli_exit_is_version_specific(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_validators(root)
            write_tests(root, None)
            cli = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", str(root / "tests")],
                cwd=root,
                capture_output=True,
                text=True,
            )
            code, out, err = self.capture(lambda: self.gate.run_gate(root))
        if sys.version_info >= (3, 12):
            self.assertEqual(cli.returncode, 5)
        else:
            self.assertEqual(cli.returncode, 0)
        self.assertNotEqual(code, 0)
        self.assertIn("no tests discovered", out + err)
        self.assertNotIn("PASS:", out + err)

    def test_all_skip_cli_exits_zero_and_gate_rejects_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_validators(root)
            write_tests(root, ALL_SKIP)
            cli = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", str(root / "tests"), "-v"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            self.gate.ROOT = root
            # Explicit argv: ambient unittest arguments must not select report mode.
            code, out, err = self.capture(lambda: self.gate.main([]))
        self.assertEqual(cli.returncode, 0)
        self.assertIn("skipped", cli.stdout + cli.stderr)
        self.assertNotEqual(code, 0)
        self.assertIn("no required test body executed", out + err)
        self.assertIn("SKIP required:", err)
        self.assertNotIn("PASS:", out + err)

    def test_explicit_empty_args_do_not_rewrite_a_report_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_validators(root)
            write_tests(root, ALL_SKIP)
            target = root / "must-not-write.json"
            self.gate.ROOT = root
            old = sys.argv
            sys.argv = [str(ROOT / "scripts" / "check_local.py"), "--unittest-report", "--result", str(target)]
            try:
                code, out, err = self.capture(lambda: self.gate.main([]))
            finally:
                sys.argv = old
        self.assertNotEqual(code, 0)
        self.assertFalse(target.exists())
        self.assertIn("no required test body executed", out + err)

    def test_one_real_test_passes_without_a_fixed_count(self):
        code, out, err = self.gate_on(PASSING_TEST)
        combined = out + err
        self.assertEqual(code, 0, combined)
        self.assertIn(f"PYTHON: {sys.version.split()[0]}", out)
        self.assertIn("discovered=1 executed=1 skipped=0", out)
        self.assertIn("required_skipped=0 optional_skipped=0 failures=0 errors=0", out)
        self.assertIn("PASS: local repository checks only; no live provider assessment performed.", out)
        self.assertNotIn("170", combined)
        self.assertNotIn("NOTE:", out)

    def test_failed_test_and_import_error_fail(self):
        code, out, err = self.gate_on(FAILING_TEST)
        self.assertNotEqual(code, 0)
        self.assertIn("failures=1", out)
        self.assertIn("unittest failures or errors", out + err)
        self.assertNotIn("PASS:", out + err)
        code, out, err = self.gate_on('raise RuntimeError("synthetic import failure")\n')
        self.assertNotEqual(code, 0)
        self.assertIn("errors=1", out)
        self.assertNotIn("PASS:", out + err)

    def test_mixed_optional_skip_is_reported_and_not_full_execution(self):
        code, out, err = self.gate_on(MIXED_OPTIONAL)
        combined = out + err
        self.assertEqual(code, 0, combined)
        self.assertIn("discovered=2 executed=1 skipped=1", out)
        self.assertIn("required_skipped=0 optional_skipped=1", out)
        self.assertIn("SKIP optional:", out)
        self.assertIn("NOTE: optional tests were skipped; not all discovered tests executed.", out)
        self.assertNotIn("all tests executed", combined)
        self.assertNotIn("all discovered tests executed", combined.replace(
            "not all discovered tests executed", ""
        ))

    def test_required_skip_mixed_with_a_pass_fails(self):
        code, out, err = self.gate_on(REQUIRED_SKIP)
        self.assertNotEqual(code, 0)
        self.assertIn("required test skipped", out + err)
        self.assertIn("SKIP required:", err)
        self.assertIn("discovered=2 executed=1", out)
        self.assertNotIn("PASS:", out + err)

    def test_optional_results_do_not_replace_the_required_suite(self):
        code, out, err = self.gate_on(OPTIONAL_ONLY_PASS)
        self.assertNotEqual(code, 0)
        self.assertIn("no required test body executed", out + err)
        self.assertNotIn("PASS:", out + err)
        code, out, err = self.gate_on(OPTIONAL_ONLY_SKIP)
        self.assertNotEqual(code, 0)
        self.assertIn("no required test body executed", out + err)
        self.assertIn("SKIP optional:", out)
        self.assertNotIn("PASS:", out + err)

    def test_validator_failure_blocks_overall_pass(self):
        code, out, err = self.gate_on(
            PASSING_TEST,
            {
                "validate_repository.py": 0,
                "validate_accuracy_invariants.py": 4,
                "validate_semianalysis_profile.py": 0,
            },
        )
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("EXIT 0: validate_repository.py", out)
        self.assertIn("EXIT 4: validate_accuracy_invariants.py", out)
        self.assertIn("EXIT 0: validate_semianalysis_profile.py", out)
        self.assertIn("discovered=1 executed=1", out)
        self.assertIn("FAIL: one or more local checks failed or did not run", err)
        self.assertNotIn("PASS:", combined)

    def test_steps_use_subprocess_timeout(self):
        seen = []
        real = subprocess.run

        def spy(command, **kwargs):
            seen.append((list(command), kwargs.get("timeout")))
            return real(command, **kwargs)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_validators(root)
            write_tests(root, PASSING_TEST)
            with patch.object(self.gate.subprocess, "run", spy):
                code, out, err = self.capture(lambda: self.gate.run_gate(root))
        self.assertEqual(code, 0, out + err)
        self.assertGreaterEqual(len(seen), 4)
        self.assertTrue(all(timeout == 120 for _command, timeout in seen))
        rendered = [" ".join(command) for command, _timeout in seen]
        self.assertTrue(any("validate_repository.py" in item for item in rendered))
        self.assertTrue(any("--unittest-report" in item for item in rendered))

    def test_timeout_start_failure_and_exit_zero_are_not_pass(self):
        passing = base_report(discovered=2, executed=2, required_executed=2)

        def timeout_validator(command, **kwargs):
            if "validate_repository.py" in " ".join(command):
                raise subprocess.TimeoutExpired(command, 120)
            if "--unittest-report" in command:
                result = Path(command[command.index("--result") + 1])
                result.write_text(json.dumps(passing), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0)
            return subprocess.CompletedProcess(command, 0)

        with patch.object(self.gate.subprocess, "run", side_effect=timeout_validator):
            code, out, err = self.capture(lambda: self.gate.run_gate(ROOT))
        self.assertNotEqual(code, 0)
        self.assertIn("EXIT timeout: validate_repository.py", out)
        self.assertIn("discovered=2 executed=2", out)
        self.assertNotIn("PASS:", out + err)

        def timeout_after_writing_pass(command, **kwargs):
            if "--unittest-report" in command:
                result = Path(command[command.index("--result") + 1])
                result.write_text(json.dumps(passing), encoding="utf-8")
                raise subprocess.TimeoutExpired(command, 120)
            return subprocess.CompletedProcess(command, 0)

        with patch.object(self.gate.subprocess, "run", side_effect=timeout_after_writing_pass):
            code, out, err = self.capture(lambda: self.gate.run_gate(ROOT))
        self.assertNotEqual(code, 0)
        self.assertIn("EXIT timeout: unittest", out)
        self.assertNotIn("PASS:", out + err)

        def cannot_start(command, **kwargs):
            if "--unittest-report" in command:
                raise OSError("synthetic start failure")
            return subprocess.CompletedProcess(command, 0)

        with patch.object(self.gate.subprocess, "run", side_effect=cannot_start):
            code, out, err = self.capture(lambda: self.gate.run_gate(ROOT))
        self.assertNotEqual(code, 0)
        self.assertIn("EXIT start-failed: unittest: synthetic start failure", out)
        self.assertNotIn("PASS:", out + err)

        def exit_zero_without_result(command, **kwargs):
            return subprocess.CompletedProcess(
                command, 0, stdout="OK (skipped=1)\nPASS: local repository checks only; no live provider assessment performed.\n"
            )

        with patch.object(self.gate.subprocess, "run", side_effect=exit_zero_without_result):
            code, out, err = self.capture(lambda: self.gate.run_gate(ROOT))
        self.assertNotEqual(code, 0)
        self.assertIn("unittest result is missing", err)
        self.assertNotIn("PASS: local repository checks only", out)

        skipped = base_report(
            executed=0, required_executed=0, skipped=1, required_skipped=1,
        )

        def exit_zero_with_skip_payload(command, **kwargs):
            if "--unittest-report" in command:
                result = Path(command[command.index("--result") + 1])
                result.write_text(json.dumps(skipped), encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, stdout="OK (skipped=1)\n")

        with patch.object(self.gate.subprocess, "run", side_effect=exit_zero_with_skip_payload):
            code, out, err = self.capture(lambda: self.gate.run_gate(ROOT))
        self.assertNotEqual(code, 0)
        self.assertIn("no required test body executed", out + err)
        self.assertNotIn("PASS:", out + err)

    def test_optional_setup_class_skip_counts_each_leaf(self):
        source = PASSING_TEST + textwrap.dedent(
            """\
            class Optional(unittest.TestCase):
                neocloud_optional = True
                @classmethod
                def setUpClass(cls):
                    raise unittest.SkipTest("synthetic optional fixture unavailable")
                def test_one(self):
                    pass
                def test_two(self):
                    pass
            """
        )
        code, out, err = self.gate_on(source)
        combined = out + err
        self.assertEqual(code, 0, combined)
        self.assertIn("discovered=3 executed=1 skipped=2", out)
        self.assertIn("required_skipped=0 optional_skipped=2", out)
        self.assertIn("required_executed=1", out)
        self.assertIn("not_run=0", out)
        self.assertIn("SKIP optional:", out)
        self.assertIn("test_one", out)
        self.assertIn("test_two", out)
        self.assertIn("setUpClass:", out)
        self.assertIn("NOTE: optional tests were skipped; not all discovered tests executed.", out)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("required test skipped", combined)
        self.assertIn("PASS: local repository checks only; no live provider assessment performed.", out)

    def test_optional_subtest_skips_are_disclosed_and_non_negative(self):
        source = PASSING_TEST + textwrap.dedent(
            """\
            class Optional(unittest.TestCase):
                neocloud_optional = True
                def test_partial(self):
                    for n in range(3):
                        with self.subTest(n=n):
                            self.skipTest("synthetic optional subtest unavailable")
            """
        )
        code, out, err = self.gate_on(source)
        combined = out + err
        self.assertEqual(code, 0, combined)
        self.assertIn("discovered=2 executed=2 skipped=0", out)
        self.assertIn("required_skipped=0 optional_skipped=0", out)
        self.assertIn("subtests_skipped=3", out)
        self.assertIn("subtests_required_skipped=0", out)
        self.assertIn("subtests_optional_skipped=3", out)
        self.assertIn("required_executed=1", out)
        self.assertIn("optional_executed=1", out)
        self.assertIn("SKIP optional subtest:", out)
        self.assertIn("NOTE: optional subtests were skipped; partial coverage is not full execution.", out)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("all tests executed", combined)
        self.assertNotIn("required test skipped", combined)
        self.assertNotIn("required subtest skipped", combined)

    def test_required_setup_class_and_module_skips_still_fail(self):
        source = PASSING_TEST + textwrap.dedent(
            """\
            class Needed(unittest.TestCase):
                @classmethod
                def setUpClass(cls):
                    raise unittest.SkipTest("synthetic required fixture")
                def test_one(self):
                    pass
                def test_two(self):
                    pass
            """
        )
        code, out, err = self.gate_on(source)
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=3 executed=1 skipped=2", out)
        self.assertIn("required_skipped=2", out)
        self.assertIn("required_executed=1", out)
        self.assertIn("required test skipped", combined)
        self.assertIn("SKIP required:", err)
        self.assertIn("test_one", err)
        self.assertIn("test_two", err)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_files({
            "test_required.py": PASSING_TEST,
            "test_blocked.py": textwrap.dedent(
                """\
                import unittest
                def setUpModule():
                    raise unittest.SkipTest("synthetic required module")
                class Needed(unittest.TestCase):
                    def test_one(self):
                        pass
                    def test_two(self):
                        pass
                """
            ),
        })
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=3 executed=1 skipped=2", out)
        self.assertIn("required_skipped=2", out)
        self.assertIn("setUpModule:", err)
        self.assertIn("required test skipped", combined)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("PASS:", combined)

    def test_optional_setup_module_skip_does_not_hide_a_required_pass(self):
        code, out, err = self.gate_files({
            "test_required.py": PASSING_TEST,
            "test_optional_module.py": textwrap.dedent(
                """\
                import unittest
                def setUpModule():
                    raise unittest.SkipTest("synthetic optional module")
                class Optional(unittest.TestCase):
                    neocloud_optional = True
                    def test_one(self):
                        pass
                    def test_two(self):
                        pass
                """
            ),
        })
        combined = out + err
        self.assertEqual(code, 0, combined)
        self.assertIn("discovered=3 executed=1 skipped=2", out)
        self.assertIn("required_skipped=0 optional_skipped=2", out)
        self.assertIn("setUpModule:", out)
        self.assertIn("NOTE: optional tests were skipped; not all discovered tests executed.", out)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("required test skipped", combined)

    def test_required_subtest_skip_fails(self):
        source = PASSING_TEST + textwrap.dedent(
            """\
            class Needed(unittest.TestCase):
                def test_partial(self):
                    for n in range(2):
                        with self.subTest(n=n):
                            self.skipTest("synthetic required subtest")
            """
        )
        code, out, err = self.gate_on(source)
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=2 executed=2 skipped=0", out)
        self.assertIn("subtests_required_skipped=2", out)
        self.assertIn("subtests_optional_skipped=0", out)
        self.assertIn("required_executed=2", out)
        self.assertIn("required subtest skipped", combined)
        self.assertIn("SKIP required subtest:", err)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("PASS:", combined)

    def test_setup_errors_are_not_body_execution(self):
        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                @classmethod
                def setUpClass(cls):
                    raise RuntimeError("synthetic class fixture error")
                def test_one(self):
                    pass
                def test_two(self):
                    pass
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=2 executed=0 skipped=0", out)
        self.assertIn("not_run=2", out)
        self.assertIn("errors=1", out)
        self.assertIn("required_executed=0", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def setUp(self):
                    raise RuntimeError("synthetic setup error")
                def test_one(self):
                    self.assertTrue(True)
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=0 skipped=0", out)
        self.assertIn("not_run=1", out)
        self.assertIn("errors=1", out)
        self.assertIn("required_executed=0", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            def setUpModule():
                raise RuntimeError("synthetic module error")
            class Needed(unittest.TestCase):
                def test_one(self):
                    pass
                def test_two(self):
                    pass
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=2 executed=0 skipped=0", out)
        self.assertIn("not_run=2", out)
        self.assertIn("errors=1", out)
        self.assertIn("required_executed=0", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("PASS:", combined)

    def test_subtest_failures_count_as_one_leaf(self):
        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def test_partial(self):
                    for n in range(3):
                        with self.subTest(n=n):
                            self.fail("synthetic subtest failure")
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=1 skipped=0", out)
        self.assertIn("failures=3", out)
        self.assertIn("required_executed=1", out)
        self.assertIn("optional_executed=0", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("executed=-", combined)
        self.assertNotIn("PASS:", combined)

    def test_leaf_skip_after_subtest_stays_one_skip(self):
        source = PASSING_TEST + textwrap.dedent(
            """\
            class Optional(unittest.TestCase):
                neocloud_optional = True
                def test_partial(self):
                    with self.subTest(n=0):
                        self.assertTrue(True)
                    self.skipTest("synthetic optional skip after subtest")
            """
        )
        code, out, err = self.gate_on(source)
        combined = out + err
        self.assertEqual(code, 0, combined)
        self.assertIn("discovered=2 executed=1 skipped=1", out)
        self.assertIn("required_skipped=0 optional_skipped=1", out)
        self.assertIn("required_executed=1", out)
        self.assertIn("SKIP optional:", out)
        self.assertIn("NOTE: optional tests were skipped; not all discovered tests executed.", out)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("executed=-", combined)

        code, out, err = self.gate_on(PASSING_TEST + textwrap.dedent(
            """\
            class Needed(unittest.TestCase):
                def test_partial(self):
                    with self.subTest(n=0):
                        self.assertTrue(True)
                    self.skipTest("synthetic required skip after subtest")
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=2 executed=1 skipped=1", out)
        self.assertIn("required_skipped=1", out)
        self.assertIn("required test skipped", combined)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def test_partial(self):
                    with self.subTest(n=0):
                        self.fail("synthetic subtest failure")
                    self.skipTest("synthetic skip after subtest failure")
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=0 skipped=1", out)
        self.assertIn("failures=1", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("PASS:", combined)

    def test_setup_failure_stays_not_run_when_later_events_fire(self):
        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def setUp(self):
                    def boom():
                        raise RuntimeError("synthetic cleanup error")
                    self.addCleanup(boom)
                    raise RuntimeError("synthetic setup error")
                def test_one(self):
                    self.assertTrue(True)
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=0 skipped=0", out)
        self.assertIn("not_run=1", out)
        self.assertIn("errors=2", out)
        self.assertIn("required_executed=0", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def setUp(self):
                    with self.subTest(n=0):
                        self.assertTrue(True)
                    raise RuntimeError("synthetic setup error")
                def test_one(self):
                    self.assertTrue(True)
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=0 skipped=0", out)
        self.assertIn("not_run=1", out)
        self.assertIn("errors=1", out)
        self.assertIn("required_executed=0", out)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def setUp(self):
                    with self.subTest(n=0):
                        self.fail("synthetic setup subtest failure")
                def test_one(self):
                    self.assertTrue(True)
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=0 skipped=0", out)
        self.assertIn("not_run=1", out)
        self.assertIn("failures=1", out)
        self.assertIn("required_executed=0", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("unittest result is inconsistent", combined)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def setUp(self):
                    self.assertTrue(False)
                def test_one(self):
                    self.assertTrue(True)
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=0 skipped=0", out)
        self.assertIn("not_run=1", out)
        self.assertIn("failures=1", out)
        self.assertIn("required_executed=0", out)
        self.assertNotIn("PASS:", combined)

        code, out, err = self.gate_on(textwrap.dedent(
            """\
            import unittest
            class Needed(unittest.TestCase):
                def test_one(self):
                    def boom():
                        raise RuntimeError("synthetic cleanup error")
                    self.addCleanup(boom)
                    self.assertTrue(True)
            """
        ))
        combined = out + err
        self.assertNotEqual(code, 0)
        self.assertIn("discovered=1 executed=1 skipped=0", out)
        self.assertIn("not_run=0", out)
        self.assertIn("errors=1", out)
        self.assertIn("required_executed=1", out)
        self.assertIn("unittest failures or errors", combined)
        self.assertNotIn("PASS:", combined)

    def gate_files(self, files: dict[str, str], codes: dict[str, int] | None = None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_validators(root, codes)
            tests = root / "tests"
            tests.mkdir()
            for name, source in files.items():
                (tests / name).write_text(textwrap.dedent(source), encoding="utf-8")
            return self.capture(lambda: self.gate.run_gate(root))


if __name__ == "__main__":
    unittest.main()
