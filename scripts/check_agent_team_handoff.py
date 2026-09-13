#!/usr/bin/env python3
"""Check the bounded Project Kickoff handoff consumed by Agent-Team."""

import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


MAX_HANDOFF_BYTES = 250 * 1024
MAX_REQUEST_BYTES = 256 * 1024
MAX_TASKS = 500
MAX_LIST_ITEMS = 100
CHECKER_VERSION = "0.4.2"
SUPPORTED_PAIRS = frozenset({
    ("0.3.1", "7.0.2"),
    ("0.4.0", "7.0.2"),
    ("0.4.1", "7.1.0"),
    ("0.4.1", "7.2.0"),
    ("0.4.1", "7.2.1"),
    ("0.4.2", "7.2.3"),
    ("0.4.2", "7.2.4"),
})
ID_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
RESERVED_IDS = {"none", "unknown", "unassigned", "-"}
READY = {"ready", "open", "todo", "pending"}
FINISHED = {"verified", "integrated", "deployed", "closed", "done"}
KNOWN_STATUSES = READY | FINISHED | {
    "active", "approved deferred", "approved_deferred", "blocked", "canceled", "cancelled", "complete",
    "completed", "deferred", "in_progress", "paused", "parked", "working",
}
UNCLAIMED = {"", "none", "unassigned", "-"}


def is_object(value):
    return isinstance(value, dict)


def text(value, maximum):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= maximum and "\0" not in value


def string_list(value, *, allow_empty=False, maximum=4096):
    return (isinstance(value, list) and (allow_empty or bool(value))
            and len(value) <= MAX_LIST_ITEMS
            and all(text(item, maximum) for item in value))


def valid_id(value):
    return (isinstance(value, str) and bool(ID_PATTERN.fullmatch(value))
            and value.lower() not in RESERVED_IDS)


def safe_relative(value):
    if not text(value, 256) or os.path.isabs(value) or any(part == ".." for part in re.split(r"[\\/]", value)):
        return False
    return not any(character in value for character in ("\r", "\n", "|"))


def split_dependencies(value):
    return [item for item in re.split(r"\s*,\s*", str(value or ""))
            if item and item.lower() not in {"none", "-"}]


def compatibility_pair(project_kickoff_version, agent_team_version):
    pair = (project_kickoff_version, agent_team_version)
    if pair not in SUPPORTED_PAIRS:
        raise ValueError(
            f"unsupported handoff compatibility {project_kickoff_version}/{agent_team_version}; "
            f"checker {CHECKER_VERSION} requires an approved migration"
        )
    return pair


