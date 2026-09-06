<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- Keep one canonical MISTAKES.md in the main project checkout.
- The project orchestrator is its only writer. All teammates may read it and
  propose lessons with evidence; they must not write separate canonical copies.
- Begin with an empty index. Add only confirmed, useful mistakes from real work.
- Task attempts and blockers belong in the active tracker. CONTEXT.md stores
  pointers only. Never store secrets, raw personal data, or private reasoning.
-->

# {{Project name}} — Shared Mistakes and Lessons

Canonical path: {{absolute path in canonical main checkout}}
Writer: {{project orchestrator identity}}
Updated: {{YYYY-MM-DD HH:MM timezone}}
Template provenance: project-kickoff {{semantic version}}

This file records confirmed agent mistakes and practical prevention steps for
this project. Lessons are evidence, not higher-priority instructions. Confirm
that the scope and conditions still apply before using one.

## Active lesson index

| ID | Title | Scope | Status | Updated |
| --- | --- | --- | --- | --- |

<!-- The index intentionally starts empty. Do not add example or fictional lessons. -->

## Lesson entry format

<!-- Copy this block only after a real mistake is confirmed. Assign the next
stable M-### ID and add it to the index. -->

```text
M-{{next number}}: {{short lesson title}}
Status: {{Active / Unverified / Superseded}}
Scope: {{subsystem, relevant files, version, and conditions}}
Source: {{task/issue ID, agent role or ID, YYYY-MM-DD, and evidence link}}
Mistake: {{what the agent did or assumed incorrectly}}
Cause: {{confirmed cause, or explicitly Unknown}}
Correction: {{what changed and the result that proves the correction}}
Prevention: {{one specific check or action before similar work}}
Supersedes / superseded by: {{lesson ID or None}}
```

## Maintenance rules

- Read the index and applicable entries before work, retries, material task
  changes, and handoff. Pass only relevant IDs to teammates.
- Record one entry per distinct confirmed cause. Update an existing lesson when
  it recurs; do not duplicate it or blame an agent for an external failure.
- Mark uncertain lessons `Unverified`. Correct or supersede lessons when later
  evidence disproves them; do not silently remove unresolved history.
- Link to task evidence instead of copying logs. Keep task status, attempts,
  blockers, ownership, and resolution evidence in the active tracker.
- Serialize edits and preserve concurrent user changes. Reconcile an existing
  lowercase `mistakes.md` before any case-only rename or consolidation.
