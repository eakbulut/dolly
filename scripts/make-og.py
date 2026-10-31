#!/usr/bin/env python3
"""Regenerate assets/og-image.png, the social card.

    python3 scripts/make-og.py

The move and exit counts are READ FROM src/dolly.css, never typed here. The
card once said "31 moves" while the library shipped 34, which is the kind of
thing nobody notices until it is the image on a link somebody posts.

The card is the homepage's title card: the blue field, the claim in Jost
capitals, the credits underneath. Jost is the variable font from a local
google/fonts checkout (one `wght` axis); set DOLLY_JOST to use another copy.
"""

import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
CSS = os.path.join(ROOT, 'src', 'dolly.css')
OUT = os.path.join(ROOT, 'assets', 'og-image.png')
FONT = os.environ.get('DOLLY_JOST') or os.path.expanduser(
    '~/Library/Fonts/fonts/ofl/jost/Jost[wght].ttf')

W, H = 1200, 630
BLUE, WHITE = (43, 75, 232), (255, 255, 255)      # --accent, and type on it
PAPER, PALE = (243, 238, 227), (217, 224, 255)     # --paper; the credit labels

SS = 3  # supersample: Pillow has no antialiasing on shapes


def count(attr):
    """Count the moves (or exits) the stylesheet actually ships."""
    css = re.sub(r'/\*[\s\S]*?\*/', '', open(CSS, encoding='utf-8').read())
    names = set()
    for m in re.finditer(r'\[' + attr + r'="([^"]+)"\]([^{]*)\{([^}]*)\}', css):
        if 'animation-name' in m.group(3):
            names.add(m.group(1))
    return len(names)


def font(size, weight):
    f = ImageFont.truetype(FONT, size * SS)
    f.set_variation_by_axes([weight])   # Jost has one axis: wght
    return f


def centred(d, y, text, f, fill, tracking=0):
    """Draw text centred on the card, with letter-spacing in px."""
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + tracking * SS * (len(text) - 1)
    x = (W * SS - total) / 2
    for c, w in zip(text, widths):
        d.text((x, y * SS), c, font=f, fill=fill)
        x += w + tracking * SS


def main():
    if not os.path.exists(FONT):
        sys.exit(f'Jost not found at {FONT}\n'
                 'Point DOLLY_JOST at a copy of Jost[wght].ttf from google/fonts.')

    moves, exits = count('data-dolly'), count('data-dolly-exit')
    im = Image.new('RGB', (W * SS, H * SS), BLUE)
    d = ImageDraw.Draw(im)

    centred(d, 92, 'DOLLY', font(26, 700), WHITE, tracking=9)
    centred(d, 196, 'SCROLL ANIMATIONS', font(92, 700), WHITE, tracking=2)
    centred(d, 298, 'IN PLAIN CSS', font(92, 700), WHITE, tracking=2)
    d.line([(150 * SS, 450 * SS), (1050 * SS, 450 * SS)], fill=PALE, width=SS)
    centred(d, 474, 'STARRING  ·  DIRECTED BY  ·  JAVASCRIPT', font(17, 500), PALE, tracking=4)
    centred(d, 504, f'{moves} MOVES, {exits} EXITS  ·  YOUR BROWSER  ·  NONE',
            font(22, 700), WHITE, tracking=3)

    im = im.resize((W, H), Image.LANCZOS)

    # Stamp the counts into the file's metadata. A test cannot read type out
    # of a PNG, but it can read a tEXt chunk, so this is what makes the card
    # guardable at all.
    meta = PngImagePlugin.PngInfo()
    meta.add_text('dolly-moves', str(moves))
    meta.add_text('dolly-exits', str(exits))

    tmp = OUT + '.tmp'
    im.save(tmp, 'PNG', optimize=True, pnginfo=meta)
    os.replace(tmp, OUT)
    print(f'wrote {OUT} — {moves} moves, {exits} exits, {os.path.getsize(OUT) // 1024} kB')


if __name__ == '__main__':
    main()