def stable_regular_bytes(path, maximum, label):
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise ValueError(f"{label} must be a regular non-symlink file") from error
        raise
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"{label} must be a regular non-symlink file")
        if before.st_size > maximum:
            raise ValueError(f"{label} exceeds {maximum} bytes")
        source = b""
        while len(source) <= maximum:
            chunk = os.read(descriptor, min(65536, maximum + 1 - len(source)))
            if not chunk:
                break
            source += chunk
        after = os.fstat(descriptor)
        identity = (before.st_dev, before.st_ino, before.st_size,
                    before.st_mtime_ns, before.st_ctime_ns)
        if identity != (after.st_dev, after.st_ino, after.st_size,
                        after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError(f"{label} changed while being read")
        if len(source) > maximum:
            raise ValueError(f"{label} exceeds {maximum} bytes")
        return source, identity
    finally:
        os.close(descriptor)


def git(root, *arguments):
    return subprocess.run(
        ["git", "-C", root, *arguments],
        capture_output=True, text=True, timeout=3,
    )


def git_boundary(root, branch, approved_revision, integration_revision):
    top = git(root, "rev-parse", "--show-toplevel")
    canonical_root = os.path.realpath(root)
    if (top.returncode != 0 or canonical_root != os.path.abspath(root)
            or top.stdout.strip() != canonical_root):
        return "project.root must be the selected Git root", None
    current = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if current.returncode != 0 or current.stdout.strip() != branch:
        return "project.branch must be checked out in the selected Git root", None
    branch_ref = git(root, "rev-parse", "--verify", f"refs/heads/{branch}^{{commit}}")
    if branch_ref.returncode != 0:
        return "integration branch does not exist", None
    observed_revision = branch_ref.stdout.strip()
    approved = git(root, "rev-parse", "--verify", f"{approved_revision}^{{commit}}")
    baseline = git(root, "rev-parse", "--verify", f"{integration_revision}^{{commit}}")
    if approved.returncode != 0 or approved.stdout.strip() != approved_revision:
        return "approved revision is not an ancestor of the generation baseline", None
    if baseline.returncode != 0 or baseline.stdout.strip() != integration_revision:
        return "generation baseline is not an ancestor of the observed branch tip", None
    ancestor = git(root, "merge-base", "--is-ancestor", approved_revision, integration_revision)
    if ancestor.returncode != 0:
        return "approved revision is not an ancestor of the generation baseline", None
    descendant = git(root, "merge-base", "--is-ancestor", integration_revision, observed_revision)
    if descendant.returncode != 0:
        return "generation baseline is not an ancestor of the observed branch tip", None
    return None, observed_revision


def markdown_tracker_snapshot(path):
    encoded, identity = stable_regular_bytes(path, 1024 * 1024, "selected Markdown tracker")
    source = encoded.decode("utf-8")
    lines = source.splitlines()
    task_rows = []
    index = 0
    while index < len(lines) - 1:
        if (not re.match(r"^\s*\|", lines[index])
                or not re.match(r"^\s*\|(?:\s*:?-+:?\s*\|)+\s*$", lines[index + 1])):
            index += 1
            continue
        headers = [cell.strip().lower() for cell in lines[index].strip().strip("|").split("|")]
        index += 2
        rows = []
        while index < len(lines) and re.match(r"^\s*\|", lines[index]):
            cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
            rows.append(dict(zip(headers, cells)))
            index += 1
        if "id" in headers:
            if "owner" not in headers or "status" not in headers or len(set(headers)) != len(headers):
                raise ValueError("selected Markdown tracker has an invalid task table")
            task_rows.extend(rows)
    if not task_rows:
        raise ValueError("selected Markdown tracker has no task table")
    if (any(not row.get("id") or not row.get("owner") or not row.get("status") for row in task_rows)
            or len({row["id"] for row in task_rows}) != len(task_rows)):
        raise ValueError("selected Markdown tracker has invalid or duplicate task rows")
    rows = [{"id": row["id"], "status": row["status"], "owner": row["owner"],
             "dependencies": split_dependencies(row.get("depends on"))}
            for row in task_rows]
    return rows, {
        "kind": "markdown", "path": str(path), "sha256": hashlib.sha256(encoded).hexdigest(),
        "identity": identity,
    }


def markdown_tracker(path):
    return markdown_tracker_snapshot(path)[0]


def beads_tracker_snapshot(root, executable):
    environment = os.environ.copy()
    routing = [
        "DB", "DOLT_DATA_DIR", "DOLT_DATABASE", "DOLT_SERVER_DATABASE", "DOLT_HOST",
        "DOLT_PORT", "DOLT_SERVER_HOST", "DOLT_SERVER_PORT", "DOLT_SERVER_SOCKET",
        "DOLT_SHARED_SERVER", "DOLT_SERVER_MODE", "SHARED_SERVER_DIR", "ROUTING_MODE",
        "ROUTING_DEFAULT", "ROUTING_MAINTAINER", "ROUTING_CONTRIBUTOR",
    ]
    for name in routing:
        for prefix in ("BEADS_", "BD_"):
            environment.pop(f"{prefix}{name}", None)
    for name in ("GT_DOLT_DATA", "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE"):
        environment.pop(name, None)
    environment["BEADS_DIR"] = str(Path(root) / ".beads")
    environment["PWD"] = root
    result = subprocess.run(
        [executable, "list", "--all", "--limit", "0", "--json", "--readonly"],
        cwd=root, env=environment, capture_output=True, text=True, timeout=5,
    )
    if result.returncode != 0:
        raise ValueError("selected Beads tracker read failed")
    if len(result.stdout.encode("utf-8")) > 1024 * 1024:
        raise ValueError("selected Beads response exceeds 1 MiB")
    rows = json.loads(result.stdout)
    if (not isinstance(rows, list)
            or any(not is_object(row) or not text(row.get("id"), 128)
                   or not text(row.get("status"), 128) or not text(row.get("title"), 4096)
                   or (row.get("assignee") is not None and not isinstance(row["assignee"], str))
                   for row in rows)
            or len({row["id"] for row in rows}) != len(rows)):
        raise ValueError("selected Beads tracker returned invalid rows")
    normalized = [{
        "id": row["id"],
        "status": row["status"],
        "owner": row.get("assignee") or "",
        "dependencies": [dependency["depends_on_id"] for dependency in row.get("dependencies", [])
                         if is_object(dependency) and dependency.get("type") == "blocks"
                         and isinstance(dependency.get("depends_on_id"), str)],
        "dependencyEvidence": (row.get("dependency_count") == 0
                               or isinstance(row.get("dependencies"), list)
                               and all(is_object(dependency)
                                       and isinstance(dependency.get("depends_on_id"), str)
                                       and dependency.get("type") in {"blocks", "parent-child", "related"}
                                       for dependency in row["dependencies"])),
    } for row in rows]
    return normalized, {
        "kind": "beads", "root": root, "executable": executable,
        "sha256": hashlib.sha256(
            json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }


def beads_tracker(root, executable):
    return beads_tracker_snapshot(root, executable)[0]


def validate_handoff(value, *, size=None, details=None):
    errors = []
    if size is not None and size > MAX_HANDOFF_BYTES:
        errors.append(f"handoff exceeds {MAX_HANDOFF_BYTES} bytes")
    if not is_object(value):
        return errors + ["handoff must be a JSON object"]
    if value.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if value.get("kind") != "project-kickoff-agent-team-handoff":
        errors.append("kind must identify the Project Kickoff Agent-Team handoff")
    if value.get("status") != "approved":
        errors.append("status must be approved")

    kickoff = value.get("projectKickoff")
    if not is_object(kickoff):
        errors.append("projectKickoff must be an object")
    else:
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(kickoff.get("version", ""))):
            errors.append("projectKickoff.version must be semantic")
        if not valid_id(kickoff.get("approvalId")):
            errors.append("projectKickoff.approvalId is invalid")
        if not re.fullmatch(r"[0-9a-f]{40}", str(kickoff.get("approvedRevision", ""))):
            errors.append("projectKickoff.approvedRevision must be a full Git revision")

    agent_team = value.get("agentTeam")
    if not is_object(agent_team):
        errors.append("agentTeam must be an object")
    else:
        kickoff_version = kickoff.get("version") if is_object(kickoff) else None
        tested_version = agent_team.get("testedVersion")
        if (re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(kickoff_version or ""))
                and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(tested_version or ""))):
            try:
                compatibility_pair(kickoff_version, tested_version)
            except ValueError as error:
                errors.append(str(error))
        elif not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(tested_version or "")):
            errors.append("agentTeam.testedVersion must be semantic")
        if agent_team.get("initializationSource") != "existing":
            errors.append("agentTeam.initializationSource must be existing")

    project = value.get("project")
    if not is_object(project):
        errors.append("project must be an object")
        project = {}
    else:
        if not valid_id(project.get("id")):
            errors.append("project.id is invalid")
        if not text(project.get("root"), 4096) or not os.path.isabs(project["root"]):
            errors.append("project.root must be absolute")
        if not text(project.get("branch"), 256):
            errors.append("project.branch is invalid")
        if not re.fullmatch(r"[0-9a-f]{40}", str(project.get("revision", ""))):
            errors.append("project.revision must be a full Git revision")

    tracker = value.get("tracker")
    if not is_object(tracker):
        errors.append("tracker must be an object")
    elif tracker.get("kind") == "markdown":
        if tracker.get("path") not in {"TASKS.md", ".agent-team/TASKS.md"}:
            errors.append("unsupported tracker: markdown path must be TASKS.md or .agent-team/TASKS.md")
    elif tracker.get("kind") == "beads":
        executable = tracker.get("executable")
        if not text(executable, 4096) or not os.path.isabs(executable):
            errors.append("unsupported tracker: Beads executable must be absolute")
    else:
        errors.append("unsupported tracker: supported Agent-Team contracts accept only Beads or Markdown")

    plan = value.get("plan")
    if not is_object(plan):
        return errors + ["plan must be an object"]
    if not text(plan.get("scope"), 4096):
        errors.append("plan.scope is invalid")
    for field in ("acceptance", "verification"):
        if not string_list(plan.get(field)):
            errors.append(f"plan.{field} must contain 1 to 100 nonempty strings")
    if not text(plan.get("branch"), 256):
        errors.append("plan.branch is invalid")
    elif plan.get("branch") != project.get("branch"):
        errors.append("plan.branch must match project.branch")
    if "requiredCapabilities" in plan:
        required_capabilities = plan["requiredCapabilities"]
        if not isinstance(required_capabilities, list):
            errors.append("plan.requiredCapabilities must be a bounded unique list of safe capability IDs")
        elif len(required_capabilities) > MAX_LIST_ITEMS:
            errors.append(f"{len(required_capabilities)} required capabilities exceeds Agent-Team limit of {MAX_LIST_ITEMS}")
        elif any(not valid_id(capability) for capability in required_capabilities):
            errors.append("invalid required capability ID")
        elif len(set(required_capabilities)) != len(required_capabilities):
            errors.append("duplicate required capability ID")

    if (is_object(kickoff) and re.fullmatch(r"[0-9a-f]{40}", str(kickoff.get("approvedRevision", "")))
            and text(project.get("root"), 4096) and text(project.get("branch"), 256)
            and re.fullmatch(r"[0-9a-f]{40}", str(project.get("revision", "")))
            and os.path.isabs(project["root"])):
        try:
            git_error, observed_revision = git_boundary(
                project["root"], project["branch"], kickoff["approvedRevision"],
                project["revision"],
            )
            if git_error:
                errors.append(git_error)
            elif details is not None:
                details["observedRevision"] = observed_revision
        except (OSError, subprocess.SubprocessError) as error:
            errors.append(f"Git validation failed: {error}")

    authority = plan.get("authority")
    if not is_object(authority):
        errors.append("plan.authority must be an object")
    else:
        owned = authority.get("ownedPaths")
        if not string_list(owned, maximum=256):
            errors.append("plan.authority.ownedPaths must contain 1 to 100 paths")
        elif any(not safe_relative(path) for path in owned):
            errors.append("unsafe owned path")
        external = authority.get("externalActions", [])
        if not string_list(external, allow_empty=True):
            errors.append("plan.authority.externalActions must be a bounded string list")

    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return errors + ["plan.tasks must contain at least one task"]
    if len(tasks) > MAX_TASKS:
        errors.append(f"{len(tasks)} tasks exceeds Agent-Team limit of {MAX_TASKS}")
    ids = [task.get("id") if is_object(task) else None for task in tasks]
    if any(not is_object(task) or set(task) != {"id"} for task in tasks):
        errors.append("handoff tasks must contain only id; the selected tracker owns task content")
    if any(not valid_id(task_id) for task_id in ids):
        errors.append("invalid task ID")
    if len(set(ids)) != len(ids):
        errors.append("duplicate task ID")
    id_set = set(ids)
    tracker_rows = None
    tracker_identity = None
    try:
        if is_object(tracker) and is_object(project) and text(project.get("root"), 4096):
            if tracker.get("kind") == "markdown" and tracker.get("path") in {"TASKS.md", ".agent-team/TASKS.md"}:
                tracker_rows, tracker_identity = markdown_tracker_snapshot(
                    Path(project["root"]) / tracker["path"]
                )
            elif tracker.get("kind") == "beads" and text(tracker.get("executable"), 4096):
                tracker_rows, tracker_identity = beads_tracker_snapshot(
                    project["root"], tracker["executable"]
                )
    except (OSError, UnicodeError, json.JSONDecodeError, subprocess.SubprocessError, ValueError) as error:
        errors.append(f"tracker validation failed: {error}")
    if tracker_rows is not None:
        if details is not None:
            details["trackerRows"] = tracker_rows
            details["trackerIdentity"] = tracker_identity
        tracker_by_id = {row["id"]: row for row in tracker_rows}
        if [row["id"] for row in tracker_rows] != ids:
            errors.append("tracker task IDs do not exactly match handoff task IDs")
        else:
            graph = {}
            for row in tracker_rows:
                if row["status"] not in KNOWN_STATUSES:
                    errors.append(f"status {row['status']} is not compatible with the selected Agent-Team contract")
                dependencies = row["dependencies"]
                if (len(set(dependencies)) != len(dependencies)
                        or any(dependency not in id_set or dependency == row["id"]
                               for dependency in dependencies)):
                    errors.append(f"tracker task {row['id']} dependencies are invalid")
                    graph[row["id"]] = []
                else:
                    graph[row["id"]] = dependencies

            visiting = set()
            visited = set()

            def cycle(task_id):
                if task_id in visiting:
                    return True
                if task_id in visited:
                    return False
                visiting.add(task_id)
                found = any(cycle(dependency) for dependency in graph.get(task_id, []))
                visiting.remove(task_id)
                visited.add(task_id)
                return found

            if any(cycle(task_id) for task_id in graph):
                errors.append("task dependency cycle")
            tracker_actionable = [row for row in tracker_rows if row["status"] in READY
                                  and row["owner"].lower() in UNCLAIMED
                                  and row.get("dependencyEvidence", True)
                                  and all(tracker_by_id.get(dependency, {}).get("status") in FINISHED
                                          for dependency in row["dependencies"])]
            if not tracker_actionable and "handoff has no actionable Agent-Team task" not in errors:
                errors.append("handoff has no actionable Agent-Team task")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", required=True)
    parser.add_argument("--emit-request", action="store_true",
                        help="emit a direct Agent-Team project-initialize request")
    parser.add_argument("--actor-session-id")
    parser.add_argument("--operation-id")
    parser.add_argument("--expected-version", type=int)
    args = parser.parse_args()
    handoff = Path(args.handoff)
    try:
        source, _ = stable_regular_bytes(handoff, MAX_HANDOFF_BYTES, "handoff")
        value = json.loads(source.decode("utf-8"))
        details = {}
        errors = validate_handoff(value, size=len(source), details=details)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        errors = [str(error)]
        value = {}
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.emit_request:
        runtime_errors = []
        if not valid_id(args.actor_session_id):
            runtime_errors.append("actor-session-id is invalid")
        if not valid_id(args.operation_id):
            runtime_errors.append("operation-id is invalid")
        if args.expected_version is None or args.expected_version < 0:
            runtime_errors.append("expected-version must be a nonnegative integer")
        if runtime_errors:
            for error in runtime_errors:
                print(error, file=sys.stderr)
            return 1
        current = {}
        current_errors = validate_handoff(value, size=len(source), details=current)
        if (current.get("trackerRows") != details.get("trackerRows")
                or current.get("trackerIdentity") != details.get("trackerIdentity")):
            print("tracker changed after handoff validation", file=sys.stderr)
            return 1
        if current_errors:
            for error in current_errors:
                print(error, file=sys.stderr)
            return 1
        try:
            project_root = Path(value["project"]["root"]).resolve(strict=True)
            relative_handoff = handoff.resolve(strict=True).relative_to(project_root).as_posix()
            producer_version, tested_version = compatibility_pair(
                value["projectKickoff"]["version"], value["agentTeam"]["testedVersion"]
            )
        except (OSError, ValueError):
            print("handoff path must be within project.root", file=sys.stderr)
            return 1
        request = {
            "schemaVersion": 1,
            "actorSessionId": args.actor_session_id,
            "expectedVersion": args.expected_version,
            "request": {
                "projectId": value["project"]["id"],
                "operationId": args.operation_id,
                "source": value["agentTeam"]["initializationSource"],
                "tracker": value["tracker"],
                "plan": value["plan"],
                "handoff": {
                    "schemaVersion": 1,
                    "path": relative_handoff,
                    "sha256": hashlib.sha256(source).hexdigest(),
                    "generatedBy": {
                        "name": "project-kickoff",
                        "version": producer_version,
                    },
                    "testedAgainst": {
                        "name": "agent-team",
                        "version": tested_version,
                    },
                    "generationBaseline": value["project"]["revision"],
                    "observedRevision": current["observedRevision"],
                },
            },
        }
        serialized = json.dumps(request, ensure_ascii=False, separators=(",", ":"))
        if len(serialized.encode("utf-8")) > MAX_REQUEST_BYTES:
            print(f"emitted request exceeds {MAX_REQUEST_BYTES} bytes", file=sys.stderr)
            return 1
        print(serialized)
        return 0
    print(json.dumps({
        "status": "passed",
        "agentTeamVersion": value["agentTeam"]["testedVersion"],
        "taskCount": len(value["plan"]["tasks"]),
        "tracker": value["tracker"]["kind"],
    }, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
