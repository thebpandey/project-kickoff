# Project Kickoff

Current version: **0.1.0**

Project Kickoff is a reusable skill for Codex and Claude Code. It turns a software
idea into approved product, experience, technical, and implementation plans. It
then prepares a minimal scaffold and a verified handoff to Agent-Team. It does
not implement product features during kickoff.

The workflow supports web, mobile, desktop, API, CLI, and library projects. It
asks one decision at a time, saves interrupted discovery, researches alternatives,
and waits for the user before it selects a stack or fallback tracker. For an
existing project, it first audits current code, documents, Git state, checks, and
tracking without changing them. It then guides retain/change decisions and
approved document, setup, and tracker updates. Product code changes go to the
Agent-Team handoff. An explicit audit-only request stops after the evidence report.

## Install for one project

Use one native location for the host that will run the skill. Copy or clone the
complete private package directory; do not copy only `SKILL.md`.

For Codex:

```text
<project>/.agents/skills/project-kickoff/
```

For Claude Code:

```text
<project>/.claude/skills/project-kickoff/
```

The package must include `SKILL.md`, `LICENSE`, `CHANGELOG.md`, `agents/`,
`references/`, and `assets/`. Both hosts support symlinked skill folders. Keep
the package private and preserve the license. If the project repository is not
authorized to contain the Skill, exclude the local installation directory from
that repository and do not include it in project deliverables.

Current host documentation:

- Codex: https://learn.chatgpt.com/docs/build-skills
- Claude Code: https://code.claude.com/docs/en/skills

## Invoke

In Codex:

```text
$project-kickoff Help me define and prepare this project.
```

In Claude Code:

```text
/project-kickoff Help me define and prepare this project.
```

The host can also select the skill automatically when a request matches its
description. If a new installation does not appear, follow the current host's
refresh or restart guidance and verify which same-named skill source was loaded.

## Output

A completed kickoff produces an approved `PRD.md`, `DESIGN.md`, and `PLAN.md`;
shared `AGENTS.md` and a Claude adapter; discovery and context records; a selected
single tracker; dependency receipts; a minimal scaffold; and an exact Agent-Team
handoff. The scaffold can intentionally have no runnable application before
feature implementation starts.

Dependency installation is project-scoped by default. The workflow inspects
current official sources and actual installed versions before it proposes any
change. It does not add global configuration or hooks without matching approval.

## License

The Skill package uses the proprietary terms in `LICENSE`. Written permission
from the licensors is required to use, modify, or redistribute the Skill. The
license permits authorized commercial and client application development without
a paid entitlement.

Generated project files and template-derived project instructions have the
separate output permissions in Section 4 of `LICENSE`: they may be edited and
distributed, including commercially. Third-party tools keep their own licenses.
For permission, contact support@learnstackos.com.

## Releases and upgrades

Releases use semantic version numbers. A release tag has the form `v0.1.0`, and
the matching archive name has the form `project-kickoff-0.1.0.zip`. Build the
archive from that exact tag. Review [CHANGELOG.md](CHANGELOG.md) and the release
license before upgrading. Replace the complete installed package so references
and templates stay at one version. Preserve project outputs and local project
state; they are not part of the Skill package upgrade.

Verify the loaded skill path and `metadata.version` after an upgrade. Do not mix
files from different release tags. A newer version does not grant new license
rights or permission automatically.
