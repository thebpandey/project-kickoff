# Model and reasoning effort selection

The user selects the model and the reasoning effort that Project Kickoff uses.
The user makes two selections in one question:

- **Planning:** the guided interview and the writing of approved artifacts. This
  work runs in the user's main session.
- **Delegated work:** the scaffold and check agents that Project Kickoff sends to
  task worktrees.

## When to ask

Ask this question one time for each conversation. "First invocation" means that
no selection is resolved in the current conversation. This Skill cannot read a
session identifier. It does not track sessions. It knows only whether the current
conversation already resolved a selection.

Ask the question before the first product question and before any setup step. Ask
it for `start`, `audit`, `audit-only`, `resume`, and for an equivalent
natural-language request.

`status`, `help`, and `version` are read-only. Never ask this question for those
three actions. Never write a selection record for them. Never continue from a
read-only action into discovery.

After the conversation resolves the selection, do not ask again. A later `start`
or `resume` in the same conversation uses the resolved selection. The user can
change the selection at any time with a direct instruction.

A timeout or silence is not an answer. Do not select a profile for the user. Do
not start the interview, write an artifact, or dispatch an agent while this
question is open.

## The question

Use the plain-text shape in [the interview workflow](interview.md), or the host's
native choice UI. Offer named profiles. Put the recommended profile first with the
`(Recommended)` label. Close with the exact line that `interview.md` specifies.

Offer three profiles:

1. A balanced pairing. It uses a strong model for planning and a mid-tier model
   for delegated work. Recommend this profile.
2. A pairing that puts the strongest available model and the highest available
   effort on both selections.
3. A cheaper pairing. It uses a mid-tier model for planning and the fastest
   available model for delegated work.

State the concrete trade-off of each profile. Give depth, cost, and speed in
parallel terms. A free-text answer is always valid. The user can pair any
available model with any available effort level.

Name each model and each effort level exactly as the current host reports it.
Read [the host adapters](hosts.md) for the identifiers of each host. Never invent
a model identifier, an effort level, or a host control.

This example uses the documented Claude Code identifiers:

```text
Which model and reasoning effort should Project Kickoff use in this session?

1. Balanced: claude-opus-5 at high for planning, claude-sonnet-5 at high for delegated work (Recommended) — Strong interview and artifact quality, lower cost for scaffold and check agents.
2. Strong for all work: claude-opus-5 at xhigh for planning and for delegated work — The most depth on every step, the highest cost, and the slowest turns.
3. Lower cost: claude-sonnet-5 at high for planning, claude-haiku-4-5-20251001 for delegated work — The lowest cost and the fastest turns, less depth on hard trade-offs.

Reply with a number or your own answer.
```

## Saved values

Read `.project-kickoff/DISCOVERY.md` for the resolved project before you ask. If
its decision register holds a previous model and effort selection, offer those
values back as the recommended profile. Label them as the saved values. The user
confirms them with one reply or selects another profile.

If no discovery record exists, or the record holds no selection, use the standard
recommended profile. Never report a saved value that you did not read.

## Where to record the selection

Record the answer as a `DEC-###` decision in the decision register of
`.project-kickoff/DISCOVERY.md`. Follow [the artifact contracts](artifacts.md)
for that register. Record the selected planning model, the planning effort, the
delegated model, the delegated effort, the user's answer source, and the date.

The discovery record is a planning record. The discovery write limit in
`SKILL.md` permits this write. Do not create a separate state file for the
selection. Do not write `.agent-team/setup.json`. Do not change host settings,
user settings, or any file outside the project.

If the project path is not confirmed, no discovery record exists yet. Keep the
answer in the conversation. Write the `DEC-###` record when you create
`.project-kickoff/DISCOVERY.md`. Tell the user that the selection is not recorded
until that moment.

When the user changes the selection later, mark the old `DEC-###` superseded.
Record the new decision with its source and date. A model or effort change does
not invalidate a stage approval and does not invalidate a derived artifact.

## What the Skill can apply

A Skill cannot change the model or the reasoning effort of its own parent
session. The planning selection applies to that parent session.

For the planning selection:

- Report the selected model and the selected effort to the user.
- Give the user the exact supported control of the current host. Read
  [the host adapters](hosts.md) for that control.
- Never say that the Skill changed the parent model or the parent effort.
- Never say that a recorded selection is active. Say only that it is recorded.

For the delegated selection:

- Set the model and the effort on each dispatched agent when the host exposes
  that control.
- Record the model and the effort that the host accepted.
- If the host exposes no such control, report that limit. Continue the work at
  the host's own setting and name the setting that applied.

If a selected model or a selected effort level is unavailable, report the
constraint and ask one question. Never move the work to a weaker tier without the
user's answer. Never report a lower tier as the selected tier.
