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
/* animation-name is a LIST: `sequence` drives one stepped animation per axis
   so its sheet can be a grid. Map each move to every keyframes block it
   names, so the bijection below still catches an orphan on either side. */
const moves = new Map();
for (const rule of rules) {
  const name = rule.selector.match(/^\[data-dolly="([^"]+)"\]$/)?.[1];
  if (!name) continue;
  const animation = decls(rule.body).find(([p]) => p === 'animation-name')?.[1];
  if (!animation || animation === 'none') continue;
  const named = animation.split(',').map((n) => n.trim()).filter((n) => n && n !== 'none');
  if (named.length) moves.set(name, named);
}

/* exit name -> animation-name, out of the [data-dolly-exit="…"] rules. Exit
   names repeat entrance names on purpose, so they get their own map. */
const exits = new Map();
for (const rule of rules) {
  const name = rule.selector.match(/^\[data-dolly-exit="([^"]+)"\]$/)?.[1];
  if (!name) continue;
  const animation = decls(rule.body).find(([p]) => p === 'animation-name')?.[1];
  if (animation && animation !== 'none') exits.set(name, animation);
}

test('every move has keyframes and every keyframes block has a move', () => {
  const defined = [...new Set(keyframes.map((k) => k.keyframes))].sort();
  const referenced = [...new Set([...[...moves.values()].flat(), ...exits.values()])].sort();
  assert.deepEqual(referenced, defined, 'orphaned keyframes or a move pointing at nothing');

  /* An exit is `to` only: its start is the element as authored, which is
     what lets it sit untouched until it leaves. A `from` would hide it. */
  for (const [name, kf] of exits) {
    const body = keyframes.find((k) => k.keyframes === kf)?.body || '';
    const steps = [...body.matchAll(/([\w%.,\s]+)\{/g)].map((m) => m[1].trim());
    assert.deepEqual(steps, ['to'], `exit ${name} must have a single \`to\` keyframe`);
  }
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

  /* The rule above is satisfied by [data-dolly] alone, so it cannot see
     exits. They need their own. */
  const exitOff = rules.find(
    (rule) =>
      rule.within.some((at) => /prefers-reduced-motion\s*:\s*reduce/.test(at)) &&
      rule.selector.includes('[data-dolly-exit]') &&
      decls(rule.body).some(([p, v]) => p === 'animation-name' && v === 'none')
  );
  assert.ok(exitOff, 'reduced motion does not turn exits off');
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
      .map((r) => {
        const exit = r.selector.match(/\[data-dolly-exit="([^"]+)"\]/)?.[1];
        return exit ? `exit:${exit}` : (r.selector.match(/\[data-dolly="([^"]+)"\]/) || [])[1];
      })
      .filter(Boolean)[0];

  const inSupportsNot = rules.filter((r) => r.within.some((a) => a.includes('@supports') && a.includes('not')));
  const guarded = inSupportsNot
    .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]));
  /* One bare [data-dolly-exit] rule turns every exit off at once. */
  if (inSupportsNot.some((r) => /(^|,)\s*\[data-dolly-exit\]\s*(,|$)/.test(r.selector) &&
      /animation-name\s*:\s*none\s*!important/.test(r.body))) {
    guarded.push(...[...exits.keys()].map((n) => `exit:${n}`));
  }

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

/* agents.md is the file other people's agents read to write Dolly markup.
   A move missing from it is a move no assistant will ever suggest, which is a
   quieter failure than a missing README row and a more expensive one. Prose
   lists are allowed here — the check is only that the name appears as code. */
test('agents.md names every move that ships', () => {
  const agents = read('../agents.md');
  const shipped = new Set(
    rules
      .filter((r) => decls(r.body).some(([p]) => p === 'animation-name'))
      .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]))
  );
  const missing = [...shipped].filter((name) => !agents.includes(`\`${name}\``));
  assert.deepEqual(missing, [], 'missing from agents.md');
});

/* moves.html is the reference page: one card per move, each playing on its
   own view timeline. It is generated by scripts/build-moves.py, which aborts
   if a move is missing from its groups — this guard is the second half of
   that, catching a stale committed page that was never regenerated. */
test('the moves page has a live card for every move that ships', () => {
  const page = read('../moves.html');
  const shipped = [...new Set(
    rules
      .filter((r) => decls(r.body).some(([p]) => p === 'animation-name'))
      .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]))
  )];

  assert.deepEqual(
    shipped.filter((n) => !page.includes(`<article class="card" id="${n}">`)),
    [], 'moves.html is missing a card — rerun scripts/build-moves.py'
  );
  /* A card that names the move but never applies it is a screenshot, not a
     demo. Each card must actually carry the attribute. */
  assert.deepEqual(
    shipped.filter((n) => !page.includes(`data-dolly="${n}"`)),
    [], 'a card names a move it never applies'
  );
});

