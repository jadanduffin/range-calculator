# SPEC: Wardogs range calculator

## 1. The problem
In the game Wardogs I mark my mortar and a target on the map (Mark Coordinates prints x, y in chat) and need the range in meters to dial into the sight's RNG readout, without doing A² + B² = C² by hand.

## 2. The user
Me.

## 3. The job
When I have two points, I want to paste them and press a button, so I can get C instantly.

## 4. MVP cut
| Must (MVP) | Should (if time) | Won't (moved to BACKLOG.md) |
|---|---|---|
| Paste A and B, press Calculate, see C | Show the working | Third-corner / per-axis modes |

## 5. User flow
1. Open index.html in a browser.
2. Paste Point A and Point B (e.g. `x98.42, y110.38`).
3. Press Calculate C (or Enter) and read C.

## 6. Decision table
| Point A text | Point B text | Expected result |
|---|---|---|
| two numbers | two numbers | C = √(Δx² + Δy²) × meters per unit |
| not two numbers | anything | "Point A needs exactly two numbers…" |
| two numbers | not two numbers | "Point B needs exactly two numbers…" |

## 7. Acceptance criteria
- [x] AC1: Given A = x98.42, y110.38 and B = x94.53, y109.03, when I press Calculate, then C ≈ 4.1176.
- [x] AC2: Given points pasted as `x1, y2`, `1, 2`, `1 2` or `X: 1 Y: 2`, then they are all understood.
- [x] AC3: Given a point without exactly two numbers, then a clear error names which point is wrong.
- [x] AC4: Given a meters-per-unit scale (default 100), then C is shown in meters to two decimals (example: 411.76 m).
- [x] AC6: Given a result, then the page shows the whole-meter RNG to dial (example: 412).
- [x] AC7: Given a result, then the page shows the compass bearing to face (0 = north, Y counts north) and its compass point (example: 251° WSW).
- [x] AC8: Given a range past 684 m, then a warning says it is beyond the L81's last range tick.
- [x] AC9: Given the weapon switch (Mortar default, or Artillery), then range warnings use that weapon's reach (L81 132–684 m, SPH-2 745–2,660 m) and say too close or too far.
- [x] AC10: Given Artillery, then the page says whether only the high arc reaches (under ~1,070 m).
- [x] AC11: Given a phone (under 640 px wide), then each point has separate X and Y boxes with the number keypad; Enter moves to the next box and calculates after the last; a comma decimal is accepted; an empty box is flagged.
- [x] AC5: Given a blank, zero, negative or non-number scale, then a clear error asks for a number above 0.
