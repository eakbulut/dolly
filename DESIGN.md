---
name: Dolly
description: Scroll animations in plain CSS, shown as a screening in a dark auditorium.
colors:
  cinema: "#0B0A09"
  paper: "#F3EEE3"
  house-lights: "#CFC7B7"
  usher: "#BDB5A5"
  exit-sign: "#A39B8B"
  aisle-dim: "#8F8778"
  screen-ink: "#1B1A17"
  screen-ink-soft: "#2A2824"
  booth: "#17150F"
  booth-inline: "#24211D"
  booth-edge: "#2E2A24"
  row-rule: "#3A362F"
  code-text: "#EDE8DC"
  code-attribute: "#FFE08A"
  code-tag: "#A9B9FF"
  ink: "#141310"
  ink-soft: "#4F4A40"
  accent: "#2B4BE8"
  surface: "#E8E1D2"
  rule: "#CFC6B4"
typography:
  display:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "min(4.4cqi, 10.5vw)"
    fontWeight: 700
    lineHeight: 0.96
    letterSpacing: "0.02em"
  marquee:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(40px, 1.6rem + 6vw, 96px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.03em"
  headline:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(28px, 1.3rem + 2vw, 44px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.03em"
  subtitle:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(19px, 1rem + .6vw, 23px)"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(17px, .95rem + .3vw, 19px)"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(14px, .8rem + .2vw, 15.5px)"
    fontWeight: 400
  label:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "12px"
    fontWeight: 500
    letterSpacing: "0.14em"
  screen-line:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "max(11px, min(.9cqi, 3vw))"
    fontWeight: 400
    letterSpacing: "0.2em"
  credit-role:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.08em"
  credit-name:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(13px, 1.1vw, 16px)"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0"
  code:
    fontFamily: "Azeret Mono, Azeret Mono Fallback, ui-monospace, monospace"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.7
  reference-title:
    fontFamily: "Jost, Jost Fallback, sans-serif"
    fontSize: "clamp(28px, 1.3rem + 2vw, 44px)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  reference-label:
    fontFamily: "Azeret Mono, Azeret Mono Fallback, ui-monospace, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "0.02em"
rounded:
  none: "0px"
  plate: "5px"
  chip: "6px"
  well: "8px"
  card: "12px"
spacing:
  gutter: "clamp(20px, 4vw, 56px)"
  stack-sm: "22px"
  stack-md: "30px"
  stack-lg: "44px"
  container: "1180px"
  reference-container: "1320px"
components:
  install-command:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "10px 16px"
  slate:
    textColor: "{colors.paper}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "10px 16px"
  code-well:
    backgroundColor: "{colors.booth}"
    textColor: "{colors.code-text}"
    typography: "{typography.code}"
    rounded: "{rounded.none}"
    padding: "20px"
  inline-code:
    backgroundColor: "{colors.booth-inline}"
    textColor: "{colors.paper}"
    padding: ".1em .35em"
  still:
    backgroundColor: "{colors.booth}"
    rounded: "{rounded.none}"
  demo-frame:
    rounded: "{rounded.none}"
    padding: "26px"
  reference-card:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "clamp(14px, 1.4vw, 20px)"
  reference-stage:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.well}"
    height: "132px"
  reference-snippet:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.reference-label}"
    rounded: "{rounded.chip}"
    padding: "7px 9px"
---

# Design System: Dolly

## Overview

**Creative North Star: "The Screening"**

The homepage is an evening in an empty cinema. The first screen is a full-bleed photograph of an auditorium facing a blank screen, and the claim is projected onto that screen in dark capitals over a soft wash of projected light; the line, the install command and the poster credits sit below in the dark seats in paper-coloured type. From there the page walks through the building in real photographs (seat 23, a full audience, the aisle, the red house, reels, popcorn, the projector, the box office), each still performing one named camera move. The film lineage is the product's binding idea, since every move is named for what a camera does, so the world is the place films are shown rather than a graphic pastiche of film titles.

Density is low and theatrical: a chapter is a capitalised title, one short paragraph in house-light grey, and one exhibit (a seat photograph beside the code, a tableau of stills, a diptych, a running-time table). The ground is near-black, type is warm paper, and colour arrives only through the photographs' own reds and golds. Motion is the page's proof and is held to a test-enforced budget; with motion off the page is the finished page.

The site has two registers on one set of tokens. The homepage is the dark screening. The generated moves page is the calm, light reference: paper ground, ink type, white cards on a three-column grid, one blue accent. It answers "which move do I want?" and deliberately does not perform.

