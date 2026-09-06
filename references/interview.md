# Adaptive interview and checkpoint

## State model

Use these stages in order, but ask only questions that remain material:

1. **Product definition:** problem, users, current alternatives, proposed value,
   available evidence, and riskiest assumptions.
2. **First-release scope:** journeys, priorities, exclusions, measurable
   outcomes, acceptance criteria, budget, schedule, and constraints.
3. **Experience and design:** interaction type, accessibility, brand direction,
   reference examples, states, errors, and behavior. Do not invent visual screens
   for an API, CLI, or library.
4. **Technical blueprint:** researched stack alternatives, architecture, data
   ownership, integrations, security, deployment, operations, and folder shape.
5. **Execution and handoff:** task graph, verification, dependencies, scaffold,
   tracker, project rules, and Agent-Team readiness.

Follow up when an answer is vague, conflicts with another decision, or leaves a
high-risk assumption unresolved. Explain the concern and offer realistic options.
Do not impose a fixed number of questions.

At the end of each stage, summarize confirmed decisions, assumptions, evidence,
and open items. Then ask one separate approval question. A revision answer keeps
the stage open. Later stages may be explored only when they do not depend on the
unapproved decision.

## One-question protocol

Ask exactly one question per turn. Prefer the host's native choice UI when it is
available. In Codex, use the exposed user-input tool with one question, two or
three mutually exclusive choices, the recommended choice first, and
`(Recommended)` in its label. The host supplies a free-text Other choice; do not
add a duplicate. In another host, use its native equivalent with the same shape.

If no native choice UI is available, send exactly this plain-text shape and end
the turn:

```text
<One question>

1. <Choice> (Recommended) — <effect or trade-off>
2. <Choice> — <effect or trade-off>
3. <Choice> — <effect or trade-off>

Reply with a number or your own answer.
```

Two choices are enough when there are only two real options. Free-text answers
are always valid. Record the question as pending before asking it. Do not ask the
next question, write a dependent decision, activate a fallback, or start setup
until the answer arrives.

For research-dependent decisions, first inspect relevant project evidence and
current primary sources. Present alternatives, their material trade-offs, source
links, and the check date. Recommend one based on confirmed constraints. The user
selects the stack, architecture, tracker, and other consequential alternatives.

## Checkpoint

After the intended project path and safe repository boundary are confirmed,
create `.project-kickoff/DISCOVERY.md` from
[the discovery template](../assets/templates/DISCOVERY.md) at the start. Keep
`CONTEXT.md`, adapted from [the context template](../assets/templates/CONTEXT.md),
as the short resumption pointer. Never store
credentials, raw sensitive data, or private reasoning in either file.

If the target path is unknown, keep the single pending path question in the
conversation and wait. Do not invent a destination or write a checkpoint into
the current directory or an ambient ancestor repository.

Use stable records:

- the generating `project-kickoff` metadata version;
- `DEC-###` for a material decision, including source, date, status, rationale,
  and affected artifacts.
- `APR-001` through `APR-005` for stage approvals, including approved revision and
  the user's answer source.
- One pending question with its stage, exact text, options, and asked date.
- Explicit open assumptions and blockers; do not convert them into facts.

An approved [session context hook](context-hook.md) can load the existing short
checkpoint fields. Do not duplicate them in a separate summary. Keep their
labels and one-line values clear. A missing hook or unknown record format does
not prevent manual resume.

On resume, inspect actual files before trusting the checkpoint. Continue the
pending question if it still applies. If the user changes `DEC-###`, mark the old
value superseded, identify the dependency edges, invalidate affected `APR-###`
records and derived sections, and preserve unrelated approvals. Refresh only the
affected artifacts after renewed approval.

Record an explicit user-supplied change as the answer and decision source. Do not
ask the user to reconfirm that same decision. Ask only for its next unresolved
consequence or for approval of a revised stage bundle that the instruction did
not already approve.

Compare the recorded Skill version with the loaded `metadata.version`. On a
mismatch, read the intervening `CHANGELOG.md` entries and record whether artifact
or workflow contracts changed. Do not replace a pinned installation, regenerate
approved files, or invalidate approvals solely because a newer version exists.
Propose only the compatibility work that affects this project and wait for its
approval.

During discovery, limit writes to `.project-kickoff/DISCOVERY.md`, `CONTEXT.md`,
the explicitly approved `.project-kickoff/context-hook.json` activation marker,
and other user-approved planning notes. Hook configuration follows its separate
project-scoped approval and worktree procedure. Do not initialize dependencies, generate
a scaffold, seed a tracker, or select defaults while a dependent choice is open.
