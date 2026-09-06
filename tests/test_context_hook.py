"""Run with python3 -m unittest discover -s tests -v."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/load_context.py"
SUMMARY = """# Fixture
Current stage: Discovery stage 2
State: Awaiting answer
## Current phase
Phase: Discovery stage 2
Phase status: Awaiting answer
## Approved decisions needed for resumption
| DEC-001 | Launch scope | APR-001 | PRD.md |
## Evidence and current state
- Pending question: OQ-002
## Next action
Wait for OQ-002; do no dependent work.
## Open questions and pending question
Pending question: OQ-002
## Resume checkpoint
- Last completed stage / approval: Stage 1 APR-001
- Next action: Wait for OQ-002; do no dependent work.

## History
PRIVATE_DIARY_DO_NOT_LOAD
"""


class ContextHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        (self.root / ".project-kickoff").mkdir(parents=True)
        self.marker = self.root / ".project-kickoff/context-hook.json"
        self.marker.write_text('{"enabled": true}')
        (self.root / "CONTEXT.md").write_text(SUMMARY)
        (self.root / ".project-kickoff/DISCOVERY.md").write_text(SUMMARY)

    def run_hook(self, payload=None, raw=None, project_root=None, cwd=None):
        payload = payload or {"hook_event_name": "SessionStart", "source": "resume", "cwd": str(self.root)}
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project-root", str(project_root or self.root)],
            input=raw if raw is not None else json.dumps(payload), text=True,
            capture_output=True, cwd=cwd or self.root, timeout=3,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertLessEqual(len(result.stdout.encode()), 8192)
        if not result.stdout:
            return ""
        output = json.loads(result.stdout)
        self.assertEqual(set(output), {"hookSpecificOutput"})
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
        return output["hookSpecificOutput"]["additionalContext"]

    def test_active_events_both_hosts(self):
        for host in ("codex", "claude"):
            for source in ("startup", "resume", "clear", "compact"):
                with self.subTest(host=host, source=source):
                    payload = {"hook_event_name": "SessionStart", "source": source,
                               "cwd": str(self.root), "session_id": host + "-fixture",
                               "transcript_path": "/unreadable/do-not-read.jsonl"}
                    output = self.run_hook(payload)
                    self.assertIn("OQ-002", output)
                    self.assertIn("APR-001", output)
                    self.assertIn("untrusted reference data", output)
                    self.assertNotIn("PRIVATE_DIARY", output)

    def test_inactive_is_silent_even_with_bad_input(self):
        for content in ('{"enabled": false}', '{"enabled": "true"}', '{}'):
            self.marker.write_text(content)
            self.assertEqual(self.run_hook(raw="not json"), "")
        self.marker.unlink()
        self.assertEqual(self.run_hook(raw="not json"), "")

    def test_bad_marker_and_input_are_nonblocking_diagnostics(self):
        self.marker.write_text("{")
        self.assertIn("marker", self.run_hook())
        self.marker.write_text('{"enabled": true}')
        for raw in ("{", "[]", "x" * 65537):
            self.assertIn("input", self.run_hook(raw=raw))

    def test_missing_and_oversized_records(self):
        context = self.root / "CONTEXT.md"
        context.unlink()
        self.assertIn("CONTEXT.md", self.run_hook())
        context.write_text("x" * 65537)
        self.assertIn("too large", self.run_hook())
        context.write_bytes(b"\xff")
        self.assertIn("unreadable", self.run_hook())

    def test_only_known_fields_and_conflicts(self):
        (self.root / "CONTEXT.md").write_text(SUMMARY.replace("OQ-002", "OQ-003"))
        self.assertIn("conflicting Pending question", self.run_hook())
        (self.root / "CONTEXT.md").write_text("# Legacy\nPhase: Old\nPRIVATE_DIARY")
        output = self.run_hook()
        self.assertIn("no supported checkpoint fields", output)
        self.assertNotIn("PRIVATE_DIARY", output)

    def test_large_summary_is_bounded(self):
        summary = "## Current phase\nPhase: " + "😀" * 2500 + "\n## Next action\n" + "😀" * 2500
        (self.root / "CONTEXT.md").write_text(summary)
        (self.root / ".project-kickoff/DISCOVERY.md").write_text(summary)
        self.assertIn("truncated", self.run_hook())

    def test_symlinks_and_nonregular_files_not_read(self):
        context = self.root / "CONTEXT.md"
        external = Path(self.temp.name) / "secret"
        external.write_text(SUMMARY.replace("OQ-002", "PRIVATE_SECRET"))
        context.unlink()
        context.symlink_to(external)
        output = self.run_hook()
        self.assertNotIn("PRIVATE_SECRET", output)
        self.assertIn("unreadable", output)
        context.unlink()
        os.mkfifo(context)
        self.assertIn("not a regular file", self.run_hook())

    def test_symlinked_record_directory_not_read(self):
        directory = self.root / ".project-kickoff"
        directory.rename(self.root / "other")
        directory.symlink_to(self.root / "other", target_is_directory=True)
        self.assertIn("marker", self.run_hook())

    def test_explicit_root_subdirectory_and_other_checkouts(self):
        subdir = self.root / "src"
        subdir.mkdir()
        payload = {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(subdir)}
        self.assertIn("OQ-002", self.run_hook(payload, cwd=subdir))
        (subdir / ".git").write_text("gitdir: /never/read/this")
        self.assertEqual(self.run_hook(payload, cwd=subdir), "")
        payload["cwd"] = self.temp.name
        self.assertEqual(self.run_hook(payload), "")
        self.assertIn("absolute", self.run_hook(project_root="."))

    def test_other_events_are_silent(self):
        self.assertEqual(self.run_hook({"hook_event_name": "UserPromptSubmit", "source": "resume", "cwd": str(self.root)}), "")

    def test_project_bytes_and_git_state_unchanged(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args])
        git("init", "-b", "main")
        git("add", ".")
        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.test", "commit", "-m", "fixture")
        (self.root / "untracked.txt").write_text("keep me")
        def snapshot():
            return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        status = git("status", "--porcelain=v1")
        self.run_hook()
        self.assertEqual(before, snapshot())
        self.assertEqual(status, git("status", "--porcelain=v1"))


if __name__ == "__main__":
    unittest.main()
