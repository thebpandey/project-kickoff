# Safe setup and dependency selection

Read this after the dependent product, scope, design, and technical decisions are
approved. Setup changes only the selected project.

## Resolve the project and Git boundary

1. Resolve the intended project path from the user's request and existing files.
2. Inspect `git rev-parse --show-toplevel`, `git status`, remotes, branches, and
   worktrees. If Git resolves to an ancestor above the intended project and the
   user did not select that repository, treat it as unrelated. Do not add files
   to it or initialize a nested repository until the intended boundary is clear.
3. If the intended project has no repository, initialize Git at that exact path
   only after the approved setup covers it. Use `main` as the new canonical
   branch. For an existing repository, preserve its branch names and record the
   actual designated canonical branch; do not force a rename. Do not overwrite
   an existing repository or files.
4. Create the initial commit on the new repository's `main` branch from approved
   planning and instruction files before worktrees are needed. In an existing
   repository, use its user-designated integration branch and established commit
   process. Follow existing commit authority and hooks. Do not install or bypass
   hooks without matching authorization.

## Inspect before proposing changes

Check the host, operating system, project package manager, installed skills,
executables, versions, supporting files, and project configuration. Reuse a
compatible installation. A directory, download, or successful installer exit is
not proof that a tool works. Use the selected executable's version/help output
and a small functional check where appropriate.

Present these dependencies even when some are already ready:

| Dependency | Purpose | Authoritative source |
| --- | --- | --- |
| Ponytail | Minimal implementation and YAGNI guidance | https://github.com/DietrichGebert/ponytail |
| Using-Superpowers | Existing planning, debugging, testing, and review procedures | https://github.com/obra/superpowers |
| Beads | Dependency-aware implementation tracker | https://github.com/gastownhall/beads |
| Agent-Team | Delegated implementation, integration, and coordination | Use the authorized package source recorded for the installed proprietary copy |
| Impeccable | Product and interface design workflow | https://github.com/pbakaus/impeccable |
| UI UX Pro Max Skill | UI/UX patterns, data, and search tools | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| Serena | Scoped semantic navigation for implementation | https://github.com/oraios/serena |
| Graphify | Code-only repository structure and dependency analysis | https://github.com/Graphify-Labs/graphify |

For each item, show purpose, Ready/Missing/Cannot use status, selected executable
or skill path, source URL, version or exact revision, installation scope and
location, license or access terms, required supporting files, and verification.
Read the current official install instructions and license before proposing an
installation. Agent-Team access is separate from open-source licenses; never
copy or redistribute it based on filesystem access alone.

Prefer project scope. Keep skill folders under the current host's project skill
directory and packages in the project. Do not mutate user-wide stores, global
configuration, global hooks, or system packages unless the user approved that
exact scope. Install sequentially when tools share a package manager or skill
store. Preserve lockfiles, existing settings, and unrelated receipt fields.

For Beads, enumerate all `bd` executables and record the selected absolute path.
Read that executable's current `init`, create, dependency, and setup help. Use
idempotent initialization and options that suppress generated agent files and
hooks when the selected version supports them. Confirm the task prefix, storage
mode, files, and any automatic commit or background-process side effects before
running it. The current default may use embedded storage and need no external
database, but verify the selected version instead of assuming this. Do not use a
destructive reinitialization option to repair an existing tracker. Do not treat
a sandbox flag as proof of offline operation; verify version-specific telemetry
and network behavior or report it as unknown.

Invoke dependency skills only when relevant. A backend-only project does not use
UI skills merely because they are installed. Reuse applicable existing
Superpowers procedures rather than adding competing workflow packages.

## Record setup

Use `.project-kickoff/setup.json` for Project Kickoff's setup receipt. Preserve
unrelated fields. Keep it in the canonical planning checkout and record:

- host and project identity;
- generating `project-kickoff` metadata version and relevant compatibility note;
- tracker mode and canonical absolute path;
- each dependency's source, version/revision, license/access condition, scope,
  selected path, status, verification evidence, and check date;
- declined, deferred, failed, and superseded choices;
- every implementation task plan-ID to tracker-ID mapping and the last seeded
  plan revision. Keep epic and story hierarchy in `PLAN.md`.

Do not store credentials or task status there. The receipt records choices; it
does not grant new permission.

Do not create or edit `.agent-team/setup.json`. Agent-Team owns that file and
creates it atomically with its runtime state during project initialization.
Project Kickoff may read an existing Agent-Team receipt to resume or audit, but
must treat it as read-only.

Initialize and seed the selected tracker as project-orchestrator planning-record
operations in the canonical checkout. This keeps the shared database or task file
outside disposable feature worktrees. Tool-package installation, scaffold code,
configuration, builds, tests, and executable helpers remain delegated execution
in task worktrees and return through integration.

