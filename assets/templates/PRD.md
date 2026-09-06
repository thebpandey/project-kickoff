<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- Replace every {{...}} value with approved project information or an explicit
  "Open" / "Not applicable — <reason>" value.
- Keep stable IDs. Do not renumber an ID after it is referenced elsewhere.
- Record evidence, assumptions, and approved decisions separately. Do not turn
  an assumption into a fact or invent a target, budget, date, or market result.
- Keep later-release ideas outside the first-release boundary.
-->

# {{Project name}} — Product Requirements Document

Status: {{Draft | Awaiting approval | Approved | Superseded}}
Version: {{document version}}
Updated: {{YYYY-MM-DD}}
Owner: {{project owner}}
Approval source: {{DISCOVERY.md stage approval ID/link, or Pending}}
Generated with: project-kickoff {{semantic version}}

## Product definition

### Summary

{{Describe the product, the problem it addresses, who it serves, and the value
of the first release in a short paragraph.}}

### Intended users and problems

| User group | Context | Problem or unmet need | Current alternative | Evidence / assumption ID |
| --- | --- | --- | --- | --- |
| {{user group}} | {{when and where the need occurs}} | {{observable problem}} | {{current behavior or product}} | {{EV-001 or ASM-001}} |

### Evidence

| ID | Claim supported | Source and date | Strength / limits | Affected requirements |
| --- | --- | --- | --- | --- |
| EV-001 | {{claim}} | {{interview, research, analytics, or test; link; YYYY-MM-DD}} | {{what the source establishes and does not establish}} | {{REQ-001}} |

### Assumptions and risks

| ID | Assumption | Why it matters | Validation method | Owner / timing | Status |
| --- | --- | --- | --- | --- | --- |
| ASM-001 | {{unverified proposition}} | {{impact if false}} | {{specific test or evidence needed}} | {{owner / milestone}} | {{Unverified / Supported / Disproved}} |
| RISK-001 | {{product, delivery, technical, legal, or operational risk}} | {{impact and likelihood if known}} | {{mitigation or contingency}} | {{owner / trigger}} | {{Open / Mitigated / Accepted}} |

## Outcomes and scope

### Current state and approved target

<!-- For a new project, describe the current state as approved planning or the
minimal verified scaffold. For an existing project, link AUDIT findings and
preserve the prior approved baseline. -->

| Area | Current observed / documented state | Approved first-release target | Evidence / decision |
| --- | --- | --- | --- |
| {{product behavior, architecture, stack, or operations}} | {{fact with AUD/EV/path/revision, or Unverified}} | {{approved target, or Assumption/Open}} | {{AUD/EV/DEC/APR IDs}} |

An inferred target remains an assumption until approved. Approved changes do
not erase current behavior, documentation, stable IDs, or approval history.

### Expected outcomes and success measures

| Outcome ID | Desired change | Measure | Baseline | First-release target | Measurement method / window |
| --- | --- | --- | --- | --- | --- |
| OUT-001 | {{observable user or business outcome}} | {{metric or qualitative signal}} | {{known value or Not yet measured}} | {{approved target or Open}} | {{how and when it will be assessed}} |

Do not use delivery activity, task count, or lines of code as a product outcome.

### First-release boundary

Included:

- {{capability or journey explicitly approved for the first release}}

Excluded / non-goals:

- {{capability intentionally excluded and why}}

Later ideas belong in the roadmap section of `PLAN.md`; they are not approved
first-release requirements or active tasks.

### User journeys

#### JNY-001 — {{journey name}}

- Actor and trigger: {{who starts it and why}}
- Preconditions: {{required state}}
- Main path: {{ordered, observable steps at product level}}
- Alternate / failure path: {{important recovery behavior}}
- Successful end state: {{what the user can observe}}
- Requirements: {{REQ-001, REQ-002}}

## First-release requirements

Use `REQ-###` for functional requirements and `NFR-###` for quality constraints.
Each criterion must be observable without prescribing unnecessary implementation.

| ID | Requirement | Priority | Acceptance criteria | Journey / outcome | Evidence / decision source |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | {{required product behavior}} | {{Must / Should / Could}} | {{Given/when/then or another observable result}} | {{JNY-001 / OUT-001}} | {{DEC-001 / EV-001 / DISCOVERY link}} |
| NFR-001 | {{accessibility, reliability, security, compatibility, or performance requirement}} | {{Must / Should / Could}} | {{measurable or directly verifiable criterion; use Open if target is undecided}} | {{affected journey}} | {{decision or authoritative source}} |

## Constraints

| ID | Constraint | Source | Effect on the solution | Status |
| --- | --- | --- | --- | --- |
| CON-001 | {{budget, schedule, policy, platform, staffing, legal, compatibility, or other constraint}} | {{user decision, policy, or evidence link}} | {{architectural or scope consequence}} | {{Approved / Open / Assumed}} |

## Technical blueprint

### Architecture and rationale

{{Describe the system boundary, major components, communication paths, runtime
shape, and why this architecture fits the approved first release. State what is
owned by this project and what is an external dependency.}}

