# Project Kickoff

Current version: **0.1.0**

Project Kickoff is a skill for Codex and Claude Code. It turns a software idea
into an approved product definition, design direction, technical blueprint, and
implementation plan. It prepares a minimal scaffold and an Agent-Team handoff.
It does not implement product features during kickoff.

The Skill supports new and existing web, mobile, desktop, API, CLI, and library
projects. It asks one question at a time. It records each answer and waits for
each required approval. It does not choose an unresolved stack or fallback
tracker for the user.

The package uses short sentences, one topic per sentence, and active voice. The
[official ASD-STE100 FAQ](https://www.asd-ste100.org/STE_faq.html) recommends
these principles for clear writing. The full standard is available free of
charge from its official downloads page. This README does not claim formal
certification or verified dictionary compliance.

## How the workflow operates

GitHub renders this Mermaid diagram as a graphical flowchart.

```mermaid
flowchart TD
    U["Type a Project Kickoff action in host chat"] --> R{"Which action?"}
    R -->|help, version, or status| RO["Return read-only information"]
    RO --> ROSTOP["Stop without interview or setup"]

    R -->|start idea| MODE{"Does meaningful project content exist outside installed skills?"}
    MODE -->|No| NP["Confirm the new project path and Git boundary"]
    MODE -->|Yes| EP
    R -->|audit path| EP["Inspect the existing project without changes"]
    R -->|audit-only path| EPO["Inspect the existing project without changes"]
    R -->|resume path| RS["Read checkpoint, approvals, version, and setup receipt"]

    EP --> AUD["Write or merge AUDIT.md with evidence and stable findings"]
    AUD --> KEEP["Ask retain, change, or defer decisions one at a time"]
    KEEP --> LOOP
    EPO --> AUDO["Write or merge AUDIT.md with evidence and stable findings"]
    AUDO --> STOP["Stop after the audit report"]
    NP --> LOOP
    RS --> NEXT{"What is the saved next action?"}
    NEXT -->|Pending decision| LOOP
    NEXT -->|Approved setup| SETUP
    NEXT -->|Ready| READY

    STAGES["Stages: 1 Product; 2 First release; 3 Experience; 4 Technical; 5 Execution"] -.-> LOOP
    subgraph DISCOVERY["Adaptive stage loop"]
        LOOP["Ask one unresolved question with recommended choices"] --> WAIT["Wait for the user answer"]
        WAIT --> RECORD["Record the answer, source, decision, and affected artifacts"]
        RECORD --> SUMMARY["Summarize the current stage"]
        SUMMARY --> APPROVE{"Approve this stage?"}
        APPROVE -->|Revise| LOOP
        APPROVE -->|Approve and move to next stage| LOOP
    end

    APPROVE -->|All five stages approved| PLAN["Finalize PRD.md, DESIGN.md, and PLAN.md"]
    PLAN --> SETUP["Inspect six dependencies and project setup"]
    SETUP --> TRACKER{"Is the selected tracker ready?"}
    TRACKER -->|Yes| SEED["Seed stable plan IDs once and verify hierarchy"]
    TRACKER -->|No| ALT["Research free or open-source choices"]
    ALT --> CHOOSE["Ask the user to choose a fallback"]
    CHOOSE --> WAIT2["Wait; do not activate a temporary tracker"]
    WAIT2 --> SEED
    SEED --> DOCS["Finalize agent rules, context, receipts, and one live tracker"]
    DOCS --> WT["Delegate minimal scaffold work in a task worktree"]
    WT --> INT["Verify in one integration worktree"]
    INT --> CLEAN["Update the canonical branch and clean verified integrated work"]
    CLEAN --> READY["Prepare the exact Agent-Team handoff"]
    READY --> NOAUTO["Stop; do not start Agent-Team automatically"]
```

Each stage uses the same question loop. A timeout is not an answer. A direct user
decision is an answer. The Skill does not ask the user to approve the same
decision again. It asks only for the next unresolved consequence or stage bundle.

## Dependencies

The Skill checks these six dependencies. It records the selected path, source,
version or revision, scope, license or access terms, and verification result.
It installs nothing only to complete this list.

```mermaid
flowchart LR
    PK["Project Kickoff"] --> P["Ponytail: minimal implementation guidance"]
    PK --> S["Using-Superpowers: planning, debugging, testing, and review"]
    PK --> B["Beads: dependency-aware task tracking"]
    PK --> A["Agent-Team: delegated implementation and integration"]
    PK --> I["Impeccable: product and interface design"]
    PK --> UI["UI UX Pro Max Skill: UI patterns and tools"]

    B --> BR{"Beads ready?"}
    BR -->|Yes| BT["Use Beads as the only live tracker"]
    BR -->|No| RESEARCH["Research current alternatives"]
    RESEARCH --> USER["User selects root TASKS.md or another verified option"]
    USER --> FT["Activate only the selected tracker"]

    I --> VIS{"Visual interface?"}
    UI --> VIS
    VIS -->|Yes and relevant| DESIGN["Apply selected UI guidance"]
    VIS -->|No| NONVIS["Use API, CLI, or library interaction guidance"]

    PK -.-> SEC["Optional: one relevant security skill"]
    PK -.-> BROWSER["Optional: browser verification when current tools are insufficient"]
    BT --> HANDOFF["Verified Agent-Team handoff"]
    FT --> HANDOFF
    A --> HANDOFF
```

The Skill prefers compatible project-local installations. It preserves current
project settings. It does not add global configuration or hooks without matching
authorization. If one tool is unavailable, it continues independent work.

## Requirements before installation

You need written permission from the licensors. You also need authenticated
access to the private GitHub repository. The examples use GitHub CLI and the
planned `v0.1.0` release tag. Run them only after that tag is published and
verified.

Install the Skill into the repository where you will use it. Do not install it
into an unrelated ancestor repository. Each command block stops when an existing
Git root does not match the current directory. For an empty new directory, the
block creates a new repository with a `main` branch. For a nonempty directory
without Git, first inspect the content and confirm the intended root. Then run
`git init -b main` yourself and repeat the install block.

## Install for Codex

Open a shell at the intended project root. Run:

```sh
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  kickoff_project_root="$(git rev-parse --show-toplevel)"
  test "$(pwd -P)" = "$(cd "$kickoff_project_root" && pwd -P)" || { echo "Run from the intended Git root."; exit 1; }
else
  test -z "$(find . -mindepth 1 -maxdepth 1 -print -quit)" || { echo "Confirm and initialize this nonempty project first."; exit 1; }
  git init -b main
  kickoff_project_root="$(git rev-parse --show-toplevel)"
fi
kickoff_skill_path="$kickoff_project_root/.agents/skills/project-kickoff"
test ! -e "$kickoff_skill_path" || { echo "Target already exists: $kickoff_skill_path"; exit 1; }
kickoff_exclude_path="$(git rev-parse --git-path info/exclude)"
touch "$kickoff_exclude_path"
grep -qxF '/.agents/skills/project-kickoff/' "$kickoff_exclude_path" || printf '%s\n' '/.agents/skills/project-kickoff/' >> "$kickoff_exclude_path"
mkdir -p "$kickoff_project_root/.agents/skills"
gh repo clone thebpandey/project-kickoff "$kickoff_skill_path" -- --branch v0.1.0 --single-branch
test -f "$kickoff_skill_path/SKILL.md" && test -f "$kickoff_skill_path/CHANGELOG.md" && test -f "$kickoff_skill_path/LICENSE"
git -C "$kickoff_project_root" check-ignore -q "$kickoff_skill_path/SKILL.md" || { echo "The private Skill is not excluded. Do not stage it."; exit 1; }
```

Codex discovers repository skills under `.agents/skills/`. Start or refresh
Codex according to the current host documentation if the Skill does not appear.

## Install for Claude Code

Open a shell at the intended project root. Run:

```sh
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  kickoff_project_root="$(git rev-parse --show-toplevel)"
  test "$(pwd -P)" = "$(cd "$kickoff_project_root" && pwd -P)" || { echo "Run from the intended Git root."; exit 1; }
else
  test -z "$(find . -mindepth 1 -maxdepth 1 -print -quit)" || { echo "Confirm and initialize this nonempty project first."; exit 1; }
  git init -b main
  kickoff_project_root="$(git rev-parse --show-toplevel)"
fi
kickoff_skill_path="$kickoff_project_root/.claude/skills/project-kickoff"
test ! -e "$kickoff_skill_path" || { echo "Target already exists: $kickoff_skill_path"; exit 1; }
kickoff_exclude_path="$(git rev-parse --git-path info/exclude)"
touch "$kickoff_exclude_path"
grep -qxF '/.claude/skills/project-kickoff/' "$kickoff_exclude_path" || printf '%s\n' '/.claude/skills/project-kickoff/' >> "$kickoff_exclude_path"
mkdir -p "$kickoff_project_root/.claude/skills"
gh repo clone thebpandey/project-kickoff "$kickoff_skill_path" -- --branch v0.1.0 --single-branch
test -f "$kickoff_skill_path/SKILL.md" && test -f "$kickoff_skill_path/CHANGELOG.md" && test -f "$kickoff_skill_path/LICENSE"
git -C "$kickoff_project_root" check-ignore -q "$kickoff_skill_path/SKILL.md" || { echo "The private Skill is not excluded. Do not stage it."; exit 1; }
```

Claude Code discovers repository skills under `.claude/skills/`. A same-named
personal skill can take precedence. Verify the loaded source when behavior does
not match this release.

These commands use the repository-local Git exclude path returned by Git. This
works when `.git` is a directory or a linked-worktree file. The commands do not
edit the project's committed `.gitignore`. They do not install global software
or hooks. They verify that Git ignores the private Skill before later app commits.

The clone contains its own private Git metadata and development documents. The
host reads the Skill package from that checkout. Keep the whole checkout private.

Official host documentation:

- Codex: https://learn.chatgpt.com/docs/build-skills
- Claude Code: https://code.claude.com/docs/en/skills

## Release archive layout

The release archive is `project-kickoff-0.1.0.zip`. Install the complete extracted
directory at one native host path. Its package root contains:

```text
project-kickoff/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── artifacts.md
│   ├── communication.md
│   ├── existing-projects.md
│   ├── handoff.md
│   ├── hosts.md
│   ├── interview.md
│   └── setup.md
└── assets/
    └── templates/
        ├── AGENTS.md
        ├── AUDIT.md
        ├── CLAUDE.md
        ├── CONTEXT.md
        ├── DESIGN.md
        ├── DISCOVERY.md
        ├── MISTAKES.md
        ├── PLAN.md
        ├── PRD.md
        ├── README.md
        └── TASKS.md
```

Do not install only `SKILL.md`. The workflow needs its references and templates.
Check a published archive against its release checksum when one is supplied.
Do not mix files from different release tags.

## Action vocabulary

Actions are text that you enter in Codex or Claude Code chat. They are not shell
binaries. Do not type `$project-kickoff` into a shell.

| Action | Result | State change |
| --- | --- | --- |
| `start <idea>` | Starts a kickoff. It audits first when meaningful project content exists. Otherwise it starts the new-project questions. | Writes records only after the project path is confirmed. |
| `audit [path]` | Inspects an existing project, produces `AUDIT.md`, and continues to guided retain/change decisions and setup. | Audit starts with inspection. Later writes follow user decisions and approvals. |
| `audit-only [path]` | Inspects an existing project and stops after `AUDIT.md`. | Does not start guided setup or remediation. |
| `resume [path]` | Restores saved decisions, approvals, pending question, version, tracker, and next action. | Continues only the recorded authorized workflow. |
| `status [path]` | Reports version, project, revision, phase, last approval, pending question, blockers, and next action. | Read-only. It does not write checkpoints, replay questions, initialize tools, or run tests. |
| `help` | Lists supported actions and host syntax. | Read-only. It does not inspect a project. |
| `version` | Reports the loaded Skill version, path, and CHANGELOG entry. | Read-only. It does not start an interview. |

Clear natural-language requests work too. Examples include “Audit this project
and then help me plan the approved changes” and “Show project kickoff status for
`/path/to/project`.”

## Codex chat examples

Enter one of these lines in Codex chat:

```text
$project-kickoff start Build a scheduling tool for a small repair shop.
$project-kickoff audit /path/to/existing-project
$project-kickoff audit-only /path/to/existing-project
$project-kickoff resume /path/to/project
$project-kickoff status /path/to/project
$project-kickoff help
$project-kickoff version
```

## Claude Code chat examples

Enter one of these lines in Claude Code chat:

```text
/project-kickoff start Build a scheduling tool for a small repair shop.
/project-kickoff audit /path/to/existing-project
/project-kickoff audit-only /path/to/existing-project
/project-kickoff resume /path/to/project
/project-kickoff status /path/to/project
/project-kickoff help
/project-kickoff version
```

## What the Skill creates

| Output | Purpose |
| --- | --- |
| `.project-kickoff/DISCOVERY.md` | Stores answers, evidence, decisions, stage approvals, the one pending question, and the Skill version. |
| `AUDIT.md` | Records bounded evidence and stable findings for an existing project. |
| `PRD.md` | Defines users, problems, release scope, requirements, architecture, stack, data, integrations, and acceptance criteria. |
| `DESIGN.md` | Defines the relevant visual or nonvisual experience, accessibility, states, content, and interaction rules. |
| `PLAN.md` | Defines the approved first-release epics, stories, tasks, dependencies, verification, and future roadmap boundary. |
| `AGENTS.md` | Gives shared project rules to coding agents. |
| `CLAUDE.md` | Tells Claude Code to read the shared rules and adds necessary host differences. |
| `MISTAKES.md` | Stores confirmed lessons under one project-orchestrator writer. It starts empty. |
| `CONTEXT.md` | Stores a short resumption checkpoint and links to the live tracker. |
| `README.md` | Orients people to the generated project and verified commands. |
| `.agent-team/setup.json` | Records host, dependency, version, tracker, and stable ID mappings. It does not store task status or secrets. |
| Selected tracker | Owns live execution status. The Skill activates only one tracker. |
| Minimal scaffold | Adds only approved folders and basic tooling. It can contain no runnable application yet. |

Generated project files are separate from this package README. The Skill adapts
the templates. It does not leave unresolved template fields in completed output.

## Existing-project behavior

The audit distinguishes three things: the current implemented system, the
documented intent, and the proposed target. It states whether each check passed,
failed, was blocked, or was not run. It does not call old CI output a new pass.

| The Skill preserves | The Skill changes only after approval |
| --- | --- |
| Product code, application configuration, useful project documents, Git history, branch names, worktrees, local edits, untracked files, and ignored files. | Planning documents, project agent instructions, project-local skill setup, and tracker setup within the approved scope. |
| Existing requirement IDs, task IDs, task history, completed work, and evidence when they remain valid. | Contradictory or stale planning sections after a retain/change decision and stage approval. |
| The actual designated integration branch. It does not require a branch named `main`. | Product-code or application-configuration remediation only through the later Agent-Team plan. |

The audit can find that no remediation is needed. In that case, the Skill records
the evidence and retain decisions. It does not create work to make the tracker
nonempty.

Installed host skill folders under `.agents/skills/` or `.claude/skills/` do not
make an otherwise empty project an existing application. The audit does not
inspect private skill-package source as the user's product.

The `start` action also uses this test. It does not bypass the audit when an
existing application is present. The `audit-only` action always stops after the
evidence report.

## Setup, tracking, and recovery

The Skill keeps `PLAN.md` as the approved baseline. The selected tracker owns
live status. It maps stable epic, story, and task plan IDs to tracker IDs. It
creates parent records before child records when the tracker supports hierarchy.
It verifies blocker direction separately from parent-child links.

After an interrupted seed, the Skill reads the tracker and saved mappings. It
reuses exact matches. It creates only missing records. It stores each mapping
after each successful create. It does not delete and rebuild a partial tracker.

If Beads is unavailable, the Skill explains the failure. It offers root
`TASKS.md` and researched current alternatives. It waits for the user's choice.
It does not use `TASKS.md` as a temporary tracker. It does not switch back to
Beads automatically if Beads becomes available later.

On resume, the Skill checks the actual files, Git revision, recorded version,
approved decisions, active tracker, and pending question. A version mismatch does
not replace a pinned Skill or regenerate approved files. The Skill reads the
CHANGELOG and proposes only relevant compatibility work.

## Scaffold, handoff, and cleanup

The canonical checkout holds planning and shared records. New repositories use
`main`. Existing repositories use their designated integration branch without a
rename. All scaffold code, configuration, builds, tests, and executable helper
work occurs in task worktrees. One integration worktree combines and verifies
the result.

After verified integration, the workflow preserves evidence and checks tracked,
untracked, and ignored files. It removes only clean, fully integrated task
worktrees and branches. It keeps uncertain or unfinished work. This cleanup does
not wait for production deployment.

The final handoff gives the user the exact Agent-Team invocation for the active
host. Preparing the handoff does not run Agent-Team. The user starts the next
workflow when ready.

## Optional targeted skills

The Skill can propose one relevant security skill from the Trail of Bits skill
collection. It can propose Agent Browser when a visual project needs browser
verification and current tools are insufficient. It checks the current source,
license, host support, and scope first. It does not install whole collections by
default.

## Releases and upgrades

Releases use semantic version numbers. Tags use the form `v0.1.0`. Archives use
the form `project-kickoff-0.1.0.zip`. A patch release makes a compatible fix. A
minor release adds a compatible capability. During `0.x`, a documented breaking
change also uses a minor bump. A major release changes a contract incompatibly.

Review [CHANGELOG.md](CHANGELOG.md) and `LICENSE` before an upgrade. Install from
a verified tag. Replace the complete package. Preserve generated project files,
tracker data, decisions, approvals, and evidence. A new release does not grant
new license rights or future-update permission.

## License and support

The Skill package uses the proprietary terms in `LICENSE`. Written permission
from the licensors is required to use, modify, or redistribute it. The license
permits authorized commercial and client application development without a paid
entitlement.

Generated project files and template-derived project instructions have the
separate permissions in Section 4 of `LICENSE`. They can be edited and
distributed, including commercially. Third-party tools keep their own licenses.

For permission or support, contact support@learnstackos.com.
