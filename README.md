# Dolly

Scroll-driven motion, in CSS. One attribute, 30 camera moves, no JavaScript.

```html
<h2 data-dolly="tilt-up">This rises into place as you scroll to it.</h2>
```

That is the whole API. No init call, no observer, no wrapper component, no
runtime. The stylesheet is the product.

The other half of the pitch is the failure mode. Every mainstream scroll
library hides content in a base rule and reveals it from script; when the
script fails or the browser can't help, the content is simply gone. Dolly
keeps the hidden state inside `@keyframes` only, so a browser without scroll
timelines renders the page complete and just doesn't animate.

- [usedolly.dev](https://usedolly.dev/) — the demo is the documentation
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
<link rel="stylesheet" href="https://unpkg.com/@dollyjs/core/src/dolly.css">
```

Nothing else runs. Drop it beside Tailwind, vanilla CSS, or any framework —
it only touches elements carrying a `data-dolly` attribute.

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
| `parallax` | Drifts vertically against the scroll by `--dolly-depth`. |
| `zoom` | Ken Burns: a slow push to `--dolly-zoom`. |

Beats. Enter, hold long enough to read, leave. Intended for pinned scenes —
see below.

| Move | What it does |
| --- | --- |
| `beat` | Rises in, holds, leaves upward. |
| `beat-in` | Arrives out of blur and scale, holds, leaves. |
| `hold` | Arrives and stays. |

The cinematic three, plus one.

| Move | What it does |
| --- | --- |
| `iris` | The aperture opening: a circle clip growing from nothing. |
| `track` | Vertical scroll driving horizontal travel. Put a too-wide row in a pinned scene. |
| `mask` | Pushes a background picture inside letterforms. The element supplies its own `background-image` and `background-clip: text`. |
| `letter` | Letter-spacing tightens from loose to tight while fading in. |

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

## Pinned scenes

The move scroll libraries need JavaScript for: pin an element to the viewport
and let scroll scrub a transformation through it. Here it is `position: sticky`
plus a named view timeline.

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

### Staging beats

Give each beat its own slice of the scene with `--dolly-range`, and they play
in sequence instead of all at once:

```html
<div data-dolly-scene style="--dolly-scene: 400vh">
  <div data-dolly-pin>
    <p data-dolly="beat" data-dolly-on="scene" data-dolly-range
       style="--dolly-range: contain 0% contain 34%">First.</p>
    <p data-dolly="beat" data-dolly-on="scene" data-dolly-range
       style="--dolly-range: contain 30% contain 64%">Then this.</p>
    <p data-dolly="hold" data-dolly-on="scene" data-dolly-range
       style="--dolly-range: contain 60% contain 96%">And it stays.</p>
  </div>
</div>
```

Overlap the ranges slightly so one beat leaves as the next arrives.

## Knobs

Set these as inline styles or in your own CSS. `data-dolly-range` and
`data-dolly-ease` are attributes you add; the rest are plain custom properties.

| Knob | Applies to | Default |
| --- | --- | --- |
| `data-dolly-range` + `--dolly-range` | any move | the move's own range |
| `data-dolly-ease` + `--dolly-ease` | any move | `cubic-bezier(.22,1,.36,1)` |
| `--dolly-scene` | `data-dolly-scene` | `300vh` |
| `--dolly-depth` | `parallax` | `4rem` |
| `--dolly-zoom` | `zoom` | `1.12` |
| `--dolly-track-from` / `--dolly-track-to` | `track` | `0` / `-60%` |
| `--dolly-mask-from` / `--dolly-mask-to` | `mask` | `150%` / `210%` |
| `--dolly-letter-from` / `--dolly-letter-to` | `letter` | `.12em` / `-.05em` |

Ranges use the standard `animation-range` syntax: `entry`, `exit`, `cover`,
`contain`, with percentages.

## Browser support

`animation-timeline` is supported in Chrome and Edge 115+, Safari 26+, and
Opera 101+ — about 87% of global traffic. Firefox does not support it through
158; it lands in 159.

There is no shim, and there will not be one. Unsupported browsers get the page
with all its content, unanimated. That is the design, not a gap:
`animation-fill-mode: both` with no timeline resolves every move to its end
state immediately, and the end state is the element as you authored it. The
failure mode is "didn't animate", never "didn't appear".

The same holds for an unknown attribute value, a typo, or a partially loaded
stylesheet.

## Reduced motion

`prefers-reduced-motion: reduce` disables every move. Content renders exactly
as authored, because the authored state was never the hidden one — there is
nothing to un-hide.

## Gotchas

### `letter` reflows unless the line cannot wrap

It animates `letter-spacing`, which changes the text's width. On a line that
can wrap, the line count changes mid-scrub and the layout jumps. Give it
`white-space: nowrap` and size the type to fit at the widest tracking value.

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
table or the tests fail. That is deliberate.

## License

MIT.

---

Named for the camera dolly, and for Dolly Parton (1946–2026), who funded
[the Imagination Library](https://imaginationlibrary.com/).
