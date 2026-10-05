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
    result = run_js('calculate("x98.42, y110.38", "x94.53, y109.03")')
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
    result = run_js(f'calculate({json.dumps(text)}, "x1, y1")')
    assert "error" in result
    assert "A" in result["error"]


def test_classic_3_4_5_triangle():
    assert run_js('calculate("0, 0", "3, 4")')["distance"] == 5
