# -*- coding: utf-8 -*-
"""Regenerate moves.html — the reference page — from src/dolly.css.

    python3 scripts/build-moves.py

moves.html is GENERATED. Edit this script or scripts/moves-head.html (the
shell and all the CSS), never the output. The move list is read from the
stylesheet, so a move added to the CSS and to no group here aborts the build
rather than quietly going undocumented.
"""
import re, json, os, sys

css = open('src/dolly.css', encoding='utf-8').read()
nocom = re.sub(r'/\*[\s\S]*?\*/', '', css)
order, seen, anims = [], set(), {}
for m in re.finditer(r'\[data-dolly="([^"]+)"\]([^{]*)\{([^}]*)\}', nocom):
    n = m.group(1)
    if 'animation-name' in m.group(3) and n not in seen:
        seen.add(n); order.append(n)
        anims[n] = re.search(r'animation-name\s*:\s*([^;]+)', m.group(3)).group(1)

# Exits get their own list and map. Their names repeat the entrance names on
# purpose, so folding them into GROUPS would trip the duplicate check below.
exit_order, exit_anims = [], {}
for m in re.finditer(r'\[data-dolly-exit="([^"]+)"\]([^{]*)\{([^}]*)\}', nocom):
    n = m.group(1)
    if 'animation-name' in m.group(3) and n not in exit_anims:
        exit_order.append(n)
        exit_anims[n] = re.search(r'animation-name\s*:\s*([^;]+)', m.group(3)).group(1)

# Anything a move's keyframes animate beyond these runs on the main thread and
# repaints every frame. The cards tag those moves, read from the CSS so the
# tag cannot drift from what actually ships.
COMPOSITED = {'opacity', 'transform', 'translate', 'scale', 'rotate'}
keyframe_props = {
    m.group(1): set(re.findall(r'([a-z-]+)\s*:', m.group(2))) - COMPOSITED
    for m in re.finditer(r'@keyframes\s+([\w-]+)\s*\{((?:[^{}]*\{[^{}]*\})*[^{}]*)\}', nocom)}

def repaints(n, amap=anims):
    props = set().union(*(keyframe_props.get(a.strip(), set()) for a in amap[n].split(',')))
    return sorted({'counter' if p.startswith('--') else re.sub(r'-[xy]$', '', p) for p in props})

PLATE = '<div class="plate" data-dolly="{n}"></div>'
CLIP  = '<div class="clip"><div class="plate tall" data-dolly="{n}"></div></div>'
SPACE = '<div class="space" data-dolly-space><div class="plate" data-dolly="{n}"></div></div>'

SUBJECT = {
  'progress': '<div class="bar"><i data-dolly="progress"></i></div>',
  'travel':   '<div class="rail"><i data-dolly="travel"></i></div>',
  'parallax': CLIP, 'zoom': CLIP,
  'track':    '<div class="clip"><div class="row" data-dolly="track">'
              + ''.join('<span></span>' for _ in range(7)) + '</div></div>',
  'mask':     '<p class="masked" data-dolly="mask">MASK</p>',
  'letter':   '<p class="letters" data-dolly="letter">letter</p>',
  'sequence': '<div class="sheet" data-dolly="sequence" role="img"'
              ' aria-label="A countdown leader"'
              ' style="--dolly-cols:12;--dolly-rows:3"></div>',
  'draw':     '<svg class="scribble" viewBox="0 0 200 80" fill="none" aria-hidden="true">'
              '<path data-dolly="draw" pathLength="1" stroke="currentColor"'
              ' stroke-width="6" stroke-linecap="round"'
              ' d="M14 58C30 20 46 18 62 46s28 32 44 8 26-26 40-12"/></svg>',
  'count':    '<p class="tally"><span data-dolly="count" role="img" aria-label="240"'
              ' style="--dolly-count-to:240"></span></p>',
}
for n in ('drop','pass','push','pull','swing','tumble','fly'):
    SUBJECT[n] = SPACE
for n in ('iris','beat','beat-in','hold'):
    SUBJECT[n] = PLATE

