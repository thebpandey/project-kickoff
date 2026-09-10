<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- This is the common project policy for every supported host and every agent.
- Replace every {{...}} value and remove inapplicable optional rules only after
  recording the approved choice. Keep CLAUDE.md as a thin host adapter.
- Repository instructions remain below system, developer, platform, and tool
  controls. When rules conflict at the same level, use the more specific rule.
-->

# Agent instructions for {{Project name}}

Policy baseline: project-kickoff {{semantic version}}; generated {{YYYY-MM-DD}};
approved by {{approval ID / source}}.

## Source of truth and scope

Read these files before changing the project:

1. `PRD.md` — approved product requirements and technical decisions.
2. `DESIGN.md` — approved experience contract where relevant.
3. `PLAN.md` — immutable-ID implementation baseline for the first release.
4. `{{canonical tracker path or identity}}` — live execution status.
5. `MISTAKES.md` — applicable confirmed lessons.
6. `CONTEXT.md` or the assigned team context — current resumption pointers.

Project decisions recorded with approval take precedence over conflicting
preferences in optional skills or dependencies, subject to higher-priority
system, platform, tool, and organization controls. Preserve unknown files,
unrelated user changes, unfinished work, and required evidence.

The first release is bounded by the approved PRD and PLAN. Do not promote future
roadmap items, add product scope, invent decisions, or relax acceptance criteria.

## Decisions and communication

All project and team orchestrators follow this rule during discovery, approval,
setup choices, preview gates, and other user decisions:

1. Ask one focused question at a time.
2. Offer two or three useful choices when possible. Put the recommended choice
   first and explain its concrete trade-off.
3. Wait for the user's explicit answer before dependent work. Elapsed time,
   silence, prior approval of a different version, or partial progress is not an
   answer or approval.
4. Record material decisions with stable IDs, source, date, status, and affected
   artifacts in `.project-kickoff/DISCOVERY.md`.
5. If a decision changes, invalidate only affected approvals and derived files;
   preserve unrelated approved decisions.

Challenge weak assumptions with evidence and a practical alternative. Label
facts, inferences, assumptions, and open questions. Use concise ASD-STE100-style
communication: write short, active sentences; put one instruction in each
sentence; use approved terms consistently; explain technical words at first use;
and preserve official names and commands. Apply an authorized formal ASD
standard when it is available and required. Never certify ASD-STE100 compliance
without the applicable licensed standard and a verified compliance process.

## Dependencies and skills

Use this approved dependency map. Fill it from the verified setup receipt; a
named dependency is not proof that it is installed or relevant.

| Capability | Selected dependency / mode | Use when | Verified source / version / path | Receipt pointer |
| --- | --- | --- | --- | --- |
| Simplicity review | {{Ponytail / built-in simple-code guidance / skipped}} | {{implementation/review tasks where reducing unnecessary complexity helps}} | {{actual installed source/version/path or Unavailable}} | {{setup.json field}} |
| Skill routing and process | {{Using-Superpowers / built-in project policy / skipped}} | {{resolving and applying relevant installed skills}} | {{actual source/version/path or Unavailable}} | {{setup.json field}} |
| Task tracking | {{Beads / root TASKS.md / approved alternative}} | {{all live execution status and evidence}} | {{actual source/version/path or canonical tracker location}} | {{setup.json field}} |
| Orchestration | {{Agent-Team / selected approved orchestrator}} | {{implementation handoff and execution}} | {{actual source/version/path or Unavailable}} | {{setup.json field}} |
| UI quality | {{Impeccable / built-in UI guidance / skipped}} | {{only projects/tasks with a relevant visual UI}} | {{actual source/version/path or Unavailable}} | {{setup.json field}} |
| UI/UX reference | {{UI UX Pro Max Skill / selected alternative / skipped}} | {{only concrete visual UI/UX research or design tasks}} | {{actual source/version/path or Unavailable}} | {{setup.json field}} |

