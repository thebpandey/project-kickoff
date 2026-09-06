# Context hook checks

Scope: user-approved audit finding 1, optional read-only saved-context loading.
Implementation baseline: `c67d432`; the final change also fixes the reviewed fence
delimiter case and includes host examples, lifecycle guidance, and version 0.2.0.

## Test-first evidence

On 2026-09-06, `python3 -m unittest discover -s tests -v` failed before the hook
existed. The failures reported the missing `scripts/load_context.py` executable.
After implementation, all 11 initial test methods passed.

Independent review identified a closing code fence being accepted as the next
action. A focused test reproduced the failure. The parser now skips every fence
delimiter. The final suite has 14 passing test methods, including eight shared
host/source subcases and direct execution of both example command definitions.

Checked behavior:

- Codex and Claude Code event-shaped fixtures for startup, resume, clear, and
  compact produce the documented SessionStart additional-context envelope.
- Missing, disabled, and non-boolean enabled markers remain silent.
- Malformed input and markers, missing files, invalid encoding, and oversized
  records produce non-blocking diagnostics.
- Existing 0.1 checkpoint headings load only supported fields. Diary text is not
  included. Unknown formats retain manual resume. Conflicting pending values are
  reported without deciding which value is correct.
- Field truncation and serialized Unicode output remain within the 8192-byte
  output limit.
- File symlinks, directory symlinks, and FIFOs are rejected without reading them.
- An explicit project root and ordinary subdirectory load the same records.
  Outside sessions and nested checkouts do not load the parent checkpoint.
- A Git fixture preserved every project and Git file hash, plus the working-tree
  status, after hook execution. No fixture contents were retained.
- Both illustrative host JSON files parse. Their substituted command strings
  run correctly in an isolated test project. README shell blocks pass `bash -n`.
- Runtime relative links resolve. The bundled Skill validator and
  `git diff --check` pass.

The local read-only Codex feature query reported `hooks stable true`. The CLI
also printed a stale temporary-directory cleanup warning; this did not affect
the result. No host configuration, trust record, or active project marker was
created or changed for this Skill repository.

## Limits

These are direct subprocess and configuration-shape checks, not native-session
integration tests. Host event and output contracts were checked against current
[Codex](https://learn.chatgpt.com/docs/hooks) and
[Claude Code](https://code.claude.com/docs/en/hooks) documentation. Native startup,
resume, and compaction still require a user-approved project installation and
normal host trust review.

The runtime requires Python 3.9 or later on POSIX. The loader recognizes the
existing templates' short fields; it is not a general Markdown parser or an
approval validator. It reports limits and leaves semantic verification to the
agent. The release excludes this report and the test suite.
