"""Exercise the edit guard and checkpoint advisory through their CLI entry points."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
GUARD = PACKAGE / "scripts/guard_edits.py"
CHECKPOINT = PACKAGE / "scripts/check_checkpoint.py"
SETTINGS = ".project-kickoff/hooks.json"
VALID_CONTEXT = """# Context
## Current phase
Phase: Discovery stage 2
Phase status: Awaiting answer
## Evidence and current state
- Pending question: OQ-002
## Next action
Wait for OQ-002.
"""
VALID_DISCOVERY = """# Discovery
Current stage: Discovery stage 2
State: Awaiting answer
## Open questions and pending question
Pending question: OQ-002
## Resume checkpoint
- Last completed stage / approval: Stage 1 APR-001
- Next action: Wait for OQ-002.
"""


class ProjectHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "canonical"
        (self.root / ".project-kickoff").mkdir(parents=True)
        (self.root / "src").mkdir()
        (self.root / "config").mkdir()
        (self.root / "handoffs").mkdir()
        (self.root / "src/app.py").write_text("print('keep')\n")
        (self.root / "config/app.toml").write_text("mode = 'keep'\n")
        (self.root / "CONTEXT.md").write_text(VALID_CONTEXT)
        (self.root / ".project-kickoff/DISCOVERY.md").write_text(VALID_DISCOVERY)
        (self.root / ".project-kickoff/context-hook.json").write_text('{"enabled": true}\n')
        subprocess.run(["git", "init", "-b", "main", str(self.root)], check=True,
                       capture_output=True, text=True)
        self.write_settings()

    def write_settings(self, *, guard=True, checkpoint=True, approved=None,
                       project_root=None):
        data = {
            "version": 1,
            "project_root": str(project_root or self.root),
            "edit_guard": {
                "enabled": guard,
                "approved_paths": approved if approved is not None else [
                    "CONTEXT.md", ".project-kickoff/DISCOVERY.md",
                    "handoffs/agent-CONTEXT.md", "MISTAKES.md",
                    ".agent-team/TASKS.md",
                ],
            },
            "checkpoint_advisory": {"enabled": checkpoint},
        }
        (self.root / SETTINGS).write_text(json.dumps(data))

    def event(self, event_name, tool_name, tool_input, *, cwd=None, **extra):
        return {
            "hook_event_name": event_name,
            "session_id": "shared-session-is-not-an-actor",
            "cwd": str(cwd or self.root),
            "tool_name": tool_name,
            "tool_input": tool_input,
            **extra,
        }

    def run_script(self, script, payload=None, *, raw=None, host="codex", cwd=None):
        result = subprocess.run(
            [sys.executable, str(script), "--project-root", str(self.root),
             "--host", host],
            input=raw if raw is not None else json.dumps(payload),
            text=True, capture_output=True, cwd=cwd or self.root, timeout=3,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertLessEqual(len(result.stdout.encode()), 8192)
        return json.loads(result.stdout) if result.stdout else None

    def guard(self, payload=None, **kwargs):
        return self.run_script(GUARD, payload, **kwargs)

    def checkpoint(self, payload=None, **kwargs):
        return self.run_script(CHECKPOINT, payload, **kwargs)

    def assert_denied(self, output, phrase=None):
        specific = output["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "PreToolUse")
        self.assertEqual(specific["permissionDecision"], "deny")
        if phrase:
            self.assertIn(phrase, specific["permissionDecisionReason"])

    def advisory(self, output):
        specific = output["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "PostToolUse")
        self.assertNotIn("decision", output)
        self.assertNotIn("permissionDecision", specific)
        return specific["additionalContext"]

    def test_guard_is_opt_in_and_inactive_mode_does_not_parse_input(self):
        self.write_settings(guard=False)
        self.assertIsNone(self.guard(raw="not json"))
        (self.root / SETTINGS).unlink()
        self.assertIsNone(self.guard(raw="not json"))

    def test_active_hooks_require_a_real_canonical_git_checkout(self):
        (self.root / ".git").rename(self.root / ".git-disabled")
        guard = self.event("PreToolUse", "Write", {"file_path": "src/app.py"})
        self.assert_denied(self.guard(guard), "Git checkout")
        post = self.event("PostToolUse", "Write", {"file_path": "CONTEXT.md"})
        self.assertIn("Git checkout", self.advisory(self.checkpoint(post)))

    def test_guard_blocks_canonical_source_from_relative_or_external_cwd(self):
        payloads = [
            self.event("PreToolUse", "Write", {"file_path": "src/app.py"}),
            self.event("PreToolUse", "Edit", {"file_path": str(self.root / "src/app.py")},
                       cwd=Path(self.temp.name)),
            self.event("PreToolUse", "Write", {"file_path": "../canonical/src/app.py"},
                       cwd=Path(self.temp.name) / "sibling"),
            self.event("PreToolUse", "Edit", {"file_path": "config/app.toml"}),
        ]
        (Path(self.temp.name) / "sibling").mkdir()
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assert_denied(self.guard(payload), "task worktree")

    def test_guard_allows_only_exact_approved_canonical_paths(self):
        approved = self.event("PreToolUse", "Write", {"file_path": "CONTEXT.md"})
        self.assertIsNone(self.guard(approved, host="claude"))

        self.write_settings(approved=[".project-kickoff/*"])
        marker = self.event("PreToolUse", "Write", {
            "file_path": ".project-kickoff/context-hook.json",
        })
        self.assert_denied(self.guard(marker), "settings")

        self.write_settings(approved=[SETTINGS, ".project-kickoff/context-hook.json"])
        for relative in (SETTINGS, ".project-kickoff/context-hook.json"):
            with self.subTest(relative=relative):
                event = self.event("PreToolUse", "Edit", {"file_path": relative})
                self.assert_denied(self.guard(event), "hook configuration")

    def test_guard_parses_mixed_patch_add_delete_update_and_move_paths(self):
        patch = """*** Begin Patch
