# Optional session context hook

This hook supplies saved kickoff context when a session starts, resumes, clears,
or compacts. It does not start a kickoff or answer a question. Keep the normal
resume instructions as the fallback. The agent must still verify actual files,
valid approvals, and the user's current request.

## Enable for one approved project

The user must approve activation for the intended project. A Skill installation
or upgrade does not activate the hook. Confirm the project boundary first. This
optional planning setup can occur during discovery; it does not authorize product
setup or resolve an open stage decision. Record the activation choice in discovery.

1. Check that Python 3.9 or later is already available on Linux, macOS, or WSL.
   Use its verified absolute path. This script needs only the standard library.
   If the runtime or host hook feature is absent, keep instruction-based resume.
   Do not install a runtime or change global settings as a hook side effect.
   In Codex, `codex features list` can report the local `hooks` feature state.
   Current builds enable it by default. If a supported build has it disabled,
   include project-scoped `[features] hooks = true` in the proposed configuration
   change; merge the existing table. Respect managed policy. Do not assume an
   older build supports the feature or bypass an enforced disable setting.
2. Read the host's existing project configuration and matching hooks. Use
   [the Codex example](../assets/hooks/codex-session-start.json) or
   [the Claude Code example](../assets/hooks/claude-session-start.json).
   These files are examples, not active configuration. Replace each placeholder
   with a verified absolute path. Quote each argument for the host shell; the
   examples use POSIX single quotes. Escape any apostrophe in an actual path.
3. Merge only this `SessionStart` entry. Preserve all unrelated settings and
   hooks. Reuse an identical entry instead of adding a duplicate. For Codex, use
   the project's `.codex/hooks.json`, or its existing inline hook representation.
   For Claude Code, prefer `.claude/settings.local.json`; merge with its existing
   `hooks` object. Do not replace the whole configuration with an example.
4. Inspect the proposed command and complete the host's normal trust review.
   In Codex, use `/hooks` to review and trust the definition. In Claude Code,
   use `/hooks` and the normal project/settings review. Never bypass trust.
5. After the checkpoint files exist, create the project opt-in record at
   `.project-kickoff/context-hook.json` with `{"enabled": true}`. If this file
   exists, preserve other fields and change only the approved enabled state.
   Do not create it for `help`, `version`, or `status`.
6. Test the command with a `SessionStart` event for this project. Check that its
   output contains only the intended short checkpoint fields. Record the paths,
   loaded Skill version, host configuration, activation approval, and test result
   in discovery. Do not claim native hook execution from a direct script test.

Host configuration and executable checks follow the project's approved worktree
process. The orchestrator maintains the canonical marker as a planning record.
Keep local absolute paths and private Skill files out of public deliverables.

The hook opens only the explicit project's marker, `CONTEXT.md`, and
`.project-kickoff/DISCOVERY.md`. The command's project root must be absolute. It
does not search ancestors or use paths supplied by checkpoint text. A session in
that root or an ordinary subdirectory can load context. A session outside it, or
inside a nested repository or linked worktree, loads no parent context. Give a
different worktree its own approved root and records if it needs this hook. Do
not point worker sessions at the canonical orchestrator's checkpoint.

## Maintain and disable

Keep the existing short template fields current. The loader reads:

- `CONTEXT.md`: phase and status under `Current phase`, the pending-question
  field under `Evidence and current state`, approval IDs under
  `Approved decisions needed for resumption`, and the first `Next action` line.
- `DISCOVERY.md`: the top-level current stage and state, the pending-question
  field under `Open questions and pending question`, and the pending question,
  next action, and last approval ID under `Resume checkpoint`.

Use the existing labels and one line per short field. Put full question choices,
history, rationale, and evidence in their normal detailed sections. The hook does
not read those sections into the session. It reports unknown formats instead of
rewriting old records. Version 0.1 checkpoint templates remain supported.

On completed handoff, completed audit-only scope, or abandonment, set the marker's
`enabled` field to `false`. A temporary pause can keep it enabled. On an explicit
restart, restore the user's recorded hook choice only within its approved scope.
The hook never changes its own marker. If the marker is missing or disabled, it
prints nothing and creates nothing. Remove only its matching hook entry if the
user wants to uninstall the hook; preserve other hooks and checkpoint files.

## Limits and diagnostics

The hook is read-only. It makes no network calls, launches no subprocess, installs
nothing, and changes no Git or project data. The host supplies a finite JSON
event on standard input and closes the input stream. Host examples use a five
second timeout. Input and each checkpoint have a 64 KiB limit. The marker has a
4 KiB limit. Each field has a 240-character limit. Serialized output is at most
8192 bytes. Oversized records are skipped; oversized excerpts are marked.

All record symlinks and symlinked record directories are rejected, including
links within the project. Nonregular files are rejected. This implementation
uses POSIX file controls; use instruction-based resume on native Windows.

Missing, malformed, or inaccessible records produce a short diagnostic and exit
successfully. Explicit conflicting pending-question values are reported. The
loader does not decide which record is correct or validate approval meaning.
It labels extracted text as untrusted reference data. That label and field limits
reduce accidental misuse; they do not prove that a record is trustworthy.

`help`, `version`, and `status` still follow their read-only routes. Receiving
saved context does not authorize an interview, setup, or another user question.

Host contracts checked 2026-09-06:
[Codex hooks](https://learn.chatgpt.com/docs/hooks) and
[Claude Code hooks](https://code.claude.com/docs/en/hooks). Both accept the
`SessionStart` JSON output used by this script. The examples cover the four
shared event sources; other events are outside this hook's scope.
