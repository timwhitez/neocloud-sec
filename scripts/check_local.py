#!/usr/bin/env python3
"""Run repository checks locally; never invoke GitHub Actions or install packages.

This is the only ordinary local entry. Each validator and the unittest step
runs in a subprocess limited to 120 seconds. The unittest step is an internal
``--unittest-report`` mode of this same file. It writes structured counts
from ``unittest.TestResult``. The parent decides from those counts. A process
exit code of 0 is not evidence that required tests ran, and the summary text
is not parsed.

The counted unit is the discovered leaf test. ``testsRun`` and ``len(skipped)``
are not the same unit: a shared fixture is one holder event, and each subTest
skip is its own event. Leaf totals are therefore not derived by subtracting
those events. A ``setUpClass`` or ``setUpModule`` skip counts every affected
leaf under that leaf's own required or optional marker. Subtest skips stay
beside the leaf count. An error in ``setUp``, ``setUpClass``, or ``setUpModule``
is not test-body execution.

Tests discovered under ``tests/`` are required unless that test function or
its ``TestCase`` class sets ``neocloud_optional = True``. The gate fails when
nothing is discovered, when no required test body executes, when a required
leaf or required subtest is skipped, or when a skip event cannot be attributed.
An optional skip is reported and is not execution. Counts stay non-negative.
The suite size is the number discovered on that run.

The result does not change NOT_TESTED, VERIFIED, or T0 deployment meaning.
"""
from __future__ import annotations

import json
import os
import re
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


_HOLDER_EVENT = re.compile(
    r"^(setUpClass|setUpModule|tearDownClass|tearDownModule) \((.*)\)$"
)


def _event_kind(test) -> str:
    """Separate leaf tests from unittest's fixture holders and subtests."""
    name = type(test).__name__
    if name == "_SubTest":
        return "subtest"
    if name == "_ErrorHolder":
        return "holder"
    return "leaf"


def _frame_names(err) -> set[str]:
    names = set()
    traceback = err[2] if isinstance(err, tuple) and len(err) >= 3 else None
    while traceback is not None:
        names.add(traceback.tb_frame.f_code.co_name)
        traceback = traceback.tb_next
    return names


def _error_is_before_body(err) -> bool:
    """True when setUp failed and the test method was not entered."""
    names = _frame_names(err)
    if "_callTestMethod" in names or "_callTearDown" in names or "_callCleanup" in names:
        return False
    return "_callSetUp" in names


class RecordingResult(unittest.TextTestResult):
    """Record leaf, fixture-holder, and subtest events without mixing them."""

    def __init__(self, stream, descriptions, verbosity, **kwargs):
        if kwargs:
            super().__init__(stream, descriptions, verbosity, **kwargs)
        else:
            super().__init__(stream, descriptions, verbosity)
        self.started: set[str] = set()
        self.leaf_skips: dict[str, str] = {}
        self.leaf_success: set[str] = set()
        self.leaf_failure: set[str] = set()
        self.leaf_body_error: set[str] = set()
        self.leaf_pre_body_error: set[str] = set()
        self.leaf_other_executed: set[str] = set()
        self.subtest_parents: set[str] = set()
        self.subtest_skips: list[tuple[str, str, str]] = []
        self.holder_skips: list[tuple[str, str]] = []
        self.holder_errors: list[str] = []

    def startTest(self, test):
        super().startTest(test)
        if _event_kind(test) == "leaf":
            self.started.add(test.id())

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        kind = _event_kind(test)
        if kind == "subtest":
            parent = test.test_case.id()
            self.subtest_parents.add(parent)
            self.subtest_skips.append((parent, test.id(), str(reason)))
        elif kind == "holder":
            self.holder_skips.append((test.id(), str(reason)))
        else:
            self.leaf_skips[test.id()] = str(reason)

    def addSuccess(self, test):
        super().addSuccess(test)
        if _event_kind(test) == "leaf":
            self.leaf_success.add(test.id())

    def addFailure(self, test, err):
        super().addFailure(test, err)
        if _event_kind(test) == "leaf":
            self.leaf_failure.add(test.id())

    def addError(self, test, err):
        super().addError(test, err)
        kind = _event_kind(test)
        if kind == "holder":
            self.holder_errors.append(test.id())
        elif kind == "leaf":
            if _error_is_before_body(err):
                self.leaf_pre_body_error.add(test.id())
            else:
                self.leaf_body_error.add(test.id())

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        if _event_kind(test) == "leaf":
            self.leaf_other_executed.add(test.id())

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        if _event_kind(test) == "leaf":
            self.leaf_other_executed.add(test.id())

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        parent = test.test_case.id() if _event_kind(test) == "subtest" else test.id()
        self.subtest_parents.add(parent)


