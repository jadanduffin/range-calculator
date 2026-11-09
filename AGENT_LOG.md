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

## 2026-10-05: Direction and out-of-range warning
- Did: Result now reads "Dial RNG to 412 · Face 251° WSW". Ranges over 684 m show an orange-dot warning. Step 05 and the compass entry explain using the Face number. 7 new tests.
- Decided and why: Bearing uses Y = north (community guides). 684 m is the last range tick in the walkthrough guide, so it is the safe cut-off.
- Unsure about: Y-north is unconfirmed in the game itself; the page asks the user to report if the first shot lands on the opposite side.

## 2026-10-05: Artillery, weapon switch, PC layout
- Did: Orange button now reads "Enemy range". Added a Mortar / Artillery switch; warnings follow the chosen weapon's reach, and artillery shows "High arc only" or "Low or high arc". Added an SPH-2 guide (crew, B for shells, scroll to stabilize, R then WASD prompts to reload) and a Reach section. On screens 960 px and wider the guides sit in two columns: 02 and 04 on the left, 03 and 05 on the right. 9 new tests.
- Decided and why: The user asked for 02 left and 03 right; Reach went under 02 to keep the columns about even. User approved the weapon switch.
- Unsure about: The vehicle is the SPH-2 self-propelled howitzer (guides call it a tank or self-propelled gun, not a truck). No guide says how to switch arcs in the game. All ranges come from player guides.

## 2026-10-05: Aiming feedback
- Did: No page change. User clarified aiming: put the target on the vertical crosshair line, and above or below center is fine. User chose to keep step order and test the compass Face number tomorrow; the visual-check rewrite is parked in BACKLOG.md.
- Unsure about: Whether Y counts north (drives the Face number). Waiting on the user's in-game test.

## 2026-10-05: "Your gun" → "Your position"
- Did: Replaced every "gun" on the page with "your position" (title, intro, A label, step 01, step 03). Crew wording ("gunner") left as is.
- Decided and why: The user had asked for this in the previous message and I misread it as a step-order request. Owned the mistake and fixed it.

## 2026-10-05: Humanizer pass on page wording
- Did: Applied blader/humanizer rules (not installed on the account; read from GitHub) to all page text. 9 edits: plainer intro, removed "tell me" and "I couldn't find" (my own voice leaking into a page other players read), dropped decorative bold, replaced an unsourced claim ("the closer you mark, the closer the shell lands") with a factual one, and made the untested compass caveat tell the reader what to do.
- Unsure about: Step 03 uses A and B for both the points and the triangle's sides (A² + B² = C²). It's the user's formula, but could confuse readers. Mentioned to the user.

