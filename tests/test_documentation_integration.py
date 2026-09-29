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
ANCHOR_TAG = re.compile(r'<a id="([^"]+)"></a>')
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


def anchor_counts(text: str, anchors: tuple[str, ...]) -> dict[str, int]:
    """Count explicit anchors before any section dict can overwrite a duplicate."""
    counts = {anchor: 0 for anchor in anchors}
    for anchor in ANCHOR_TAG.findall(text):
        if anchor in counts:
            counts[anchor] += 1
    return counts


def anchored_sections(text: str, anchors: tuple[str, ...]) -> dict[str, str]:
    """Return the text of each named anchor through the next anchor."""
    counts = anchor_counts(text, anchors)
    bad = {anchor: count for anchor, count in counts.items() if count != 1}
    if bad:
        raise ValueError(f"expected exactly one explicit anchor, got {bad}")
    markers = list(ANCHOR_TAG.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(markers):
        anchor = match.group(1)
        if anchor not in counts:
            continue
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        sections[anchor] = text[match.end() : end]
    return sections


def heading_section(text: str, anchor: str) -> str:
    """Return one anchored block through the next Markdown heading."""
    marker = f'<a id="{anchor}"></a>'
    count = text.count(marker)
    if count != 1:
        raise ValueError(f"{anchor} occurs {count} times")
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


def split_markdown_destination(raw: str) -> tuple[str, str] | None:
    """Split an inline destination into a still-encoded path and fragment.

    External and protocol-relative URLs are not local navigation. Path and
    fragment are decoded separately after ``urlsplit``.
    """
    target = raw.strip()
    if not target:
        return None
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    if target.startswith("//"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    return unquote(parsed.path), unquote(parsed.fragment)


def normalize_repo_path(document: str, path: str) -> str:
    if path.startswith("/"):
        relative = path.lstrip("/")
    elif path:
        relative = posixpath.join(posixpath.dirname(document), path)
    else:
        relative = document
    return posixpath.normpath(relative)


def local_link_targets(text: str, document: str) -> set[tuple[str, str]]:
    """Return normalized ``(path, fragment)`` pairs for inline local links."""
    found = set()
    for raw in LINK.findall(text):
        split = split_markdown_destination(raw)
        if split is None:
            continue
        path, fragment = split
        found.add((normalize_repo_path(document, path), fragment))
    return found


def expected_bindings(language: str) -> tuple[tuple[str, str, str], ...]:
    """Promised README, white paper and runbook links for one language."""
    if language == "en":
        readme, whitepaper, runbook = (
            "README.md",
            "docs/en/WHITEPAPER.md",
            "docs/en/VALIDATION_RUNBOOKS.md",
        )
    elif language == "zh-CN":
        readme, whitepaper, runbook = (
            "README.zh-CN.md",
            "docs/zh-CN/WHITEPAPER.md",
            "docs/zh-CN/VALIDATION_RUNBOOKS.md",
        )
    else:
        raise ValueError(language)
    bindings = []
    for anchor in EXTENSION_ANCHORS:
        bindings.append((readme, runbook, anchor))
        bindings.append((whitepaper, runbook, anchor))
        bindings.append((runbook, runbook, anchor))
    bindings.append((readme, whitepaper, "inference-accelerator-boundaries"))
    return tuple(bindings)


def binding_problems(
    documents: dict[str, str], bindings: tuple[tuple[str, str, str], ...]
) -> list[str]:
    """Report a missing link or an explicit anchor that is not unique."""
    problems = []
    for source, target, fragment in bindings:
        source_text = documents.get(source)
        if source_text is None:
            problems.append(f"missing source {source}")
            continue
        if (target, fragment) not in local_link_targets(source_text, source):
            problems.append(f"{source} has no link to {target}#{fragment}")
            continue
        target_text = documents.get(target)
        if target_text is None:
            problems.append(f"missing target {target}")
            continue
        count = anchor_counts(target_text, (fragment,))[fragment]
        if count != 1:
            problems.append(f"{target}#{fragment} explicit anchor count is {count}")
    return problems


def one_local_link(document: str, raw_target: str) -> tuple[str, str] | None:
    found = local_link_targets(f"[label]({raw_target})", document)
    if not found:
        return None
    if len(found) != 1:
        raise AssertionError(found)
    return next(iter(found))


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

    def _language_documents(self, language: str) -> dict[str, str]:
        paths = set()
        for source, target, _fragment in expected_bindings(language):
            paths.add(source)
            paths.add(target)
        return {path: self.text(path) for path in paths}

    def test_inference_extension_markers_are_bilingual(self):
        for language in ("en", "zh-CN"):
            text = self.text(f"docs/{language}/VALIDATION_RUNBOOKS.md")
            with self.subTest(language=language, check="anchors"):
                self.assertEqual(
                    anchor_counts(text, EXTENSION_ANCHORS),
                    {anchor: 1 for anchor in EXTENSION_ANCHORS},
                )
            sections = anchored_sections(text, EXTENSION_ANCHORS)
            with self.subTest(language=language):
                self.assertEqual(set(sections), set(EXTENSION_ANCHORS))
                for anchor, section in sections.items():
                    self.assertTrue(section_delivery_ok(section), anchor)
            documents = self._language_documents(language)
            with self.subTest(language=language, check="bindings"):
                self.assertEqual(binding_problems(documents, expected_bindings(language)), [])
            whitepaper = documents[f"docs/{language}/WHITEPAPER.md"]
            boundary = heading_section(whitepaper, "inference-accelerator-boundaries")
            runbook = f"docs/{language}/VALIDATION_RUNBOOKS.md"
            with self.subTest(language=language, document="whitepaper"):
                self.assertEqual(whitepaper.count('<a id="inference-accelerator-boundaries"></a>'), 1)
                boundary_links = local_link_targets(boundary, f"docs/{language}/WHITEPAPER.md")
                for anchor in EXTENSION_ANCHORS:
                    self.assertIn((runbook, anchor), boundary_links)
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

    def test_duplicate_prepended_anchor_is_not_shadowed(self):
        text = self.text("docs/en/VALIDATION_RUNBOOKS.md")
        mutant = (
            '<a id="inference-resource-budgets"></a>\n'
            "### Misleading first target\n"
            "deployment PASS\n" + text
        )
        self.assertEqual(anchor_counts(mutant, EXTENSION_ANCHORS)["inference-resource-budgets"], 2)
        self.assertIsNotNone(EXECUTION_CLAIM.search(mutant))
        with self.assertRaises(ValueError) as caught:
            anchored_sections(mutant, EXTENSION_ANCHORS)
        message = str(caught.exception)
        self.assertIn("inference-resource-budgets", message)
        self.assertIn("2", message)

    def test_duplicate_appended_anchor_is_rejected(self):
        text = self.text("docs/zh-CN/VALIDATION_RUNBOOKS.md")
        mutant = text + (
            '\n<a id="confidential-composition"></a>\n'
            "### Later copy\n"
            "Unexecuted checks remain `NOT_TESTED`.\n"
        )
        self.assertEqual(anchor_counts(mutant, ("confidential-composition",))["confidential-composition"], 2)
        with self.assertRaises(ValueError):
            anchored_sections(mutant, EXTENSION_ANCHORS)

    def test_duplicate_whitepaper_anchor_before_or_after_is_rejected(self):
        text = self.text("docs/en/WHITEPAPER.md")
        marker = '<a id="inference-accelerator-boundaries"></a>'
        mutants = (
            marker + "\n## Fake\ndeployment PASS\n" + text,
            text + "\n" + marker + "\n## Trailing\n",
        )
        for mutant in mutants:
            with self.subTest(prepend=mutant.startswith(marker)):
                with self.assertRaises(ValueError):
                    heading_section(mutant, "inference-accelerator-boundaries")

    def test_wrong_existing_file_is_not_a_topic_binding(self):
        documents = self._language_documents("en")
        old = "docs/en/VALIDATION_RUNBOOKS.md#inference-resource-budgets"
        new = "docs/en/WHITEPAPER.md#inference-resource-budgets"
        self.assertIn(old, documents["README.md"])
        self.assertTrue((ROOT / "docs/en/WHITEPAPER.md").is_file())
        documents["README.md"] = documents["README.md"].replace(old, new, 1)
        documents["docs/en/WHITEPAPER.md"] += "\ninference-resource-budgets\n"
        problems = binding_problems(documents, expected_bindings("en"))
        self.assertTrue(any(old in item for item in problems))

    def test_missing_fragment_on_the_correct_file_fails(self):
        documents = self._language_documents("en")
        runbook = "docs/en/VALIDATION_RUNBOOKS.md"
        anchor = '<a id="gpu-memory-disturbance"></a>'
        self.assertEqual(documents[runbook].count(anchor), 1)
        documents[runbook] = documents[runbook].replace(anchor, "", 1)
        problems = binding_problems(documents, expected_bindings("en"))
        self.assertTrue(any("gpu-memory-disturbance" in item and "count is 0" in item for item in problems))

    def test_same_file_missing_fragment_fails(self):
        documents = self._language_documents("en")
        runbook = "docs/en/VALIDATION_RUNBOOKS.md"
        self.assertEqual(documents[runbook].count("](#gpu-memory-disturbance)"), 1)
        documents[runbook] = documents[runbook].replace(
            "](#gpu-memory-disturbance)",
            "](#gpu-memory-disturbance-missing)",
            1,
        )
        self.assertNotIn('<a id="gpu-memory-disturbance-missing"></a>', documents[runbook])
        problems = binding_problems(documents, expected_bindings("en"))
        self.assertTrue(any(f"{runbook}#gpu-memory-disturbance" in item for item in problems))

    def test_cross_language_topic_link_fails(self):
        cases = (
            (
                "zh-CN",
                "README.zh-CN.md",
                "docs/zh-CN/VALIDATION_RUNBOOKS.md#",
                "docs/en/VALIDATION_RUNBOOKS.md#",
                "docs/zh-CN/WHITEPAPER.md#inference-accelerator-boundaries",
                "docs/en/WHITEPAPER.md#inference-accelerator-boundaries",
            ),
            (
                "en",
                "README.md",
                "docs/en/VALIDATION_RUNBOOKS.md#",
                "docs/zh-CN/VALIDATION_RUNBOOKS.md#",
                "docs/en/WHITEPAPER.md#inference-accelerator-boundaries",
                "docs/zh-CN/WHITEPAPER.md#inference-accelerator-boundaries",
            ),
        )
        for language, readme, old_prefix, new_prefix, old_whitepaper, new_whitepaper in cases:
            with self.subTest(language=language):
                documents = self._language_documents(language)
                documents[readme] = (
                    documents[readme]
                    .replace(old_prefix, new_prefix)
                    .replace(old_whitepaper, new_whitepaper)
                )
                problems = binding_problems(documents, expected_bindings(language))
                self.assertTrue(any(old_prefix + "inference-resource-budgets" in item for item in problems))
        documents = self._language_documents("zh-CN")
        documents["docs/zh-CN/WHITEPAPER.md"] = documents["docs/zh-CN/WHITEPAPER.md"].replace(
            "VALIDATION_RUNBOOKS.md#",
            "../en/VALIDATION_RUNBOOKS.md#",
        )
        problems = binding_problems(documents, expected_bindings("zh-CN"))
        self.assertTrue(any("docs/zh-CN/VALIDATION_RUNBOOKS.md#layer-specific-cache-isolation" in item for item in problems))

    def test_keyword_without_navigation_link_fails(self):
        documents = self._language_documents("en")
        pattern = re.compile(
            r"\[[^\]]*\]\(docs/en/VALIDATION_RUNBOOKS.md#layer-specific-cache-isolation\)"
        )
        self.assertIsNotNone(pattern.search(documents["README.md"]))
        documents["README.md"] = pattern.sub("#layer-specific-cache-isolation", documents["README.md"], count=1)
        self.assertIn("#layer-specific-cache-isolation", documents["README.md"])
        self.assertIsNone(pattern.search(documents["README.md"]))
        problems = binding_problems(documents, expected_bindings("en"))
        self.assertTrue(any("layer-specific-cache-isolation" in item for item in problems))

    def test_percent_encoded_and_relative_links_match_contract(self):
        encoded = "docs/%65n/%56ALIDATION_RUNBOOKS.md#inference%2Dresource-budgets"
        self.assertEqual(
            one_local_link("README.md", encoded),
            ("docs/en/VALIDATION_RUNBOOKS.md", "inference-resource-budgets"),
        )
        self.assertEqual(
            one_local_link("README.md", "docs%2Fen%2FVALIDATION_RUNBOOKS.md#inference-resource-budgets"),
            ("docs/en/VALIDATION_RUNBOOKS.md", "inference-resource-budgets"),
        )
        self.assertEqual(
            one_local_link("docs/en/WHITEPAPER.md", "./VALIDATION_RUNBOOKS.md#gpu-memory-disturbance"),
            ("docs/en/VALIDATION_RUNBOOKS.md", "gpu-memory-disturbance"),
        )
        self.assertEqual(
            one_local_link(
                "docs/en/WHITEPAPER.md",
                "<../en/VALIDATION_RUNBOOKS.md#layer-specific-cache-isolation>",
            ),
            ("docs/en/VALIDATION_RUNBOOKS.md", "layer-specific-cache-isolation"),
        )
        self.assertEqual(
            one_local_link(
                "docs/en/VALIDATION_RUNBOOKS.md",
                '#inference%2Dresource-budgets "section"',
            ),
            ("docs/en/VALIDATION_RUNBOOKS.md", "inference-resource-budgets"),
        )
        documents = {
            "README.md": f"[budgets]({encoded})\n",
            "docs/en/VALIDATION_RUNBOOKS.md": '<a id="inference-resource-budgets"></a>\n',
        }
        self.assertEqual(
            binding_problems(
                documents,
                (("README.md", "docs/en/VALIDATION_RUNBOOKS.md", "inference-resource-budgets"),),
            ),
            [],
        )

    def test_external_history_link_is_not_a_local_topic_target(self):
        text = (
            "[history](https://github.com/timwhitez/neocloud-sec/blob/a64938821f1a28d1f435de56332f19a12051aad0/"
            "docs/en/VALIDATION_RUNBOOKS.md#inference-resource-budgets) "
            "[protocol-relative](//example.com/docs/en/VALIDATION_RUNBOOKS.md#inference-resource-budgets)"
        )
        self.assertEqual(local_link_targets(text, "README.md"), set())
        documents = self._language_documents("en")
        documents["README.md"] += "\n" + text + "\n"
        self.assertEqual(binding_problems(documents, expected_bindings("en")), [])


if __name__ == "__main__":
    unittest.main()
