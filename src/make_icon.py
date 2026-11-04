# Draws the Range Calculator icon from scratch (a crosshair: outer ring broken by the cross bars, a dashed ring
# and a small centre ring) in brand orange, writes RangeCalculator.ico + icon_preview.png. Needs Pillow.
import math, os
from PIL import Image, ImageDraw

ORANGE = (251, 75, 29, 255)
S = 4  # supersample for clean edges
N = 1000 * S  # drawing canvas; every number below is on a 1000-unit square
HERE = os.path.dirname(os.path.abspath(__file__))
C = N / 2

def px(v): return v * S

def ring(d, radius, width, gaps=(), gap_deg=0):
    """A stroked circle; `gaps` are angles (degrees) where a slice `gap_deg` wide is left out."""
    box = (C - px(radius), C - px(radius), C + px(radius), C + px(radius))
    if not gaps:
        d.ellipse(box, outline=255, width=px(width))
        return
    gaps = sorted(g % 360 for g in gaps)
    for i, g in enumerate(gaps):
        start = g + gap_deg / 2
        end = gaps[(i + 1) % len(gaps)] - gap_deg / 2 + (360 if i == len(gaps) - 1 else 0)
        d.arc(box, start, end, fill=255, width=px(width))

mask = Image.new("L", (N, N), 0)
d = ImageDraw.Draw(mask)

# outer ring, cut where the four bars cross it (bar half-width 27 + 16 clearance)
ring(d, 340, 42, gaps=(0, 90, 180, 270), gap_deg=2 * math.degrees(math.asin(43 / 340)))

# four bars: from just outside the dashed ring to past the outer ring
for a in (0, 90, 180, 270):
    dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
    x0, y0, x1, y1 = C + dx * px(140), C + dy * px(140), C + dx * px(410), C + dy * px(410)
    w = px(27)
    d.rectangle((min(x0, x1) - (w if dy else 0), min(y0, y1) - (w if dx else 0),
                 max(x0, x1) + (w if dy else 0), max(y0, y1) + (w if dx else 0)), fill=255)

# dashed ring: eight dashes, gaps on the bars' axes and the diagonals
ring(d, 104, 22, gaps=[i * 45 for i in range(8)], gap_deg=16)

# centre ring
ring(d, 50, 22)

art = Image.new("RGBA", (N, N), (0, 0, 0, 0))
art.paste(Image.new("RGBA", (N, N), ORANGE), mask=mask)
art = art.resize((1024, 1024), Image.LANCZOS)
art.save(os.path.join(HERE, "icon_preview.png"))
art.save(os.path.join(HERE, "RangeCalculator.ico"), sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
art.resize((56, 56), Image.LANCZOS).save(os.path.join(HERE, "icon-56.png"))  # header mark, shown at half size on high-DPI
print("wrote RangeCalculator.ico, icon-56.png + icon_preview.png")