def _count(report: dict, key: str) -> int:
    value = report[key]
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(key)
    return value


def _count_if_present(report: dict, key: str) -> int:
    if key not in report or report[key] is None:
        return 0
    return _count(report, key)


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
        not_run = _count_if_present(report, "not_run")
        failures = _count(report, "failures")
        errors = _count(report, "errors")
        unexpected = _count(report, "unexpected_successes")
        subtests_skipped = _count_if_present(report, "subtests_skipped")
        subtests_required_skipped = _count_if_present(report, "subtests_required_skipped")
        subtests_optional_skipped = _count_if_present(report, "subtests_optional_skipped")
        for key, expected in (
            ("skipped_required", required_skipped),
            ("skipped_optional", optional_skipped),
            ("skipped_subtests_required", subtests_required_skipped),
            ("skipped_subtests_optional", subtests_optional_skipped),
        ):
            if key not in report or report[key] is None:
                continue
            items = report[key]
            if not isinstance(items, list) or len(items) != expected:
                return False, "unittest result is inconsistent"
        if executed + skipped + not_run != discovered:
            return False, "unittest result is inconsistent"
        if required_executed + optional_executed != executed:
            return False, "unittest result is inconsistent"
        if required_skipped + optional_skipped != skipped:
            return False, "unittest result is inconsistent"
        subtest_keys = (
            "subtests_skipped",
            "subtests_required_skipped",
            "subtests_optional_skipped",
        )
        if any(key in report and report[key] is not None for key in subtest_keys):
            if subtests_required_skipped + subtests_optional_skipped != subtests_skipped:
                return False, "unittest result is inconsistent"
    except (KeyError, TypeError, ValueError):
        return False, "unittest result is incomplete"
    if failures or errors or unexpected:
        return False, "unittest failures or errors"
    if discovered == 0:
        return False, "no tests discovered"
    if not_run:
        return False, "unittest did not start every discovered test"
    if required_executed < 1:
        return False, "no required test body executed"
    if required_skipped:
        return False, "required test skipped"
    if subtests_required_skipped:
        return False, "required subtest skipped"
    notes = []
    if optional_skipped:
        notes.append("optional tests skipped")
    if subtests_optional_skipped:
        notes.append("optional subtests skipped")
    if notes:
        return True, "required tests executed; " + "; ".join(notes)
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
        "not_run": 0,
        "subtests_skipped": 0,
        "subtests_required_skipped": 0,
        "subtests_optional_skipped": 0,
        "incomplete": incomplete or bool(error),
        "python": sys.version,
        "error": error,
        "skipped_required": [],
        "skipped_optional": [],
        "skipped_subtests_required": [],
        "skipped_subtests_optional": [],
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


