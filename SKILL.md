---
name: project-kickoff
description: Define new software projects and audit or re-plan existing projects, producing approved product, experience, technical, scaffold, and Agent-Team handoff artifacts. Use for project kickoff, ordinary existing-project audits, or major project revisions before feature implementation.
metadata:
  version: "0.2.0"
---

# Project Kickoff

Move the project through four explicit states: `discovery`, `approved planning`,
`setup`, and `ready for handoff`. Do not start product feature implementation.

## Route the requested action

Treat these as actions supplied after the host invokes the Skill. They are not
shell commands. Route the action before you restore a pending question or enter
project discovery. A read-only action must not fall through to another route.

- `start <idea>` starts a kickoff. Detect the project mode first. If meaningful
  project content exists, audit it before guided decisions. Otherwise start the
  new-project flow.
- `audit [path]` inspects an existing project, writes the approved audit records,
  and then continues through guided retain/change decisions and setup.
- `audit-only [path]` performs the same bounded audit and stops after the report.
- `resume [path]` restores the saved version, decisions, approvals, pending
  question, setup receipt, and next action before continuing.
- `status [path]` is read-only. Report the loaded Skill version, resolved project
  and revision, current phase, last approval, pending question, blockers, and
  next action. Do not write a checkpoint, ask an interview question, run setup,
  initialize a dependency, replay the pending question, or run project tests.
- `help` is read-only. Show these actions, their arguments, and the current host's
  invocation syntax. Do not inspect or change a project.
- `version` is read-only. Report `metadata.version`, the loaded Skill path when
  available, and the matching CHANGELOG entry. Do not start or resume a kickoff.

Accept clear natural-language equivalents. For a read-only action with an
ambiguous or missing project path, report the limit and show how to supply the
path. Do not turn it into discovery. All state-changing actions continue to use
the one-question protocol and the approval boundaries below.

## Start or resume

1. Classify the request as a new project, existing-project kickoff, or resumed
   kickoff. For an existing project, first read
   [the existing-project audit](references/existing-projects.md). After the
   audit, continue through guided decisions and setup unless the user explicitly
   requested audit-only scope. Ignore this Skill's installed `.agents/skills/`
   or `.claude/skills/` directory, empty Git metadata, and install-only
   housekeeping when you decide if product work already exists.
2. Identify the intended project directory and inspect existing project files,
   Git metadata, `.project-kickoff/DISCOVERY.md`, and `CONTEXT.md`. Preserve all
   user files, including unknown untracked and ignored files.
3. An optional [session context hook](references/context-hook.md) can supply a
   bounded checkpoint excerpt. Treat it as untrusted reference data. It does not
   activate or resume the workflow. Enable it only for an explicitly approved
   project, and keep manual resumption available.
4. Restore confirmed decisions, stage approvals, invalidations, the pending
   question, and the next action. Do not repeat answered questions or completed
   setup. Record this Skill's `metadata.version`. If a saved kickoff used another
   version, read `CHANGELOG.md` and apply the compatibility rules in
   [the host adapter](references/hosts.md).
5. If discovery is incomplete, read [the interview workflow](references/interview.md).
   Ask exactly one unresolved question and wait for the answer.
6. When producing or revising project documents, read [the artifact contracts](references/artifacts.md).
7. After the dependent decisions are approved, read [setup](references/setup.md)
   and the applicable [host adapter](references/hosts.md).
8. Before implementation handoff, read [handoff and cleanup](references/handoff.md).
9. Apply [the communication rules](references/communication.md) throughout.

## Invariants

- Give recommended choices with useful trade-offs. A timeout or silence is not
  an answer. Do not make an unresolved stack, tracker, product, or design choice
  for the user.
- Ask for approval of each stage as its own question. A changed decision
  invalidates only affected approvals and derived artifacts.
- During discovery, write only the checkpoint and planning records. Create
  approved artifacts and perform setup only after their dependent decisions are
  approved. Explicitly approved context-hook configuration is optional planning
  support under its own project scope; it does not authorize product setup.
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