## 2026-10-05: Readability pass (accessibility-review, design-critique, ux-copy)
- Did: Result now shows two big readouts, SET RNG (412) and FACE (251° WSW); the 411.76 m distance moved into the small working line. Faint grey lifted from #696c72 to #83868c so all small text passes 4.5:1 (was 3.5–3.8). On screens 960 px and wider the title sits left and the calculator right, so the result ends at ~605 px on a 1440×900 screen (was 898). Errors use the box names ("Your position…", "Target…") and are linked to their box for screen readers. Weapon buttons 29 → 37 px tall. Terms unified: RNG for range, Face for direction.
- Decided and why: Face uses weight 500, not 800: the design system allows one bold value per card, and Face is still untested in game. The grey change departs from the jadan-design token (#696c72) on this page only; the design system itself is unchanged.
- Unsure about: Whether to update the design system's --jd-muted-2 everywhere. Asked the user.

## 2026-10-05: Phone X/Y boxes
- Did: Under 640 px wide, each point shows two boxes (X, Y) with the number keypad instead of one paste box. Enter jumps box to box and calculates at the end. Comma decimals accepted (joinPoint, tested). Phone and PC boxes stay in sync. Phone errors say "needs a number in both X and Y" and flag only the empty box. Step 01 mentions the phone boxes. PC unchanged.
- Decided and why: Phone boxes use 16 px text so iPhones don't zoom in when you tap them.
- Unsure about: The iPhone number keypad has no minus key, so negative coordinates can't be typed on iPhone. Wardogs coordinates seen so far are all positive.

## 2026-10-05: Removed the meters-per-unit box
- Did: Removed the box; the page always uses 100 m per map unit (confirmed by guides). calculate() keeps its scale input so existing tests still cover the maths. Intro now says "Enter" instead of "Paste" so it fits phones.

## 2026-10-05: Published as a private link
- Did: Renamed the page title to "Wardogs Range Calculator", set color-scheme: dark, and published a copy without the outer html/head/body wrapper (the publishing service adds its own) at https://claude.ai/artifact/EN8FSC17mcHVnXy2E1iZm9 (private). index.html keeps its wrapper so it still opens by double-click.
- Unsure about: The publish copy lives in the session scratchpad; to republish after future edits, rebuild it from index.html with the same steps.

## 2026-11-04: Windows desktop app + installer
- Did: Rebuilt the calculator as a native Windows app modelled on jadanduffin/AutoClicker: tkinter window (src/RangeCalculator.pyw), maths in src/rangecalc.py (27 new tests, one checks it matches the web page), crosshair icon drawn by src/make_icon.py from the user's reference in #FB4B1D, brand fonts bundled and loaded privately on Windows, HOW TO view showing only the selected weapon's steps, last points/weapon remembered, update check against GitHub releases. build.ps1 + installer/RangeCalculator.iss mirror AutoClicker's. README is now the app's download page; the template README moved to docs/TEMPLATE.md.
- Decided and why: tkinter (no new runtime dependency, same as AutoClicker). The user builds on their PC with build.ps1 -Release, as they chose. Kept index.html for phones.
- Unsure about: The Windows .exe and installer could not be built here (Linux). PyInstaller packaging was checked on Linux and the packaged app ran. Private font loading (AddFontResourceExW) and the dark title bar are Windows-only and untested here. The repo is private, so releases and the update check won't work for others until it is made public.

## 2026-11-04: Repo renamed
- Did: Repo renamed to jadanduffin/wardogs-range-calculator and made public by the user. Updated REPO in the app and README links, bumped to 1.1 so installed copies pick up the new name.

## 2026-11-04: Match AutoClicker 1.6 (v1.2)
- Did: Fixed window width (460 px) on every view and weapon; Mortar/Artillery switch also on the How to view; picked weapon is an orange pill; orange hover stroke on every button; view titles in Schibsted Grotesk ExtraBold 14, sentence case; Enemy range is AutoClicker's glowing primary pill (60 px, ExtraBold 22). Version 1.2.
- Unsure about: AutoClicker itself cannot run here (Windows only), so the match is from its code, not a side-by-side screenshot.

## 2026-11-05: Match AutoClicker 1.7 (v1.3)
- Did: Icon on a rounded ink tile (22% radius, art at 68%) with thicker crosshair lines; header mark crops the tile margin by 14% like AutoClicker; Enter-range glow peak 0.16 -> 0.20 (25% brighter, same as AutoClicker 1.7). Version 1.3.

## 2026-11-05: Centre the icon (v1.4)
- Did: cos(90°) is 6e-17, which the bar code treated as non-zero, so the top, bottom and left bars were drawn 38 px longer and the mark sat 7.7 px off centre. Rounded the direction to exact 0/1. Measured every size: equal margins on all sides, centre within 1 px. Version 1.4.
- Decided and why: The user asked to see and approve changes before anything is pushed or released. From now on: check (measure, not just look), show, wait for OK, then push.

## 2026-11-05: v1.5
- Did: Header icon no longer opens GitHub (VIEW SOURCE on How to still does). Glow peak 0.20 -> 0.24 (20% brighter; measured 4 px above the pill: red 39 -> 45). Before/after shown and approved by the user before pushing.

## 2026-11-05: Smooth pills (v1.6)
- Did: Tk canvas curves are not anti-aliased, so pills and strokes were jagged. New src/pill.py shades each pixel by coverage (pure Python, tested in tests/test_pill.py); all buttons, the hover stroke and the glowing Enemy range pill use it. Glow strength unchanged within ~5%. Approved by the user before pushing. Version 1.6.
- Unsure about: AutoClicker has the same jagged edges; user wants it noted for that project.

## 2026-11-08 · 1.7: version in the corner
- Added v1.7 at 9px, faint grey, bottom-right of the window; placed on top so nothing moves; hidden while the update stripe shows. Same corner number as Shot Tracker and AutoClicker (Jadan's request, 9px his pick).
- Checked: 73 tests pass; a picture of the window shows it in the corner, clear of the formula line.

