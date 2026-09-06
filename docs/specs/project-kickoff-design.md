# Project Kickoff — Draft Skill Design

Status: Approved by the user on 2026-09-06, including the implementation design
and LICENSE. Build, validation, packaging, and private GitHub publication are
authorized.

## Purpose

Create a reusable `project-kickoff` skill for Codex and Claude Code. Turn a
user's idea into an approved product definition, design vision, technical
blueprint, and implementation handoff for `agent-team`.

## Confirmed decisions

1. Support any software project. Adapt discovery to web, mobile, desktop,
   API, CLI, and library projects. Apply visual UI/UX work when relevant.
2. End kickoff with approved documents and a minimal scaffold: folders,
   basic tooling, Git, agent instructions, dependency setup, and task tracking.
   Product feature implementation belongs to the subsequent agent-team run.
3. Use project-scoped instructions and skill installations where supported.
   Reuse suitable installed tools. Explain tools that require user-level setup.
4. If a dependency is unavailable, continue independent work. Suggest
   `TASKS.md` as a Beads replacement. Research comparable free or open-source
   alternatives and explain relevant trade-offs. Wait for the user's choice
   before adopting a substitute. Do not report a failed installation as ready.
5. Prepare a private repository at `github.com/thebpandey/project-kickoff`.
6. Use a custom proprietary license. The owner's explicit permission authorizes
   use; no paid entitlement is required. Permit commercial application
   development. Require permission to modify or redistribute the skill.
7. Fully detail the approved first release in `PLAN.md`. Outline later phases
   separately until approved for implementation.
8. Use the five-stage adaptive interview below, with one question at a time,
   stage approvals, and saved progress for interrupted sessions.
9. Use Bhaskar Pandey and Almora Technology, LLC as copyright holders, with
   support@learnstackos.com as the permission contact.

## Required project outputs

- `PRD.md`: Product definition; users and problems; scope; expected outcomes;
  observable acceptance criteria; constraints; approved technical and
  architectural decisions; technology choices; folder structure.
- `DESIGN.md`: Design, brand, and styling guidance. Adapt to the actual
  interface; do not invent screens for a project without a visual interface.
- `PLAN.md`: First-release epics, user stories, actionable tasks, dependencies,
  acceptance criteria, and verification. Separate future roadmap ideas.
- `AGENTS.md` and `CLAUDE.md`: Consistent project instructions for both hosts,
  dependency use, decision approvals, communication, delegation, and cleanup.
- Beads initialized from the approved plan, or a user-selected replacement.
- `MISTAKES.md`: Shared lessons maintained by the project orchestrator and
  available to all teammates.
- `CONTEXT.md`: Current resumption notes maintained by the project orchestrator.
- Additional setup records and handoff information where needed to make the
  project ready for implementation.

## Required operating rules

- Ask one question at a time. Give recommended answers as choices with useful
  trade-offs. Wait for the user's response before asking the next question.
- Obtain user decisions or approval before proceeding with dependent work.
- Preserve answers and approvals across sessions. A timeout is not approval.
- Apply ASD-STE100 to concise explanations. Verify the applicable source and
  distinguish practical writing guidance from any formal compliance claim.
- Keep the canonical local main checkout for planning and discussion. Use
  subagents in separate worktrees for code execution, with model and reasoning
  effort appropriate to task complexity and actual host capabilities.
- Clean up completed worktrees and branches after verified integration into
  main. Preserve unfinished work, user changes, and required evidence.
- Initialize tracking from `PLAN.md`; keep one authoritative execution tracker.
- Prepare a clear agent-team handoff without starting product implementation.

## Requested dependency set

- Ponytail
- Using-Superpowers
- Beads
- Agent-Team
- Impeccable
- UI UX Pro Max Skill

Check installed copies and authoritative sources before selecting installation
methods. Install missing dependencies within the agreed scope. Recommend
additional skills only when they add a concrete capability. Confirm current
licenses before describing an alternative as free or open source.

## Approved interview flow

Use five stages, with project-specific follow-up questions:

