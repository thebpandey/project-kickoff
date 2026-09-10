"""Validate the Project Kickoff to Agent-Team handoff contract."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
CHECKER = PACKAGE / "scripts/check_agent_team_handoff.py"
TEMPLATE = PACKAGE / "assets/templates/AGENT_TEAM_HANDOFF.json"


def valid_handoff(root):
    revision = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True,
    ).strip()
    return {
        "schemaVersion": 1,
        "kind": "project-kickoff-agent-team-handoff",
        "status": "approved",
        "projectKickoff": {
            "version": "0.3.0",
            "approvalId": "APR-005",
            "approvedRevision": revision,
        },
        "agentTeam": {"testedVersion": "7.0.2", "initializationSource": "existing"},
        "project": {
            "id": "fixture-project",
            "root": str(root),
            "branch": "main",
            "revision": revision,
        },
        "tracker": {"kind": "markdown", "path": "TASKS.md"},
        "plan": {
            "scope": "Implement the approved first release.",
            "acceptance": ["The approved behavior passes its checks."],
            "verification": ["python3 -m unittest discover -s tests -v"],
            "branch": "main",
            "authority": {"ownedPaths": ["src/**", "tests/**"], "externalActions": []},
            "tasks": [{"id": "AT-001"}],
        },
    }


class AgentTeamHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Fixture"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "fixture@example.test"], check=True)
        (self.root / "TASKS.md").write_text(
            "# Agent-Team Tasks\n\n"
            "| ID | Requirement / acceptance | Owner | Depends on | Status | Revision / evidence | Next action |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            "| AT-001 | Approved behavior | unassigned | none | ready | none | Implement the plan. |\n"
        )
        subprocess.run(["git", "-C", str(self.root), "add", "TASKS.md"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture tracker"], check=True)

    def check(self, handoff):
        path = self.root / "AGENT_TEAM_HANDOFF.json"
        path.write_text(json.dumps(handoff))
        return subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(path)],
            capture_output=True, text=True, timeout=3,
        )

    def emit_request(self, handoff):
        path = self.root / "AGENT_TEAM_HANDOFF.json"
        path.write_text(json.dumps(handoff))
        return subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(path),
             "--emit-request", "--actor-session-id", "project-owner",
             "--operation-id", "initialize-project-kickoff-handoff",
             "--expected-version", "0"],
            capture_output=True, text=True, timeout=3,
        )

    def test_package_declares_the_machine_readable_handoff(self):
        template = json.loads(TEMPLATE.read_text())
        self.assertEqual(template["schemaVersion"], 1)
        self.assertEqual(template["kind"], "project-kickoff-agent-team-handoff")
        self.assertEqual(template["agentTeam"]["testedVersion"], "7.0.2")
        self.assertIn("tasks", template["plan"])
        self.assertEqual(set(template["plan"]["tasks"][0]), {"id"})

        setup = (PACKAGE / "references/setup.md").read_text()
        handoff = (PACKAGE / "references/handoff.md").read_text()
        readme = (PACKAGE / "README.md").read_text()
        tracker = (PACKAGE / "assets/templates/TASKS.md").read_text()
        for source in (setup, handoff, readme):
            self.assertIn("AGENT_TEAM_HANDOFF.json", source)
        self.assertIn("Do not create or edit `.agent-team/setup.json`", setup)
        self.assertIn(".project-kickoff/setup.json", setup)
        self.assertIn("| AT-001", tracker)
        self.assertIn("| {{ready}} |", tracker)
        self.assertNotIn("| {{planned}} |", tracker)

    def test_checker_accepts_the_702_contract(self):
        result = self.check(valid_handoff(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "passed")
        self.assertEqual(output["agentTeamVersion"], "7.0.2")
        self.assertEqual(output["taskCount"], 1)

    def test_checker_emits_a_direct_agent_team_request(self):
        handoff = valid_handoff(self.root)
        result = self.emit_request(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)
        request = json.loads(result.stdout)
        self.assertEqual(request["schemaVersion"], 1)
        self.assertEqual(request["actorSessionId"], "project-owner")
        self.assertEqual(request["expectedVersion"], 0)
        self.assertEqual(request["request"]["projectId"], handoff["project"]["id"])
        self.assertEqual(request["request"]["source"], "existing")
        self.assertEqual(request["request"]["tracker"], handoff["tracker"])
        self.assertEqual(request["request"]["plan"], handoff["plan"])

    def test_checker_rejects_limits_and_non_actionable_status(self):
        cases = []
        too_many = valid_handoff(self.root)
        too_many["plan"]["tasks"] = [{"id": f"AT-{index:03d}"} for index in range(1, 502)]
        cases.append(("501 tasks", too_many))

        duplicate = valid_handoff(self.root)
        duplicate["plan"]["tasks"].append(copy.deepcopy(duplicate["plan"]["tasks"][0]))
        cases.append(("duplicate task ID", duplicate))

        unsafe = valid_handoff(self.root)
        unsafe["plan"]["authority"]["ownedPaths"] = ["../outside/**"]
        cases.append(("unsafe owned path", unsafe))

        alternative = valid_handoff(self.root)
        alternative["tracker"] = {"kind": "other", "path": "BACKLOG.md"}
        cases.append(("unsupported tracker", alternative))

        non_ascii = valid_handoff(self.root)
        non_ascii["plan"]["tasks"][0]["id"] = "AT-é"
        cases.append(("invalid task ID", non_ascii))

        duplicated_content = valid_handoff(self.root)
        duplicated_content["plan"]["tasks"][0]["title"] = "Duplicate tracker content"
        cases.append(("handoff tasks must contain only id", duplicated_content))

        for phrase, value in cases:
            with self.subTest(phrase=phrase):
                result = self.check(value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(phrase, result.stderr)

    def test_checker_rejects_planned_tracker_status(self):
        handoff = valid_handoff(self.root)
        (self.root / "TASKS.md").write_text(
            (self.root / "TASKS.md").read_text().replace("| ready |", "| planned |")
        )
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("status planned", result.stderr)

    def test_checker_rejects_a_tracker_identity_mismatch(self):
        handoff = valid_handoff(self.root)
        handoff["plan"]["tasks"][0]["id"] = "AT-002"
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tracker task IDs do not exactly match", result.stderr)

    def test_checker_rejects_an_oversized_handoff(self):
        handoff = valid_handoff(self.root)
        handoff["padding"] = "x" * (250 * 1024)
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("handoff exceeds", result.stderr)

    def test_checker_preserves_a_cancelled_history_row(self):
        with (self.root / "TASKS.md").open("a") as tracker:
            tracker.write(
                "| AT-OLD | Historical work | unassigned | none | cancelled | none | None. |\n"
            )
        handoff = valid_handoff(self.root)
        handoff["plan"]["tasks"].append({
            "id": "AT-OLD",
        })
        result = self.check(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_checker_rejects_an_unreachable_approved_revision(self):
        handoff = valid_handoff(self.root)
        handoff["projectKickoff"]["approvedRevision"] = "a" * 40
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("approved revision is not on the integration branch", result.stderr)

    def test_checker_rejects_a_stale_integration_tip(self):
        handoff = valid_handoff(self.root)
        handoff["project"]["revision"] = "b" * 40
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("project.revision must match the integration branch tip", result.stderr)

    def test_beads_read_can_exceed_the_old_1_5_second_limit(self):
        executable = self.root / "slow-bd"
        executable.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "import time\n"
            "time.sleep(1.6)\n"
            "print(json.dumps([{'id': 'AT-001', 'title': 'Approved behavior', "
            "'status': 'ready', 'assignee': '', 'dependency_count': 0, "
            "'dependencies': []}]))\n"
        )
        executable.chmod(0o700)
        handoff = valid_handoff(self.root)
        handoff["tracker"] = {"kind": "beads", "executable": str(executable)}
        result = self.check(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.environ.get("AGENT_TEAM_ROOT"),
                         "set AGENT_TEAM_ROOT for real Agent-Team qualification")
    def test_real_agent_team_702_adopts_the_handoff(self):
        agent_team = Path(os.environ["AGENT_TEAM_ROOT"]).resolve()
        version = (agent_team / "SKILL.md").read_text()
        self.assertIn('version: "7.0.2"', version)

        (self.root / "README.md").write_text("Fixture project.\n")
        (self.root / "TASKS.md").write_text(
            "# Agent-Team Tasks\n\n"
            "| ID | Requirement / acceptance | Owner | Depends on | Status | Revision / evidence | Next action |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            "| AT-001 | Approved behavior | unassigned | none | ready | none | Implement the plan. |\n"
        )
        subprocess.run(["git", "-C", str(self.root), "add", "README.md", "TASKS.md"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture project"], check=True)

        handoff = valid_handoff(self.root)
        handoff["projectKickoff"]["approvedRevision"] = subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True,
        ).strip()
        emitted = self.emit_request(handoff)
        self.assertEqual(emitted.returncode, 0, emitted.stderr)
        envelope = json.loads(emitted.stdout)
        request = self.root / "initialization.json"
        request.write_text(json.dumps(envelope))
        cli = agent_team / "hooks/agent-team-cli.mjs"
        result = subprocess.run(
            ["node", str(cli), "project-initialize", "--project", str(self.root),
             "--request", str(request)], capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        initialized = json.loads(result.stdout)
        self.assertEqual(initialized["status"], "applied")
        self.assertTrue(initialized["canonicalReady"])
        self.assertEqual(initialized["taskIds"], ["AT-001"])

        readiness = subprocess.run(
            ["node", str(cli), "readiness", "--project", str(self.root),
             "--host", "codex", "--scope", "user"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(readiness.returncode, 0, readiness.stderr)
        state = json.loads(readiness.stdout)
        self.assertFalse(state["projectInitialization"]["required"])


if __name__ == "__main__":
    unittest.main()