*** Update File: CONTEXT.md
@@
-old
+new
*** Add File: src/new.py
+new
*** Delete File: src/old.py
*** Update File: handoffs/agent-CONTEXT.md
*** Move to: src/moved.md
@@
-a
+b
*** End Patch"""
        event = self.event("PreToolUse", "apply_patch", {"command": patch})
        output = self.guard(event)
        self.assert_denied(output, "src/new.py")
        reason = output["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("src/old.py", reason)
        self.assertIn("src/moved.md", reason)

    def test_guard_matches_native_header_whitespace_and_rejects_environment_target(self):
        patch = ("  *** Begin Patch\n*** Add File: CONTEXT.md\n+allowed\n"
                 "   *** Add File: src/hidden.py" + "   \n"
                 "+blocked\n  *** End Patch  ")
        event = self.event("PreToolUse", "apply_patch", {"command": patch})
        self.assert_denied(self.guard(event), "src/hidden.py")

        environment_patch = """*** Begin Patch
*** Environment ID: remote
*** Add File: CONTEXT.md
+text
*** End Patch"""
        event = self.event("PreToolUse", "apply_patch", {
            "command": environment_patch,
        })
        self.assert_denied(self.guard(event), "environment")

    def test_guard_denial_output_is_bounded_for_long_patch_paths(self):
        path = "src/" + "/".join(["segment" * 20] * 12) + "/file.py"
        entries = "\n".join("*** Add File: " + path + str(index) + "\n+x"
                            for index in range(8))
        patch = "*** Begin Patch\n" + entries + "\n*** End Patch"
        event = self.event("PreToolUse", "apply_patch", {"command": patch})
        self.assert_denied(self.guard(event), "task worktree")

    def test_guard_allows_patch_when_every_canonical_path_is_approved(self):
        patch = """*** Begin Patch
