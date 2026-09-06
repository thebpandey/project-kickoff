<!--
TEMPLATE INSTRUCTIONS — use only for an existing project. Remove this comment
after adapting the document.
- Audit before proposing a retrofit. Preserve current project truth, unknown
  files, user changes, IDs, Git history, approvals, and evidence.
- Every finding needs a path/revision and must say whether behavior was tested.
  Do not call a superficial scan comprehensive.
- Recommendations are not approved changes. Do not edit product code or seed
  implementation tasks until the user approves the relevant target change.
-->

# {{Project name}} — Existing Project Audit

Status: {{In progress | Awaiting decisions | Approved baseline | Superseded}}
Version: {{document version}}
Updated: {{YYYY-MM-DD HH:MM timezone}}
Auditor / host: {{agent identity and actual host}}
Scope: {{directories, documents, runtime behavior, and exclusions inspected}}
Base revision: {{Git revision and worktree state}}
Generated with: project-kickoff {{semantic version}}
Audit depth: {{Inventory | Focused audit | Tested audit}} — {{practical limits}}

## Entry decision and boundary

- User-selected path: {{Audit then guided approved planning/setup/tracker retrofit | Other approved path | Pending}}
- Decision source / date: {{DEC/ANS ID, message, YYYY-MM-DD}}
- Code-change boundary: Audit and planning only; approved product code changes
  are mapped to `PLAN.md` and executed later by agent-team.
- Preservation boundary: {{existing docs, IDs, user changes, history, data,
  branches, worktrees, generated evidence, or other protected state}}

## Current project state

### Repository and ownership

| Concern | Observed current state | Evidence path / revision | Confidence / limits |
| --- | --- | --- | --- |
| Repository root and main checkout | {{actual paths and branch}} | {{git command/result pointer and revision}} | {{High/Medium/Low and why}} |
| Worktrees and branches | {{active/unknown ownership and dirty state}} | {{evidence}} | {{confidence/limits}} |
| Shared-record ownership | {{instructions, tracker, context, lessons writers}} | {{paths/revision}} | {{confidence/limits}} |
| Uncommitted / unknown files | {{preservation summary}} | {{status evidence}} | {{confidence/limits}} |

### Architecture, stack, and operations

| Area | Observed current state | Evidence path / revision | Test state | Confidence / limits |
| --- | --- | --- | --- | --- |
| System boundary / components | {{observed architecture}} | {{paths and revision}} | {{run-pass / run-fail / blocked / not-run}} — {{check/result}} | {{confidence/limits}} |
| Stack / dependencies | {{manifest and installed state}} | {{paths, versions, lockfiles}} | {{run-pass / run-fail / blocked / not-run}} — {{check/result}} | {{confidence/limits}} |
| Data / integrations | {{ownership, schemas, external systems}} | {{paths/revision}} | {{run-pass / run-fail / blocked / not-run}} — {{check/result}} | {{confidence/limits}} |
| Security / configuration | {{observed controls and unknowns; no secret values}} | {{paths/revision}} | {{run-pass / run-fail / blocked / not-run}} — {{check/result}} | {{confidence/limits}} |
| Build / test / deployment | {{documented and observed commands/pipelines}} | {{paths/revision}} | {{run-pass / run-fail / blocked / not-run}} — {{what actually ran}} | {{confidence/limits}} |

### Architecture comparison

| Area | Current observed state | Current documented state | Approved target | Gap / preservation need | Evidence / decision |
| --- | --- | --- | --- | --- | --- |
| {{component, boundary, data flow, stack, or operation}} | {{observed code/runtime state or Unverified}} | {{existing document claim or Undocumented}} | {{approved target or Pending}} | {{difference, explicit preservation, or Unknown}} | {{path/revision/AUD/DEC/APR IDs}} |

### Product, design, and documentation

| Artifact / concern | Current documented intent | Observed code or behavior | Evidence | Status |
| --- | --- | --- | --- | --- |
| {{requirement, flow, design, README, runbook, etc.}} | {{document claim or Unknown}} | {{observed implementation or Unverified}} | {{path/revision/test}} | {{Aligned / Drift / Missing docs / Missing implementation / Unverified}} |

### Agent and tracker state

