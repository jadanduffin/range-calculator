# Smooth pill shapes for the window. Tk's canvas draws curves without anti-aliasing, so rounded buttons came out
# jagged; here every pixel is shaded by how much of it the pill covers. Pure Python, no extra packages.
import math


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def pill_pixels(w, h, fill, bg, stroke=None, glow=None, inset=0):
    """Rows of '#rrggbb' strings for a w x h image: a capsule `inset` px in from every side, filled with `fill`,
    a 1 px `stroke` just inside its edge, and an optional `glow` = (colour, peak strength, reach in px) outside it."""
    fill_c, bg_c = _rgb(fill), _rgb(bg)
    stroke_c = _rgb(stroke) if stroke else None
    glow_c, peak, reach = (_rgb(glow[0]), glow[1], glow[2]) if glow else (None, 0, 1)
    r = (h - 2 * inset) / 2  # end radius
    cy = h / 2
    x0, x1 = inset + r, w - inset - r  # the capsule's centre line
    rows = []
    for y in range(h):
        py = y + 0.5
        row = []
        for x in range(w):
            px = x + 0.5
            cx = min(max(px, x0), x1)
            d = math.hypot(px - cx, py - cy) - r  # signed distance to the edge: < 0 inside
            c = bg_c
            if glow_c and 0 < d < reach:
                c = _mix(bg_c, glow_c, peak * (1 - d / reach) ** 2)
            c = _mix(c, fill_c, min(1.0, max(0.0, 0.5 - d)))  # fill, with a one-pixel soft edge
            if stroke_c:
                c = _mix(c, stroke_c, min(1.0, max(0.0, 1.0 - abs(d + 0.5))))  # 1 px line on the inner edge
            row.append("#%02x%02x%02x" % tuple(round(v) for v in c))
        rows.append(row)
    return rows


def pill_image(tk, w, h, **kw):
    """The same pill as a tk.PhotoImage."""
    img = tk.PhotoImage(width=w, height=h)
    img.put(" ".join("{" + " ".join(row) + "}" for row in pill_pixels(w, h, **kw)))
    return img