*** Update File: CONTEXT.md
@@
-old
+new
*** Update File: handoffs/agent-CONTEXT.md
@@
-old
+new
*** End Patch"""
        event = self.event("PreToolUse", "apply_patch", {"command": patch})
        self.assertIsNone(self.guard(event))

    def test_guard_handles_symlink_aliases_in_both_directions(self):
        outside_alias = Path(self.temp.name) / "alias"
        outside_alias.symlink_to(self.root, target_is_directory=True)
        event = self.event("PreToolUse", "Write", {
            "file_path": str(outside_alias / "src/app.py"),
        }, cwd=Path(self.temp.name))
        self.assert_denied(self.guard(event), "src/app.py")

        external = Path(self.temp.name) / "external.txt"
        external.write_text("keep")
        linked = self.root / "src/link.txt"
        linked.symlink_to(external)
        event = self.event("PreToolUse", "Edit", {"file_path": str(linked)})
        self.assert_denied(self.guard(event), "src/link.txt")

    def test_approved_symlink_name_does_not_hide_source_or_shared_target(self):
        context = self.root / "CONTEXT.md"
        context.unlink()
        context.symlink_to(self.root / "src/app.py")
        event = self.event("PreToolUse", "Edit", {"file_path": "CONTEXT.md"})
        self.assert_denied(self.guard(event), "src/app.py")

        context.unlink()
        (self.root / "MISTAKES.md").write_text("# Shared\n")
        context.symlink_to(self.root / "MISTAKES.md")
        event = self.event("PreToolUse", "Write", {"file_path": "CONTEXT.md"},
                           agent_id="agent-123")
        self.assert_denied(self.guard(event, host="claude"), "orchestrator")

    def test_guard_allows_real_linked_worktree_nested_under_canonical(self):
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True,
                       capture_output=True, text=True)
        subprocess.run([
            "git", "-C", str(self.root), "-c", "user.name=Fixture", "-c",
            "user.email=fixture@example.test", "commit", "-m", "fixture",
        ], check=True, capture_output=True, text=True)
        worktree = self.root / ".worktrees/task"
        subprocess.run([
            "git", "-C", str(self.root), "worktree", "add", "-b", "task",
            str(worktree),
        ], check=True, capture_output=True, text=True)
        event = self.event("PreToolUse", "Write", {
            "file_path": "../../src/app.py",
        }, cwd=worktree / "deep/path")
        (worktree / "deep/path").mkdir(parents=True)
        self.assertIsNone(self.guard(event, cwd=worktree / "deep/path"))

        nested = self.root / "vendor/nested"
        nested.mkdir(parents=True)
        subprocess.run(["git", "init", "-b", "main", str(nested)], check=True,
                       capture_output=True, text=True)
        event = self.event("PreToolUse", "Write", {
            "file_path": str(nested / "source.py"),
        })
        self.assertIsNone(self.guard(event))

    def test_claude_positive_subagent_identity_protects_shared_records(self):
        for relative in ("MISTAKES.md", "CONTEXT.md", "TASKS.md",
                         ".agent-team/TASKS.md", ".agent-team/TEAMS.md"):
            with self.subTest(relative=relative):
                shared = self.event("PreToolUse", "Write", {
                    "file_path": relative,
                }, agent_id="agent-123")
                self.assert_denied(self.guard(shared, host="claude"), "orchestrator")
        assigned = self.event("PreToolUse", "Write", {
            "file_path": "handoffs/agent-CONTEXT.md",
        }, agent_id="agent-123")
        self.assertIsNone(self.guard(assigned, host="claude"))

    def test_codex_does_not_infer_actor_from_shared_fields(self):
        event = self.event("PreToolUse", "Write", {"file_path": "MISTAKES.md"},
                           agent_id="untrusted-on-codex", agent_type="worker")
        self.assertIsNone(self.guard(event, host="codex"))

    def test_guard_fails_closed_for_bad_supported_input_and_bad_settings(self):
        cases = [
            self.event("PreToolUse", "Write", {}),
            self.event("PreToolUse", "apply_patch", {"command": "not a patch"}),
        ]
        for event in cases:
            with self.subTest(event=event):
                self.assert_denied(self.guard(event), "malformed")
        self.assert_denied(self.guard(raw="{"), "malformed")
        (self.root / SETTINGS).write_text("{")
        event = self.event("PreToolUse", "Write", {"file_path": "CONTEXT.md"})
        self.assert_denied(self.guard(event), "settings")

    def test_guard_ignores_unsupported_tools_and_events(self):
        bash = self.event("PreToolUse", "Bash", {"command": "printf text > src/app.py"})
        post = self.event("PostToolUse", "Write", {"file_path": "src/app.py"})
        self.assertIsNone(self.guard(bash))
        self.assertIsNone(self.guard(post))

    def test_checkpoint_is_opt_in_and_valid_records_are_silent(self):
        context = self.event("PostToolUse", "Write", {"file_path": "CONTEXT.md"})
        self.assertIsNone(self.checkpoint(context, host="claude"))
        self.write_settings(checkpoint=False)
        self.assertIsNone(self.checkpoint(raw="not json"))

    def test_checkpoint_reports_local_missing_duplicate_and_size_diagnostics(self):
        (self.root / "CONTEXT.md").write_text("""## Current phase
