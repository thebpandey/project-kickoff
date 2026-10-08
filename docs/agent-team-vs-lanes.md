# Agent-Team and Lanes: shared planning, different execution

Agent-Team v9 keeps coordination inside the active host session, using Beads
for task state and Git for revisions. Lanes adds an installed orchestration
harness with model routing and scripts for integration. Both can use Project
Kickoff's approved documents. Their runtime records belong to each skill.

This comparison checks Agent-Team 9.0.0, the installed Lanes 0.2.0 package
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

## Efficiency depends on the workload

Lanes has the stronger design for reducing model cost and token use.
Agent-Team has the stronger design for keeping setup and coordination simple.
This is an inference from their contracts, not a measured benchmark.

| Efficiency measure | Likely advantage | Reason |
| --- | --- | --- |
| Model cost | Lanes | Explicit tiers route bounded routine work to cheaper workers and reserve stronger models for complex tasks. Agent-Team also allows cheaper available models through task preferences. |
| Token use | Lanes | Task budgets, compact reports, completion notifications, and a usage ledger make consumption explicit. Agent-Team also limits its ready page to 20 rows and can retain useful worker context. |
| Small documentation changes | Lanes | Its narrow TRIVIAL classification skips independent review. Agent-Team requires review before every integration. |
| Setup effort | Agent-Team | Git, Beads, and native host agents are sufficient. Lanes adds a harness and tooling for the selected routes. |
| Coordination overhead | Agent-Team | Beads and Git own task and revision state, with fewer supporting runtime records to maintain. |
| Completion speed | Unproven | Worker quality and fix rounds can outweigh savings from model routing or fewer review steps. Neither workflow was benchmarked here. |

For sustained work with many routine tasks, I would choose Lanes to control
running costs. Its usage ledger gives you something to check. For occasional
work in an existing Beads project, Agent-Team's smaller setup is easier to
justify.

Measure cost per accepted task, including fixes and reviews. Record elapsed
time too. A cheaper first attempt that needs several repairs may cost more than
a stronger worker completing the same task once.

## Choosing by project size

I would usually choose Lanes for a long, complex project with an elaborate
implementation plan. Its task tiers and usage records help manage a large
backlog over several sessions. Scripted integration adds a consistent process
as more tasks finish.

For a quick, small project with a simple plan, I would usually choose
Agent-Team, especially when Beads is already in place. Its smaller setup means
less preparation before the first task. If Lanes is already installed or the
project uses another tracker, Lanes may be the easier choice even for a small
job.

Both can handle either project size. They are alternatives, but switching
requires preparation: reconcile the live tracker and unfinished worktrees,
then follow the new skill's review and resume rules. Their runtime records and
handoff formats are different. An elaborate plan also works with Agent-Team
when its tasks have clear boundaries and dependencies; project size alone
does not force a particular skill.

## Scenarios that favor each skill

These are examples of workloads, not results from observed runs. They assume
the selected skill and its required host capabilities are available.

| Scenario | Preferred skill | Why |
| --- | --- | --- |
| A Beads project needs two contained bug fixes in the current session. | Agent-Team | It can select bounded ready work and dispatch native agents with little extra setup. Each fix still receives independent review. |
| Kickoff has produced a validated Agent-Team handoff with existing Beads IDs. | Agent-Team | It has a defined adoption procedure that verifies those IDs in the target database. Lanes would prepare its own briefs from the documents. |
| A backlog has many independent routine edits and a few difficult tasks. | Lanes | Tiers make the model choice explicit for each task, while budgets and usage records support cost comparisons. Harder tasks can move upward in tier. |
| A README needs a prose-only addition of at most 40 lines, with no deletions or changes to instruction, control, or legal files. | Lanes | The classifier can identify TRIVIAL work and skip independent review. The integration script still checks the scope and classification. |
| An established project tracks work in a Markdown file and wants to keep that convention. | Lanes | It follows the existing tracker. Agent-Team requires Beads and treats Markdown tasks as an approved one-time import source. |
| Project policy permits execution only through the current host's approved native agent facilities. | Agent-Team | Native dispatch is its required route. Lanes has native routes too, but its relay options require separate policy decisions. The host still needs to meet the project's data rules. |
| A multi-session project needs fresh workers to continue checkpointed work in preserved worktrees after a restart. | Lanes | It explicitly supports new subagents in those worktrees and reattachment to relay jobs. Reconcile unfinished work and any still-running processes first. Agent-Team preserves uncertain earlier launches until original host evidence permits action. |

