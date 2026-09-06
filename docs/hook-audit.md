# Hook audit decisions

Audit baseline: project-kickoff 0.1.0, source `daf472d`.

The user requested findings one at a time, with a decision before each
conversion. Approval for one finding does not authorize other conversions.

## Finding 1 — Load saved kickoff context

Decision: approved. The user answered "yes" to the proposed read-only
context-loading hook.

Add a small shared command hook with separate Codex and Claude Code setup
examples. On supported SessionStart events, load a bounded excerpt of existing
kickoff records for an explicitly enabled project. Missing or inconsistent
records produce factual diagnostics. The hook does not change files, infer
approval, answer a question, install tools, or start setup.

Keep instructions for verifying saved state against the current project. Keep
manual resumption when hooks are disabled, unsupported, or not trusted. Existing
host configuration and hooks must survive setup. Enabling hooks in a generated
project follows that project's approved scope and normal host trust controls.

Implementation uses a task worktree, meaningful script tests, and independent
review before integration. This compatible capability increments the skill to
0.2.0. The 0.1.0 release remains unchanged.

Primary interface references checked during audit:

- https://learn.chatgpt.com/docs/hooks
- https://code.claude.com/docs/en/hooks

Later findings remain undecided. Present the next finding only after completing
the approved conversion.
