"""Validate the Project Kickoff to Agent-Team handoff contract."""

import copy
import hashlib
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
            "version": "0.5.0",
            "approvalId": "APR-005",
            "approvedRevision": revision,
        },
        "agentTeam": {"testedVersion": "7.3.1", "initializationSource": "existing"},
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
            "requiredCapabilities": ["graphify"],
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

    def commit_file(self, name, contents, message="fixture descendant"):
        (self.root / name).write_text(contents)
        subprocess.run(["git", "-C", str(self.root), "add", name], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", message], check=True)
        return subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True,
        ).strip()

    def test_package_declares_the_machine_readable_handoff(self):
        template = json.loads(TEMPLATE.read_text())
        self.assertEqual(template["schemaVersion"], 1)
        self.assertEqual(template["kind"], "project-kickoff-agent-team-handoff")
        self.assertEqual(template["agentTeam"]["testedVersion"], "7.3.1")
        self.assertEqual(template["plan"]["requiredCapabilities"], ["graphify"])
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

    def test_checker_accepts_the_731_contract(self):
        result = self.check(valid_handoff(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "passed")
        self.assertEqual(output["agentTeamVersion"], "7.3.1")
        self.assertEqual(output["taskCount"], 1)

    def native_handoff(self, version="8.0.11"):
        (self.root / "TASKS.md").write_text(
            "# Tasks\n\n## Active tasks\n"
            "| ID | Intended outcome / acceptance pointer | Owner | Depends on | Status |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| AT-001 | Approved behavior | unassigned | none | ready |\n"
        )
        handoff = valid_handoff(self.root)
        handoff["agentTeam"]["testedVersion"] = version
        return handoff

    def test_native_schema_check_does_not_claim_runtime_verified(self):
        for version in ("8.0.10", "8.0.11"):
            with self.subTest(version=version):
                result = self.check(self.native_handoff(version))
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output["agentTeamVersion"], version)
                self.assertEqual(output["compatibility"], "schema-only")
                self.assertFalse(output["runtimeVerified"])
                self.assertEqual(output["requiredSetupContract"], "status-and-next-action")

    def test_native_handoff_does_not_emit_legacy_identity_request(self):
        result = self.emit_request(self.native_handoff())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("native setup", result.stderr)
        self.assertNotIn("actorSessionId", result.stdout)

    def test_native_rejects_stale_revision_and_external_actions(self):
        handoff = self.native_handoff()
        handoff["plan"]["authority"]["externalActions"] = ["deploy"]
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("separate native authority", result.stderr)
        handoff["plan"]["authority"]["externalActions"] = []
        self.commit_file("later.txt", "later")
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("current branch tip", result.stderr)

    def test_native_rejects_handoff_outside_project(self):
        handoff = self.native_handoff()
        path = Path(self.temp.name) / "outside.json"
        path.write_text(json.dumps(handoff))
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(path)],
            capture_output=True, text=True, timeout=3,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("within project.root", result.stderr)

    def test_native_rejects_unsupported_table_shape_and_unsafe_path(self):
        handoff = self.native_handoff()
        handoff["plan"]["authority"]["ownedPaths"] = ["../outside"]
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe owned path", result.stderr)
        handoff["plan"]["authority"]["ownedPaths"] = ["src/**"]
        path = self.root / "TASKS.md"
        path.write_text(path.read_text().replace("## Active tasks", "## Other tasks"))
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Active tasks", result.stderr)

    @unittest.skipIf(os.name == "nt", "symlink creation may require privileges")
    def test_native_rejects_symlinked_tracker_and_owned_path_escapes(self):
        handoff = self.native_handoff()
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "TASKS.md").write_text((self.root / "TASKS.md").read_text())
        (self.root / ".agent-team").symlink_to(outside, target_is_directory=True)
        handoff["tracker"]["path"] = ".agent-team/TASKS.md"
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("escapes project.root", result.stderr)
        handoff["tracker"]["path"] = "TASKS.md"
        handoff["plan"]["authority"]["ownedPaths"] = [".agent-team/**"]
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("escapes project.root", result.stderr)

    def test_checker_emits_a_direct_agent_team_request(self):
        handoff = valid_handoff(self.root)
        result = self.emit_request(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)
        request = json.loads(result.stdout)
        self.assertEqual(set(request), {"schemaVersion", "actorSessionId", "expectedVersion", "request"})
        self.assertEqual(set(request["request"]), {
            "projectId", "operationId", "source", "tracker", "plan", "handoff",
        })
        self.assertEqual(request["schemaVersion"], 1)
        self.assertEqual(request["actorSessionId"], "project-owner")
        self.assertEqual(request["expectedVersion"], 0)
        self.assertEqual(request["request"]["projectId"], handoff["project"]["id"])
        self.assertEqual(request["request"]["source"], "existing")
        self.assertEqual(request["request"]["tracker"], handoff["tracker"])
        self.assertEqual(request["request"]["plan"], handoff["plan"])
        self.assertEqual(request["request"]["plan"]["requiredCapabilities"], ["graphify"])
        self.assertEqual(set(request["request"]["handoff"]), {
            "schemaVersion", "path", "sha256", "generatedBy", "testedAgainst",
            "generationBaseline", "observedRevision",
        })

    def test_checker_copies_required_capabilities_to_the_agent_team_request(self):
        handoff = valid_handoff(self.root)
        handoff["plan"]["requiredCapabilities"] = ["graphify", "serena"]
        result = self.emit_request(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)
        request = json.loads(result.stdout)
        self.assertEqual(request["request"]["plan"]["requiredCapabilities"], ["graphify", "serena"])

    def test_checker_rejects_invalid_required_capabilities(self):
        cases = [
            ("plan.requiredCapabilities must be a bounded unique list of safe capability IDs", "graphify"),
            ("duplicate required capability ID", ["graphify", "graphify"]),
            ("invalid required capability ID", ["../graphify"]),
            ("101 required capabilities", [f"cap-{index}" for index in range(101)]),
        ]
        for phrase, required_capabilities in cases:
            with self.subTest(phrase=phrase):
                handoff = valid_handoff(self.root)
                handoff["plan"]["requiredCapabilities"] = required_capabilities
                result = self.check(handoff)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(phrase, result.stderr)

    def test_checker_rejects_limits_and_non_actionable_status(self):
        cases = []
        too_many = valid_handoff(self.root)
        too_many["plan"]["tasks"] = [{"id": f"AT-{index:04d}"} for index in range(1, 1002)]
        cases.append(("1001 tasks", too_many))

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

    def test_checker_accepts_the_default_1000_task_boundary(self):
        task_ids = [f"AT-{index:04d}" for index in range(1, 1001)]
        rows = "".join(
            f"| {task_id} | Approved behavior | unassigned | none | ready | none | Implement the plan. |\n"
            for task_id in task_ids
        )
        (self.root / "TASKS.md").write_text(
            "# Agent-Team Tasks\n\n"
            "| ID | Requirement / acceptance | Owner | Depends on | Status | Revision / evidence | Next action |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n" + rows
        )
        handoff = valid_handoff(self.root)
        handoff["plan"]["tasks"] = [{"id": task_id} for task_id in task_ids]
        result = self.check(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["taskCount"], 1000)

    def test_checker_rejects_agent_team_lane_runtime_state(self):
        for field in ("lanes", "claims", "assignments", "briefs", "workerIdentities", "capacity"):
            with self.subTest(field=field):
                handoff = valid_handoff(self.root)
                handoff["plan"][field] = []
                result = self.check(handoff)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Agent-Team runtime state", result.stderr)

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
        self.assertIn("approved revision is not an ancestor of the generation baseline", result.stderr)

    def test_checker_accepts_a_committed_handoff_descendant(self):
        handoff = valid_handoff(self.root)
        self.commit_file("README.md", "descendant\n")
        result = self.check(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_checker_rejects_an_unrelated_generation_revision(self):
        handoff = valid_handoff(self.root)
        tree = subprocess.check_output(
            ["git", "-C", str(self.root), "write-tree"], text=True,
        ).strip()
        unrelated = subprocess.check_output(
            ["git", "-C", str(self.root), "commit-tree", tree, "-m", "unrelated"],
            text=True,
        ).strip()
        handoff["project"]["revision"] = unrelated
        handoff["projectKickoff"]["approvedRevision"] = unrelated
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generation baseline is not an ancestor of the observed branch tip", result.stderr)

    def test_checker_rejects_approved_revision_after_generation_baseline(self):
        handoff = valid_handoff(self.root)
        approved = self.commit_file("README.md", "after baseline\n")
        handoff["projectKickoff"]["approvedRevision"] = approved
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("approved revision is not an ancestor of the generation baseline", result.stderr)

    def test_checker_enforces_the_supported_compatibility_matrix(self):
        supported = [
            ("0.3.1", "7.0.2"),
            ("0.4.0", "7.0.2"),
            ("0.4.1", "7.1.0"),
            ("0.4.1", "7.2.0"),
            ("0.4.1", "7.2.1"),
            ("0.4.2", "7.2.3"),
            ("0.4.2", "7.2.4"),
            ("0.4.2", "7.2.5"),
            ("0.4.2", "7.2.6"),
            ("0.5.0", "7.3.0"),
            ("0.5.0", "7.3.1"),
        ]
        for kickoff, agent_team in supported:
            with self.subTest(pair=(kickoff, agent_team)):
                handoff = valid_handoff(self.root)
                handoff["projectKickoff"]["version"] = kickoff
                handoff["agentTeam"]["testedVersion"] = agent_team
                result = self.check(handoff)
                self.assertEqual(result.returncode, 0, result.stderr)
        for kickoff, agent_team in [("0.3.1", "7.2.0"), ("0.4.1", "7.0.2"), ("0.4.2", "7.2.2"), ("0.5.0", "7.2.0")]:
            with self.subTest(unsupported=(kickoff, agent_team)):
                handoff = valid_handoff(self.root)
                handoff["projectKickoff"]["version"] = kickoff
                handoff["agentTeam"]["testedVersion"] = agent_team
                result = self.check(handoff)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"unsupported handoff compatibility {kickoff}/{agent_team}", result.stderr)
                self.assertIn("checker 0.5.0 requires an approved migration", result.stderr)

    def test_emit_request_rebinds_the_current_descendant_tip(self):
        handoff = valid_handoff(self.root)
        baseline = handoff["project"]["revision"]
        path = self.root / "AGENT_TEAM_HANDOFF.json"
        source = (json.dumps(handoff, indent=2) + "\n").encode()
        path.write_bytes(source)
        subprocess.run(["git", "-C", str(self.root), "add", path.name], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "commit handoff"], check=True)
        tip = subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True,
        ).strip()
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(path),
             "--emit-request", "--actor-session-id", "project-owner",
             "--operation-id", "initialize-project-kickoff-handoff",
             "--expected-version", "0"],
            capture_output=True, text=True, timeout=3,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.read_bytes(), source)
        emitted = json.loads(result.stdout)
        binding = emitted["request"]["handoff"]
        self.assertEqual(set(binding), {
            "schemaVersion", "path", "sha256", "generatedBy", "testedAgainst",
            "generationBaseline", "observedRevision",
        })
        self.assertEqual(binding, {
            "schemaVersion": 1,
            "path": "AGENT_TEAM_HANDOFF.json",
            "sha256": hashlib.sha256(source).hexdigest(),
            "generatedBy": {"name": "project-kickoff", "version": "0.5.0"},
            "testedAgainst": {"name": "agent-team", "version": "7.3.1"},
            "generationBaseline": baseline,
            "observedRevision": tip,
        })

    def test_emit_request_rejects_tracker_drift(self):
        row = {"id": "AT-001", "title": "Approved behavior", "status": "ready",
               "assignee": "", "dependency_count": 0, "dependencies": []}
        second = {"id": "AT-002", "title": "Second behavior", "status": "ready",
                  "assignee": "", "dependency_count": 0, "dependencies": []}
        cases = {
            "addition": ([row], [row, second]),
            "removal": ([row], []),
            "reorder": ([row, second], [second, row]),
            "status": ([row], [{**row, "status": "active"}]),
            "owner": ([row], [{**row, "assignee": "developer"}]),
            "dependencies": ([row], [{**row, "dependency_count": 1,
                                       "dependencies": [{"type": "blocks", "depends_on_id": "AT-002"}]}]),
        }
        for label, (first_rows, second_rows) in cases.items():
            with self.subTest(drift=label):
                counter = self.root / f"counter-{label}"
                executable = self.root / f"changing-bd-{label}"
                executable.write_text(
                    "#!/usr/bin/env python3\n"
                    "import json\n"
                    "from pathlib import Path\n"
                    f"counter = Path({str(counter)!r})\n"
                    "count = int(counter.read_text()) if counter.exists() else 0\n"
                    "counter.write_text(str(count + 1))\n"
                    f"first = json.loads({json.dumps(first_rows)!r})\n"
                    f"second = json.loads({json.dumps(second_rows)!r})\n"
                    "print(json.dumps(first if count == 0 else second))\n"
                )
                executable.chmod(0o700)
                handoff = valid_handoff(self.root)
                handoff["tracker"] = {"kind": "beads", "executable": str(executable)}
                handoff["plan"]["tasks"] = [{"id": item["id"]} for item in first_rows]
                path = self.root / "AGENT_TEAM_HANDOFF.json"
                source = json.dumps(handoff).encode()
                path.write_bytes(source)
                result = subprocess.run(
                    [sys.executable, str(CHECKER), "--handoff", str(path),
                     "--emit-request", "--actor-session-id", "project-owner",
                     "--operation-id", "initialize-project-kickoff-handoff",
                     "--expected-version", "0"],
                    capture_output=True, text=True, timeout=3,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("tracker changed after handoff validation", result.stderr)
                self.assertEqual(path.read_bytes(), source)

    def test_checker_rejects_symlink_handoff_and_tracker(self):
        handoff = valid_handoff(self.root)
        target = self.root / "handoff-target.json"
        target.write_text(json.dumps(handoff))
        link = self.root / "AGENT_TEAM_HANDOFF.json"
        link.symlink_to(target)
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(link)],
            capture_output=True, text=True, timeout=3,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

        link.unlink()
        tracker = self.root / "TASKS.md"
        tracker_source = tracker.read_bytes()
        tracker.unlink()
        tracker_target = self.root / "tracker-target.md"
        tracker_target.write_bytes(tracker_source)
        tracker.symlink_to(tracker_target)
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("regular non-symlink", result.stderr)

    def test_checker_rejects_a_symlink_alias_as_the_selected_git_root(self):
        alias = Path(self.temp.name) / "project-alias"
        alias.symlink_to(self.root, target_is_directory=True)
        handoff = valid_handoff(self.root)
        handoff["project"]["root"] = str(alias)
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("project.root must be the selected Git root", result.stderr)

    def test_checker_rejects_wrong_branch_and_detached_head(self):
        wrong = valid_handoff(self.root)
        wrong["project"]["branch"] = "other"
        wrong["plan"]["branch"] = "other"
        result = self.check(wrong)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("project.branch must be checked out", result.stderr)

        handoff = valid_handoff(self.root)
        subprocess.run(["git", "-C", str(self.root), "checkout", "-q", "--detach"], check=True)
        result = self.check(handoff)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("project.branch must be checked out", result.stderr)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO unavailable on this platform")
    def test_checker_rejects_a_special_handoff_without_blocking(self):
        fifo = self.root / "AGENT_TEAM_HANDOFF.json"
        os.mkfifo(fifo)
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(fifo)],
            capture_output=True, text=True, timeout=3,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("regular non-symlink", result.stderr)

    def test_emit_request_rejects_out_of_root_handoff_without_traceback(self):
        handoff = valid_handoff(self.root)
        outside = Path(self.temp.name) / "outside.json"
        source = json.dumps(handoff).encode()
        outside.write_bytes(source)
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(outside),
             "--emit-request", "--actor-session-id", "project-owner",
             "--operation-id", "initialize-project-kickoff-handoff",
             "--expected-version", "0"], capture_output=True, text=True, timeout=3,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("handoff path must be within project.root", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(outside.read_bytes(), source)

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

    def test_beads_response_can_exceed_the_old_1_mib_limit(self):
        task_ids = [f"AT-{index:04d}" for index in range(1, 1001)]
        rows = [{
            "id": task_id,
            "title": "x" * 1100,
            "status": "ready",
            "assignee": "",
            "dependency_count": 0,
            "dependencies": [],
        } for task_id in task_ids]
        executable = self.root / "large-bd"
        executable.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            f"print(json.loads({json.dumps(json.dumps(rows))!r}))\n"
        )
        executable.chmod(0o700)
        handoff = valid_handoff(self.root)
        handoff["tracker"] = {"kind": "beads", "executable": str(executable)}
        handoff["plan"]["tasks"] = [{"id": task_id} for task_id in task_ids]
        result = self.check(handoff)
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.environ.get("AGENT_TEAM_ROOT"),
                         "set AGENT_TEAM_ROOT for preliminary Agent-Team qualification")
    def test_preliminary_local_agent_team_731_consumes_the_050_handoff(self):
        agent_team = Path(os.environ["AGENT_TEAM_ROOT"]).resolve()
        version = (agent_team / "SKILL.md").read_text()
        self.assertIn('version: "7.3.1"', version)
        expected_revision = os.environ.get("AGENT_TEAM_EXPECTED_REVISION")
        if expected_revision:
            observed_revision = subprocess.check_output(
                ["git", "-C", str(agent_team), "rev-parse", "HEAD"], text=True,
            ).strip()
            self.assertEqual(observed_revision, expected_revision)

        task_ids = [f"AT-{index:04d}" for index in range(1, 1001)]
        rows = "".join(
            f"| {task_id} | Approved behavior | unassigned | none | ready | none | Implement the plan. |\n"
            for task_id in task_ids
        )
        (self.root / "README.md").write_text("Fixture project.\n")
        (self.root / "TASKS.md").write_text(
            "# Agent-Team Tasks\n\n"
            "| ID | Requirement / acceptance | Owner | Depends on | Status | Revision / evidence | Next action |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            + rows
        )
        subprocess.run(["git", "-C", str(self.root), "add", "README.md", "TASKS.md"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture project"], check=True)

        handoff = valid_handoff(self.root)
        handoff["plan"]["tasks"] = [{"id": task_id} for task_id in task_ids]
        self.assertEqual(handoff["plan"]["requiredCapabilities"], ["graphify"])
        handoff_path = self.root / "AGENT_TEAM_HANDOFF.json"
        handoff_source = (json.dumps(handoff, indent=2) + "\n").encode()
        handoff_path.write_bytes(handoff_source)
        subprocess.run(["git", "-C", str(self.root), "add", handoff_path.name], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture handoff"], check=True)
        observed_tip = subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True,
        ).strip()
        emitted = subprocess.run(
            [sys.executable, str(CHECKER), "--handoff", str(handoff_path),
             "--emit-request", "--actor-session-id", "project-owner",
             "--operation-id", "initialize-project-kickoff-handoff",
             "--expected-version", "0"], capture_output=True, text=True, timeout=3,
        )
        self.assertEqual(emitted.returncode, 0, emitted.stderr)
        envelope = json.loads(emitted.stdout)
        provenance = envelope["request"]["handoff"]
        self.assertEqual(provenance["generationBaseline"], handoff["project"]["revision"])
        self.assertEqual(provenance["observedRevision"], observed_tip)
        self.assertEqual(provenance["sha256"], hashlib.sha256(handoff_source).hexdigest())
        self.assertEqual(envelope["request"]["plan"]["requiredCapabilities"], ["graphify"])
        self.assertEqual(handoff_path.read_bytes(), handoff_source)
        request = self.root / "initialization.json"
        request.write_text(json.dumps(envelope))
        cli = agent_team / "hooks/agent-team-cli.mjs"
        before_shell = {
            item.relative_to(self.root).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
            for item in self.root.rglob("*") if item.is_file() and ".git" not in item.parts
        }
        result = subprocess.run(
            ["node", str(cli), "project-initialize", "--project", str(self.root),
             "--request", str(request)], capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        shell = json.loads(result.stdout)
        self.assertEqual(shell["status"], "validated")
        self.assertEqual(shell["reason"], "native_identity_required")
        after_shell = {
            item.relative_to(self.root).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
            for item in self.root.rglob("*") if item.is_file() and ".git" not in item.parts
        }
        self.assertEqual(after_shell, before_shell)

        driver = self.root / "consume.mjs"
        driver.write_text(
            "import { initializeProject } from "
            f"{json.dumps((agent_team / 'hooks/lib/initialization.mjs').as_uri())};\n"
            "import { readFile } from 'node:fs/promises';\n"
            "const root = process.argv[2];\n"
            "const envelope = JSON.parse(await readFile(process.argv[3], 'utf8'));\n"
            "const result = await initializeProject(root, envelope.request, {"
            "actorSessionId: envelope.actorSessionId, expectedVersion: envelope.expectedVersion, "
            "nativeIdentity: {host:'codex',sessionId:envelope.actorSessionId,observed:true,cwd:root}});\n"
            "process.stdout.write(JSON.stringify(result));\n"
        )
        consumed = subprocess.run(
            ["node", str(driver), str(self.root), str(request)],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(consumed.returncode, 0, consumed.stderr)
        initialized = json.loads(consumed.stdout)
        self.assertEqual(initialized["status"], "applied", initialized)
        self.assertTrue(initialized["ready"])
        self.assertEqual(initialized["taskIds"], task_ids)
        setup = json.loads((self.root / ".agent-team/setup.json").read_text())
        self.assertEqual(setup["ownership"]["current"]["host"], "codex")
        self.assertEqual(setup["ownership"]["current"]["sessionId"], "project-owner")
        self.assertEqual(setup["plan"]["requiredCapabilities"], ["graphify"])
        self.assertEqual(setup["initialization"]["initialTaskIds"], task_ids)
        tracker_source = (self.root / "TASKS.md").read_bytes()
        tracker_id = f"markdown:{self.root / 'TASKS.md'}".encode()
        self.assertEqual(
            setup["initialization"]["trackerFingerprint"],
            hashlib.sha256(tracker_id + b"\0" + tracker_source).hexdigest(),
        )
        consumed_handoff = setup["initialization"]["handoff"]
        for key, value in provenance.items():
            self.assertEqual(consumed_handoff[key], value)
        self.assertEqual(consumed_handoff["consumptionOperationId"], envelope["request"]["operationId"])
        self.assertFalse((self.root / "graphify-out").exists())
        self.assertFalse((self.root / ".agent-team/tools").exists())
        self.assertEqual(handoff_path.read_bytes(), handoff_source)


if __name__ == "__main__":
    unittest.main()
