# Independent integrated review

Date: 2026-09-06
Reviewer: independent Codex delegated worker
Reviewed source: `d31621052f1f1a9b4b23ab1b0ad6d5c584456dce` (project-kickoff 0.1.0)
Reviewed Git tree: `9ee238ea181783bfe0f081bfb2619cdc921bd497`
SHA-256 of sorted runtime path/content-hash manifest: `2eaa48ae681f067a4774eefff110b3c2db3e20afba62061a4643f5ccbe91197f`

## Result and scope

No material requirement defect found in the pinned source. Read the approved
`docs/specs/project-kickoff-design.md`, entrypoint, all seven references, all eleven
output templates, README, UI metadata, CHANGELOG, and LICENSE. Prior baseline,
behavior, and package-check report conclusions were not read for this review.

The source changed concurrently after this review began. The parent explicitly
kept this review pinned to d316210 and reserved the newer README/action-router
changes for a separate targeted check. This report does not approve those changes.

| Contract | Reviewed evidence and conclusion |
| --- | --- |
| New-project workflow | Entrypoint, interview, setup, artifact contracts and templates cover five separate stage approvals, saved answers, first-release scope, project-specific visual or nonvisual design, detailed implementation tasks and minimal scaffold. No feature implementation starts as a handoff side effect. |
| Existing-project workflow | Audit route distinguishes source, documents and target, preserves actual branch names and established task IDs, and leads to retain/change/defer decisions before setup. Audit-only scope stops at evidence. Completed work can remain historical without manufactured new work. |
| Decisions and resumption | One unresolved question is saved before asking; explicit user changes are recorded without asking to reconfirm the same choice. Only affected approvals/derived sections are invalidated; unrelated answers and approvals survive. |
| Tracker and execution | One tracker owns status, PLAN owns baseline; seeding preserves identity and resumes partial mappings. Worktrees separate execution and integration; cleanup checks tracked, untracked and ignored content after verified integration. |
| Dependencies and host portability | All six requested dependencies have defined availability/source/version/scope/license checks. Missing tools lead to independent progress and a user-selected researched replacement. Codex and Claude have separate paths/invocations and shared policy. No actual installation was attempted in this review. |
| License/output distinction | Sections 2–3 require written permission for the proprietary Skill and permit authorized commercial/client work without a paid entitlement. Section 4 separately allows adapting/distributing generated output and template-derived instructions. Section 5 keeps third-party terms separate. This is a textual contract review, not legal enforceability advice. |
| Versioning | SKILL metadata, README, CHANGELOG and generating-version fields agree on 0.1.0. References describe compatible/breaking changes, pinned upgrades and preserved project history. Tag/archive/publication were outside this review's task. |
| Maintainability | Short routing entrypoint delegates detail to seven focused references. Templates supply the requested detailed document contracts without a custom executable framework. No concrete maintenance defect requiring correction was identified. |

## Actual disposable fixture audit

This was a real local file audit performed by the review worker after reading the
skill, not an assertion inferred from instruction strings. The worker created a
synthetic repo, captured its initial state, inspected it with read-only Git/file
commands, wrote the skill's next permitted planning records, then compared state.

Fixture: `/tmp/project-kickoff-existing-ue4mi0fj`
Fixture base revision: `3a024f8e4a270e82b13cd60dd16b5ce2764d8092`
Canonical branch: `dev`, designated by synthetic AGENTS.md; no branch `main`.
Initial tracked files: Python CLI, pyproject manifest, stale React/Node/PostgreSQL
README, TASKS.md, AGENTS.md and .gitignore. Initial preserved user state: a source
comment edit, untracked user-notes.txt and ignored .local-cache/scratch.txt.
Tracker rows: `LEGACY-17 / R-COUNT / completed` and
`LEGACY-23 / R-ERROR / in_progress`.

Setup used Python 3 standard-library fixture utilities and local Git. An initial
`python` command was unavailable (exit 127); the same setup used `python3` and
completed. No fixture product command, package install, test suite, service,
network request or app import was run. The fixture was deliberately synthetic;
Git initialization and commit occurred only as test setup before the audit.

Observed audit output:

- Root AUDIT.md identifies the concrete README/source contradiction and limits
  its behavior claims to static evidence. It preserves completed-task history and
  distinguishes missing runtime evidence from a failed test.
- `.project-kickoff/DISCOVERY.md` records exactly one pending product-direction
  question, five unapproved stages, proposed direction and source evidence.
