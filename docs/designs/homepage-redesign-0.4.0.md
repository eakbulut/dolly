# Dolly 0.4.0 and the homepage redesign

*   **Author:** eakbulut
*   **Status:** Proposed (revised after review, see `../../consolidated_review_report.md`)
*   **Date:** 2026-10-30

--------------------------------------------------------------------------------

## Overview

Dolly is a CSS-only scroll-animation library (`@dollyjs/core`). Its homepage, `index.html` on usedolly.dev, is where developers decide whether to install it. This document covers three pieces of work. Each has a short code that the rest of the document uses:

1.  **L: Library 0.4.0.** A new attribute, `data-dolly-exit="<move>"`, makes an element keep moving out of the viewport as it scrolls off the top. An exit `tilt-up` keeps rising and an exit `pan-left` leaves to the left. Every change to `src/dolly.css` is a pure addition, so existing moves, keyframes and default ranges don't change. It is released to npm before the homepage uses it, because the homepage's copy-paste snippets point at the jsDelivr `@0` build.
2.  **P0–P1: Performance fixes on the current homepage.** P0 records baseline traces. P1 removes the pinned scenes and the effects that make phones drop frames. P1 ships before the redesign, so the complaints stop while the redesign is built.
3.  **P2–P5: Homepage redesign.** A new `index.html` for developers deciding whether to install. The look comes from framing, type and camera-like motion, with no film props: no grain, no countdown leaders. P2 is the static page, P3 the motion, P4 the repaint moves and P5 the `moves.html` restyle. `moves.html` takes the new type and colours but keeps its layout.

All three are in one document so the order and the dependencies between them sit in one place. The library section is self-contained, so that the redesign can't hold up the release. Once L is approved, 0.4.0 can be built and released while the redesign sections are still in review.

Terms used throughout:

*   **Fails-visible promise.** If animation can't run, every element renders fully visible where the layout puts it. That covers reduced motion, print, and browsers without scroll timelines. The hidden state lives only in `@keyframes`, never in a base rule. This is product principle 1 in `PRODUCT.md` and rule 1 in the header of `src/dolly.css`.
*   **Floor devices.** The slowest phones the homepage promises smooth scrolling on: a Pixel 7 Pro and an iPhone 14.
*   **Deadpan voice.** The site's copy voice: sentence case, dry jokes, no marketing adjectives. For example: "now go delete some JavaScript".

## The Problem

People on Reddit who visited usedolly.dev complained about performance ("Janky on my phone", "Do I need an M6 Macbook Pro for this to work?") and about scrolljacking ("scrolljacking is the absolute worst cliche in all of web UX", "It's the worst part of any website ever, scrolljacking animations.."). For an animation library, a demo that stutters reads as proof that the library stutters.

The causes, found in `index.html` at commit `3d6bfcc`:

*   **Scrolljacking.** Five pinned scenes (`data-dolly-scene`, with heights of 420, 320, 340, 460 and 360vh) total 19 screen-heights. For about 14 of them, the scrollbar moves but the content doesn't, because each scene holds its content still for its height minus one viewport.
*   **Work the GPU can't take over.** These effects force the browser to recompute styles or repaint on every scroll frame:
    *   `--bg`, `--glow` and `--grain` animated on `:root` from the page scroll (`index.html:65-80`);
    *   a fixed full-screen grain layer with `mix-blend-mode: overlay` (`index.html:84`);
    *   the masthead's `mix-blend-mode: difference` (`index.html:104`), and its scroll-percentage readout, which animates a custom property in a fixed header (`index.html:135-141`);
    *   filters on moving images (`data-dolly-depth` far, mid and near), the `.glyph` filter (`index.html:352`), and two `backdrop-filter`s (`index.html:282`, `:298`).
*   **Oversized images.** 12 `<img>` tags show only 5 distinct photos. Their `srcset` widths go up to 1200w, and their `sizes` are larger than the space they fill.

Separately, the maintainer dislikes the current look. It is meant to feel cinematic and doesn't. The page also teaches rather than sells: the install line comes after all five pinned scenes, and the 34-row reference table takes up the homepage.

The library also has a gap that the redesign exposes: no library move can animate an element *leaving* the viewport. Entrances (`tilt-up`, `fade` and the rest) have keyframes with only a `from` block, and they play from `entry 0%` to `cover 35%`. An element that is already on screen at load has finished its entrance, so scrolling does nothing to it. Continuous moves (`zoom`, `track`, `parallax` and the rest) run while the element is in view. Only `zoom` and `track` start at the authored position, so only they can move an element away from it. Neither changes opacity. A hero that hands over to the next section as the reader scrolls needs exits.

## Goals

*   **G1. No stutter on the floor devices.** Pass on both devices, using the procedure in the Verification Plan (frame-rate acceptance):
    *   **Pixel 7 Pro:** the worst of three cold-load runs has under 1% dropped plus partially presented frames, and no frame over 50 ms.
    *   **iPhone 14:** the worst of three cold-load runs has a hitch ratio under 5 ms/s.
    *   **Calibration:** the same procedure fails on today's `index.html`; otherwise the test is broken.
*   **G2. No scrolljacking on the homepage.** No pinned scene anywhere on `index.html`. The page scrolls at the reader's pace the whole way down.
*   **G3. The still page explains dolly in 10 seconds.** Before any scroll, with JavaScript off, the first screen shows all of these:
    *   the claim;
    *   one attribute snippet;
    *   the npm and CDN install lines;
    *   "no JavaScript";
    *   the fails-visible promise.

    **Check:** three developers look at the still page for 10 seconds. It passes if at least two describe dolly as a CSS scroll-animation library that needs no JavaScript.
*   **G4. The first scroll uses only library moves.** As the reader scrolls, hero layers leave with `data-dolly-exit` while the next section arrives with published library entrances. Every animated element on the homepage uses a move defined in `src/dolly.css`, and each one shows the `data-dolly` or `data-dolly-exit` value that produced it. **Check:** the still-frame screenshots in the Verification Plan.
*   **G5. Exit mode keeps the fails-visible promise.** With reduced motion, in print, and in browsers without scroll timelines, every element with `data-dolly-exit` renders fully visible where the layout puts it.
*   **G6. No existing move changes.** Every change to `src/dolly.css` in 0.4.0 is a pure addition. `git diff v0.3.2 -- src/dolly.css` shows no removed or changed lines.
*   **G7. The performance fixes ship first,** as their own deploy, before the redesign lands.
*   **G8. Contrast and copyable code.** Every text and code colour pairing passes WCAG AA. Code and attribute values stay lowercase monospace and copy exactly as shown.

## Non-Goals

*   **Removing or weakening any library move.** Blur and filter moves (`rack`, `whip`, `beat-in`, `data-dolly-depth`) stay in the library; they are only kept off the homepage.
*   **JavaScript,** in the library or on the homepage.
*   **Animation on the homepage that isn't a library move,** including time-based animation on page load.
*   **Pinned scenes on the homepage, or a separate pinned demo page.** A pinned demo can return later on its own page, traced separately.
*   **`track` on the homepage.** Its fallback gap is recorded under Future Improvements. `pan-left` and `pan-right` give sideways motion instead.
*   **Staggered exits.** Not in 0.4.0. The hero orders its few exit layers by hand.
*   **Exits combined with `data-dolly-on`, `data-dolly-stagger` or scenes.** Not supported in 0.4.0. These are documented as unsupported.
*   **One element carrying both `data-dolly` and `data-dolly-exit`.** To enter with one move and exit with another, nest two elements.
*   **Exits for the remaining moves, in 0.4.0.** There will be no exits for `beat`, `beat-in`, `fly`, `drop`, `pass`, `zoom`, `parallax`, `track`, `mask`, `letter`, `sequence`, `progress`, `travel`, `hold`, `push`, `pull`, `swing` or `tumble`, because none of them has a natural way to keep going. Exits for `iris`, `draw` and `count` are deferred (see Future Improvements).
*   **A split-flap move,** or animation one letter at a time.
*   **Restructuring the `moves.html` card grid.** It takes the new type and colours, plus a compact index at the top.
*   **A browser-automation test dependency** such as Puppeteer. Frame-rate and screenshot checks stay manual and documented.
*   **A notice telling visitors that animation has switched off.**

## Open Questions

These are checks, not decisions. Each one is answered before a named gate, and each says what happens if the answer is bad.

*   **Q1. Inactive exit timelines.** What does an element with `data-dolly-exit` show when its view timeline is inactive? Two cases: under an `overflow: hidden` ancestor, and in a horizontal scroller without `--dolly-axis: inline`.
    *   **Expected:** visible at the authored position. `src/dolly.css:341-345` records that an inactive timeline holds the animation's `from` state. A `to`-only exit's `from` state is the element as authored.
    *   **Answered by:** `test/exit-probe.html` in Chrome, Safari 26 and Firefox 159, in phase L, before tagging `v0.4.0`.
    *   **If bad:** document both cases as unsupported for exits in README and `agents.md`, and ship anyway. CSS can't detect an inactive timeline, so no library guard is possible.
*   **Q2. Hero-layer and repaint caps.** How many full-viewport hero layers, and how many repaint moves on screen together, can the floor devices carry? This also covers whether Safari 26 runs scroll-driven `translate`, `scale` and `opacity` off the main thread.
    *   **Starting caps:** 3 hero layers. 4 repaint moves, with at most 2 uses each (see Motion budget).
    *   **Answered by:** the P0 and P1 traces, before P3 starts.
    *   **If bad:** lower the caps to what passes, and record the new numbers in this document.
