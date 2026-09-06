---
name: project-kickoff
description: Define new software projects and audit or re-plan existing projects, producing approved product, experience, technical, scaffold, and Agent-Team handoff artifacts. Use for project kickoff, ordinary existing-project audits, or major project revisions before feature implementation.
metadata:
  version: "0.1.0"
---

# Project Kickoff

Move the project through four explicit states: `discovery`, `approved planning`,
`setup`, and `ready for handoff`. Do not start product feature implementation.

## Start or resume

1. Classify the request as a new project, existing-project kickoff, or resumed
   kickoff. For an existing project, first read
   [the existing-project audit](references/existing-projects.md). After the
   audit, continue through guided decisions and setup unless the user explicitly
   requested audit-only scope.
2. Identify the intended project directory and inspect existing project files,
   Git metadata, `.project-kickoff/DISCOVERY.md`, and `CONTEXT.md`. Preserve all
   user files, including unknown untracked and ignored files.
3. Restore confirmed decisions, stage approvals, invalidations, the pending
   question, and the next action. Do not repeat answered questions or completed
   setup. Record this Skill's `metadata.version`. If a saved kickoff used another
   version, read `CHANGELOG.md` and apply the compatibility rules in
   [the host adapter](references/hosts.md).
4. If discovery is incomplete, read [the interview workflow](references/interview.md).
   Ask exactly one unresolved question and wait for the answer.
5. When producing or revising project documents, read [the artifact contracts](references/artifacts.md).
6. After the dependent decisions are approved, read [setup](references/setup.md)
   and the applicable [host adapter](references/hosts.md).
7. Before implementation handoff, read [handoff and cleanup](references/handoff.md).
8. Apply [the communication rules](references/communication.md) throughout.

## Invariants

- Give recommended choices with useful trade-offs. A timeout or silence is not
  an answer. Do not make an unresolved stack, tracker, product, or design choice
  for the user.
- Ask for approval of each stage as its own question. A changed decision
  invalidates only affected approvals and derived artifacts.
- During discovery, write only the checkpoint and planning records. Create
  approved artifacts and perform setup only after their dependent decisions are
  approved.
- Keep `PLAN.md` as the approved implementation baseline. Keep execution status
  in one user-selected live tracker. Never use a second or temporary live tracker.
- Use stable requirement and plan-task IDs. Resume task seeding from recorded
  mappings without creating duplicates.
- Reuse verified project tools. Install only approved, project-scoped items by
  their current official procedure. Do not change global configuration, install
  global hooks, or overwrite existing instructions without matching authority.
- Keep the canonical checkout for planning and shared records. For a new
  repository, its integration branch is `main`. For an existing repository, use
  the user-designated existing integration branch without renaming it. Delegate
  all scaffold and later code execution to task worktrees. Combine work in one
  integration worktree.
- A minimal scaffold contains only approved structure and basic tooling. State
  when it has no runnable application. Prepare the Agent-Team invocation, but do
  not start it as a side effect.
- After verified integration into the canonical integration branch, clean
  eligible task branches, worktrees, and task-owned processes. This cleanup does
  not depend on production deployment.

Use the templates in `assets/templates/`. Adapt them to the project; do not copy
unresolved placeholders into completed artifacts.
