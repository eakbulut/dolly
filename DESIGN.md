---
name: Dolly
description: Scroll animations in plain CSS, presented as a film's opening titles.
colors:
  accent: "#2B4BE8"
  block: "#D9A441"
  paper: "#F3EEE3"
  ink: "#141310"
  ink-soft: "#4F4A40"
  surface: "#E8E1D2"
  rule: "#CFC6B4"
  board: "#FFFFFF"
  code-attribute: "#FFE08A"
typography:
  display:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(40px, 1.6rem + 6vw, 96px)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "0.02em"
  headline:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(28px, 1.3rem + 2vw, 44px)"
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: "0.16em"
  title:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(28px, 1.3rem + 2vw, 44px)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.02em"
  subtitle:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(19px, 1rem + .6vw, 23px)"
    fontWeight: 400
    lineHeight: 1.4
  body:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(17px, .95rem + .3vw, 19px)"
    fontWeight: 400
    lineHeight: 1.55
  small:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(14px, .8rem + .2vw, 15.5px)"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "12px"
    fontWeight: 500
    letterSpacing: "0.14em"
  code:
    fontFamily: "Azeret Mono, Azeret Mono Fallback, ui-monospace, monospace"
    fontSize: "clamp(14px, .8rem + .2vw, 15.5px)"
    fontWeight: 400
    lineHeight: 1.7
rounded:
  none: "0px"
spacing:
  gutter: "clamp(20px, 4vw, 56px)"
  stack-sm: "22px"
  stack-md: "34px"
  stack-lg: "44px"
  container: "1180px"
components:
  title-card:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.board}"
    typography: "{typography.display}"
  slate:
    textColor: "{colors.board}"
    rounded: "{rounded.none}"
    padding: "16px 22px"
  install-command:
    backgroundColor: "{colors.board}"
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "10px 16px"
  install-command-on-block:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.board}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "10px 16px"
  letter-board:
    backgroundColor: "{colors.board}"
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.none}"
    padding: ".35em .9em .3em"
  code-well:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "22px"
  stage-panel:
    backgroundColor: "{colors.block}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    padding: "28px"
  inline-code:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    padding: ".1em .35em"
---

# Design System: Dolly

## Overview

**Creative North Star: "The Opening Titles"**

Dolly's homepage is a film's opening title sequence, shot front-on and symmetrical, that happens to be a CSS library's install page. Every composition is planimetric: one centre axis, flat colour fields filling the frame, and type set the way a title designer sets credits, in tracked uppercase Jost where weight, not colour, carries emphasis. The film lineage is the product's binding idea (moves are named for camera moves), so the visual world takes its devices from cinema print: the title card, the cinema letter board, the poster billing block, the framed shot, the runtime line.

Density is low and theatrical. A section is a chapter: a letter-board title, one short paragraph, one framed exhibit. Materials are flat paper, ink and two fields of colour; nothing is lit, blurred, lifted or glossed. Motion is the page's proof and is held to a written, test-enforced budget: the title card leaves on the first scroll like an opening sequence, chapter titles arrive word by word, and everything stays readable with motion off.

**Key Characteristics:**
- Full-bleed flat fields of brand blue and muted ochre on warm paper and near-black ink.
- Centred, symmetrical compositions on one axis; tableaux balanced left and right of a larger centre frame.
- Uppercase, generously tracked Jost for titles and labels; Azeret Mono only for code.
- Square corners everywhere; 1.5px ink rules and frames; no shadows, glass or tonal gradients.
- Motion only through Dolly's own `data-dolly` and `data-dolly-exit` attributes, inside the homepage motion budget.

## Colors

A two-field poster palette: one strong blue, one muted ochre, warm paper, and near-black ink, with contrast pairs recorded at the token source (`assets/site.css`).

### Primary
- **Title-Card Blue** (accent): the one strong colour. Fills the masthead and the full-height title card, colours links on hover, selection, caret and focus rings on paper, and fills the blue shot frames. White and paper text sit on it (6.0:1 and 5.4:1).

### Secondary
- **Projector Ochre** (block): a muted ochre for flat panels only: the stage panel beside the snippet, ochre shot frames, and the full-width tickets field. Ink on ochre is 9.5:1. Never used for text or rules.

### Tertiary
- **Attribute Gold** (code-attribute): highlights the `data-dolly` attribute inside dark or blue code (the slate and code wells). Its sibling, a pale periwinkle (`#A9B9FF`), marks tag names in the dark code well only.

### Neutral
- **House Paper** (paper): the page background and the subtitle colour on blue.
- **Projection Ink** (ink): body text, frames, rules, letter-board capitals, the dark code well and the inverted install command on ochre (17.0:1 on paper).
- **Faded Ink** (ink-soft): secondary prose, captions, footer, the `$` prompt (8.1:1 on paper).
- **Code Well Linen** (surface): background of inline code on paper.
- **Groove Grey** (rule): the letter board's ruled grooves.
- **Board White** (board): the letter board face, white shot frames, and the install command on blue.