- CONTEXT.md points to that question and the existing tracker, while preserving
  dirty/untracked/ignored content. No branch question was needed because project
  instructions already named `dev`.
- The exact next reply was written to fixture evidence, not asked of a real user.
  No answer was synthesized and no next stage, setup or tracker mutation followed.

Exact next reply:

```text
Should the kickoff retain the Python CLI as the product baseline and reconcile the conflicting README?

1. Retain the CLI (Recommended) — preserve current code and task history; revise the planning documents after the relevant stage approval.
2. Plan the web product — treat the README as proposed intent and define the migration scope before any implementation.
3. Defer the direction — preserve both records and pause dependent planning until the product direction is known.

Reply with a number or your own answer.
```

### Preservation evidence

The standard-library comparison asserted equality of all eight original file
hashes, Git HEAD, branch refs, worktree listing, raw index hash, and source diff.
It also checked both original tracker IDs and checked the exact added paths.
All assertions passed.

| Original file | SHA-256 before and after (equal) |
| --- | --- |
| pyproject.toml | `ea2e1d43716440eddbea7a9b492a389f249349cbd5b590e161f246b0e0f115a6` |
| count_cli.py | `9371b51583f48a649cc9d69c527d9fd924555cc5aa390090db5c146b581f8f23` |
| README.md | `533f4aaf399e34b726c4f14c00747d49f6fbf58f89ac59d961f85cec3b611981` |
| TASKS.md | `f1505cebde217ef88263b1d245ee16b2365c277dde769e781ef9a154e201b88a` |
| AGENTS.md | `6af33fdddbaccbc6b483438e7cab7f6abb7bddaea2c49a1d097a695314d8bb96` |
| .gitignore | `5ccde98fdacb0e7c1106c9c5fe3d3d936d0741e63eeadd5e82389f8b93549afe` |
| user-notes.txt | `cb12806da200443e3f15dda8d7419a6d1f4e58afa674c745a309d98ddfada78f` |
| .local-cache/scratch.txt | `e2d8a0533f13447d031fd96be09e60c155f5d289980e2f5f8b4713b7ee76a58a` |

Git index SHA-256 before and after:
`86970ce9b0cd585f1293e01ea7c5de0df9fb2bb494f1816cac6cc7f8a83e4b1d`.
HEAD and sole branch ref before and after:
`refs/heads/dev 3a024f8e4a270e82b13cd60dd16b5ce2764d8092`.
Worktree listing before and after named only the original fixture root at that
revision on dev. The source diff before and after contained the same two added
lines: a blank line and the user's missing-file-work comment.

Before:

```text
 M count_cli.py
?? user-notes.txt
!! .local-cache/scratch.txt
```

After:

```text
 M count_cli.py
?? .project-kickoff/DISCOVERY.md
?? AUDIT.md
?? CONTEXT.md
?? user-notes.txt
!! .local-cache/scratch.txt
```

Runtime tests: **NOT RUN**. File/Git preservation comparison: **RUN AND PASSED**.
No branch, tracker, product code, original README, or configuration mutation was
observed during the audit. This proves this bounded worker run; it does not prove
that every future model invocation will follow the prose skill.

## Changed-decision replay

Scenario input: the problem and users are approved, the technical stage selected
cloud/Postgres, and the user now says: “Use device-local offline storage with no
network; update the kickoff.” This replay drafts the next reply and record plan;
it does not claim to have executed a second project migration.

Exact next reply:

```text
I’ll record device-local offline storage and no network as the new constraint. Your approved problem and users remain valid. The cloud/Postgres design and affected plan sections need revision.

Does the first release need to bring existing cloud data onto the device?

1. Support a user-supplied local export (Recommended) — preserve existing data without giving the application network access; define the file format next.
2. Start with device-local data only — keep the first release smaller; existing cloud data stays outside this release.

Reply with a number or your own answer.
```

The recommendation preserves possible existing data without assuming that such
data exists. The question resolves migration scope, not whether the already
instructed offline/no-network direction should be adopted. No network-enabled
sync, cloud database, storage engine, export format or data-deletion choice is
silently selected.

Planned record changes under the current skill:

1. Inspect saved decisions, approvals, artifact versions and pending question.
   Record the user's exact instruction as the new answer/source. Supersede the
   cloud decision in the decision history with the approved device-local,
   no-network constraint. Withdraw a now-inapplicable pending cloud question.
