# Hook audit decisions

Audit baseline: project-kickoff 0.1.0, source `daf472d`.

The user requested findings one at a time, with a decision before each
conversion. Approval for one finding does not authorize other conversions.
After approving finding 2, the user changed the execution sequence: finish all
finding decisions first, then implement the approved changes together. Until
then, update only the audit decision record; do not implement queued changes.

## Finding 1 — Load saved kickoff context

Decision: approved. The user answered "yes" to the proposed read-only
context-loading hook.

Add a small shared command hook with separate Codex and Claude Code setup
examples. On supported SessionStart events, load a bounded excerpt of existing
kickoff records for an explicitly enabled project. Missing or inconsistent
records produce factual diagnostics. The hook does not change files, infer
approval, answer a question, install tools, or start setup.

Keep instructions for verifying saved state against the current project. Keep
manual resumption when hooks are disabled, unsupported, or not trusted. Existing
host configuration and hooks must survive setup. Enabling hooks in a generated
project follows that project's approved scope and normal host trust controls.

Implementation uses a task worktree, meaningful script tests, and independent
review before integration. This compatible capability increments the skill to
0.2.0. The 0.1.0 release remains unchanged.

Primary interface references checked during audit:

- https://learn.chatgpt.com/docs/hooks
- https://code.claude.com/docs/en/hooks

Finding 1 was implemented before the user requested deferred implementation.
The revised execution sequence above applies to all remaining findings.

Implementation and independent review are complete for finding 1. Fourteen
script tests pass. An independent existing-template fixture confirmed 0.1.0
checkpoint compatibility. A fence-parsing defect was reproduced and fixed.
The host examples and runtime file lists passed review. See
[implementation checks](context-hook-checks.md) and
[independent review](context-hook-review.md) for evidence and limits.

The optional script needs Python 3.9 or later on Linux, macOS, or WSL. Native
Windows retains manual resumption. Native CLI hook sessions were not exercised;
the tests executed event-shaped inputs and the example command definitions.
No hook was activated in the skill repository or global host configuration.

