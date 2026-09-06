# Project Kickoff Implementation Plan

> **For agentic workers:** Use subagent-driven development in separate worktrees.
> The user approved execution. Do not reopen the execution-method question.

**Goal:** Deliver the approved project-kickoff skill for Codex and Claude Code
and publish the validated release to the private thebpandey/project-kickoff repo.

**Architecture:** One shared skill entrypoint routes to focused references and
output templates. The host performs the interview and setup with its available
tools. No custom application, installer service, or tracker implementation.

**Tech Stack:** Markdown, YAML metadata, Git. Use existing skill validation tools
and a small standard-library packaging/check helper only if needed.

**Spec:** [Approved design](../../specs/project-kickoff-design.md).

## Global constraints

- Preserve every confirmed decision and the approved LICENSE.
- One pending question, recommended choices, and explicit answers/approvals.
- Project-scoped setup; inspect existing tools and authoritative sources.
- Missing tools: finish independent work, suggest TASKS.md/free alternatives,
  wait for a selection before substitution, use one tracker.
- Canonical main owns planning; delegate execution to isolated worktrees.
- Verify integration before removing eligible worktrees and task branches.
- Do not vendor dependencies or publish local runtime state.

## Task 1: Baseline and package instructions

**Files:** SKILL.md, agents/openai.yaml, README.md,
references/interview.md, references/artifacts.md, references/setup.md,
references/hosts.md, references/handoff.md, references/communication.md.
Also include references/existing-projects.md and CHANGELOG.md for the added scope.

**Consumes:** Approved design, license, baseline scenario observations.
**Produces:** Complete workflow and references to templates from Task 2.

- [ ] Run bounded no-skill scenarios for discovery, unavailable Beads, and cleanup.
- [ ] Record actual baseline responses without inventing failure evidence.
- [ ] Write a concise entrypoint with relevant routing and essential invariants.
- [ ] Define adaptive stages, approval/revision state, checkpoints, scope limits.
- [ ] Define task seeding/deduplication, tracker selection and partial recovery.
- [ ] Define host-specific install steps from checked primary documentation.
- [ ] Define dependency receipts, fallback choice, and artifact readiness checks.
- [ ] Add semantic version metadata, matching changelog, and upgrade rules.
- [ ] Add existing-project audit routing and the user's selected transition,
  preserving current code, documents, task IDs, branches, and uncommitted work.
- [ ] Document license, installation, invocation, optional skills, and limitations.
- [ ] Check metadata with the bundled quick_validate.py and review references.
- [ ] Commit the deliverable in its owned worktree.

## Task 2: Output templates

**Files:** assets/templates/PRD.md, DESIGN.md, PLAN.md, AGENTS.md, CLAUDE.md,
MISTAKES.md, CONTEXT.md, TASKS.md, DISCOVERY.md, README.md.
Also add assets/templates/AUDIT.md for existing-project findings and decisions.

**Consumes:** Approved design. Task 1 links to these exact names.
**Produces:** Instructional output templates, adapted by the executing agent.

- [ ] Define requirement/decision IDs and explicit evidence/assumption states.
- [ ] Include the full PRD and first-release plan contracts from the spec.
- [ ] Make DESIGN.md suitable for both visual and nonvisual projects.
- [ ] Define one shared agent policy with a Claude Code adapter.
- [ ] Define single-writer mistakes, context, discovery, and fallback task records.
- [ ] Include actionable handoff, dependency availability, and verified commands.
- [ ] Include artifact provenance/version and current-versus-target truth for
  existing projects, with audit evidence and approved findings linked to tasks.
- [ ] Check that placeholders are labeled template inputs, not completed output.
- [ ] Commit templates in their owned worktree.

## Task 3: Integration and behavioral validation

**Files:** docs/validation.md and package corrections where evidence requires.
**Consumes:** Exact Task 1 and Task 2 revisions in one integration worktree.
**Produces:** Validated package and recorded evidence with practical limits.

- [ ] Merge the two nonoverlapping branches into the integration worktree.
- [ ] Independently execute discovery and resume scenarios using the skill.
- [ ] Exercise nonvisual artifact generation in a disposable fixture.
- [ ] Exercise missing dependencies and repeated seeding with existing task IDs.
- [ ] Examine scope-change approval invalidation and cleanup safety.
- [ ] Exercise an existing project with stale docs, a current tracker, a non-main
  branch, and local edits; verify inspection preserves state and asks for change.
- [ ] Verify version metadata, changelog, release tag and archive naming agree.
- [ ] Run package metadata, local-reference, and release-content checks.
- [ ] Review requirements and license/output boundaries; fix demonstrated defects.
- [ ] Recheck only affected scenarios and record real results.

## Task 4: Package, publish, and clean up

**Consumes:** Verified integration revision and user-approved private destination.
**Produces:** Private GitHub repository, release archive, clean canonical main.

- [ ] Create an archive from an explicit package-file allowlist; exclude docs
  used only for development, worktrees, runtime state, and dependency copies.
- [ ] Inspect archive contents and verify the extracted skill package.
- [ ] Update canonical main to the verified integration revision.
- [ ] Verify branch integration, preserve validation evidence, and remove only
  eligible task-owned worktrees and branches.
- [ ] Create or reuse the intended GitHub repo, verify it is private, then push.
- [ ] Verify remote main matches local main; report repository and archive paths.
