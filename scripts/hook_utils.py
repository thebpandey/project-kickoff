"""Shared bounded input and path handling for Project Kickoff hooks."""
import json
import os
from pathlib import Path

from load_context import read_record


INPUT_LIMIT = 65536
SETTINGS_LIMIT = 16384
SETTINGS_PATH = ".project-kickoff/hooks.json"
MAX_PATHS = 128
RESERVED_PATHS = {SETTINGS_PATH, ".project-kickoff/context-hook.json"}
SHARED_RECORDS = {
    "CONTEXT.md", "MISTAKES.md", "TASKS.md",
    ".agent-team/TASKS.md", ".agent-team/TEAMS.md",
}
SUPPORTED_TOOLS = {"Write", "Edit", "apply_patch"}


class HookInputError(ValueError):
    """The active hook received data outside its documented contract."""


def command_args(argv):
    if (len(argv) != 5 or argv[1] != "--project-root" or argv[3] != "--host"
            or argv[4] not in {"codex", "claude"}):
        raise HookInputError("supply --project-root ABSOLUTE_PATH --host codex|claude")
    supplied = Path(argv[2])
    if not supplied.is_absolute():
        raise HookInputError("project root must be absolute")
    try:
        root = supplied.resolve(strict=True)
    except OSError as error:
        raise HookInputError("project root is unavailable") from error
    if not root.is_dir():
        raise HookInputError("project root is not a directory")
    return root, argv[4]


def load_settings(root):
    """Return validated settings, or None when the project did not opt in."""
    try:
        settings = json.loads(read_record(root, SETTINGS_PATH, SETTINGS_LIMIT))
    except FileNotFoundError:
        return None
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        raise HookInputError("hook settings are unreadable or malformed") from error
    try:
        configured_root = Path(settings["project_root"])
        guard = settings["edit_guard"]
        checkpoint = settings["checkpoint_advisory"]
        approved = guard["approved_paths"]
        valid = (
            isinstance(settings, dict)
            and settings.get("version") == 1
            and configured_root.is_absolute()
            and configured_root.resolve(strict=True) == root
            and isinstance(guard, dict)
            and isinstance(guard.get("enabled"), bool)
            and isinstance(approved, list)
            and len(approved) <= 64
            and isinstance(checkpoint, dict)
            and isinstance(checkpoint.get("enabled"), bool)
        )
    except (KeyError, TypeError, OSError):
        valid = False
    if not valid:
        raise HookInputError("hook settings do not match version 1 or this project root")
    normalized = []
    for item in approved:
        if (not isinstance(item, str) or not item or len(item) > 512
                or "\0" in item or Path(item).is_absolute()):
            raise HookInputError("approved paths must be short relative file paths")
        path = Path(os.path.normpath(item))
        if path == Path(".") or ".." in path.parts:
            raise HookInputError("approved paths must stay inside the project")
        normalized.append(path.as_posix())
    settings["edit_guard"]["approved_paths"] = frozenset(normalized)
    return settings


def read_event(stream):
    raw = stream.buffer.read(INPUT_LIMIT + 1)
    if len(raw) > INPUT_LIMIT:
        raise HookInputError("event input is oversized")
    try:
        event = json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise HookInputError("event input is malformed") from error
    if not isinstance(event, dict):
        raise HookInputError("event input is malformed")
    return event


def edit_paths(event, event_name):
    """Return documented edit paths, None for an unrelated event or tool."""
    if event.get("hook_event_name") != event_name:
        return None
    tool = event.get("tool_name")
    if not isinstance(tool, str):
        raise HookInputError("event tool_name is malformed")
    if tool not in SUPPORTED_TOOLS:
        return None
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        raise HookInputError("supported edit payload is malformed")
    if tool in {"Write", "Edit"}:
        path = tool_input.get("file_path")
        if not isinstance(path, str) or not path or len(path) > 4096 or "\0" in path:
            raise HookInputError("supported edit payload is malformed")
        return [path]
    command = tool_input.get("command")
    if not isinstance(command, str) or len(command.encode("utf-8")) > INPUT_LIMIT:
        raise HookInputError("supported patch payload is malformed")
    return patch_paths(command)


def patch_paths(command):
    lines = command.splitlines()
    if not lines or lines[0].strip() != "*** Begin Patch":
        raise HookInputError("supported patch payload is malformed")
    prefixes = (
        "*** Add File: ", "*** Delete File: ", "*** Update File: ",
        "*** Move to: ",
    )
    paths = []
    state = "started"
    for line in lines[1:]:
        header = line.rstrip() if state == "update" else line.strip()
        if state == "ended":
            if line.strip():
                raise HookInputError("supported patch payload is malformed")
            continue
        if header == "*** End Patch":
            state = "ended"
            continue
        if state == "started" and header.startswith("*** Environment ID:"):
            raise HookInputError("apply_patch environment targets are unsupported")
        matched = False
        for prefix in prefixes:
            if header.startswith(prefix):
                path = header[len(prefix):]
                if not path or len(path) > 4096 or "\0" in path:
                    raise HookInputError("supported patch payload is malformed")
                paths.append(path)
                state = "update" if prefix in {"*** Update File: ", "*** Move to: "} else prefix.split()[1].casefold()
                matched = True
                break
        if matched:
            continue
    if state != "ended" or not paths or len(paths) > MAX_PATHS:
        raise HookInputError("supported patch payload is malformed")
    return paths


def _valid_git_marker(marker):
    if marker.is_dir():
        return (marker / "HEAD").is_file()
    if not marker.is_file():
        return False
    try:
        with marker.open("rb") as stream:
            data = stream.read(4097)
        if len(data) > 4096:
            return False
        line = data.decode("utf-8").strip()
        target = line.removeprefix("gitdir: ")
        if target == line:
            return False
        gitdir = Path(target)
        if not gitdir.is_absolute():
            gitdir = marker.parent / gitdir
        return gitdir.resolve(strict=True).is_dir()
    except (OSError, UnicodeError):
        return False


def require_canonical_checkout(root):
    if not _valid_git_marker(root / ".git"):
        raise HookInputError("configured project root is not a real canonical Git checkout")


def _checkout_root(path):
    current = path if path.is_dir() else path.parent
    while not current.exists() and current != current.parent:
        current = current.parent
    for directory in (current, *current.parents):
        if _valid_git_marker(directory / ".git"):
            return directory.resolve(strict=False)
    return None


def canonical_relatives(raw_path, cwd, root):
    """Return every canonical relative destination, including symlink aliases."""
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        raise HookInputError("event cwd is missing or not absolute")
    path = Path(raw_path)
    combined = path if path.is_absolute() else Path(cwd) / path
    lexical = Path(os.path.normpath(str(combined)))
    candidates = [lexical]
    try:
        resolved = combined.resolve(strict=False)
    except OSError:
        resolved = lexical
    if resolved != lexical:
        candidates.append(resolved)
    relatives = set()
    for candidate in candidates:
        if _checkout_root(candidate) != root:
            continue
        try:
            relatives.add(candidate.relative_to(root).as_posix())
        except ValueError:
            continue
    return frozenset(relatives)
