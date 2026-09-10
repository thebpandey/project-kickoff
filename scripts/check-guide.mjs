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
const IMAGE_PLACEHOLDERS = ["IMAGE_HERO_PLACEHOLDER", "IMAGE_FLOW_PLACEHOLDER"];
const FORBIDDEN_TEXT = ["Agent-Team field guide", "agent-team-guide-v7.0.2", "Morpheus"];

const guidePath = argv[2] ?? DEFAULT_GUIDE;
const html = readFileSync(guidePath, "utf8");

const results = [];

function check(name, run) {
  const failures = run();
  results.push({ name, failures });
}

function matchAll(pattern) {
  return [...html.matchAll(pattern)];
}

function countOccurrences(needle) {
  return html.split(needle).length - 1;
}

check("internal links resolve", () => {
  const ids = new Set(matchAll(/\sid="([^"]+)"/g).map((m) => m[1]));
  const targets = matchAll(/href="#([^"]+)"/g).map((m) => m[1]);
  const missing = [...new Set(targets.filter((target) => !ids.has(target)))];
  return missing.map((target) => `no element has id "${target}"`);
});

check("image placeholders appear exactly once", () =>
  IMAGE_PLACEHOLDERS.flatMap((placeholder) => {
    const count = countOccurrences(placeholder);
    return count === 1 ? [] : [`${placeholder} appears ${count} times`];
  }));

check("no em dash and no en dash", () => {
  const problems = [];
  for (const [label, character] of [["em dash", "—"], ["en dash", "–"]]) {
    const count = countOccurrences(character);
    if (count > 0) problems.push(`${label} appears ${count} times`);
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
