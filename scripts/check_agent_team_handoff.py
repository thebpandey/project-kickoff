#!/usr/bin/env python3
"""Check the bounded Project Kickoff handoff consumed by Agent-Team 7.0.2."""

import argparse
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


def git_boundary(root, branch, approved_revision, integration_revision):
    top = subprocess.run(
        ["git", "-C", root, "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, timeout=3,
    )
    if top.returncode != 0 or os.path.realpath(top.stdout.strip()) != os.path.realpath(root):
        return "project.root must be the selected Git root"
    current = subprocess.run(
        ["git", "-C", root, "symbolic-ref", "--quiet", "--short", "HEAD"],
        capture_output=True, text=True, timeout=3,
    )
    if current.returncode != 0 or current.stdout.strip() != branch:
        return "project.branch must be checked out in the selected Git root"
    branch_ref = subprocess.run(
        ["git", "-C", root, "show-ref", "--verify", f"refs/heads/{branch}"],
        capture_output=True, text=True, timeout=3,
    )
    if branch_ref.returncode != 0:
        return "integration branch does not exist"
    if branch_ref.stdout.split()[0] != integration_revision:
        return "project.revision must match the integration branch tip"
    ancestor = subprocess.run(
        ["git", "-C", root, "merge-base", "--is-ancestor", approved_revision, branch],
        capture_output=True, text=True, timeout=3,
    )
    if ancestor.returncode != 0:
        return "approved revision is not on the integration branch"
    return None


def markdown_tracker(path):
    metadata = path.lstat()
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise ValueError("selected Markdown tracker must be a regular non-symlink file")
    if metadata.st_size > 1024 * 1024:
        raise ValueError("selected Markdown tracker exceeds 1 MiB")
    source = path.read_text(encoding="utf-8")
    if len(source.encode("utf-8")) > 1024 * 1024:
        raise ValueError("selected Markdown tracker exceeds 1 MiB")
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
    return [{"id": row["id"], "status": row["status"], "owner": row["owner"],
             "dependencies": split_dependencies(row.get("depends on"))}
            for row in task_rows]


def beads_tracker(root, executable):
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
    return [{
        "id": row["id"],
        "status": row["status"],
        "owner": row.get("assignee", ""),
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


def validate_handoff(value, *, size=None):
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
        if agent_team.get("testedVersion") != "7.0.2":
            errors.append("agentTeam.testedVersion must be 7.0.2")
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
        errors.append("unsupported tracker: Agent-Team 7.0.2 accepts only Beads or Markdown")

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

    if (is_object(kickoff) and re.fullmatch(r"[0-9a-f]{40}", str(kickoff.get("approvedRevision", "")))
            and text(project.get("root"), 4096) and text(project.get("branch"), 256)
            and re.fullmatch(r"[0-9a-f]{40}", str(project.get("revision", "")))
            and os.path.isabs(project["root"])):
        try:
            git_error = git_boundary(
                project["root"], project["branch"], kickoff["approvedRevision"],
                project["revision"],
            )
            if git_error:
                errors.append(git_error)
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
    try:
        if is_object(tracker) and is_object(project) and text(project.get("root"), 4096):
            if tracker.get("kind") == "markdown" and tracker.get("path") in {"TASKS.md", ".agent-team/TASKS.md"}:
                tracker_rows = markdown_tracker(Path(project["root"]) / tracker["path"])
            elif tracker.get("kind") == "beads" and text(tracker.get("executable"), 4096):
                tracker_rows = beads_tracker(project["root"], tracker["executable"])
    except (OSError, UnicodeError, json.JSONDecodeError, subprocess.SubprocessError, ValueError) as error:
        errors.append(f"tracker validation failed: {error}")
    if tracker_rows is not None:
        tracker_by_id = {row["id"]: row for row in tracker_rows}
        if len(tracker_rows) != len(tasks) or set(tracker_by_id) != id_set:
            errors.append("tracker task IDs do not exactly match handoff task IDs")
        else:
            graph = {}
            for row in tracker_rows:
                if row["status"] not in KNOWN_STATUSES:
                    errors.append(f"status {row['status']} is not compatible with Agent-Team 7.0.2")
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
        metadata = handoff.lstat()
        if handoff.is_symlink() or not stat.S_ISREG(metadata.st_mode):
            raise ValueError("handoff must be a regular non-symlink file")
        if metadata.st_size > MAX_HANDOFF_BYTES:
            raise ValueError(f"handoff exceeds {MAX_HANDOFF_BYTES} bytes")
        source = handoff.read_bytes()
        value = json.loads(source.decode("utf-8"))
        errors = validate_handoff(value, size=len(source))
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