def _iter_leaves(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _iter_leaves(item)
        else:
            yield item


def _leaf_fact(test) -> dict:
    return {
        "id": test.id(),
        "optional": is_optional_test(test),
        "class_name": f"{test.__class__.__module__}.{test.__class__.__qualname__}",
        "module": test.__class__.__module__,
    }


def _account_leaves(leaves: list[dict], result: RecordingResult) -> dict:
    """Assign each discovered leaf once. Do not subtract fixture or subtest events."""
    by_id = {leaf["id"]: leaf for leaf in leaves}
    inconsistent = len(by_id) != len(leaves) or len(result.started) != result.testsRun
    unattributed_skip = False
    fixture_skip: dict[str, str] = {}
    blocked_by_error: set[str] = set()

    def available(leaf: dict) -> bool:
        leaf_id = leaf["id"]
        return leaf_id not in result.started and leaf_id not in result.leaf_skips and leaf_id not in fixture_skip

    for description, reason in result.holder_skips:
        match = _HOLDER_EVENT.fullmatch(description)
        kind = match.group(1) if match else ""
        parent = match.group(2) if match else ""
        if kind == "setUpClass":
            targets = [leaf for leaf in leaves if leaf["class_name"] == parent and available(leaf)]
        elif kind == "setUpModule":
            targets = [leaf for leaf in leaves if leaf["module"] == parent and available(leaf)]
        else:
            targets = []
        if not targets:
            unattributed_skip = True
            continue
        for leaf in targets:
            fixture_skip[leaf["id"]] = f"{kind}: {reason}"

    for description in result.holder_errors:
        match = _HOLDER_EVENT.fullmatch(description)
        if match is None:
            continue
        kind, parent = match.group(1), match.group(2)
        if kind == "setUpClass":
            matched = [leaf for leaf in leaves if leaf["class_name"] == parent and available(leaf)]
        elif kind == "setUpModule":
            matched = [leaf for leaf in leaves if leaf["module"] == parent and available(leaf)]
        else:
            matched = []
        for leaf in matched:
            blocked_by_error.add(leaf["id"])

    for leaf_id in result.leaf_skips:
        if leaf_id not in by_id:
            unattributed_skip = True
    for parent, _sub_id, _reason in result.subtest_skips:
        if parent not in by_id:
            unattributed_skip = True

    executed_mark = (
        result.leaf_success
        | result.leaf_failure
        | result.leaf_body_error
        | result.leaf_other_executed
        | result.subtest_parents
    )
    skipped_required = []
    skipped_optional = []
    required_executed = 0
    optional_executed = 0
    not_run = 0
    unexplained = 0
    for leaf in leaves:
        leaf_id = leaf["id"]
        optional = bool(leaf["optional"])
        ran = leaf_id in executed_mark
        reason = result.leaf_skips.get(leaf_id)
        if reason is None:
            reason = fixture_skip.get(leaf_id)
        if reason is not None and ran:
            inconsistent = True
            continue
        if reason is not None:
            entry = {"test": leaf_id, "reason": reason}
            if optional:
                skipped_optional.append(entry)
            else:
                skipped_required.append(entry)
            continue
        if leaf_id in result.leaf_pre_body_error and not ran:
            not_run += 1
            continue
        if ran or (leaf_id in result.started and leaf_id not in result.leaf_pre_body_error):
            if optional:
                optional_executed += 1
            else:
                required_executed += 1
            continue
        not_run += 1
        if leaf_id not in blocked_by_error:
            unexplained += 1

    subtests_required = []
    subtests_optional = []
    for parent, sub_id, reason in result.subtest_skips:
        entry = {"test": sub_id, "reason": reason, "parent": parent}
        parent_leaf = by_id.get(parent)
        if parent_leaf is not None and parent_leaf["optional"]:
            subtests_optional.append(entry)
        else:
            subtests_required.append(entry)

    error = ""
    if inconsistent:
        error = "unittest result is inconsistent"
    elif unattributed_skip:
        error = "unattributed unittest skip"
    failures = result.failures
    errors = result.errors
    return {
        "discovered": len(leaves),
        "executed": required_executed + optional_executed,
        "required_executed": required_executed,
        "optional_executed": optional_executed,
        "skipped": len(skipped_required) + len(skipped_optional),
        "required_skipped": len(skipped_required),
        "optional_skipped": len(skipped_optional),
        "failures": len(failures),
        "errors": len(errors),
        "unexpected_successes": len(getattr(result, "unexpectedSuccesses", [])),
        "expected_failures": len(getattr(result, "expectedFailures", [])),
        "not_run": not_run,
        "subtests_skipped": len(subtests_required) + len(subtests_optional),
        "subtests_required_skipped": len(subtests_required),
        "subtests_optional_skipped": len(subtests_optional),
        "incomplete": unexplained > 0 and not failures and not errors,
        "python": sys.version,
        "error": error,
        "skipped_required": skipped_required,
        "skipped_optional": skipped_optional,
        "skipped_subtests_required": subtests_required,
        "skipped_subtests_optional": subtests_optional,
        "failure_tests": _outcome_names(failures),
        "error_tests": _outcome_names(errors),
    }


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
    try:
        leaves = [_leaf_fact(test) for test in _iter_leaves(suite)]
    except Exception as exc:
        return _empty_report(error=f"unittest discovery failed: {exc}", errors=1, incomplete=True)
    discovered = suite.countTestCases()
    if len(leaves) != discovered:
        return _empty_report(
            error="unittest result is inconsistent",
            errors=1,
            incomplete=True,
            discovered=discovered,
        )
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
    if not isinstance(result, RecordingResult):
        return _empty_report(
            error="unittest result is incomplete",
            errors=1,
            incomplete=True,
            discovered=discovered,
        )
    return _account_leaves(leaves, result)


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
        f"not_run={value('not_run')} subtests_skipped={value('subtests_skipped')} "
        f"subtests_required_skipped={value('subtests_required_skipped')} "
        f"subtests_optional_skipped={value('subtests_optional_skipped')} "
        f"required_executed={value('required_executed')} "
        f"optional_executed={value('optional_executed')} "
        f"reason={reason}"
    )


def _print_skip_details(report: dict) -> None:
    for label, key in (
        ("required", "skipped_required"),
        ("optional", "skipped_optional"),
        ("required subtest", "skipped_subtests_required"),
        ("optional subtest", "skipped_subtests_optional"),
    ):
        items = report.get(key) or []
        if not isinstance(items, list):
            continue
        stream = sys.stderr if label.startswith("required") else sys.stdout
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
        if _count_or_zero(report, "subtests_optional_skipped"):
            print("NOTE: optional subtests were skipped; partial coverage is not full execution.")
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
