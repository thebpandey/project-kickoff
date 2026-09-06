<!--
- The optional context hook reads existing short fields and section labels. Keep
  each phase, status, pending question, and next action value on one line after
  adaptation. Do not add a duplicate hook summary or store secrets in these fields.
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- Keep this checkpoint short, current, and normally under 600 words. Replace
  stale notes instead of appending a diary.
- The project orchestrator alone writes the main CONTEXT.md. Each team/agent
  uses its assigned unique context path and must not overwrite this file.
- Link to the active tracker; do not copy task status or failure history here.
- Never store credentials, raw personal data, private reasoning, or full logs.
-->

# {{Project name}} — Resumption Context

Updated: {{YYYY-MM-DD HH:MM timezone}}
Project / team: {{stable project ID / project-orchestrator or team ID}}
Agent / session: {{owner and attempt/session identity}}
Harness: {{Agent-Team version and applicable instruction paths}}
Kickoff baseline: project-kickoff {{semantic version}}; {{approval/version pointers}}

## Current phase

Phase: {{Discovery stage 1–5 | Approved planning | Setup | Ready for handoff |
Implementation | Verification | Integration | Release | Blocked}}
Phase status: {{In progress | Awaiting answer | Approved | Complete | Blocked}}

## Canonical locations

- Project root / main checkout: {{absolute path}}
- Branch / revision: {{branch and exact revision}}
- Uncommitted changes: {{concise inspected summary or None}}
- Discovery record: {{absolute .project-kickoff/DISCOVERY.md path}}
- Approved baselines: {{PRD/DESIGN/PLAN paths and versions}}
- Existing-project audit: {{absolute AUDIT.md path/version or Not applicable — new project}}
- Active tracker: {{mode and absolute path or identity}}
- Tracker setup receipt: {{absolute .agent-team/setup.json path}}
- Shared lessons: {{absolute MISTAKES.md path, revision, relevant M-IDs or None}}
- Team registry / handoffs: {{paths or Not initialized}}

## Approved decisions needed for resumption

| Decision ID | Essential approved result | Source / approval ID | Affected artifacts |
| --- | --- | --- | --- |
| {{DEC-001}} | {{brief result, not full rationale}} | {{DISCOVERY link}} | {{paths / requirement IDs}} |

Detailed interview answers, evidence, rationale, and approval history remain in
`DISCOVERY.md`; durable product and architecture detail remains in the approved
project documents.

## Evidence and current state

- Relevant revisions: {{feature/integration revision pointers or None}}
- Verification evidence: {{paths, environment identity, matching revision}}
- Dependency state: {{setup receipt pointer and only material exceptions}}
- Owned resources: {{worktrees, processes, previews, locks, or None}}
- Blockers / unresolved decisions: {{OQ/failure IDs and pointer, or None}}
- Pending question: {{exact DISCOVERY question ID or None}}
- Pending external operation: {{intent, target, approval/operation identity, or None}}

## Next action

{{One executable action. If awaiting a user answer, state the exact question ID
and do no dependent work. If resuming execution, state the task ID and required
pre-checks of Git state, ownership, approval, and external operation status.}}

Refresh this checkpoint at major milestones, before handoff or compaction, and
before eligible worktree cleanup. Old labels are not proof of completion; verify
the files, revisions, tracker, ownership, approvals, and external state.
