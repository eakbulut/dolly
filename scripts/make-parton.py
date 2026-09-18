"""Regenerates assets/parton.webp — the photograph the countdown opens on.

Square-cropped on her face, and tinted at BUILD TIME rather than with a CSS
filter. That is not a preference: a filter puts the element on its own
compositing path, and against the leader's composited background animation it
beat an explicit z-index outright — the photo rendered, correctly clipped, and
stayed underneath. Baking the duotone leaves the element plain.

The duotone spans nearly the full range (3,5,16) to (246,248,255), so it reads
as a cool cast rather than a blue wash; pulling the light end down to ~232
flattens the picture noticeably.

    python3 scripts/make-parton.py <source-image>
"""
from PIL import Image
import sys, os

SRC   = sys.argv[1] if len(sys.argv) > 1 else "00parton-dolly-phwq-superJumbo.webp"
SIZE  = 960
DARK  = (3, 5, 16)
LIGHT = (246, 248, 255)

im = Image.open(SRC).convert("RGB")
W, H = im.size
side = min(W, H)
cx, cy = int(W * 0.60), int(H * 0.35)          # her face sits high in the frame
x0 = max(0, min(W - side, cx - side // 2))
y0 = max(0, min(H - side, cy - side // 2))
sq = im.crop((x0, y0, x0 + side, y0 + side)).resize((SIZE, SIZE), Image.LANCZOS)

lut = []
for c in range(3):
    lut += [int(DARK[c] + (LIGHT[c] - DARK[c]) * (i / 255)) for i in range(256)]
out = os.path.join(os.path.dirname(__file__), "..", "assets", "parton.webp")
sq.convert("L").convert("RGB").point(lut).save(out, "WEBP", quality=70, method=6)
print(f"{SIZE}x{SIZE} -> {os.path.getsize(out)/1024:.1f} kB")
