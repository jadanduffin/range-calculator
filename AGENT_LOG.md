# Agent Log (the agent's)

The agent appends here after every task (see CLAUDE.md).
Compare it with DEVLOG.md: where the two logs disagree is where you learn the most.

---

## YYYY-MM-DD: <task>
- Did:
- Decided and why:
- Unsure about:

## 2026-10-05: Point distance calculator
- Did: Built index.html (one file, no installs) that takes two pasted points and shows C = distance between them, plus the working. Tests in tests/test_calculator.py run the page's own script through Node. Screenshots in screenshots/.
- Decided and why: User chose "distance A→B" over third-corner / per-axis readings. Plain HTML instead of a Python server because it's the simplest thing that works (double-click to open).
- Unsure about: Tests need Node installed to run. Result shown to 4 decimal places — user may want more/fewer.
