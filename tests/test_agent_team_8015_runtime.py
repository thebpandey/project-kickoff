"""Opt-in cross-repository qualification for Project Kickoff 0.5.2."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
CHECKER = PACKAGE / "scripts/check_agent_team_handoff.py"
AGENT_TEAM_SOURCE = os.environ.get("AGENT_TEAM_8015_SOURCE", "")
BD_EXECUTABLE = os.environ.get("BD_122_EXECUTABLE", shutil.which("bd") or "")


@unittest.skipUnless(AGENT_TEAM_SOURCE and BD_EXECUTABLE,
                     "requires AGENT_TEAM_8015_SOURCE and bd 1.2.2")
class AgentTeam8015RuntimeQualification(unittest.TestCase):
    def run_command(self, *args, cwd=None):
        return subprocess.run(args, cwd=cwd, env={**os.environ, "BD_NON_INTERACTIVE": "1"},
                              capture_output=True, text=True, timeout=120)

    def require_command(self, *args, cwd=None):
        result = self.run_command(*args, cwd=cwd)
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        return result

    def test_same_real_beads_handoff_checks_and_reserves(self):
        version = self.require_command(BD_EXECUTABLE, "--version").stdout
        self.assertIn("1.2.2", version)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            self.require_command("git", "init", "-q", "-b", "main", str(root))
            self.require_command("git", "config", "user.name", "Fixture", cwd=root)
            self.require_command("git", "config", "user.email", "fixture@example.test", cwd=root)
            (root / "README.md").write_text("fixture\n")
            self.require_command("git", "add", "README.md", cwd=root)
            self.require_command("git", "commit", "-qm", "fixture", cwd=root)
            self.require_command(BD_EXECUTABLE, "init", "--non-interactive", "--skip-agents",
                                 "--skip-hooks", "--prefix", "fixture", cwd=root)
            metadata = json.dumps({
                "criteria": ["done"],
                "checks": [{"name": "test", "command": ["true"]}],
            }, separators=(",", ":"))
            for epic in ("fixture-e1", "fixture-e2"):
                self.require_command(BD_EXECUTABLE, "create", "--id", epic, "--title", epic,
                                     "--type", "epic", cwd=root)
            for task_id, parent, kind in (
                    ("fixture-a", "fixture-e1", "task"),
                    ("fixture-d1", "fixture-e1", "decision"),
                    ("fixture-b", "fixture-e2", "task"),
                    ("fixture-d2", "fixture-e2", "decision")):
                command = [BD_EXECUTABLE, "create", "--id", task_id, "--title", task_id,
                           "--type", kind]
                if kind == "task":
                    command += ["--metadata", metadata]
                self.require_command(*command, cwd=root)
                self.require_command(BD_EXECUTABLE, "update", task_id, "--parent", parent, cwd=root)
                if kind == "decision":
                    self.require_command(BD_EXECUTABLE, "update", task_id, "--status", "blocked", cwd=root)
            self.require_command(BD_EXECUTABLE, "create", "--id", "fixture-closed",
                                 "--title", "closed unrelated", "--type", "task", cwd=root)
            self.require_command(BD_EXECUTABLE, "close", "fixture-closed", cwd=root)
            revision = self.require_command("git", "rev-parse", "HEAD", cwd=root).stdout.strip()

            handoff = {
                "schemaVersion": 1,
                "kind": "project-kickoff-agent-team-handoff",
                "status": "approved",
                "projectKickoff": {"version": "0.5.2", "approvalId": "APR-8015",
                                   "approvedRevision": revision},
                "agentTeam": {"testedVersion": "8.0.15", "initializationSource": "existing"},
                "project": {"id": "fixture", "root": str(root), "branch": "main",
                            "revision": revision},
                "tracker": {"kind": "beads", "executable": str(Path(BD_EXECUTABLE).resolve())},
                "plan": {
                    "scope": "two approved epics",
                    "acceptance": ["done"],
                    "verification": ["true"],
                    "branch": "main",
                    "authority": {"ownedPaths": ["Packages/Feature/**"], "externalActions": []},
                    "tasks": [{"id": "fixture-b"}, {"id": "fixture-a"}],
                },
            }
            handoff_dir = root / ".project-kickoff"
            handoff_dir.mkdir()
            handoff_path = handoff_dir / "AGENT_TEAM_HANDOFF.json"
            handoff_path.write_text(json.dumps(handoff))

            checked = self.require_command("python3", str(CHECKER), "--handoff",
                                           str(handoff_path), cwd=root)
            checked_output = json.loads(checked.stdout)
            self.assertEqual(checked_output["compatibility"], "runtime-qualified")
            self.assertTrue(checked_output["runtimeVerified"])

            binary = Path(temporary) / "agent-teamctl"
            self.require_command("go", "build", "-o", str(binary), "./cmd/agent-teamctl",
                                 cwd=Path(AGENT_TEAM_SOURCE) / "vnext")

            def controller(*args):
                result = self.require_command(str(binary), *args, "--json", cwd=root)
                return json.loads(result.stdout)

            setup = controller("setup", "--kickoff", ".project-kickoff/AGENT_TEAM_HANDOFF.json",
                               "--approve-kickoff", "--approve")
            self.assertEqual(setup["next_action"], "settings")
            controller("settings", "claude.developer.model=inherit",
                       "claude.reviewer.model=inherit")
            started = controller("start", "--host", "claude")
            self.assertTrue(started["host_dispatch_required"])
            self.assertEqual(started["actual_host"], "claude")
            self.assertEqual(started["packet"]["task"], "fixture-a")
            self.assertEqual(started["packet"]["scope"], ["packages/feature/**"])


if __name__ == "__main__":
    unittest.main()
