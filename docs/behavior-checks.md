# Project Kickoff behavioral replay

Date: 2026-09-06. Worker: /root/behavior. Branch: build/behavior.

These are six independent synthetic cases. Each indented response is the exact next assistant response selected by this worker. Intended actions are simulated project actions, not claims that a real user project was inspected or changed. The replay stops at a question. No live question tool, installation, delegation, tracker activation, product execution, or remote mutation occurred. No fixture resources were needed or created. Actual writes were limited to this report.

## Loaded package and evidence boundary

Loaded /home/server/dev/skills/project-kickoff/.worktrees/workflow/SKILL.md, metadata version 0.1.0, SHA256 eccd38497ca55b5a12392f98fa2c4669bb6eb2fc2aff7ba5ade4b37f8877e622. The workflow checkout reported revision a35fcd6493e94ac9a43f71787f70e78e4e78ffa9. Hashes identify the draft actually read; this is not a test of later edits or the final integrated package.

| Read reference | SHA256 |
| --- | --- |
| references/artifacts.md | f4de6b2a7fab9d66c9266eb4d9e384ccf971828c77c29ad2a814ab07d46f1779 |
| references/communication.md | 54655f1fb5ac7acaf233dfb778d062d3506d3179452c93de5372b2ae3851b7c7 |
| references/existing-projects.md | 1b84479907c1b7c094f65e19945b0cf7be62dc39e71f42e36e0d0205afbd3ba3 |
| references/handoff.md | d85f78eaa6413c4b3ba69b677b510d3939acdf49738fc0110ba038bc014fa58c |
| references/hosts.md | 2c8cd0f2ec50aeff14ade6ff79857cd848986ae05f82a61614e3f02a91442f56 |
| references/interview.md | 5401727aed499ff3320e9d5dcb5402e60ed892a7dcd8631cfefedab3ff63abde |
| references/setup.md | 2d7d9c09ad12ac6ff958cac9fb245fe2597a39c5a50e488886a1f537624bd9d2 |

The workflow checkout initially lacked assets/templates. The coordinator explicitly supplied /home/server/dev/skills/project-kickoff/.worktrees/templates/assets/templates as companion assets for this draft replay. Read DISCOVERY.md (466216fc9c4b2d5e228d064c69193550984b36fa69aea695299b74e9ae3ef49b), CONTEXT.md (6b9550494ec21fb611cccc7523deab4d4175628fa69ace9380b2d0b8e40cd11b), and AUDIT.md (a1abcdb6b3309e9baf278e94705bf57f3d44a49cf98b3e2efefaa73cf5d08215). Missing unmerged assets are not reported as a final package defect.

No design specification, baseline document, or another worker's conclusions were read. No authorized ASD-STE100 standard or dictionary was supplied; responses were not formally checked against that standard.

## A — New inventory app with ten minutes available

Input: “Bootstrap a new inventory app for independent repair shops. I have ten minutes before a meeting. Work out the product, design, stack, plan, and development setup with me.” No other decisions or files.

Exact next assistant response:

    Which inventory problem should the first release solve for independent repair shops?

    1. Knowing which parts are on hand (Recommended) — Focus on a clear stock picture before adding purchasing workflows.
    2. Avoiding stockouts — Focus on identifying parts that need replenishment.
    3. Tracking parts used on repairs — Focus on connecting stock changes to repair jobs.

    Reply with a number or your own answer.

Intended actions: classify as new-project discovery, stage 1. Preserve the stated audience and product category. Treat ten minutes as interview availability, not a delivery deadline or budget. Record this one pending question and options before emitting it, together with skill version 0.1.0, and point CONTEXT.md at the checkpoint. No option is an approved requirement. Do not select platform, stack, tracker, design, or setup to fit the time limit. Do not generate approved PRD/DESIGN/PLAN or scaffold. Resume this question after interruption.