1. Product definition: problem, intended users, current alternatives, value,
   evidence, and the riskiest assumptions.
2. First-release scope: user journeys, priorities, exclusions, measurable
   outcomes, acceptance criteria, budget, schedule, and other constraints.
3. Experience and design: interaction needs, accessibility, brand direction,
   reference examples, and interface-specific states and behavior.
4. Technical blueprint: stack options, architecture, data, integrations,
   security, deployment, operations, and folder structure as relevant.
5. Execution and handoff: task breakdown, dependencies, verification, skill
   setup, agent rules, tracking, and readiness for agent-team.

Ask only unresolved questions. Challenge weak assumptions with reasons and
alternatives. Summarize each stage and ask for approval as its own question.
Do not impose a fixed question count; detail follows the project's needs.

Maintain a small discovery checkpoint from the beginning. Record confirmed
answers, approval state, unresolved decisions, and the pending question.
On resume, restore that state and continue with the pending decision.

## Integration decisions

- The installed Agent-Team supports a local `TASKS.md` tracker and requires one
  authoritative tracker. Its default path is `.agent-team/TASKS.md`, but it can
  use a user-designated path. Offer root `TASKS.md` as the requested fallback
  and record its canonical location in the Agent-Team setup receipt.
- Agent-Team keeps shared mistakes under one orchestrator writer and uses
  per-agent context notes. Reuse its compact lesson fields and context fields.
  Start MISTAKES.md with instructions and an empty index, not invented lessons.
- Agent-Team's current cleanup procedure is tied to production verification.
  This project's requested rule is cleanup after verified integration into
  main. State that project rule explicitly in generated instructions.
- The installed Impeccable expects product context as well as `DESIGN.md`.
  Generate a compact derived `PRODUCT.md` only when the selected Impeccable
  version requires it. Identify PRD.md as its source, record that revision, and
  refresh the derived summary when relevant approved product decisions change.
- Third-party dependencies retain their own licenses. The custom license must
  distinguish the skill package from generated project files and third-party
  materials.

## Package and readiness checks

Keep one shared `SKILL.md` entrypoint for both hosts. Put the detailed interview,
artifact requirements, dependency setup, host differences, and handoff procedure
in focused reference files. Include project document templates, Codex UI metadata,
installation instructions, and the custom license. Do not bundle third-party
skills under the proprietary license.

The skill must distinguish discovery, approved planning, setup, and ready for
handoff. During discovery, write only planning and checkpoint records. Perform
dependent setup after the relevant decisions are approved. Resuming must inspect
existing artifacts and task IDs rather than repeat initialization or seed tasks
again. A changed decision invalidates affected approvals and derived documents;
unrelated approved decisions remain valid.

Use stable requirement and plan-task IDs. Map first-release requirements to
observable acceptance criteria and implementation tasks. Map plan IDs to the
selected tracker's IDs, check dependency direction and cycles, and verify that
future roadmap ideas did not become active implementation tasks. `PLAN.md` owns
the approved baseline; the selected tracker owns execution status.

Before handoff, check document consistency, unresolved decisions, prerequisite
availability, scaffold scope, tracker coverage, shared-record ownership, and the
first actionable task. Supply the exact invocation appropriate to the current
host. Do not start agent-team as a side effect of preparing the handoff.

Validate the package format and references. Use bounded behavioral scenarios for
one-question waiting, interruption recovery, a project without visual UI, missing
dependencies with user-selected alternatives, repeated setup, changed scope, and
worktree cleanup that preserves unfinished changes.

## Artifact contracts

PRD.md must distinguish user-approved decisions from evidence, assumptions, and
open questions. Include the first-release boundary, non-goals, user journeys,
requirement IDs, success measures, constraints, architecture and its rationale,
stack alternatives and the selected stack, data ownership, integrations,
project-relevant security needs, deployment assumptions, and the folder tree.
Do not invent market evidence, budgets, delivery dates, or performance targets.

