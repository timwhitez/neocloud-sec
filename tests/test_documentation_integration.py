"""Structural checks for canonical documentation, not a prose or security audit."""
from __future__ import annotations

import json
import posixpath
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
RETIRED = {
    "docs/en/WEEKLY_SECURITY_REVIEW.md",
    "docs/zh-CN/WEEKLY_SECURITY_REVIEW.md",
    "reviews/2026-09-08-weekly-security-review.md",
}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SOURCE = re.compile(r"^- \[(S\d+)\s+[^\]]+\]\((https://[^)]+)\)$", re.M)


def relative_targets(text: str, document: str) -> set[str]:
    """Resolve inline local links without fetching or requiring target files."""
    targets = set()
    for target in LINK.findall(text):
        parsed = urlsplit(target.strip().strip("<>"))
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = unquote(parsed.path)
        targets.add(posixpath.normpath(posixpath.join(posixpath.dirname(document), path)))
    return targets


class DocumentationIntegrationTests(unittest.TestCase):
    def text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_canonical_documents_present(self):
        for path in (
            "README.md", "README.zh-CN.md", "CONTRIBUTING.md",
            ".github/PULL_REQUEST_TEMPLATE.md", "docs/EVIDENCE_VALIDATION.md",
            "docs/en/VALIDATION_RUNBOOKS.md", "docs/zh-CN/VALIDATION_RUNBOOKS.md",
            "REFERENCES.md", "CHANGELOG.md", "templates/README.md",
        ):
            with self.subTest(path=path):
                self.assertTrue(self.text(path).strip())

    def test_retired_documents_absent(self):
        for path in RETIRED:
            with self.subTest(path=path):
                self.assertFalse((ROOT / path).exists())

    def test_no_relative_links_to_retired_documents(self):
        documents = list(ROOT.rglob("*.md"))
        self.assertTrue(documents)
        for document in documents:
            if ".git" in document.relative_to(ROOT).parts:
                continue
            relative = document.relative_to(ROOT).as_posix()
            with self.subTest(path=relative):
                self.assertFalse(relative_targets(document.read_text(encoding="utf-8"), relative) & RETIRED)

    def test_runbook_anchors_unique_and_bilingual(self):
        expected = [f"rb-{number:02d}" for number in range(1, 11)]
        for language in ("en", "zh-CN"):
            text = self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md")
            with self.subTest(language=language):
                self.assertEqual(re.findall(r'<a id="(rb-\d{2})"></a>', text), expected)
                self.assertEqual(re.findall(r"^## (RB-\d{2})\b", text, re.M), [x.upper() for x in expected])

    def test_runbook_sources_have_bilingual_identity(self):
        sources = []
        for language in ("en", "zh-CN"):
            text = self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md")
            pairs = SOURCE.findall(text)
            self.assertTrue(pairs)
            self.assertEqual(len(pairs), len(dict(pairs)), "duplicate source ID")
            used = set(re.findall(r"\bS\d+\b", text))
            self.assertEqual(used, set(dict(pairs)), "unresolved source ID")
            sources.append(dict(pairs))
        self.assertEqual(sources[0], sources[1])

    def test_runbook_control_references_exist(self):
        catalog = json.loads(self.text("controls/neocloud-security-baseline.v1.json"))
        control_ids = {control["id"] for control in catalog["controls"]}
        references = []
        for language in ("en", "zh-CN"):
            ids = set(re.findall(r"\bNCS-[A-Z]+-\d{2}\b", self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md")))
            self.assertTrue(ids)
            self.assertFalse(ids - control_ids)
            references.append(ids)
        self.assertEqual(references[0], references[1])

    def test_ordinary_navigation_reaches_maintenance_and_evidence(self):
        for path in ("README.md", "README.zh-CN.md"):
            targets = relative_targets(self.text(path), path)
            self.assertIn("CONTRIBUTING.md", targets)
            self.assertIn("docs/EVIDENCE_VALIDATION.md", targets)
        self.assertIn('<a id="recurring-research"></a>', self.text("CONTRIBUTING.md"))
        self.assertIn("scripts/check_local.py", self.text(".github/PULL_REQUEST_TEMPLATE.md"))

    def test_optional_record_examples_are_discoverable(self):
        targets = relative_targets(self.text("templates/README.md"), "templates/README.md")
        for path in ("templates/evidence-record.example.csv", "templates/advisory-triage.example.json", "docs/EVIDENCE_VALIDATION.md"):
            self.assertIn(path, targets)
        example = json.loads(self.text("templates/advisory-triage.example.json"))
        guide = self.text("docs/EVIDENCE_VALIDATION.md")
        for field in set(example) | set(example["records"][0]):
            self.assertIn(f"`{field}`", guide)

    def test_retired_relative_path_normalization(self):
        for text in (
            "[old](../docs/en/WEEKLY_SECURITY_REVIEW.md#test)",
            "[old](../docs/en/./WEEKLY_SECURITY_REVIEW.md)",
            "[old](../docs/en/%57EEKLY_SECURITY_REVIEW.md)",
        ):
            self.assertTrue(relative_targets(text, "templates/README.md") & RETIRED)

    def test_historical_external_links_are_not_active_local_paths(self):
        text = "[history](https://github.com/timwhitez/neocloud-sec/blob/old/docs/en/WEEKLY_SECURITY_REVIEW.md) [anchor](#here)"
        self.assertEqual(relative_targets(text, "README.md"), set())


if __name__ == "__main__":
    unittest.main()
