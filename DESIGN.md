---
name: Project Kickoff
description: A tactile planning studio for turning ambiguity into approved execution records.
colors:
  action-coral: "#f17762"
  continuity-cyan: "#72d4d0"
  registration-brass: "#d5a54d"
  paper: "#f0e4cf"
  night: "#07121c"
  navy: "#0c1d2a"
  panel: "#102534"
  line: "#29404d"
  ink: "#f6efe3"
  muted: "#b9b2a8"
  subtle: "#89857f"
typography:
  display:
    fontFamily: '"Newsreader", "Iowan Old Style", Palatino, serif'
    fontSize: "clamp(3.8rem, 7.5vw, 6.8rem)"
    fontWeight: 700
    lineHeight: 0.9
    letterSpacing: "-0.035em"
  headline:
    fontFamily: '"Newsreader", "Iowan Old Style", Palatino, serif'
    fontSize: "clamp(2.4rem, 5vw, 4.8rem)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "-0.03em"
  body:
    fontFamily: '"Avenir Next", "Segoe UI", ui-sans-serif, system-ui, sans-serif'
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  mono:
    fontFamily: '"SFMono-Regular", Consolas, monospace'
    fontSize: "0.86rem"
    lineHeight: 1.7
rounded:
  control: "10px"
  surface: "14px"
spacing:
  control-x: "1.15rem"
  surface: "1.7rem"
components:
  button-primary:
    backgroundColor: "#f59a89"
    textColor: "{colors.night}"
    rounded: "{rounded.control}"
    padding: "0.75rem 1.15rem"
    height: "48px"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "1.7rem"
---

# Design System: Project Kickoff

## Overview

**Creative North Star: “The Tactile Planning Studio”**

Deep ink-blue work surfaces hold warm cotton paper, brass registration marks, coral actions, and cyan continuity lines. The result feels deliberate and archival rather than administrative: strategic serif headlines introduce each decision, while structured cards and connectors make the approval sequence legible. The generated planning plate is the primary image, but its meaning is repeated in alt text and page copy.

## Colors

Coral identifies action and active stage labels, cyan connects sequential work and continuity, and brass marks registration, boundary, and version facts. Paper is a rare high-contrast surface for the compatibility record. Dark navy layers and restrained blue-gray rules organize the remainder.

**The Material Role Rule.** Keep coral actionable, cyan connective, brass evidentiary, and paper exceptional.

## Typography

Self-hosted Newsreader (`font-display: swap`, weights 600–700) carries hero and section headings, falling back to Iowan Old Style and Palatino. Body and interface copy use the Avenir/Segoe/system sans stack. Monospace is reserved for commands, identifiers, approvals, versions, and compact labels.

The hero is constrained to roughly `9.5ch`; section headlines to `13ch`. On narrow screens, the hero becomes `clamp(3.35rem, 16vw, 5.1rem)` and section headings become `2.8rem`. The hero release line is intentionally sentence case sans on the final build rather than an uppercase monospace badge.

## Layout

A centered `1160px` container with `3rem` total side clearance supports an asymmetric two-column hero, two-column editorial section headers, a four-state grid, a five-stage connected path, paired decision panels, and a two-card handoff. Section spacing scales from `5rem` to `8rem`.

At `900px`, the hero and section headers stack, the state grid becomes two columns, the five-stage path becomes vertical with cyan down-connectors, and paired panels become single-column. At `680px`, side clearance becomes `1.25rem`; navigation scrolls horizontally; facts, states, handoff cards, captions, and footer stack; and the handoff arrow rotates downward. The command strip owns horizontal scrolling, long text wraps within cards, and root overflow is clipped.

## Elevation & Depth

Most structure comes from one-pixel borders and tonal surface changes. The hero image alone carries a large ambient shadow (`0 26px 75px #0008`) and blurred brass backglow; routine cards remain flat. The sticky header uses translucent night and `18px` backdrop blur. The paper compatibility panel creates depth by tonal inversion, not shadow.

## Shapes

Cards, flow stages, imagery, and callouts share soft planning-board corners (`14px`). Buttons and the command strip use tighter control corners (`10px`), while the release status dot is circular. Cyan connector rules bridge cards without turning them into a continuous pipeline graphic.

## Components

### Buttons and links

Buttons are at least `48px` high. The shipped primary uses light coral (`#f59a89`) with dark ink and no shadow; hover lift is `2px` without a color change. The secondary uses the panel surface and line border. Links use cyan and all links receive a visible `3px` coral focus outline with `4px` offset.

### Cards, paths, and boundaries

Panels combine the dark panel fill, one-pixel blue-gray line, `14px` radius, and `1.7rem` padding. State cards share one bordered grid with one-pixel gutters. Five path cards connect with cyan rules that turn downward below `900px`. The brass boundary callout uses a faint brass wash; the compatibility record reverses to paper with dark text.

### Navigation, imagery, and handoff

The header remains sticky, with brass confined to the emphasized wordmark. The hero image is cropped to `8 / 5`, fills its column, and carries a descriptive alt; its caption is uppercase monospace. The handoff uses two balanced cards separated by a cyan arrow, then linearizes vertically on mobile.

## Do's and Don'ts

- **Do** keep coral, cyan, brass, and paper in their established material roles.
- **Do** preserve the visible distinction between producer, tested compatibility, and current native version facts.
- **Do** retain the skip link, semantic image description, visible focus indicators, and `prefers-reduced-motion` treatment; reduced motion disables smooth scrolling, transitions, and hover lift.
- **Don't** make the planning illustration necessary to understand the lifecycle.
- **Don't** add shadows to routine planning cards or overuse the paper surface.
- **Don't** allow the connected path, command strip, or navigation to create page-level horizontal overflow.
