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

Pending the integrated skill revision. Record actual results and corrections
here before publication. Do not infer passes from the presence of instructions.
