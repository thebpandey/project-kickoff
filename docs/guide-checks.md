# Field guide checks

Checked: 2026-09-10

This report records the automated checks for the published field guide
`project-kickoff-guide-v0.3.1.html`. The checked source is the
`feat/kickoff-guide` worktree at base revision
`185af44ecd973a4deca172d8dca16ec7cf7224b0`. The page is a single self-contained
HTML file with one inline stylesheet and one inline script. It loads no external
CSS, JavaScript, or font.

The two images are not embedded yet. The page carries the literal strings
`IMAGE_HERO_PLACEHOLDER` and `IMAGE_FLOW_PLACEHOLDER` as the `src` values. The
project orchestrator replaces them with PNG data URIs at integration.

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
| Internal links resolve | Passed. Every `href="#id"` in the page resolves to an element with that `id`. |
| Image placeholders | Passed. `IMAGE_HERO_PLACEHOLDER` and `IMAGE_FLOW_PLACEHOLDER` each appear exactly once. |
| Dash characters | Passed. No U+2014 em dash and no U+2013 en dash anywhere in the file. |
| Heading, section, and image structure | Passed. Exactly one `h1`. All 10 `section.section` elements have an `id`. Both images that carry a `src` have non-empty `alt` text. |
| Reference-guide text | Passed. The strings `Agent-Team field guide`, `agent-team-guide-v7.0.2`, and `Morpheus` are absent. |
| Command blocks | Passed. All 13 `.command` blocks contain a `<pre>` element and a Copy button. |

The dialog image `#modal-image` carries no `src` and an empty `alt`. The inline
script sets both values when a reader opens the image dialog. The image check
therefore inspects only `img` elements that ship a `src` attribute.

## Negative check

A deliberately broken copy of the page was checked to confirm that the script can
fail. The copy renamed `IMAGE_FLOW_PLACEHOLDER` to `IMAGE_HERO_PLACEHOLDER` and
inserted the string `Morpheus`. The script reported both failures and exited `1`.

## Shell checks

| Command | Actual result |
| --- | --- |
| `grep -o '[A-Za-z_]*PLACEHOLDER[A-Za-z_]*' project-kickoff-guide-v0.3.1.html \| sort \| uniq -c` | Exactly two lines: `1 IMAGE_FLOW_PLACEHOLDER` and `1 IMAGE_HERO_PLACEHOLDER`. No other placeholder remains. |
| `grep -c -E 'TODO\|TBD\|FIXME\|XXX\|lorem ipsum\|\[INSERT' project-kickoff-guide-v0.3.1.html` | `0`. |
| `grep -c '<section class="section"' project-kickoff-guide-v0.3.1.html` | `10`, matching the ten rail links. |

A disposable tag-balance script counted opening and closing tags for `div`,
`section`, `article`, `figure`, `ol`, `ul`, `li`, `table`, `details`, `pre`,
`button`, `dialog`, `main`, `aside`, `header`, `footer`, `p`, `h2`, `h3`, `td`,
`th`, and `tr`. Every pair matched. The page has one `h1` and ten `h2` headings.

## Limits

These checks validate structure, links, placeholders, dash characters, and
command-block shape. No browser rendered the page, and no W3C validator ran. The
copy button and the image dialog were not exercised in a real browser; their
script is copied verbatim from the checked Agent-Team 7.0.2 guide. The stylesheet
is also copied verbatim from that guide with no added or changed rule.

Editorial rules that a script cannot check were applied by hand: ASD-STE100
sentence limits for the instructional text, and the human-writing rules for the
headings, ledes, callouts, and worked examples. This report does not claim formal
ASD-STE100 certification.

No image was generated, converted, or embedded here. No release, tag, push, or
GitHub Pages change occurred.
