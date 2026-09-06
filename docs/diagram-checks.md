# README Mermaid diagram checks

Checked: 2026-09-06
Source: `README.md` at integration revision
`73a73d42e1244ba405f85335bb65d5d52d6c55bc`
Source blob: `57a3a144bab9b47d1308133e4fadad564e213a7f`

## Renderer

- Mermaid CLI: `@mermaid-js/mermaid-cli@11.17.0`
- Package source: npm registry package metadata for
  `@mermaid-js/mermaid-cli`; repository metadata points to
  `github.com/mermaid-js/mermaid-cli`; MIT license
- Node.js: `v24.16.0`
- npm: `12.0.2`
- Browser: Google Chrome `151.0.7922.108` at
  `/usr/bin/google-chrome`
- Installation: isolated under
  `/tmp/project-kickoff-diagrams-lOTXjH`; used `--ignore-scripts`,
  `--no-audit`, `--no-fund`, `--no-save`, and
  `PUPPETEER_SKIP_DOWNLOAD=true`
- Browser configuration: system Chrome with `--no-sandbox` and
  `--disable-setuid-sandbox`

The check did not modify a global install, the source README, or a project
dependency manifest. It did not use an external rendering service or upload a
diagram.

## Results

Both fenced Mermaid blocks were extracted from the committed README object.
Each block rendered independently to SVG and PNG. Mermaid CLI exited with status
0 for all four renders. The generated SVG files contain no Mermaid syntax-error
or parse-error marker.

| Block | README section | Result | SVG layout | Visual inspection |
| --- | --- | --- | --- | --- |
| 1 | How the workflow operates | Pass with layout warning | View box `0.5 0 1515.2265625 4193.921875`; PNG `3032 × 8388` | All nodes, labels, arrowheads, and the stage subgraph render. No clipping or node overlap was visible. The vertical aspect ratio makes labels small when the full chart is fitted to a normal README content column. |
| 2 | Dependencies | Pass | View box `0 0 2094.6875 1083.5`; PNG `4190 × 2168` | All nodes, labels, decisions, optional links, and handoff paths render. No clipping or node overlap was visible. The aspect ratio is suitable for inline README display. |

The first chart's tall layout is a readability concern, not a parse failure. A
reader can inspect the SVG at full size, but the inline GitHub view can require
zooming. Splitting the workflow or changing its layout direction would improve
inline legibility if the author chooses to revise it.

## Evidence

The preview files remain in the temporary directory for parent visual review:

- `/tmp/project-kickoff-diagrams-lOTXjH/readme-diagram-01.png`
- `/tmp/project-kickoff-diagrams-lOTXjH/readme-diagram-01.svg`
- `/tmp/project-kickoff-diagrams-lOTXjH/readme-diagram-02.png`
- `/tmp/project-kickoff-diagrams-lOTXjH/readme-diagram-02.svg`

Source block hashes:

- Block 1: `904ef580845a09ca1a4fe028324072412548c36b4da6162c9d92d6284831b0aa`
- Block 2: `7473fa8b14f7d400676f213326b07247e2d9674392b106aef6da6eb65fa07352`

Rendered artifact hashes:

- Block 1 SVG:
  `18b029dfc9c711674566c6539fcec9149a229924f9433536a32d1d2dba0f4386`
- Block 1 PNG:
  `2a666f0b627b31c7c8d964383a1f0c5172c652a4507ed8f2a229c739b45660cb`
- Block 2 SVG:
  `b6ca08179eb52a9c36fbb3ac99a5d45df85cbf8b975fcdadf78d7730e058a7d3`
- Block 2 PNG:
  `be24dc3299106d26a36b014fb40629a3239df1d8010c3a81511d094a4632c33b`

## Limits

This check used Mermaid CLI 11.17.0 with its default theme and a white
background. GitHub can use a different Mermaid release, theme, font, or
responsive container. Local rendering proves that this renderer accepts the
syntax and that the generated layouts contain the expected visible elements. It
does not prove pixel-identical GitHub rendering. The parent visual review of the
retained PNGs is still required before temporary preview cleanup.