```text
{{Optional project-specific component/data-flow diagram. Remove when prose is clearer.}}
```

### Stack selection

| Concern | Considered options | Selected option | Rationale and trade-offs | Decision ID |
| --- | --- | --- | --- | --- |
| {{runtime/framework/database/build/deployment concern}} | {{credible alternatives considered}} | {{approved selection or Open}} | {{fit, cost, constraints, and accepted downside}} | {{DEC-001}} |

Do not name a selected stack until the user has approved it. Verify current
version, support, license, and platform facts when those facts affect the choice.

### Components and boundaries

| Component | Responsibility | Interfaces | Owns data? | Trust / failure boundary |
| --- | --- | --- | --- | --- |
| {{component}} | {{single clear responsibility}} | {{API, event, command, file, UI, or library surface}} | {{dataset or None}} | {{validation, timeout, retry, or isolation concern}} |

### Data ownership and lifecycle

| Data | System of record / owner | Created or received | Retention / deletion | Sensitivity and access | Backup / recovery |
| --- | --- | --- | --- | --- | --- |
| {{data class}} | {{project component, user, or external system}} | {{source and purpose}} | {{approved rule or Open}} | {{classification and authorized actors}} | {{requirement or Not applicable — reason}} |

Record data residency, migration, portability, audit, and consent needs when
they are relevant. Never put credentials or real personal data in this file.

### Integrations

| Integration | Purpose | Direction / protocol | Authentication | Failure behavior | Owner / source |
| --- | --- | --- | --- | --- | --- |
| {{service or system}} | {{why it is needed}} | {{inbound/outbound and interface}} | {{approved mechanism or Open}} | {{timeout, retry, fallback, reconciliation}} | {{team/vendor and docs link}} |

### Security and privacy needs

- Identity and authorization: {{roles, boundaries, or Not applicable — reason}}
- Input and output protection: {{validation, encoding, abuse controls}}
- Secrets: {{approved secret store and local-development approach; no values}}
- Sensitive data: {{classification, minimization, encryption, logging limits}}
- Supply chain: {{dependency and provenance expectations}}
- Threats requiring design work: {{project-relevant threats or Open}}
- Compliance / policy: {{confirmed obligations and source; avoid unsupported claims}}

### Deployment and operations

- Target environment: {{approved host/runtime or Assumption — ...}}
- Environments: {{local, test, staging, production as actually needed}}
- Configuration: {{source and validation approach}}
- Observability: {{logs, metrics, traces, alerts tied to requirements}}
- Reliability / recovery: {{availability, backup, rollback, RTO/RPO if approved}}
- Release authority: {{who may deploy and required gates}}
- Operational ownership: {{owner and support expectation}}

### Intended folder structure

Adapt this tree to the selected architecture. Include only folders the first
release needs and add a brief responsibility for each.

```text
{{project-root}}/
├── {{source-directory}}/       # {{responsibility}}
├── {{test-directory}}/         # {{responsibility}}
├── {{docs-directory}}/         # {{responsibility}}
├── AGENTS.md                   # Shared agent policy
├── CLAUDE.md                   # Claude Code adapter
├── PRD.md                      # Approved product baseline
├── DESIGN.md                   # Approved experience guidance
└── PLAN.md                     # Approved implementation baseline
```

## Decisions and open questions

### Approved decisions

| ID | Decision | Alternatives / trade-offs | Source and date | Affected artifacts |
| --- | --- | --- | --- | --- |
| DEC-001 | {{approved choice}} | {{options considered and accepted trade-off}} | {{DISCOVERY decision ID/link; YYYY-MM-DD}} | {{PRD, DESIGN, PLAN, scaffold paths}} |

### Existing ID and baseline reconciliation

| Existing artifact / ID | Current meaning / last approval | Target artifact / ID | Action | Source |
| --- | --- | --- | --- | --- |
| {{path and existing REQ/decision ID}} | {{definition and baseline revision}} | {{same stable ID or explicit new ID}} | {{Preserve / Merge / Deprecate with mapping / Add}} | {{AUD/DEC/APR IDs}} |

For an existing project, merge this PRD into useful current documentation. Do
not replace files wholesale or renumber referenced IDs for formatting. Record an
old-to-new mapping and approval before an unavoidable migration.

### Open questions

| ID | Question | Why it blocks or affects work | Owner | Next decision point |
| --- | --- | --- | --- | --- |
| OQ-001 | {{one unresolved question}} | {{affected requirement or design}} | {{decision owner}} | {{before stage/task/milestone}} |

## Traceability and approval

- Requirement-to-task mapping: [`PLAN.md`](PLAN.md)
- Interview evidence and stage approvals: [`.project-kickoff/DISCOVERY.md`](.project-kickoff/DISCOVERY.md)
- Current resumption state: [`CONTEXT.md`](CONTEXT.md)

Approval record: {{approval ID, approver, date, scope, and source; or Pending}}

When an approved decision changes, record the new decision in `DISCOVERY.md`,
mark the affected approval there as invalidated, update this document and its
version, and reconcile affected plan tasks. Preserve unrelated approvals.
