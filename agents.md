# Dolly for agents

Scroll-driven motion in pure CSS. One stylesheet, no JavaScript, no init call,
no build step. You add one attribute to markup that already exists.

This file is for agents writing code that *uses* Dolly. Read it before
generating markup.

## Install

```sh
npm i @dollyjs/core
```

```css
@import "@dollyjs/core";
```

Or without a build step:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@dollyjs/core@0/src/dolly.css">
```

Nothing else runs. There is no JS entry point and no function to call. If you
find yourself writing `import ... from '@dollyjs/core'`, stop — it is a
stylesheet.

## The whole API

```html
<h2 data-dolly="tilt-up">Arrives as you reach it</h2>
```

That is a complete, working use. Everything below is refinement.

Three attributes and a set of custom properties:

| Attribute | Values | Purpose |
| --- | --- | --- |
| `data-dolly` | one of the 34 move names | what the element does |
| `data-dolly-on` | `scene`, `page` | which timeline drives it (default: the element's own trip across the viewport) |
| `data-dolly-ease` | `linear`, `out`, `in-out`, `out-expo`, `out-back` | easing preset |

Structural attributes: `data-dolly-scene`, `data-dolly-pin`, `data-dolly-space`,
`data-dolly-stagger`, `data-dolly-depth`.

## Choosing a move

Do not enumerate all 34 to the user. Pick one.

**Something should appear as the reader reaches it** — this is the common case,
and any of these is correct. Default to `fade` or `tilt-up` unless the user
asked for something with more character.

| Want | Use |
| --- | --- |
| the safe default | `fade` |
| text or cards arriving | `tilt-up` |
| arriving from above | `tilt-down` |
| lateral entry | `pan-left`, `pan-right` |
| a photo settling in | `dolly-in`, `dolly-out` |
| the big arrival, a hero | `crane` |
| coming into focus | `rack` |
| fast lateral with blur | `whip` |
| a wipe rather than a fade | `reveal` (left→right), `wipe-up` (bottom→up) |
| a slight tilt to level | `roll` |

**Something should keep moving the whole time it is on screen**

| Want | Use |
| --- | --- |
| a reading-progress bar | `progress` |
| a marker riding the page | `travel` |
| background drifting against scroll | `parallax` |
| slow Ken Burns push on a photo | `zoom` |

**Something should enter, be read, then leave** — these are for pinned scenes.

`beat` (rises in, holds, leaves), `beat-in` (out of blur and scale), `hold`
(arrives and stays).

**Cinematic**

`iris` (circular aperture opening), `track` (vertical scroll drives horizontal
travel — put a too-wide row in a pinned scene), `mask` (picture inside
letterforms), `letter` (letter-spacing tightening).

**Depth** — real Z translation under a perspective, not scale. Requires
`data-dolly-space` on an ancestor.

`push`, `pull` (camera toward / away), `swing` (rotates in on Y), `tumble`
(pitches in on X), `fly` (travels from far past the camera), `drop` (falls
through the frame), `pass` (tracks laterally, reversing yaw).

**Data and drawing**

`sequence` (sprite-sheet scrubbing), `draw` (a stroke drawing itself),
`count` (a number counting up).

## Timelines

Every move defaults to `view()` — progress is the element's own trip across the
viewport. Two opt-ins:

- `data-dolly-on="page"` — runs from the top of the document to the bottom.
- `data-dolly-on="scene"` — reads the enclosing `data-dolly-scene` timeline.

Range phases differ by timeline. On the default and on `scene`, use `entry`,
`exit`, `cover`, `contain` with percentages. On `page` the only meaningful
range is `normal` (the full scroller) — an `entry`/`cover` range copied from an
entrance means nothing there and will not do what it looks like it does.

`progress` and `travel` always read the page scroller and ignore
`data-dolly-on`.

## Pinned scenes

A scene is a tall track that pins its child and scrubs moves through it. This
is what other libraries need JavaScript for; here it is `position: sticky` plus
a named view timeline.

```html
<div data-dolly-scene style="--dolly-scene: 300vh">
  <div data-dolly-pin>
    <img data-dolly="zoom" data-dolly-on="scene" src="shot.jpg" alt="">
  </div>
</div>
```

Children must opt in with `data-dolly-on="scene"`, so an ordinary entrance
inside a scene still behaves like an entrance.

Sequence several beats through one scene by giving each its own range:

```html
<div data-dolly-scene>
  <div data-dolly-pin>
    <p data-dolly="beat" data-dolly-on="scene" style="--dolly-range: contain 0% contain 33%">First</p>
    <p data-dolly="beat" data-dolly-on="scene" style="--dolly-range: contain 33% contain 66%">Second</p>
    <p data-dolly="beat" data-dolly-on="scene" style="--dolly-range: contain 66% contain 100%">Third</p>
  </div>