/* A clip-path with only one end written takes its other end from the
   element, whose clip-path is `none` unless something sets it, and `none` does
   not interpolate with inset() or circle(): the move swaps halfway instead of
   wiping. `reveal` shipped like that from the start. Every one-ended clip move
   needs a base clip-path of the same shape. */
test('clip wipes have an end state of the same shape to interpolate to', () => {
  const shapeOf = (v) => v.match(/^\s*(inset|circle|ellipse|polygon)\(/)?.[1];
  const steps = (body) => [...body.matchAll(/(from|to|\d+%)\s*\{([^}]*)\}/g)]
    .map((m) => ({ at: m[1], decls: decls(m[2]) }));
  const broken = [];
  const check = (attr, map) => {
    for (const [name, anims] of map) {
      for (const kf of [anims].flat()) {
        const body = keyframes.find((k) => k.keyframes === kf)?.body || '';
        const clips = steps(body).filter((st) => st.decls.some(([p]) => p === 'clip-path'));
        if (clips.length !== 1) continue;
        const shape = shapeOf(clips[0].decls.find(([p]) => p === 'clip-path')[1]);
        const sel = `[${attr}="${name}"]`;
        const base = rules.find((r) => !r.within.length &&
          r.selector.split(',').map((x) => x.trim()).includes(sel) &&
          decls(r.body).some(([p, v]) => p === 'clip-path' && shapeOf(v) === shape));
        if (!base) broken.push(`${sel} (${kf})`);
      }
    }
  };
  check('data-dolly', moves);
  check('data-dolly-exit', exits);
  assert.deepEqual(broken, [], 'these clip moves swap instead of wiping');
});

/* Exits are documented in their own section, because every exit name is
   also an entrance name and would already "appear" in the move tables. */
