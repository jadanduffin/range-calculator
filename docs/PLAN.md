# PLAN: Point Distance

## Build steps
| # | Step | Satisfies AC | Test that proves it |
|---|---|---|---|
| 1 | Single-file index.html with parsePoint + calculate | AC1–AC3 | tests/test_calculator.py |
| 2 | Meters output with editable meters-per-unit scale | AC4–AC5 | tests/test_calculator.py |
| 3 | Windows desktop app (tkinter, like AutoClicker): src/rangecalc.py maths, src/RangeCalculator.pyw window, crosshair icon, build.ps1 + Inno Setup installer, GitHub release + update check | AC1–AC3, AC7, AC9–AC10, AC12 | tests/test_rangecalc.py |

## Risks the critique found
| Risk | What we changed |
|---|---|
| "A²+B²=C²" on coordinates is ambiguous (distance, third corner, per-axis) | Asked the user; chose distance A→B |
| Pasted text comes in many shapes | Parser just pulls out exactly two numbers, errors otherwise |

## Approval
- Approved by: user (via chat choices)  Date: 2026-10-05
