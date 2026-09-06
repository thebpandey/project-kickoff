# Optional project hooks

Project Kickoff includes three optional hook actions for Codex and Claude Code:

- `SessionStart` loads a bounded saved checkpoint.
- `PreToolUse` guards supported direct edits to the canonical checkout.
- `PostToolUse` reports checkpoint structure diagnostics after supported edits.

Each action is off until the user approves it for the intended project. A Skill
installation or upgrade does not activate a hook. Hook output does not start a
kickoff, answer a question, or establish approval. Keep the normal instructions
as the fallback and verify the actual project state.

## Enable for one approved project

1. Confirm the canonical project root and the approved hook actions. Initialize
   the intended Git root before activation. The guard and advisory refuse an
   active configuration until the root is a real canonical Git checkout; do not
   claim protection for an uninitialized directory. Check that Python 3.9 or
   later is already available on Linux, macOS, or WSL. Use its
   verified absolute path. The scripts use only the standard library. If the
   runtime or host hook feature is absent, keep the instruction-based workflow.
   Do not install a runtime or change global settings as a hook side effect.
   In Codex, `codex features list` can report the local `hooks` feature state.
   Respect managed policy and do not bypass an enforced setting.
2. Read the host's existing project settings and matching hooks. Use
   [the Codex example](../assets/hooks/codex-session-start.json) or
   [the Claude Code example](../assets/hooks/claude-session-start.json).
   The examples contain all three actions. Select only the approved entries.
   Replace each placeholder with a verified absolute path. Quote each argument
   for the host shell; the examples use POSIX single quotes. Escape any
   apostrophe in an actual path.
3. For the loader, create `.project-kickoff/context-hook.json` with
   `{"enabled": true}` after checkpoint files exist. Preserve other fields in an
   existing marker. For the guard or advisory, create
   `.project-kickoff/hooks.json` before the guard starts. Use this schema:

   ```json
   {
     "version": 1,
     "project_root": "/ABSOLUTE/PROJECT/ROOT",
     "edit_guard": {
       "enabled": true,
       "approved_paths": [
         "CONTEXT.md",
         ".project-kickoff/DISCOVERY.md",
         "PRD.md",
         "DESIGN.md",
         "PLAN.md",
         "AUDIT.md"
       ]
     },
     "checkpoint_advisory": {
       "enabled": true
     }
   }
   ```

   Record only files whose canonical edits the user approved. Each entry is an
   exact POSIX-style project-relative filename. Entries do not expand globs and
   do not approve a directory. The `project_root` must resolve to the canonical
   checkout supplied to the command. Set either feature's `enabled` value to
   `false` when that feature was not approved.
4. Merge each selected event group into the existing hook object. Preserve all
   unrelated settings, event groups, and handlers. Reuse an identical entry
   instead of adding a duplicate. For Codex, use `.codex/hooks.json`, or keep its
   existing inline TOML representation. For Claude Code, prefer
   `.claude/settings.local.json`; keep its JSON representation. Do not replace a
   complete configuration with the example.
5. Inspect the proposed commands and complete the host's normal trust review.
   In Codex, use `/hooks` to review and trust the definition. In Claude Code,
   use `/hooks` and the normal project/settings review. Never bypass trust.
6. Test each selected command with its documented event shape for this project.
   Check a permitted planning edit and a rejected source edit before relying on
   the guard. Check one valid and one malformed checkpoint for the advisory.
   Record the absolute paths, loaded Skill version, host configuration,
   activation approval, and result in discovery. A direct script test does not
   establish that a native host loaded or ran the hook.

Host configuration and executable checks follow the approved worktree process.
The project orchestrator maintains the canonical markers and settings. Keep
local absolute paths and private Skill files out of public deliverables.

## Saved-context loader

The loader opens only the explicit project's marker, `CONTEXT.md`, and
`.project-kickoff/DISCOVERY.md`. It does not search ancestors or use paths from
checkpoint text. A session in the root or an ordinary subdirectory can load
context. A session outside it, or inside a nested repository or linked worktree,
loads no parent context. Give another worktree its own approved root and records
if it needs this hook. Do not point worker sessions at the canonical
orchestrator's checkpoint.

The loader reads:

- `CONTEXT.md`: phase and status under `Current phase`, pending question under
  `Evidence and current state`, approval IDs under `Approved decisions needed
  for resumption`, and the first `Next action` line.
- `DISCOVERY.md`: top-level current stage and state; pending question under
  `Open questions and pending question`; and pending question, next action, and
  last approval ID under `Resume checkpoint`.

Use the existing labels and one line per short field. Put full choices, history,
rationale, and evidence in their normal sections. The loader does not add those
sections to the session. It supports the version 0.1 checkpoint templates and
reports unknown formats instead of rewriting records.

## Direct-edit guard

