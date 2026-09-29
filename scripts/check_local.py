#!/usr/bin/env python3
"""Run repository checks locally; never invoke GitHub Actions or install packages.

This is the only ordinary local entry. Each validator and the unittest step
runs in a subprocess limited to 120 seconds. The unittest step is an internal
``--unittest-report`` mode of this same file. It writes structured counts
from ``unittest.TestResult`` (discovered, executed, skipped, failures, errors).
The parent decides from those counts. A process exit code of 0 is not evidence
that required tests ran, and the summary text is not parsed.

Tests discovered under ``tests/`` are required offline regressions unless that
test function or its ``TestCase`` class sets ``neocloud_optional = True``.
The gate fails when nothing is discovered, when no required test body executes,
or when a required test is skipped. An optional skip is reported and is not
execution. The suite size is the number discovered on that run.

The result does not change NOT_TESTED, VERIFIED, or T0 deployment meaning.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

STEP_TIMEOUT_SECONDS = 120
OPTIONAL_ATTRIBUTE = "neocloud_optional"
VALIDATORS = (
    "validate_repository.py",
    "validate_accuracy_invariants.py",
    "validate_semianalysis_profile.py",
)
SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[1]


def run_command(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess:
    """Run one gate step. The timeout is part of the local-entry contract."""
    return subprocess.run(command, cwd=cwd, check=False, timeout=STEP_TIMEOUT_SECONDS)


def is_optional_test(test: unittest.TestCase) -> bool:
    """True only for an explicit optional marker, not for every skip."""
    if getattr(test.__class__, OPTIONAL_ATTRIBUTE, None) is True:
        return True
    method_name = getattr(test, "_testMethodName", None)
    if not method_name:
        return False
    function = getattr(test.__class__, method_name, None)
    if getattr(function, OPTIONAL_ATTRIBUTE, None) is True:
        return True
    bound = getattr(test, method_name, None)
    underlying = getattr(bound, "__func__", bound)
    return getattr(underlying, OPTIONAL_ATTRIBUTE, None) is True


class RecordingResult(unittest.TextTestResult):
    """Count required and optional bodies that actually executed."""

    def __init__(self, stream, descriptions, verbosity, **kwargs):
        if kwargs:
            super().__init__(stream, descriptions, verbosity, **kwargs)
        else:
            super().__init__(stream, descriptions, verbosity)
        self.required_executed = 0
        self.optional_executed = 0

    def _count_executed(self, test) -> None:
        if is_optional_test(test):
            self.optional_executed += 1
        else:
            self.required_executed += 1

    def addSuccess(self, test):
        super().addSuccess(test)
        self._count_executed(test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._count_executed(test)

    def addError(self, test, err):
        super().addError(test, err)
        self._count_executed(test)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self._count_executed(test)

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self._count_executed(test)


def _count(report: dict, key: str) -> int:
    value = report[key]
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(key)
    return value


def assess(report: dict) -> tuple[bool, str]:
    """Decide the unittest step from structured counts, not from an exit code."""
    try:
        if report.get("error"):
            return False, str(report["error"])
        if report.get("incomplete"):
            return False, "unittest did not start every discovered test"
        discovered = _count(report, "discovered")
        executed = _count(report, "executed")
        required_executed = _count(report, "required_executed")
        optional_executed = _count(report, "optional_executed")
        skipped = _count(report, "skipped")
        required_skipped = _count(report, "required_skipped")
        optional_skipped = _count(report, "optional_skipped")
        failures = _count(report, "failures")
        errors = _count(report, "errors")
        unexpected = _count(report, "unexpected_successes")
        for key, expected in (
            ("skipped_required", required_skipped),
            ("skipped_optional", optional_skipped),
        ):
            if key not in report or report[key] is None:
                continue
            items = report[key]
            if not isinstance(items, list) or len(items) != expected:
                return False, "unittest result is inconsistent"
        if executed + skipped != discovered:
            return False, "unittest result is inconsistent"
        if required_executed + optional_executed != executed:
            return False, "unittest result is inconsistent"
        if required_skipped + optional_skipped != skipped:
            return False, "unittest result is inconsistent"
    except (KeyError, TypeError, ValueError):
        return False, "unittest result is incomplete"
    if failures or errors or unexpected:
        return False, "unittest failures or errors"
    if discovered == 0:
        return False, "no tests discovered"
    if required_executed < 1:
        return False, "no required test body executed"
    if required_skipped:
        return False, "required test skipped"
    if optional_skipped:
        return True, "required tests executed; optional tests skipped"
    return True, "required tests executed"


def _empty_report(*, error: str, errors: int = 0, incomplete: bool = False, discovered: int = 0) -> dict:
    return {
        "discovered": discovered,
        "executed": 0,
        "required_executed": 0,
        "optional_executed": 0,
        "skipped": 0,
        "required_skipped": 0,
        "optional_skipped": 0,
        "failures": 0,
        "errors": errors,
        "unexpected_successes": 0,
        "expected_failures": 0,
        "incomplete": incomplete or bool(error),
        "python": sys.version,
        "error": error,
        "skipped_required": [],
        "skipped_optional": [],
        "failure_tests": [],
        "error_tests": [],
    }


def _prepare_discovery_path(root: Path) -> None:
    """Match ``python -m unittest discover`` launched with the checkout as cwd."""
    script_dir = str(SCRIPT.parent)
    sys.path[:] = [entry for entry in sys.path if os.path.abspath(entry or os.curdir) != script_dir]
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)


def _outcome_names(entries) -> list[str]:
    names = []
    for item in entries:
        test = item[0] if isinstance(item, tuple) else item
        names.append(test.id() if hasattr(test, "id") else str(test))
    return names


def collect_unittest_report(root: Path) -> dict:
    tests_dir = root / "tests"
    if not tests_dir.is_dir():
        return _empty_report(error="tests directory is missing", errors=1, incomplete=True)
    _prepare_discovery_path(root)
    loader = unittest.TestLoader()
    try:
        suite = loader.discover(str(tests_dir), pattern="test*.py", top_level_dir=str(tests_dir))
    except Exception as exc:
        return _empty_report(error=f"unittest discovery failed: {exc}", errors=1, incomplete=True)
    discovered = suite.countTestCases()
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2, resultclass=RecordingResult)
    try:
        result = runner.run(suite)
    except Exception as exc:
        return _empty_report(
            error=f"unittest execution failed: {exc}",
            errors=1,
            incomplete=True,
            discovered=discovered,
        )
    skipped_required = []
    skipped_optional = []
    for test, reason in result.skipped:
        entry = {"test": test.id(), "reason": str(reason)}
        if is_optional_test(test):
            skipped_optional.append(entry)
        else:
            skipped_required.append(entry)
    started = result.testsRun
    skipped = len(result.skipped)
    executed = started - skipped
    return {
        "discovered": discovered,
        "executed": executed,
        "required_executed": result.required_executed,
        "optional_executed": result.optional_executed,
        "skipped": skipped,
        "required_skipped": len(skipped_required),
        "optional_skipped": len(skipped_optional),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "unexpected_successes": len(getattr(result, "unexpectedSuccesses", [])),
        "expected_failures": len(getattr(result, "expectedFailures", [])),
        "incomplete": started != discovered or bool(getattr(result, "shouldStop", False)) or executed < 0,
        "python": sys.version,
        "error": "",
        "skipped_required": skipped_required,
        "skipped_optional": skipped_optional,
        "failure_tests": _outcome_names(result.failures),
        "error_tests": _outcome_names(result.errors),
    }


def _write_json(path: Path, report: dict) -> None:
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=True, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def _load_report(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def _format_stats(report: dict, reason: str) -> str:
    python = str(report.get("python", "unknown")).split()[0]
    def value(key: str) -> object:
        return report.get(key, "?")
    return (
        f"python={python} discovered={value('discovered')} executed={value('executed')} "
        f"skipped={value('skipped')} required_skipped={value('required_skipped')} "
        f"optional_skipped={value('optional_skipped')} failures={value('failures')} "
        f"errors={value('errors')} unexpected_successes={value('unexpected_successes')} "
        f"reason={reason}"
    )


def _print_skip_details(report: dict) -> None:
    for label, key in (("required", "skipped_required"), ("optional", "skipped_optional")):
        items = report.get(key) or []
        if not isinstance(items, list):
            continue
        stream = sys.stderr if label == "required" else sys.stdout
        for item in items:
            if not isinstance(item, dict):
                continue
            print(f"SKIP {label}: {item.get('test', '?')}: {item.get('reason', '')}", file=stream)


def _argument(args: list[str], name: str) -> str | None:
    if name not in args:
        return None
    index = args.index(name)
    if index + 1 >= len(args):
        return None
    return args[index + 1]


def report_main(args: list[str]) -> int:
    result_arg = _argument(args, "--result")
    if result_arg is None:
        print("unittest report requires --result", file=sys.stderr)
        return 2
    root_arg = _argument(args, "--root")
    root = ROOT if root_arg is None else Path(root_arg)
    report = collect_unittest_report(root)
    _write_json(Path(result_arg), report)
    accepted, _reason = assess(report)
    return 0 if accepted else 1


def _run_named_step(command: list[str], cwd: Path, name: str) -> bool:
    """Return True when the step fails, times out, or cannot start."""
    print("RUN: " + " ".join(command), flush=True)
    try:
        completed = run_command(command, cwd=cwd)
    except subprocess.TimeoutExpired:
        print(f"EXIT timeout: {name}")
        return True
    except OSError as exc:
        print(f"EXIT start-failed: {name}: {exc}")
        return True
    print(f"EXIT {completed.returncode}: {name}")
    return completed.returncode != 0


def _run_unittest_step(root: Path) -> bool:
    """Return True when required tests were not executed or the result is unusable."""
    print(f"RUN: {sys.executable} {SCRIPT} --unittest-report", flush=True)
    descriptor, name = tempfile.mkstemp(prefix="neocloud-unittest-", suffix=".json")
    os.close(descriptor)
    result_path = Path(name)
    command = [
        sys.executable,
        str(SCRIPT),
        "--unittest-report",
        "--root",
        str(root),
        "--result",
        str(result_path),
    ]
    try:
        try:
            completed = run_command(command, cwd=root)
        except subprocess.TimeoutExpired:
            print("EXIT timeout: unittest")
            return True
        except OSError as exc:
            print(f"EXIT start-failed: unittest: {exc}")
            return True
        report = _load_report(result_path)
        if report is None:
            print(f"EXIT {completed.returncode}: unittest")
            print("FAIL: unittest result is missing", file=sys.stderr)
            return True
        accepted, reason = assess(report)
        print(f"EXIT {completed.returncode}: unittest {_format_stats(report, reason)}")
        _print_skip_details(report)
        if not accepted:
            print(f"FAIL: unittest: {reason}", file=sys.stderr)
            return True
        if completed.returncode != 0:
            print(f"FAIL: unittest process exited {completed.returncode}", file=sys.stderr)
            return True
        if _count_or_zero(report, "optional_skipped"):
            print("NOTE: optional tests were skipped; not all discovered tests executed.")
        return False
    finally:
        result_path.unlink(missing_ok=True)
        Path(str(result_path) + ".tmp").unlink(missing_ok=True)


def _count_or_zero(report: dict, key: str) -> int:
    try:
        return _count(report, key)
    except (KeyError, TypeError, ValueError):
        return 0


def run_gate(root: Path | None = None) -> int:
    root = ROOT if root is None else Path(root)
    print(f"PYTHON: {sys.version.split()[0]}", flush=True)
    failed = False
    for name in VALIDATORS:
        command = [sys.executable, str(root / "scripts" / name)]
        failed = _run_named_step(command, root, name) or failed
    failed = _run_unittest_step(root) or failed
    if failed:
        print("FAIL: one or more local checks failed or did not run", file=sys.stderr)
        return 1
    print("PASS: local repository checks only; no live provider assessment performed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--unittest-report" in args:
        return report_main(args)
    return run_gate(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
