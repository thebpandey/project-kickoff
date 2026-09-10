#!/usr/bin/env node
/**
 * Check the published Project Kickoff field guide.
 *
 * The guide is a single self-contained HTML file. This script checks the
 * structural and editorial rules that the page must satisfy before the
 * orchestrator embeds the artwork and publishes it.
 *
 * Usage:
 *   node scripts/check-guide.mjs [path-to-guide.html]
 *
 * It prints one line per check and exits non-zero when any check fails.
 * It uses only the Node standard library.
 */

import { readFileSync } from "node:fs";
import { argv, exit } from "node:process";

const DEFAULT_GUIDE = "project-kickoff-guide-v0.3.1.html";
const GUIDE_IMAGES = [
  ["overview-image", "IMAGE_HERO_PLACEHOLDER"],
  ["flowchart-image", "IMAGE_FLOW_PLACEHOLDER"],
];
const FORBIDDEN_TEXT = ["Agent-Team field guide", "agent-team-guide-v7.0.2", "Morpheus"];

const guidePath = argv[2] ?? DEFAULT_GUIDE;
const html = readFileSync(guidePath, "utf8");

// A <pre> block quotes an official format verbatim. The prose rules do not apply inside one.
const prose = html.replace(/<pre>[\s\S]*?<\/pre>/g, "");

const results = [];

function check(name, run) {
  const failures = run();
  results.push({ name, failures });
}

function matchAll(pattern) {
  return [...html.matchAll(pattern)];
}

function countOccurrences(haystack, needle) {
  return haystack.split(needle).length - 1;
}

check("ids are unique and internal links resolve", () => {
  const ids = matchAll(/\sid="([^"]+)"/g).map((m) => m[1]);
  const problems = [];

  const seen = new Set();
  const duplicates = new Set();
  for (const id of ids) {
    if (seen.has(id)) duplicates.add(id);
    seen.add(id);
  }
  if (ids.length !== seen.size) {
    for (const id of duplicates) problems.push(`id "${id}" is used more than once`);
  }

  const targets = matchAll(/href="#([^"]+)"/g).map((m) => m[1]);
  for (const target of new Set(targets)) {
    if (!seen.has(target)) problems.push(`no element has id "${target}"`);
  }

  return problems;
});

// The orchestrator swaps each placeholder for a PNG data URI at integration.
// This check must hold before and after that swap, and must still fail if an
// image loses its source entirely.
check("both guide images have a usable source", () =>
  GUIDE_IMAGES.flatMap(([id, placeholder]) => {
    const tag = html.match(new RegExp(`<img[^>]*\\sid="${id}"[^>]*>`));
    if (!tag) return [`no img element has id "${id}"`];
    const src = (tag[0].match(/\ssrc="([^"]*)"/) || [])[1] || "";
    if (src === placeholder || src.startsWith("data:image/")) return [];
    return [`${id} src is neither ${placeholder} nor a data:image URI`];
  }));

check("no em dash and no en dash in prose", () => {
  const problems = [];
  for (const [label, character] of [["em dash", "—"], ["en dash", "–"]]) {
    const count = countOccurrences(prose, character);
    if (count > 0) problems.push(`${label} appears ${count} time(s) outside pre blocks`);
  }
  return problems;
});

check("heading, section, and image structure", () => {
  const problems = [];

  const headingCount = matchAll(/<h1\b/g).length;
  if (headingCount !== 1) problems.push(`found ${headingCount} h1 elements, expected 1`);

  const sections = matchAll(/<section\b([^>]*)>/g)
    .map((m) => m[1])
    .filter((attributes) => /class="[^"]*\bsection\b[^"]*"/.test(attributes));
  const sectionsWithoutId = sections.filter((attributes) => !/\sid="[^"]+"/.test(attributes));
  if (sectionsWithoutId.length > 0) {
    problems.push(`${sectionsWithoutId.length} section.section elements have no id`);
  }

  // The dialog image carries no src; the script fills its source and alt on open.
  const images = matchAll(/<img\b[^>]*>/g).map((m) => m[0]).filter((tag) => /\ssrc="/.test(tag));
  for (const tag of images) {
    const alt = tag.match(/\salt="([^"]*)"/);
    if (!alt || alt[1].trim() === "") problems.push(`img without alt text: ${tag.slice(0, 80)}`);
  }

  return problems;
});

check("no leftover reference-guide text", () =>
  FORBIDDEN_TEXT.filter((text) => html.includes(text)).map((text) => `found "${text}"`));

check("every command block has a pre and a Copy button", () => {
  const blocks = html.split('<div class="command">').slice(1);
  const problems = [];
  blocks.forEach((block, index) => {
    const end = block.indexOf("</pre>");
    if (end === -1) {
      problems.push(`command block ${index + 1} has no pre element`);
      return;
    }
    const head = block.slice(0, end);
    if (!head.includes("<pre>")) problems.push(`command block ${index + 1} has no opening pre tag`);
    if (!head.includes('class="copy"')) problems.push(`command block ${index + 1} has no Copy button`);
  });
  if (blocks.length === 0) problems.push("no command blocks found");
  return problems;
});

let failed = 0;
for (const { name, failures } of results) {
  if (failures.length === 0) {
    console.log(`PASS  ${name}`);
  } else {
    failed += 1;
    console.log(`FAIL  ${name}`);
    for (const failure of failures) console.log(`      ${failure}`);
  }
}

console.log(`\n${results.length - failed} of ${results.length} checks passed for ${guidePath}`);
exit(failed === 0 ? 0 : 1);