*   **Q3. jsDelivr alias freshness.** Does `https://cdn.jsdelivr.net/npm/@dollyjs/core@0/src/dolly.min.css` serve 0.4.0 after release?
    *   **Answered by:** the release verification in item 7, before any homepage PR that uses exits is merged.
    *   **If bad:** purge the alias through jsDelivr's purge endpoint, and wait until it serves 0.4.0.

## Critical User Journeys (CUJs)

### CUJ 1: A developer from Reddit opens the homepage on a phone

*   **Given**:
    *   A Pixel 7 Pro or an iPhone 14, held in portrait (390px wide).
    *   No prior visit.
    *   For the Pixel test, the network is throttled to Chrome's "Fast 4G" profile.
*   **When**: The page loads, the reader looks at it for 10 seconds, then swipes up.
*   **Then**:
    *   Before any scroll, the first screen shows everything G3 lists.
    *   The hero doesn't reflow when the web fonts arrive.
    *   On the first swipe, the hero's layers leave the viewport (rising, panning, pushing past the camera) while chapter 1 arrives from below.
    *   The page moves with the finger the whole time; nothing pins.
    *   No frame takes longer than 50 ms.
    *   Each animated element shows the `data-dolly` or `data-dolly-exit` value that produced it.

### CUJ 2: A developer adds an exit to their own page

*   **Given**: A page using `@dollyjs/core@0`, from npm or from `https://cdn.jsdelivr.net/npm/@dollyjs/core@0/src/dolly.min.css`, after 0.4.0 is published.
*   **When**: They add `data-dolly-exit="tilt-up"` to a section header.
*   **Then**:
    *   The header sits where their layout puts it until its top reaches the top of the viewport.
    *   It then rises and fades out as it scrolls off.
    *   Scrolling back brings it back.
    *   A value that isn't in the exit list (for example `data-dolly-exit="zoom"`) does nothing, and the element stays visible.

### CUJ 3: A visitor with reduced motion, or a browser without scroll timelines

*   **Given**: Any one of:
    *   iOS with Reduce Motion on;
    *   Safari 18 on iOS 18, which has no `animation-timeline` support;
    *   the page printed.
*   **When**: They load and scroll the homepage, or any page using `data-dolly-exit`.
*   **Then**:
    *   Every element renders fully visible in its authored position.
    *   Nothing is left part-faded, clipped or offset.
    *   The hero looks the same as the still first screen in CUJ 1.

### CUJ 4: The maintainer releases 0.4.0 and switches the homepage to it

*   **Given**: The library PR is merged with tests passing. The homepage redesign is not merged.
*   **When**: The maintainer runs the release steps in item 7: bump the version, tag, and push.
*   **Then**:
    *   `release.yml` publishes 0.4.0 to npm.
    *   The checks in item 7 pass.
    *   Only then is the homepage PR that uses `data-dolly-exit` merged.

## Technical Plan (Architecture)

### Shape of the work

```text
 ┌────────────────────────┐   tag v0.4.0    ┌──────────────────────────┐
 │ L. Library 0.4.0       │ ──────────────▶ │ npm + jsDelivr @0        │
 │ data-dolly-exit        │                 │ (site snippets point     │
 │ src/dolly.css + tests  │                 │  here)                   │
 └────────────────────────┘                 └────────────┬─────────────┘
           ┆ no dependency: both deploy                  │ gate: item 7 checks
           ┆ src/dolly.css from main                     │ pass before P3 merges
           ┆                                             ▼
 ┌────────────────────────┐ gate: guard  ┌──────────────────────────────┐
 │ P0–P1. Perf fixes on   │ test + base- │ P2–P4. Redesigned index.html │
 │ the CURRENT index.html │ line traces  │ assets/site.css, fonts,      │
 │ (no library change)    │ ───────────▶ │ images                       │
 └────────────────────────┘              └───────────────┬──────────────┘
                                                         ▼ gate: site.css exists
                                         ┌──────────────────────────────┐
                                         │ P5. moves.html links         │
                                         │ assets/site.css              │
                                         └──────────────────────────────┘
```

The dotted line marks no dependency. L and P0–P1 can run in parallel. P2 depends on P1 for two things: the homepage guard test, and the P0/P1 traces that set the caps in Q2. The parts of P3 that use exit mode depend on L being published and verified.

### Background: how dolly attaches motion

*   **`data-dolly="<move>"`** gives an element a move.
*   **Knobs** are custom properties: `--dolly-range` (when the move plays), `--dolly-ease` (its easing) and `--dolly-axis` (which scroll direction drives it).
*   **`data-dolly-on`** picks which timeline drives a move:
    *   no attribute: the element's own view timeline;
    *   `scene`: the enclosing pinned scene's timeline;
    *   `page`: the whole page's scroll.
*   **`data-dolly-stagger`** on a parent offsets each child's range, using a per-child index `--dolly-i`.
*   **Two fallback blocks** turn animation off so content stays visible:
    *   `@supports not (animation-timeline: view())` (`src/dolly.css:252-275`);
    *   `@media (prefers-reduced-motion: reduce), print` (`src/dolly.css:278-280`).

### L. Library 0.4.0: `data-dolly-exit`

**API.** A new attribute whose value names an exit:

```html
<header data-dolly-exit="tilt-up">…</header>
```

*   An element carries either `data-dolly` or `data-dolly-exit`, never both. To enter with one move and leave with another, nest two elements: the outer one exits, the inner one enters, and their transforms combine.
*   An exit accepts `--dolly-range`, `--dolly-ease`, `data-dolly-ease` and `--dolly-axis`.
*   `data-dolly-on`, `data-dolly-stagger` and scenes aren't supported with exits in 0.4.0.

**Mechanism.** A new rule for `[data-dolly-exit]` sets the same four longhands as the existing `[data-dolly]` rule (`src/dolly.css:55-63`), plus its own range:

*   `animation-name: none`. An unknown value means no animation.
*   `animation-fill-mode: both`.
*   `animation-timing-function: var(--dolly-ease, linear)`.
*   `animation-timeline: view(var(--dolly-axis, block))`.
*   `animation-range: var(--dolly-range, exit 0% exit 100%)`.

The duplication is deliberate. Sharing the rule (`[data-dolly], [data-dolly-exit]`) would edit an existing line, and G6 allows additions only.

Each supported value then sets `animation-name` to a new keyframe with **only a `to` block**. With no `from`, the start of each exit is the element as authored. Before the exit range starts, `fill-mode: both` holds that start, so the element sits where the layout puts it. The animation plays forwards; no `animation-direction: reverse` is used.

**`exit 0%` → `exit 100%`** on a view timeline runs from when the element's top edge reaches the top of the viewport until its bottom edge has passed it. For an element no taller than the viewport, that is "while it leaves the viewport". For a 100svh hero wrapper at the top of the page, that is scroll position 0 to 100svh on every device. An element taller than the viewport starts its exit when its bottom edge reaches the bottom of the viewport, and finishes when its bottom passes the top. That is safe (it stays visible at rest), but the exit plays while the element still fills the screen and is being read. For the hero, that means taller content starts its exit later in the scroll. Verified with `test/exit-probe.html` in Chrome.

**The 13 exits.** Each exit's `to` state mirrors its entrance's `from` state, so the motion keeps going in the same direction instead of reversing. Mirroring means:

*   translate and rotate are negated;
*   scale is reflected about 1 (0.9 becomes 1.1);
*   opacity, blur and clip-path keep the entrance's hidden value, with clip-path insets moved to the opposite edge.

| `data-dolly-exit` | `to` state | Reads as |
| :--- | :--- | :--- |
| `fade` | opacity 0 | fades out |
| `tilt-up` | opacity 0; translate 0 -2.5rem | keeps rising |
| `tilt-down` | opacity 0; translate 0 2.5rem | keeps sinking |
| `pan-left` | opacity 0; translate -3rem 0 | keeps moving left |
| `pan-right` | opacity 0; translate 3rem 0 | keeps moving right |
| `dolly-in` | opacity 0; scale 1.1 | the camera pushes past it |
| `dolly-out` | opacity 0; scale 0.9 | the camera pulls away |
| `crane` | opacity 0; translate 0 -5rem; scale 1.06 | the camera keeps craning up |
| `roll` | opacity 0; rotate 5deg; scale 1.04 | keeps rolling |
| `reveal` | clip-path inset(0 0 0 100%) | wipes off to the right |
| `wipe-up` | clip-path inset(0 0 100% 0) | wipes off upward |
| `rack` | opacity 0; filter blur(14px) | focus pulls away (blurs; kept off the homepage) |
| `whip` | opacity 0; translate -4rem 0; filter blur(8px) | whips out left (blurs; kept off the homepage) |

**Keyframe names.** Each exit's keyframe is named `dolly-<move>-exit`, with two exceptions: `dolly-in` and `dolly-out` become `dolly-in-exit` and `dolly-out-exit`, matching their entrance keyframes `dolly-in` and `dolly-out`.

**Fallbacks.** With no timeline, duration resolves to 0s, and `fill-mode: both` would park a `to`-only animation on its hidden `to` state. To prevent that, a new, separate rule `[data-dolly-exit] { animation-name: none !important }` is added inside each of the two fallback blocks. The existing selectors and declarations in those blocks are untouched, which G6 checks.

**Scroll padding.** View timelines treat the scroller's `scroll-padding` as an inset. The homepage's old `scroll-padding-top: 64px` made every exit start 64px early (the hero sat at 92% opacity at scroll 0), so the homepage sets none. README Gotchas documents it for users.