DESC = {
 'fade':'Fades up from nothing.','tilt-up':'Rises 2.5rem into place.',
 'tilt-down':'Drops 2.5rem into place.','pan-left':'Enters from the right, travelling left.',
 'pan-right':'Enters from the left, travelling right.','dolly-in':'Pushes in from 0.9 scale.',
 'dolly-out':'Settles back from 1.1 scale.','crane':'Rises 5rem with a slight scale. The big arrival.',
 'rack':'Rack focus: a 14px blur clearing.','whip':'Whip pan: lateral travel plus blur.',
 'reveal':'Clip wipe, left edge to right.','wipe-up':'Clip wipe, bottom edge upward.',
 'roll':'Rotates -5deg to level.',
 'progress':'Scales a bar from 0 to 1 across the document.',
 'travel':'Rides the document scroll along its own track.',
 'parallax':'Drifts vertically against the scroll.','zoom':'Ken Burns: a slow push in.',
 'drop':'Falls through the frame, pitching as it goes.',
 'pass':'Tracks laterally, reversing its yaw as it crosses.',
 'push':'The camera travels toward it.','pull':'The camera draws back from it.',
 'swing':'Rotates in from the side on Y.','tumble':'Pitches in from above on X.',
 'fly':'Travels from far, past the camera.',
 'beat':'Rises in, holds, leaves upward.','beat-in':'Arrives out of blur and scale, holds, leaves.',
 'hold':'Arrives and stays.','iris':'The aperture opening: a circle clip growing.',
 'track':'Vertical scroll driving horizontal travel.',
 'mask':'Pushes a picture inside letterforms.',
 'letter':'Letter-spacing tightens from loose to tight.',
 'sequence':'Steps through a sprite sheet, one cell per slice of scroll.',
 'draw':'A stroke draws itself along its own path.',
 'count':'A number counts up as it scrolls into place.',
}

EXIT_DESC = {
 'fade':'Fades out.','tilt-up':'Keeps rising 2.5rem as it goes.',
 'tilt-down':'Keeps sinking 2.5rem as it goes.','pan-left':'Keeps travelling left.',
 'pan-right':'Keeps travelling right.','dolly-in':'The camera pushes past it, to 1.1 scale.',
 'dolly-out':'The camera pulls away, to 0.9 scale.','crane':'Keeps craning up 5rem.',
 'roll':'Keeps rolling, to 5deg.','reveal':'Clip wipe off to the right.',
 'wipe-up':'Clip wipe off the top.','rack':'Focus pulls away into a 14px blur.',
 'whip':'Whips out to the left, with blur.',
}

GROUPS = [
 ('entrances','Entrances','Resolve once, as the element enters the viewport.',
  ['fade','tilt-up','tilt-down','pan-left','pan-right','dolly-in','dolly-out',
   'crane','rack','whip','reveal','wipe-up','roll']),
 ('continuous','Continuous','Run the whole time the element is on screen, or the whole page.',
  ['progress','travel','parallax','zoom']),
 ('beats','Beats','Enter, hold long enough to read, leave. Built for pinned scenes.',
  ['beat','beat-in','hold']),
 ('cinematic','Cinematic','The effects people usually install a JavaScript library for.',
  ['iris','track','mask','letter']),
 ('depth','Depth','Moves elements toward and away from the camera in 3D. Needs '
  '<code>data-dolly-space</code> on an ancestor.',
  ['push','pull','swing','tumble','fly','drop','pass']),
 ('data','Drawing and data','A sprite sheet, a pen line, and a number.',
  ['sequence','draw','count']),
]

listed = [n for g in GROUPS for n in g[3]]
missing = [n for n in order if n not in listed]
extra   = [n for n in listed if n not in order]
if missing or extra:
    sys.exit('ABORT: group coverage mismatch. missing=%s extra=%s' % (missing, extra))
if len(listed) != len(set(listed)):
    sys.exit('ABORT: a move is listed in two groups')
if set(exit_order) != set(EXIT_DESC):
    sys.exit('ABORT: exit coverage mismatch. missing=%s extra=%s' % (
        sorted(set(exit_order) - set(EXIT_DESC)), sorted(set(EXIT_DESC) - set(exit_order))))

LEAVES = {'beat', 'beat-in', 'fly', 'drop', 'pass'}

# The library's default, entry 0% -> cover 35%, is tuned for a page where a
# section owns the screen. This page is a dense grid: a card finishes moving
# while it is still in the bottom quarter, so by the time the reader's eye
# reaches it, it has been static for a third of a screen. These cards retime
# the move to land as the card arrives at eye level instead.
#
# Two groups keep their own range and must never be retimed:
#   - progress and travel read the page scroller; cover/entry phases are
#     meaningless there and would silently break them.
#   - parallax, zoom, track, fly, drop and pass are continuous or travel
#     straight through; their whole point is to run the full passage.
KEEP_OWN_RANGE = {'progress', 'travel', 'parallax', 'zoom', 'track',
                  'fly', 'drop', 'pass'}
SCRUB = {'sequence'}   # 36 cells need a longer window than a single gesture

