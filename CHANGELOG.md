# Changelog

All notable changes to Project Kickoff are recorded here. Versions follow
[Semantic Versioning](https://semver.org/).

## [0.4.0] - 2026-09-10

### Added

- A first-invocation question that lets the user select the model and the
  reasoning effort for planning work and for delegated work.
- `references/model-effort.md` with the question shape, the named profiles, the
  record location, and the honest limits.
- Host controls for the selection in `references/hosts.md`, including the
  documented Claude Code model identifiers and the Codex capability lookup.
- A package manifest test that checks version consistency across `SKILL.md`,
  `CHANGELOG.md`, the README, and the handoff template, and that checks both
  README `kickoff_required_files` allowlists against the package files.
- `docs/model-effort-checks.md` with the instruction-level check steps.

### Compatibility

- The selection is recorded as a `DEC-###` decision in
  `.project-kickoff/DISCOVERY.md`. No new state file is added and the discovery
  write limit is unchanged.
- A Skill cannot change the model or the reasoning effort of its parent session.
  Project Kickoff reports the planning selection and names the host control. It
  never claims that it switched the parent model.
- `status`, `help`, and `version` stay read-only. They do not ask the new
  question and they do not write its record.
- Install the complete package, including the new `references/model-effort.md`.
  Existing checkpoints, decisions, approvals, and trackers stay valid.

## [0.3.1] - 2026-09-09

### Added

- Machine-readable `.project-kickoff/AGENT_TEAM_HANDOFF.json` template for
  Agent-Team 7.0.2 initialization.
- A bounded handoff checker and cross-repository integration test against the
  real Agent-Team 7.0.2 command-line harness.

### Fixed

- Project Kickoff now keeps its setup receipt in
  `.project-kickoff/setup.json`. It no longer creates or edits Agent-Team's
  `.agent-team/setup.json` runtime receipt.
- Markdown tracker examples now seed the first executable task as `ready`
  instead of the unsupported `planned` state.
- Agent-Team handoffs now limit the tracker to Beads or supported Markdown
  paths, limit the request to 500 implementation tasks and 250 KiB, and reject
  unsafe paths, duplicate IDs, broken dependencies, and non-actionable plans.
- Handoff task entries contain canonical tracker IDs only. Task content remains
  in the tracker and approved plan, which prevents a conflicting duplicate.
- Beads handoff validation uses the Agent-Team 7.0.2 five-second read window
  instead of the former 1.5-second limit.
- Epic and story summaries remain in `PLAN.md` instead of being exposed as
  runnable Agent-Team tracker work.

## [0.3.0] - 2026-09-06

### Added

- Optional PreToolUse guard for supported direct edits to a canonical checkout,
  with exact planning-path approval, linked-worktree handling, and bounded patch
  parsing.
- Claude Code shared-record protection when the host supplies a positive
  subagent `agent_id`. Codex keeps instruction-based single-writer controls.
- Optional read-only PostToolUse checkpoint structure diagnostics.
- Filled-block Project Kickoff wordmark with loaded version and creator credit.

### Compatibility

- The version 0.2.0 SessionStart loader and marker remain compatible. New guard
  and advisory features use a separate version 1 settings file and are disabled
  until the user approves and configures them for one project.
- Install the complete package, including the three new hook scripts and
  `references/wordmark.md`. Python 3.9 or later on a POSIX host is needed only
  for optional hooks. No third-party module is used.
- Existing host settings and trust decisions are not changed by an upgrade.
  Shell commands, external writers, unsupported tools, and native Windows stay
  under the manual workflow and normal host controls.

## [0.2.0] - 2026-09-06

### Added

- Optional read-only SessionStart context loader for Codex and Claude Code.
- Explicit project activation, bounded checkpoint excerpts, and separate host
  examples that preserve existing hook settings and normal trust controls.
- Non-blocking diagnostics and instruction-based resumption when context cannot
  be loaded. Existing 0.1 checkpoint fields remain supported.

### Compatibility

- Install the complete package, including `scripts/`. Python 3.9 or later on a
  POSIX host is needed only for the optional hook. No third-party module is used.
- Upgrading does not activate hooks, modify host settings, or migrate project
  files. Activation requires a recorded choice for the intended project.

## [0.1.0] - 2026-09-06

### Added

- Five-stage adaptive discovery with one-question approval gates and resumption.
- Project artifact contracts, dependency setup, tracker seeding, and Agent-Team
  handoff procedures.
- Read-only audit followed by guided planning and setup for existing projects,
  with an explicit audit-only boundary.
- Codex and Claude Code installation and invocation guidance.
- Read-only help, version, and status actions plus explicit start, audit,
  audit-only, and resume prompt actions.
- Detailed project-local installation with fail-closed package checks, operator
  workflow, dependency sources, and Mermaid diagrams in the package README.
- Proprietary package license with separate permissions for project outputs.