**Placement.** The exit rules go in a new `---------- exits ----------` section after named easings and before the authoring-knobs comment. Order relative to other rules doesn't matter: every exit knob is read through a custom property, and exit elements carry no other dolly attribute that a later rule could override.

**Header comment.** Rule 1 at the top of `src/dolly.css` gains one sentence: exits hide an element only after it has left the viewport, and only where a timeline drives them.

**Authoring rules,** documented in README and `agents.md`:

*   An exit range uses `exit` offsets only, never `entry`, `cover` or `contain`. Sub-ranges such as `exit 0% exit 45%` are fine.
*   Don't put an exit on an element in the last viewport-height of the page. It never reaches `exit 100%`, so it stays part-faded.
*   A container whose children use `pan-*`, `dolly-in`, `crane` or `whip` exits needs `overflow: clip`, never `overflow: hidden`. `hidden` makes the container its own scroller, which deactivates the children's view timelines.

**Docs.**

*   README gets a top-level `## Exits` section containing:
    *   a table of each value and what it does;
    *   the nesting pattern;
    *   the authoring rules;
    *   the 0.4.0 limits.
*   `agents.md` gets the same rules, plus a table whose rows give the literal `data-dolly-exit="<name>"`.
*   Copy-paste snippets switch from `@0/src/dolly.min.css` to `@0/src/dolly.min.css`, the file that npm ships. jsDelivr serves it as published, so no minifier can change the new syntax.

**`moves.html`.** A new "Exits" section of 13 cards, generated by `scripts/build-moves.py`. On the default range, a 60px card subject would exit over 60px of scroll, and under the sticky header. So exit cards use `--dolly-range: exit -35vh exit calc(100% - 60px)`: still exit offsets only, starting 35vh early and finishing as the subject slides under the header. Verified in Chrome during PR-L. The page also gets a compact index (in P5).

#### Release flow (0.4.0)

The steps are written once, in item 7. Rollback is described under Non-Functional Requirements.

### P0–P1. Performance fixes on the current homepage

**P0, baseline.** Record traces of today's `index.html` on both devices, using the G1 procedure. These traces are the calibration evidence: the procedure has to fail here. They also feed Q2.

**P1, removals.** These edit the current `index.html` (commit `3d6bfcc`) only, with no library change:

1.  **Unpin the five scenes.**
    *   Remove `data-dolly-scene`, `data-dolly-pin` and `data-dolly-on="scene"`, along with the `contain`-based `--dolly-range` values they used. Children fall back to their own entrance ranges.
    *   Moves that assume a pin, or misbehave once unpinned, are swapped for library entrances:

        | Current move | Replacement | Why |
        | :--- | :--- | :--- |
        | `fly` (4 plates, Act I) | removed | as static plates they would sit half off-screen; 2 of the 4 photos repeat elsewhere |
        | `drop` (14 empty panes, Act II) | removed | decoration with no content; 14 composited 3D layers |
        | `pass` (5 plates, Act IV) | removed | all 5 photos repeat elsewhere; stacked at the centre once unpinned |
        | `beat` | `tilt-up` | `beat` ends at opacity 0, so unpinned it fades copy away |
        | `letter` | `tilt-up` | `letter` reflows the line |
        | `track` | `pan-left` | `track` loses content in the fallback once unpinned |
        | the five `mask` glyphs | `fade` | they relied on the `.glyph` filter, which is removed |
        | Act V `sequence` and `iris` | kept, with ranges on their own view timeline (`cover 15%`–`55%`, `cover 55%`–`70%`) | on the default range the iris opened before the countdown played |

    *   `push`, `count`, `iris` and `sequence` stay; the redesign replaces the page anyway. `sequence` keeps `assets/leader.png`, so the deploy check is unchanged.
2.  **Remove the scroll-driven `:root` world animation:** the `@property` rules for `--bg`, `--glow` and `--grain`, and the `world` keyframes. Set `--bg: #0B0B0C` and `--glow: #191922` as fixed values. `--grain` goes with the grain layer.
3.  **Remove the costly effects:**
    *   the grain layer and its rule;
    *   both `mix-blend-mode`s;
    *   both `backdrop-filter`s, replaced by a solid background;
    *   the `.glyph` filter and the dead `.masked` rule;
    *   every `data-dolly-depth`;
    *   the masthead `.readout`, with its `@property --scroll-pct` and `read-out` keyframes.
4.  **Clean up the leftovers** those removals leave: the references at `index.html:129`, `:133`, `:142` and `:547`; the `.film [data-dolly-pin]::before/::after` rules (`:161-165`); and the comment block about pinning (`:566-580`).
5.  **Images:**
    *   Remove duplicate plates that reuse a photo.
    *   Cap `srcset` at 800w.
    *   Set `sizes` to the rendered width.
6.  **Fix stale copy** that refers to pinned sections. The size figures for AOS are handled by item 10's measurement rule.
7.  **Delete `scripts/make-ribbon.py`** and fix README's ribbon passage. The ribbon is already gone from `index.html`: the script exits with "no ribbon markup in index.html".
8.  **Add the PR-1 guard test** (item 11).

P1 is traced on both devices before deploy. If P1 fails G1, find the remaining causes and revise the motion budget before P2 starts.

### P2–P4. The redesigned homepage

These are three stages, committed in order inside PR-2:

| Stage | Contents | Exit criterion |
| :--- | :--- | :--- |
| P2 | Tokens, fonts, static markup and copy. No motion. | The maintainer approves the copy and the decision checklist (item 13). Contrast ratios are recorded. The still page passes G3 with JavaScript off. |
| P3 | Hero exits and library entrances, using transform and opacity only. | Item 7's published-package checks have passed. Traces pass G1. Still-frame screenshots pass. |
| P4 | Repaint moves below the title card, added one per commit. | A trace after each commit passes G1, within the Q2 caps. |

**Files.**

*   `index.html`: markup, plus a page-only `<style>` block for layout and components.
*   `assets/site.css` (new): design tokens and `@font-face` rules, shared with `moves.html` from P5.
*   `assets/fonts/` (new): self-hosted, Latin-subset `woff2` files and their OFL licence texts.
*   `src/dolly.css`: the motion, loaded as today.

`deploy.yml` fingerprints `assets/site.css` for cache-busting, the way it already does for `src/dolly.css`.

**Type.** Two families, both self-hosted (item 15):

*   **Jost**, weights 400, 500 and 700, for display and body text.
    *   Using Jost for body text changes the brief, which had reserved Jost for display. The maintainer chose one family to cut a download and a set of fallback metrics, and for a more uniform look. That accepts that a geometric face reads worse in long paragraphs.
    *   To compensate, body text is at least 17px, with a line height of 1.55 and lines of about 65 characters.
    *   The homepage has little body copy. The `moves.html` card descriptions are the main test.
*   **Azeret Mono**, weights 400 and 500, for code. It is already in use, under the OFL.

**Colour.** Tokens in `assets/site.css`:

*   `--paper`: warm off-white;
*   `--ink`: near-black;
*   `--ink-soft`;
*   `--accent`: `#2B4BE8`;
*   `--block`: one muted warm colour for flat colour panels;
*   `--surface`;
*   `--rule`.

Every text and code pairing is checked to WCAG AA. The exact values are chosen in P2 and recorded next to each token, with its contrast ratio.

**Page structure.** Composed for 390px portrait first, then checked at 1440×900, in phone landscape and at 200% zoom:

1.  **Title card,** the only full-viewport section. It contains:
    *   the claim, set in Jost;
    *   the snippet, in Azeret Mono;
    *   below the snippet, at body size and full opacity, the npm and CDN install lines;
    *   a poster billing block (`<dl>`) holding `@dollyjs/core`, "v0", MIT, "0 JS" and the supported browsers;
    *   the fails-visible promise.
2.  **"One attribute":** a band of at most half a viewport, with a letter-board title. The snippet runs live on a real element next to it.
3.  **Sampler:** 4–6 shots. Each is captioned with its attribute in lowercase monospace and a plain verb, such as "`tilt-up` rises into place".
4.  **Fails visible:** the same content shown with animation off, as proof of the fails-visible promise.
5.  **Performance:** one line comparing dolly's size with AOS (Animate On Scroll, a common JavaScript scroll-animation library). The comparison is gzipped `@0/src/dolly.min.css` against AOS's published CSS plus JS, measured the same way. The measured figure replaces both today's homepage figure (14 kB) and README's (4.7 kB). Trace numbers are added once G1 has passed.
6.  **Install again:** the install lines at full opacity, outside any exit element. Links to `moves.html`, `agents.md` and GitHub, and the one-line footer dedication.

**The hero cross-cut.** The title card is a container with these rules:

*   `display: flex; flex-direction: column; min-height: 100svh; overflow: clip`.
*   It holds up to 3 **layers**, stacked top to bottom in a flex column (revised during P2: layers overlaid on one grid cell collided at 360×780). Each layer's exit starts when its own top reaches the viewport top, so the claim leaves first and the billing block after it.
*   If the content needs more height (an iPhone SE, 200% zoom), the box grows instead of the layers overlapping, and the exits start a little later.
*   Each layer carries `data-dolly-exit`, plus a sub-range that orders the layers.
*   **Transform and opacity only:** no repaint move appears in the title card.