| Concern | Current state | Evidence | Preserve / reconcile need |
| --- | --- | --- | --- |
| Instruction files | {{AGENTS/CLAUDE/other policy and precedence}} | {{paths/revision}} | {{content to preserve or conflict to decide}} |
| Requirements / plan IDs | {{ID schemes and references}} | {{paths/revision}} | {{reuse or explicit mapping needed}} |
| Active tracker | {{mode, canonical location, status}} | {{receipt/path/tool evidence}} | {{single-authority or migration issue}} |
| Context / lessons / team registry | {{locations and writers}} | {{paths/revision}} | {{ownership or merge need}} |

## Findings

Use stable `AUD-###` IDs. Severity describes impact if unresolved; priority
describes recommended ordering. Confidence reflects evidence quality.

### AUD-001 — {{finding title}}

- Category: {{product | architecture | code | design | documentation | testing |
  security | operations | Git | agent policy | tracking}}
- Current state: {{specific observed fact}}
- Expected / documented state: {{source requirement or Unknown}}
- Gap / discrepancy: {{difference, or None — informational finding}}
- Evidence: {{path and line if stable, exact revision, command/output pointer}}
- Test state: {{run-pass | run-fail | blocked | not-run}} — {{method,
  environment, and result or reason it was not run}}
- Severity: {{Critical | High | Medium | Low | Informational}} — {{impact basis}}
- Priority: {{Now | First release | Later | No action}}
- Confidence: {{High | Medium | Low}} — {{why}}
- Impact: {{user, system, delivery, security, or maintenance consequence}}
- Recommended decision / action: {{preserve, investigate, document, reconcile,
  or change, including the concrete trade-off}}
- Decision needed: {{DEC/OQ ID or None}}
- Affected requirements / tasks: {{existing IDs, proposed mapping, or None}}

Do not describe an inferred cause as confirmed. If behavior was not executed,
state that the finding is based on static inspection. Use `Critical` or `High`
only when evidence supports the impact.

## Current-to-target decisions

| Decision ID | Area | Current state / finding IDs | Proposed target | Recommendation and trade-off | User decision / source | Status |
| --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | {{area}} | {{AUD IDs and existing artifact version}} | {{target state}} | {{Preserve / Change / Investigate, with reason}} | {{answer/approval/date or Pending}} | {{Proposed / Approved / Rejected / Superseded}} |

An inference remains an assumption until approved or verified. Preserve decisions
that keep current behavior as explicitly as decisions that change it.

## Document and ID reconciliation

| Existing artifact / ID | Current meaning and history | Approved target artifact / ID | Action | Approval / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| {{path, REQ/TASK/decision ID}} | {{current definition and last approved baseline}} | {{same ID or mapped ID}} | {{Preserve / Merge / Deprecate with mapping / Add}} | {{DEC/APR/AUD IDs}} | {{Pending / Approved / Applied}} |

Merge generated sections around useful existing content. Do not replace an
existing document wholesale merely because its format differs. Preserve prior
approved versions and Git history. Record old-to-new mappings before changing
referenced IDs or tracker tasks.

## Approved retrofit mapping

| Approved decision / finding | Requirement ID | PLAN task ID | Intended outcome | Dependency | Tracker mapping | Status |
| --- | --- | --- | --- | --- | --- | --- |
| {{DEC/AUD IDs}} | {{existing or new REQ ID}} | {{immutable TASK ID}} | {{approved change or preservation work}} | {{IDs or None}} | {{tracker ID or Pending seeding}} | {{Approved for planning / Seeded / Deferred}} |

Only approved changes appear here. This mapping is a planning handoff, not proof
that code changed. An approved preserve decision or no-remediation finding does
not require a new task; record `None — no implementation work` in the PLAN task
column. Live execution state belongs only in the selected tracker.

## Audit limits and next decision

- Inspected: {{explicit scope}}
- Not inspected / not tested: {{explicit limits}}
- External or unavailable evidence: {{items and effect}}
- Audit completeness claim: {{for example "Focused audit of X; no claim about Y"}}
- Pending question: {{one OQ ID or None}}
- Recommended next action: {{one decision, deeper inspection, or approved
  document retrofit step}}
