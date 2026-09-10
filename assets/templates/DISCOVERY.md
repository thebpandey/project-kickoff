<!--
- The optional context hook reads existing short fields and section labels. Keep
  each phase, status, pending question, and next action value on one line after
  adaptation. Do not add a duplicate hook summary or store secrets in these fields.
TEMPLATE INSTRUCTIONS — copy to .project-kickoff/DISCOVERY.md, then remove this
comment after adapting the document.
- Write this checkpoint from the first question. Ask and record only one pending
  question at a time; a timeout or silence is not an answer.
- Replace every {{...}} value. Preserve prior answers and approvals with source,
  date, status, and affected artifacts. Never invent user decisions or evidence.
- Reuse suitable stable IDs in an existing project. When they do not exist, use
  this template's EV-, ANS-, APR-, DEC-, OQ-, and CHG- prefixes.
- Keep credentials and raw sensitive data out of this file.
-->

# {{Project name}} — Kickoff Discovery Record

Updated: {{YYYY-MM-DD HH:MM timezone}}
Project mode: {{New project | Existing project audit and guided retrofit}}
Kickoff skill version: project-kickoff {{semantic version}}
Current stage: {{1–5 and stage name}}
State: {{Interviewing | Awaiting answer | Awaiting stage approval | Revising |
Approved planning | Setup | Ready for handoff | Blocked}}
Canonical project root: {{absolute path or Pending detection}}

## Sources and evidence

| ID | Claim / information | Source type | Source, date, path / revision | Strength and limits | Affected decisions / artifacts |
| --- | --- | --- | --- | --- | --- |
| EV-001 | {{what is supported}} | {{user answer / repository inspection / product research / authoritative documentation / test}} | {{message/link/path, revision if applicable, YYYY-MM-DD}} | {{direct, inferred, unverified; what was not established}} | {{DEC/OQ IDs and paths}} |

For existing projects, use [`AUDIT.md`](../AUDIT.md) for detailed findings and
link its IDs here. A superficial scan is not a comprehensive audit. Mark files
or behavior not directly inspected as unverified.

## Existing-project entry decision

<!-- Keep for existing projects; otherwise state Not applicable — new project. -->

- Current state summary: {{existing docs, architecture, code, Git/worktree,
  instruction, tracker, setup, and ownership state, with AUDIT IDs}}
- Recommended path: Audit, then guided approved planning/setup/tracker retrofit;
  route any code changes to the later agent-team implementation run.
- User choice: {{Approved recommended path | Different approved path | Pending}}
- Source / date: {{message or decision ID / YYYY-MM-DD}}
- Preservation boundary: {{files, IDs, history, changes, and evidence to retain}}

Do not change existing product code or integrate audit recommendations during
kickoff. Record recommendations, obtain decisions, and map approved changes into
planning. Product implementation belongs to agent-team.

## Stage status

| Stage | Purpose | Status | Approval ID / date | Affected artifacts | Invalidated by |
| --- | --- | --- | --- | --- | --- |
| 1 | Product definition | {{Not started / In progress / Awaiting approval / Approved / Invalidated}} | {{APR-001 / date or Pending}} | {{PRD sections / AUDIT findings}} | {{decision ID or None}} |
| 2 | First-release scope | {{status}} | {{APR ID / date or Pending}} | {{PRD requirements, scope, PLAN}} | {{decision ID or None}} |
| 3 | Experience and design | {{status}} | {{APR ID / date or Pending}} | {{DESIGN sections or nonvisual rationale}} | {{decision ID or None}} |
| 4 | Technical blueprint | {{status}} | {{APR ID / date or Pending}} | {{PRD architecture/stack/tree, AUDIT target}} | {{decision ID or None}} |
| 5 | Execution and handoff | {{status}} | {{APR ID / date or Pending}} | {{PLAN, setup, tracker, agent instructions}} | {{decision ID or None}} |

## Stage 1 — Product definition

Capture the problem, intended users, current alternatives, value, evidence, and
riskiest assumptions. For an existing project, distinguish current documented
intent, observed behavior, and the approved target.

### Confirmed answers