```text
 scroll 0 ───────────────────────────────────────────▶ 100svh
 layer A: claim + snippet    ██████████░░░░░░░░░░  exit 0%  → exit 50%  (tilt-up)
 layer B: billing + install  ░░░░██████████░░░░░░  exit 20% → exit 70%  (dolly-in)
 layer C: flat colour panel  ░░░░░░░░██████████░░  exit 40% → exit 90%  (pan-left)
 chapter 1 (next section)    ░░░░░░░░░██████████░  library entrances, default range
 (each cell is 5% of the scroll from 0 to 100svh)
```

*   The layer moves and ranges are starting values, tuned in P3 and recorded on the decision checklist (item 13).
*   Layer C is a solid `--block` panel; `pan-left` moves it sideways inside the title card's clip.
*   Layers set `pointer-events: none` and their content sets `pointer-events: auto`, so text in a lower layer stays selectable.
*   For a hard cut instead of a dissolve, set `--dolly-ease: steps(2, jump-none)` on the outgoing layer, and give the incoming section's elements a matching stepped ease.

**Letter-board rows.** Chapter titles are black uppercase Jost on a white board.

*   The board's grooves are a static `repeating-linear-gradient` background. It is painted once and never animated.
*   Rows enter with library entrances using `data-dolly-stagger`, one word per child. Nothing is split per letter.
*   Letter-board styling never applies to code, attribute values or install lines.

**Motion budget.** This is one allow-list, enforced by the guard (item 21):

*   **Allowed:**
    *   the entrances `fade`, `tilt-up`, `tilt-down`, `pan-left`, `pan-right`, `dolly-in`, `dolly-out`, `crane` and `roll`;
    *   the 9 exits that use only transform and opacity: `fade`, `tilt-up`, `tilt-down`, `pan-left`, `pan-right`, `dolly-in`, `dolly-out`, `crane` and `roll`;
    *   `progress` and `travel`.
*   **Allowed below the title card only, under the Q2 cap** (starting at 4 repaint moves with at most 2 uses each, never on an element as large as the viewport): the entrances `reveal`, `wipe-up`, `iris`, `draw`, `count` and `mask` (`mask` at most once), and the `reveal` and `wipe-up` exits.
*   **Everything else is rejected,** including `track`, any `filter`, `backdrop-filter` or `mix-blend-mode`, and animated custom properties on `:root` or on fixed or sticky elements.

**Images.** Three or fewer, self-hosted in `assets/`. Each is at most 800w, with `sizes` matching its rendered width. Flat colour and type do most of the work.

**Content no longer on the homepage.**

*   The 34-row reference table. Its job moves to `moves.html`, which has a live card for every move plus a compact linked index (P5).
*   The Dolly Parton photo and the countdown leader. `assets/leader.png` stays, because `moves.html` uses it.
*   The fine-print cards.

### P5. `moves.html`

*   `scripts/moves-head.html` drops its own `:root` token block and its Google Fonts links, and links `assets/site.css` instead.
*   Headings take Jost.
*   The card grid, card markup and demo behaviour are unchanged.
*   A compact index at the top lists every move and exit with its cost, each linking to its card.
*   Class names that collide with the new homepage (`.card`, `.plate`, `.rail`, `.sheet`) stay page-local, because each page has its own `<style>`. Only tokens and fonts are shared.

### Tests (intent)

The tests are dependency-free, run under `npm test`, and live in `test/moves.test.mjs`. Item numbers point to the exact checks.

*   **L:** the exit rules and their keyframes pair up; both fallback blocks turn exits off; the docs and `moves.html` list every exit; and counts stay consistent (items 3 and 6).
*   **P1:** a guard keeps the removed effects from coming back (item 11).
*   **P2:** the guard becomes an allow-list for the whole homepage, and the homepage table test is retired (item 21).
*   **P5:** the `moves.html` index links resolve (item 23b).

## Alternatives Considered

### Alternative A: Pin one section, then not the next

*   **Pros**: Keeps one of dolly's headline features on the homepage.
*   **Cons**: The Reddit quotes object to pinning itself, not to how often it happens. Alternating also makes scrolling unpredictable, because the reader can't tell whether the next swipe will move the page.
*   **Reason for Rejection**: It doesn't answer the complaint.

### Alternative B: Animate only `transform` and `opacity` on the homepage

*   **Pros**: The cheapest possible budget, which passes G1 with the most margin.
*   **Cons**: It removes `reveal`, `wipe-up`, `iris`, `mask`, `draw` and `count`, the moves that most clearly show what CSS can do. The maintainer judged the result would look cheap.
*   **Reason for Rejection**: Rejected by the maintainer for the page as a whole. The title card does use transform and opacity only. Repaint moves are allowed below it, on small elements, under a cap.

### Alternative C: Remove or cheapen blur in the library

*   **Pros**: Library users would get cheaper `rack` and `whip` too.
*   **Cons**: It changes how existing moves look for everyone who already uses them.
*   **Reason for Rejection**: It breaks G6. Blur stays in the library and off the homepage.

### Alternative D: Fake blur with a crossfade to a pre-blurred copy

*   **Pros**: Looks close to blur at the cost of an opacity animation.
*   **Cons**: It only works on images, not live text, and it doubles markup or image weight.
*   **Reason for Rejection**: Blur is off the homepage, so there's nothing to fake.

### Alternative E: Fix the current page in place instead of redesigning

*   **Pros**: Much less work: P1 alone is about one file of removals and may pass G1.
*   **Cons**: The maintainer dislikes the current look, and the page teaches rather than sells.
*   **Reason for Rejection**: It doesn't fix the look. The removals survive as P1, which ships first.

### Alternative F: Film-looking visuals (grain, leaders, sprocket holes)

*   **Pros**: Reads as "film" at once.
*   **Cons**: The current page already uses them and doesn't feel cinematic. The grain layer is also one of the performance costs.
*   **Reason for Rejection**: The maintainer wants film language and camera-like motion, not props.

### Alternative G: A time-based CSS animation on page load for the hero

*   **Pros**: Motion before the reader touches anything.
*   **Cons**: Dolly doesn't do time-based animation, so the first thing visitors see would be something the library can't do.
*   **Reason for Rejection**: It misrepresents the product, and it breaks G4.

### Alternative H: Build the hero from entrances, reversed entrances, or stock `zoom`/`track`

*   **Pros**: No library change, so the homepage wouldn't depend on 0.4.0 being published.
*   **Cons**:
    *   **Entrances:** these play between `entry 0%` and `cover 35%`, so an element already on screen at load shows finished and does nothing on scroll. Elements in the lower part of the first screen load part-faded, by an amount that depends on viewport height.
    *   **Reversed entrances in page CSS:** the element starts hidden. With no scroll timeline it parks on the hidden keyframe, and nothing in the library's fallback catches it.
    *   **`zoom` and `track` over an exit range:** they start at the authored position, but neither changes opacity. They can scale or slide a layer, but not hand over to the next section.
*   **Reason for Rejection**: None of them can produce the cross-cut, and the reversed version breaks the fails-visible promise.

### Alternative I: Exit mode as reversed entrances (`data-dolly-on="exit"`)

*   **Pros**: No new keyframes. Every entrance would play backwards over the exit range.
*   **Cons**:
    *   While waiting to exit, a reversed element holds the move's final keyframe. That leaves `beat`, `beat-in`, `fly`, `drop` and `pass` invisible on screen, and `zoom`, `parallax`, `track`, `iris`, `mask`, `letter` and `sequence` displaced.
    *   Easing flips.
    *   Inside a `data-dolly-stagger` container, the more specific stagger rule wins, and the element vanishes as it arrives.
    *   It plays like a tape rewinding.
    *   `data-dolly-on` names a timeline and holds one value.
*   **Reason for Rejection**: Fragile, and less like film. Replaced by `data-dolly-exit`, which uses `to`-only keyframes.

### Alternative J: A split-flap move (`flap`)

*   **Pros**: A recognisable, mechanical "announcement" look.
*   **Cons**:
    *   A new move touching about 7 files, with per-character markup.
    *   Decoy glyphs would have to live in CSS generated content, because ARIA forbids `aria-label` on `span`, `div`, `p` and `code`.
    *   About one GPU layer per character. That is an unmeasured estimate of about 10 MB per 20-character heading on an iPhone.
    *   Wrong letters would show in the hero at load.
    *   It contradicts README's "no text splitting".
*   **Reason for Rejection**: The maintainer dropped it in favour of letter boards, which are static type and need no new move.

### Alternative K: A pinned demo, on the homepage or on its own page

*   **Pros**: Still demonstrates scenes, which are a real library feature.
*   **Cons**:
    *   On the homepage, it brings back what Reddit objected to.
    *   Behind a `:has(:checked)` toggle, opening it changes the page height under the reader.
    *   On its own page, it needs deploy wiring and its own trace.
*   **Reason for Rejection**: Cut from this change.

### Alternative L: Futura for display type

*   **Pros**: The face most associated with Wes Anderson's titles.
*   **Cons**: It's a commercial font, and the Adobe Fonts hosting adds a tracking request.
*   **Reason for Rejection**: Jost (OFL) is closely modelled on it and can be self-hosted.

### Alternative M: Split this into two or three design documents

*   **Pros**: The library API gets reviewed on its own, and the urgent fix isn't tied to the redesign.
*   **Cons**: Two or three review cycles, with cross-references between them.
*   **Reason for Rejection**: The maintainer chose one document. The library section is self-contained, so it can ship once approved.

### Alternative N: Build-time token copy, or hand-mirrored tokens with a test

*   **Pros**:
    *   Build-time copy needs no extra request and no deploy change.
    *   Hand-mirroring needs no new mechanism.
*   **Cons**:
    *   Build-time copy couples `build-moves.py` to the homepage's markup.
    *   Hand-mirroring means every token change is made twice.
