"""Tests for the desktop app's maths (src/rangecalc.py). Same acceptance criteria as the web page."""

import pytest

from rangecalc import calculate, compass_point, parse_point


# AC1: the example values give the right distance and RNG.
def test_example_values():
    r = calculate("x98.42, y110.38", "x94.53, y109.03")
    assert r.meters == pytest.approx(411.7596, abs=1e-4)
    assert r.rng == 412


# AC2: common paste formats are understood, including what Mark Coordinates puts in chat.
@pytest.mark.parametrize(
    "text",
    ["x98.42, y110.38", "98.42, 110.38", "98.42 110.38", "X: 98.42  Y: 110.38", " x98.42,y110.38 "],
)
def test_paste_formats(text):
    assert parse_point(text) == (98.42, 110.38)


def test_negative_numbers():
    assert parse_point("x-3, y-4.5") == (-3, -4.5)


# AC3: bad input names the box that is wrong.
@pytest.mark.parametrize("text", ["", "x98.42", "hello", "1, 2, 3"])
def test_bad_position(text):
    assert calculate(text, "1, 1").error.startswith("Your position")


def test_bad_target():
    assert calculate("1, 1", "x5").error.startswith("Target")


# AC7: compass bearing, 0 = north, 90 = east (Y counts north).
@pytest.mark.parametrize("target, bearing", [("0, 10", 0), ("10, 0", 90), ("0, -10", 180), ("-10, 0", 270), ("5, 5", 45)])
def test_bearing(target, bearing):
    assert calculate("0, 0", target).bearing == pytest.approx(bearing)


def test_example_face():
    r = calculate("x98.42, y110.38", "x94.53, y109.03")
    assert r.face == 251
    assert compass_point(r.bearing) == "WSW"
    assert compass_point(359) == "N"


# AC9: weapon reach.
@pytest.mark.parametrize(
    "meters, weapon, out",
    [(100, "mortar", True), (400, "mortar", False), (690, "mortar", True),
     (700, "artillery", True), (1500, "artillery", False), (2700, "artillery", True)],
)
def test_reach(meters, weapon, out):
    r = calculate("0, 0", f"{meters / 100}, 0", weapon)
    assert (r.range_note is not None) is out


def test_too_close_and_too_far_say_which():
    assert "too close" in calculate("0, 0", "7, 0", "artillery").range_note.lower()
    assert "past" in calculate("0, 0", "27, 0", "artillery").range_note.lower()


# AC10: artillery arc advice.
def test_arc():
    assert calculate("0, 0", "9, 0", "artillery").arc == "High arc only"
    assert calculate("0, 0", "15, 0", "artillery").arc == "Low or high arc"
    assert calculate("0, 0", "4, 0", "mortar").arc is None


# The desktop app and the web page must give the same answers.
def test_matches_the_web_page():
    from test_calculator import run_js

    for a, b, w in [("x98.42, y110.38", "x94.53, y109.03", "mortar"), ("12.5, 40", "30.1, 22.7", "artillery")]:
        js = run_js(f'calculate("{a}", "{b}", "100", "{w}")')
        py = calculate(a, b, w)
        assert py.meters == pytest.approx(js["meters"])
        assert py.bearing == pytest.approx(js["bearing"])
        assert py.range_note == js["rangeNote"]
        assert py.arc == js["arc"]