**Key Characteristics:**
- Near-black auditorium ground with warm paper type; colour comes from photographs, not fills.
- Real, self-hosted photographs of a cinema, full-bleed or in square-cornered stills.
- Uppercase tracked Jost for titles, credits and navigation; Azeret Mono only for code.
- Flat surfaces; depth is photographic, plus dark scrims and one projected-light wash where type sits on a picture.
- Motion only through `data-dolly` and `data-dolly-exit`, timed to play at eye level, inside the homepage motion budget.

## Colors

A dark-house palette: one near-black ground, warm paper type stepped down through four dimmer greys, a few warm near-blacks for code and frames, and a light paper set kept for the reference page. The custom properties live in `assets/site.css`; the dark-house greys and booth tones are repeated literals in the homepage's own stylesheet.

### Primary
- **Projected Paper** (paper): the homepage's type colour, focus ring, link underline at full strength, selection fill, the install command's face, and the moves page's ground (17.1:1 on the cinema ground).

### Secondary
- **Signal Blue** (accent): the reference page's single accent: demo plates and bars, the wordmark's full stop, nav hover. It does not appear on the homepage outside the favicon.

### Tertiary
- **Attribute Gold** (code-attribute): the `data-dolly` attribute in the slate and the code well (14.2:1 on the booth).
- **Tag Periwinkle** (code-tag): tag names in the code well only (9.6:1).

### Neutral
- **Auditorium Black** (cinema): the homepage ground behind every photograph and section; also the tint of every scrim.
- **House Lights** (house-lights): chapter paragraphs, captions, the CDN line, runtime captions (11.8:1).
- **Usher Grey** (usher): credit role words and the footer text (9.7:1).
- **Exit-Sign Grey** (exit-sign): footnotes under an exhibit (7.2:1).
- **Aisle Dim** (aisle-dim): the photo credit line, the dimmest text allowed (5.6:1).
- **Screen Ink** (screen-ink) and **Screen Ink Soft** (screen-ink-soft): the claim and its line, set dark on the lit cinema screen.
- **Booth** (booth): code-well ground and the placeholder behind stills while they load. **Booth Inline** (booth-inline) backs inline code in paragraphs. **Booth Edge** (booth-edge) is the 1px edge of the code well and demo frame. **Row Rule** (row-rule) draws the running-time table.
- **Code Text** (code-text): plain text in the code well.
- **Ink** (ink), **Faded Ink** (ink-soft), **Linen** (surface), **Groove Grey** (rule): the reference page's text, secondary text, demo stages and snippet chips, and hairline dividers. Ink is also the text on the homepage's paper install command.

### Named Rules
**The Photographs Carry Colour Rule.** The homepage has no flat colour fields and no accent hue. Red seats, gold lights and the lit screen supply the colour; the interface stays black and paper.

**The House Lights Rule.** Text dims in fixed steps (paper, house lights, usher, exit sign, aisle dim) and never below Aisle Dim's 5.6:1 on the cinema ground.

## Typography

**Display Font:** Jost (metric-matched Futura/Arial fallback)
**Body Font:** Jost
**Label/Mono Font:** Azeret Mono (metric-matched Courier New fallback), code only on the homepage

**Character:** One geometric sans set as cinema signage: heavy capitals for titles, small tracked capitals for credits and navigation, plain sentence case for prose. The mono is the projector's technical voice: commands, snippets, move names.

Fonts are self-hosted Latin subsets at fixed weights (Jost 400, 500, 700; Azeret Mono 400, 500). Fallback faces carry `size-adjust` and ascent/descent overrides so nothing reflows when the web fonts arrive; keep that when adding a weight.