| Answer ID | Topic | Answer | Status | Source / date | Evidence / assumption IDs | Affected artifacts |
| --- | --- | --- | --- | --- | --- | --- |
| ANS-001 | {{topic}} | {{user's answer, accurately condensed}} | {{Confirmed / Revised / Superseded}} | {{source / YYYY-MM-DD}} | {{EV/ASM IDs}} | {{PRD sections / requirement IDs}} |

### Stage summary and approval

- Summary presented: {{exact summary or durable message pointer}}
- Open concerns: {{OQ/ASM IDs or None}}
- Approval question: {{one explicit approve/revise question}}
- Approval: {{APR-001 — Approved | Revisions requested | Pending}}
- Approver / source / date: {{identity, message pointer, YYYY-MM-DD}}
- Approved scope: {{what this approval covers}}

## Stage 2 — First-release scope

Capture user journeys, priorities, exclusions, outcomes, acceptance criteria,
budget, schedule, and other constraints. Do not invent missing targets.

### Confirmed answers

| Answer ID | Topic | Answer | Status | Source / date | Affected artifacts |
| --- | --- | --- | --- | --- | --- |
| {{ANS-...}} | {{journey/scope/outcome/constraint}} | {{confirmed answer}} | {{status}} | {{source/date}} | {{REQ/OUT/CON IDs}} |

### Stage summary and approval

- Summary presented: {{summary or pointer}}
- Open concerns: {{IDs or None}}
- Approval question: {{one explicit approve/revise question}}
- Approval: {{APR-... — status, approver, source, date, approved scope}}

## Stage 3 — Experience and design

Capture interface type, interaction needs, accessibility, brand direction,
references, and interface-specific states. Do not invent visual screens for a
CLI, API, library, or other project without a rendered visual interface.

### Confirmed answers

| Answer ID | Topic | Answer | Status | Source / date | Affected artifacts |
| --- | --- | --- | --- | --- | --- |
| {{ANS-...}} | {{interface/flow/accessibility/brand topic}} | {{confirmed answer}} | {{status}} | {{source/date}} | {{DESIGN sections / DDES IDs}} |

### Stage summary and approval

- Summary presented: {{summary or pointer}}
- Open concerns: {{IDs or None}}
- Approval question: {{one explicit approve/revise question}}
- Approval: {{APR-... — status, approver, source, date, approved scope}}

## Stage 4 — Technical blueprint

Capture stack options, architecture, data, integrations, security, deployment,
operations, and intended folder structure as relevant. For existing projects,
compare observed current architecture with the approved target and record
preserve/change decisions without overwriting repository truth.

### Confirmed answers

| Answer ID | Topic | Current state / evidence | Approved target or assumption | Status | Source / date | Affected artifacts |
| --- | --- | --- | --- | --- | --- | --- |
| {{ANS-...}} | {{architecture/stack/data/etc.}} | {{AUDIT/EV IDs}} | {{approved result or labeled assumption}} | {{Confirmed / Open / Revised}} | {{source/date}} | {{PRD/PLAN paths and IDs}} |

### Stage summary and approval

- Summary presented: {{summary or pointer}}
- Open concerns: {{IDs or None}}
- Approval question: {{one explicit approve/revise question}}
- Approval: {{APR-... — status, approver, source, date, approved scope}}

## Stage 5 — Execution and handoff

Capture task breakdown, dependencies, verification, skill setup, agent rules,
tracker selection, readiness, and first actionable task. Setup that depends on a
choice begins only after that choice is approved.

### Confirmed answers

| Answer ID | Topic | Answer | Status | Source / date | Affected artifacts |
| --- | --- | --- | --- | --- | --- |
| {{ANS-...}} | {{tracking/setup/delegation/verification topic}} | {{confirmed answer}} | {{status}} | {{source/date}} | {{PLAN/AGENTS/setup/tracker}} |

### Stage summary and approval

- Summary presented: {{summary or pointer}}
- Open concerns: {{IDs or None}}
- Approval question: {{one explicit approve/revise question}}
- Approval: {{APR-... — status, approver, source, date, approved scope}}

## Decision register

| ID | Decision | Status | Source / date | Evidence / alternatives | Affected artifacts | Supersedes / invalidates |
| --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | {{decision or explicit preservation choice}} | {{Proposed / Approved / Rejected / Superseded}} | {{user/source / YYYY-MM-DD}} | {{EV/AUD/ASM IDs and trade-offs}} | {{paths, REQ/TASK IDs}} | {{DEC/APR IDs or None}} |

When a decision changes, append or update the decision history. Preserve the
previous approved baseline and source. Mark only affected stage approvals and
derived artifacts invalidated; do not silently rewrite history.

## Open questions and pending question

| ID | Stage | Question | Choices and trade-offs | Recommended choice / reason | Blocks / affects | Status |
| --- | --- | --- | --- | --- | --- | --- |
| OQ-001 | {{stage}} | {{one focused question}} | {{2–3 choices, each with concrete impact}} | {{choice and reason}} | {{artifact/task/setup}} | {{Pending / Answered by ANS ID / Withdrawn}} |

Pending question: {{exactly one OQ ID, or None}}
Waiting since: {{timestamp or Not waiting}}
Independent work allowed while waiting: {{specific work or None}}

Do not ask another question until the pending one is answered or withdrawn and
recorded. On resume, inspect this record and continue with the pending decision;
do not repeat completed initialization, approvals, or task seeding.

## Change and artifact impact

| Change ID | Trigger / source | Prior approved baseline | Proposed / approved change | Approvals invalidated | Artifacts to merge or refresh | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CHG-001 | {{new evidence or user revision}} | {{version/DEC/APR IDs}} | {{change}} | {{APR IDs or None}} | {{paths and derived files}} | {{Proposed / Approved / Applied / Rejected}} |

Merge updates into existing documents non-destructively. Preserve useful project
content, stable requirement and task IDs, Git history, and approval provenance.
If an ID must change, record an old-to-new mapping and the reason before updating
references or tracker records.

## Dependency and setup choices

| Dependency | Availability / checked source | Version / revision | Purpose | Scope | License / access note | User choice | Receipt status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{dependency}} | {{installed, missing, unusable; authoritative source/date}} | {{version or Unknown}} | {{concrete capability}} | {{project/user/external}} | {{verified current condition}} | {{reuse/install/skip/alternative/Pending}} | {{.project-kickoff/setup.json pointer or Pending}} |

Missing dependencies do not erase independent progress. Offer verified
alternatives and wait for the user's explicit selection before adoption. Keep
one authoritative tracker and preserve the selected mode across recovery.

## Resume checkpoint

- Last completed stage / approval: {{stage and APR ID}}
- Current artifact versions: {{PRD/DESIGN/PLAN/AUDIT versions}}
- Setup / tracker state: {{receipt and canonical tracker pointer}}
- Pending question: {{OQ ID or None}}
- Next action: {{one specific action}}
