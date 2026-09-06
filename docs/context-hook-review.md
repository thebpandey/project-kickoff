# Context hook review

Review date: 2026-09-06. Scope: the approved, optional SessionStart context
loader. This review does not approve or implement other hook candidates.

## Pinned source review

Reviewed source: `c67d4320529df23694c8ec9a1853d6036ef1e0c8`.

- Script SHA-256: `71a3b35cf123e23baf5cc4c9ec7edb428ad41d7907bd1fc38f1181dc46a25c6e`.
- Test SHA-256: `2bfe1bb2f13a8fe036bc268efc00abbb9ba3f8001bc0cf3479578498a2fad518`.
- Environment: Linux, Python 3.14.4.
- Command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`.
- Result: all 11 tests passed.

The implementation requires an enabled project marker and an explicit project
root. It reads fixed checkpoint paths, limits input and output, and returns
reference context. It does not change files, answer questions, set approvals,
execute checkpoint text, or start an interview. Unknown or unavailable records
retain the manual resumption path.

An independent temporary fixture adapted the actual version 0.1 CONTEXT and
DISCOVERY templates. It removed template comments, supplied a phase, status,
pending question, approval reference, and next action, and added unrelated
history and a separate private-data sentinel file.

The fixture established these results:

- All five expected checkpoint fields appeared in the output.
- Unrelated history and the separate sentinel file did not appear.
- SHA-256 snapshots of every project file were identical before and after the
  hook call.
- Events from a nested checkout and a folder outside the project were silent.
- A missing DISCOVERY record produced a manual-read diagnostic.
- The temporary fixture was removed when the check ended.

## Defect found during review

The closing Markdown fence could be recorded as the next action. For example,
this CONTEXT section returned `Next action` as three backticks and omitted the
real action after the code block:

````markdown
## Next action
```text
Not checkpoint data
```
Wait for OQ-102.
````

The parser toggled its fence flag and then continued to parse the closing line.
The builder received this reproduction and a request for a narrow fix and
regression test. The fix and its verification are recorded below.

## Final delta review

Reviewed final implementation and documentation: `7253e6d`. The review branch
merged that source after preserving the initial report. No material defect
remains within the reviewed scope.

The parser now skips the delimiter immediately after updating fence state. A
fresh run passed all 14 test methods. A separate fixture repeated the original
failure with `source: compact` and a project path containing spaces and an
apostrophe. It loaded `Wait for OQ-102.` and omitted the fence and fenced text.
The fixture was removed when the check ended.

The targeted documentation and configuration review confirmed:

- Activation is optional and scoped to an approved project. Installing or
  upgrading the Skill does not activate the hook.
- Both example commands use explicit interpreter, Skill, and project paths.
  Their JSON definitions select only the four shared source values and apply a
  five-second timeout. The suite executed both substituted example commands.
- Configuration guidance preserves unrelated host settings, avoids duplicate
  entries, and retains host trust controls. It explains how to check an available
  Codex hook feature without bypassing managed policy.
- The marker is disabled after completed handoff, completed audit-only work, or
  abandonment. The loader never edits its marker or validates approval meaning.
- The guide states Python 3.9 or later and POSIX requirements. Native Windows
  and unavailable hooks retain manual resumption. Existing short checkpoint
  fields remain the source; no duplicate summary is introduced.
- Both README installation allowlists exactly match the 27 tracked runtime
  files. The lists include the script, two configuration examples, and guide.
  README shell blocks passed `bash -n` without running their install commands.
- Skill metadata, README, and changelog agree on version 0.2.0. The bundled
  Skill validator and `git diff --check` passed.

The README names the intended v0.2.0 release. Release publication and archive
verification remain the release owner's work; this review did not publish it.

## Host contract and limits

The [Codex hook reference](https://learn.chatgpt.com/docs/hooks#sessionstart)
documents the four source values used by this script and the SessionStart
`hookSpecificOutput.additionalContext` response. It also documents project
trust and review of changed hook definitions.

The [Claude Code hook reference](https://code.claude.com/docs/en/hooks#sessionstart)
documents the same response shape and four sources. It also lists a separate
`fork` source, which this initial implementation does not handle.

The tests simulate hook event JSON. They do not establish that either host CLI
loaded a real configuration, accepted trust, or delivered the output to a live
model session. No real host configuration was changed. No model API call was
made. Template adaptation was checked; arbitrary Markdown conventions and
arbitrary existing-project identifier schemes were not certified.