## Agent-Team dependencies and aids

Required means the workflow needs the item. Optional means it is used for a
specific task or chosen route. Recommended means useful guidance with an
optional installation. A conditional requirement applies only when its named
operation is used. Project build and test tools are additional dependencies
determined by the actual project.

Agent-Team's project prerequisites are Git and Beads. Execution also requires
a supported host with observable native agents and independent review.
Its [v9 skill](https://github.com/thebpandey/agent-team/blob/v9.0.0/SKILL.md)
defines the boundary; optional aids never determine readiness.

| Status | Name | GitHub repository | What it does and when it is needed |
| --- | --- | --- | --- |
| Required | Git | [git/git](https://github.com/git/git) | Tracks revisions and supplies isolated worktrees. Needed for task development and verified integration. |
| Required | Beads (`bd`) | [gastownhall/beads](https://github.com/gastownhall/beads) | Owns live task state and dependencies. Needed for ready-work selection, claims, and closure. Initialization requires approval. |
| Required, choose a supported host | Codex or Claude Code native agent facilities | [openai/codex](https://github.com/openai/codex), [anthropics/claude-code](https://github.com/anthropics/claude-code) | Launches observable workers and independent reviewers. The running host must expose the required native tools; a CLI installation alone does not prove that capability. |
| Recommended; package optional | Ponytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Guides the smallest working implementation. Agent-Team applies that discipline even without the package and uses the skill when available. |
| Optional | Project Kickoff | [thebpandey/project-kickoff](https://github.com/thebpandey/project-kickoff) | Supplies approved plans and an optional handoff. Useful before implementation; never a setup requirement. |
| Optional | Serena | [oraios/serena](https://github.com/oraios/serena) | Provides semantic code navigation and scoped editing when those operations benefit a task. Native search and editing remain fallbacks. |
| Optional | Graphify | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Builds a queryable repository graph. Useful for a specific structure or relationship question. |
| Optional | Playwright | [microsoft/playwright](https://github.com/microsoft/playwright) | Automates browsers for task-specific verification of web behavior. |

Agent-Team also allows installed visual skills when a task needs visual work.
It names no required visual package. LeanCTX is explicitly excluded from this
workflow. Agent-Team v9 has no separate controller or mandatory hook package.

## Lanes dependencies and aids

Lanes has more supporting tooling. The
[installer](https://github.com/thebpandey/lanes/blob/0f82a46898e6848f48b7d53555854b357d94f14c/install.sh)
checks the machine prerequisites; the
[Codex adapter](https://github.com/thebpandey/lanes/blob/0f82a46898e6848f48b7d53555854b357d94f14c/CODEX.md)
defines the Codex review route. The installer marks Claude Code as required and
reports both provider keys even when you intend to use another route. Each
external relay actually needs its own configured provider key.

| Status | Name | GitHub repository | What it does and when it is needed |
| --- | --- | --- | --- |
| Required | Lanes harness | [thebpandey/lanes](https://github.com/thebpandey/lanes) | Bundles worktree helpers, scope checking, integration, and relay launchers such as `model-relay` and `codex-review`. These scripts belong to Lanes. |
| Required | Git | [git/git](https://github.com/git/git) | Supplies task branches and linked worktrees, plus the revision evidence used during review and integration. |
| Required | Bash | [GNU Bash mirror](https://github.com/gnu-mirror-unofficial/bash) | Runs installation and lane shell scripts. This GitHub link is an unofficial mirror, not the GNU upstream. |
| Required | Python 3 | [python/cpython](https://github.com/python/cpython) | Runs the bundled relay process launcher, parses provider results, and supports deterministic checks. |
| Required | curl | [curl/curl](https://github.com/curl/curl) | Performs the installer's HTTP checks for configured provider credentials. |
| Required, compatible host utilities | Unix core utilities | [coreutils/coreutils](https://github.com/coreutils/coreutils) | Supplies file and path operations used by the scripts, including `mktemp` and `readlink`. This is the GNU implementation; the host must supply compatible commands. |
| Required by installer and Claude/provider routes | Claude Code | [anthropics/claude-code](https://github.com/anthropics/claude-code) | Runs Claude workers and the Claude-based DeepSeek/GLM relays. Installed Claude agent definitions load after a host restart. |
| Required for Codex-hosted review; optional on Claude route | Codex CLI | [openai/codex](https://github.com/openai/codex) | Runs `codex-review` for an independent revision-bound review. Claude uses its lane-reviewer agent instead. |
| Required before any push | Gitleaks | [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | Scans the outgoing commit range for secrets. Lanes' pre-push script blocks when the scanner is absent or fails. |
| Required before context compaction | Session Detail skill | [thebpandey/session-detail](https://github.com/thebpandey/session-detail) | Produces full and incremental session archives for recovery. Lanes requires an archive saved before compaction. |
| Optional; use when it is the project tracker | Beads (`bd`) | [gastownhall/beads](https://github.com/gastownhall/beads) | Tracks ready work and dependencies. Lanes can follow an existing alternative tracker. |
| Optional; needed for tasks using disposable containers | Docker | [docker/cli](https://github.com/docker/cli), [moby/moby](https://github.com/moby/moby) | Runs task-owned test databases or services. It is needed when the task's verification uses those containers. |
| Optional, Linux watchdog timer | systemd | [systemd/systemd](https://github.com/systemd/systemd) | Schedules the bundled watchdog when the user timer is installed. It does not provide worker dispatch or task state. |
| Recommended for elaborate new plans; optional | Project Kickoff | [thebpandey/project-kickoff](https://github.com/thebpandey/project-kickoff) | Provides approved scope and task definitions before lane triage. This recommendation is this report's judgment, not a Lanes prerequisite. |

The external worker providers are service dependencies. Their runtime APIs
have no standalone source repository identified by the Lanes package, so the
GitHub links here point to the actual bundled integrations.

| Status | Name | GitHub integration source | What it does and when it is needed |
| --- | --- | --- | --- |
| Optional route; required when selected | DeepSeek API and `DEEPSEEK_API_KEY` | [Lanes DeepSeek configuration](https://github.com/thebpandey/lanes/blob/0f82a46898e6848f48b7d53555854b357d94f14c/config/deepseek.json) | Supplies the external DeepSeek worker for bounded routine work. Requires a configured key for the [DeepSeek platform](https://platform.deepseek.com/). A model repository would not supply this service. |
| Optional route; required when selected | GLM through OpenRouter and `OPENROUTER_API_KEY` | [Lanes GLM configuration](https://github.com/thebpandey/lanes/blob/0f82a46898e6848f48b7d53555854b357d94f14c/config/glm.json) | Supplies the external GLM worker through the [OpenRouter API](https://openrouter.ai/docs/quickstart). Requires its provider key; a separate Z.ai SDK is not a packaged requirement. |

Both skills rely on whatever build and test tools the project itself needs.
Neither dependency table is a promise that its model routes or review tools
were exercised in this comparison.

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
- Lanes: `/home/server/.codex/skills/lanes/SKILL.md`, plus `CODEX.md`,
  `rules/brief-template.md`, `VERSION`, `README.md`, and `install.sh`. Provider
  requirements also use the bundled routing configuration and relay scripts.
- Project Kickoff: [artifact contracts](../references/artifacts.md),
  [setup](../references/setup.md), [handoff and cleanup](../references/handoff.md),
  and the [plan template](../assets/templates/PLAN.md).

Project Kickoff's 0.6.0/Agent-Team 9.0.0 checker result is
`schema-valid-unverified`, with `runtimeVerified: false`. Lanes compatibility
here follows from its documented inputs; Project Kickoff has no Lanes handoff
schema or runtime acceptance test. A real host run is still needed to prove
execution for either route.
