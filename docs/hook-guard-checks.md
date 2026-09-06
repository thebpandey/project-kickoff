# Hook guard and checkpoint advisory checks

Check date: 2026-09-06. Baseline: `bba5fc8`. Environment: Linux, Python
3.14.4. The tests use temporary Git repositories and execute each script as a
real subprocess through its standard-input and command-line interface.

## Acceptance flows

| Requirement and test ID | Preconditions and data | Actions | Expected result | Evidence and outcome |
| --- | --- | --- | --- | --- |
| PKH-002 / AT-01 canonical edit guard | Version 1 project settings enable the guard. Temporary canonical and linked checkouts contain test-owned files. | Send Write, Edit, and apply_patch PreToolUse events with relative, absolute, `..`, symlink, mixed, move, delete, nested-repository, linked-worktree, and uninitialized-root destinations. | Exact approved planning files and task worktrees proceed silently. Canonical source, configuration, hidden symlink targets, malformed supported input, nonlocal environment patches, and active non-Git roots return a bounded deny result. | `tests.test_project_hooks`: guard path, patch, settings, symlink, worktree, malformed-input, canonical-checkout, and output-bound methods pass. AT-01 Pass. |
| PKH-002 / AT-02 shared-record writer | Claude fixtures use a nonempty documented `agent_id`. Codex fixtures reuse session and working-directory values and include untrusted actor-like fields. | Attempt approved canonical shared-record and assigned handoff edits on each host mode. | Claude subagent shared-record edit is denied and assigned output is allowed. Codex does not infer actor identity from unsupported fields. | `test_claude_positive_subagent_identity_protects_shared_records`, `test_approved_symlink_name_does_not_hide_source_or_shared_target`, and `test_codex_does_not_infer_actor_from_shared_fields` pass. AT-02 Pass. |
| PKH-003 / AT-03 checkpoint advisory | Version 1 settings enable the advisory. Test-owned checkpoints cover valid, missing, duplicate, conflicting, oversized, and cross-file intermediate states. | Send Write, Edit, and apply_patch PostToolUse events. | Valid structure is silent. Record-local faults add bounded context without a decision or write. Cross-file pending-question differences are not called final defects. | `tests.test_project_hooks`: all checkpoint methods and the byte-snapshot method pass. AT-03 Pass. |
| PKH-004 / AT-04 host examples | Codex and Claude example JSON uses substituted temporary absolute paths. | Confirm both event matchers accept the literal `Write`, `Edit`, and `apply_patch` names. Execute each new sample command with event-shaped input. | Both samples route every documented literal tool name. Both hosts receive the shared PreToolUse deny envelope and PostToolUse additional-context envelope. | `test_example_commands_run_each_public_entry_point` passes. Native host loading and alias semantics remain untested. AT-04 Pass for the sample command boundary. |

Test data exists only in temporary directories and is removed by the test suite.
The scripts do not persist results, so reload verification is not applicable.

## Red-green evidence

The first focused run contained 16 tests. All failed because
`scripts/guard_edits.py` and `scripts/check_checkpoint.py` did not exist. This
confirmed that the public-entry tests exercised the new behavior. Later focused
red runs reproduced three concrete defects before correction:

- an approved symlink name hid an unapproved canonical source target;
- eight long patch paths produced 13,864 bytes instead of the 8192-byte limit;
- a native-recognized indented Add header hid a canonical source destination;
- list and object `tool_name` values raised an uncaught `TypeError` instead of
  returning the event-appropriate bounded diagnostic.

The host-command test also failed with missing PreToolUse and PostToolUse groups
before the example files were updated. Each focused reproduction passed after
the narrow implementation change.

Focused verification command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_project_hooks -v
```

Result: 22 tests passed. The complete command
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` then passed
all 36 tests, including the unchanged 14-test SessionStart loader suite.

The Skill validator passed. Both README shell blocks passed `bash -n`. The two
runtime-package allowlists match all 31 package files. JSON samples, local
package links, version references, the two-line wordmark width, and
`git diff --check` passed focused checks.

## Tested artifact hashes

| Artifact | SHA-256 |
| --- | --- |
| `scripts/guard_edits.py` | `4c9c8b8d1ba97ce38677b190f787081b422d9e4c12b2a64e0b15ff131bdcb689` |
| `scripts/check_checkpoint.py` | `616e9a9a06644a38bc55cc5e52d4aadd459ed948cf03152374131a6bc8be5f09` |
| `scripts/hook_utils.py` | `727e86a111f0ab62214ac9aec26023c5b4b55f2ca4bfef154013a8528159fd32` |
| `scripts/load_context.py` | `4c439242dc6dac215dbd02e478d4f161bec5d73e75c1c74787dff1d808c98a1e` |
| `tests/test_project_hooks.py` | `1708ea0433d9a1c1b828d610a1e771bcfb973d1f7cc8f54ee9c757d145344e15` |
| Codex hook example | `ef04a6a4c00aba5947287c69daf01d6d69d7e3c209260f70557c980e22d3eb06` |
| Claude hook example | `f1a4237b0c6e39677af6bc2267e4ab55f993142fca08cc90fd1889d3bccca3c7` |

## Coverage limits

The checks simulate documented event JSON. No Codex or Claude Code session
loaded these files as active native hooks, and no host or global settings were
changed. The guard covers only matched Write, Edit, and apply_patch calls. Shell
commands, external processes, unsupported tools, and native sessions without the
hook stay under host controls and project instructions. Claude actor enforcement
uses only a positive `agent_id`; Codex shared-record ownership remains an
instruction because its edit events do not provide a verified actor identity.
The sample matcher test establishes portable literal-name coverage. It does not
test either host's native matcher-alias behavior.

The advisory validates bounded structure only. It does not establish semantic
freshness, correct approval meaning, readiness, or final agreement between files.
Dependency installation, tracker seeding, cleanup, lesson selection, writing
quality review, and readiness remain explicit orchestrator actions.

Primary contracts checked on 2026-09-06:
[Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Codex apply_patch streaming parser](https://github.com/openai/codex/blob/main/codex-rs/apply-patch/src/streaming_parser.rs),
and [Claude Code hooks](https://code.claude.com/docs/en/hooks).