2. Preserve APR-001 and its problem/users baseline. Mark APR-004's dependent
   cloud blueprint invalidated. Invalidate affected portions of other existing
   stage approvals only if their actual dependency records show an impact;
   do not invent a previously approved stage 5.
3. Record the impact on PRD architecture/data/integrations/deployment, relevant
   DESIGN network/sync behavior, PLAN cloud tasks and verification, and any
   existing derived PRODUCT/setup/handoff sections. Preserve old baselines,
   stable IDs, unrelated decisions, tracker status and historical evidence.
4. Save the single data-migration-scope question and set CONTEXT to revising /
   awaiting that answer. The explicit instruction authorizes recording the
   offline direction; unresolved storage and migration consequences still need
   decisions. Keep stale derived sections visibly invalidated rather than
   claiming the former cloud design remains approved.
5. After consequential choices and the revised dependent stage bundle are
   approved, merge affected document revisions, reconcile approved delta tasks,
   and refresh setup/handoff receipts if applicable. Product migration code,
   package setup, tracker switch, cloud data changes and infrastructure cleanup
   are not side effects of the new constraint.

## Retained fixture output

The following is the actual generated AUDIT.md, retained here before deleting
the disposable synthetic fixture. File paths refer to that historical fixture.

<details>
<summary>Generated AUDIT.md</summary>

