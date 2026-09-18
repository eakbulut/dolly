"""Fits assets/dolly-word.svg into the ribbon on index.html.

The word is authored elsewhere as a single continuous CENTERLINE stroke — one
open path, no fill, no closed contours — because `draw` animates
stroke-dashoffset along a path, so the path has to be the pen line itself.
Text converted to outlines would trace the rim of each letter instead of
writing it, and no amount of fitting fixes that.

This script only transplants it: read the artwork's path, size the ribbon's
viewBox to the artwork with a margin, and inline the `d`. Send a new
assets/dolly-word.svg and re-run; nothing else on the page changes.

    python3 scripts/make-ribbon.py
"""
import re, os

HERE = os.path.dirname(__file__)
ART  = os.path.join(HERE, '..', 'assets', 'dolly-word.svg')
IDX  = os.path.join(HERE, '..', 'index.html')
PAD  = 16                      # viewBox margin so the word never touches an edge

art = open(ART, encoding='utf-8').read()
paths = re.findall(r'<path[^>]*\sd="([^"]*)"', art)
if len(paths) != 1:
    raise SystemExit(f"expected exactly one <path>, found {len(paths)}")
d = paths[0].strip()

if 'Z' in d.upper():
    print("warning: the path contains Z (closed subpaths) — check it is a "
          "centerline and not converted outlines")
subpaths = d.upper().count('M')
print(f"path: {len(d)} chars, {subpaths} subpath{'s' if subpaths != 1 else ''}")

nums = [float(x) for x in re.findall(r'-?\d+\.?\d*(?:e-?\d+)?', d)]
xs, ys = nums[0::2], nums[1::2]
x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
vb = f"{x0-PAD:.0f} {y0-PAD:.0f} {x1-x0+2*PAD:.0f} {y1-y0+2*PAD:.0f}"
print(f"art bbox {x0:.0f},{y0:.0f} -> {x1:.0f},{y1:.0f}   viewBox \"{vb}\"")

t = open(IDX, encoding='utf-8').read()

# `meet`, not `none`: the ribbon is full-viewport, and `none` would stretch the
# letterforms to whatever the window's aspect happens to be. The artwork is
# close enough to a typical screen that `meet` still nearly fills the frame.
# Two ribbon layers (film and paper) — both must carry the same viewBox or
# the copies drift apart.
t, n = re.subn(r'(<svg class="ribbon ribbon-\w+" viewBox=")[^"]*(" preserveAspectRatio=")[^"]*(")',
               lambda m: m.group(1)+vb+m.group(2)+'xMidYMid meet'+m.group(3), t)
if n == 0:
    raise SystemExit(
        "no ribbon markup in index.html — the drawing ribbon is currently\n"
        "removed from the page. scratchpad/ribbon-removed.txt has the exact\n"
        "blocks that were taken out; put them back, then re-run this.")
if n != 3:
    raise SystemExit(f"expected 3 ribbon <svg> tags, updated {n}")

m = re.search(r'<path id="dolly-word"[\s\S]*?/>', t)
if not m:
    raise SystemExit("could not find the ribbon <path>")
new = ('<path id="dolly-word" data-dolly="draw" data-dolly-on="page" pathLength="1"\n'
       '        fill="none" stroke="#4A6BFF" stroke-width="7"\n'
       '        stroke-linecap="round" stroke-linejoin="round"\n'
       f'        d="{d}"/>')
# Build the whole document in memory, then replace the file atomically.
# `open(path,'w').write(expr)` truncates the file the moment open() is
# evaluated — if the expression then raises, the file is left EMPTY. That is
# exactly how index.html got destroyed once.
out = t[:m.start()] + new + t[m.end():]
tmp = IDX + '.tmp'
with open(tmp, 'w', encoding='utf-8') as fh:
    fh.write(out)
os.replace(tmp, IDX)
print("index.html updated")