Before Agent-Team initializes the project, follow the selected mode in this
table, `.project-kickoff/setup.json`, and the validated
`.project-kickoff/AGENT_TEAM_HANDOFF.json`. After initialization, Agent-Team owns
`.agent-team/setup.json`; treat it as the runtime receipt. If the records
disagree, stop dependent work and have the project orchestrator reconcile them
from the user's recorded choice.

- Inspect the actual runtime, repository, installed commands, and available
  skills before selecting a method. A directory or downloaded package alone is
  not proof that a dependency works.
- Resolve the actual installed name and read the relevant skill instructions
  before invoking a skill. Use a skill only when it applies to the task. For
  example, do not invoke visual UI skills for a backend-only change.
- Reuse compatible project-scoped installations. Do not mutate global host,
  user, editor, shell, package-manager, or credential configuration.
- Use project-scoped setup when the tool supports it. Explain any dependency
  that can only be installed or configured at user scope and wait for the
  user's choice before that mutation.
- For missing or unusable dependencies, continue independent work. Present
  verified current alternatives and trade-offs, then ask one question and wait
  before adopting a substitute. Never report an unavailable or failed install
  as ready.
- Keep one authoritative task tracker. Use the choice recorded in
  `.project-kickoff/setup.json` before initialization and the Agent-Team runtime
  receipt afterward. Do not switch automatically if another tool appears.

Do not store or print credentials. Use example environment-variable names only
when selected tooling needs them.

## Execution and delegation

The project orchestrator owns planning, coordination, shared records,
integration, and release decisions. It may read and update approved planning
files and the canonical tracker in the canonical main checkout.

All package installation, scaffold source/configuration changes, product code,
builds, tests, executable helper work, and implementation repairs must run
through a subagent whose model and reasoning effort fit the task's actual
complexity and host capabilities. Give each subagent a bounded task, relevant
requirement and lesson IDs, acceptance criteria, owned paths, and expected
evidence. Developers, reviewers, and testers do not spawn their own agents. If
delegation is unavailable, finish planning and ask for an explicit exception or
the missing capability before executing code or installation work.

Use the strongest available orchestrator configuration for cross-project
reasoning. Use routine capacity for bounded, low-risk tasks; standard capacity
for substantive implementation; complex capacity for intertwined architecture,
ambiguous failures, migrations, security boundaries, or other difficult work.
Do not claim a requested model or effort was used unless the host exposed it.

Use only the parallelism that independent work supports. Assign one
implementation owner to each task. Serialize overlapping paths, unresolved
contracts, shared environments, tracker writes, integration, and release work.

## Git and worktrees

- Detect the actual Git repository, common directory, canonical main checkout,
  branch, and existing worktrees before initialization. "Canonical main" means
  the selected primary checkout and its actual branch name; it does not require
  a branch named `main`. Audit first. Do not create or rename a branch, adopt an
  unrelated ancestor repository, or overwrite an existing project during audit.
- Keep the canonical main checkout for planning, user discussion, and shared
  records. After the approved planning commit, do feature code, tests, feature
  documentation, scaffold work, and repairs in task-specific worktrees.
- Create feature branches from an identified revision. Record the task ID,
  branch, worktree, owner, base revision, and owned resources. Preserve existing
  edits and follow repository commit and branch-protection rules.
- Use one reusable integration worktree. Merge feature branches serially there,
  verify the combined revision, and update main only through the authorized
  repository process. Feature agents do not merge directly into main.
- For squash integration, record the tested source revision and diff evidence;
  ancestry alone does not prove integration.

Do not force-reset, force-remove, or discard unknown content to simplify
cleanup. Do not treat worktrees as isolation for databases, ports, services,
credentials, caches, or other external resources.

## Tracking and shared records

