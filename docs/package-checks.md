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
| Markdown links | All 37 local runtime links resolved. Links in templates were resolved as generated-project sibling targets against the corresponding named templates. Two external Markdown links were excluded from local resolution. No link contained a dynamic placeholder. |
| ID schema | No stale `AP-`, `E-`, or `US-` workflow prefixes were found. The package uses `APR-`, `EPIC-`, and `STORY-`, while its existing-project rules preserve established external IDs. |
| Release contents | Exact allowlist match: 23 regular files, no symlinks, no executable files, no binary archives, and no dependency or cache trees. |
| Sensitive content | Credential and private-key pattern scan returned no matches in the release allowlist. Source inspection found instructions and labeled placeholders, not credential values. |
| Patch hygiene | `git diff --check` passed. |

## Limits

These checks validate the package structure and the integrated source tree. They
do not replace the independent behavior scenarios in `docs/behavior-checks.md`.
No release archive, Git tag, installation, publication, dependency download, or
external mutation occurred during this check.
