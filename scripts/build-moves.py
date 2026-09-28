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
order, seen = [], set()
for m in re.finditer(r'\[data-dolly="([^"]+)"\]([^{]*)\{([^}]*)\}', nocom):
    n = m.group(1)
    if 'animation-name' in m.group(3) and n not in seen:
        seen.add(n); order.append(n)

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

GROUPS = [
 ('entrances','Entrances','Resolve once, as the element enters the viewport.',
  ['fade','tilt-up','tilt-down','pan-left','pan-right','dolly-in','dolly-out',
   'crane','rack','whip','reveal','wipe-up','roll']),
 ('continuous','Continuous','Run the whole time the element is on screen, or the whole page.',
  ['progress','travel','parallax','zoom']),
 ('beats','Beats','Enter, hold long enough to read, leave. Built for pinned scenes.',
  ['beat','beat-in','hold']),
 ('cinematic','Cinematic','The three that usually cost a JavaScript library, plus one.',
  ['iris','track','mask','letter']),
 ('depth','Depth','Real Z translation under a perspective, not scale. Needs '
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

LEAVES = {'beat', 'beat-in', 'fly', 'drop', 'pass'}

def card(n):
    subj = SUBJECT.get(n, PLATE).format(n=n)
    cls = 'demo leaves' if n in LEAVES else 'demo'
    return (f'      <article class="card" id="{n}">\n'
            f'        <div class="{cls}">{subj}</div>\n'
            f'        <h3>{n}</h3>\n'
            f'        <p>{DESC[n]}</p>\n'
            f'        <code>data-dolly="{n}"</code>\n'
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

nav = ' '.join(f'<a href="#{s}">{t}</a>' for s, t, _, _ in GROUPS)

HEAD = open(os.path.join(os.path.dirname(__file__), 'moves-head.html'), encoding='utf-8').read()
html = HEAD.replace('{{COUNT}}', str(len(order))) \
           .replace('{{NAV}}', nav) \
           .replace('{{SECTIONS}}', '\n'.join(sections))

tmp = 'moves.html.tmp'
open(tmp, 'w', encoding='utf-8').write(html)
os.replace(tmp, 'moves.html')
print('ok: %d moves across %d groups' % (len(order), len(GROUPS)))