Phase: Discovery
Phase: Setup
## Evidence and current state
- Pending question: OQ-1
## Next action
""")
        event = self.event("PostToolUse", "Edit", {"file_path": "CONTEXT.md"})
        message = self.advisory(self.checkpoint(event, host="claude"))
        self.assertIn("conflicting Phase entries", message)
        self.assertIn("missing Status", message)
        self.assertIn("missing Next action", message)
        self.assertNotIn("DISCOVERY.md", message)

        (self.root / "CONTEXT.md").write_text("x" * 65537)
        message = self.advisory(self.checkpoint(event))
        self.assertIn("too large", message)

    def test_checkpoint_checks_each_edited_record_without_cross_file_comparison(self):
        (self.root / ".project-kickoff/DISCOVERY.md").write_text(
            VALID_DISCOVERY.replace("OQ-002", "OQ-999"))
        patch = """*** Begin Patch
*** Update File: CONTEXT.md
@@
-a
+b
*** Update File: .project-kickoff/DISCOVERY.md
@@
-a
+b
*** End Patch"""
        event = self.event("PostToolUse", "apply_patch", {"command": patch})
        self.assertIsNone(self.checkpoint(event))

    def test_checkpoint_reports_malformed_supported_input_but_ignores_other_paths(self):
        malformed = self.event("PostToolUse", "Write", {})
        self.assertIn("malformed", self.advisory(self.checkpoint(malformed)))
        source = self.event("PostToolUse", "Edit", {"file_path": "src/app.py"})
        self.assertIsNone(self.checkpoint(source, host="claude"))
        unsupported = self.event("PostToolUse", "Bash", {"command": "true"})
        self.assertIsNone(self.checkpoint(unsupported))

    def test_hooks_are_read_only_for_project_bytes(self):
        def snapshot():
            return {
                str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob("*") if path.is_file()
            }
        before = snapshot()
        guard = self.event("PreToolUse", "Write", {"file_path": "src/app.py"})
        checkpoint = self.event("PostToolUse", "Write", {"file_path": "CONTEXT.md"})
        self.guard(guard)
        self.checkpoint(checkpoint)
        self.assertEqual(before, snapshot())

    def test_example_commands_run_each_public_entry_point(self):
        (self.root / "CONTEXT.md").write_text("# Missing checkpoint fields\n")
        for host in ("codex", "claude"):
            with self.subTest(host=host):
                example = json.loads(
                    (PACKAGE / f"assets/hooks/{host}-session-start.json").read_text())
                replacements = (
                    ("'/ABSOLUTE/PYTHON3'", shlex.quote(sys.executable)),
                    ("'/ABSOLUTE/SKILL/PATH/scripts/guard_edits.py'",
                     shlex.quote(str(GUARD))),
                    ("'/ABSOLUTE/SKILL/PATH/scripts/check_checkpoint.py'",
                     shlex.quote(str(CHECKPOINT))),
                    ("'/ABSOLUTE/PROJECT/ROOT'", shlex.quote(str(self.root))),
                )
                for event_name, payload, expected in (
                    ("PreToolUse", self.event("PreToolUse", "Write", {
                        "file_path": "src/app.py",
                    }), "permissionDecision"),
                    ("PostToolUse", self.event("PostToolUse", "Write", {
                        "file_path": "CONTEXT.md",
                    }), "additionalContext"),
                ):
                    command = example["hooks"][event_name][0]["hooks"][0]["command"]
                    for before, after in replacements:
                        command = command.replace(before, after)
                    result = subprocess.run(
                        command, shell=True, text=True, capture_output=True,
                        input=json.dumps(payload), cwd=self.root, timeout=3,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    specific = json.loads(result.stdout)["hookSpecificOutput"]
                    self.assertIn(expected, specific)


if __name__ == "__main__":
    unittest.main()
