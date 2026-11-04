# Wardogs Range Calculator

A small Windows app for the game Wardogs. Paste your map position and the target's (from **Mark Coordinates** in chat), press **Enemy range**, and it tells you the RNG and compass heading (FACE) to set on the L81 mortar or SPH-2 artillery sight. Pick Mortar or Artillery at the top; **HOW TO** shows the steps for the weapon you picked.

## Install
Grab `RangeCalculator-Setup.exe` from the latest [release](https://github.com/jadanduffin/wardogs-range-calculator/releases/latest). It asks for admin, defaults to Program Files (any folder works), and adds Start Menu and Desktop shortcuts plus an uninstaller.

Windows may show "Windows protected your PC" because the installer is not code-signed. Click **More info**, then **Run anyway**.

## Updates
On launch the app checks the latest GitHub release. If it is newer, a `v1.x available · UPDATE` row appears; UPDATE downloads the new setup and runs it.

## Folders
- `src\` — `RangeCalculator.pyw` (the app), `rangecalc.py` (the maths), icons, `fonts\` (Schibsted Grotesk + JetBrains Mono, SIL OFL), `make_icon.py` (redraws the icon)
- `tests\` — `test_rangecalc.py` (the app's maths) and `test_calculator.py` (the web page's maths); one checks the other
- `installer\` — Inno Setup script
- `index.html` — the same calculator as a web page, for phones
- `dist\` — build output: `RangeCalculator.exe` (portable) and `RangeCalculator-Setup.exe` (installer). Not in git.

## Release a new version
Bump `VERSION` in `src\RangeCalculator.pyw` and merge to `main`. GitHub builds the installer on Windows and publishes the release (`.github/workflows/release.yml`).

To build on your own PC instead:
```
powershell -File build.ps1 -Release
```
That runs the tests, builds both exes and publishes a GitHub release tagged `v<VERSION>` with the setup attached. Installed copies see it on their next launch.

Needs Python 3.14 with pytest + PyInstaller, Inno Setup 6 (`winget install JRSoftware.InnoSetup`) and a logged-in `gh`. To redraw the icon, also install Pillow and run `python src\make_icon.py`.

Settings (last points and weapon) live in `%APPDATA%\RangeCalculator.json`.

The project-template notes this repo started from are in `docs/TEMPLATE.md`.
