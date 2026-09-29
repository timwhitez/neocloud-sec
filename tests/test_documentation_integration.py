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
EXTENSION_ANCHORS = (
    "inference-resource-budgets",
    "disaggregated-kv-lifecycle",
    "layer-specific-cache-isolation",
    "gpu-memory-disturbance",
    "confidential-composition",
)
EXECUTION_CLAIM = re.compile(
    r"deployment (?:is |was )?(?:PASS|VERIFIED)|marked as VERIFIED|已完成部署验证"
)


def anchored_sections(text: str, anchors: tuple[str, ...]) -> dict[str, str]:
    """Return the text of each named anchor through the next anchor."""
    markers = list(re.finditer(r'<a id="([^"]+)"></a>', text))
    sections: dict[str, str] = {}
    for index, match in enumerate(markers):
        anchor = match.group(1)
        if anchor not in anchors:
            continue
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        sections[anchor] = text[match.end() : end]
    return sections


def heading_section(text: str, anchor: str) -> str:
    """Return one anchored block through the next Markdown heading."""
    marker = f'<a id="{anchor}"></a>'
    start = text.index(marker)
    rest = text[start:]
    match = re.search(r"\n## ", rest)
    if match is None:
        raise ValueError(f"no following heading after {anchor}")
    return rest[: match.start()]


def section_delivery_ok(section: str) -> bool:
    """A delivered section names unexecuted work and does not claim execution."""
    return "`NOT_TESTED`" in section and EXECUTION_CLAIM.search(section) is None


def boundary_statement_ok(section: str, anti_execution: str) -> bool:
    return section_delivery_ok(section) and anti_execution in section


ANTI_EXECUTION = {
    "en": "repository text is not PASS or `VERIFIED`",
    "zh-CN": "仓库正文不是 PASS，也不是 `VERIFIED`",
}
ARCHITECTURE_NOT_TESTED = {
    "en": "keep unexecuted checks `NOT_TESTED`",
    "zh-CN": "将未执行的检查保持为 `NOT_TESTED`",
}


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

    def test_core_catalog_shape_unchanged(self):
        catalog = json.loads(self.text("controls/neocloud-security-baseline.v1.json"))
        tiers: dict[str, int] = {}
        for control in catalog["controls"]:
            tiers[control["tier"]] = tiers.get(control["tier"], 0) + 1
        self.assertEqual(len(catalog["controls"]), 90)
        self.assertEqual(tiers, {"T0": 32, "T1": 31, "T2": 19, "T3": 7, "T4": 1})
        self.assertEqual(catalog["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())

    def test_inference_extension_markers_are_bilingual(self):
        for language in ("en", "zh-CN"):
            text = self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md")
            sections = anchored_sections(text, EXTENSION_ANCHORS)
            with self.subTest(language=language):
                self.assertEqual(set(sections), set(EXTENSION_ANCHORS))
                for anchor, section in sections.items():
                    self.assertTrue(section_delivery_ok(section), anchor)
            whitepaper = self.text(f"docs/{language}/WHITEPAPER.md")
            boundary = heading_section(whitepaper, "inference-accelerator-boundaries")
            with self.subTest(language=language, document="whitepaper"):
                self.assertEqual(whitepaper.count('<a id="inference-accelerator-boundaries"></a>'), 1)
                for anchor in EXTENSION_ANCHORS:
                    self.assertIn(f"#{anchor}", boundary)
                self.assertTrue(boundary_statement_ok(boundary, ANTI_EXECUTION[language]))
                self.assertIsNone(EXECUTION_CLAIM.search(boundary))
                self.assertIn(ARCHITECTURE_NOT_TESTED[language], whitepaper)
                self.assertIn("1.0.0-draft.1", whitepaper)
        self.assertIn("T3 is not mandatory for every service", self.text("docs/en/WHITEPAPER.md"))
        self.assertIn("T3 不是每项服务的强制等级", self.text("docs/zh-CN/WHITEPAPER.md"))

    def test_gputhor_visibility_limit_is_bilingual(self):
        expected = {
            "en": ("§6.1 and §7.1", "§9", "on-die ECC reduces error visibility", "reduced visibility is not immunity"),
            "zh-CN": ("§6.1 与 §7.1", "§9", "降低错误可见性", "可见性下降并不等于免疫"),
        }
        for language, phrases in expected.items():
            section = anchored_sections(
                self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md"),
                ("gpu-memory-disturbance",),
            )["gpu-memory-disturbance"]
            for phrase in phrases:
                with self.subTest(language=language, phrase=phrase):
                    self.assertIn(phrase, section)
            self.assertNotIn("can reduce error visibility", section)
        register = self.text("REFERENCES.md")
        self.assertIn("§9 states that HBM3/e and GDDR7 on-die ECC reduces error visibility", register)
        self.assertNotIn("§10 leaves HBM3", register)

    def test_extension_source_urls_match_references(self):
        maps = []
        for language in ("en", "zh-CN"):
            maps.append(dict(SOURCE.findall(self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md"))))
        self.assertEqual(maps[0], maps[1])
        references = self.text("REFERENCES.md")
        for number in range(21, 31):
            source_id = f"S{number}"
            url = maps[0][source_id]
            with self.subTest(source_id=source_id):
                self.assertIn(url, references)

    def test_negative_missing_not_tested_marker_is_visible(self):
        section = anchored_sections(
            self.text("docs/en/VALIDATION_RUNBOOKS.md"), EXTENSION_ANCHORS
        )["inference-resource-budgets"]
        self.assertTrue(section_delivery_ok(section))
        stripped = section.replace("`NOT_TESTED`", "NOT_TESTED")
        self.assertNotEqual(stripped, section)
        self.assertFalse(section_delivery_ok(stripped))
        boundary = heading_section(
            self.text("docs/zh-CN/WHITEPAPER.md"), "inference-accelerator-boundaries"
        )
        self.assertTrue(boundary_statement_ok(boundary, ANTI_EXECUTION["zh-CN"]))
        self.assertFalse(section_delivery_ok(boundary.replace("`NOT_TESTED`", "NOT_TESTED")))

    def test_negative_execution_claim_is_detected(self):
        boundary = heading_section(
            self.text("docs/en/WHITEPAPER.md"), "inference-accelerator-boundaries"
        )
        phrase = ANTI_EXECUTION["en"]
        self.assertTrue(boundary_statement_ok(boundary, phrase))
        self.assertFalse(boundary_statement_ok(boundary.replace(phrase, "repository notes are separate"), phrase))
        self.assertFalse(boundary_statement_ok(boundary + "\nThe lab recorded deployment PASS for the GPU.\n", phrase))
        self.assertFalse(boundary_statement_ok(boundary + "\ncontrols were marked as VERIFIED\n", phrase))
        runbook = anchored_sections(
            self.text("docs/zh-CN/VALIDATION_RUNBOOKS.md"), EXTENSION_ANCHORS
        )["confidential-composition"]
        self.assertTrue(section_delivery_ok(runbook))
        self.assertFalse(section_delivery_ok(runbook + "\n已完成部署验证。\n"))
        self.assertIsNone(EXECUTION_CLAIM.search(phrase))


if __name__ == "__main__":
    unittest.main()