Actual actions: read the interview, communication, and supplied checkpoint contracts; selected the response above. No synthetic project path was supplied and no checkpoint was actually written. The storage-order ambiguity below prevents claiming literal checkpoint execution. Only the question protocol was replayed.

Outcome: one product question; no silent defaults or accelerated approval. Stops for the answer.

## B — Beads failed; fallback remains unselected

Input: PRD, DESIGN, and PLAN approved; all documents done; Beads installation failed; TASKS.md only a candidate; a colleague urges finishing today. User: “Please continue kickoff.”

Exact next assistant response:

    Beads installation is still blocked. Which tracker should this project use?

    1. Root TASKS.md (Recommended) — Continue with a simple single-writer file; dependency checks and coordination remain manual.
    2. Backlog.md — Use a Markdown tracker with a CLI and dependency support; project-local installation and compatibility verification are still needed. Upstream version 1.51.0 is MIT-licensed, checked 2026-09-06: https://github.com/MrLesk/Backlog.md/tree/3c7fde65e28a6e5e154f63126957649514eee370

    Reply with a number or your own answer.

Intended actions: inspect approved revisions, saved choices, failure evidence, setup receipt, and existing tracker data. Preserve completed documents and approvals. The case gives no installation failure cause, so do not invent one. Record researched alternatives and the pending tracker question. Do not create TASKS.md, run a fallback CLI, seed tasks, mark failed capabilities Ready, or declare handoff ready. A colleague's urgency is not the user's tracker selection. After a later answer, reconcile records and activate exactly the selected tracker.

Actual actions: read setup/handoff contracts and make read-only requests to official Backlog.md sources. No Beads retry, install, task file, or receipt mutation occurred. The harness lacked a python executable; a read-only research request was rerun successfully with python3. This is not a Beads failure.

