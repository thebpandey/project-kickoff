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
| `test_release_tree_holds_every_package_path` | The README release tree holds every package path and no other path. The check builds a full path for each tree entry from the box-drawing indentation. |
| `test_package_version_is_consistent` | `SKILL.md` `metadata.version`, the newest `CHANGELOG.md` entry, the handoff template `projectKickoff.version`, the README version line, the README wordmark line, the README archive name, and both README `--branch` tags hold the same version. |

The package file set comes from `git ls-files`, not from the README. The test
removes `docs/`, `tests/`, `assets/guide/`, `.gitignore`,
`scripts/check-guide.mjs`, and every `.html` file. A new package file must be
tracked in Git before the check sees it.

### Red evidence

Each check was broken in a separate copy under a temporary directory. An
unbroken control copy passed all four checks with exit status 0. Each break
below returned exit status 1.

| Break | Focused test | Reported failure |
| --- | --- | --- |
| Removed `references/model-effort.md` from the first allowlist. | `test_allowlists_match_the_package_files` | `Items in the second set but not the first: 'references/model-effort.md'`. |
| Removed the `model-effort.md` line from the release tree. | `test_release_tree_holds_every_package_path` | `Items in the second set but not the first: 'references/model-effort.md'`. |
| Removed the nested `assets/templates/README.md` line from the release tree. | `test_release_tree_holds_every_package_path` | `Items in the second set but not the first: 'assets/templates/README.md'`. |
| Set `SKILL.md` `metadata.version` to `0.4.1` only. | `test_package_version_is_consistent` | `AssertionError: '0.4.0' != '0.4.1'`. |
| Reordered the first allowlist. | `test_readme_repeats_one_identical_allowlist` | `AssertionError: Lists differ`. |

The third row is the reviewer's finding 5. The first version of the tree check
compared basenames only, so it returned exit status 0 on that break. The
top-level `README.md` line satisfied the old assertion. `README.md`, `CLAUDE.md`,
and `AGENT_TEAM_HANDOFF.json` each occur at more than one path in the package,
so the path-aware check is needed for all three.

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
| ME-06 | Start a new conversation with the working directory set to the ME-05 project. Send bare `start Add invoice export to this tool.` with no path argument. | The selection question appears once and does not wait for a path. The recommended profile shows the values saved in ME-05 and names the exact path they came from. The assistant does not treat that directory as the confirmed project root; it still asks its normal path question afterwards. | The question offers the built-in profile although the record is readable. The question waits for a path. The assistant adopts the looked-up directory as the confirmed root. |
| ME-07 | Start a new conversation with the working directory set to a directory that holds no `.project-kickoff/DISCOVERY.md`. Send bare `start Build a small scheduling tool.` | The selection question appears once. It offers the built-in recommended profile. It claims no saved value and names no path. | Any claimed saved value. A question that waits for a path. A read of an unrelated project's record reported as this project's saved value. |
| ME-08 | Start a new conversation. Send `resume /path/to/project` with the ME-05 project path. | The selection question appears once. The recommended profile shows the values saved in ME-05, labels them as the saved values, and names that path. | The question offers the built-in profile instead of the saved values. The question claims a saved value that the record does not hold. The question does not appear. |
| ME-09 | Answer ME-08 with a different profile, then confirm the same project. | The assistant records a new `DEC-###` with status `Approved` and the user's answer as the source. It marks the previous selection superseded and names the values it held. It invalidates no stage approval. | A silently overwritten record. An invalidated stage approval. A lost previous decision. |
| ME-10 | Complete ME-06, then confirm a different project directory than the one the record came from. | The assistant says the offered values belong to another project and names both paths. It writes a new `DEC-###` in the confirmed project. It supersedes no record in either project. | A supersede written into the looked-up project. A saved value carried into the confirmed project with no disclosure. |
| ME-11 | Send `resume /path/to/project` for a project whose discovery record holds a pending stage question. | The model and effort question is asked first. The pending-question record still holds the original stage question and its stage. The restored stage question follows the answer. | The pending-question record now holds the model and effort question. The restored stage question is lost. |
| ME-12 | Read the assistant's report of the planning selection in ME-01 or ME-08. | The report states the selected planning model and effort. It names the host control that applies it, `/model` in Claude Code. It does not say that the Skill changed the session model. It does not call a recorded selection active. | Any claim that the Skill switched the parent model or effort. Any claim that a saved selection is already in effect. |
| ME-13 | Answer the question with a model identifier that the current session does not expose. | The assistant reports the constraint and asks one question. It does not start work on another model. | A silent move to a lower tier. A report that names the selected tier while a lower tier ran. |
| ME-14 | Complete a selection, then let the Skill dispatch a scaffold or check agent. | The dispatched agent uses the selected delegated model and effort. The handoff names the model and effort that the host accepted. | A dispatch that ignores the selection without a report. A handoff that names a model the host did not accept. |
| ME-15 | Complete a selection on a host that exposes no subagent model control, then reach a dispatch. | The assistant stops before the dispatch. It names the setting that would apply instead. It asks one question and waits. | A dispatch at the host default with no question. Any report of the selected tier while the default ran. |

## Limits

The automated checks cover the package manifest and the version strings only.
They do not prove that a host asks the question, records the decision, or honors
the selected tier. No live Codex or Claude Code session ran for this record. No
host setting, global configuration, or hook was changed.

The Claude Code model identifiers and the `/model` control in
`references/hosts.md` come from the task specification for this change. The Codex
model list and the Codex effort list stay unresolved by design; the Skill reads
them from current host capability at each selection.