## Missing tools and alternatives

A missing optional dependency does not block independent planning. Explain the
actual failure and continue work that does not need it. For any missing required
capability, research current free or open-source alternatives from authoritative
sources. Compare the needed capability, gaps, maintenance, host support, source,
and verified license. Do not describe an unverified or paid product as a free
equivalent.

For an Agent-Team handoff, the selected tracker must be Beads or Markdown
at root `TASKS.md` or `.agent-team/TASKS.md`. Other researched trackers remain
valid for projects that will not use Agent-Team, but are not compatible handoff
targets for these contracts. Native setup must preserve the selected tracker;
an available Beads executable never authorizes changing an approved Markdown
tracker or discarding an existing task file.

If Beads is unavailable, include root `TASKS.md` as one choice and explain that
it is a simple single-writer file without Beads automation. Present researched
alternatives as separate choices. Ask one question and wait. Do not create,
write, or call any fallback tracker before the user selects it. After selection,
record the choice and activate only that tracker. Retain and reconcile existing
task data. Never switch back automatically when a preferred tool appears later.

One candidate to verify at setup time is
[Backlog.md](https://github.com/MrLesk/Backlog.md), a local Markdown task system
with a CLI and dependency support. Its upstream repository identified it as MIT
when this Skill was prepared. Verify the current revision, license, package name,
and feature gaps before offering it. Do not use an unrelated package returned by
an ambiguous `npx` name. A Superpowers task workflow can help coordinate work,
but it is not a task database or a drop-in Agent-Team replacement; explain that
gap if it is offered.

## Minimal scaffold

After stage 5 approval, derive only the folders, basic tooling, environment
examples, Git files, and instructions needed for the approved first release.
Delegate scaffold code and configuration to a task-specific worktree as described
in [handoff](handoff.md). Do not implement product features. Verify only commands
that actually exist, and state when no runnable application exists yet.

## Prepare the Agent-Team input

After the plan, tracker, and scaffold are verified, adapt
`assets/templates/AGENT_TEAM_HANDOFF.json` to
`.project-kickoff/AGENT_TEAM_HANDOFF.json`. Put only the ID of each implementation
task in its task list. Include every selected tracker row exactly once. Do not
copy titles, status, dependencies, or acceptance details into this list. The
selected tracker and approved plan own that content. Limit the list to 1000 tasks
and the file to 250 KiB so Agent-Team can wrap it in its
256 KiB initialization request. Validate it with:

```bash
python3 <project-kickoff-skill-path>/scripts/check_agent_team_handoff.py \
  --handoff .project-kickoff/AGENT_TEAM_HANDOFF.json
```

Resolve `<project-kickoff-skill-path>` to the loaded Skill directory. Do not
start Agent-Team or pre-create its runtime receipt as part of this check.

Agent-Team 7.3.1 defaults `maxPlanTasks` to 1000, but the selected host can have
a lower effective setting. Verify the current host setting before declaring the
handoff ready. Do not raise it or reduce approved scope without matching
authorization.

`plan.requiredCapabilities` is optional. When supplied, use at most 100 unique
safe capability IDs. The historical template declares `graphify`; retain it only
when the approved project requires it. An empty list is valid when no optional
capability gates implementation. Native setup prepares selected tools and reports
their actual readiness. A selected optional tool may remain deferred; a declared
required capability must be ready before handoff.

### Native v8 setup after approvals

Project Kickoff 0.5.1 writes the existing nested handoff shape with producer
version 0.5.1 and still accepts 0.5.0 producers. Its checker accepts native
Agent-Team 8.0.12 and retains 8.0.10/8.0.11 schema compatibility.
It reports `compatibility: schema-only` and `runtimeVerified: false`. The original
published 8.0.10 binary has incomplete onboarding and needs an update; its version
alone never qualifies it. After publication, install or update from the verified 8.0.12 release,
then qualify the actual installed setup contract. Passing schema checks does
not establish that a package is installed or ready.

1. Reuse all five current stage approvals, the approved documents, tracker
   selection, task mapping, installation scope, and known model choices. Do not
   restart discovery, repeat answered questions, or switch trackers.
2. Run `agent-teamctl setup --host <codex-or-claude> --json` from the canonical project checkout. Require
   structured `status`, `next_action`, and the selected tracker. A generic success
   message without those fields is not preparation evidence: record an update
   blocker and use the authorized native update procedure before continuing.
3. Complete selected dependency preparation before seeding or creating the
   final handoff. Use the native preparation-only route so this step does not
   bind an incomplete project handoff into the immutable setup receipt.
   Offer Serena, Graphify, rg, ast-grep, and lean-ctx together, plus Beads when
   selected. Name any project-local uv/Python prerequisites in the same consent
   question. After the selected bundle and project scope have been approved, use
   `agent-teamctl setup --prepare-only --install beads,serena,graphify,rg,ast-grep,lean-ctx --approve --tracker beads --host <codex-or-claude> --json`.
   Omit unselected packages; use `--tracker tasks-md` for an approved Markdown
   fallback. Installation consent is already covered only when the saved
   approval names the same packages and scope.
   Reuse healthy installations. If an install is needed, provide only the
   previously approved package, source, project scope, and location. Follow
   structured consent/resume results and save returned paths, versions, checks,
   and unresolved blockers in `.project-kickoff/setup.json`. Present a new
   question only for a scope, access, or dependency choice not already approved.
   For selected Beads, install/verify the chosen executable and initialize its
   tracker before idempotent seeding. If it cannot be used, offer TASKS.md and
   wait for the user's selection. Prepare selected Serena and Graphify before
   readiness; no external hook is necessary. Keep Graphify in the native
   code-only profile and do not add MCP registration or global hooks implicitly.
   Require the structured prepared result and per-tool functional evidence;
   mere executable existence is not readiness. A missing `--prepare-only`
   contract requires the native update, not a normal setup call in its place.
4. Seed the one selected tracker idempotently, verify the approved scaffold,
   then generate the nested handoff with `agentTeam.testedVersion` equal to the
   qualified controller version and run this Skill's checker. For the native
   bridge, `project.revision` must be the current branch tip and
   `plan.authority.externalActions` must be empty; publication authority is a
   separate later native decision. Keep the exact approved task IDs and paths.
5. Use the native setup response and its installed help to submit the handoff
   and existing setup approval. The supported handoff route is
   `agent-teamctl setup --kickoff .project-kickoff/AGENT_TEAM_HANDOFF.json --approve-kickoff --approve --host <codex-or-claude> --json`.
   These flags carry the already-recorded approvals; they do not create new
   authority. Agent-Team creates its own governance files and receipt while
   preserving existing user instructions and the seeded tracker. If a project
   already has native setup, use its approved handoff-attachment transition;
   never rewrite its immutable receipt or silently ignore the new handoff.
6. Complete the first native role settings step. Read the returned roles, models,
   efforts, and profile; reuse approved execution choices. If execution choices
   are unresolved, ask the one remaining role-settings question, persist the
   answer through the native settings contract, and confirm the resulting
   settings. Use supported, observed host model choices or `inherit`, not an
   invented latest model name. Native keys have the form
   `<codex-or-claude>.<orchestrator|developer|reviewer|visual_reviewer>.<model|effort>=value`.
   `coder` aliases `developer`; `inherit` clears a role override. When inherited
   defaults were approved, persist that choice with
   `agent-teamctl settings parallel_teams=1 codex.developer.model=inherit claude.developer.model=inherit --json`.
   Never claim this changed the current parent session model.
7. Reinspect native setup. Declare ready only from its completed setup,
   dependency, and settings evidence. Resume failed or interrupted preparation
   from the same receipts; do not recreate tasks or reinstall verified packages.
   Save `agent-teamctl start --host <codex-or-claude> --json` as the later
   implementation invocation without starting workers. `status --json` is the
   read-only inspection route after setup.

Native v8 does not use `project-initialize`, an owner-session transfer, operation
ID, or the legacy `--emit-request` wrapper. Project Kickoff must not invent any
of those runtime identities. Optional Project Kickoff context hooks remain
separate and are not prerequisites for this path.

### Explicitly selected legacy 7.3.1 initialization

Keep the tested 7.3.1 template value for this route. Required capabilities remain
declarations here: Project Kickoff does not prepare Graphify through legacy
hooks or create `graphify-out/`; legacy Agent-Team owns that preparation.

At the later Agent-Team initialization step, use the actual registered project
owner session, a new operation ID, and the freshly observed Agent-Team setup
version. Emit the direct request that `project-initialize` accepts:

```bash
python3 <project-kickoff-skill-path>/scripts/check_agent_team_handoff.py \
  --handoff .project-kickoff/AGENT_TEAM_HANDOFF.json \
  --emit-request \
  --actor-session-id <actual-project-owner-session> \
  --operation-id <new-unique-operation-id> \
  --expected-version <current-agent-team-setup-version>
```

Save that output to a bounded temporary JSON file. Then give it to Agent-Team's
`project-initialize --project <absolute-project-root> --request <file>` helper.
Project Kickoff must not invent the actor, operation, or expected version.
