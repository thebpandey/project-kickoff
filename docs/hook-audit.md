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

Implementation and independent review are complete for finding 1. Fourteen
script tests pass. An independent existing-template fixture confirmed 0.1.0
checkpoint compatibility. A fence-parsing defect was reproduced and fixed.
The host examples and runtime file lists passed review. See
[implementation checks](context-hook-checks.md) and
[independent review](context-hook-review.md) for evidence and limits.

The optional script needs Python 3.9 or later on Linux, macOS, or WSL. Native
Windows retains manual resumption. Native CLI hook sessions were not exercised;
the tests executed event-shaped inputs and the example command definitions.
No hook was activated in the skill repository or global host configuration.

Published [v0.2.0](https://github.com/thebpandey/project-kickoff/releases/tag/v0.2.0)
from source `698489791878fd64386a32b34bfb043e3fb81903`. The extracted ZIP has
exactly 27 runtime files matching that commit; all 14 integrated tests passed.
GitHub's uploaded ZIP digest matches the local SHA-256:
`a61331eafeaebe0ac6b02df92de3a93df1550c3ee25ac8f02d8a480d608f602b`.
The repository remains private. Remote main and the peeled release tag matched
the release source. The uploaded checksum file's digest also matches its local
copy. The three clean, integrated task worktrees and branches were removed
through normal Git operations. The 0.1.0 release and local archive were preserved.
