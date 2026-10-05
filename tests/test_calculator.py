"""Tests for the distance calculator in index.html.

The math lives in a <script> block inside index.html. These tests pull that
script out and run it with Node, so we test the exact code the page uses.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

PAGE = Path(__file__).resolve().parent.parent / "index.html"


def run_js(expression):
    """Run the page's calculator code in Node and return the result of `expression`."""
    html = PAGE.read_text()
    match = re.search(r"<script id=\"calculator\">(.*?)</script>", html, re.S)
    assert match, "index.html must contain <script id=\"calculator\">"
    code = match.group(1) + f"\nconsole.log(JSON.stringify({expression}));"
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


# AC1: the example values from the brief give the right distance.
def test_example_values_give_expected_distance():
    result = run_js('calculate("x98.42, y110.38", "x94.53, y109.03", "100")')
    assert result["distance"] == pytest.approx(4.117596, abs=1e-6)


# AC2: common paste formats are all understood.
@pytest.mark.parametrize(
    "text",
    ["x98.42, y110.38", "98.42, 110.38", "98.42 110.38", "X: 98.42  Y: 110.38", " x98.42,y110.38 "],
)
def test_paste_formats_are_understood(text):
    assert run_js(f"parsePoint({json.dumps(text)})") == {"x": 98.42, "y": 110.38}


def test_negative_numbers_are_understood():
    assert run_js('parsePoint("x-3, y-4.5")') == {"x": -3, "y": -4.5}


# AC3: bad input gives a clear message instead of a wrong number.
@pytest.mark.parametrize("text", ["", "x98.42", "hello", "1, 2, 3"])
def test_bad_input_gives_error_message(text):
    result = run_js(f'calculate({json.dumps(text)}, "x1, y1", "100")')
    assert "error" in result
    assert result["error"].startswith("Your position")


def test_target_error_names_the_target():
    assert run_js('calculate("1, 1", "x5", "100")')["error"].startswith("Target")


def test_classic_3_4_5_triangle():
    assert run_js('calculate("0, 0", "3, 4", "100")')["distance"] == 5


# AC4: distance is converted to meters using the "meters per unit" scale.
def test_example_values_in_meters_at_default_scale():
    result = run_js('calculate("x98.42, y110.38", "x94.53, y109.03", "100")')
    assert result["meters"] == pytest.approx(411.7596, abs=1e-4)
    assert run_js("formatMeters(411.7596)") == "411.76 m"


def test_scale_can_change():
    assert run_js('calculate("0, 0", "3, 4", "10")')["meters"] == 50


# AC5: a missing or nonsense scale gives a clear message.
@pytest.mark.parametrize("scale", ["", "abc", "0", "-5"])
def test_bad_scale_gives_error_message(scale):
    result = run_js(f'calculate("0, 0", "3, 4", {json.dumps(scale)})')
    assert "meters per unit" in result["error"].lower()


# AC6: the page tells you the whole-meter RNG to dial in the game.
def test_rng_to_dial_is_whole_meters():
    assert run_js("dialRange(411.7596)") == 412
    assert run_js("dialRange(411.4)") == 411


# AC7: the page gives the compass direction from gun to target (0 = north, 90 = east; Y counts north).
@pytest.mark.parametrize(
    "target, bearing",
    [("0, 10", 0), ("10, 0", 90), ("0, -10", 180), ("-10, 0", 270), ("5, 5", 45)],
)
def test_bearing_points_the_right_way(target, bearing):
    assert run_js(f'calculate("0, 0", {json.dumps(target)}, "100")')["bearing"] == pytest.approx(bearing)


def test_example_bearing():
    result = run_js('calculate("x98.42, y110.38", "x94.53, y109.03", "100")')
    assert result["bearing"] == pytest.approx(250.86, abs=0.01)
    assert run_js("compassPoint(250.86)") == "WSW"
    assert run_js("compassPoint(359)") == "N"


# AC8: ranges past the L81's last tick are flagged.
def test_out_of_range_is_flagged():
    assert run_js('calculate("0, 0", "6, 0", "100")')["outOfRange"] is False
    assert run_js('calculate("0, 0", "6.9, 0", "100")')["outOfRange"] is True


# AC9: the weapon switch sets which range limits apply.
def at(meters, weapon):
    """calculate() for a target `meters` due east of the gun."""
    return run_js(f'calculate("0, 0", "{meters / 100}, 0", "100", "{weapon}")')


def test_mortar_is_the_default_weapon():
    assert run_js('calculate("0, 0", "6.9, 0", "100")')["outOfRange"] is True


@pytest.mark.parametrize(
    "meters, weapon, out_of_range",
    [(100, "mortar", True), (400, "mortar", False), (690, "mortar", True),
     (700, "artillery", True), (1500, "artillery", False), (2700, "artillery", True)],
)
def test_range_limits_per_weapon(meters, weapon, out_of_range):
    result = at(meters, weapon)
    assert result["outOfRange"] is out_of_range
    assert (result["rangeNote"] is not None) is out_of_range


def test_too_close_and_too_far_say_which():
    assert "too close" in at(700, "artillery")["rangeNote"].lower()
    assert "past" in at(2700, "artillery")["rangeNote"].lower()


# AC10: artillery says which arc reaches the target.
def test_artillery_arc_advice():
    assert at(900, "artillery")["arc"] == "High arc only"
    assert at(1500, "artillery")["arc"] == "Low or high arc"
    assert at(400, "mortar")["arc"] is None