### Named Rules
**The Two Fields Rule.** Colour arrives as whole flat fields (a section, a frame, a panel), never as tints, washes or gradients. Blue is the title card and the accent; ochre is a panel; everything else is paper and ink.

**The Ochre Is A Surface Rule.** Ochre fills panels and frames. It never colours text, links or rules.

## Typography

**Display Font:** Jost (with a metric-matched Futura/Arial fallback)
**Body Font:** Jost (same family)
**Label/Mono Font:** Azeret Mono (with a metric-matched Courier New fallback), for code only

**Character:** One geometric sans set three ways: heavy tracked capitals for title cards, mid-weight wide-tracked capitals for letter boards and labels, and plain sentence-case text for prose. The mono is strictly functional.

Fonts are self-hosted Latin subsets at fixed weights (Jost 400, 500, 700; Azeret Mono 400, 500). Fallback faces carry `size-adjust` and ascent/descent overrides so nothing reflows when the web fonts arrive; keep that property when adding a weight.

### Hierarchy
- **Display** (700, 40px to 96px fluid, line-height 0.98, 0.02em, uppercase, max 12ch, balanced): the title-card claim only.
- **Headline** (500, 28px to 44px fluid, line-height 1.25, 0.16em, uppercase): chapter titles on the letter board.
- **Title** (700, 28px to 44px fluid, uppercase): big set pieces inside exhibits, such as the stage-panel line and runtime figures (tabular numerals).
- **Subtitle** (400, 19px to 23px fluid, line-height 1.4, max 34ch): the one deadpan line under the claim.
- **Body** (400, 17px to 19px fluid, line-height 1.55, max 58ch): chapter paragraphs.
- **Small** (400, 14px to 15.5px fluid): captions, install lines, footer, link rows.
- **Label** (500, 12px, 0.14em, uppercase): masthead and link-row navigation.
- **Code** (Azeret Mono 400, small size, line-height 1.7, ligatures off): slates, code wells, install commands, inline code at 0.88em.

### Named Rules
**The Weight Not Colour Rule.** Emphasis in titles and credits is a weight step (400, 500, 700) and tracking, never a colour change. Colour in type is reserved for code syntax; the billing block's paler role words are the one tonal step, as on a poster.

**The Mono Is Code Rule.** Azeret Mono appears only on code: commands, snippets, attribute names and the CDN URL. Never for labels, numbers or decoration.

## Layout

A single centred axis. Content sits in a 1180px container with a fluid gutter (20px to 56px); exhibits narrow further (820px to 900px) and centre. Text is centre-aligned for titles and chapter prose; code, captions and figure content align left inside their frames.

The title card is a full-height (`100svh`) blue field stacked in two layers, the claim and the billing block, so a short phone or 200% zoom grows the card instead of overlapping them. Chapters open with generous viewport-relative top padding (80px to 150px). Vertical rhythm between parts of a chapter uses three recurring steps (22px, 34px, 44px); these are repeated literals in the page CSS, not custom properties.

Grids are symmetrical: the snippet and its stage panel side by side (1:1); the "now showing" tableau as 1 : 1.6 : 1 with the largest frame in the centre spanning both rows; the diptych and runtime table as halves. Breakpoints: at 760px the pair and tableau collapse (the tableau to the centre frame on top, then pairs); at 620px the diptych stacks, and the masthead drops its left links and moves the wordmark left.

**The Centre Axis Rule.** Every section composes on the vertical centreline; asymmetric layouts are outside this world.

## Elevation & Depth

Completely flat. There are no shadows, no blur, no backdrop filters and no blend modes; the homepage motion test fails the build on `filter`, `backdrop-filter` and `mix-blend-mode`. Depth comes from colour fields abutting, from 1.5px ink frames around shots, and from the letter board's white face set against paper.

**The Flat Print Rule.** Surfaces never lift. If something needs to separate, frame it with a rule or set it on a different flat field.

**The Grooves Exception.** Tonal and decorative gradients are out, but the letter board's grooves are a hard-stop `repeating-linear-gradient` of the rule colour, painted once as a static background. That is the board's native material and the only gradient in the system.

## Shapes

Square corners throughout (0px): frames, slates, boards, commands, panels and code wells. Lines are 1.5px solid ink for frames, boards, and the runtime table; the billing block's top rule is a 1px translucent white hairline on blue, and the slate is a 1.5px white frame on blue. The only curve is a prop inside a shot frame (a disc), which is an exhibit, not a container. Overflowing frames clip (`overflow: clip`), never `hidden`.

## Components

### Masthead
- **Character:** a symmetrical credit line across the top of the blue field.
- **Style:** absolute over the title card, blue, 64px tall, three-column grid: links left, wordmark centred, links right. Links are white Label caps, underlined on hover.
- **Wordmark:** Jost 700, 15px, 0.32em tracking, uppercase, with matching left padding so the tracked word is optically centred.
- **Mobile (620px and below):** left links hidden, wordmark left, right links kept. The footer and tickets link row repeat every link.