</div>
```

## Stagger

A row of cards all cross `entry 0%` together and fire as one block. Offset them
along the same timeline:

```html
<div data-dolly-stagger style="--dolly-step: 6%">
  <article data-dolly="tilt-up">…</article>
  <article data-dolly="tilt-up">…</article>
  <article data-dolly="tilt-up">…</article>
</div>
```

`data-dolly-stagger="center"` cascades outward from the middle; `"edges"` lands
the outermost pair last. Offsets are defined for the first eight children;
beyond that they share the last step.

## Knobs

Set as inline styles or in your own CSS.

| Knob | Applies to | Default |
| --- | --- | --- |
| `--dolly-range` | any move | the move's own range |
| `--dolly-ease` | any move | `cubic-bezier(.22,1,.36,1)` |
| `--dolly-scene` | `data-dolly-scene` | `300vh` |
| `--dolly-depth` | `parallax` | `4rem` |
| `--dolly-zoom` | `zoom` | `1.12` |
| `--dolly-track-from` / `--dolly-track-to` | `track` | `0` / `-60%` |
| `--dolly-mask-from` / `--dolly-mask-to` | `mask` | `150%` / `210%` |
| `--dolly-letter-from` / `--dolly-letter-to` | `letter` | `.12em` / `-.05em` |
| `--dolly-cols` / `--dolly-rows` | `sequence` | `6` / `1` |
| `--dolly-count-from` / `--dolly-count-to` | `count` | `0` / `100` |
| `--dolly-perspective`, `--dolly-vanish`, `--dolly-z-from`, `--dolly-z-to`, `--dolly-angle` | depth moves | — |

In Tailwind, set these as arbitrary properties — underscores become spaces:

```html
<img data-dolly="zoom" class="[--dolly-range:contain_0%_contain_60%] [--dolly-zoom:1.2]">
```

There is no Tailwind plugin and none is needed.

## Rules

1. **Never add a `data-dolly` attribute to an element you also hide in CSS.**
   The keyframes own the hidden state. If you write `opacity: 0` on the element
   and the browser lacks scroll timelines, it stays invisible forever — the one
   failure this library is built to prevent.

2. **`draw` needs `pathLength="1"`** on the `<path>`. It has no CSS equivalent.
   Without it the path renders dashed rather than drawn. Never put
   `vector-effect="non-scaling-stroke"` on a path you are drawing — it computes
   the dash pattern in screen space and the stroke comes apart.

3. **`count` needs an accessible name.** It renders through `counter()` in
   `::after`, and generated content is decorative to assistive tech. Use
   `role="img"` with `aria-label`. CSS counters have no digit grouping, so 1380
   prints as `1380`.

4. **`sequence` sheets must be a grid, not a single row.** The sheet renders at
   `cols ×` the element width; an animated background tens of element-widths
   across silently stops rasterising and paints nothing. Keep `--dolly-cols` in
   single digits and add rows.

5. **A parent with `overflow: hidden` becomes its own scroll container** and
   pins the move at its end state. Use `overflow: clip`.

6. **`letter` changes the text's width**, so a wrapping line reflows mid-scrub.
   Put it on a `white-space: nowrap` line sized to fit at its widest tracking.

7. **Do not use `loading="lazy"` on a depth layer.** It is off-screen at load
   by construction and may never fetch.

8. **Set a scene's height with `--dolly-scene`, not `height`.** The scene needs
   its own min-height to have scroll to spend.

9. **Match the range to the layout.** The default `entry 0% cover 35%` suits a
   section that owns the screen. In a dense grid the reader scans the middle,
   and an element's centre crosses the viewport's centre at exactly
   `cover 50%` — so use `--dolly-range: cover 30% cover 70%` there and the
   move is half-played at eye level. Never apply a `cover` range to `progress`
   or `travel`.

## What it cannot do

Do not generate these; reach for JavaScript instead, and say so.

- **No per-letter or per-word splitting.** CSS has no text-node access.
- **No callbacks.** Scroll-driven animations fire no `animationstart` or
  `animationend` — zero events, verified across a full sweep. For lazy-init or
  analytics on arrival, use an `IntersectionObserver` and keep Dolly for the
  motion.
- **No formatted counters.** `42,350` with a separator is string work.
- **No looping.** Scroll position is the clock; there is nothing to loop.

## Degradation

Unsupported browsers render the page complete and unanimated. That is the
design, not a gap: `animation-fill-mode: both` with no timeline resolves every
move to its end state immediately, and the end state is the element as
authored. The same holds for a typo in a move name.

`prefers-reduced-motion: reduce` and printing disable every move.

Support: Chrome/Edge 115+, Safari 26+, Opera 101+. Firefox lands in 159.

---

Full documentation: [README](README.md) · Live demo: <https://usedolly.dev>
