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

    def test_source_keeps_timeout_and_does_not_hardcode_suite_size(self):
        source = (ROOT / "scripts" / "check_local.py").read_text(encoding="utf-8")
        self.assertIn("STEP_TIMEOUT_SECONDS = 120", source)
        self.assertIn('OPTIONAL_ATTRIBUTE = "neocloud_optional"', source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("170", source)

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


if __name__ == "__main__":
    unittest.main()
