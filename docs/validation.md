# Validation record

This file records observed checks. It is development evidence, not part of the
installed skill. Synthetic scenarios do not prove behavior in every host or model.

## Baseline before the skill existed

One independent agent received three synthetic requests without project-kickoff
or its design. It was instructed to return its next response and intended
actions without making changes. The baseline ran before SKILL.md was written.

| Scenario | Observed behavior | Assessment |
| --- | --- | --- |
| Vague repair-shop inventory idea, ten-minute time pressure | Proposed inventory features, UI screens, Next.js, TypeScript, and PostgreSQL before eliciting product needs; asked one shop-type question. | The new workflow needs explicit discovery and stack-decision boundaries. This was not a multi-question failure. |
| Approved docs, Beads failed, TASKS.md not selected | Said it would use TASKS.md as a temporary checklist without a user choice. | Demonstrated the fallback-selection failure the skill must prevent. |
| Integrated task, unknown untracked CSV, no deployment | Preserved the affected worktree and proposed removing only eligible clean task worktrees. | Baseline already handled this safety boundary correctly; test it as a regression. |

Exact fallback response excerpt: “Since Beads installation failed, I’ll use the
available TASKS.md candidate as a temporary local checklist, map it to the
approved plan, and record the tracking setup issue in the handoff.”

## Package and behavior checks

The workflow, templates, host adapters, and license were reviewed together.
Evidence reports identify the exact draft or integrated revision they checked.

- [Behavioral replay](behavior-checks.md): six bounded scenarios cover discovery,
  a missing tracker, resumption, cleanup, changed scope, and an existing project.
  Three draft ambiguities were corrected before integrated review.
- [Integrated review](integrated-review.md): independent contract review and an
  actual existing Python CLI fixture audit. All eight original files and Git
  state were preserved. The audit produced three planning records and stopped
  at one question. Product runtime tests were not run.
- [Beads smoke](beads-smoke.md): actual selected CLI initialization, task
  hierarchy/blockers, and repeated reconciliation without duplicate records.
  This used a synthetic fixture, not a user project. Version-specific side
  effects and limits are recorded in the report.
- [Package checks](package-checks.md): metadata, version, local links, exact
  runtime allowlist, and patch hygiene. README install and action checks are
  recorded with the source revision they checked.
- [Model and effort checks](model-effort-checks.md): the automated package
  manifest and version tests with their red evidence, plus the instruction-level
  check steps for the first-invocation model and effort selection.
- [Diagram checks](diagram-checks.md): both README Mermaid diagrams rendered
  locally. The main workflow is tall; native SVG supports close inspection.

These checks do not certify every model or host version. The package uses
ASD-STE100 writing principles; no formal dictionary compliance is claimed.
The final release archive is checked separately before upload. GitHub release
assets and the version tag provide the published package and source identity.
