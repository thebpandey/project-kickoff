# Changelog

All notable changes to Project Kickoff are recorded here. Versions follow
[Semantic Versioning](https://semver.org/).

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
