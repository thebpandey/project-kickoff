<!--
TEMPLATE INSTRUCTIONS — remove this comment after adapting the document.
- Use approved PRD and discovery decisions. Replace every {{...}} value.
- Keep the sections that apply to the product's interface. For a CLI, API, or
  library with no visual UI, use the nonvisual contract and remove visual tokens.
- Do not invent screens, branding, accessibility targets, or reference products.
-->

# {{Project name}} — Experience and Design

Status: {{Draft | Awaiting approval | Approved | Superseded}}
Version: {{document version}}
Updated: {{YYYY-MM-DD}}
Interface type: {{Visual UI | CLI | API | Library | Mixed}}
Source: {{approved PRD version and DISCOVERY stage approval}}
Generated with: project-kickoff {{semantic version}}

## Experience intent

### Current experience and approved target

| Area | Current observed / documented state | Approved target | Evidence / decision |
| --- | --- | --- | --- |
| {{flow, visual system, API/CLI convention, content, accessibility}} | {{AUD ID/path/revision or Unverified}} | {{approved change, explicit preservation, assumption, or Open}} | {{AUD/EV/DDES/DEC/APR IDs}} |

For an existing product, preserve useful design guidance and working conventions.
Merge approved changes without implying that recommendations are implemented or
that untested behavior exists.

### Audience and context

{{Describe the primary users, their environment, domain familiarity, devices or
tools, time pressure, accessibility needs, and other confirmed context.}}

### Brand and communication

- Product promise: {{approved short promise}}
- Voice: {{specific traits with examples of what they mean}}
- Tone by situation: {{success, guidance, warning, failure, sensitive moment}}
- Terminology: {{preferred terms and terms to avoid}}
- Existing brand source: {{brand kit/link/version or None approved}}

### Interaction principles

| Principle | Required behavior | Avoid | Source |
| --- | --- | --- | --- |
| {{principle}} | {{concrete design consequence}} | {{specific failure pattern}} | {{decision, evidence, or requirement ID}} |

## Information structure and flows

### Structure

{{Describe navigation, commands, endpoints, modules, or other information
hierarchy appropriate to the interface. Explain how users find core actions.}}

### FLOW-001 — {{flow name}}

- Goal / linked journey: {{JNY-001 and REQ IDs}}
- Entry condition: {{trigger and prerequisites}}
- Steps: {{ordered interaction steps}}
- Decision points: {{meaningful choices and defaults}}
- Success state: {{observable completion and next option}}
- Empty / loading / partial state: {{behavior, when relevant}}
- Error and recovery: {{message, retained work, retry or escape route}}
- Accessibility considerations: {{keyboard, assistive technology, cognitive,
  contrast, motion, output format, or interface-specific need}}

## Accessibility requirements

| ID | Requirement | Applies to | Verification | Source |
| --- | --- | --- | --- | --- |
| A11Y-001 | {{approved standard or concrete accessible behavior}} | {{flow/component/output}} | {{manual or automated check and environment}} | {{REQ/NFR/decision/source}} |

Include only applicable requirements. Address input method, focus/order,
semantics, alternatives for non-text content, readable errors, color and motion,
localization, and zoom/reflow when relevant. Name a formal conformance level only
when it is an approved requirement and its source is recorded.

## Visual interface contract

<!-- Keep this section only for a visual or mixed interface. -->

### Visual direction

{{Describe the approved visual character, density, hierarchy, imagery, and
reference examples. State which qualities to borrow, not merely product names.}}

### Design tokens

Use semantic roles so themes and states remain consistent. Values below are
inputs, not recommended defaults.

