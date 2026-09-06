# Tracker seeding, handoff, and cleanup

## Seed one tracker idempotently

Seed only after `PLAN.md` is approved and the user selected the tracker. The
tracker is authoritative for execution status; `PLAN.md` remains authoritative
for the approved task definitions and acceptance criteria.

1. Read the approved plan revision and every stable plan ID. New plans use
   `EPIC-###`, `STORY-###`, and `TASK-###`; existing projects keep their
   established IDs and prefixes. Read the active tracker and
   `.agent-team/setup.json`. Inspect existing tracker records before any create.
2. For each plan ID, resolve a tracker item from the saved mapping or the
   tracker's stored plan-ID field. If exactly one exists, update its definition
   only when needed. If more than one exists, stop that item and reconcile the
   duplicate. If none exists, create one. Create parents before their children
   when the tracker supports hierarchy. Otherwise keep explicit parent mappings.
3. After each successful create, immediately persist that epic, story, or task's
   stable plan ID to tracker-ID mapping. A failure leaves a valid partial seed
   that the next run resumes.
4. After all nodes exist, add or verify parent-child relationships. Then add or
   verify blocker edges separately. Do not use hierarchy as a blocker, reverse
   blocker direction, or create self-links or cycles.
5. Verify every runnable first-release plan node maps exactly once, every
   requirement has coverage, each story and task has the intended parent, and
   roadmap-only ideas are absent from the runnable queue. Record the seeded plan
   revision.

Never delete and recreate the tracker to recover from partial setup. Never use a
second tracker as a staging ledger. Preserve unknown items and user changes. If
the selected tracker becomes unavailable, record the blocker and ask the user to
select a researched fallback before activation.

When the selected Beads version provides external references, metadata, or spec
IDs, store each stable epic, story, and task plan identity there and in the setup
receipt. Preserve existing project IDs even when their prefixes differ from this
Skill's convention. Discover the installed dependency command's argument
direction before adding each edge; do not infer it from prose. Use the selected
executable's absolute path during setup when more than one `bd` is installed.

## Scaffold execution and integration

Keep the canonical planning checkout for the project orchestrator's planning,
tracker, discovery, context, and shared-record updates. For a new repository,
this uses `main`. For an existing repository, it uses the user-designated
integration branch without renaming it. After the approved planning commit exists:

1. Create a task branch and worktree from the verified canonical integration
   revision for the minimal scaffold. Record its path, owner, base, and task IDs.
2. Delegate all scaffold code, configuration, builds, tests, and executable
   helpers to that worktree. Give the worker approved artifacts, relevant
   decisions, task IDs, boundaries, and checks. Preserve user work.
3. Require a handoff with exact commit, changed paths, requirement/task coverage,
   checks and environment, remaining limits, and context or mistake pointers.
4. Combine the branch in one project integration worktree. Verify the integrated
   revision, then update the canonical integration branch through the authorized
   project process. Do not merge directories or let a feature worker update that
   branch.

Use installed Agent-Team procedures for the subsequent implementation run.
Kickoff supplies the approved documents, selected tracker and mapping, setup
receipt, project instructions, first ready task when implementation remains, and
exact host invocation. For a healthy completed existing project, it can instead
supply evidence that no implementation work remains. It also records the
generating `project-kickoff` metadata version and any resolved compatibility note.
It does not start Agent-Team or implement the first feature.

## Readiness gate

Declare `ready for handoff` only when:

- all five stage approvals are current and no implementation-blocking decision
  remains unresolved;
- PRD, DESIGN, and PLAN agree on first-release scope, stack, architecture,
  requirement IDs, and acceptance criteria;
- the scaffold matches approved scope and its actual checks pass;
- dependency receipt statuses are factual and required capabilities are ready;
- exactly one tracker is active, mappings are complete, dependencies are acyclic,
  and the first actionable task is known, or audit evidence establishes that no
  implementation work remains;
- AGENTS, CLAUDE, MISTAKES, CONTEXT, discovery, and tracker ownership agree;
- no roadmap item was activated and no feature implementation began.

At completed handoff, disable the optional saved-context loader marker through
the manual maintenance flow in [the project hook guide](context-hook.md). Keep
the guard and advisory within their recorded activation scope. Keep checkpoint
files for manual resumption. Do not remove unrelated host hooks.

Report any deferred optional tool separately. A failed install is not Ready.

## Cleanup after verified integration

Cleanup is triggered by verified integration into the canonical integration
branch. Production deployment is a separate decision and does not delay this
project rule.

For each task-owned worktree, verify the integrated revision by ancestry. For a
squash or rewritten integration, compare the exact source diff or patch identity
and record that evidence. Then stop only task-owned processes, preserve required
logs and resumption evidence outside the disposable checkout, and inspect tracked,
untracked, and ignored files. Unknown files, local data, secrets, and unfinished
changes must be retained and reported.

Remove only clean, fully integrated worktrees through normal Git worktree
commands. Do not force removal. Delete only the corresponding verified integrated
task branches. Preserve the canonical branch, unrelated branches and worktrees,
unintegrated or uncertain work, user changes, and required evidence. Reuse at
most one integration worktree while needed; remove it when clean and idle. Record
removed and retained resources with reasons.
