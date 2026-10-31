# Dolly

Scroll animations in plain CSS: 34 camera moves and 13 exits, each set with one
attribute, and no JavaScript.

```html
<h2 data-dolly="tilt-up">This rises into place as you scroll to it.</h2>
```

That attribute is the whole API. You don't call or wrap anything, and the
browser runs the animation itself.

Named for the camera dolly, the cart that carries a camera through a shot.
Sibling to [Foley](https://usefoley.dev) ([repo](https://github.com/eakbulut/foley)),
which does the same for UI sound and synthesizes every sound live.

It also fails safely. Most scroll libraries hide content with a CSS rule and
reveal it with JavaScript, so if the script fails or the browser can't run it,
the content stays hidden. Dolly only hides content inside `@keyframes`. A
browser without scroll timelines shows the whole page and skips the motion.

- [usedolly.dev](https://usedolly.dev/) — the demo site
- [usedolly.dev/moves.html](https://usedolly.dev/moves.html) — all 34 moves and 13 exits, playing as you scroll
- [`agents.md`](./agents.md) — point your coding agent at it
- MIT, zero dependencies, zero JavaScript

## Install

```sh
npm i @dollyjs/core
```

```css
@import "@dollyjs/core";
```

Or link the file directly:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@dollyjs/core@0/src/dolly.min.css">
```

It works next to Tailwind, plain CSS or any framework, and only touches
elements with a `data-dolly` attribute.

Tailwind needs no plugin. Every `--dolly-*` is a custom property, so Tailwind's
arbitrary properties set them straight from the class attribute — underscores
become spaces:

```html
<h2 data-dolly="tilt-up" class="[--dolly-range:entry_0%_cover_40%]">Arrives early</h2>
<img data-dolly="zoom" class="[--dolly-zoom:1.2]" src="shot.jpg" alt="">
```

## Usage

Add the attribute to markup you already have:

```html
<section data-dolly="fade">…</section>
<img data-dolly="dolly-in" src="…" alt="…">
<div data-dolly="progress"></div>
```

Entrance moves run on a view timeline over `entry 0% cover 35%` — they scrub
with the scroll as the element comes up the viewport, and are finished by the
time it is comfortably on screen. An unknown value animates nothing and leaves
the element exactly as authored.

## Moves

Entrances. These resolve as the element enters the viewport.

| Move | What it does |
| --- | --- |
| `fade` | Fades up from nothing. |
| `tilt-up` | Rises 2.5rem into place. |
| `tilt-down` | Drops 2.5rem into place. |
| `pan-left` | Enters from the right, travelling left. |
| `pan-right` | Enters from the left, travelling right. |
| `dolly-in` | Pushes in from 0.9 scale. |
| `dolly-out` | Settles back from 1.1 scale. |
| `crane` | Rises 5rem with a slight scale. The big arrival. |
| `rack` | Rack focus: a 14px blur clearing. |
| `whip` | Whip pan: lateral travel plus blur. |
| `reveal` | Clip wipe, left edge to right. |
| `wipe-up` | Clip wipe, bottom edge upward. |
| `roll` | Rotates -5deg to level. |

Continuous. These run the whole time the element is on screen, or the whole
length of the page, rather than resolving once on entry.

| Move | What it does |
| --- | --- |
| `progress` | Scales a bar from 0 to 1 across the document's scroll. |
| `travel` | Rides the document's scroll — a marker moving along its own track. |
| `parallax` | Drifts vertically against the scroll by `--dolly-depth`. |
| `zoom` | Ken Burns: a slow push to `--dolly-zoom`. |

Beats. Enter, hold long enough to read, leave. Intended for pinned scenes —
see below.

| Move | What it does |
| --- | --- |
| `beat` | Rises in, holds, leaves upward. |
| `beat-in` | Arrives out of blur and scale, holds, leaves. |
| `hold` | Arrives and stays. |

Cinematic. Effects that usually need a JavaScript library.

| Move | What it does |
| --- | --- |
| `iris` | The aperture opening: a circle clip growing from nothing. |
| `track` | Vertical scroll driving horizontal travel. Put a too-wide row in a pinned scene. |
| `mask` | Pushes a background picture inside letterforms. The element supplies its own `background-image` and `background-clip: text`. |
| `letter` | Letter-spacing tightens from loose to tight while fading in. |

### Frame sequences

Steps through a frame sequence as you scroll, using one sprite sheet. This is
usually done with canvas.

| Move | What it does |
| --- | --- |
| `sequence` | Steps through a sprite sheet, one cell per slice of scroll. |

```html
<div data-dolly="sequence"
     style="--dolly-cols: 8; --dolly-rows: 4;
            background-image: url(sheet.png)"></div>
```

The sheet is a **grid**, read left to right, top to bottom. Everything is
percentage-based, so there is no cell size to hardcode and nothing breaks at
2x, 3x or a fractional element width.

**Use a grid, not a single row.** The sheet is rendered at `cols ×` the
element's width, so a one-row sheet of thirty-two cells is drawn thirty-two
element-widths across. An *animated* background that wide stops rasterising
and paints **nothing** — no error, no fallback, and inconsistently enough that
it can look fine on the machine that built it. Eight columns draws eight
element-widths instead. Keep `--dolly-cols` in single digits and put the
frames in rows.

Pick the format by what the cells contain. Flat or synthetic art palettises
extremely well: this site's own leader is forty-eight cells at 384px — a
4608×1536 sheet — and weighs 187 kB as a 64-colour PNG. For photographic
sequences the choice flips to WebP, which additionally caps any dimension at
16383px. PNG has no such limit.

It is one of the moves that repaints (see [Performance](#performance)), but
it only repaints once per cell across the whole scroll, not once a frame.

Knobs: `--dolly-cols` (default 6), `--dolly-rows` (default 1). `--dolly-ease`
does not apply: stepping is the move, and an eased sheet reads as a stutter.


### Drawing and counting

| Move | What it does |
| --- | --- |
| `draw` | A stroke draws itself along its own path. |
| `count` | A number counts up (or down) as it scrolls into place. |

```html
<svg viewBox="0 0 420 160" fill="none">
  <path data-dolly="draw" pathLength="1" d="…" stroke="currentColor"/>
</svg>

<span data-dolly="count" role="img" aria-label="1,380"
      style="--dolly-count-to: 1380"></span>
```

`draw` needs `pathLength="1"` on the path. That normalises any path to a length
of 1 so a single dash covers it exactly, and it is an SVG attribute with no CSS
equivalent — the one move in this library that needs a second authoring step.
Leave it off and the path renders dashed rather than drawn: wrong, but never
invisible. With `stroke-linecap: round` the dashes overlap into a solid line, so
the mistake can hide; check it with `butt` caps.

`count` renders through `counter()` in `::after`, which has two consequences
worth knowing before you use it. There is no digit grouping in CSS counters, so
1380 prints as `1380`. And generated content is decorative to assistive tech, so
give the element an accessible name — `role="img"` plus `aria-label` is the
shortest thing that works.

Knobs: `--dolly-count-from` (default 0), `--dolly-count-to` (default 100).

### Depth

A dolly move is physically a move through Z. These use `translateZ` under a
perspective rather than `scale`, so layered children separate at different
rates and the frame edges distort the way a lens does. Put `data-dolly-space`
on the ancestor that should hold the camera.

| Move | What it does |
| --- | --- |
| `push` | the camera travels toward it |
| `pull` | the camera draws back from it |
| `swing` | rotates in from the side on Y |
| `tumble` | pitches in from above on X |
| `fly` | travels from far past the camera, fading before it crosses the plane |
| `drop` | falls through the frame, pitching as it goes |
| `pass` | tracks laterally and reverses its yaw as it crosses, the way a shop window does as you walk past |

```html
<div data-dolly-space style="--dolly-perspective: 1400px">
  <img data-dolly="fly" style="--dolly-z-from: -2400px" src="…" alt="">
  <img data-dolly="fly" style="--dolly-z-from: -1400px" src="…" alt="">
</div>
```

Knobs: `--dolly-perspective`, `--dolly-vanish`, `--dolly-z-from`, `--dolly-z-to`,
`--dolly-angle`.

## Exits

Every move above plays as the element arrives. An exit plays as it leaves:
the element sits exactly where your layout put it until its top reaches the
top of the viewport, then keeps going the way it came in. A `tilt-up` exit
keeps rising; a `pan-left` exit keeps moving left.

```html
<header data-dolly-exit="tilt-up">…</header>
```

| Exit | What it does |
| --- | --- |
| `fade` | Fades out. |
| `tilt-up` | Keeps rising 2.5rem as it goes. |
| `tilt-down` | Keeps sinking 2.5rem as it goes. |
| `pan-left` | Keeps travelling left. |
| `pan-right` | Keeps travelling right. |
| `dolly-in` | The camera pushes past it, to 1.1 scale. |
| `dolly-out` | The camera pulls away, to 0.9 scale. |
| `crane` | Keeps craning up 5rem. |
| `roll` | Keeps rolling, to 5deg. |
| `reveal` | Clip wipe off to the right. |
| `wipe-up` | Clip wipe off the top. |
| `rack` | Focus pulls away into a 14px blur. |
| `whip` | Whips out to the left, with blur. |

To arrive with one move and leave with another, nest two elements. Their
transforms combine:

```html
<section data-dolly-exit="dolly-in">
  <h2 data-dolly="tilt-up">Enters rising, leaves past the camera.</h2>
</section>
```

Rules worth knowing:

- **One attribute per element.** `data-dolly` and `data-dolly-exit` on the
  same element is not supported; nest instead.
- **Exit offsets only.** A custom `--dolly-range` on an exit uses `exit`
  values, such as `exit 0% exit 45%`. An `entry` or `cover` range copied off
  an entrance fades the element out while it arrives.
- **Not in the last screen of the page.** An element there never scrolls far
  enough to finish leaving, so it stays half-faded.
- **Not taller than the viewport.** A tall element starts its exit while its
  bottom is still being read.
- **`overflow: clip`, never `hidden`, on the container.** `pan-*`, `dolly-in`,
  `crane` and `whip` carry the element past its box; `hidden` would make the
  container its own scroller and stop the exit playing.
- **Not yet:** exits ignore `data-dolly-on`, `data-dolly-stagger` and scenes.

Like every move, an exit renders the element exactly as authored under
reduced motion, in print, and in browsers without scroll timelines.

## Pinned scenes

Pinning is where most scroll libraries need JavaScript: an element sticks to
the viewport while scrolling plays an animation on it. Here it is
`position: sticky` plus a named view timeline.

```html
<div data-dolly-scene>
  <div data-dolly-pin>
    <div data-dolly="zoom" data-dolly-on="scene">…</div>
  </div>
</div>
```

- `data-dolly-scene` — the tall track that owns the timeline. Height is
  `--dolly-scene`, default `300vh`.
- `data-dolly-pin` — sticks to the viewport for the track's length.
- `data-dolly-on="scene"` — opt an element into the scene's timeline over
  `contain 0% contain 100%`, the exact span the track is pinned. Without it, a
  move inside a scene still behaves like an ordinary entrance, which is
  usually what you want for anything that isn't part of the sequence.

In a browser without scroll timelines, or with reduced motion on, nothing
scrubs, so scenes stop pinning and collapse to their content height. Without
that, a pin would hold one still frame for several screens of scrolling, and
on a phone the page looks like it won't scroll.

### Staging beats

Give each beat its own slice of the scene with `--dolly-range`, and they play
in sequence instead of all at once:

```html
<div data-dolly-scene style="--dolly-scene: 400vh">
  <div data-dolly-pin>
    <p data-dolly="beat" data-dolly-on="scene"
       style="--dolly-range: contain 0% contain 34%">First.</p>
    <p data-dolly="beat" data-dolly-on="scene"
       style="--dolly-range: contain 30% contain 64%">Then this.</p>
    <p data-dolly="hold" data-dolly-on="scene"
       style="--dolly-range: contain 60% contain 96%">And it stays.</p>
  </div>
</div>
```

Overlap the ranges slightly so one beat leaves as the next arrives.

## Riding the page

Every move defaults to `view()`: progress is the element's own trip across the
viewport. `data-dolly-on="page"` swaps that for the page scroller, so a move
runs from the top of the document to the bottom instead.

```html
<svg class="ribbon" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
  <path data-dolly="draw" data-dolly-on="page" pathLength="1" d="…"
        stroke="currentColor" fill="none" stroke-linecap="round"/>
</svg>
```

A ribbon like this can write a word in cursive as the reader scrolls from the
top of the page to the bottom: one unbroken stroke, never lifted, which is
what `draw` is for. A font would not work here: glyphs are filled outlines,
not strokes, so they have no path to draw along.

The artwork has to be a **centerline**: one open path, `fill="none"`, drawn in
writing order, with the weight coming from `stroke-width`.
`assets/dolly-word.svg` is an example. Text converted to outlines gives the
*contour* of each letter, so drawing it traces the rim instead of writing the
word — and that cannot be fixed downstream.

**Do not put `vector-effect="non-scaling-stroke"` on a path you are drawing.**
It makes the browser compute the dash pattern in screen space, which fights
`pathLength="1"`, and the stroke comes apart into disconnected pieces instead
of advancing as one line. It looks like a geometry bug and it is not. If the
stroke needs to keep a constant width, scale the SVG uniformly instead.

`normal` is the default range here and means the full length of the scroller.
`entry`, `exit`, `cover` and `contain` are view-timeline phases and mean
nothing on this timeline, so a `--dolly-range` copied off an entrance will not
do what it looks like it does.

`progress` and `travel` already read the page scroller and ignore this
attribute; they have nowhere else to read from.

## Knobs

Set these as inline styles or in your own CSS. `data-dolly-ease` is an
attribute you add; the rest are plain custom properties.

| Knob | Applies to | Default |
| --- | --- | --- |
| `--dolly-range` | any move or exit | the move's own range |
| `data-dolly-ease` + `--dolly-ease` | any move or exit | `linear` |
| `--dolly-scene` | `data-dolly-scene` | `300vh` |
| `--dolly-depth` | `parallax` | `4rem` |
| `--dolly-zoom` | `zoom` | `1.12` |
| `--dolly-track-from` / `--dolly-track-to` | `track` | `0` / `-60%` |
| `--dolly-mask-from` / `--dolly-mask-to` | `mask` | `150%` / `210%` |
| `--dolly-letter-from` / `--dolly-letter-to` | `letter` | `.12em` / `-.05em` |

Ranges use the standard `animation-range` syntax: `entry`, `exit`, `cover`,
`contain`, with percentages.

## Performance

Browsers can run animations of `transform` and `opacity` on the GPU, where
they stay smooth even when the page is busy. Animating any other property
makes the browser repaint on the main thread every frame, and on a phone that
is where scroll animation starts to stutter.

23 of the 34 moves, and 9 of the 13 exits, only use transform and opacity.
These repaint:

| Move | Animates |
| --- | --- |
| `rack`, `whip`, `beat-in`, and the `rack` and `whip` exits | `filter: blur()` |
| `reveal`, `wipe-up`, `iris`, and the `reveal` and `wipe-up` exits | `clip-path` |
| `mask` | `background-size` |
| `sequence` | `background-position`, once per cell |
| `letter` | `letter-spacing`, which also reflows the line |
| `draw` | `stroke-dashoffset` |
| `count` | a registered custom property, printed by `counter()` |

Use them on a few elements at a time rather than every card in a grid, and
check them on a real phone. The [moves page](https://usedolly.dev/moves.html)
tags each one.

## Browser support

`animation-timeline` is supported in Chrome and Edge 115+, Safari 26+,
Firefox 159+, and Opera 101+.

There is no polyfill, and there won't be one. Unsupported browsers get the page
with all its content, unanimated. With no timeline, `animation-fill-mode: both`
resolves every move to its end state immediately, and the end state is the
element as you wrote it.

The same holds for an unknown attribute value, a typo, or a partially loaded
stylesheet.

## Reduced motion

`prefers-reduced-motion: reduce` disables every move. Content renders as you
wrote it, since Dolly never hid it in the first place.

## Where this sits

`usal` was built because AOS and sal "don't handle text splitting well" — its
author's words. Word-by-word and letter-by-letter animation needs `<span>`s
inserted into a text node, which CSS cannot do at all. So that is genuinely
their territory, not a gap to close: if you need text splitting or number
counters, use usal.

The same thread opened with *"9kb is too much for scroll animation"*, and the
author agreed, pointing simple cases at sal.js. For a fade, a reveal, a
parallax or a pinned scrub, Dolly does the job without running any code.

How the alternatives compare, checked against their published packages.
Sizes are minified and gzipped.

| | ships | hides content first | reduced motion | maintained |
| --- | --- | --- | --- | --- |
| AOS | 4.7 kB JS | yes | no | last published 2022 |
| ScrollReveal | 5.6 kB JS | yes, via `html.sr` | no | last published 2021 |
| sal.js | 1.8 kB JS + CSS | yes | no | last published 2021 |
| usal | 7.5 kB JS | **no** | **no** | active |
| Motion | 43.8 kB (React) | yes, in SSR HTML | yes | active |
| Dolly | 2.3 kB CSS | no | yes | — |

Two of those deserve credit: usal never pre-hides, and ScrollReveal's
`html.sr` scoping is the least-bad version of hiding. Motion is a different
purchase — a whole animation runtime — and on its fast path it hands
scroll-linked work to the same `ViewTimeline` this library is built on.

## What it cannot do

Each of these was tested, not assumed:

- **No text splitting.** `split-letter` / `split-word` effects need `<span>`s
  inserted into a text node. CSS has no text-node access, so per-letter
  animation is out.
- **No callbacks.** Scroll-driven animations fire no `animationstart` or
  `animationend` — measured across a full scroll sweep in Chrome, forward and
  back: zero events. If you need to lazy-init a map or fire analytics when a
  section arrives, use an IntersectionObserver for that and keep Dolly for
  the motion.
- **No number counters with formatting.** `@property` can animate an integer
  and `counter()` can print it, but preserving `42,350` is string work.
- **No looping.** Scroll position is the clock; there is nothing to loop.

## Stagger

A row of cards all cross `entry 0%` at the same instant and fire as one block.
Offset each child along the same timeline instead:

```html
<div class="grid" data-dolly-stagger style="--dolly-step: 6%">
  <article data-dolly="tilt-up">…</article>
  <article data-dolly="tilt-up">…</article>
  <article data-dolly="tilt-up">…</article>
</div>
```

`data-dolly-stagger="center"` cascades outward from the middle;
`"edges"` lands the outermost pair last. `--dolly-step` sets the spacing.

## Gotchas

### `scroll-padding` shifts every range

View timelines treat the scroller's `scroll-padding` as an inset. With
`scroll-padding-top: 64px` on `html`, every range starts 64px early: an exit
on a hero at the top of the page is already 8% gone before anyone scrolls.
Leave `scroll-padding` off the scroller, or account for it in `--dolly-range`.

### `letter` reflows unless the line cannot wrap

It animates `letter-spacing`, which changes the text's width. On a line that
can wrap, the line count changes mid-scrub and the layout jumps. Give it
`white-space: nowrap` and size the type to fit at the widest tracking value.

### A dense grid needs a later range

The default, `entry 0% cover 35%`, is tuned for a page where one section owns
the screen: it finishes while the element is still low, which is right when
the reader is scrolling toward it. In a tightly packed grid the reader scans
the middle of the screen instead, and a move that ends at `cover 35%` has been
static for a third of a screen by the time their eye arrives.

An element's centre crosses the viewport's centre at exactly `cover 50%`, so
centre the range there and the move is half-played at eye level:

```css
.card [data-dolly] { --dolly-range: cover 30% cover 70% }
```

This page's own [moves reference](https://usedolly.dev/moves.html) does that.
Leave `progress` and `travel` out of any such rule — they read the page
scroller, where `cover` means nothing.

### `loading="lazy"` does not work on a depth layer

A plate pushed back on Z inside a clipped container is, as far as the
browser's lazy-load heuristic is concerned, off-screen — it cannot know a
scroll-driven transform is about to bring it forward. The image never starts
loading and the layer flies past empty. Use `decoding="async"` and
`fetchpriority="low"` instead; they reduce the cost without gating the fetch
on visibility.


**An ancestor with `overflow: hidden` breaks view timelines.** It makes that
element a scroll container, and children measured against it sit at progress 1
forever — so they look pinned in their end state and never animate. Use
`overflow: clip` instead. It clips identically and creates no scrollport. This
is the single most common way a Dolly move "stops working", and it is why
`data-dolly-pin` uses `clip`.

**The `animation` shorthand resets `animation-timeline`.** Writing
`animation: 2s ease-in` anywhere that also carries a `data-dolly` move sets the
timeline back to `auto`, silently converting a scroll-driven animation into a
time-driven one that fires once on load. Use the longhands — `animation-name`,
`animation-duration`, `animation-timing-function`. Dolly itself never uses the
shorthand, and the test suite enforces that.

## Contributing

`npm test` is the spec. The suite derives its expectations from `src/dolly.css`
rather than from a hardcoded list, so a new move must appear in this README's
table or the tests fail.

## License

MIT.

---

Named for the camera dolly. Dedicated to Dolly Parton (1946–2026), who founded
[the Imagination Library](https://imaginationlibrary.com/).
