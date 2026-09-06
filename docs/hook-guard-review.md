# Hook guard independent review

Review date: 2026-09-06. Reviewer task: PKH-005. Baseline: `bba5fc8`.
Reviewed runtime: `b3928fa0d3ffc8a18da705852088bc04b5a74c78`.
Reviewed example configuration: `37e29432c5e62d9b7d53a70f0ef22808fe1bd334`.

## Result

No material defect remains in the approved findings 2, 4, and 5 scope. The
review approves `37e2943` for integration, subject to the limits below.

The review found two defects before the final revision:

- `7c23330` raised an unhandled `TypeError` for list or object `tool_name`
  input. `b3928fa` validates the field before set membership. The regression
  now checks both values for the PreToolUse denial and PostToolUse advisory.
- `b3928fa` used `Write|Edit` in the sample matchers while the guide named
  `apply_patch`. Current Codex documentation permits matcher aliases, so this
  did not establish a Codex bypass. `37e2943` nevertheless makes the portable
  literal contract explicit as `^(Write|Edit|apply_patch)$` in both samples and
  tests all three names against each expression.

## Acceptance evidence

| Requirement and flow | Preconditions and actions | Expected result | Independent evidence and outcome |
| --- | --- | --- | --- |
| PKH-002 / direct-edit guard | Enabled version-1 settings in a temporary canonical Git checkout. Send Write, Edit, and apply_patch events for relative, absolute, external-cwd, mixed patch, symlink, linked-worktree, nested-repository, and non-Git-root paths. | Exact approved canonical planning paths proceed. Canonical source/configuration, aliases, malformed supported payloads, and an active root without Git metadata are denied. | Eight public subprocess tests passed at `7c23330`; four focused boundary tests also passed. Final inspection confirms the runtime is unchanged after `b3928fa`. Pass. |
| PKH-005 / shared records | Claude event uses nonempty `agent_id`; Codex event uses untrusted actor-like fields. | Claude subagent edits to canonical shared records are denied with an orchestrator handoff instruction. Assigned output remains allowed. Codex does not infer an actor. | `test_claude_positive_subagent_identity_protects_shared_records` passed. Code inspection confirms the host and positive-string checks. Pass. |
| PKH-003 / checkpoint advisory | Enabled advisory with valid, missing, duplicate, oversized, and cross-file-intermediate checkpoints. | Valid records are silent. Record-local structural diagnostics are advisory only. Cross-file mismatch is not declared a final defect. | Two focused advisory tests and the read-only byte-snapshot test passed at `7c23330`. The advisory runtime is unchanged in later revisions. Pass. |
| PKH-002/003 / malformed envelope repair | Use the public command-line entry points with list and object `tool_name` values. | A bounded event-appropriate denial or advisory is returned without a traceback. | `test_non_string_tool_names_return_bounded_hook_diagnostics` passed at `37e2943`. A direct subprocess-fixture check confirmed all four event/value combinations produced the expected envelope keys within 8192 bytes. Pass. |
| PKH-002/003 / host sample entry points | Substitute test-owned absolute interpreter, package, and project paths in each host JSON sample. | The guard emits PreToolUse denial and the advisory emits PostToolUse context. Both matchers accept Write, Edit, and apply_patch literals. | `test_example_commands_run_each_public_entry_point` passed at `37e2943`. Pass for the sample-command boundary. |
| Wordmark | Inspect the loaded `SKILL.md`, metadata, and wordmark reference. | A filled-block PROJECT KICKOFF wordmark, loaded version, and `Created by thebpandey.` appear for a genuine explicit or implicit invocation and the completed workflow report; `#` fallback is documented. | `SKILL.md` invokes `references/wordmark.md`; `agents/openai.yaml` retains `allow_implicit_invocation: true`. The reference excludes quoted mentions and hook output. Pass. |

Commands run independently:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_project_hooks.ProjectHookTests.test_guard_blocks_canonical_source_from_relative_or_external_cwd \
  tests.test_project_hooks.ProjectHookTests.test_guard_parses_mixed_patch_add_delete_update_and_move_paths \
  tests.test_project_hooks.ProjectHookTests.test_guard_handles_symlink_aliases_in_both_directions \
  tests.test_project_hooks.ProjectHookTests.test_active_hooks_require_a_real_canonical_git_checkout \
  tests.test_project_hooks.ProjectHookTests.test_claude_positive_subagent_identity_protects_shared_records \
  tests.test_project_hooks.ProjectHookTests.test_checkpoint_reports_local_missing_duplicate_and_size_diagnostics \
  tests.test_project_hooks.ProjectHookTests.test_checkpoint_checks_each_edited_record_without_cross_file_comparison \
  tests.test_project_hooks.ProjectHookTests.test_example_commands_run_each_public_entry_point

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_project_hooks.ProjectHookTests.test_guard_matches_native_header_whitespace_and_rejects_environment_target \
  tests.test_project_hooks.ProjectHookTests.test_guard_denial_output_is_bounded_for_long_patch_paths \
  tests.test_project_hooks.ProjectHookTests.test_approved_symlink_name_does_not_hide_source_or_shared_target \
  tests.test_project_hooks.ProjectHookTests.test_hooks_are_read_only_for_project_bytes

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_project_hooks.ProjectHookTests.test_non_string_tool_names_return_bounded_hook_diagnostics \
  tests.test_project_hooks.ProjectHookTests.test_example_commands_run_each_public_entry_point

git diff --check bba5fc8..37e2943
```

Each listed command completed successfully. The developer's full 36-test suite,
validator, shell syntax, package allowlist, JSON, link, version, and wordmark
checks are recorded in `docs/hook-guard-checks.md`; this review did not repeat
the unchanged full suite.

## Limits

These checks run the actual Python command entry points with event-shaped test
input. They do not prove that Codex or Claude Code loads, trusts, matches, or
delivers a live hook in a native session. No host configuration, global setting,
project marker, package, or release was changed. The guard remains limited to
matched Write, Edit, and apply_patch calls. Shell writes, external processes,
unsupported tools, and missing native hook execution remain outside its claim.
Claude shared-record enforcement relies only on a positive `agent_id`; Codex
continues to rely on the single-writer instructions.