DESIGN.md must translate the approved experience into actionable guidance:
audience, brand voice, interaction principles, information structure, user flows,
and relevant accessibility requirements. For visual interfaces, add typography,
color and semantic tokens, spacing, layout, responsive behavior, component
states, content guidance, and motion rules. For CLI/API/library work, address
appropriate interaction, errors, documentation, and naming conventions; explain
why visual sections do not apply.

PLAN.md must give each first-release task an ID, parent epic or story,
requirement links, intended outcome, prerequisites, implementation steps,
affected paths or boundaries, acceptance criteria, verification, and an effort
or complexity estimate with its assumptions. Identify parallel work only when
the tasks can proceed independently. Separate roadmap ideas from runnable work.
Avoid task counts or line counts as proxies for completeness.

AGENTS.md is the common project policy. CLAUDE.md must load or reference it
through the host's supported mechanism and add only necessary host differences.
The rule to read the common policy must work even if automatic imports are
unavailable. Keep project decisions above conflicting dependency preferences
within the host's instruction hierarchy; do not claim project files override
system instructions or tool controls.

CONTEXT.md holds the current phase, canonical locations, approved decisions and
their sources, blockers, pending question, and next action. It links to the
tracker rather than duplicating task history. Each teammate maintains its own
resumption notes in its assigned location; shared project records have one
project-orchestrator writer.

Keep detailed interview answers and stage approval records in
`.project-kickoff/DISCOVERY.md`, referenced by CONTEXT.md. Record source, date,
status, and affected artifact for each material decision. Keep credentials and
raw sensitive data out of both files. Store dependency setup choices in the
canonical `.agent-team/setup.json` where compatible, preserving unrelated fields.

Provide a short project README for orientation and handoff. Add an appropriate
`.gitignore` and example environment variable names only when the chosen tooling
needs them. Never include actual credentials. Include launch or check commands
only for tooling actually created and verified. A minimal scaffold may have
no runnable application yet; state that clearly.

## Execution boundary and cleanup

Detect the project root and actual Git repository before initialization. Do not
adopt an unrelated ancestor repository or overwrite an existing project. Create
an initial main commit for approved planning files so worktrees can be created.
Allow the orchestrator to read files and maintain planning, tracker, and context
records on canonical main. Treat package installation, scaffold code/config
changes, builds, tests, and executable helper work as delegated code execution.

Use a task-specific subagent worktree for scaffold execution. Use a separate
integration worktree for code combination and checks, then update canonical
main through the authorized process. Resolve model and effort from actual host
capabilities. If delegation is unavailable, continue planning and ask for the
missing capability or an explicitly approved exception before code execution.

After verified integration, stop task-owned processes, preserve evidence,
inspect tracked/untracked/ignored content, remove eligible worktrees normally,
and delete only verified integrated task branches. Handle squash integration
with explicit revision/diff evidence instead of assuming Git ancestry proves it.
Do not force removal past uncertain or uncommitted content. Preserve unrelated
branches, main, active tasks, and evidence. Remove an idle integration worktree
when eligible; keep at most one while needed. Record retained resources and why.
Production deployment is a separate decision and does not gate this requested
post-integration cleanup rule.

## Dependency and research policy

Present the requested six dependencies with actual availability, purpose,
source, version or revision, installation scope, and relevant license/access
conditions. Reuse compatible installations. Scope affects installation, while
task relevance affects which skills are invoked. Do not invoke UI skills for
backend-only work just to satisfy the dependency list.

Install approved missing dependencies sequentially where they share an install
store. Read current official setup instructions and check the selected executable
or skill plus its required supporting files. A folder or successful download is
not a working installation. Keep proprietary Agent-Team access distinct from
open-source dependencies; do not assume permission to redistribute it.

For an unavailable dependency, continue independent work, report the cause, and
offer TASKS.md where Beads would apply. Research suitable current free/open-source
alternatives from authoritative sources and state capability gaps. Do not claim
a paid, unavailable, or unverified product is a free equivalent. If no suitable
alternative is verified, say so. Ask for the user's choice once, preserve it,
and activate only the selected tracker. Retain and reconcile existing task data
before switching trackers. Do not switch back automatically after a recovery.

