/* Guards for the three rules at the top of src/dolly.css, plus doc drift.
   Everything here is derived from the stylesheet — no hardcoded move lists,
   so adding a move to the CSS and nowhere else is what makes these fail. */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');

const source = read('../src/dolly.css');
const readme = read('../README.md');

/* The comments deliberately quote the anti-patterns ("never overflow:hidden"),
   so every check below runs against declarations only. */
const css = source.replace(/\/\*[\s\S]*?\*\//g, '');

/* Flatten the stylesheet into blocks. @keyframes bodies are kept whole;
   other at-rules (@media) are descended into, so no amount of nesting can
   hide a rule from a guard.

   `order` is the offset of the rule's opening brace in the flattened source,
   because equal-specificity rules are resolved by source order and nothing
   else. */
function blocks(src, within = [], base = 0) {
  const out = [];
  let prelude = '';
  for (let i = 0; i < src.length; ) {
    if (src[i] !== '{') { prelude += src[i++]; continue; }
    let depth = 1, j = i + 1;
    while (j < src.length && depth > 0) {
      if (src[j] === '{') depth++;
      else if (src[j] === '}') depth--;
      j++;
    }
    const body = src.slice(i + 1, j - 1);
    const at = prelude.trim();
    const order = base + i;
    if (/^@keyframes\b/.test(at)) out.push({ keyframes: at.replace(/^@keyframes\s+/, ''), body, within, order });
    else if (at.startsWith('@')) out.push(...blocks(body, [...within, at], order + 1));
    else out.push({ selector: at, body, within, order });
    prelude = '';
    i = j;
  }
  return out;
}

const all = blocks(css);
const keyframes = all.filter((b) => b.keyframes);
const rules = all.filter((b) => b.selector);

const decls = (body) =>
  body
    .split(';')
    .map((d) => d.trim())
    .filter(Boolean)
    .map((d) => {
      const at = d.indexOf(':');
      return [d.slice(0, at).trim(), d.slice(at + 1).replace(/!important/, '').trim()];
    })
    .filter(([prop]) => prop);

/* move name -> animation-name, straight out of the [data-dolly="…"] rules */
const moves = new Map();
for (const rule of rules) {
  const name = rule.selector.match(/^\[data-dolly="([^"]+)"\]$/)?.[1];
  if (!name) continue;
  const animation = decls(rule.body).find(([p]) => p === 'animation-name')?.[1];
  if (animation && animation !== 'none') moves.set(name, animation);
}

test('every move has keyframes and every keyframes block has a move', () => {
  const defined = [...new Set(keyframes.map((k) => k.keyframes))].sort();
  const referenced = [...new Set(moves.values())].sort();
  assert.deepEqual(referenced, defined, 'orphaned keyframes or a move pointing at nothing');
});

test('no base rule hides an element — the hidden state lives in @keyframes only', () => {
  const hiding = { opacity: '0', visibility: 'hidden', display: 'none' };
  for (const rule of rules) {
    if (!rule.selector.includes('[data-dolly')) continue;
    for (const [prop, value] of decls(rule.body)) {
      assert.notEqual(
        hiding[prop],
        value,
        `${rule.selector} sets ${prop}: ${value} outside @keyframes — unsupported browsers would render nothing`
      );
    }
  }
});

test('the animation shorthand is never used (it resets animation-timeline)', () => {
  const shorthand = css.match(/(?:^|[;{}\s])animation\s*:/);
  assert.equal(shorthand, null, 'use animation-* longhands');
});

test('overflow: hidden is never used (it creates a scroll container)', () => {
  for (const rule of rules) {
    for (const [prop, value] of decls(rule.body)) {
      if (prop.startsWith('overflow')) {
        assert.notEqual(value, 'hidden', `${rule.selector} — use overflow: clip`);
      }
    }
  }
  assert.ok(/overflow\s*:\s*clip/.test(css), 'clip is the approved form and should be in use');
});

test('reduced motion turns every move off', () => {
  const off = rules.find(
    (rule) =>
      rule.within.some((at) => /prefers-reduced-motion\s*:\s*reduce/.test(at)) &&
      rule.selector.includes('[data-dolly') &&
      decls(rule.body).some(([p, v]) => p === 'animation-name' && v === 'none')
  );
  assert.ok(off, 'no @media (prefers-reduced-motion: reduce) rule setting animation-name: none');
});

/* `[data-dolly-range]` and `[data-dolly-ease]` are per-element overrides made
   of one attribute selector each, and every rule they have to beat is made of
   attribute selectors too — `[data-dolly-on="scene"]` sets a range, so does
   `[data-dolly="track"]`, and the beat group sets an easing. Specificity is
   therefore identical across all of them and source order is the entire
   mechanism. Move an override up the file, or append a new move rule below it,
   and the override stops overriding: no parse error, no warning, the knob
   documented in the README simply does nothing. */
const singleAttributeSelector = /^\[[^\]]+\](\s*,\s*\[[^\]]+\])*$/;

for (const [selector, property] of [
  ['[data-dolly-range]', 'animation-range'],
  ['[data-dolly-ease]', 'animation-timing-function'],
]) {
  test(`${selector} comes last, so it actually overrides ${property}`, () => {
    const override = rules.find((rule) => rule.selector === selector);
    assert.ok(override, `${selector} is missing from the stylesheet`);

    const rivals = rules.filter(
      (rule) =>
        rule !== override &&
        singleAttributeSelector.test(rule.selector.replace(/\s+/g, ' ')) &&
        decls(rule.body).some(([prop]) => prop === property)
    );
    assert.ok(rivals.length, `nothing else sets ${property} — this guard has stopped guarding`);

    const winning = rivals.filter((rule) => rule.order > override.order).map((rule) => rule.selector);
    assert.deepEqual(
      winning,
      [],
      `equal specificity, later in the file: these silently beat ${selector} instead of losing to it`
    );
  });
}

test('the README documents exactly the moves that ship', () => {
  const claimed = Number(readme.match(/\b(\d+) camera moves\b/)?.[1]);
  assert.equal(claimed, moves.size, 'the README move count disagrees with the stylesheet');

  /* Scoped to the Moves section on purpose. The knobs table names moves in its
     "Applies to" column, so an unscoped search counts `| `zoom` |` there as
     documentation and lets a move vanish from every move table unnoticed. */
  const movesSection = readme.match(/\n## Moves\n([\s\S]*?)\n## /)?.[1];
  assert.ok(movesSection, 'the README has no "## Moves" section to check against');

  const undocumented = [...moves.keys()].filter((name) => !movesSection.includes(`| \`${name}\` |`));
  assert.deepEqual(undocumented, [], 'missing from the README move tables');
});
