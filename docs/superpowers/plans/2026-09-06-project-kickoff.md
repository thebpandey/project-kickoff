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

- [x] Run bounded no-skill scenarios for discovery, unavailable Beads, and cleanup.
- [x] Record actual baseline responses without inventing failure evidence.
- [x] Write a concise entrypoint with relevant routing and essential invariants.
- [x] Define adaptive stages, approval/revision state, checkpoints, scope limits.
- [x] Define task seeding/deduplication, tracker selection and partial recovery.
- [x] Define host-specific install steps from checked primary documentation.
- [x] Define dependency receipts, fallback choice, and artifact readiness checks.
- [x] Add semantic version metadata, matching changelog, and upgrade rules.
- [x] Add existing-project audit routing and the user's selected transition,
  preserving current code, documents, task IDs, branches, and uncommitted work.
- [x] Document license, installation, invocation, optional skills, and limitations.
- [x] Expand README with detailed simple-language installation and command
  instructions. Implement its start/audit/audit-only/resume/status/help/version
  action descriptions in the actual skill routing.
- [x] Add readable Mermaid workflow/dependency charts and render them locally.
- [x] Check metadata with the bundled quick_validate.py and review references.
- [x] Commit the deliverable in its owned worktree.

## Task 2: Output templates

**Files:** assets/templates/PRD.md, DESIGN.md, PLAN.md, AGENTS.md, CLAUDE.md,
MISTAKES.md, CONTEXT.md, TASKS.md, DISCOVERY.md, README.md.
Also add assets/templates/AUDIT.md for existing-project findings and decisions.

**Consumes:** Approved design. Task 1 links to these exact names.
**Produces:** Instructional output templates, adapted by the executing agent.

- [x] Define requirement/decision IDs and explicit evidence/assumption states.
- [x] Include the full PRD and first-release plan contracts from the spec.
- [x] Make DESIGN.md suitable for both visual and nonvisual projects.
- [x] Define one shared agent policy with a Claude Code adapter.
- [x] Define single-writer mistakes, context, discovery, and fallback task records.
- [x] Include actionable handoff, dependency availability, and verified commands.
- [x] Include artifact provenance/version and current-versus-target truth for
  existing projects, with audit evidence and approved findings linked to tasks.
- [x] Check that placeholders are labeled template inputs, not completed output.
- [x] Commit templates in their owned worktree.

## Task 3: Integration and behavioral validation

**Files:** docs/validation.md and package corrections where evidence requires.
**Consumes:** Exact Task 1 and Task 2 revisions in one integration worktree.
**Produces:** Validated package and recorded evidence with practical limits.

- [x] Merge the two nonoverlapping branches into the integration worktree.
- [x] Independently execute discovery and resume scenarios using the skill.
- [ ] Exercise nonvisual artifact generation in a disposable fixture.
- [x] Exercise missing dependencies and repeated seeding with existing task IDs.
- [x] Examine scope-change approval invalidation and cleanup safety.
- [x] Exercise an existing project with stale docs, a current tracker, a non-main
  branch, and local edits; verify inspection preserves state and asks for change.
- [x] Verify version metadata, changelog, release tag and archive naming agree.
- [x] Check README/command changes, nonmutating informational actions, and new
  project detection when only private skill installation files are present.
- [x] Run package metadata, local-reference, and release-content checks.
- [x] Review requirements and license/output boundaries; fix demonstrated defects.
- [x] Recheck only affected scenarios and record real results.

The nonvisual disposable fixture covered an existing-project `AUDIT.md` plus
`DISCOVERY.md` and `CONTEXT.md` checkpoints. A separate new-project fixture
saved its first question and stopped. It did not generate the full new-project
PRD, design, plan, policy, tracker, and handoff artifact set. The unchecked item
above preserves that validation limit.

## Task 4: Package, publish, and clean up

**Consumes:** Verified integration revision and user-approved private destination.
**Produces:** Private GitHub repository, release archive, clean canonical main.

- [x] Create an archive from an explicit package-file allowlist; exclude docs
  used only for development, worktrees, runtime state, and dependency copies.
- [x] Inspect archive contents and verify the extracted skill package.
- [x] Update canonical main to the verified integration revision.
- [x] Verify branch integration, preserve validation evidence, and remove only
  eligible task-owned worktrees and branches.
- [x] Create or reuse the intended GitHub repo, verify it is private, then push.
- [x] Verify remote main matches local main; report repository and archive paths.