*   **Reason for Rejection**: The maintainer chose a shared `assets/site.css`, fingerprinted in `deploy.yml`. It costs one render-blocking request ahead of the hero.

### Alternative O: A pasted keyframe snapshot test for G6

*   **Pros**: Catches any change to an existing keyframe body or default range.
*   **Cons**:
    *   A pasted list breaks the test file's rule that "everything here is derived from the stylesheet".
    *   It forces a commit-order rule.
    *   It misses the fallback blocks this change edits.
*   **Reason for Rejection**: Replaced by "every change to `src/dolly.css` is a pure addition", checked with `git diff v0.3.2 -- src/dolly.css`.

### Alternative P: Point the CDN snippets at the unminified `src/dolly.css` (reversed during the build)

*   **Pros**: No dependency on jsDelivr's minifier, which generates `dolly.min.css` on request and isn't in the repo.
*   **Cons**: Measured after 0.4.0 shipped: 10.6 kB gzipped against 2.7 kB for the minified file, about four times larger. The review assumed the difference was small; it isn't, because the source is mostly comments.
*   **Reason for Rejection**: The 0.4.0 `dolly.min.css` was checked and keeps every exit keyframe and both fallback rules intact, so the risk this guarded against didn't materialise. The snippets went back to `dolly.min.css` with the maintainer's approval. The release check in item 7 now greps the minified file.

### Alternative Q: `track` on the homepage, with its clip lifted in page CSS

*   **Pros**: A true scrolling row of shots.
*   **Cons**: In the fallback, the library only lifts `overflow: clip` for pinned scenes. The homepage would need its own workaround and a guard to check it.
*   **Reason for Rejection**: `pan-left` and `pan-right` give sideways motion without the gap. The library fix is a Future Improvement.

## Risks & Mitigations

*   **The `@0` CDN alias serves the old version after release.** Mitigated by Q3: the item 7 checks gate P3, and the alias is purged if it's stale.
*   **The hero reflows when fonts load.** Mitigated by metric-matched fallback faces and a preloaded hero weight (item 15). The P2 exit criterion checks for it.
*   **Too many composited layers on the iPhone.** Mitigated by the hero-layer cap and the repaint cap in Q2, set from traces. The hero uses transform and opacity only.
*   **Exits on elements taller than the viewport, or in the last viewport-height of a page.** Mitigated by documented authoring rules in README and `agents.md`, and a review-checklist item for the homepage (Verification Plan).
*   **The homepage uses an exit before npm has it.** Mitigated by the P3 gate on item 7. On rollback, homepage commits are reverted before library commits (see Rollout and rollback).
*   **`assets/site.css` delays first paint.** It is render-blocking. Mitigated by keeping it to tokens and `@font-face` rules only, and by recording time to first paint in the P2 trace.
*   **Contrast fails in the new palette.** Mitigated by recording WCAG ratios next to each token (P2 exit criterion).
*   **Security:** the change is CSS and static files only, all self-hosted. It adds no new attack surface, and the homepage stops making third-party requests.

--------------------------------------------------------------------------------

## Non-Functional Requirements

*   **Performance:** G1 is the bar. Every PR that changes `index.html` (PR-1, and PR-2 at P3 and P4) attaches traces from both devices. Each trace records the device, browser version, refresh rate and the swipe script used.
*   **Accessibility:**
    *   WCAG AA contrast for every pairing.
    *   Reduced motion renders the page static.
    *   Code copies exactly as shown.
    *   Hero layers don't block text selection.
    *   At 200% zoom and in phone landscape, the title card grows instead of overlapping.
*   **Privacy:** no third-party requests from the homepage. Fonts and images are self-hosted, and the `fonts.googleapis.com`, `fonts.gstatic.com` and `images.unsplash.com` preconnects are removed.
*   **Rollout and rollback:**
    *   Each PR is its own merge and deploy to `main`, and is rolled back by reverting that merge.
    *   npm releases are fixed forward, as 0.4.1.
    *   On the site, homepage commits are reverted before library commits, so the page never uses an exit that the deployed stylesheet lacks.
    *   Exits are additive, so a bad 0.4.0 only affects pages that use `data-dolly-exit`.

## Additional Resources

*   [`concepts_brief.md`](../../concepts_brief.md): the brainstorm brief. It covers three Goldfish reviews and decisions D1–D26. It sits in the repo root and is not committed.
*   [`consolidated_review_report.md`](../../consolidated_review_report.md): the review of this document. Not committed.
*   [`src/dolly.css`](../../src/dolly.css): the header comments explain the library's three rules, and the comment above the no-timeline block explains its reasoning.

## Future Improvements

*   **Exits for `iris`, `draw` and `count`,** if users ask. These need their own "keep going" definition.
*   **Staggered exits:** a `[data-dolly-stagger] > [data-dolly-exit]` rule with `--dolly-i` offsets, if a real page needs credits that leave in sequence.
*   **Exits inside scenes and on the page timeline:** a separate definition of "leaves" for scene children, for example over the last part of the scene's `contain` range, and for `data-dolly-on="page"`.
*   **An entrance and an exit on one element:** comma-separated animation lists built from two custom properties, if nesting proves awkward.
*   **`track` fallback fix in the library:** inside each fallback block, an additive rule `:has(> [data-dolly="track"]) { overflow: visible !important }`. Without it, a user who follows the library's own "pair with overflow:clip" advice loses content when there's no timeline.
*   **A pinned-scene demo page,** traced separately and clearly labelled.
*   **A split-flap move,** as its own release, if its accessibility and layer-cost problems get solved.

--------------------------------------------------------------------------------

## Detailed Implementation Plan

There are four PRs. PR-L and PR-1 are independent and can be open at the same time.

| PR | Phase | Depends on | Ships to |
| :--- | :--- | :--- | :--- |
| PR-L | L: library 0.4.0 | none | `main`, then npm through the git tag `v0.4.0` |
| PR-1 | P0–P1: performance fixes | none | `main` (the site) |
| PR-2 | P2–P4: redesign | PR-1 merged. P3 needs the item 7 checks passed. | `main` (the site) |
| PR-3 | P5: `moves.html` restyle | PR-2 merged (needs `assets/site.css`) | `main` (the site) |

The P2–P4 stages inside PR-2, with their exit criteria, are in the table under "P2–P4. The redesigned homepage". `ci.yml` runs `npm test` on every push and PR, so every commit has to pass on its own.

### Maintainer-local edits (not in any PR)

These files are gitignored (`.gitignore:8`, `:14`, `:15`), so no PR can carry them. The maintainer edits them locally, at the point given.

*   **`PRODUCT.md`, one edit, before PR-1 work starts:**
    *   Principle 3 becomes "the homepage sells; `moves.html` is the reference and plays every move".
    *   Product principle 1 (`PRODUCT.md:101`) gains the exit exception: exits hide an element only after it has left the viewport, and only where a timeline drives them.
    *   Rewrite the Stack paragraph: two pages, plus `assets/site.css`.
    *   Update the preset list (`:89`) and the fixture reference (`:90`).
    *   Reword the `@starting-style` exclusion (`:61-62`) so it clearly means elements added to or removed from the DOM, not scroll exits.
    *   Record the design direction in one paragraph: framing, title-sequence type, letter boards, and Jost for display and body.
*   **`RELEASING.md`, before tagging `v0.4.0`:**
    *   Add the jsDelivr check from item 7 to the existing "Verifying a release actually shipped" section (`RELEASING.md:97-108`).
    *   Add an "adding a move or exit" checklist: keyframes; rule; README row; `agents.md`; `build-moves.py` group or exit list, and description; regenerate `moves.html`; counts; CHANGELOG.
*   **`test/exit-probe.html`, before tagging `v0.4.0`:**
    *   A page with labelled exit elements, opened in Chrome, Safari 26 and Firefox 159, with and without reduced motion.
    *   Expected results:

        | Case | Expected result |
        | :--- | :--- |
        | Normal flow | Sits at its authored position until its top reaches the viewport top, then completes its exit by the time its bottom passes the top. With reduced motion: visible, no animation. |
        | Under an `overflow: hidden` ancestor | Visible at its authored position, no animation (Q1). |
        | Inside a horizontal scroller without `--dolly-axis: inline` | Visible at its authored position, no animation (Q1). |
        | Taller than the viewport | Starts its exit when its bottom reaches the viewport bottom, and completes by the time its bottom passes the viewport top. |

    *   If either Q1 case shows a hidden or offset element, follow Q1's "if bad" action before tagging.

Binding rules for contributors live in this document and in `agents.md`, not in the local files.

### PR-L: Library 0.4.0 (`data-dolly-exit`)

Items 2 and 3 land in the same commit, so `npm test` passes at every commit.

#### 1. (Removed)

The snapshot test was replaced by the G6 pure-addition rule (see Alternative O). Item numbers are kept so that references elsewhere stay stable.

#### 2. `src/dolly.css` (Modify, additions only)

*   **Type / Scope**: The library stylesheet.
*   **Proposed Changes**:
    *   **Header, rule 1:** add one new sentence. No existing line changes.
    *   **New section `---------- exits ----------`,** placed after the named easings and before the authoring-knobs comment. It contains:
        *   a comment explaining the `to`-only design and why it doesn't use `reverse`;
        *   13 `@keyframes`, named and valued as in the Technical Plan table;
        *   the `[data-dolly-exit]` rule with the five longhands listed in the Technical Plan;
        *   13 `[data-dolly-exit="<move>"]` rules, each setting only `animation-name`.
    *   **Fallbacks:** inside the `@supports not (animation-timeline: view())` block at `src/dolly.css:252-275`, and inside the `@media (prefers-reduced-motion: reduce), print` block at `:278-280`, add a new rule `[data-dolly-exit] { animation-name: none !important }`. Each gets a one-line comment. Existing rules in both blocks are untouched.
