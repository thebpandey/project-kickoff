<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- Use this root TASKS.md only when the user selected it as the fallback tracker.
  Record that choice and this absolute path in `.project-kickoff/setup.json` and
  `.project-kickoff/AGENT_TEAM_HANDOFF.json`.
- The project orchestrator is the only writer. Teammates send structured updates.
- PLAN.md owns the approved baseline; this file owns live execution state. Seed
  by immutable PLAN TASK- IDs and never maintain a second writable tracker.
- Preserve existing IDs, evidence, unknown fields, and unrelated user content.
-->

# {{Project name}} — Agent-Team Tasks

Updated: {{YYYY-MM-DD HH:MM timezone}}
Writer: {{project orchestrator identity}}
Tracker mode: local fallback
Canonical path: {{absolute path to root TASKS.md in canonical main checkout}}
Objective: {{approved first-release outcome}}
Plan baseline: {{PLAN.md version, approval ID, and revision}}
Kickoff baseline: project-kickoff {{semantic version}}

## Status rules

Use `ready`, `in_progress`, `blocked`, `verified`, `deployed`, or `deferred`.
`verified` can be terminal when deployment is outside scope. Integration,
deployment, and production verification are separate facts. Only the project
orchestrator changes status, dependencies, ownership, or task closure.
Agent-Team can claim only `ready`, `open`, `todo`, or `pending` tasks. Use
`ready` for a new task whose dependencies are complete.

## Plan-to-tracker mapping

| Plan ID | Tracker ID | Parent | Requirement IDs | Baseline acceptance summary |
| --- | --- | --- | --- | --- |
| TASK-001 | AT-001 | {{EPIC-001 / STORY-001}} | {{REQ-001, NFR-001}} | {{short pointer to PLAN criterion; do not redefine it}} |

This mapping is one-to-one for each runnable first-release task unless a recorded
reason supports a different mapping. Repeated setup must reconcile these IDs and
must not create duplicates. Do not seed future-roadmap ideas.

## Active tasks

| ID | Plan ID / requirements | Intended outcome / acceptance pointer | Owner | Depends on | Status | Revision / evidence | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AT-001 | TASK-001 / REQ-001 | {{PLAN.md task link or concise criterion}} | {{unassigned or one owner}} | {{AT IDs or None}} | {{ready}} | {{None yet}} | {{one actionable step}} |

Dependencies point from a task to its prerequisites. Check for missing IDs and
cycles before claims. A blocked task names the blocker and the independent work,
if any, that can continue.

## Failures

<!-- Add one record per distinct meaningful cause. Append materially different
attempts to the same record. Routine typos and expected empty searches do not
need failure records. -->

### F-{{next number}} — {{short symptom or cause}}

- Tasks / requirements: {{AT/TASK/REQ IDs}}
- Category: {{implementation | verification | environment | deployment |
  permission | tracking}}
- Symptom / reproduction: {{observable behavior}}
- Revision / environment: {{exact identity}}
- Evidence: {{durable pointer}}
- Owner: {{agent/team}}
- Status: {{Open | Resolved}}
- Attempts:
  - {{YYYY-MM-DD — hypothesis; material change; result; learning; next action}}
- Resolution proof: {{evidence or Pending}}
- Related lesson: {{M-### or None; do not copy the lesson here}}

## Integrations, releases, and cleanup

| Event ID | Tasks | Source / integrated revision | Verification / environment | Deployment identity | Cleanup result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| INT-001 | {{AT IDs}} | {{feature revision and main integration boundary}} | {{check/evidence pointer}} | {{Not requested / Pending / provider result}} | {{removed and retained resources with reasons}} | {{Integrated / Deployed / Verified in production / Blocked}} |

Cleanup occurs after verified integration into main and does not wait for
deployment. Preserve unfinished work and uncertain content. For squash merges,
record source revision and diff evidence rather than relying on ancestry.

## Run record

- Run ID / owner: {{ID and project orchestrator}}
- Scope / admitted top-level delivery IDs: {{IDs}}
- Effective user choices and source: {{continuous, preview, deployment batch,
  or built-in defaults with approval/decision pointers}}
- Capacity / occupied slots: {{actual host capacity and task/team pointers}}
- Hold / pause state: {{None or reason}}
- Integration boundaries: {{INT IDs}}
- Pending batch / in-flight operation: {{IDs and exact target, or None}}

## Reconciliation

| Requirement ID | Plan tasks | Final status | Evidence | Approved deferral / unresolved issue |
| --- | --- | --- | --- | --- |
| REQ-001 | TASK-001 / AT-001 | {{ready / verified / deployed / deferred / blocked}} | {{pointer}} | {{approval ID / failure ID / None}} |

At handoff, reconcile every first-release requirement, identify the first ready
task, and save the tracker location and mode in each agent assignment. When
switching trackers by explicit user choice, pause writes, snapshot this file,
transfer IDs, dependencies, failures, and evidence, verify coverage, and mark
this file archived with a pointer. If transfer fails, keep this tracker active.