### Title Card (signature)
- **Character:** the opening title of the film.
- **Style:** full-height blue field, white Display claim, paper-coloured Subtitle, then the slate, then the install lines, then the billing block at the foot.
- **Motion:** the claim layer leaves with `data-dolly-exit="tilt-up"` and the billing layer with `data-dolly-exit="dolly-in"`. The install line also exists in the tickets section, which never exits.

### Slate
- **Character:** the one line of code that is the whole integration, framed like a clapperboard.
- **Style:** 1.5px white frame on blue, 16px by 22px padding, mono at 12px to 17px fluid, no wrap with horizontal scroll, the attribute in Attribute Gold.

### Install Command
- **Style:** a square mono chip, 10px by 16px. White with ink text on blue; inverted (ink with white text) on the ochre tickets field. The `$` prompt is Faded Ink, aria-hidden and unselectable; the command itself is select-all.
- **Companion:** the CDN line in Small text beneath, URL in mono 12px with break points after each slash.

### Billing Block (signature)
- **Character:** a poster one-sheet's credits.
- **Style:** a definition list of run-on credit pairs, centred and balanced under a 1px translucent white hairline. Role words are small (11px), regular weight, 0.06em tracking in pale blue (`#D9E0FF`); names are 700 at 14px to 17px with slightly tight tracking (-0.01em). The final promise breaks onto its own line in sentence case at 500.

### Letter Board (signature)
- **Character:** black capitals pushed into a white ribbed cinema board.
- **Style:** inline block, Board White face, 1.5px ink border, Headline type, grooves every 1.25em in Groove Grey.
- **Motion:** each word is its own span with `data-dolly="tilt-up"` under `data-dolly-stagger`, so chapter titles arrive word by word.

### Shot Frame
- **Style:** 4:3 frame with a 1.5px ink border, filled with one flat field (blue, ochre, ink or white), holding a single geometric prop that performs one named move. Caption below in Small Faded Ink with the move name in ink mono.

### Code Well and Stage Panel
- **Code well:** ink background, paper-coloured mono at line-height 1.7, 22px padding, wraps; tags in periwinkle, attributes in Attribute Gold.
- **Stage panel:** flat ochre, 28px padding, min 180px, holding a centred Title line that performs the snippet's move.

### Runtime Table
- **Style:** two cells between 1.5px ink rules top and bottom, divided by a 1.5px vertical rule; Title figures in tabular numerals over a Small Faded Ink caption. Enters with the page's single `reveal`.

### Links
- Inherit colour, 1px underline offset 0.22em; on paper they turn blue on hover; on ochre they thicken to 2px instead. Focus is a 2px accent outline offset 3px, white on the blue masthead and title card.

### Motion
Motion comes only from `src/dolly.css` through attributes, never page CSS. The budget is enforced by the test "the homepage stays inside its motion budget" in `test/moves.test.mjs`:
- Anywhere, including the title card: `fade`, `tilt-up`, `tilt-down`, `pan-left`, `pan-right`, `dolly-in`, `dolly-out`, `crane`, `roll`, `progress`, `travel`; exits from the same list minus `progress` and `travel`.
- Below the title card only: the repaint moves `reveal`, `wipe-up`, `iris`, `draw`, `count`, `mask`, and the exits `reveal` and `wipe-up`.
- Never: `data-dolly-scene`, `data-dolly-pin`, `data-dolly-depth`; one element carrying both a move and an exit; a scroll-driven animation on `:root`; page CSS that hides `[data-dolly]` elements with `opacity: 0`, `visibility: hidden` or `clip-path`.

**The Fails Visible Rule.** The page at rest with motion off must look like the finished page. Hidden states live inside Dolly's animations, never in page CSS.

## Do's and Don'ts

### Do:
- **Do** compose every section on the centre axis, with titles on a letter board and exhibits in square ink frames.
- **Do** fill colour as whole flat fields: blue for the title card and accent, ochre for panels, paper and ink for the rest.
- **Do** set titles and labels in uppercase tracked Jost and move emphasis with weight (400, 500, 700).
- **Do** keep Azeret Mono for code and ship each new weight with a metric-matched fallback face.
- **Do** animate only with `data-dolly` and `data-dolly-exit`, inside the motion budget, and keep the install line somewhere that never exits.

### Don't:
- **Don't** add shadows, blur, glass, blend modes or tonal gradients; the letter-board grooves are the only gradient.
- **Don't** round corners on frames, slates, boards, commands or panels.
- **Don't** use ochre for text, links or rules.
- **Don't** pin scenes, use depth layers, or put repaint moves in the title card.
- **Don't** hide `[data-dolly]` elements in page CSS or use `overflow: hidden` (use `clip`).