Research uncertain product assumptions and current stack facts with focused,
non-sensitive queries. Cite sources and dates in the decision record. Label
inferences and unverified assumptions. A project needing substantial market or
domain research can add that work before approval; do not substitute fabricated
findings when browsing or domain access is unavailable.

## Communication and host portability

Use short, active sentences, consistent terms, and explanations of unfamiliar
technical words. Preserve official names, commands, and identifiers. Apply the
ASD-STE100 standard when an authorized copy is available; do not label a simple
style check as certified compliance or bundle the standard's dictionary.
Detailed artifacts remain detailed; concise language must not remove necessary
acceptance criteria or architecture explanations.

Use each host's actual skill discovery and invocation capabilities. Codex and
Claude Code share the skill content but have separate installation guidance.
Use native question choices where available. Otherwise ask one plain-text
question with recommended choices and end the turn. Never issue the next
question while an answer remains pending. Free-text choices remain valid.

## License design

The draft [LICENSE](../../LICENSE) requires explicit recorded permission, permits
commercial and client development, and prohibits unauthorized redistribution or
modification of the Skill. It permits installation copies and normal AI-tool
processing. Generated project files and template-derived project instructions
can be edited and distributed, including commercially, without transferring the
Skill package. Third-party licenses remain separate. No paid entitlement,
subscription, automatic future-update right, or runtime license server is added.

The draft states terms; it does not promise that technical access controls or
license wording can prevent every unauthorized copy. Legal drafting references:
[U.S. Copyright Office, Chapter 1](https://www.copyright.gov/title17/92chap1.html)
and [GitHub repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## Build and delivery acceptance

1. The package has valid skill metadata, resolvable local references, complete
   templates, host installation instructions, and the agreed license.
2. Independent bounded scenarios verify interview waiting and resumption,
   non-visual projects, dependency failures and approved alternatives, repeat
   setup without duplicate tasks, changed-decision handling, and cleanup safety.
3. Any executable helper is checked for meaningful behavior. Do not introduce
   custom installation or tracker frameworks when host tools suffice.
4. The release includes only intended skill files, with no third-party skill
   copies, credentials, local agent state, or temporary test artifacts.
5. Initialize an isolated repository for this package, use main as its canonical
   branch, and preserve unrelated ancestor-repository contents. Verify private
   GitHub visibility and the intended destination before pushing the validated
   release. Report the actual published revision or any access limitation.

Host documentation checked:
[Codex skill documentation](https://developers.openai.com/codex/skills) and
[Claude Code skills](https://code.claude.com/docs/en/skills).

## Source checks and optional recommendations

Checked on 2026-09-06. Use current installed-version help during actual setup;
these findings do not freeze future commands or authorize installations.

- [Beads](https://github.com/gastownhall/beads): The installed `bd` is 1.1.2.
  Its `init --help` supports skipping agent-file and hook generation, and its
  default backend is embedded Dolt. Reconcile generated host instructions;
  do not assume a separate database server is required. Two `bd` paths exist
  in this environment, so record the selected executable as well as its version.
- [Superpowers](https://github.com/obra/superpowers): Reuse applicable debugging,
  testing, and review skills from this dependency before adding competing
  workflow packages. Installation differs by host.
- [Ponytail](https://github.com/DietrichGebert/ponytail),
  [Impeccable](https://github.com/pbakaus/impeccable), and
  [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
  have authoritative upstream repositories. Include required supporting files,
  not only each entrypoint.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Candidate
  optional security review skills for a relevant project. Select a specific
  capability; do not install the whole collection by default.
- [Agent Browser](https://github.com/vercel-labs/agent-browser): Candidate
  browser verification capability when a UI project lacks usable browser tools.
- [ASD-STE100](https://www.asd-ste100.org/): Consult the official standard for
  the requested communication rules. Do not redistribute its text as part of
  this proprietary package without establishing permission.

The GitHub CLI could not resolve `thebpandey/project-kickoff` with current access.
This alone does not establish whether the repository is absent or inaccessible.
No remote repository was created or changed during these checks.
