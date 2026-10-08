# Agent-Team and Lanes: shared planning, different execution

Agent-Team v9 keeps coordination inside the active host session, using Beads
for task state and Git for revisions. Lanes adds an installed orchestration
harness with model routing and scripts for integration. Both can use Project
Kickoff's approved documents. Their runtime records belong to each skill.

This comparison checks Agent-Team 9.0.0, the installed unversioned Lanes skill
and its Codex adapter, and Project Kickoff 0.6.0 on 2026-10-08. It is a contract
review. Neither execution workflow was launched for this report.

## What they share

Both split work into bounded tasks with separate Git worktrees. Workers need
clear file ownership and acceptance checks. The orchestrator handles
integration, while an independent reviewer examines work that requires review.
Both preserve unfinished changes and keep unrelated ready tasks moving when
one task blocks.

They also separate the approved plan from live execution state. That makes
Project Kickoff's `PLAN.md` useful to either workflow: a task already has its
requirements, prerequisites, and evidence expectations before a worker starts.

## Where the workflows differ

| Concern | Agent-Team v9 | Lanes |
| --- | --- | --- |
| Setup | Git and Beads. Beads initialization requires explicit approval; optional aids never gate readiness. | An installed harness checked with `install.sh --check`; relay tooling and credentials depend on the chosen route. |
| Task authority | Beads only. `TASKS.md` is an optional one-time import source. | Uses Beads when present; otherwise follows the project's existing tracker. |
| Dispatch | Native Codex or Claude agent tooling only, with real handles retained in the active session. Shell workers cannot substitute. | Host agents and supported relays, including DeepSeek or GLM for bounded routine work. |
| Model selection | Offers preferences for host roles using models the host actually exposes. | Assigns T0 to T3 tiers before dispatch, with model and effort routes for each tier. |
| Queue and capacity | Reads at most 20 ready rows. Defaults to two parallel teams, each with at most four ordered tasks; claims only the task starting. | Uses lane planning and the agreed lane cap; records each lane in `lanes.tsv`. |
| Runtime records | Beads and Git remain authoritative. Optional session breadcrumbs and a static dashboard provide context. No controller or daemon. | Per-project state under `~/.local/state/lanes/`, with briefs, reports, reviews, and a usage ledger. Includes a timer watchdog. |
| Review | Requires independent native review of every candidate revision before integration. The orchestrator rechecks review identity and evidence. | Classifies completed work. Narrow TRIVIAL prose changes skip review; REVIEW work needs an independent CLEAN verdict for its exact head. The orchestrator acts on the verdict. |
| Integration | Orchestrator integrates the reviewed revision, commits it, then closes the Beads issue. | Only `integrate.sh` merges lane work. Failed required post-merge checks trigger a revert and another fix cycle. |
| Resume | Reconciles Beads and Git with original observable handles. An uncertain earlier launch stays blocked; a substitute worker is forbidden. | Starts new subagents in the same preserved worktrees after a session restart; relay jobs can be reattached. |
| Cleanup and publication | Requires clean integrated work or recorded patch-equivalence evidence; deployment needs an approved batch command and verification rule. | Requires clean integrated work; pushes need authorization and a passing secret scan. Outward actions require approval. |

The resume difference matters. A worktree and task name do not give Agent-Team
permission to replace an uncertain worker. Lanes explicitly supports fresh
subagents after a restart. Those policies need reconciliation when switching
the orchestrator for existing work.

## Which kickoff artifacts each skill can use

| Artifact | Reuse in both workflows |
| --- | --- |
| `PRD.md` | Product scope, requirement IDs, and observable acceptance criteria. |
| `DESIGN.md` | Interaction rules and design obligations relevant to a task. |
| `PLAN.md` | Executable task definitions, dependencies, path boundaries, verification, and complexity assumptions. |
| `AGENTS.md` and `CLAUDE.md` | Common project policy and the host adapter, within each skill's execution rules. |
| `CONTEXT.md` and `.project-kickoff/DISCOVERY.md` | Approved decisions and recovery pointers; pass only relevant excerpts to workers. |
| `AUDIT.md` and `MISTAKES.md` | Existing-project findings and recorded lessons when applicable. |
| Selected tracker and `.project-kickoff/setup.json` | Existing task IDs and seeding mappings; the setup receipt records kickoff preparation. |
| Minimal scaffold and project `README.md` | Approved starting revision and verified commands. A scaffold may have no runnable application yet. |

Yes, these artifacts can be used by both skills. The reuse is direct at the
planning level. Execution still needs the chosen skill's own preparation.

For Agent-Team, the optional `.project-kickoff/AGENT_TEAM_HANDOFF.json` has a
defined schema and checker. With Beads selected, `plan.tasks` contains existing
IDs; Agent-Team verifies each in the target database and adopts them without
an import. A selected `TASKS.md` follows the separate approved dry-run/import
procedure. Beads then becomes the sole live tracker.

Lanes has no defined importer for that JSON. Its orchestrator reads the
approved documents and current tracker, triages tasks, and turns the task scope
into a bounded brief with exact owned paths. It also supplies token limits and
a stop condition. Kickoff estimates inform the tier; they do not assign it.
The ownership formats differ too: kickoff JSON uses `directory/**`, while
Lanes' `owned.txt` uses `directory/`.

I would choose Agent-Team for native host coordination around Beads, and Lanes
when explicit model tiers and scripted integration are wanted. Keep one
orchestrator responsible for each task, and reconcile unfinished work before
changing workflows.

## Evidence and limits

The comparison uses these local skill sources:

- Agent-Team: `/home/server/.agents/skills/agent-team/SKILL.md`, plus
  `references/HOSTS.md`, `references/WORKER_RULES.md`, and `references/STATE.md`.
- Lanes: `/home/server/.codex/skills/lanes/SKILL.md`, plus `CODEX.md` and
  `rules/brief-template.md`.
- Project Kickoff: [artifact contracts](../references/artifacts.md),
  [setup](../references/setup.md), [handoff and cleanup](../references/handoff.md),
  and the [plan template](../assets/templates/PLAN.md).

Project Kickoff's 0.6.0/Agent-Team 9.0.0 checker result is
`schema-valid-unverified`, with `runtimeVerified: false`. Lanes compatibility
here follows from its documented inputs; Project Kickoff has no Lanes handoff
schema or runtime acceptance test. A real host run is still needed to prove
execution for either route.
