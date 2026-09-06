#!/usr/bin/env python3
"""Guard supported direct edits to an opted-in canonical checkout."""
import json
import sys

from hook_utils import (
    HookInputError, RESERVED_PATHS, SHARED_RECORDS, canonical_relatives,
    command_args, edit_paths, load_settings, read_event,
    require_canonical_checkout,
)


def deny(reason):
    reason = "Project Kickoff edit guard: " + reason
    while True:
        output = {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}
        serialized = json.dumps(output, ensure_ascii=False)
        if len(serialized.encode("utf-8")) <= 8192:
            print(serialized)
            return
        reason = reason[:len(reason) // 2] + "…"


def main():
    try:
        root, host = command_args(sys.argv)
        settings = load_settings(root)
    except HookInputError as error:
        deny(str(error) + "; review hook settings before editing.")
        return
    if settings is None or settings["edit_guard"]["enabled"] is not True:
        return
    try:
        require_canonical_checkout(root)
        event = read_event(sys.stdin)
        paths = edit_paths(event, "PreToolUse")
    except HookInputError as error:
        deny(str(error) + "; use a documented Write, Edit, or apply_patch payload.")
        return
    if paths is None:
        return
    blocked = []
    for raw_path in paths:
        try:
            relatives = canonical_relatives(raw_path, event.get("cwd"), root)
        except HookInputError as error:
            deny(str(error) + "; use an absolute event cwd.")
            return
        for relative in relatives:
            if relative in RESERVED_PATHS:
                deny(relative + " is hook configuration (settings or marker); use the documented manual maintenance flow.")
                return
            if (host == "claude" and isinstance(event.get("agent_id"), str)
                    and event["agent_id"] and relative in SHARED_RECORDS):
                deny(relative + " is a canonical shared record; submit the update to the project orchestrator.")
                return
            if relative not in settings["edit_guard"]["approved_paths"]:
                blocked.append(relative)
    if blocked:
        names = ", ".join(name[:240] for name in sorted(set(blocked))[:8])
        deny(names + " is not an approved planning path; edit it in an approved task worktree.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError):
        deny("unexpected input or filesystem state; review the hook and use a task worktree.")
