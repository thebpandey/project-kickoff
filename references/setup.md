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

Present these six requested dependencies even when some are already ready:

| Dependency | Purpose | Authoritative source |
| --- | --- | --- |
| Ponytail | Minimal implementation and YAGNI guidance | https://github.com/DietrichGebert/ponytail |
| Using-Superpowers | Existing planning, debugging, testing, and review procedures | https://github.com/obra/superpowers |
| Beads | Dependency-aware implementation tracker | https://github.com/gastownhall/beads |
| Agent-Team | Delegated implementation, integration, and coordination | Use the authorized package source recorded for the installed proprietary copy |
| Impeccable | Product and interface design workflow | https://github.com/pbakaus/impeccable |
| UI UX Pro Max Skill | UI/UX patterns, data, and search tools | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |

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

Use the canonical `.agent-team/setup.json` when it is compatible. Preserve
unrelated fields. Keep it in the canonical planning checkout and record:

- host and project identity;
- generating `project-kickoff` metadata version and relevant compatibility note;
- tracker mode and canonical absolute path;
- each dependency's source, version/revision, license/access condition, scope,
  selected path, status, verification evidence, and check date;
- declined, deferred, failed, and superseded choices;
- `TASK-###` to tracker-ID mappings and last seeded plan revision.

Do not store credentials or task status there. The receipt records choices; it
does not grant new permission.

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