*   **Why**: The feature itself, plus the fallbacks that keep G5. Making every change an addition is what lets G6 be checked with `git diff`.

#### 3. `test/moves.test.mjs` (Modify, same commit as item 2)

*   **Type / Scope**: Unit tests.
*   **Proposed Changes**: Tests are cited by their names.
    *   **New `exits` Map.** Built from `^\[data-dolly-exit="([^"]+)"\]$` rules the same way the existing `moves` Map is built, so no list is hardcoded.
    *   **Extend "every move has keyframes and every keyframes block has a move".**
        *   A keyframe counts as used if either map names it.
        *   Every keyframe named in `exits` has a `to` (or `100%`) block and no `from` or other percentage blocks.
    *   **Extend "moves whose `to` is not the authored state turn off without a timeline":**
        *   `moveOf()` also matches `\[data-dolly-exit="([^"]+)"\]`, and returns `exit:<name>`.
        *   A bare `[data-dolly-exit]` rule inside `@supports not (animation-timeline` that sets `animation-name: none !important` counts as guarding every `exit:*`.
    *   **Extend "the no-timeline safety block cannot be overridden by a later move rule".** Its selector filter becomes `/\[data-dolly(-exit)?(="|\])/`, so the bare exit rule is checked for `!important` too.
    *   **Extend "reduced motion turns every move off".** Today it only requires some reduced-motion rule whose selector includes `[data-dolly`, which a `[data-dolly]` rule already satisfies. It now also requires a rule inside that media block whose selector includes `[data-dolly-exit]` and sets `animation-name: none`.
    *   **New: "the README documents every exit that ships".**
        *   It scopes to the README `## Exits` section, from `\n## Exits\n` to the next `\n## `.
        *   It requires a table row starting `| \`<name>\` |` for each key in `exits`, and no rows for anything else.
    *   **New: "agents.md documents every exit that ships".** For each key in `exits`, `agents.md` contains the literal `data-dolly-exit="<name>"`.
    *   **New: "the moves page has a live card for every exit".** For each key in `exits`, `moves.html` has `id="exit-<name>"` on an element containing `data-dolly-exit="<name>"`.
    *   **"Every built-in animation-range is overridable through --dolly-range"** already matches `[data-dolly-exit]` rules, because they start with `[data-dolly`. No change.
    *   **"No base rule hides an element"** already covers the new rule. No change.
*   **Why**: These lock in the fails-visible promise for exits and stop the docs and `moves.html` drifting from the stylesheet, with every list derived from the CSS.

#### 4. `README.md` (Modify)

*   **Type / Scope**: User documentation, shipped to npm.
*   **Proposed Changes**:
    *   **New top-level `## Exits` section** after `## Moves`, containing:
        *   one sentence on what `data-dolly-exit` does;
        *   a table with one row per exit: `` | `<name>` | what it does | ``;
        *   the nesting pattern;
        *   the three authoring rules from the Technical Plan;
        *   the fails-visible promise for exits;
        *   the 0.4.0 limits (no `data-dolly-on`, stagger or scenes).
    *   **Count strings:**
        *   line 3: "34 camera moves" becomes "34 camera moves and 13 exits";
        *   line 23: "all 34 moves" becomes "all 34 moves and 13 exits";
        *   line 328: rewrite to "23 of the 34 moves, and 9 of the 13 exits, use only transform and opacity. These repaint:". Add rows for the `reveal` and `wipe-up` exits (clip-path) and the `rack` and `whip` exits (filter).

        The phrase "N camera moves" survives where "the README documents exactly the moves that ship" parses it.
    *   **CDN snippet (line 40):** `@0/src/dolly.min.css` becomes `@0/src/dolly.min.css`.
    *   **Knobs:**
        *   Lines 304-305 become "`data-dolly-ease` is an attribute you add; the rest are plain custom properties."
        *   The table row at 309 becomes `--dolly-range` only.
        *   The example at lines 251-255 drops its `data-dolly-range` attributes, so it keeps only the `--dolly-range` style.
        *   Line 310's documented `--dolly-ease` default becomes `linear`, matching `src/dolly.css`.
*   **Why**: The npm-facing documentation of the new API. Also fixes two existing errors that the new exit docs would otherwise copy: the `data-dolly-range` attribute that nothing reads, and the wrong easing default.

#### 5. `agents.md` (Modify)

*   **Type / Scope**: Instructions for coding assistants writing dolly markup.
*   **Proposed Changes**:
    *   **Attribute table (line 41):**
        *   keep "one of the 34 move names" for `data-dolly`;
        *   add a `data-dolly-exit` row: "one of the 13 exit names", "how the element leaves".
    *   **New "Exits" table** with one row per exit. Its first column is the literal `data-dolly-exit="<name>"`.
    *   **Rules:**
        *   never put `data-dolly` and `data-dolly-exit` on one element; nest instead;
        *   use `exit` offsets only in an exit range;
        *   no exit in the last viewport-height of a page;
        *   no exits on elements taller than the viewport;
        *   no exits inside `data-dolly-stagger` or a scene;
        *   use `overflow: clip`, never `hidden`, around exiting elements.
    *   **Line 50:** "Do not enumerate all 34" becomes "Do not enumerate all 34 moves or 13 exits".
    *   **Line 170:** the documented `--dolly-ease` default becomes `linear`.
    *   **Line 22 CDN snippet:** use `@0/src/dolly.min.css`.
*   **Why**: Assistants follow this file literally, so the misuse cases have to be written down.

#### 6. `scripts/build-moves.py` and `moves.html` (Modify; `moves.html` regenerated)

*   **Type / Scope**: The reference page generator and its output.
*   **Proposed Changes**:
    *   **Parse the exits separately:** `[data-dolly-exit="…"]` rules into `exit_order` and `exit_anims`, next to the existing `order` and `anims` (`build-moves.py:16-20`).
    *   **Coverage check:** add one for exits, which aborts if an exit has no `EXIT_DESC` entry or `EXIT_DESC` names an unknown exit.
    *   **Keep exits out of `GROUPS`.** Exit names repeat entrance names, so listing them there would trip the "listed in two groups" check (`:109-110`).
    *   **`EXIT_DESC`:** a new dict, with a one-line description per exit.
    *   **`repaints(n, anims_map)`:** takes the map to read from. Entrance cards pass `anims`, and exit cards pass `exit_anims`. Clip-path and filter tagging then follows from `keyframe_props` with no manual list.
    *   **`exit_card(n)`:** a new function, next to `card()` (`:139-149`). It emits:
        *   `id="exit-<n>"`;
        *   a subject with `data-dolly-exit="<n>"`;
        *   a `<code>data-dolly-exit="<n>"</code>` snippet;
        *   a `demo leaves exits` stage class instead of `arrive`. `moves-head.html` retimes `.demo.exits [data-dolly-exit]` as described in the Technical Plan.
    *   **Exits section:** rendered after the last group, with its own `{{NAV}}` entry.
    *   **`{{COUNT}}`** in `scripts/moves-head.html`'s title and description becomes "34 moves and 13 exits", built from `len(order)` and `len(exit_order)`.
    *   **Regenerate** `moves.html` with `python3 scripts/build-moves.py`.
*   **Why**: The reference page has to play every published option, and the new exit-card test requires it.

#### 7. `package.json`, `CHANGELOG.md` (Modify), and release steps

*   **Type / Scope**: Package metadata, release notes and the release runbook for 0.4.0.
*   **Proposed Changes**:
    *   **`package.json`:**
        *   `version` becomes 0.4.0;
        *   `description` becomes "Scroll animations in plain CSS: 34 camera moves and 13 exits, each set with one attribute. …". The "34 camera moves" substring is kept for "package.json agrees with the stylesheet on the move count". The exit count is prose, and no test checks it.
    *   **`CHANGELOG.md`:**
        *   `## 0.4.0 — <date>`.
        *   "Added": `data-dolly-exit`, with 13 exits.
        *   "Changed": the CDN snippets now point at `src/dolly.css`.
        *   "Fixed": the documented `--dolly-ease` default, and the removed `data-dolly-range` attribute docs.
    *   **Release steps.** This is the only copy of them in this document.
        1.  Merge PR-L.
        2.  Push `main` and the git tag `v0.4.0` together. `release.yml` checks that the tag matches `package.json`, runs `npm test` and publishes.
        3.  Run `npm view @dollyjs/core version`. Expect `0.4.0`.
        4.  Fetch `https://cdn.jsdelivr.net/npm/@dollyjs/core@0/src/dolly.min.css`. Check that it contains `[data-dolly-exit` and `dolly-tilt-up-exit`.
        5.  If step 4 shows 0.3.2, purge the `@0` alias through jsDelivr's purge endpoint, then repeat step 4.
        6.  Record the result in the PR-2 description. This is a manual pre-merge gate; no test enforces it.
*   **Why**: Semantic versioning (the change is additive, so it is a minor version), and CUJ 4.

#### 8 and 9. (Moved)

The exit probe and the `RELEASING.md` changes are maintainer-local. See "Maintainer-local edits".

### PR-1: P0–P1 performance fixes

#### 10. `index.html` (Modify, the current page)