```markdown
# Synthetic Count — Existing Project Audit

Status: Awaiting decisions
Version: 1
Updated: 2026-09-06
Auditor / host: independent delegated review worker / Codex
Generated with: project-kickoff 0.1.0 at d31621052f1f1a9b4b23ab1b0ad6d5c584456dce
Base revision: 3a024f8e4a270e82b13cd60dd16b5ce2764d8092, plus the preserved local source edit below.
Audit depth: Focused static audit. No application, installation, build, or runtime test was run.

## Entry decision and boundary

The synthetic test instruction requests audit followed by the next single decision.
Product code, configuration, tracking, branch names, and user files are outside the mutation scope. Only this audit and discovery/context planning records are produced. Any approved application change belongs in a later plan and Agent-Team handoff.

## Current project state

The intended directory and actual Git root both resolve to `/tmp/project-kickoff-existing-ue4mi0fj`. Git reports one checkout and one branch, `dev`, at the base revision. `AGENTS.md:3` explicitly designates `dev` as canonical. There is no `main` branch and no configured remote. No branch choice is pending.

Before audit, `count_cli.py` has one uncommitted added comment about missing-file handling. `user-notes.txt` is untracked; `.local-cache/scratch.txt` is ignored. All are preserved. Notes and ignored cache contents are not used as product evidence. `AGENTS.md` assigns the existing `TASKS.md` tracker to the project orchestrator. No setup receipt exists.

| Area | Observed source or manifest | Documented intent | Target / evidence limit |
| --- | --- | --- | --- |
| Interface | `count_cli.py:5-9` defines argparse input, local text-file reading, and a line-count print | `README.md:3` says React dashboard | Target pending OQ-001; application unrun |
| Stack | `pyproject.toml:5-16` declares Python >=3.10, no runtime dependencies, setuptools build, and `count-lines = count_cli:main` | README says Node.js API and PostgreSQL | Python packaging declared; installed state and packaged command unverified |
| Data / network | Inspected source reads one user-selected local file; no write, database, or network call appears in that file | README names PostgreSQL | No network or data-safety runtime claim; no cloud deployment inferred |
| Errors / accessibility | argparse provides an input surface; local file read has no explicit OSError handling | `LEGACY-23` tracks better missing-file errors | Error behavior and assistive-tool usability untested |
| Operations | No package.json, lockfile, test suite, or CI file was found in this bounded file inventory | README advertises npm installation and development commands | Commands are unverified and do not match supplied manifest; no deployment evidence |

## Document and ID reconciliation

| Existing artifact or ID | Contract comparison | Preservation / next decision |
| --- | --- | --- |
| README.md | Present, conflicts with observed Python source and manifest | Preserve until direction and stage approval; AUD-001 |
| PRD.md / DESIGN.md / PLAN.md | Absent; no approved users, journeys, acceptance criteria, nonvisual contract, or task graph was supplied | Record as missing kickoff inputs; resolve through stages without inventing evidence |
| AGENTS.md | Provides canonical branch, single tracker, writer, and preservation policy | Retain useful policy; any approved additions must merge |
| CLAUDE.md / CONTEXT.md / MISTAKES.md / discovery | No existing files before audit | Create only discovery/context records for this question; adapter and lessons remain future approved setup |
| .agent-team/setup.json | Absent | Current tracker is identified by project instructions; no initialization or migration |
| LEGACY-17 / R-COUNT | Existing row says completed, with historical owner acceptance and no attached runtime log | Preserve exact row and ID; this audit does not retest or reopen it; PLAN mapping absent |
| LEGACY-23 / R-ERROR | Existing row says in_progress, for missing-file error improvement | Preserve exact row and ID and source edit; acceptance and PLAN mapping remain unresolved |

## Findings

### AUD-001 — README describes a different product stack

- Category: documentation / product direction.
- Current state: source and manifest define a Python local-file CLI; README claims a React / Node.js / PostgreSQL web product and gives npm commands.
- Evidence: `count_cli.py:5-9`, `pyproject.toml:5-16`, `README.md:3-4` at the base revision plus the inspected working copy.
- Test state: not run — static comparison only.
- Severity: Medium. A maintainer can select the wrong setup and plan a different product from the available source.
- Priority: Now, before dependent planning or setup.
- Confidence: High for the contradiction. The intended target and whether a web product exists elsewhere remain unknown.
- Recommendation: retain the source-backed CLI baseline and merge corrected orientation after relevant approval. Planning a web transition adds scope and requires its own definition.
- Decision: OQ-001; proposed DEC-001, not approved.
- Affected requirements / tasks: R-COUNT and R-ERROR may remain valid; no new task created.

### AUD-002 — Completed task has no attributable runtime evidence in this checkout

- Category: testing / delivery evidence.
- Current state: LEGACY-17 records historical acceptance, but no test suite or attached runtime log is present in the inspected inventory.
- Evidence: `TASKS.md:8` and the bounded file inventory at the base revision.
- Test state: not run — no CLI, build, install, or test execution authorized in this audit.
- Severity: Low. Current behavior cannot be reported as freshly verified; the task's historical status remains intact.
- Priority: Before an implementation readiness claim, if fresh verification is needed.
- Confidence: High for the absence of local attributable evidence; external or historical evidence may exist.
- Recommendation: retain task history and seek existing evidence or plan delegated checks after scope approval. Do not reopen completed work merely for this audit.
- Decision: Later verification-stage consequence; no second question asked now.
- Affected requirement / task: R-COUNT / LEGACY-17.

## Current-to-target decisions and approved retrofit

DEC-001 is proposed only: retain the CLI and reconcile documentation. The web direction and deferral remain explicit alternatives. No target architecture, remediation, stage approval, tracker migration, or code change is approved by this audit. Approved retrofit mapping: none.

## Checks and limits

- Run and passed: Git root/branch/worktree/state inventory and static source/manifest/document/tracker inspection.
- Not run: CLI, packaging, dependency installation, unit or integration tests, error-path execution, network checks, accessibility execution, and deployment checks.
- No external source research was needed to report the direct local contradiction. No stack or license recommendation is being verified here.
- This is a focused static audit, not a complete security or product-quality assessment. No sensitive file content was reproduced.
- Practical concise-language guidance applied; no authorized ASD-STE100 standard was checked and no formal compliance is claimed.
- Pending question: OQ-001, recorded in `.project-kickoff/DISCOVERY.md`.
- Next action: wait for the single product-direction answer below; do no dependent setup.

Should the kickoff retain the Python CLI as the product baseline and reconcile the conflicting README?

1. Retain the CLI (Recommended) — preserve current code and task history; revise the planning documents after the relevant stage approval.
2. Plan the web product — treat the README as proposed intent and define the migration scope before any implementation.
3. Defer the direction — preserve both records and pause dependent planning until the product direction is known.

Reply with a number or your own answer.
```

</details>

## Limitations and cleanup

This review covers the named source revision and bounded static fixture audit.
No dependency readiness, current external host documentation, legal validity,
release archive, GitHub publication, live host discovery, install flow or product
runtime is certified. New-project full interview and tracker creation/retry were
reviewed as contracts, not re-executed here. The changed-decision reply is an
explicit replay, with planned record changes, not observed application results.

The original package source was not edited. The only deliverable changed in the
worker worktree is this new report; the old behavior report was not modified.
Fixture cleanup confirmation will be recorded below after synthetic-only removal.

Cleanup verified: removed only the fixture and evidence directories created by this worker, after confirming the expected synthetic file inventory and retaining the audit, hashes, Git states and exact question in this report. No temporary fixture or review-state file remains.
