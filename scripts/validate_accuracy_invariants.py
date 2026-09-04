#!/usr/bin/env python3
"""Validate version and template semantics not covered by the core catalog validator."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(r"\b\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?\b")
ALLOWED_RESULTS = {"PASS", "FAIL", "INCONCLUSIVE", "NOT_TESTED"}
OWNER_VALUES = {"provider", "customer", "shared"}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def read_text(relative: str, validation: Validation) -> str:
    path = ROOT / relative
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        validation.errors.append(f"missing required file: {relative}")
        return ""


def validate_versions(validation: Validation) -> str:
    version = read_text("VERSION", validation).strip()
    validation.require(
        VERSION_RE.fullmatch(version) is not None,
        f"VERSION is not valid semantic-version syntax: {version!r}",
    )
    for relative in (
        "ACCURACY_REVIEW.md",
        "docs/en/SCOPE_AND_LIMITATIONS.md",
        "docs/zh-CN/SCOPE_AND_LIMITATIONS.md",
    ):
        text = read_text(relative, validation)
        observed = set(VERSION_RE.findall(text))
        validation.require(
            observed == {version},
            f"{relative} version set {sorted(observed)!r} differs from VERSION {version!r}",
        )
    return version


def validate_evidence_template(validation: Validation) -> None:
    path = ROOT / "templates/evidence-register.csv"
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = reader.fieldnames or []
    except FileNotFoundError:
        validation.errors.append("missing required file: templates/evidence-register.csv")
        return

    required = {
        "evidence_id",
        "control_id",
        "service",
        "observed_at",
        "valid_until",
        "verifier",
        "verification_result",
        "verified_at",
        "limitations",
    }
    validation.require(required.issubset(fieldnames), "evidence-register.csv is missing required columns")
    validation.require(bool(rows), "evidence-register.csv must contain an example row")
    for index, row in enumerate(rows, start=2):
        result = (row.get("verification_result") or "").strip()
        validation.require(
            result in ALLOWED_RESULTS,
            f"evidence-register.csv line {index} has invalid verification_result {result!r}",
        )
        if result == "PASS":
            validation.require(bool((row.get("verifier") or "").strip()), f"line {index}: PASS requires verifier")
            validation.require(bool((row.get("verified_at") or "").strip()), f"line {index}: PASS requires verified_at")


def validate_responsibility_template(validation: Validation) -> int:
    path = ROOT / "templates/shared-responsibility-matrix.csv"
    try:
        text = path.read_text(encoding="utf-8")
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = reader.fieldnames or []
    except FileNotFoundError:
        validation.errors.append("missing required file: templates/shared-responsibility-matrix.csv")
        return 0

    expected_fields = [
        "capability",
        "provider_responsibility",
        "customer_responsibility",
        "shared_activity",
        "default_owner",
        "evidence",
        "escalation_path",
    ]
    validation.require(fieldnames == expected_fields, "shared-responsibility-matrix.csv columns changed unexpectedly")
    capabilities = [(row.get("capability") or "").strip() for row in rows]
    validation.require(len(capabilities) == len(set(capabilities)), "shared-responsibility-matrix.csv has duplicate capabilities")

    by_capability = {capability: row for capability, row in zip(capabilities, rows, strict=True)}
    provider_roots = {
        "Physical facility",
        "Hardware firmware and BMC/OOB",
        "Provider control plane and API",
        "Managed Kubernetes provider control plane",
        "Managed Slurm provider control plane",
        "GPU and accelerator isolation",
        "Provider Ethernet storage network InfiniBand/RDMA and DPU fabric",
        "Agent platform guardrails",
    }
    customer_scopes = {
        "Customer-managed guest operating system",
        "Kubernetes tenant workloads and namespace configuration",
        "Slurm tenant jobs data and requested placement",
        "Customer agent use case tools data and approvals",
    }
    for capability in sorted(provider_roots):
        validation.require(capability in by_capability, f"missing provider-root row: {capability}")
        if capability in by_capability:
            validation.require(
                by_capability[capability].get("default_owner") == "provider",
                f"provider-exclusive capability is not provider-owned: {capability}",
            )
    for capability in sorted(customer_scopes):
        validation.require(capability in by_capability, f"missing customer-scope row: {capability}")
        if capability in by_capability:
            validation.require(
                by_capability[capability].get("default_owner") == "customer",
                f"customer-controlled capability is not customer-owned: {capability}",
            )

    for index, row in enumerate(rows, start=2):
        owner = (row.get("default_owner") or "").strip()
        validation.require(owner in OWNER_VALUES, f"shared-responsibility line {index} has invalid owner {owner!r}")
        for field in expected_fields:
            validation.require(bool((row.get(field) or "").strip()), f"shared-responsibility line {index} has empty {field}")

    for ambiguous in ("Kubernetes control plane", "Slurm scheduler", "Network and InfiniBand/RDMA"):
        validation.require(ambiguous not in by_capability, f"ambiguous unsplit responsibility row remains: {ambiguous}")
    validation.require("PKey" not in text, "use the standard P_Key spelling, not PKey")
    validation.require("P_Key" in text, "shared-responsibility template lacks P_Key coverage")
    return len(rows)


def validate_threat_model(validation: Validation) -> None:
    text = read_text("templates/threat-model.md", validation)
    validation.require("time-slicing without isolation" not in text, "ambiguous time-slicing wording remains")
    validation.require(
        "time-slicing used without a separately justified memory/fault-isolation boundary" in text,
        "threat model must state the missing independently justified memory/fault boundary",
    )
    validation.require("PKey" not in text, "threat model uses non-standard PKey spelling")
    validation.require("P_Key" in text, "threat model lacks P_Key coverage")
    validation.require(
        "MCS/PrivateData controls mistaken for complete network, storage, GPU, process, or data isolation" in text,
        "threat model must prevent Slurm scheduler/visibility controls being treated as complete isolation",
    )


def validate_template_readme(validation: Validation) -> None:
    text = read_text("templates/README.md", validation)
    for token in ("PROPOSED", "READY", "IMPLEMENTED", "CANDIDATE_DONE", "VERIFIED"):
        validation.require(token in text, f"templates/README.md omits control state {token}")
    for token in sorted(ALLOWED_RESULTS):
        validation.require(token in text, f"templates/README.md omits verification result {token}")
    validation.require("`NOT_REVIEWED` is not a valid result" in text, "template README does not reject NOT_REVIEWED")
    validation.require("NO_GO_NONCONFORMANT" in text, "template README omits T0 nonconformance semantics")
    validation.require("Provider-exclusive roots" in text, "template README omits provider-root ownership rule")


def main() -> int:
    validation = Validation()
    version = validate_versions(validation)
    validate_evidence_template(validation)
    responsibility_rows = validate_responsibility_template(validation)
    validate_threat_model(validation)
    validate_template_readme(validation)

    if validation.errors:
        for error in validation.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"NeoCloud accuracy-invariant validation failed with {len(validation.errors)} error(s).", file=sys.stderr)
        return 1

    print(
        "NeoCloud accuracy invariants passed: "
        f"version={version}, evidence_results={sorted(ALLOWED_RESULTS)}, "
        f"responsibility_rows={responsibility_rows}, provider roots and GPU/P_Key/Slurm semantics verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