*   **Type / Scope**: Homepage markup and inline CSS, at commit `3d6bfcc`.
*   **Proposed Changes**: Steps 1–6 of "P1, removals" in the Technical Plan. Specifically:
    *   **Unpin:** remove the five `.film` tracks' `data-dolly-scene` and `--dolly-scene`, every `data-dolly-pin`, every `data-dolly-on="scene"`, and the scene children's `contain`-based `--dolly-range`. Remove the `[data-dolly-pin]{min-height:70svh}` rules (`index.html:552`, `:560`).
    *   **Swap moves** using the P1 table: `fly`, `drop`, `pass`, `beat` (`:796`), `letter` (`:947`), `track` (`:775`), and the five `mask` glyphs (`:709-727`).
    *   **Remove:**
        *   the `world` animation (`:65-80`), with `--bg: #0B0B0C` and `--glow: #191922` set as fixed values;
        *   `.grain` and its element;
        *   the `.mast` blend mode;
        *   both `backdrop-filter`s, replaced with solid backgrounds;
        *   the `.glyph` filter and the `.masked` rule;
        *   all `data-dolly-depth`;
        *   `.readout`, its `@property` and keyframes, and its element.
    *   **Leftovers:** `:129`, `:133`, `:142`, `:547`, `:161-165` and `:566-580`.
    *   **Images:** remove the duplicate plates; cap `srcset` at 800w; correct `sizes`.
    *   **Copy:** rewrite the lines that describe pinned sections (`:7`, `:648`, `:845`, `:849`, `:909`, `:916`, `:927-932`).
    *   **CDN snippet (`:941`):** use `@0/src/dolly.min.css`. This can merge before 0.4.0, because the file already exists at 0.3.2.
*   **Why**: G1 and G2 on the page people visit today, shipped before the redesign (G7).

#### 10a. `scripts/make-ribbon.py` (Delete), `README.md` (Modify)

*   **Type / Scope**: A stale script and its documentation.
*   **Proposed Changes**:
    *   Delete `scripts/make-ribbon.py`.
    *   In README, rewrite lines 276-286 so they no longer say the homepage has a ribbon, or that `make-ribbon.py` refits it. Keep the `draw` centerline guidance, and keep `assets/dolly-word.svg` as its example.
*   **Why**: The ribbon is already gone from `index.html`. Running the script would only print an error.

#### 11. `test/moves.test.mjs` (Modify): the PR-1 guard

*   **Type / Scope**: Unit test.
*   **Proposed Changes**:
    *   New test: "the homepage keeps the removed effects out".
    *   **CSS:** take the text of every `<style>` block in `index.html` and parse it with the existing `blocks()` and `decls()` helpers (`test/moves.test.mjs:25-61`), which skip comments.
    *   **HTML:** match attributes only inside start tags (`<[a-z][^>]*>`). Code samples in the page must be HTML-escaped (`&lt;`), so they never form start tags.
    *   **It fails on any of:**
        *   a `data-dolly-scene` or `data-dolly-pin` attribute;
        *   a `filter`, `backdrop-filter` or `mix-blend-mode` declaration;
        *   a `data-dolly-depth` attribute;
        *   `data-dolly="beat"` or `data-dolly="letter"`;
        *   an `animation-timeline` declaration in a rule whose selector is `:root`.
*   **Why**: It keeps the P1 removals from coming back. It checks only what P1 removed, because the rest of today's page is replaced in PR-2.

#### 12. `.github/workflows/deploy.yml` (no change in PR-1)

The current page still uses `assets/leader.png`, so its checks still hold.

### PR-2: P2–P4 redesign

#### 13. `index.html` (Modify, rewritten)

*   **Type / Scope**: Homepage markup and page CSS.
*   **Proposed Changes**:
    *   **Content and order:** as in Technical Plan > Page structure. This item adds only the markup specifics.
    *   **Head:**
        *   link `src/dolly.css`, then `assets/site.css`;
        *   preload the hero's Jost weight (item 15 gives the exact tag);
        *   remove the Google Fonts and Unsplash preconnects;
        *   keep the `og:` and `twitter:` tags, with the description rewritten to match the new copy;
        *   keep the canonical URL.
    *   **Title card:** a `<section>` holding up to 3 layer `<div>`s, using the grid rule from the Technical Plan. It contains:
        *   the `<h1>`;
        *   the snippet as an HTML-escaped `<pre><code>`;
        *   the install lines, with `user-select: all` on each command, as today;
        *   the billing block as a `<dl>`;
        *   the fails-visible line.
    *   **Letter-board titles:** `<h2>` with `data-dolly-stagger`, one word per child `<span>`.
    *   **Sampler shots:** each is a `<figure>`, with the attribute in `<code>` and a verb in its `<figcaption>`.
    *   **Accessibility:**
        *   heading levels in order;
        *   the billing block reads as a definition list;
        *   no `text-transform` on code;
        *   the hero layers' `pointer-events` set as in the Technical Plan.
    *   **Commits:** P2, P3 and P4 commits follow the stage table. P4 adds one repaint move per commit, each with a trace note. The note records the device, the browser version, the result against G1, and the move added.
    *   **Decision checklist.** The maintainer decides these in P2, before any motion is added, and records them in the PR description:
        *   the copy (hero claim, chapter titles, captions), in the deadpan voice;
        *   the colour values and their contrast ratios (in `assets/site.css`);
        *   the hero layer count (at most 3), each layer's exit move, and its sub-range (starting values in the Technical Plan);
        *   the 4–6 sampler moves, from the allow-list;
        *   the letter-board values: board colour, groove spacing and letter spacing;
        *   the 0–3 images.
*   **Why**: G2, G3, G4 and G8. The page sells instead of teaching.

#### 14. `assets/site.css` (Create)

*   **Type / Scope**: Shared stylesheet.
*   **Proposed Changes**:
    *   **`:root` tokens.** Every custom property `scripts/moves-head.html` defines today, so `moves.html` keeps working after P5:
        *   colours: `--paper`, `--ink`, `--ink-soft`, `--accent`, `--surface`, `--rule`;
        *   families: `--mono`, `--sans`;
        *   spacing: `--gutter`;
        *   type sizes: `--t-00`, `--t-02`, `--t-03`, `--t-06`.

        Plus the new tokens `--block` and `--display`, and any new type sizes the homepage needs, named `--t-NN` in the same series.

        `--display` and `--sans` both resolve to Jost. `--sans` keeps its name, so rules that use it need no change.

        Each colour gets a comment giving its WCAG contrast ratio against the colours it's paired with.
    *   **`@font-face`:** one rule per file in item 15, with `font-display: swap`. Fallback faces named `Jost Fallback` and `Azeret Mono Fallback` use `local()` system fonts, with `size-adjust`, `ascent-override`, `descent-override` and `line-gap-override` set as item 15 describes.
    *   **Nothing animated, and no component styles.**
*   **Why**: The shared token file the maintainer chose.

#### 15. `assets/fonts/` (Create)

*   **Type / Scope**: Static font files.
*   **Proposed Changes**:
    *   **Files:**
        *   `jost-400.woff2`, `jost-500.woff2`, `jost-700.woff2`;
        *   `azeret-mono-400.woff2`, `azeret-mono-500.woff2`;
        *   `OFL-Jost.txt` and `OFL-AzeretMono.txt`.
    *   **Source:** the variable fonts in the `google/fonts` repository, `ofl/jost/Jost[wght].ttf` and `ofl/azeretmono/AzeretMono[wght].ttf`, with their `OFL.txt` files.
    *   **Production, per weight:**
        1.  Pin the `wght` axis with fontTools' `varLib.instancer`, for example `fonttools varLib.instancer Jost[wght].ttf wght=500 -o jost-500.ttf`.
        2.  Subset and compress: `pyftsubset jost-500.ttf --unicodes=U+0000-00FF,U+2013-2014,U+2018-201D,U+2022,U+2026 --layout-features='kern,liga' --flavor=woff2 --output-file=assets/fonts/jost-500.woff2`.

        Record both commands in a comment at the top of `assets/site.css`.
    *   **Size:** at most 70 KB for all five `woff2` files together.
    *   **Preload** in `index.html`: `<link rel="preload" href="assets/fonts/jost-700.woff2" as="font" type="font/woff2" crossorigin>`. Use the weight the hero claim uses. In `assets/site.css`, the matching `@font-face` uses `url("fonts/jost-700.woff2")`, which resolves to the same URL. Without `crossorigin`, the font downloads twice.
    *   **Fallback metrics:**
        *   `size-adjust` is the ratio of Jost's average Latin character width to the fallback font's. The fallback is `local("Futura")`, then `local("Arial")`. Futura covers Apple devices, and Arial everything else.
        *   `ascent-override`, `descent-override` and `line-gap-override` are Jost's `hhea` ascender, descender and line gap, divided by `unitsPerEm` and by `size-adjust`.
        *   The values are computed with fontTools, and recorded next to the rules with the command used.
*   **Why**: Self-hosting removes the third-party requests. Metric-matched fallbacks stop the hero reflowing. The OFL requires shipping the licence.

#### 16. `assets/` images (Create and Delete)

*   **Type / Scope**: Static images.
*   **Proposed Changes**:
    *   Add at most three self-hosted WebP images for the sampler, each at most 800w.
    *   Delete `assets/parton.webp`.
    *   Keep `assets/leader.png`, used by `moves.html`.
    *   Keep `assets/dolly-word.svg`, which README documents.
*   **Why**: Fewer and smaller images, and no hotlinking.

#### 17. `scripts/make-parton.py` (Delete), `.gitignore` (Modify)

