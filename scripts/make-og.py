#!/usr/bin/env python3
"""Regenerate assets/og-image.png, the social card.

    python3 scripts/make-og.py

The move and exit counts are READ FROM src/dolly.css, never typed here. The
card once said "31 moves" while the library shipped 34, which is the kind of
thing nobody notices until it is the image on a link somebody posts.

The card is the homepage's first screen: the auditorium photograph with the
claim on the cinema screen and the credits in the seats. Jost is the variable font from a local
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
PAPER, PALE = (243, 238, 227), (189, 181, 165)     # --paper; the credit labels

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


PHOTO = os.path.join(ROOT, 'assets', 'photos', 'auditorium-2400.webp')
# The screen inside that photograph, as fractions of its width and height.
SCREEN = (0.214, 0.188, 0.740, 0.524)


def main():
    if not os.path.exists(FONT):
        sys.exit(f'Jost not found at {FONT}\n'
                 'Point DOLLY_JOST at a copy of Jost[wght].ttf from google/fonts.')

    moves, exits = count('data-dolly'), count('data-dolly-exit')

    # The homepage's first screen: the empty auditorium, the claim on the
    # cinema screen, the credits in the dark seats underneath.
    photo = Image.open(PHOTO).convert('RGB')
    pw, ph = photo.size
    crop_h = round(pw * H / W)
    top = round(ph * 0.06)
    photo = photo.crop((0, top, pw, top + crop_h)).resize((W * SS, H * SS), Image.LANCZOS)
    im = photo
    d = ImageDraw.Draw(im)
    sx0, sx1 = SCREEN[0] * W, SCREEN[2] * W
    sy0 = (SCREEN[1] * ph - top) / crop_h * H
    sy1 = (SCREEN[3] * ph - top) / crop_h * H
    cx = (sx0 + sx1) / 2

    def centred_at(y, text, f, fill, tracking=0, x_mid=cx):
        widths = [d.textlength(c, font=f) for c in text]
        total = sum(widths) + tracking * SS * (len(text) - 1)
        x = x_mid * SS - total / 2
        for c, w in zip(text, widths):
            d.text((x, y * SS), c, font=f, fill=fill)
            x += w + tracking * SS

    ink = (27, 26, 23)
    mid = (sy0 + sy1) / 2
    centred_at(mid - 92, 'DOLLY', font(15, 700), (58, 56, 51), tracking=7)
    centred_at(mid - 58, 'SCROLL ANIMATIONS', font(48, 700), ink, tracking=1)
    centred_at(mid + 0, 'IN PLAIN CSS', font(48, 700), ink, tracking=1)
    centred_at(mid + 66, 'NOW SHOWING IN YOUR STYLESHEET', font(13, 500), (58, 56, 51), tracking=4)

    # darken the seats so the credits read, then set them
    shade = Image.new('L', (W * SS, H * SS), 0)
    sd = ImageDraw.Draw(shade)
    for y in range(H * SS):
        t = max(0.0, (y / (H * SS) - 0.62) / 0.38)
        sd.line([(0, y), (W * SS, y)], fill=round(225 * min(1.0, t)))
    im = Image.composite(Image.new('RGB', im.size, (11, 10, 9)), im, shade)
    d = ImageDraw.Draw(im)
    centred_at(548, 'STARRING  ·  DIRECTED BY  ·  JAVASCRIPT', font(14, 500), PALE, tracking=4, x_mid=W / 2)
    centred_at(572, f'{moves} MOVES, {exits} EXITS  ·  YOUR BROWSER  ·  NONE',
               font(20, 700), PAPER, tracking=3, x_mid=W / 2)

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