`PLAN.md` owns the approved task definitions and stable `TASK-###` IDs. The
tracker selected in `.project-kickoff/setup.json`, then recorded by Agent-Team
in `.agent-team/setup.json`, owns claims, dependencies, current
status, failure attempts, evidence, releases, and cleanup. Seed or reconcile by
stable ID; repeated setup must not create duplicate tasks. Future roadmap ideas
must not become active tasks without approved scope and plan changes.

Shared project records have one writer: the project orchestrator alone updates
the canonical local `TASKS.md`, `.agent-team/TEAMS.md`, main `CONTEXT.md`, and
`MISTAKES.md`. Teammates send task ID, revision, evidence, blocker, and next
action through the host message channel or a unique handoff file. They maintain
only their assigned context path. Direct tracker updates by teammates are
allowed only when the selected tracker and recorded ownership policy explicitly
support concurrent writes.

Update the active tracker at claim, meaningful progress, blocker, handoff,
verification, integration, release, and cleanup transitions. Keep attempt
history in the tracker, reusable confirmed lessons in `MISTAKES.md`, and concise
resumption pointers in `CONTEXT.md`. Never copy the same ledger into all three.

## Implementation and verification

- Claim a ready task and inspect existing code and conventions before editing.
- Implement the smallest complete change that meets linked requirements. Reuse
  existing utilities and dependencies when suitable.
- Verify changed behavior, relevant failure paths, and affected integration
  points in the environment named by the task. A stale or unrun check is not a
  pass. After a fix, rerun the failed check and affected behavior.
- For substantive work, obtain independent review of the relevant diff and
  evidence. Always independently review authorization, payment, schema, and
  destructive data changes.
- Report exact revisions and durable evidence. Distinguish implemented,
  reviewed, verified, integrated, deployed, deferred, and blocked work.
- After two attempts without useful progress, change strategy or assign the
  complex developer. If the changed approach also cannot progress, ask one
  focused question and continue unrelated ready work.

Do not delete tests, reduce required checks, or rewrite acceptance criteria to
create a passing result. Record meaningful failures by distinct cause in the
active tracker; do not turn routine typos or expected empty searches into issues.

## Integration and cleanup

Before integration, confirm the exact feature revision, requirement/task
coverage, current approval gate, relevant checks, shared-record pointers, and
unresolved limits. Verify the combined branch in the integration worktree and
confirm main still matches the tested base before updating it.

Immediately after verified integration into main:

1. Record the exact integration boundary and verification evidence.
2. Stop task-owned processes and inspect tracked, untracked, and ignored content.
3. Preserve required evidence and recover uncertain or uncommitted files.
4. Remove only clean, eligible task worktrees through normal Git worktree
   removal. Delete only branches proven integrated by ancestry or recorded
   squash revision/diff evidence.
5. Preserve main, unfinished or paused work, unrelated branches, user changes,
   active resources, and anything whose ownership or integration is uncertain.
6. Remove the clean idle integration worktree when no queued integration needs
   it; keep at most one while it is useful.
7. Record removed and retained resources, with the reason for each retention.

This cleanup follows verified integration. A production deployment or
production verification is a separate decision and is not a cleanup gate for
this project. Never deploy as a side effect of preparation, integration, or
cleanup. Follow the established release authority and user approval gates.

## Handoff format

Each implementation handoff includes:

- project/team and task/requirement IDs;
- branch, worktree, base revision, and exact changed revision;
- changed paths and resulting behavior;
- commands/checks actually run, environment, results, and evidence locations;
- dependency or configuration effects;
- applicable mistake IDs and any proposed lesson with evidence;
- open risks, blockers, approval state, and one next action;
- owned processes, previews, worktrees, or other resources needing cleanup.

The final project handoff reconciles every first-release requirement to evidence,
states tracker and setup locations, names the validated
`.project-kickoff/AGENT_TEAM_HANDOFF.json`, identifies the first actionable task
or blocker, and gives the exact host invocation. Preparing a handoff does not
create `.agent-team/setup.json` or start an Agent-Team run.
