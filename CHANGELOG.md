# Changelog

All notable changes to `@dollyjs/core`. Dates are release dates; the library
follows [semantic versioning](https://semver.org).

## 0.4.1 — unreleased

### Fixed

- `reveal` and `wipe-up` swapped from hidden to visible halfway through their
  range instead of wiping, in every browser and every release so far. Their
  keyframes left the far end implicit, the element's own `clip-path: none`,
  which does not interpolate with `inset()`. They now get `clip-path: inset(0)`,
  which clips nothing. The same applies to the `reveal` and `wipe-up` exits.

## 0.4.0 — 2026-10-30

### Added

- `data-dolly-exit`: the other half of an entrance. An element keeps going as
  it scrolls off the top of the viewport — `tilt-up` keeps rising, `pan-left`
  keeps moving left — and sits exactly as authored until then. 13 exits:
  `fade`, `tilt-up`, `tilt-down`, `pan-left`, `pan-right`, `dolly-in`,
  `dolly-out`, `crane`, `roll`, `reveal`, `wipe-up`, `rack`, `whip`. Off under
  reduced motion, in print, and in browsers without scroll timelines, like
  every move. Nothing existing changed: every line of 0.3.2 is still in the
  file.

### Changed

- The CDN snippets now point at `src/dolly.css`, the file npm ships, rather
  than jsDelivr's generated `dolly.min.css`.

### Fixed

- The docs gave the `--dolly-ease` default as a bezier; it is `linear`.
- The docs described a `data-dolly-range` attribute that nothing reads.
  `--dolly-range` on its own is the knob.

## 0.3.2 — 2026-10-24

### Fixed

- In browsers without scroll timelines (Firefox, Safari before 26), pinned
  scenes no longer leave several screens of tall, static track to scroll
  through. `[data-dolly-scene]` drops its height and `[data-dolly-pin]`
  stops sticking, so the scene scrolls like normal content. The same applies
  under `prefers-reduced-motion` and in print, replacing a reduced-motion
  `overflow` rule that had no effect.

## 0.3.1 — 2026-10-24

### Fixed

- In browsers without scroll timelines (Firefox), `beat`, `beat-in`, `iris`,
  `letter`, `mask`, `sequence` and `track` stayed on their last keyframe
  instead of switching off, which could leave content at opacity 0. The
  no-timeline block now uses `!important`, like the reduced-motion block.

### Changed

- Rewrote the README and package description in plainer language, and
  corrected the size comparison table: Dolly is 2.3 kB of CSS, minified and
  gzipped.
- The CDN link in the docs now points at `dolly.min.css`.

## 0.3.0 — 2026-09-18

### Added

- **`sequence`** — steps a sprite sheet, one cell per slice of scroll: the
  frame-scrubbing effect that otherwise needs canvas and a decode loop. The
  sheet is a grid, driven by `--dolly-cols` and `--dolly-rows`.
- **`draw`** — animates `stroke-dashoffset` along an SVG path, so a stroke
  draws itself. The path must carry `pathLength="1"`.
- **`count`** — a scroll-driven number, printed with `counter()`. Knobs:
  `--dolly-count-from`, `--dolly-count-to`.
- **`data-dolly-on="page"`** — binds any move to the document scroller
  instead of its own trip across the viewport. `progress` and `travel`
  already read the page and ignore it.

### Notes for authors

- A sprite sheet must be a **grid**, not a single row. The sheet is rendered
  at `cols ×` the element's width, and an animated background that wide stops
  rasterising and paints nothing — silently, with no fallback, and
  inconsistently enough to look fine on the machine that built it. Keep
  `--dolly-cols` in single digits and put the frames in rows.
- `draw` needs a **centreline** path: one open stroke with `fill="none"`.
  Text converted to outlines traces the rim of each letter instead of writing
  it. Never combine it with `vector-effect="non-scaling-stroke"`, which moves
  the dash calculation into screen space where `pathLength` means nothing and
  the stroke comes apart.
- `count` renders through generated content, so it has no digit grouping and
  is decorative to assistive tech. Give the element an accessible name.

## 0.2.0 — 2026-09-16

First published release: 31 scroll-driven camera moves, pinned scenes via
sticky positioning and named view timelines, beat moves for staged copy,
depth moves built on independent transform properties, sibling stagger and
named easings — with the guarantee that no move can leave content hidden in a
browser without scroll timelines.