*   **Type / Scope**: An asset script and ignore rules.
*   **Proposed Changes**:
    *   Delete `scripts/make-parton.py`. It only produces the removed photo.
    *   In `.gitignore`, delete lines 17-18: the comment naming that script, and the press-photo filename. The maintainer can delete the local photo.
*   **Why**: If the script were run, it would bring the photo back.

#### 18. (Moved to item 10a)

#### 19. `scripts/make-og.py` and `assets/og-image.png` (Modify; image regenerated)

*   **Type / Scope**: Social card generator and its output.
*   **Proposed Changes**:
    *   **Font:** load `~/Library/Fonts/fonts/ofl/jost/Jost[wght].ttf`, from the same local `google/fonts` checkout the script already uses for Archivo. Kept local; not committed. Set weights with Pillow's `set_variation_by_axes([<wght>])`, since Jost has a single `wght` axis. Keep the existing missing-font error message, with the new path.
    *   **Layout:** a poster layout using the new tokens: paper background, ink type, the accent block and Jost.
    *   **Counts:**
        *   Add `exit_count()`, which parses `[data-dolly-exit="…"]` rules that set `animation-name`, next to the existing `move_count()`.
        *   Render "34 moves · 13 exits", from the two counts.
        *   Stamp a `dolly-exits` tEXt chunk next to the existing `dolly-moves` one.
    *   Regenerate the PNG.
*   **Why**: The maintainer chose to redo the social card in this change. The card stays tied to the stylesheet's counts.

#### 20. `.github/workflows/deploy.yml` (Modify)

*   **Type / Scope**: Site deploy.
*   **Proposed Changes**:
    *   Compute `SITE_V` from `sha1sum assets/site.css`.
    *   In `_site/index.html` only, rewrite `href="assets/site.css"` to `href="assets/site.css?v=$SITE_V"`, and fail if the fingerprinted string is missing. `moves.html` only links `site.css` from PR-3 (item 23c).
    *   Remove the two checks that require `assets/leader.png` in `_site/index.html` (`deploy.yml:45-47`). Keep the `moves.html` leader check.
*   **Why**: Without a fingerprint, Pages would serve new markup against a stylesheet cached for 4 hours, which is the problem this workflow already guards against for `dolly.css`.

#### 21. `test/moves.test.mjs` (Modify): the PR-2 guard

*   **Type / Scope**: Unit test.
*   **Proposed Changes**:
    *   Replace the PR-1 guard with "the homepage uses only the motion budget".
        *   It parses CSS and attributes the same way as item 11, and also reads `assets/site.css`.
        *   It fails on everything item 11 checks.
        *   It also fails if:
            *   any `data-dolly` or `data-dolly-exit` value isn't on the motion-budget allow-list, which is held in the test and mirrors the Technical Plan's Motion budget;
            *   an element in the title card `<section>` uses a repaint move;
            *   any element carries both `data-dolly` and `data-dolly-exit`;
            *   page CSS sets `opacity: 0`, `visibility: hidden` or `clip-path` on a `[data-dolly…]` selector;
            *   any `overflow: hidden` appears (the predicate of "overflow: hidden is never used", applied to page CSS);
            *   the page requests `fonts.googleapis.com`, `fonts.gstatic.com` or `images.unsplash.com`;
            *   no element containing an install command sits outside every `[data-dolly-exit]` element;
            *   `index.html` doesn't link `assets/site.css`.
        *   The allow-list is a homepage policy, not a list of library moves, so holding it in the test doesn't break the "derived from the stylesheet" rule. A comment says so.
    *   Delete "the demo page documents every move that ships", because the homepage no longer has the table. "The moves page has a live card for every move that ships" covers the reference.
    *   Extend "the social card was rendered from the current move count" so it also reads the `dolly-exits` chunk and compares it with the `exits` Map's size.
*   **Why**: It follows the content moves and enforces the budget as one list.

#### 22. (Moved)

The `PRODUCT.md` Stack paragraph edit is part of the single local edit under "Maintainer-local edits".

### PR-3: P5 `moves.html` restyle

#### 23. `scripts/moves-head.html` (Modify)

*   **Type / Scope**: Template for the reference page.
*   **Proposed Changes**:
    *   Delete the `:root` block and the Google Fonts `<link>`s.
    *   Link `assets/site.css`.
    *   Set headings in `var(--display)`.
    *   Change `font-weight: 800` (`:44`) to 700, because Jost ships 400, 500 and 700 only.
    *   Leave the card grid, card CSS and demo retiming unchanged.
*   **Why**: Shared type and colours, with the same layout.

#### 23a. `scripts/build-moves.py` (Modify)

*   **Type / Scope**: Reference page generator.
*   **Proposed Changes**:
    *   Generate a compact index at the top of the page, next to `{{NAV}}`.
        *   It is built from `GROUPS`/`order` for moves and from `exit_order` for exits.
        *   One line per entry: the name in monospace, linking to its card `id`, then its cost from `repaints(n, map)`.
    *   **Cost labels:**
        *   an empty list prints "compositor";
        *   a list containing `filter` prints "filter";
        *   any other list prints its property names, joined with ", ".
    *   It is plain text in a CSS multi-column list: no animation and no colour blocks.
*   **Why**: It gives developers a one-glance overview of every move and its cost, without listing every move twice in full.

#### 23b. `test/moves.test.mjs` (Modify)

*   **Type / Scope**: Unit test.
*   **Proposed Changes**: Add "every link in the moves page index resolves". Every `href="#…"` inside the index points to an `id` that exists on the page.
*   **Why**: The generator already guarantees the index covers every move. This test only catches broken links.

#### 23c. `.github/workflows/deploy.yml` (Modify)

*   **Type / Scope**: Site deploy.
*   **Proposed Changes**: Extend item 20's `site.css` fingerprint rewrite and its fail-on-miss check to `_site/moves.html`.
*   **Why**: `moves.html` links `site.css` from this PR on.

#### 24. `moves.html` (Modify; regenerated)

*   **Type / Scope**: Generated reference page.
*   **Proposed Changes**: Regenerate with `python3 scripts/build-moves.py`.
*   **Why**: It is generated from items 6, 23 and 23a.

### Verification Plan

*   **Build:** there is no compile step. `python3 scripts/build-moves.py` and `python3 scripts/make-og.py` regenerate their outputs, which are committed.
*   **Unit tests:** `npm test` runs `node --test`. `ci.yml` runs it on every push and PR. `deploy.yml` and `release.yml` run it before deploying and before publishing.
*   **G6:** `git diff v0.3.2 -- src/dolly.css` shows no removed or changed lines. This is checked by hand in the PR-L review.
*   **Library acceptance (PR-L):**
    *   `test/exit-probe.html` matches the expected results in "Maintainer-local edits".
    *   Every exit card on `moves.html` sits at rest until about 35vh from the top, and finishes by the time it reaches the header.
    *   After publishing, the item 7 checks pass.
*   **Frame-rate acceptance (PR-1, PR-2 at P3 and P4):**
    *   **Pixel 7 Pro:**
        *   Chrome over remote debugging, with Smooth Display off (60 Hz) and the screen at QHD+, served locally through `adb reverse`.
        *   The swipe script is three `adb shell input swipe 540 2400 540 600 300` swipes, one second apart, then one `adb shell input swipe 540 2400 540 200 80` fling.
        *   Three cold-load runs; the worst run counts.
        *   Pass: under 1% dropped plus partially presented frames in Chrome's Frames track, and no frame over 50 ms.
    *   **iPhone 14:**
        *   Safari 26, served over the LAN, measured with Xcode Instruments "Animation Hitches".
        *   Three cold-load runs of 5 swipes plus one fling; the worst run counts.
        *   Pass: hitch ratio under 5 ms/s.
    *   **Calibration:** the same procedures fail on today's `index.html` (P0).
*   **Fallback acceptance (PR-L, PR-2):**
    *   Checked with DevTools reduced-motion emulation, iOS Reduce Motion, Safari 18 on iOS 18, and print preview.
    *   Pass:
        *   every element is at opacity 1;
        *   no element has a clip-path or transform it doesn't have at rest;
        *   the title card matches the scroll-0 screenshot.
*   **Still-frame acceptance (PR-2 at P3):**
    *   **Screenshots:**
        *   at 0, 20, 40, 60, 80, 100 and 120svh of scroll, at 390×844, in Chrome and Safari 26;
        *   at scroll 0 and 50svh at 1440×900 in Chrome;
        *   at scroll 0 at 200% zoom;
        *   at scroll 0 in phone landscape (844×390).
    *   **Pass:** every shot has text at full opacity in the middle 60% of the viewport, and no two layers' text overlaps.
    *   **Font reflow:** the hero's text boxes are the same size, within 2px, before and after the web fonts load. Compare with the fonts blocked against fonts loaded.
    *   Screenshots are attached to the PR.
*   **Review checklist (PR-2):** no `data-dolly-exit` in the last viewport-height of the page.
*   **Contrast (PR-2 at P2):** every token pairing passes WCAG AA, with the ratios recorded in `assets/site.css`.
*   **10-second check (PR-2 at P2):** G3's check passes.
*   **Reference page (PR-3):**
    *   The card grid and card markup are unchanged.
    *   There is no decorative motion.
    *   The maintainer can find any move by name in under 5 seconds, timed by the maintainer.
    *   The maintainer approves screenshots at 390, 768 and 1440px wide.

--------------------------------------------------------------------------------

<!-- Provenance: Indicates initial structural drafting via EGM. -->

*Drafted with EGM*