unknown = (KEEP_OWN_RANGE | SCRUB) - set(order)
if unknown:
    sys.exit('ABORT: timing list names moves that do not ship: %s' % sorted(unknown))
if KEEP_OWN_RANGE & SCRUB:
    sys.exit('ABORT: a move is both retimed and left alone')

def timing(n):
    if n in KEEP_OWN_RANGE: return ''
    return ' scrub' if n in SCRUB else ' arrive'

def card(n):
    subj = SUBJECT.get(n, PLATE).format(n=n)
    cls = ('demo leaves' if n in LEAVES else 'demo') + timing(n)
    r = repaints(n)
    cost = f' <span class="cost">repaints · {", ".join(r)}</span>' if r else ''
    return (f'      <article class="card" id="{n}">\n'
            f'        <div class="{cls}">{subj}</div>\n'
            f'        <h3>{n}{cost}</h3>\n'
            f'        <p>{DESC[n]}</p>\n'
            f'        <code>data-dolly="{n}"</code>\n'
            f'      </article>')

# No arrive/scrub class: those retime [data-dolly] only. Exit cards get
# .exits, which moves-head.html retimes for this page (see the comment there).
def exit_card(n):
    r = repaints(n, exit_anims)
    cost = f' <span class="cost">repaints · {", ".join(r)}</span>' if r else ''
    return (f'      <article class="card" id="exit-{n}">\n'
            f'        <div class="demo leaves exits"><div class="plate" data-dolly-exit="{n}"></div></div>\n'
            f'        <h3>{n}{cost}</h3>\n'
            f'        <p>{EXIT_DESC[n]}</p>\n'
            f'        <code>data-dolly-exit="{n}"</code>\n'
            f'      </article>')

sections = []
for slug, title, blurb, names in GROUPS:
    sections.append(
      f'    <section id="{slug}">\n'
      f'      <header class="sec">\n'
      f'        <h2>{title}</h2>\n'
      f'        <p>{blurb}</p>\n'
      f'        <span class="label">{len(names)}</span>\n'
      f'      </header>\n'
      f'      <div class="grid">\n' + '\n'.join(card(n) for n in names) + '\n      </div>\n'
      f'    </section>')

sections.append(
  f'    <section id="exits">\n'
  f'      <header class="sec">\n'
  f'        <h2>Exits</h2>\n'
  f'        <p>The other half of an entrance: keep going as the element leaves. '
  f'Set with <code>data-dolly-exit</code>.</p>\n'
  f'        <span class="label">{len(exit_order)}</span>\n'
  f'      </header>\n'
  f'      <div class="grid">\n' + '\n'.join(exit_card(n) for n in exit_order) + '\n      </div>\n'
  f'    </section>')

# The index: every move and exit on one screen, name and cost, each linked
# to its card. Built from GROUPS and exit_order, so it cannot miss one.
# Only the moves that repaint get a label; the rest run on the compositor,
# which the lede already says, so a label on every row would be noise.
def cost(n, amap=anims):
    r = repaints(n, amap)
    if not r: return ''
    return 'repaints · ' + ('filter' if 'filter' in r else ', '.join(r))

def index_entry(n, href, amap=anims):
    c = cost(n, amap)
    return f'<li><a href="#{href}"><code>{n}</code></a>' + (f' <span>{c}</span>' if c else '') + '</li>'

index = []
for slug, title, _, names in GROUPS:
    index.append(f'      <div><h2>{title}</h2><ul>' + ''.join(index_entry(n, n) for n in names) + '</ul></div>')
index.append('      <div><h2>Exits</h2><ul>' + ''.join(index_entry(n, 'exit-' + n, exit_anims) for n in exit_order) + '</ul></div>')
index_html = '    <nav class="index" aria-label="Every move">\n' + '\n'.join(index) + '\n    </nav>'

nav = ' '.join(f'<a href="#{s}">{t}</a>' for s, t, _, _ in GROUPS) + ' <a href="#exits">Exits</a>'

HEAD = open(os.path.join(os.path.dirname(__file__), 'moves-head.html'), encoding='utf-8').read()
html = HEAD.replace('{{COUNT}}', str(len(order))) \
           .replace('{{EXITS}}', str(len(exit_order))) \
           .replace('{{NAV}}', nav) \
           .replace('{{INDEX}}', index_html) \
           .replace('{{SECTIONS}}', '\n'.join(sections))

tmp = 'moves.html.tmp'
open(tmp, 'w', encoding='utf-8').write(html)
os.replace(tmp, 'moves.html')
print('ok: %d moves across %d groups, %d exits' % (len(order), len(GROUPS), len(exit_order)))