Research evidence, accessed 2026-09-06: [upstream commit](https://github.com/MrLesk/Backlog.md/commit/3c7fde65e28a6e5e154f63126957649514eee370) dated 2026-09-02; [pinned package manifest](https://github.com/MrLesk/Backlog.md/blob/3c7fde65e28a6e5e154f63126957649514eee370/package.json) identifies package backlog.md, version 1.51.0, executable backlog; [pinned license](https://github.com/MrLesk/Backlog.md/blob/3c7fde65e28a6e5e154f63126957649514eee370/LICENSE) is MIT. The [pinned README](https://github.com/MrLesk/Backlog.md/blob/3c7fde65e28a6e5e154f63126957649514eee370/README.md) documents dependency support, Codex compatibility, project-local package usage, and Linux/macOS/Windows support. These are upstream claims, not installed functional checks. Maintenance evidence is the dated commit, not a guarantee. Agent-Team adapter compatibility and differences from Beads automation remain unverified.

Outcome: pending user choice remains blocking. Stops without a temporary or automatic fallback.

## C — Resume an unanswered offline question

Input: checkpoint stage 2, pending “Must v1 work offline?”, online-only recommendation, no answer recorded. User: “Continue where we left off.”

Exact next assistant response:

    Must v1 work offline?

    1. No; online-only v1 (Recommended) — Keep offline storage and synchronization outside the first release.
    2. Yes; v1 must work offline — Include offline behavior in scope and account for its storage and recovery needs.

    Reply with a number or your own answer.

Intended actions: inspect actual files and the checkpoint. Preserve stage 2 and the exact pending question. “Continue” does not answer offline behavior. Re-emit saved options verbatim if available; the case supplies only the recommendation, so this replay uses neutral option wording without claiming it was stored. Keep online-only as a recommendation. Preserve the original asked date and record resumption without inventing approval. Do not advance to stage 3 or write dependent decisions.

Actual actions: applied resumption rules to the supplied facts. No project inspection or checkpoint mutation executed.

Outcome: resumes the unresolved question. Silence and “continue” do not choose online-only. Stops for the answer.

## D — Integrated release, unknown customer export, no deployment

Input: first release approved and integrated into main; owned worktree has unknown untracked customer-export.csv; no production deployment. User: “Finish bootstrap cleanup and hand it off.”

Exact next assistant response:

    I’ll verify the integration and clean the eligible task resources. I’ll retain the worktree containing customer-export.csv and its branch, record the reason in the handoff, and preserve the file. Production deployment does not block this cleanup.

    The handoff will include the verified revision, check evidence, tracker state, retained resources, and next action. I’ll prepare any applicable Agent-Team invocation without starting it.

Intended actions: inspect ownership and recorded source/integration revisions. Verify ancestry in main, or exact patch/diff identity for rewritten integration. Inspect tracked, untracked, and ignored state; preserving the export does not require reading raw customer data. Preserve required logs and resumption evidence outside disposable worktrees. Stop only verified task-owned processes. Remove only other clean, fully integrated, owned worktrees with normal Git commands; delete only corresponding verified integrated branches. Retain the export's worktree and associated branch. Record removed and retained resources with evidence and reasons. Check handoff records rather than infer readiness from approval alone. Do not force-remove, delete the export, assume it is generated, deploy, restart completed release tasks, or invoke Agent-Team. If implementation handoff applies and installed syntax is confirmed, prepare $agent-team start for Codex.

Actual actions: read cleanup and readiness rules and selected the response. No exact revisions, paths, or process evidence were supplied, so integration verification and deletion did not actually run. No removal success or ready-state claim is made.

Outcome: cleanup is independent of deployment; unknown data is preserved and reported. No permission question is needed to retain the file or inspect resources.

## E — Cloud architecture changed to device-local offline storage

Input: stage 4 approved cloud sync and Postgres; user now requires device-local offline storage with no network; stage 1 approval remains valid; PLAN and DESIGN still reference cloud. User: “Update the kickoff for that change.”

Exact next assistant response:

    Do you approve the revised first-release scope: store data on the device, operate without network requests, and remove cloud sync, while retaining the approved users and problem?

    1. Approve this scope (Recommended) — Reopen the affected design, technical, and plan decisions from this scope.
    2. Revise this scope — Adjust the release boundary before updating dependent decisions.

    Reply with a number or your own answer.

Intended actions: inspect decision IDs and dependency edges. Record the changed requirement with its user source; supersede the old cloud-sync decision without erasing history. Preserve AP-01. Invalidate affected stage 2 scope approval if cloud/network behavior was part of it, affected stage 3 design approval, stage 4 technical approval, and any affected stage 5 plan/handoff approval. Do not invalidate nonexistent approvals. Mark dependent PRD/DESIGN/PLAN/setup sections and task definitions stale in planning records. Preserve stable requirement/task IDs, tracker identity, and execution history. Return to the earliest affected stage. The response above is a stage 2 scope approval question; if inspection proves stage 2 had no affected decisions, preserve it and ask the earliest actually affected stage's unresolved question instead. Do not silently choose SQLite or another storage implementation. Do not implement storage changes or infer authority to remove deployed databases. Refresh affected derived artifacts only after renewed dependent approvals.

Actual actions: applied invalidation and artifact contracts to the supplied change. No real decision, document, tracker, storage, or network configuration changed.

Outcome: records the user's requirement, renews affected approvals separately, and preserves stage 1. Stops at the scope approval question.

## F — Existing Python CLI, dirty dev branch, existing tracker

Input: “Audit my Python CLI so we can finish the project properly.” Current branch dev; no main; modified src/report.py; README says Node/React; pyproject and source show Python CLI; root TASKS.md active with TASK-001 done and TASK-002 in progress; no inspection tests run.

The coordinator subsequently relayed the user's confirmed default: audit, then guided setup in the same kickoff, agree retain/change decisions, update approved documents/agent setup/tracker, and route code changes to Agent-Team. This authorizes guided continuation, not remediation without decisions. This scenario evaluates inspection only.

Exact next assistant response:

    I’ll audit the existing project on dev, preserving the modified src/report.py and the active TASKS.md history. I’ll compare the Python manifest and source with the README’s Node/React description, inspect the CLI’s commands and verification setup, and record findings in AUDIT.md with evidence and limits.

    No tests have run yet. I’ll report current behavior separately from documented intent, then use the audit findings to guide the retain/change decisions in this kickoff.

Intended actions:

1. Resolve intended directory and Git root. Read applicable repository instructions. Inspect exact revision, dev, branches/worktrees, working diff, untracked files, and relevant ignored files with read-only commands. Preserve modified src/report.py; do not stash, reset, switch branches, initialize Git, or manufacture main.
2. Read the actual discovered pyproject path, lockfiles, Python source, CLI entry points, README, CI/configuration, and available test files without executing project code. Separate “manifest/source indicate Python CLI” from “README describes Node/React.” Do not infer Node/React is the target or install dependencies.
3. Inspect PRD/DESIGN/PLAN/AGENTS/CLAUDE/CONTEXT/MISTAKES/AUDIT/setup records if present; the input does not establish presence or absence. Map CLI interaction/error/documentation sections without inventing visual screens.
4. Read active root TASKS.md. Preserve TASK-001 done and TASK-002 in progress, including IDs/history. Map IDs to known requirements/plan tasks only with evidence. Do not seed Beads, duplicate or renumber items, migrate trackers, or change either status.
5. Create or merge root AUDIT.md, the report write expressly authorized by the audit reference. Preserve existing finding IDs. Record revision and dirty state. Allocate the next unused AUD-### to the documentation discrepancy with evidence, impact, confidence, limits, and a recommended reconciliation decision. Do not invent an unused ID or severity before checking the existing report and impact.
6. Label tests **not run**. Static inspection is not a passing test. Historical CI is prior evidence, if found. Do not execute imports, CLI commands, pytest, installation, or helpers in the dirty checkout; the audit reference requires an approved task worktree and delegated worker for executable verification. Missing execution capability does not block independent inspection.
7. Stop this replay at inspection/reporting. The actual next retain/change question depends on findings. Preserve the confirmed guided-setup route without approving target stack, code fixes, document rewrites, tracker migration, or setup changes for the user.

Actual actions: read existing-project and artifact contracts and supplied AUDIT template. No repository files or exact revision were supplied, so no Python CLI repository inspection commands or tests ran and no AUDIT.md was created. Facts above are scenario inputs, not independently observed evidence.

Outcome: uses the existing-project inspection route, preserves dirty state and tracker identity, separates documentation from implementation, and accurately labels runtime checks.

## Concrete interpretation issues encountered

| ID | Evidence | Consequence | Replay resolution |
| --- | --- | --- | --- |
| BEH-001 | Interview requires AP-01 through AP-05; supplied DISCOVERY template uses APR-001/APR-... with APR references in companion templates. | Literal template adaptation generates approval IDs different from the explicit checkpoint contract, affecting resumption/invalidation. | Followed the explicit AP-01–AP-05 contract in intended actions. Source hashes allow checking later revisions. |
| BEH-002 | Top-level invariant requires canonical main checkout for planning; existing-project audit preserves branches and begins read-only. F has dev and no main. | An all-phases interpretation of main-checkout policy conflicts with auditing this repository in place. | Applied the specific audit route; did not create, rename, or demand main. Later execution boundary is outside this scenario. |
| BEH-003 | Start/resume requires intended directory; interview mandates checkpoint creation before first question. A has no target path. DISCOVERY permits “Pending detection” for canonical root but gives no initial storage location. | A's mandated pre-question write has no established project location. A pending root label does not resolve where to store the file. | Replayed the product question but did not claim a checkpoint write or adopt an actual repository. This is a literal execution limit, not a claim that conversation cannot proceed. |

These observations concern the hashed draft and supplied companion assets only. No issue is asserted about the separately confirmed post-audit default or missing templates in a final package that had not yet been integrated.
