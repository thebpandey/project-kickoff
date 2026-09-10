# Model and effort selection checks

Check date: 2026-09-10. Baseline: `731badd` plus the `feat/model-effort` change.
Scope: the first-invocation model and reasoning effort selection added in
version 0.4.0.

The feature is instruction text. A unit test cannot prove that a host model
follows an instruction. This report separates what ran from what a reviewer must
observe in a live session.

## Automated checks that ran

`tests/test_package_manifest.py` runs in the existing suite with
`python3 -m pytest tests/ -q`.

| Test | What it proves |
| --- | --- |
| `test_readme_repeats_one_identical_allowlist` | The README holds exactly two `kickoff_required_files` allowlists and both hold the same entries in the same order. |
| `test_allowlists_match_the_package_files` | Each allowlist names exactly the tracked package files, with no duplicate and no missing entry. |
| `test_release_tree_names_every_package_file` | The README release tree names every package file. |
| `test_package_version_is_consistent` | `SKILL.md` `metadata.version`, the newest `CHANGELOG.md` entry, the handoff template `projectKickoff.version`, the README version line, the README wordmark line, the README archive name, and both README `--branch` tags hold the same version. |

The package file set comes from `git ls-files`, not from the README. The test
removes `docs/`, `tests/`, `assets/guide/`, `.gitignore`,
`scripts/check-guide.mjs`, and every `.html` file. A new package file must be
tracked in Git before the check sees it.

### Red evidence

Each check was broken in a separate copy under a temporary directory. Each
focused run returned exit status 1.

| Break | Focused test | Reported failure |
| --- | --- | --- |
| Removed `references/model-effort.md` from the first allowlist. | `test_allowlists_match_the_package_files` | `Items in the second set but not the first: 'references/model-effort.md'`. |
| Removed the `model-effort.md` line from the release tree. | `test_release_tree_names_every_package_file` | `AssertionError: 'model-effort.md' not found in 'project-kickoff/...'`. |
| Set `SKILL.md` `metadata.version` to `0.4.1` only. | `test_package_version_is_consistent` | `AssertionError: '0.4.0' != '0.4.1'`. |
| Reordered the first allowlist. | `test_readme_repeats_one_identical_allowlist` | `AssertionError: Lists differ`. |

## Instruction-level check steps

These steps need a live Codex or Claude Code session with the Skill installed.
They were not executed for this record. Run each step in a new conversation
unless the step says otherwise.

| ID | Action | Expected observable result | Failure |
| --- | --- | --- | --- |
| ME-01 | Send `start Build a small scheduling tool.` as the first message of a new conversation. | The assistant sends exactly one question. It asks for the model and the reasoning effort. It offers three named profiles. The first profile carries the `(Recommended)` label. The turn ends with `Reply with a number or your own answer.` | Two or more questions in the turn. A missing `(Recommended)` label. A missing or changed closing line. Any product question before the selection. |
| ME-02 | From the ME-01 state, send no answer and wait. | The assistant does not select a profile. It does not start the interview, write a file, or dispatch an agent. | The assistant picks a profile, reports a default as chosen, or begins discovery. |
| ME-03 | Answer ME-01 with `1`. Then send `start` again in the same conversation. | The assistant does not repeat the selection question. It continues with the first product question. | The selection question appears again in the same conversation. |
| ME-04 | Send `status /path/to/project` as the first message of a new conversation. Repeat with `help` and with `version`. | No selection question appears. The action returns its read-only report and stops. `.project-kickoff/DISCOVERY.md` keeps its previous modification time and content hash. | Any selection question. Any write. Any fall-through into discovery. |
| ME-05 | Complete ME-03, then inspect `.project-kickoff/DISCOVERY.md`. | The decision register holds one new `DEC-###` row. It names the planning model, the planning effort, the delegated model, the delegated effort, the user's answer source, and the date. No other file is created. | A missing record. A record in a new state file. A write to `.agent-team/setup.json` or to any file outside the project. |
| ME-06 | Start a new conversation for the same project. Send `resume /path/to/project`. | The selection question appears once. The recommended profile shows the values saved in ME-05 and labels them as the saved values. | The question offers the standard profile instead of the saved values. The question claims a saved value that the record does not hold. The question does not appear. |
| ME-07 | Answer ME-06 with a different profile. | The assistant records a new `DEC-###`. It marks the previous selection superseded. No stage approval is invalidated. | A silently overwritten record. An invalidated stage approval. A lost previous decision. |
| ME-08 | Read the assistant's report of the planning selection in ME-01 or ME-06. | The report states the selected planning model and effort. It names the host control that applies it, `/model` in Claude Code. It does not say that the Skill changed the session model. It does not call a recorded selection active. | Any claim that the Skill switched the parent model or effort. Any claim that a saved selection is already in effect. |
| ME-09 | Answer the question with a model identifier that the current session does not expose. | The assistant reports the constraint and asks one question. It does not start work on another model. | A silent move to a weaker model or effort. A report that names the selected tier while a lower tier ran. |
| ME-10 | Complete a selection, then let the Skill dispatch a scaffold or check agent. | The dispatched agent uses the selected delegated model and effort. The handoff names the model and effort that the host accepted. If the host exposes no such control, the report states that limit and names the setting that applied. | A dispatch that ignores the selection without a report. A handoff that names a model the host did not accept. |

## Limits

The automated checks cover the package manifest and the version strings only.
They do not prove that a host asks the question, records the decision, or honors
the selected tier. No live Codex or Claude Code session ran for this record. No
host setting, global configuration, or hook was changed.

The Claude Code model identifiers and the `/model` control in
`references/hosts.md` come from the task specification for this change. The Codex
model list and the Codex effort list stay unresolved by design; the Skill reads
them from current host capability at each selection.
