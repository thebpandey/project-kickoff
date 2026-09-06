# Codex and Claude Code adapters

Detect the current host from exposed runtime and tools. A mention in the prompt
does not change the host. Use native paths and controls; do not emulate missing
capabilities or claim a model/agent switch that the host did not perform.

The action words `start`, `audit`, `audit-only`, `resume`, `status`, `help`, and
`version` are prompt vocabulary after Skill invocation. Never execute them as
shell binaries. Route them through `SKILL.md` before loading the workflow.

## Codex

- Project skills: `.agents/skills/<skill-name>/SKILL.md`, searched from the
  current directory through the repository root.
- User skills: `~/.agents/skills/<skill-name>/SKILL.md`.
- Explicit invocation: `$project-kickoff`.
- Use the exposed native user-input tool for one recommended-choice question.
- Use Codex collaboration controls for delegated work only when available and
  authorized. Resolve models and reasoning effort from current host capability.

Official source: https://learn.chatgpt.com/docs/build-skills

## Claude Code

- Project skills: `.claude/skills/<skill-name>/SKILL.md`.
- User skills: `~/.claude/skills/<skill-name>/SKILL.md`.
- Explicit invocation: `/project-kickoff`.
- Use Claude Code's exposed native question and subagent controls when present.
- A same-named personal skill can shadow a project skill. Verify the loaded
  source before relying on project-specific content.

Official source: https://code.claude.com/docs/en/skills

Both hosts support skill directories with referenced files and symlinked skill
folders. Install the complete package, including `LICENSE`, `CHANGELOG.md`, `agents/`,
`references/`, `assets/`, and `scripts/`. Preserve the private-use license. Keep a
project-local proprietary installation out of generated project deliverables and
public source control unless that repository is authorized to contain the Skill.

On resume or setup, compare the package `metadata.version` with the version in
discovery, setup, and prior handoff records. Read the intervening `CHANGELOG.md`
entries. A patch indicates a compatible correction. A minor release adds a
compatible capability, except that a documented breaking change during 0.x also
uses a minor bump. A major release changes a contract incompatibly. Report the
project-specific effect and keep the current pinned installation unless the user
approved an upgrade. Preserve stable IDs, evidence, valid approvals, and project
outputs through an approved migration.

## Instructions and handoff

Use `AGENTS.md` as common project policy. `CLAUDE.md` explicitly directs Claude
Code to read it and contains only necessary host differences. Read project
instructions by their actual hierarchy; never claim they override system rules,
permissions, or tool controls.

At handoff, give the exact invocation for the detected host:

- Codex: `$agent-team start`
- Claude Code: `/agent-team start`

If Agent-Team uses another verified installed name or version-specific syntax,
use its actual help output and record it. Preparing the command does not run it.
If delegation is unavailable, finish planning and ask for that capability or an
explicit exception before writing scaffold or product code on the canonical
integration branch.

## Optional project hooks

Read [the project hook guide](context-hook.md) before activation. Separate Codex
and Claude Code examples include the context loader, direct-edit guard, and
checkpoint advisory. Merge only approved entries into existing project settings
and complete normal host trust review. Installing or upgrading this Skill alone
does not activate a hook.
