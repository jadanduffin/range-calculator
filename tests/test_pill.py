"""Tests for src/pill.py: smooth (anti-aliased) pill shapes for the window's buttons."""

from pill import pill_pixels

INK, ORANGE, LINE = "#08090a", "#fb4b1d", "#1e1f21"


def hexes(rows):
    return {c for row in rows for c in row}


def test_size_matches():
    rows = pill_pixels(80, 26, fill=ORANGE, bg=INK)
    assert len(rows) == 26 and all(len(r) == 80 for r in rows)


def test_middle_is_solid_and_corners_are_background():
    rows = pill_pixels(80, 26, fill=ORANGE, bg=INK)
    assert rows[13][40] == ORANGE
    assert rows[0][0] == INK and rows[25][79] == INK


def test_edges_are_smoothed():
    # A jagged pill has only the two pure colours; a smooth one blends in between along the curve.
    colours = hexes(pill_pixels(80, 26, fill=ORANGE, bg=INK))
    assert len(colours) > 6


def test_left_right_and_top_bottom_mirror():
    rows = pill_pixels(81, 27, fill=ORANGE, bg=INK, stroke=LINE)
    assert all(row == row[::-1] for row in rows)
    assert rows == rows[::-1]


def test_stroke_shows_on_the_edge_only():
    rows = pill_pixels(80, 26, fill=INK, bg=INK, stroke=ORANGE)
    assert rows[0][40] != INK  # top edge carries the stroke
    assert rows[13][40] == INK  # inside stays the fill


def test_glow_brightens_around_the_pill():
    plain = pill_pixels(120, 60, fill=ORANGE, bg=INK)
    glow = pill_pixels(120, 60, fill=ORANGE, bg=INK, glow=(ORANGE, 0.24, 20), inset=20)
    assert plain[13][60] == ORANGE  # no inset: solid there
    assert glow[15][60] != INK  # 5 px above the inset pill: tinted by the glow
    assert glow[0][0] == INK  # far corner: no glow