### Hierarchy
- **Display** (700, scaled to the photograph's width, line-height 0.96, 0.02em, uppercase, max 13ch, balanced): the claim on the cinema screen only. It is sized in container units of the photograph so it always fits the screen in the picture.
- **Screen Line** (400, tiny fluid with an 11px floor, 0.2em, uppercase): the one line under the claim on the screen.
- **Marquee** (700, 40px to 96px fluid, line-height 1, 0.03em, uppercase): the box-office title.
- **Headline** (700, 28px to 44px fluid, line-height 1, 0.03em, uppercase): chapter titles, and the big line inside the demo frame.
- **Subtitle** (400, 19px to 23px fluid, line-height 1.45, max 42ch): the line under the screen and the box-office line.
- **Body** (400, 17px to 19px fluid, line-height 1.6, max 52ch in chapters).
- **Small** (400, 14px to 15.5px fluid): captions, CDN line, link rows, footer.
- **Label** (500, 12px, 0.14em, uppercase): masthead and link-row navigation.
- **Credits** (role 400 at 11px, 0.08em, Usher Grey; name 700 at 13px to 16px, no tracking): the poster billing block, all uppercase except the final promise, which drops to sentence case at 500.
- **Code** (Azeret Mono 400, ligatures off): 15px in the slate and install command (13px slate on phones), small size at line-height 1.7 in the code well, 0.88em inline.
- **Reference Title** and **Reference Label** (moves page): sentence-case 700 with tight -0.03em tracking, and mono 12px labels, nav and card names.

### Named Rules
**The Signage Rule.** On the homepage, titles, credits and navigation are uppercase Jost; emphasis is a weight step (400, 500, 700), never a colour.

**The Mono Is Code Rule.** On the homepage, Azeret Mono appears only on code: commands, snippets, attribute and move names, and the CDN URL.

## Layout

The first screen is a stage that keeps the auditorium photograph's own proportions (2400 by 1584) and is scaled to cover the window, so a position given in percent of the stage is a position in the picture: the claim block is pinned to the screen's measured rectangle (x 21.4% to 74%, y 18.8% to 52.4%) at any window shape. The credits sit at the foot of a `100svh` section over the seats. At 620px and below the stage is one screen tall, a spacer pushes the credits below the picture's screen, and the section grows if it must.

Below the screen, content sits in a 1180px container with a fluid gutter (20px to 56px), left-aligned. Chapters open with viewport-relative top padding (90px to 170px). Rhythm between parts of a chapter is a short set of repeated literals (22px after a title, about 30px before an exhibit, 40px to 44px before a grid). Exhibits: the seat photograph and the integration side by side (1:1, the photo at 4:5); the "now showing" tableau as 1 : 1.25 : 1 with the tall red-house still in the centre spanning both rows; the diptych and the running-time table as halves. The box office is a full-bleed photograph with a centred block over it. At 760px the seat pair stacks (photo to 4:3) and the tableau becomes the centre still on top, then pairs; at 620px the diptych stacks and the masthead drops its left links.

The moves page uses a 1320px container, a sticky header, a four-column index of every move, and an explicit card grid (3 columns, 2 at 1000px, 1 at 620px); never auto-fit.

**The Screen Is A Place Rule.** Type placed on a photograph is positioned in the photograph's coordinates, not the viewport's, so it stays on the object it belongs to.

## Elevation & Depth

The homepage is flat: no shadows, no blur, no backdrop filters, no blend modes (the motion-budget test fails the build on `filter`, `backdrop-filter` and `mix-blend-mode`). Depth is photographic. Where type sits on a picture, legibility comes from a gradient or flat scrim tinted with Auditorium Black (the stage's vertical scrim, 30% at the top, clear through the middle, 88% under the credits; a flat 72% over the box office) and, on the cinema screen, a radial wash of warm projected light behind the claim. The moves page has exactly one shadow: a faint, soft two-layer lift on its white cards.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 1px 2px rgba(11,11,12,.04), 0 12px 28px -22px rgba(11,11,12,.5)`): moves-page cards only.

### Named Rules
**The Scrim Not Shadow Rule.** On the homepage, nothing lifts. When type has to read over a photograph, darken the photograph with a cinema-tinted scrim, or light the screen with the projector wash; never a box behind the text.

## Shapes

On the homepage every container has square corners (0px): stills, the seat photograph, slate, install command, code well, demo frame. Lines are 1px: a translucent paper hairline frames the slate and tops the credits, Booth Edge frames the code well and demo frame, and Row Rule draws the running-time table. Overflowing frames clip (`overflow: clip`), never `hidden`. The moves page is softer by design: 12px cards, 8px stages and outro command, 6px snippet chips, 5px demo plates, pill bars, and a dashed frame where a subject has left the stage.

## Components

### Masthead
- **Character:** the house's sign over the seats.
- **Style:** absolute over the first screen, transparent, 64px tall, three-column grid: links left, wordmark centred, links right. Links are paper Label caps, underlined on hover.
- **Wordmark:** Jost 700, 15px, 0.32em tracking, uppercase, with matching left padding so the tracked word is optically centred. It repeats in the footer.
- **Mobile (620px and below):** left links hidden, wordmark left. The box-office link row and footer repeat every link.

### On-Screen Claim (signature)
- **Character:** the title projected on the cinema screen.
- **Style:** Display claim and Screen Line in Screen Ink, centred inside the screen's rectangle, over a radial wash of warm light (about 62% opaque at the centre, clear at the edges).
- **Motion:** leaves with `data-dolly-exit="fade"` on an early exit range (`exit -18vh exit 45%`) so the screen switches off while it is in view.

### Credits Over The Seats (signature)
- **Character:** the poster's billing under the screen.
- **Style:** a centred stack: Subtitle line, then the slate and install command side by side, the CDN line, then the billing block: a definition list of run-on role and name pairs under a 1px translucent paper hairline, ending with the promise on its own line.
- **Motion:** the whole stack leaves with `data-dolly-exit="tilt-up"` on an early range (`exit -48vh exit 35%`). The install line also exists at the box office, which never exits.

### Slate and Install Command
- **Slate:** the one line of code that is the integration, mono 15px in paper, framed by a 1px translucent paper line, no wrap, attribute in Attribute Gold.
- **Install command:** a square paper chip with ink mono text, 10px by 16px. The `$` prompt is Faded Ink, aria-hidden and unselectable; the command is select-all. The CDN URL beneath is mono 12px with break points after each slash.

### Still (signature)
- **Style:** a square-cornered photograph in a clipped frame (4:3 in the tableau, 3:2 in the diptych, Booth behind it), with a Small House Lights caption below naming the move in paper mono. The photograph itself carries the move.

### Code Well and Demo Frame
- **Code well:** Booth ground, 1px Booth Edge, Code Text mono at line-height 1.7, 20px padding, wraps; tags in Tag Periwinkle, attributes in Attribute Gold.
- **Demo frame:** 1px Booth Edge, 26px padding, min 200px, clipped, holding one Headline line that performs the snippet's move.

### Running-Time Table
- **Style:** two cells between 1px Row Rule lines, divided by a vertical rule; Headline-size figures in tabular numerals over a Small House Lights caption. Enters with the page's single `reveal`.

### Box Office
- **Style:** full-bleed photograph under a flat 72% cinema scrim, centred Marquee title, Subtitle line, install command, CDN line and a Label link row.

### Links
- Inherit colour with a 1px underline at 45% paper, offset 0.22em; on hover the underline goes full paper. Focus is a 2px paper outline offset 3px.

### Reference Card (moves page)
- **Style:** white card, 1px Groove Grey border, 12px corners, card lift, holding a 132px Linen stage where the move plays, a mono name with its cost tag, a two-line reserved description in Faded Ink, and a select-all snippet chip pinned to the bottom.

### Motion
Motion comes only from `src/dolly.css` through attributes, never page CSS. Entrances below the first screen run on `--dolly-range: cover 30% cover 70%`, symmetric about the moment an element's centre crosses the viewport's centre, so a move is half-played at eye level (the same timing as the moves-page cards). The budget is enforced by the test "the homepage stays inside its motion budget" in `test/moves.test.mjs`:
- Anywhere, including the first screen: `fade`, `tilt-up`, `tilt-down`, `pan-left`, `pan-right`, `dolly-in`, `dolly-out`, `crane`, `roll`, `progress`, `travel`; exits from the same list minus `progress` and `travel`.
- Below the first screen only: the repaint moves `reveal`, `wipe-up`, `iris`, `draw`, `count`, `mask`, and the exits `reveal` and `wipe-up`.
- Never: `data-dolly-scene`, `data-dolly-pin`, `data-dolly-depth`; one element carrying both a move and an exit; a scroll-driven animation on `:root`; page CSS that hides `[data-dolly]` elements with `opacity: 0`, `visibility: hidden` or `clip-path`; fonts or photographs fetched from a third party.

**The Fails Visible Rule.** The page at rest with motion off must look like the finished page. Hidden states live inside Dolly's animations, never in page CSS.

**The Early Exit Rule.** An exit on a tall layer starts early through exit offsets only (never earlier than scroll 0), so the reader sees it leave.

## Do's and Don'ts

### Do:
- **Do** set the homepage on Auditorium Black with paper type, and dim secondary text only through the House Lights steps.
- **Do** use real, self-hosted cinema photographs, square-cornered and clipped, each still performing one named move.
- **Do** darken a photograph with a cinema-tinted scrim, or light it with the projector wash, wherever type sits on it.
- **Do** set titles, credits and navigation in uppercase Jost and move emphasis with weight (400, 500, 700); keep Azeret Mono for code.
- **Do** animate only with `data-dolly` and `data-dolly-exit`, inside the motion budget, on the eye-level range, and keep an install line somewhere that never exits.

### Don't:
- **Don't** add flat colour fields or an accent hue to the homepage; Signal Blue belongs to the reference page.
- **Don't** add shadows, blur, glass or blend modes to the homepage; the card lift is the moves page's only shadow.
- **Don't** round homepage containers; rounded corners are the reference page's register.
- **Don't** hotlink photographs or fonts, pin scenes, use depth layers, or put repaint moves on the first screen.
- **Don't** hide `[data-dolly]` elements in page CSS or use `overflow: hidden` (use `clip`).