The guard handles documented `Write`, `Edit`, and `apply_patch` input. For a
patch, it collects Add, Delete, Update, and Move destinations, including multiple
files. It resolves event `cwd`, relative paths, `..`, lexical and symlink
destinations, nested repositories, and linked worktrees. Every canonical
destination must be an exact approved path. Canonical source and application
configuration stay blocked unless they are incorrectly listed as approved
planning paths. Setup must never add product source or application configuration
to this allowlist. A malformed supported payload or active settings file fails
closed. An active feature also refuses a configured root without real Git
metadata. Patches with an `Environment ID` are rejected because the local guard
cannot resolve a nonlocal destination.

The settings file and loader marker remain blocked even when their literal names
appear in `approved_paths`. A broad string such as `.project-kickoff/*` is only a
literal filename and does not approve files below that directory. This prevents
an allowlist entry from changing the guard or its activation marker.

On Claude Code, the documented nonempty `agent_id` field positively identifies
a subagent. Such an actor cannot edit canonical `MISTAKES.md`, `CONTEXT.md`,
root `TASKS.md`, `.agent-team/TASKS.md`, or `.agent-team/TEAMS.md` through the
supported tools, even when the file is approved for the main thread. The
subagent can edit an exact approved assigned context or handoff file. Codex does
not supply a verified actor identity on these edit events. Do not infer one from
the shared `session_id`, `cwd`, branch name, missing fields, or transcript data.
Keep the single-writer instructions active on Codex.

This is a direct-edit guard, not a universal filesystem sandbox. Its sample
matcher does not cover shell commands. Bash, external processes, unsupported
tools, native host sessions that do not run the hook, and changes made after a
tool call remain outside its enforcement claim. Normal host permissions,
sandboxing, review, and project policy still apply.

## Checkpoint advisory

The advisory examines a checkpoint only when its path appears in a successful
supported edit payload. It reuses the loader's bounded symlink-safe reader and
field parser. It reports missing Phase, Status, Pending question, or Next action
values; conflicting duplicate fields inside that record; unreadable records;
and the 64 KiB record limit. A structurally valid record produces no message.

The advisory checks each edited record separately. It does not compare CONTEXT
with DISCOVERY during a multi-file update, because the first completed file can
represent an intermediate state. It does not validate semantic truth,
freshness, an answer, or an approval. It does not write, return an approval
decision, block the completed edit, wait for the user, or force continuation
through a Stop hook.

## Maintain and disable

At completed handoff, completed audit-only scope, or abandonment, disable the
saved-context loader marker. A temporary pause can keep it enabled. Keep
checkpoint files. The edit guard and advisory remain within their recorded
project activation scope until the user disables them or their approved scope
expires. Do not disable them automatically at every handoff. On an explicit
restart, restore only the user's recorded hook choices within the approved scope.

The guard protects `.project-kickoff/hooks.json` and
`.project-kickoff/context-hook.json` from its matched edit tools. To maintain one
of these files, first disable or remove only the matching `PreToolUse` entry
through the trusted host settings flow or a manual editor outside that hook.
Make the approved marker or settings change, validate it, then restore the guard
entry if it remains enabled. Existing ownership policy still governs approved
assigned context and handoff paths. Preserve every unrelated hook and setting. Do not
use a broad settings replacement. If the settings file is missing, both new
actions are silent. If its feature Boolean is false, that action is silent.

## Limits and boundaries

The scripts make no network calls, launch no subprocess, and write no project
data. Input is at most 64 KiB. The loader marker is at most 4 KiB. New hook
settings are at most 16 KiB, with at most 64 exact approved paths. A patch can
name at most 128 paths. Each checkpoint is at most 64 KiB. Each loaded field is
at most 240 characters. Serialized hook output is at most 8192 bytes. Examples
use a five-second timeout.

Settings and checkpoint symlinks, symlinked record directories, and nonregular
records are rejected. The guard checks both lexical and resolved edit targets so
a symlink alias cannot hide canonical source or a shared record. These controls
use POSIX file operations; use the instruction-based workflow on native Windows.

Keep approval interpretation, the one-question interview, dependency installs,
tracker initialization and seeding, cleanup after verified integration, writing
quality review, lesson selection, and the readiness gate in the explicit Skill
workflow. No hook performs those decisions or mutations.

Host contracts checked 2026-09-06:
[Codex hooks](https://learn.chatgpt.com/docs/hooks) and
[Claude Code hooks](https://code.claude.com/docs/en/hooks). The examples use the
shared `PreToolUse` deny and `PostToolUse` additional-context envelopes. Codex
reports `apply_patch` in `tool_input.command`. Claude Code reports `Write` and
`Edit` file destinations in `tool_input.file_path` and exposes `agent_id` only
for subagent calls. Native host sessions were not exercised for this release.
