# Integrated package checks

Checked: 2026-09-06

Integration base before this check record and its source corrections:
`a4e40865f264200f0e9f91bfad7b3ffa35b47d2a`.

The candidate correction uses `APR-###` consistently. It also records explicit
user-supplied changes without asking for the same decision again. Existing-project
kickoff can update approved planning, agent, skill, and tracker setup; application
remediation remains in the Agent-Team handoff.

## Release allowlist inspected

The release contains only these 23 files:

- `SKILL.md`, `README.md`, `CHANGELOG.md`, and `LICENSE`;
- `agents/openai.yaml`;
- all seven Markdown files in `references/`;
- the eleven named Markdown templates in `assets/templates/`.

Development files under `docs/`, repository metadata, `.gitignore`, worktrees,
and local runtime state are outside this allowlist.

## Results

| Check | Observed result |
| --- | --- |
| Bundled `quick_validate.py` | Passed: `Skill is valid!` |
| YAML and release version | Parsed with PyYAML 6.0.3. `SKILL.md` version `0.1.0` matches README version, `v0.1.0` tag guidance, `project-kickoff-0.1.0.zip`, and CHANGELOG entry. Codex metadata names `$project-kickoff` and enables implicit invocation. |
| Markdown links | All 37 local runtime links resolved. Links in templates were resolved as generated-project sibling targets against the corresponding named templates. Three external Markdown links were excluded from local resolution. No link contained a dynamic placeholder. |
| ID schema | No stale `AP-`, `E-`, or `US-` workflow prefixes were found. The package uses `APR-`, `EPIC-`, and `STORY-`, while its existing-project rules preserve established external IDs. |
| Release contents | Exact allowlist match: 23 regular files, no symlinks, no executable files, no binary archives, and no dependency or cache trees. |
| Sensitive content | Credential and private-key pattern scan returned no matches in the release allowlist. Source inspection found instructions and labeled placeholders, not credential values. |
| Patch hygiene | `git diff --check` passed. |

## Limits

These checks validate the package structure and the integrated source tree. They
do not replace the independent behavior scenarios in `docs/behavior-checks.md`.
No release archive, Git tag, installation, publication, dependency download, or
external mutation occurred during this check.

## README and action-router extension

The extension started from integration revision `d316210`. The package now
documents seven prompt actions and keeps `help`, `version`, and `status` read-only.
The README contains two Mermaid flowcharts and two shell install blocks. Both
shell blocks passed `bash -n`. The package validator and patch whitespace check
also passed after this extension. Mermaid render evidence is recorded separately
after an independent renderer checks the committed source.

## Fail-closed installation fixtures

The two README install blocks were tested with a local mock of `gh repo clone`.
The fixture used no network access. For both Codex and Claude Code, a failed clone
returned status 42, a partial package returned status 1, and a complete package
returned status 0. Complete packages also passed from linked Git worktrees. Every
installed private target was ignored by Git and absent from `git status`.

Each successful fixture contained all 23 required release files. The blocks stop
before later writes and checks after a clone failure, and they stop when any
required file is missing.
