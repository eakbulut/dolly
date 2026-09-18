"""Regenerates assets/leader.png — the Academy countdown leader played by the
`sequence` move in Act V, and shown uncropped as the reel beneath it.

Twenty-four cells on a 6x4 GRID: rows are 3, 2, 1, GO and each row is six
frames of the sweep hand.

TWO HARD CONSTRAINTS, both learned the painful way:

1. The sheet must be a GRID, not a strip. A single row is rendered at
   FRAMES x element-width, and an ANIMATED background that wide stops
   rasterising and paints nothing — silently, with no error, and
   inconsistently enough to look fine on the machine that built it. Six
   columns renders six element-widths across instead of twenty-four.

2. Pillow's draw primitives are not antialiased. Everything is rendered at
   SS times size and resampled down, which is the whole difference between
   "jagged clip-art" and a drawn frame.

Indexed PNG: flat synthetic art palettises to a fraction of lossy WebP, and
WebP additionally caps any dimension at 16383px.

    python3 scripts/make-leader.py
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

CELL, COLS, ROWS = 384, 12, 4           # rows: 3, 2, 1, GO; eight sweep frames each
SS     = 4                              # supersample: Pillow does not antialias
INK    = (242, 242, 238)
BG     = (11, 11, 12)
ACCENT = (43, 75, 232)
DIM    = (112, 112, 108)
FAINT  = (46, 46, 50)
FONT   = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
THIN   = "/System/Library/Fonts/Supplemental/Arial.ttf"
LABELS = ["3", "2", "1", "GO"]

def cell(row, col):
    z = CELL * SS
    im = Image.new("RGB", (z, z), BG)
    d  = ImageDraw.Draw(im, "RGBA")
    c  = z / 2
    label = LABELS[row]
    go    = (label == "GO")
    t     = col / COLS                  # 0 .. 5/6 of a full sweep
    ang   = -90 + 360 * t

    R, R2, R3 = z*0.46, z*0.355, z*0.30

    # GO fills as it lands, so the last row reads as a release, not a fourth count
    if go:
        d.ellipse([c-R, c-R, c+R, c+R], fill=ACCENT + (int(30 + 150*t),))
    d.pieslice([c-R, c-R, c+R, c+R], -90, ang, fill=ACCENT + (54,))

    d.line([c, 0, c, z], fill=FAINT, width=int(z*0.0035))
    d.line([0, c, z, c], fill=FAINT, width=int(z*0.0035))
    d.ellipse([c-R, c-R, c+R, c+R], outline=INK, width=int(z*0.0062))
    d.ellipse([c-R3, c-R3, c+R3, c+R3], outline=DIM + (150,), width=int(z*0.0022))

    for k in range(12):
        a = math.radians(k*30); long_ = (k % 3 == 0)
        r0 = R2 * (0.90 if long_ else 0.945)
        d.line([c + r0*math.cos(a), c + r0*math.sin(a),
                c + R2*math.cos(a), c + R2*math.sin(a)],
               fill=INK if long_ else DIM, width=int(z*(0.0050 if long_ else 0.0030)))

    rr = R*0.97
    d.line([c, c, c + rr*math.cos(math.radians(ang)), c + rr*math.sin(math.radians(ang))],
           fill=ACCENT if not go else INK, width=int(z*0.0105))
    d.ellipse([c-z*0.011, c-z*0.011, c+z*0.011, c+z*0.011], fill=INK)

    f = ImageFont.truetype(FONT, int(z*(0.30 if not go else 0.21)))
    tb = d.textbbox((0,0), label, font=f)
    d.text((c-(tb[2]-tb[0])/2-tb[0], c-(tb[3]-tb[1])/2-tb[1]-z*0.012), label, font=f, fill=INK)

    fs = ImageFont.truetype(THIN, int(z*0.038))
    d.text((z*0.062, z*0.055), f"{row*COLS+col+1:02d}", font=fs, fill=DIM)
    return im.resize((CELL, CELL), Image.LANCZOS)

sheet = Image.new("RGB", (CELL*COLS, CELL*ROWS), BG)
for r in range(ROWS):
    for c_ in range(COLS):
        sheet.paste(cell(r, c_), (CELL*c_, CELL*r))

out = os.path.join(os.path.dirname(__file__), "..", "assets", "leader.png")
sheet.convert("P", palette=Image.ADAPTIVE, colors=64).save(out, optimize=True)
print(f"{COLS*ROWS} cells, {COLS}x{ROWS} grid, {CELL*COLS}x{CELL*ROWS}px -> "
      f"{os.path.getsize(out)/1024:.1f} kB")
