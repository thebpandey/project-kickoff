# Field guide checks

Checked: 2026-09-10

This report records the automated checks for the published field guide
`project-kickoff-guide-v0.3.1.html`. The checked source is the
`feat/kickoff-guide` worktree at base revision
`185af44ecd973a4deca172d8dca16ec7cf7224b0`. This revision applies the PKG-004
review findings against the earlier commit
`d06e2f4bb3111ac0b2f0bab8aa8f92573683e6bd`.

The page is a single self-contained HTML file with one inline stylesheet and one
inline script. It loads no external CSS, JavaScript, font, or image.

The two images are not embedded yet. The page carries the literal strings
`IMAGE_HERO_PLACEHOLDER` and `IMAGE_FLOW_PLACEHOLDER` as the `src` values. The
project orchestrator replaces them with PNG data URIs at integration. The image
check accepts either form, so it passes before and after that substitution.

## Checker

`scripts/check-guide.mjs` is plain Node with no third-party module. It reads the
built HTML, prints one line per check, and exits non-zero when any check fails.

```sh
node scripts/check-guide.mjs project-kickoff-guide-v0.3.1.html
```

## Results

Command exit status was `0`. All six checks passed.

| Check | Actual result |
| --- | --- |
| Ids are unique and internal links resolve | Passed. No `id` value repeats. Every `href="#id"` resolves to an element with that `id`. |
| Both guide images have a usable source | Passed. `#overview-image` and `#flowchart-image` each carry a `src` that equals its placeholder token or starts with `data:image/`. |
| No em dash and no en dash in prose | Passed. Zero U+2014 and zero U+2013 outside `<pre>` blocks. |
| Heading, section, and image structure | Passed. Exactly one `h1`. All 10 `section.section` elements have an `id`. Both images that carry a `src` have non-empty `alt` text. |
| Reference-guide text | Passed. The strings `Agent-Team field guide`, `agent-team-guide-v7.0.2`, and `Morpheus` are absent. |
| Command blocks | Passed. All 14 `.command` blocks contain a `<pre>` element and a Copy button. |

The dialog image `#modal-image` carries no `src` and an empty `alt`. The inline
script sets both values when a reader opens the image dialog. The image checks
therefore inspect only `img` elements that ship a `src` attribute.

### Dash exemption for quoted formats

`references/interview.md` specifies the plain-text question shape with an em dash
between each choice and its effect. The page reproduces that shape verbatim, so
five em dashes exist inside `<pre>` blocks. A `<pre>` quotes an official format
and is not prose. The dash check strips `<pre>` blocks before it scans, and the
prose outside them holds zero dashes of either kind.

Measured: 5 em dashes in the file, all 5 inside `<pre>`. Zero en dashes anywhere.

## Negative checks

Broken copies were built under `/tmp` and checked, then deleted. Each new check
failed on the defect it targets.

| Broken copy | Result |
| --- | --- |
| `id="title"` renamed to `id="top"`, so a duplicate id exists and every link still resolves | `FAIL ids are unique and internal links resolve / id "top" is used more than once`, exit `1`. The earlier set-based check passed this case. |
| The `src` attribute removed from `#overview-image` | `FAIL both guide images have a usable source / overview-image src is neither IMAGE_HERO_PLACEHOLDER nor a data:image URI`, exit `1`. |
| An em dash inserted into the `#states` heading | `FAIL no em dash and no en dash in prose / em dash appears 1 time(s) outside pre blocks`, exit `1`. |
| Both placeholders replaced with `data:image/png;base64,...` | All six checks passed, exit `0`. This is the post-embedding state. |

An earlier negative check confirmed the remaining checks can fail. A copy that
renamed one placeholder and inserted `Morpheus` failed the image and text checks
and exited `1`. A copy with a command block missing its `<pre>` failed check 6.

## Shell checks

| Command | Actual result |
| --- | --- |
| `grep -o '[A-Za-z_]*PLACEHOLDER[A-Za-z_]*' project-kickoff-guide-v0.3.1.html \| sort \| uniq -c` | Exactly two lines: `1 IMAGE_FLOW_PLACEHOLDER` and `1 IMAGE_HERO_PLACEHOLDER`. No other placeholder remains. |
| `grep -c -E 'TODO\|TBD\|FIXME\|XXX\|lorem ipsum\|\[INSERT' project-kickoff-guide-v0.3.1.html` | `0`. |
| `grep -c '<section class="section"' project-kickoff-guide-v0.3.1.html` | `10`, matching the ten rail links. |
| `grep -c -i 'private repository' project-kickoff-guide-v0.3.1.html` | `0`. The page states the proprietary Private Use License and the written-permission requirement, and makes no claim about repository visibility. |

A disposable tag-balance script counted opening and closing tags for `div`,
`section`, `article`, `figure`, `ol`, `ul`, `li`, `table`, `details`, `pre`,
`button`, `dialog`, `main`, `aside`, `header`, `footer`, `p`, `h2`, `h3`, `td`,
`th`, `tr`, and `a`. Every pair matched.

## Sentence length

A disposable analysis script split the prose into 539 sentences, excluding the
stylesheet, the script, and every `<pre>` block. It counted only tokens that
contain an alphanumeric character.

- Descriptive sentences over 25 words: `0`.
- Procedural sentences over 20 words: `0`.
- Longest sentence on the page: 25 words.

## Limits

These checks validate structure, links, ids, image sources, dash characters,
command-block shape, and sentence length. No browser rendered the page, and no
W3C validator ran. The copy button and the image dialog were not exercised in a
real browser; their script is copied verbatim from the checked Agent-Team 7.0.2
guide. The stylesheet is also copied verbatim from that guide with no added or
changed rule.

Vocabulary and structure rules that a script cannot check were applied by hand.
No authorized copy of ASD-STE100 or its approved dictionary was available, so
word choices outside the explicit banned list are reasoned, not dictionary
checked. This report does not claim formal ASD-STE100 compliance.

No image was generated, converted, or embedded here. No release, tag, push, or
GitHub Pages change occurred.
