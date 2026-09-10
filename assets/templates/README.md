<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- This is the generated project's README, not the project-kickoff skill README.
- Replace every {{...}} value. Describe only artifacts and tooling that actually
  exist. Include commands only after running or otherwise verifying them in the
  named environment; preserve the result and revision.
- A planning-only scaffold may have no runnable application. Say so plainly.
-->

# {{Project name}}

{{One approved sentence describing the product, intended users, and first-release value.}}

Project status: {{Discovery | Approved planning | Setup in progress | Ready for
agent-team handoff | Implementation in progress | Verified | Deployed}}
Current revision: {{exact revision or Not committed}}
Kickoff baseline: project-kickoff {{semantic version}}; {{document versions and approval ID}}

## Current and approved target state

| Area | Current verified state | Approved target | Evidence / decision |
| --- | --- | --- | --- |
| Product scope | {{what exists now or Planning only}} | {{approved first-release boundary}} | {{PRD version / AUD IDs / APR ID}} |
| Architecture / stack | {{observed or scaffolded state}} | {{approved target}} | {{PRD/AUD/DEC IDs}} |
| Execution | {{tracker and task state pointer}} | {{first actionable outcome}} | {{PLAN version / tracker path}} |

<!-- Keep this paragraph and link only for an existing project. -->
For an existing project, [`AUDIT.md`](AUDIT.md) records the inspected current
state, evidence limits, discrepancies, preserve/change decisions, and approved
retrofit mapping. Recommendations in the audit are not implemented changes.

## Start here

- [`PRD.md`](PRD.md) — approved product, requirements, and technical blueprint.
- [`DESIGN.md`](DESIGN.md) — approved visual or nonvisual experience contract.
- [`PLAN.md`](PLAN.md) — approved first-release implementation baseline.
- [`.project-kickoff/DISCOVERY.md`](.project-kickoff/DISCOVERY.md) — source
  answers, decisions, stage approvals, and pending question.
- [`CONTEXT.md`](CONTEXT.md) — current resumption pointers and next action.
- [`AGENTS.md`](AGENTS.md) — common project policy for coding agents.
- [`MISTAKES.md`](MISTAKES.md) — canonical shared lessons, initially empty.
- {{selected tracker link}} — live task state. The selection and canonical
  location are recorded in `.project-kickoff/setup.json` and the validated
  `.project-kickoff/AGENT_TEAM_HANDOFF.json`.

## Repository structure

```text
{{actual concise folder tree created or preserved, with each entry's purpose}}
```

This repository currently contains {{approved planning documents and minimal
scaffold / an existing application plus approved planning retrofit}}.
Runnable application status: {{No runnable application was created during
kickoff | Runnable component and verified command below}}.

## Prerequisites and setup

| Dependency / access | Purpose | Required now? | Verified version / state | Setup source / receipt |
| --- | --- | --- | --- | --- |
| {{tool, runtime, account, or service}} | {{purpose}} | {{Yes / Later / Optional}} | {{version/state actually checked or Pending}} | {{official docs and .project-kickoff/setup.json pointer}} |

Use project-scoped installation and configuration. Do not include credentials in
this repository. Required environment variable names, if any: {{names only or
None}}. See {{`.env.example` or approved configuration path, only if it exists}}.

## Verified commands

<!-- Keep only commands that apply to files actually present. For each command,
record when, where, and against which revision it was verified. Do not present a
planned command as working. If none exist, keep the explicit no-command state. -->

| Purpose | Command | Verified environment | Result / evidence |
| --- | --- | --- | --- |
| {{install/build/test/lint/run/check}} | `{{exact command}}` | {{OS/runtime/version, YYYY-MM-DD, revision}} | {{pass/fail and evidence path}} |

Verified launch command: {{`command` and revision | None — no runnable application yet}}

If a command is pending verification, find it in `PLAN.md` or the active tracker;
do not infer it from another project or package manager.

## Implementation handoff

- Plan approval: {{APR ID, source, date, PLAN version}}
- Active tracker: {{mode and canonical absolute path or identity}}
- Project Kickoff setup receipt: {{absolute `.project-kickoff/setup.json` path}}
- Validated Agent-Team input: {{absolute `.project-kickoff/AGENT_TEAM_HANDOFF.json` path}}
- Agent-Team initialization receipt: {{absolute `.agent-team/setup.json` path or Not initialized; Agent-Team-owned}}
- First actionable task: {{TASK ID -> tracker ID and intended outcome}}
- Current blocker / pending question: {{OQ/F ID or None}}
- Shared-record writer: {{project orchestrator identity}}
- Canonical main checkout: {{absolute path, branch, revision}}
- Integration worktree: {{absolute path or Create when first needed}}
- Required lessons: {{M-IDs or None}}
- Exact invocation for this host: `{{verified Codex or Claude Code invocation}}`
- Initialization request: {{checker command with the actual Agent-Team owner session, operation ID, and current setup version}}

The handoff is tested with Agent-Team 7.0.2. It prepares Agent-Team; it does not
create Agent-Team runtime state or start implementation. Product code,
package installation, scaffold execution, builds, and tests run later through
complexity-appropriate subagents in isolated worktrees under `AGENTS.md`.

## Verification and readiness

| Check | Status | Evidence / next action |
| --- | --- | --- |
| Document consistency and approvals | {{Verified / Blocked / Not run}} | {{revision/report or action}} |
| Requirement-to-plan coverage | {{Verified / Blocked / Not run}} | {{mapping/report}} |
| Tracker seed and dependency cycles | {{Verified / Blocked / Not run}} | {{receipt/report}} |
| Dependency availability | {{Verified / Partial / Blocked}} | {{setup receipt and exceptions}} |
| Scaffold / existing-project preservation | {{Verified / Blocked / Not run}} | {{revision/AUD IDs/status evidence}} |
| First actionable task | {{Ready / Blocked}} | {{TASK/tracker ID or blocker}} |

Ready for implementation means approved documents, one selected tracker, a
reconciled task mapping, clear ownership, and a concrete first task. It does not
mean the first release has been implemented, tested, deployed, or verified in
production.

## Change and history policy

Preserve stable requirement, decision, and task IDs. For an existing project,
merge approved planning into useful current documents without replacing history
or unapproved content. Record changed decisions in `DISCOVERY.md`, retain the
prior approval baseline, and map any unavoidable ID migration before changing
tracker records.

## Support and ownership

- Product owner: {{name or team}}
- Technical owner: {{name or team}}
- Support / issue route: {{approved channel or Pending}}
- Deployment authority: {{approved role or Not in current scope}}