```text
Typography
font.family.body       = {{approved font stack}}
font.family.display    = {{approved font stack or Same as body}}
font.size.*            = {{type scale}}
font.weight.*          = {{used weights}}
font.line-height.*     = {{line-height scale}}

Color
color.surface.*        = {{base/elevated/inverse values}}
color.text.*           = {{primary/secondary/inverse/disabled values}}
color.border.*         = {{default/strong/focus values}}
color.action.*         = {{primary/hover/pressed/disabled values}}
color.feedback.*       = {{success/warning/error/info values}}

Geometry
space.*                = {{spacing scale}}
radius.*               = {{radius scale}}
shadow.*               = {{elevation rules or None}}
layout.content-max     = {{approved maximum or Fluid}}
motion.duration.*      = {{duration scale or None}}
motion.easing.*        = {{easing values or None}}
```

For every foreground/background pair, record how contrast is verified against
the approved accessibility target. Do not rely on color alone for meaning.

### Layout and responsive behavior

| Context / breakpoint | Structure | Navigation | Density / content changes | Rationale |
| --- | --- | --- | --- | --- |
| {{width, device, container, or input context}} | {{grid/stack/regions}} | {{behavior}} | {{reflow, priority, wrapping; no unexplained hiding}} | {{user need or evidence}} |

Prefer content-driven breakpoints. Specify overflow, long text, zoom, touch
targets, safe areas, and orientation behavior where they affect the product.

### Component and interaction states

| Component / pattern | Default | Hover / focus / active | Disabled / read-only | Loading / empty | Error / recovery |
| --- | --- | --- | --- | --- | --- |
| {{component}} | {{appearance and behavior}} | {{visible and input-specific states}} | {{meaning and affordance}} | {{feedback and timing}} | {{message and next action}} |

### Content and media

- Labels and actions: {{grammar, length, capitalization, verb guidance}}
- Help and validation: {{placement, timing, actionable wording}}
- Dates, numbers, units: {{locale and formatting rules}}
- Images / icons / charts: {{style, sources, alternatives, empty/error behavior}}
- Destructive or irreversible actions: {{confirmation and recovery expectations}}

### Motion

{{State the purpose, triggers, duration principles, interruption behavior, and
reduced-motion alternative. Use "No product motion required" when approved.}}

## Nonvisual interface contract

<!-- Keep this section for CLI, API, or library interfaces. For mixed products,
keep the relevant subsections alongside the visual contract. -->

### Commands, endpoints, or public API

| Surface | Naming and structure | Inputs / defaults | Output / return contract | Stability |
| --- | --- | --- | --- | --- |
| {{command, endpoint, function, type, or event}} | {{approved convention}} | {{validation and explicit defaults}} | {{machine/human-readable shape}} | {{versioning or compatibility rule}} |

### Feedback, errors, and recovery

- Success output: {{what is returned, where, and exit/status behavior}}
- Validation errors: {{structure, field/location, remediation, status/exit code}}
- Partial failure: {{atomicity, retained work, retry/idempotency guidance}}
- Diagnostics: {{verbosity, logs, request/correlation IDs, redaction}}
- Automation: {{stable output mode, stdout/stderr, pagination, rate limits}}

### Documentation and examples

- Entry documentation: {{README, reference, generated docs, help command}}
- Minimum example set: {{happy path, common failure, authentication/setup if relevant}}
- Naming / terminology: {{case, nouns/verbs, abbreviations, deprecation}}
- Compatibility promise: {{semantic versioning or approved alternative}}

Visual typography, color, spacing, layout, responsive, component, and motion
sections are not applicable when users never interact with a rendered visual
interface. Record that reason here rather than inventing screens: {{reason or
"Not applicable because ..."}}.

## Design decisions and validation

| ID | Decision | Source | Requirements / flows affected | Validation evidence or planned check |
| --- | --- | --- | --- | --- |
| DDES-001 | {{approved experience choice}} | {{DISCOVERY decision ID, source, date}} | {{REQ/FLOW IDs}} | {{prototype/usability/accessibility review or planned task ID}} |

Unresolved design questions: {{OQ IDs or None}}

Approval record: {{approval ID, approver, date, scope, and source; or Pending}}
