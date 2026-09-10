<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- This document is the approved implementation baseline. The selected tracker
  owns live execution status; do not maintain status here after handoff.
- Replace every {{...}} value. Keep stable IDs and preserve requirement links.
- Fully detail approved first-release work. Put unapproved or later ideas only
  in Future roadmap, with no runnable status or tracker seed.
- Estimates express complexity and assumptions, not invented delivery dates.
-->

# {{Project name}} — Implementation Plan

Status: {{Draft | Awaiting approval | Approved | Superseded}}
Version: {{document version}}
Updated: {{YYYY-MM-DD}}
Baseline source: {{approved PRD and DESIGN versions}}
Approval source: {{DISCOVERY.md stage 5 approval ID/link, or Pending}}
Generated with: project-kickoff {{semantic version}}

## First-release delivery definition

- Outcome: {{observable result delivered by this plan}}
- Included requirements: {{REQ/NFR IDs}}
- Excluded work: {{explicit non-goals}}
- Key constraints: {{CON IDs}}
- Release / deployment boundary: {{what verification completes this plan and
  whether deployment is included, separate, or undecided}}

## Execution assumptions

| ID | Assumption | Effect on estimates / ordering | Validation point |
| --- | --- | --- | --- |
| PASM-001 | {{team, tooling, environment, dependency, or access assumption}} | {{impact if false}} | {{task or prerequisite check}} |

Complexity scale: {{for example XS = bounded configuration; S = one contained
change; M = several connected changes; L = cross-boundary or high-uncertainty
work}}. Estimates assume {{test environment, access, team familiarity, and other
approved conditions}}. Re-estimate when those conditions change.

## Dependency graph and parallel work

```text
{{EPIC-001 / TASK-001 dependency graph. Use arrows from prerequisite to dependent.}}
```

Parallel candidates:

| Tasks | Why they are independent | Shared boundary / merge order |
| --- | --- | --- |
| {{TASK-002 and TASK-003}} | {{no shared prerequisite or writable path}} | {{contract fixed first; serial integration if needed}} |

Do not label work parallel when it shares an unresolved decision, migration,
generated artifact, writable path, or environment resource.

## First-release epics and stories

### EPIC-001 — {{epic outcome}}

- Requirements: {{REQ/NFR IDs}}
- Intended result: {{user or system capability}}
- Completion evidence: {{integrated checks or artifacts proving the epic}}
- Dependencies: {{epic/task IDs or None}}

#### STORY-001 — {{user/system story title}}

As {{actor}}, I need {{capability}}, so that {{outcome}}.

- Requirements: {{REQ IDs}}
- Acceptance criteria:
  - {{observable criterion}}
- Dependencies: {{story/task IDs or None}}
- Child tasks: {{TASK-001, TASK-002}}

## Executable tasks

### TASK-001 — {{task title}}

- Parent: {{EPIC-001 / STORY-001}}
- Requirements: {{REQ-001, NFR-001}}
- Intended outcome: {{working behavior or concrete artifact}}
- Prerequisites: {{approved decisions, access, task IDs, or None}}
- Owner profile: {{routine developer | standard developer | complex developer |
  specialist, with why this complexity needs that profile}}
- Complexity: {{XS | S | M | L}} — {{estimate assumptions and main uncertainty}}
- Affected paths / boundaries: {{specific expected files, package, service,
  public interface, data boundary, or "resolve during task after inspection"}}
- Implementation:
  1. {{inspect or establish a concrete prerequisite}}
  2. {{make the smallest complete behavior/configuration/documentation change}}
  3. {{handle relevant failure path, compatibility, or migration}}
  4. {{record any required operator/user guidance}}
- Acceptance criteria:
  - {{observable behavior tied directly to a requirement}}
  - {{relevant error, accessibility, security, or compatibility behavior}}
- Verification:
  - {{exact test/check type, environment, and expected observation}}
  - {{integration boundary or manual review where automation cannot prove it}}
- Evidence to retain: {{test output path, screenshot, report, revision, or other
  durable pointer; do not paste credentials or full logs}}
- Handoff: {{downstream task, interface contract, or integration note}}

Repeat this task block only for work required by the approved first release.
Setup, package installation, scaffold code/configuration, builds, tests, and
executable helpers are tasks performed by complexity-appropriate subagents in
isolated worktrees under the project policy.

## Requirement coverage

| Requirement | Plan tasks | Acceptance / verification evidence expected | Coverage status |
| --- | --- | --- | --- |
| REQ-001 | {{TASK-001}} | {{criterion and planned check}} | {{Covered / Gap — decision needed}} |

Every first-release requirement must map to at least one task and verification
method. A task may cover several related requirements when its boundary remains
clear. Resolve cycles and missing prerequisites before approval.

## Tracker initialization

- Selected tracker: {{Beads | root TASKS.md | .agent-team/TASKS.md | user-approved non-Agent-Team alternative | Pending}}
- Canonical location / identity: {{absolute path, database identity, or Pending}}
- Project Kickoff setup receipt: {{.project-kickoff/setup.json path}}
- Agent-Team input: {{.project-kickoff/AGENT_TEAM_HANDOFF.json path or Not applicable}}
- Handoff validation: {{check_agent_team_handoff.py result or Pending}}
- Writer / concurrency rule: {{project orchestrator only, or verified backend rule}}
- ID mapping: {{PLAN task ID -> tracker ID, populated during seeding}}
- First actionable task: {{TASK ID, or Blocked by OQ/decision ID}}

### Existing task and ID reconciliation

| Existing requirement / task ID | Current tracker state and evidence | Approved PLAN ID | Migration action | Approval source |
| --- | --- | --- | --- | --- |
| {{existing ID}} | {{status, revision, evidence, or Unknown}} | {{same TASK-### ID or new mapped ID}} | {{Preserve / Merge / Map and deprecate / Add; never duplicate}} | {{AUD/DEC/APR IDs}} |

Preserve prior approved baselines and live evidence. Do not reset an existing
task to `planned`, reopen completed external work, or infer success from a label.
When current and target scope differ, create only approved delta tasks and link
them to the preserved requirement and audit findings. Do not create work for an
approved preserve decision or a finding whose approved outcome needs no
remediation.

Seed only the approved first-release tasks. On repeated setup, inspect existing
IDs and reconcile rather than duplicating them. Keep this plan as the baseline;
record claims, status, failures, evidence, and release state only in the active
tracker.

## Handoff and completion checks

- [ ] Approved PRD requirements all have plan coverage.
- [ ] Approved design obligations appear in tasks and verification.
- [ ] Dependencies have correct direction and no cycles.
- [ ] External access and setup prerequisites have owners.
- [ ] The selected tracker contains one mapping for each runnable task.
- [ ] The first actionable task and its worktree boundary are clear.
- [ ] Verification covers the integrated first-release behavior.
- [ ] Future ideas were not seeded as active tasks.

## Future roadmap — not active work

| Idea | Potential outcome | Evidence / decision still needed | Relationship to first release |
| --- | --- | --- | --- |
| {{later-phase idea}} | {{possible value}} | {{research, approval, or prerequisite}} | {{extension, replacement, or independent}} |

These ideas are unapproved implementation work unless an approval record says
otherwise. Promote an idea by updating the PRD scope, obtaining approval,
versioning this plan, and then reconciling the active tracker.
