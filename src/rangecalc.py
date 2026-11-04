# The Range Calculator's maths, kept apart from the window so it can be tested on its own.
# Mirrors the calculator script in index.html; tests/test_rangecalc.py checks the two agree.
import math, re
from dataclasses import dataclass

METERS_PER_UNIT = 100  # Wardogs map coordinates are in hundreds of meters

# Reach of each weapon, from community guides (no official figures exist).
WEAPONS = {
    "mortar": {"name": "L81 mortar", "min": 132, "max": 684},
    "artillery": {"name": "SPH-2", "min": 745, "max": 2660, "low_arc_min": 1070},
}
POINTS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
NUMBER = re.compile(r"-?\d+(?:\.\d+)?|-?\.\d+")


@dataclass
class Result:
    error: str | None = None
    meters: float = 0.0
    bearing: float = 0.0  # 0 = north, 90 = east
    dx: float = 0.0
    dy: float = 0.0
    range_note: str | None = None
    arc: str | None = None

    @property
    def rng(self):  # the whole-meter number to dial into the sight
        return round(self.meters)

    @property
    def face(self):
        return round(self.bearing) % 360


def parse_point(text):
    """'x98.42, y110.38' -> (98.42, 110.38); None unless the text holds exactly two numbers."""
    numbers = NUMBER.findall(str(text))
    return (float(numbers[0]), float(numbers[1])) if len(numbers) == 2 else None


def compass_point(bearing):
    return POINTS[round(bearing / 22.5) % 16]


def calculate(text_a, text_b, weapon="mortar"):
    a = parse_point(text_a)
    if not a:
        return Result(error="Your position needs an x and a y, like x98.42, y110.38")
    b = parse_point(text_b)
    if not b:
        return Result(error="Target needs an x and a y, like x94.53, y109.03")
    east, north = b[0] - a[0], b[1] - a[1]  # Y counts north on the Wardogs map
    meters = math.hypot(east, north) * METERS_PER_UNIT
    w = WEAPONS.get(weapon, WEAPONS["mortar"])
    note = None
    if meters < w["min"]:
        note = f"Too close for the {w['name']} (minimum about {w['min']} m). Move back."
    if meters > w["max"]:
        note = f"Past the {w['name']}'s reach (about {w['max']:,} m). The shell will fall short; move closer."
    arc = None
    if "low_arc_min" in w:
        arc = "High arc only" if meters < w["low_arc_min"] else "Low or high arc"
    return Result(meters=meters, bearing=math.degrees(math.atan2(east, north)) % 360,
                  dx=abs(east), dy=abs(north), range_note=note, arc=arc)
