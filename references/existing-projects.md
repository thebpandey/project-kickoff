# Existing-project audit

Use this route when the intended directory already contains product code,
project documents, configuration, a tracker, or meaningful Git history. Begin
with read-only inspection. Do not initialize Git, rename existing branches, replace
project files, select a new tracker, install dependencies, or run mutating setup
during the audit.

Do not use this route only because the directory contains installed host skill
folders, empty Git metadata, or install-only housekeeping. Exclude skill-package
source under `.agents/skills/` and `.claude/skills/` from product inspection.
An otherwise empty project remains a new project.

## Establish the evidence boundary

Resolve the intended project root and actual Git root. If they differ, report
the relationship and do not adopt an ancestor repository without the user's
choice. Record the inspected revision, branch, worktrees, tracked changes,
untracked files, ignored files relevant to setup, and any repository instructions.
Preserve all user work and existing branches. Ask which existing branch is the
canonical integration branch if project evidence and user context do not identify
it. Do not create or rename a branch during the audit.

Inspect only what is needed to understand:

- product behavior, users, first-release or current-release scope, and known
  constraints;
- current architecture, stack, folder structure, data ownership, integrations,
  security boundaries, deployment, and operations;
- existing PRD, design, plan, instruction, context, and lesson files;
- the authoritative task tracker, task IDs, active work, and history;
- package manifests, lockfiles, tool configuration, CI, and documented commands;
- available test suites and the latest attributable evidence.

Do not treat documentation as proof that the code matches it. Distinguish the
factual current system, the documented intent, and the proposed target. Label
inferences and evidence gaps.

## Report the audit

Give each finding a stable `AUD-###` ID. Include severity, evidence path or
revision, observed condition, impact, confidence, evidence gap, and recommended
decision. Use severity for material product, delivery, data, security, or
maintenance impact; do not inflate cosmetic differences.

Report checks as one of: run and passed, run and failed, blocked, or not run.
Historical CI, a README command, or another agent's statement is prior evidence,
not a test result from this audit. Do not run expensive, external, destructive,
or state-changing checks under read-only audit authority.

Map existing artifacts against the contracts in [artifacts](artifacts.md). Note
missing, stale, conflicting, or sufficient sections. Map current tracker items to
known plan or requirement IDs without changing either system. Never overwrite,
erase, renumber, close, reopen, migrate, or duplicate tracker items during audit.

Create or merge the report in root `AUDIT.md` from
[the audit template](../assets/templates/AUDIT.md). Preserve existing findings
and IDs. Record the Skill version, audit scope, inspected revision and working
state, evidence limits, current and documented architecture, target proposals,
and the disposition of each finding.

## Continue through decisions

By default, continue from the completed audit into guided project setup in the
same kickoff. Do not require a second kickoff request. If the user explicitly
asked for audit-only scope, deliver `AUDIT.md` and stop before decisions or
mutations.

Use the interview protocol to resolve audit findings one at a time. For each
material area, offer retain, change, or defer choices with trade-offs and a
recommendation. Keep accepted current decisions as valid inputs; do not force a
greenfield redesign. A completed audit does not approve remediation.

The audit can conclude that no remediation is needed. Record the evidence and
the user's retain decisions. Preserve completed and historical tracker records;
do not manufacture runnable requirements or tasks to make the handoff nonempty.

After the user selects a direction, record affected decisions and approvals.
Update documents, setup, or tracking only after the relevant stage approval.
Merge into existing files and preserve their useful content and identity. Reuse
the selected current tracker when it remains suitable. A tracker migration needs
its own user choice, reconciliation plan, and verified mapping before the new
tracker becomes authoritative.

Route product-code and application-configuration remediation through the approved
plan and Agent-Team handoff. Kickoff can update approved planning documents,
project agent instructions, skill setup, and tracker setup within their approved
scope. Any executable verification uses an approved task-owned worktree and
suitable delegated worker. If dependencies, credentials, or services are missing,
report the limit and continue independent inspection. Do not repair or refactor
product code during kickoff. Keep current and target architecture visible until
the approved transition is implemented and verified.
