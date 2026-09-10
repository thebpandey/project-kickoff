"""Check package version consistency and the README release allowlists.

The release ships a fixed set of files. Development evidence, the rendered
guide, and this test suite stay out of it. Both README install blocks repeat the
same allowlist, so drift between them, the package, and the release tree is easy
to miss during review.
"""

import json
import re
import subprocess
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
README = PACKAGE / "README.md"
SKILL = PACKAGE / "SKILL.md"
CHANGELOG = PACKAGE / "CHANGELOG.md"
HANDOFF_TEMPLATE = PACKAGE / "assets/templates/AGENT_TEAM_HANDOFF.json"

# Tracked paths that stay in the development repository.
DEVELOPMENT_FILES = {".gitignore", "scripts/check-guide.mjs"}
DEVELOPMENT_PREFIXES = ("docs/", "tests/", "assets/guide/")
DEVELOPMENT_SUFFIXES = (".html",)


def package_files():
    """Return the release file set, taken from Git rather than the README."""
    listed = subprocess.check_output(
        ["git", "-C", str(PACKAGE), "ls-files"], text=True,
    ).splitlines()
    kept = set()
    for path in listed:
        if path in DEVELOPMENT_FILES:
            continue
        if path.startswith(DEVELOPMENT_PREFIXES):
            continue
        if path.endswith(DEVELOPMENT_SUFFIXES):
            continue
        kept.add(path)
    return kept


def readme_allowlists(text):
    return re.findall(r"kickoff_required_files='([^']*)'", text)


def release_tree(text):
    match = re.search(r"```text\n(project-kickoff/\n.*?)```", text, re.S)
    return match.group(1) if match else ""


def skill_version(text):
    match = re.search(r'^\s+version:\s*"([^"]+)"\s*$', text, re.M)
    return match.group(1) if match else ""


def newest_changelog_version(text):
    match = re.search(r"^## \[([^\]]+)\] - \d{4}-\d{2}-\d{2}\s*$", text, re.M)
    return match.group(1) if match else ""


class PackageManifestTest(unittest.TestCase):
    def setUp(self):
        self.readme = README.read_text(encoding="utf-8")
        self.files = package_files()

    def test_readme_repeats_one_identical_allowlist(self):
        allowlists = readme_allowlists(self.readme)
        self.assertEqual(len(allowlists), 2, "README must hold two install allowlists")
        self.assertEqual(
            allowlists[0].split(),
            allowlists[1].split(),
            "the Codex and Claude Code allowlists must be identical",
        )

    def test_allowlists_match_the_package_files(self):
        for index, allowlist in enumerate(readme_allowlists(self.readme)):
            listed = allowlist.split()
            with self.subTest(allowlist=index):
                self.assertEqual(len(listed), len(set(listed)), "duplicate entry")
                self.assertEqual(
                    set(listed),
                    self.files,
                    "README allowlist does not match the package files",
                )

    def test_release_tree_names_every_package_file(self):
        tree = release_tree(self.readme)
        self.assertTrue(tree, "README must hold the release tree block")
        for path in sorted(self.files):
            with self.subTest(path=path):
                self.assertIn(Path(path).name, tree)

    def test_package_version_is_consistent(self):
        version = skill_version(SKILL.read_text(encoding="utf-8"))
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertEqual(
            newest_changelog_version(CHANGELOG.read_text(encoding="utf-8")),
            version,
            "the newest CHANGELOG entry must match SKILL.md metadata.version",
        )
        handoff = json.loads(HANDOFF_TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(handoff["projectKickoff"]["version"], version)

        self.assertIn(f"Current version: **{version}**", self.readme)
        self.assertIn(f"Project Kickoff v{version}\n", self.readme)
        self.assertIn(f"project-kickoff-{version}.zip", self.readme)

        tags = set(re.findall(r"--branch (v[0-9][^\s]*)", self.readme))
        self.assertEqual(
            tags,
            {f"v{version}"},
            "README install examples must pin the current release tag",
        )


if __name__ == "__main__":
    unittest.main()