test('the README documents every exit that ships', () => {
  const section = readme.match(/\n## Exits\n([\s\S]*?)(\n## |$)/)?.[1];
  assert.ok(section, 'the README has no "## Exits" section');
  const rows = [...section.matchAll(/^\| `([^`]+)` \|/gm)].map((m) => m[1]).sort();
  assert.deepEqual(rows, [...exits.keys()].sort(), 'the README exit table disagrees with the stylesheet');
});

test('agents.md documents every exit that ships', () => {
  const agents = read('../agents.md');
  const missing = [...exits.keys()].filter((n) => !agents.includes(`data-dolly-exit="${n}"`));
  assert.deepEqual(missing, [], 'missing from agents.md');
});

test('the moves page has a live card for every exit', () => {
  const page = read('../moves.html');
  const missing = [...exits.keys()].filter((n) => {
    const at = page.indexOf(`id="exit-${n}"`);
    const next = page.indexOf('<article', at + 1);
    return at < 0 || !page.slice(at, next < 0 ? undefined : next).includes(`data-dolly-exit="${n}"`);
  });
  assert.deepEqual(missing, [], 'moves.html is missing an exit card — rerun scripts/build-moves.py');
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

/* The @supports-not block is the library's whole promise for the 13% of
   traffic with no scroll timelines: moves whose `to` is not the authored
   state must turn themselves OFF. Its selectors are (0,1,0) and so are the
   move rules, so whichever comes last wins — and the move rules come last.
   That shipped: seven of thirteen moves (beat, beat-in, iris, letter, mask,
   sequence, track) had their safety net silently defeated, and Act V's copy
   rendered at opacity 0 in Firefox 158. Caught by a console check, not by a
   test, which is why this exists. */
test('the no-timeline safety block cannot be overridden by a later move rule', () => {
  const supportsBlocks = blocks(css).filter(
    (b) => b.within.some((at) => /^@supports\s+not\s*\(animation-timeline/.test(at))
  );
  const guarded = supportsBlocks.filter((b) => /\[data-dolly(-exit)?(="|\])/.test(b.selector || ''));
  assert.ok(guarded.length > 0, 'no @supports-not block turning moves off — the promise is gone');

  for (const b of guarded) {
    const names = [...b.selector.matchAll(/\[data-dolly(?:-exit)?="([^"]+)"\]/g)].map((m) => m[1]);
    const decl = decls(b.body).find(([p]) => p === 'animation-name');
    assert.ok(decl, `@supports-not block for ${names.join(', ') || b.selector} sets no animation-name`);

    /* Either it wins by !important, or every move it names is declared
       nowhere after it. Anything else and the net is defeated.
       NB: decls() strips !important, so this reads the raw body. */
    const wins = /animation-name\s*:[^;]*!important/.test(b.body);
    if (!wins) {
      const laterNames = rules
        .filter((r) => r.order > b.order)
        .filter((r) => decls(r.body).some(([p]) => p === 'animation-name'))
        .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]));
      const defeated = names.filter((n) => laterNames.includes(n));
      assert.deepEqual(defeated, [],
        'these moves re-declare animation-name after the safety block, defeating it');
    }
  }
});

/* The social card said "31 moves" while the library shipped 34, and no test
   could see it because the claim lives in a PNG. scripts/make-og.py now
   stamps the count it rendered into a tEXt chunk, which is plain ASCII in
   the file, so this reads it back without an image library. */
test('the social card was rendered from the current move count', () => {
  const png = readFileSync(new URL('../assets/og-image.png', import.meta.url));
  const i = png.indexOf('dolly-moves');
  assert.ok(i > 0,
    'assets/og-image.png carries no move count — rerun scripts/make-og.py');

  /* tEXt chunk: keyword, NUL, then the value, to the end of the chunk. */
  const start = i + 'dolly-moves'.length + 1;
  const stamped = Number(png.subarray(start, start + 8).toString('ascii').match(/^\d+/)?.[0]);

  const shipped = new Set(
    rules
      .filter((r) => decls(r.body).some(([p]) => p === 'animation-name'))
      .flatMap((r) => [...r.selector.matchAll(/\[data-dolly="([^"]+)"\]/g)].map((m) => m[1]))
  );
  assert.equal(stamped, shipped.size,
    'the social card is stale — rerun scripts/make-og.py');
});

test('the page binding is declared after every move that sets a range', () => {
  /* [data-dolly-on="page"] carries one attribute selector, exactly like a
     move rule, so nothing but source order decides which animation-range
     survives. Declared above a move, it silently hands that move's default
     range back — on a scroll timeline, where entry/cover mean nothing.
     The scene binding is safe by specificity (it is a descendant selector);
     this one is safe only by position, so position is what gets guarded. */
  const pageBinding = rules.find((r) => r.selector === '[data-dolly-on="page"]');
  assert.ok(pageBinding, 'the page binding rule has gone missing');

  const movesWithRange = rules
    .filter((r) => /^\[data-dolly="[^"]+"\]$/.test(r.selector))
    .filter((r) => decls(r.body).some(([p]) => p === 'animation-range'))
    .filter((r) => r.order > pageBinding.order)
    .map((r) => r.selector);

  assert.deepEqual(
    movesWithRange,
    [],
    'these are declared below [data-dolly-on="page"] and take their range back from it'
  );
});

/* Reddit called the old homepage janky on phones and hated the pinning. These
   are the things that were taken out for it, and they stay out. Only real
   declarations and real start tags count: the page quotes `data-dolly-scene`
   in an escaped code sample, and that is documentation, not markup. */
test('the homepage keeps the removed effects out', () => {
  const page = read('../index.html');
  const pageCss = [...page.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)]
    .map((m) => m[1]).join('\n').replace(/\/\*[\s\S]*?\*\//g, '');
  const pageRules = blocks(pageCss).filter((b) => b.selector);
  const tags = page.replace(/<!--[\s\S]*?-->/g, '').match(/<[a-z][^>]*>/gi) || [];

  const found = [];
  for (const tag of tags) {
    for (const attr of ['data-dolly-scene', 'data-dolly-pin', 'data-dolly-depth']) {
      if (new RegExp(`\\s${attr}(=|\\s|>|$)`).test(tag)) found.push(`${attr} on ${tag.slice(0, 40)}`);
    }
    const move = tag.match(/\sdata-dolly="([^"]+)"/)?.[1];
    if (['beat', 'letter'].includes(move)) found.push(`data-dolly="${move}"`);
  }
  for (const rule of pageRules) {
    for (const [prop] of decls(rule.body)) {
      if (['filter', 'backdrop-filter', '-webkit-backdrop-filter', 'mix-blend-mode'].includes(prop)) {
        found.push(`${prop} on ${rule.selector}`);
      }
      if (prop === 'animation-timeline' && rule.selector.split(',').some((s) => s.trim() === ':root')) {
        found.push('a scroll-driven animation on :root');
      }
    }
  }
  assert.deepEqual(found, [], 'the homepage brought back an effect that was removed for performance');
});
