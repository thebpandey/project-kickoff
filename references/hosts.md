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
- Read the current host capability at each selection. When exposed, recommend
  `gpt-6-sol` for planning, development, and independent review. Offer
  `gpt-6-luna` for optional routine, low-risk work. These examples were observed
  in the local Codex catalog and host tools on 2026-09-22 and are not a capability
  allowlist; use only model identifiers and effort levels available in the
  current host.

Official source: https://learn.chatgpt.com/docs/build-skills

## Claude Code

- Project skills: `.claude/skills/<skill-name>/SKILL.md`.
- User skills: `~/.claude/skills/<skill-name>/SKILL.md`.
- Explicit invocation: `/project-kickoff`.
- Use Claude Code's exposed native question and subagent controls when present.
- A same-named personal skill can shadow a project skill. Verify the loaded
  source before relying on project-specific content.
- The documented Anthropic model identifiers are `claude-fable-5-1`,
  `claude-opus-5-5`, `claude-sonnet-5`, and `claude-haiku-4-5-20251001`. The
  documented effort levels include `high` and `xhigh`. Use an identifier or a
  level only when the current session exposes it.

Official source: https://code.claude.com/docs/en/skills

Claude Opus 5.5 model configuration: https://code.claude.com/docs/en/model-config
(`claude-opus-5-5`, supported from Claude Code 2.1.280). Verify the installed
host exposes it before offering or applying it.

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

New optional handoffs use Project Kickoff 0.6.0 with Agent-Team 9.0.0 in
skill-first mode. Give the validated handoff and selected existing Beads IDs to
the user's v9 session only when the user asks to adopt it. Do not invoke a
controller, create `.agent-team/setup.json`, or start Agent-Team. The checker
result is `schema-valid-unverified` with `runtimeVerified: false`.

### Historical v8/controller projects

Released Project Kickoff 0.5.x handoffs and their Agent-Team 7.3.1 or 8.0.15
controller routes remain only for existing projects. Their setup receipts,
runtime identities, native role settings, and `project-initialize` behavior do
not apply to new v9 handoffs.

## Model and reasoning effort

Read [the model and effort selection](model-effort.md) for the question, its
timing, and its record. This section gives the host controls only.

A Skill cannot change the model or the reasoning effort of its own parent
session. The planning selection applies to that parent session. Report the
selection and give the user the control below. Never claim that the Skill made
the change.

| Host | How the user applies the planning selection |
| --- | --- |
| Codex | Use the model and reasoning-effort control that the current Codex session exposes. Read the host's own help output for its exact name before you quote it. |
| Claude Code | Use the session model control, `/model`. Read the host's own help output for the current effort control before you quote it. |

For delegated work, use the host's native subagent controls. In Claude Code, set
the model and the effort on each dispatched agent when the session exposes those
fields. In Codex, use the collaboration controls only when they are available and
authorized. Record the model and the effort that the host accepted.

When the host cannot apply the selection, follow the single stop-and-ask rule in
[the model and effort selection](model-effort.md).

## Instructions and handoff

Use `AGENTS.md` as common project policy. `CLAUDE.md` explicitly directs Claude
Code to read it and contains only necessary host differences. Read project
instructions by their actual hierarchy; never claim they override system rules,
permissions, or tool controls.

At an optional v9 handoff, give the user the validated handoff path and selected
Beads IDs. Do not give a start command or start Agent-Team automatically; the
user decides whether to ask the active Agent-Team session to adopt it. If
delegation is unavailable, finish planning and ask for that capability or an
explicit exception before writing scaffold or product code on the canonical
integration branch.

## Optional project hooks

Read [the project hook guide](context-hook.md) before activation. Separate Codex
and Claude Code examples include the context loader, direct-edit guard, and
checkpoint advisory. Merge only approved entries into existing project settings
and complete normal host trust review. Installing or upgrading this Skill alone
does not activate a hook.
