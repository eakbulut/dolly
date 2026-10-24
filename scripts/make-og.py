#!/usr/bin/env python3
"""Regenerate assets/og-image.png, the social card.

    python3 scripts/make-og.py

The move count is READ FROM src/dolly.css, never typed here. The card shipped
saying "31 moves" while the library shipped 34, which is the kind of thing
nobody notices until it is the image on a link somebody posts.

Palette and geometry were sampled from the original card so this is a
regeneration, not a redesign:
    background   vertical gradient #19191E -> #0A0A0F
    mark + word  #F2F2EE   (--film-fg)
    mark block   #2B4BE8   (--accent)
    subtitle     #A9A9B0
    stat line    #8FA6FF   (--lit, the accent used on dark)
"""

import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
CSS = os.path.join(ROOT, 'src', 'dolly.css')
OUT = os.path.join(ROOT, 'assets', 'og-image.png')
FONT = os.path.expanduser(
    '~/Library/Fonts/fonts/ofl/archivo/Archivo[wdth,wght].ttf')

W, H = 1200, 630
BG_TOP, BG_BOT = (25, 25, 30), (10, 10, 15)
CREAM, ACCENT = (242, 242, 238), (43, 75, 232)
GREY, LIT = (169, 169, 176), (143, 166, 255)

SS = 3  # supersample: Pillow has no antialiasing on shapes


def move_count():
    """Count the moves the stylesheet actually ships."""
    css = re.sub(r'/\*[\s\S]*?\*/', '', open(CSS, encoding='utf-8').read())
    moves = set()
    for m in re.finditer(r'\[data-dolly="([^"]+)"\]([^{]*)\{([^}]*)\}', css):
        if 'animation-name' in m.group(3):
            moves.add(m.group(1))
    return len(moves)


def font(size, weight):
    f = ImageFont.truetype(FONT, size * SS)
    try:
        # NB: axis order is Weight, Width — the opposite of what the
        # filename Archivo[wdth,wght].ttf implies. Passing them the other
        # way round sets Weight=100 and renders everything hairline.
        f.set_variation_by_axes([weight, 100])
    except Exception:
        pass
    return f


def main():
    if not os.path.exists(FONT):
        sys.exit(f'Archivo not found at {FONT}\n'
                 'Install it, or point FONT at another copy.')

    n = move_count()
    im = Image.new('RGB', (W * SS, H * SS), BG_TOP)
    d = ImageDraw.Draw(im)

    # background: vertical gradient, drawn as rows
    for y in range(H * SS):
        t = y / (H * SS - 1)
        d.line([(0, y), (W * SS, y)],
               fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT)))

    # ---- the mark: two posts and a truck, same as the favicon ----
    post_w, post_h, r = 18, 152, 9
    x0, y0 = 125, 239
    for dx in (0, 82):
        d.rounded_rectangle(
            [(x0 + dx) * SS, y0 * SS, (x0 + dx + post_w) * SS, (y0 + post_h) * SS],
            radius=r * SS, fill=CREAM)
    d.rounded_rectangle([x0 * SS, (y0 + 56) * SS, (x0 + 135) * SS, (y0 + 103) * SS],
                        radius=11 * SS, fill=ACCENT)

    # ---- type ----
    tx = 332
    d.text((tx * SS, 243 * SS), 'Dolly', font=font(96, 800), fill=CREAM)
    d.text((tx * SS, 352 * SS), 'Scroll animations in plain CSS.',
           font=font(31, 400), fill=GREY)
    d.text((tx * SS, 408 * SS), f'{n} moves  ·  0 kB of JavaScript',
           font=font(21, 500), fill=LIT)

    im = im.resize((W, H), Image.LANCZOS)

    # Stamp the count into the file's metadata. A test cannot read type out
    # of a PNG, but it can read a tEXt chunk — so this is what makes the card
    # guardable at all, and the reason the stale "31 moves" could sit there
    # unnoticed while three other surfaces were kept honest by tests.
    meta = PngImagePlugin.PngInfo()
    meta.add_text('dolly-moves', str(n))

    tmp = OUT + '.tmp'
    im.save(tmp, 'PNG', optimize=True, pnginfo=meta)
    os.replace(tmp, OUT)
    print(f'wrote {OUT} — {n} moves, {os.path.getsize(OUT) // 1024} kB')


if __name__ == '__main__':
    main()
