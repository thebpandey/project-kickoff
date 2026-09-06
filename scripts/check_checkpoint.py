#!/usr/bin/env python3
"""Report bounded structure diagnostics after opted-in checkpoint edits."""
import json
import sys

from hook_utils import (
    HookInputError, canonical_relatives, command_args, edit_paths, load_settings,
    read_event, require_canonical_checkout,
)
from load_context import RECORD_LIMIT, excerpt, read_record


RECORDS = {
    "CONTEXT.md": ("Phase", "Status", "Pending question", "Next action"),
    ".project-kickoff/DISCOVERY.md": (
        "Phase", "Status", "Pending question", "Next action",
    ),
}


def advise(message):
    output = {"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Project Kickoff checkpoint advisory: " + message,
    }}
    print(json.dumps(output, ensure_ascii=False))


def main():
    try:
        root, _host = command_args(sys.argv)
        settings = load_settings(root)
    except HookInputError as error:
        advise(str(error) + "; validate the checkpoint manually.")
        return
    if settings is None or settings["checkpoint_advisory"]["enabled"] is not True:
        return
    try:
        require_canonical_checkout(root)
        event = read_event(sys.stdin)
        paths = edit_paths(event, "PostToolUse")
    except HookInputError as error:
        advise(str(error) + "; validate the edited checkpoint manually.")
        return
    if paths is None:
        return
    records = set()
    for raw_path in paths:
        try:
            relatives = canonical_relatives(raw_path, event.get("cwd"), root)
        except HookInputError as error:
            advise(str(error) + "; validate the edited checkpoint manually.")
            return
        records.update(relative for relative in relatives if relative in RECORDS)
    diagnostics = []
    for relative in sorted(records):
        try:
            fields, notes = excerpt(
                read_record(root, relative, RECORD_LIMIT),
                relative == "CONTEXT.md",
            )
            missing = [name for name in RECORDS[relative] if not fields.get(name)]
            diagnostics.extend(relative + ": " + note for note in notes)
            diagnostics.extend(relative + ": missing " + name for name in missing)
        except (OSError, UnicodeError, ValueError) as error:
            reason = str(error) if isinstance(error, ValueError) and not isinstance(error, UnicodeError) else "missing or unreadable"
            diagnostics.append(relative + ": " + reason)
    if diagnostics:
        advise(" ".join(diagnostics) + ". This checks structure only; verify current meaning manually.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError):
        advise("unexpected input or filesystem state; validate the checkpoint manually.")
