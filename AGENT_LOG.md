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

## 2026-10-05: Show C in meters
- Did: Added a "Meters per unit" box (default 100). C now reads 411.76 m for the example; the working line shows units × scale.
- Decided and why: User said the scale can vary, so it's an editable box rather than a hidden ×100. Two decimals per user choice. Bad scale (blank, 0, negative, text) gives a clear error.
- Unsure about: The user asked for "412 meters"; two decimals gives 411.76, which rounds to 412, so the number is consistent.

## 2026-10-05: Restyle with the Jadan Duffin design system
- Did: Restyled index.html: near-black ground, Schibsted Grotesk + JetBrains Mono, JD mark, mono uppercase labels, one orange primary button, hairline dividers, rise-and-fade entrance (off when reduced motion is set). Added the standard round × clear button to each point box. The field with the problem turns orange on error. Maths and tests unchanged.
- Decided and why: Fonts and the mark are embedded inside index.html (base64) so the page stays one double-clickable file and never loads fonts from the network (design-system rule). The file is now ~480 KB, almost all fonts. Font licence copied to FONTS-LICENSE.txt as the OFL requires.
- Unsure about: Retitled to "The distance from A to B" to avoid a one-word last line; the user may prefer other wording.

## 2026-10-05: Wardogs instructions
- Did: Researched Wardogs mortar aiming. Confirmed 1 map unit = 100 m, RNG = range in meters (left of sight), MIL = barrel elevation in mils (right; more mils = shorter shot; follows RNG automatically). Rewrote the page: gun/target labels, a 5-step how-to, a sight glossary, L81 range and hill caveats, and a "Dial RNG to 412" line (dialRange, tested).
- Decided and why: Direction and an out-of-range warning are useful but not asked for, so they went to BACKLOG.md.
- Unsure about: Facts come from community guides (sportskeeda, gamerant, wardogstips.wiki, wardogshub.uk), not official docs; L81 max range is quoted as ~684–700 m and is disputed.