Published [v0.2.0](https://github.com/thebpandey/project-kickoff/releases/tag/v0.2.0)
from source `698489791878fd64386a32b34bfb043e3fb81903`. The extracted ZIP has
exactly 27 runtime files matching that commit; all 14 integrated tests passed.
GitHub's uploaded ZIP digest matches the local SHA-256:
`a61331eafeaebe0ac6b02df92de3a93df1550c3ee25ac8f02d8a480d608f602b`.
The repository remains private. Remote main and the peeled release tag matched
the release source. The uploaded checksum file's digest also matches its local
copy. The three clean, integrated task worktrees and branches were removed
through normal Git operations. The 0.1.0 release and local archive were preserved.

## Finding 2 — Guard direct edits in the canonical checkout

Decision: approved; queued for the combined implementation after all findings
have been decided. No implementation has started.

Proposed PreToolUse guard checks supported file-edit destinations, permits
approved canonical planning/shared-record changes, and blocks product source
and application configuration edits in the canonical checkout. Direct the agent
to an approved worktree. The guard does not create or remove worktrees. Preserve
the broader instructions: arbitrary shell commands and external processes are
outside a complete file-edit-hook enforcement claim.

## Finding 3 — One-question interview and approval interpretation

Decision: approved — retain the conversation and approval rules as skill
instructions. The user answered "yes" to keeping these rules as instructions.
Counting structured question entries can catch
batched tool questions, but does not establish one semantic decision per question
or whether a free-text answer approves the current scope. A Stop hook that
continues the agent while a question is pending can conflict with yielding to
the user. No hook conversion is proposed for this finding.

## Finding 4 — Validate checkpoint structure after edits

Decision: approved; queued for the combined implementation after all findings
have been decided. Add an opt-in read-only PostToolUse check after supported
edits to CONTEXT.md or .project-kickoff/DISCOVERY.md. Reuse the
existing bounded checkpoint-reading logic where practical. Check the edited
record for missing expected phase/pending-question/next-action fields,
conflicting pending-question entries, and size limits that prevent resumption.

Report concise advisory diagnostics. Do not rewrite records, infer answers or
approval validity, block waiting for the user, or force continuation through a
Stop hook. Treat temporarily inconsistent records during a multi-file update as
unconfirmed; avoid claiming that an intermediate state is a final defect. Keep
manual validation for unsupported edit paths and adapted formats. This checks
structure, not semantic freshness or truth. No implementation has started.

## Finding 5 — Protect shared records from subagent edits

Decision: approved; queued for the combined implementation after all findings
have been decided. Extend the finding 2 PreToolUse guard to
reject supported direct edits by positively identified subagents to canonical
MISTAKES.md, CONTEXT.md, TASKS.md (when selected), and .agent-team/TEAMS.md.
Allow their assigned context or handoff paths under the existing ownership
policy. Return a concise instruction to submit the update to the project
orchestrator. Use the same guard rather than a second overlapping hook.

This is a limited subagent write guard, not proof of universal single-writer
enforcement. Claude Code documents agent_id on subagent hook calls. Codex's
shared session_id alone cannot distinguish the writer; do not infer identity
from cwd, branch names, missing fields, or transcript heuristics. Enable actor
checks only where the selected host supplies a verified identity signal.
Otherwise retain the single-writer instructions and report the coverage limit.
Arbitrary shell writes and external processes remain outside this claim.
No implementation has started.

## Finding 6 — Keep cleanup tied to verified integration

Decision: approved — retain cleanup as an explicit orchestrator-run workflow
in the instructions. The user answered "yes" to this recommendation.
Do not convert deletion of
worktrees, branches, or processes into automatic Stop, SessionEnd, SubagentStop,
or WorktreeRemove actions.

A lifecycle event does not establish verified integration, resource ownership,
preservation of required evidence, or a clean worktree including ignored files.
Codex SessionEnd can occur on closure or idle expiry. Claude WorktreeRemove can
occur at session exit or subagent completion and cannot block removal. These
are not equivalent to the skill's integration boundary.

Keep cleanup immediate after verified integration within the existing approved
scope, independent of deployment. Preserve uncertain resources and explain why.
This recommendation adds no repeated user-approval gate for already-authorized
cleanup and proposes no automatic deletion hook. No implementation has started.

## Finding 7 — Keep tracker initialization and seeding explicit

Decision: approved — retain tracker initialization, seeding, and reconciliation
as explicit orchestrator-run setup steps. The user answered "yes" to this
recommendation. Run these steps after the tracker
choice and exact plan revision are approved. Do not attach these mutations to
SessionStart, PostToolUse on PLAN.md, or other lifecycle events.

Repeated or concurrent hook invocations do not themselves provide exactly-once
creation or serialized reconciliation. A saved or edited plan can still be a
draft. Preserve the existing ID mapping, partial-recovery, parent/blocker, and
single-active-tracker contracts. Missing dependencies still require the user's
fallback selection before activation. Continue independent work while waiting.
This recommendation changes no tracker and adds no recurring approval gate for
already-authorized seeding. No hook or new seeding helper is proposed here.

## Finding 8 — Keep dependency selection and installation explicit

Decision: approved — retain dependency discovery, selection, installation,
verification, and upgrades as explicit approved setup steps. The user answered
"Yes" to this recommendation.
Do not install, repair, replace, or upgrade dependencies from session hooks.

The setup contract requires verified sources, versions, scope, license/access
conditions, reuse of compatible installations, and a factual setup receipt.
Missing tools can require a user-selected alternative. An automatic installer
would need to duplicate these decisions and the delegated-worktree workflow.
Claude Code has an explicit Setup event for predetermined preparation; its
availability does not make this adaptive selection process a good hook target.

Keep approved installations delegated to appropriate task worktrees. Preserve
existing pins, settings, and lockfiles, verify actual usability, and continue
independent planning when a dependency is unavailable. Proceed within recorded
authorization without repeated permission requests. This finding proposes no
automatic installer or additional dependency-check hook.

Primary interface reference checked for this finding:
https://code.claude.com/docs/en/hooks-guide

## Finding 9 — Keep writing quality and STE review in the instructions

Decision: approved — retain concise writing, consistent terms, and ASD-STE100
review as instructions and document-review steps. The user answered "Yes" to
this recommendation. Do not add a
blocking style hook or automatic prose rewrite.

Sentence length and word lists can support review, but do not establish correct
word meanings, parts of speech, technical terminology, or preservation of an
approved requirement. A simplistic check can flag valid names, commands, paths,
tables, and technical terms. Automatic rewriting can change agreed meaning.

Keep short active sentences and clear terminology. Preserve exact identifiers,
commands, quotations, and requirement detail. Use the applicable standard and
dictionary for an actual STE check and record its scope; a general style review
must not be reported as formal compliance. This finding proposes no additional
linter dependency or hook. Implementation remains deferred.

Primary reference checked for this finding:
https://www.asd-ste100.org/STE_faq.html

## Finding 10 — Keep lesson creation under orchestrator review

Decision: approved — retain MISTAKES.md maintenance as an orchestrator
responsibility. The user answered "yes" to this recommendation.
Do not automatically append lessons from failed
tool calls or task-completion events.

A failed command can be an expected negative test, an exploratory check, or an
external outage. Failure alone does not establish an agent mistake, its cause,
a verified correction, or a reusable prevention step. Successful tool calls can
also contain mistakes. An automatic ledger writer would bypass the existing
single-writer and evidence-review process.

Keep attempt history and blockers in the selected tracker. Teammates submit
candidate lessons with evidence through their existing handoff channel. The
orchestrator assesses applicability, merges duplicates, records uncertainty,
and maintains stable lesson IDs. Preserve the existing requirement to read
relevant lessons before work and retries. Finding 5 still guards supported
subagent writes; this finding concerns how lessons are selected and recorded.
No automatic lesson writer, extra failure log, or hook is proposed. This adds
no user-approval requirement for routine lesson maintenance. Implementation
remains deferred until all findings have been decided.

## Finding 11 — Keep the final readiness gate evidence-based and explicit

Decision: approved — retain the final readiness gate as an explicit
orchestrator review before declaring ready for handoff. The user answered
"yes" and requested Agent-Team implementation of all approved changes. This is the
last finding in this audit. Do not automatically approve readiness, start
Agent-Team, or force continuation from a lifecycle hook.

File presence, expected headings, and a saved ready-state label do not establish
current stage approvals, consistent approved scope, verified scaffold checks,
working dependencies, complete tracker mappings, or actionable task readiness.
Existing projects can use adapted documents and established IDs. Audit-only
completion does not require the implementation-handoff artifact set.

Keep the readiness checklist in references/handoff.md. Review the applicable
documents, selected tracker, and evidence against the current project revision.
Report blockers and verification limits; provide the exact Agent-Team invocation
only as a handoff instruction, without starting implementation. Preserve the
healthy-existing-project outcome where evidence shows no implementation remains.
Finding 4 covers bounded checkpoint structure diagnostics and does not certify
handoff readiness. No additional hook or standalone readiness checker is
proposed. The existing manual context-hook deactivation step remains part of
completed handoff. All remaining implementation stays deferred until the user
decides this final finding. That decision is now complete; the combined
implementation of findings 2, 4, and 5 is authorized.

## Combined implementation scope

All eleven findings are decided. Finding 1 shipped in 0.2.0; findings 2, 4,
and 5 will ship together in 0.3.0. Findings 3 and 6 through 11 remain explicit
instructions. Retain their behavior and document the hook boundaries.

The user also requested a solid filled-block wordmark like Agent-Team, with the
loaded skill version and attribution to thebpandey below it, displayed at Skill
invocation and the completed final report. Use a plain-text # fallback when
block characters are unsupported. Keep the display in instructions, not hooks.

Use a developer task worktree and independent review, then integrate, verify,
package, and publish to the already authorized private repository. Preserve
existing releases, licensing, manual workflows, and host trust controls. Do not
activate hooks in this repository or change global host configuration.
