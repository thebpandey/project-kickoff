# Project artifact contracts

Adapt the linked templates; do not overwrite an existing file.
Inspect it, retain user content, and merge approved additions. Record the source
decision IDs, generating Skill version, and approved revision in each derived
artifact.

## Stable identity and traceability

Use stable IDs that do not change when titles or order change:

- `DEC-###`: approved decision.
- `REQ-###`: first-release requirement with observable acceptance criteria.
- `EPIC-###` and `STORY-###`: epic and user story.
- `TASK-###`: executable first-release plan task.

Never reuse a retired ID for a new meaning. Preserve a suitable existing
project's established IDs instead of renumbering them to this convention. Map
each actionable `REQ-###` to acceptance criteria and one or more `TASK-###`
entries. A satisfied existing requirement can link verified historical work
instead of creating a new task. Map
each `EPIC-###`, `STORY-###`, and `TASK-###` to its live tracker ID when the
tracker supports that record type. Validate missing mappings, hierarchy,
dependency direction, cycles, and roadmap items that were accidentally made
runnable.

## Required files

### PRD.md

Adapt [PRD.md](../assets/templates/PRD.md). Separate user-approved facts, cited evidence,
assumptions, and open questions. Include users and problem, current alternatives,
value, first-release boundary and non-goals, journeys, `REQ-###` acceptance
criteria, success measures, constraints, approved architecture and rationale,
researched stack alternatives and selected stack, data ownership, integrations,
project-specific security, deployment assumptions, and the intended folder tree.
Do not invent research, budgets, dates, or performance targets.

### DESIGN.md

Adapt [DESIGN.md](../assets/templates/DESIGN.md). Cover audience, voice, interaction principles,
information structure, flows, accessibility, errors, and content conventions.
For visual products, also define typography, colors and semantic tokens, spacing,
layout, responsive behavior, components and states, and motion. For an API, CLI,
or library, define its relevant interaction, errors, documentation, and naming;
state why visual sections do not apply.

### PLAN.md

Adapt [PLAN.md](../assets/templates/PLAN.md). Fully detail the approved first release and
keep later roadmap ideas in a non-runnable section. Each `TASK-###` includes its
epic or story, requirement links, outcome, prerequisites, implementation steps,
affected paths or boundary, acceptance criteria, verification, and an effort or
complexity estimate with assumptions. Mark parallel tasks only when their files,
state, and prerequisites permit independent work.

`PLAN.md` owns scope, acceptance criteria, and the approved task graph. The
selected tracker owns assignment and live execution status. A completed tracker
item does not silently revise `PLAN.md`; a plan revision does not erase execution
history.

### Project instructions and shared records

- Adapt [AGENTS.md](../assets/templates/AGENTS.md) as the common project policy.
- Adapt [CLAUDE.md](../assets/templates/CLAUDE.md) as a small Claude Code adapter. It must tell
  the agent to read `AGENTS.md` even when automatic import is unavailable. Add
  only real host differences. Project files do not override system instructions
  or tool controls.
- Adapt [MISTAKES.md](../assets/templates/MISTAKES.md) with instructions and an empty index. The
  project orchestrator is its sole writer. Do not invent lessons.
- Adapt [CONTEXT.md](../assets/templates/CONTEXT.md) and keep it short: current phase, canonical paths, approved decisions and
  sources, blockers, pending question, evidence, and next action. Link the live
  tracker instead of copying its history. Each teammate uses its assigned context
  path; the project orchestrator alone writes shared records.
- Adapt [README.md](../assets/templates/README.md) as a short project orientation and handoff.
- Adapt [TASKS.md](../assets/templates/TASKS.md) only after the user selects root `TASKS.md`
  as the tracker fallback. It is not an automatic or temporary tracker.

Use [DISCOVERY.md](../assets/templates/DISCOVERY.md) for the detailed interview
record. Use its decision and approval IDs as sources for derived artifacts.

For an existing project, adapt [AUDIT.md](../assets/templates/AUDIT.md) as the
bounded evidence report. Keep its `AUD-###` findings stable across revisions and
link approved remediation to requirements and plan tasks without renumbering
existing tracker records.

Generate a compact derived `PRODUCT.md` only if the installed Impeccable version
requires it. Name `PRD.md` and its revision as the source. Refresh it when a
relevant approved product decision changes.

Add `.gitignore` entries and example environment variable names only when the
approved tooling needs them. Never include secret values. List commands only for
tools that were created and verified. State clearly if the minimal scaffold does
not yet run an application.
