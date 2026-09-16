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
  /* One narrow exception, and it must stay narrow. A decorative depth layer
     (data-dolly-plate) is not content: with no timeline it would park at
     opacity 1 with no translate, piling every plate at dead centre. Removing
     it restores the authored page, so hiding IS the correct degradation —
     but only inside a degradation block, and never for a move. */
  const degrading = (rule) =>
    rule.selector.includes('[data-dolly-plate]') &&
    rule.within.some((at) => /@supports\s+not|prefers-reduced-motion|print/.test(at));

  for (const rule of rules) {
    if (!rule.selector.includes('[data-dolly')) continue;
    if (degrading(rule)) continue;
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

/* The ordering guards are gone with the rules they guarded. The invariant
   now is that every built-in default is reachable through the knob: if a
   rule sets animation-range to a bare value, the author's --dolly-range
   cannot override it and the knob silently does nothing for that move. */
test('every built-in animation-range is overridable through --dolly-range', () => {
  const offenders = rules
    .filter((rule) => rule.selector.startsWith('[data-dolly'))
    .flatMap((rule) =>
      decls(rule.body)
        .filter(([prop, value]) => prop === 'animation-range' && !value.includes('var(--dolly-range'))
        .map(([, value]) => `${rule.selector} -> animation-range: ${value}`)
    );
  assert.deepEqual(
    offenders,
    [],
    'these hardcode a range, so --dolly-range is a no-op on them'
  );
});

test('the scene binding is scoped to a descendant of a scene', () => {
  const stray = rules.find((rule) => rule.selector === '[data-dolly-on="scene"]');
  assert.ok(
    !stray,
    'unscoped: a data-dolly-on="scene" outside a scene binds to a timeline that ' +
      'does not exist, holds the from state, and renders invisible forever'
  );
  const scoped = rules.find((rule) => rule.selector === '[data-dolly-scene] [data-dolly-on="scene"]');
  assert.ok(scoped, 'the scoped scene-binding rule is missing');
});

test('moves whose `to` is not the authored state turn off without a timeline', () => {
  /* Rule 1 holds for the entrances, whose `to` IS the element as authored.
     A keyframes block with an explicit `to`/100% breaks that: with no
     timeline, fill-mode:both lands the element on it. `track` parks a row
     -60% inside overflow:clip, which is the exact disappearance this
     library promises never happens. */
  /* Only a FINAL keyframe that hides or displaces is dangerous. `hold`
     ends at opacity 1 with an identity translate — that is the authored
     state, which is the whole point of rule 1. */
  /* A var() whose FALLBACK is the identity resolves to identity when the
     author sets nothing, which is the case this guard is about. */
  const unvar = (v) => v.replace(/var\(\s*--[\w-]+\s*,\s*([^()]*)\)/g, '$1').trim();
  const zero = (n) => /^-?0(px|deg|%|em|rem)?$/.test(n);
  const identity = (p, raw) => {
    const v = unvar(raw);
    if (p === 'opacity') return v === '1';
    if (p === 'translate') return v === 'none' || v.split(/\s+/).every(zero);
    if (p === 'scale') return v === 'none' || v.split(/\s+/).every((n) => n === '1');
    if (p === 'rotate')
      return v === 'none' || zero(v.split(/\s+/).pop() || '');   /* `y 0deg` too */
    if (p === 'filter') return /^(none|blur\(0\w*\)|brightness\(1\))$/.test(v);
    return false;
  };

  const explicitTo = keyframes
    .filter((k) => {
      const m = k.body.match(/(?:^|[;}\s])(?:to|100%)\s*\{([^}]*)\}/);
      return m && decls(m[1]).some(([p, v]) => !identity(p, v));
    })
    .map((k) => k.keyframes);

  const moveOf = (kf) =>
    rules
      .filter((r) => decls(r.body).some(([p, v]) => p === 'animation-name' && v === kf))
      .map((r) => (r.selector.match(/\[data-dolly="([^"]+)"\]/) || [])[1])
      .filter(Boolean)[0];

  const guarded = rules
    .filter((r) => r.within.some((a) => a.includes('@supports') && a.includes('not')))
    .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]));

  const unguarded = explicitTo
    .map(moveOf)
    .filter(Boolean)
    /* progress parks on a full bar: visible and harmless. */
    .filter((move) => move !== 'progress' && !guarded.includes(move));

  assert.deepEqual(
    unguarded,
    [],
    'these land on an explicit `to` with no timeline — list them in the @supports not block'
  );
});

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

/* The README guard exists; the PAGE had no equivalent, and drifted to
   documenting 16 of 30 while demonstrating all of them. */
test('the demo page documents every move that ships', () => {
  const page = read('../index.html');
  const shipped = rules
    .filter((r) => decls(r.body).some(([p]) => p === 'animation-name'))
    .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]));

  const body = page.slice(page.indexOf('<tbody>'), page.indexOf('</tbody>'));
  const documented = [...body.matchAll(/<tr><td>([^<]+)<\/td>/g)].map((m) => m[1].trim());

  assert.deepEqual(
    [...new Set(shipped)].filter((m) => !documented.includes(m)),
    [],
    'the reference table on the page is missing moves the library ships'
  );
});

/* package.json drifted to "23 camera moves" while the library shipped 30.
   Three files now claim a count; all three are derived from one source. */
test('package.json agrees with the stylesheet on the move count', () => {
  const pkg = JSON.parse(read('../package.json'));
  const shipped = new Set(
    rules
      .filter((r) => decls(r.body).some(([p]) => p === 'animation-name'))
      .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]))
  );
  const claimed = Number((pkg.description.match(/(\d+) camera moves/) || [])[1]);
  assert.equal(claimed, shipped.size, 'package.json description has a stale move count');
});
