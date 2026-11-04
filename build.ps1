# Builds dist\RangeCalculator.exe (PyInstaller) and dist\RangeCalculator-Setup.exe (Inno Setup). Run from anywhere.
# -Release also publishes a GitHub release tagged with the version in RangeCalculator.pyw (what the app's update check looks for).
param([switch]$Release)
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$src = "$root\src"
$work = "$env:TEMP\RangeCalculator-build"
$ver = (Select-String -Path "$src\RangeCalculator.pyw" -Pattern 'RANGECALC_VERSION", "([\d.]+)"').Matches[0].Groups[1].Value
"version $ver"

python -m pytest -q "$root\tests\test_rangecalc.py" -k "not matches_the_web_page"  # the maths must pass before anything ships
if ($LASTEXITCODE) { throw "tests failed" }

python -m PyInstaller --noconfirm --onefile --noconsole --name RangeCalculator `
    --icon "$src\RangeCalculator.ico" `
    --paths "$src" `
    --add-data "$src\icon-56.png;." `
    --add-data "$src\RangeCalculator.ico;." `
    --add-data "$src\fonts;fonts" `
    --distpath "$root\dist" --workpath $work --specpath $work "$src\RangeCalculator.pyw"
if ($LASTEXITCODE) { throw "PyInstaller failed" }

$iscc = Get-ChildItem "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe", "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $iscc) { throw "Inno Setup 6 not found (winget install JRSoftware.InnoSetup)" }
& $iscc.FullName /Q "/DAppVersion=$ver" "$root\installer\RangeCalculator.iss"
if ($LASTEXITCODE) { throw "Inno Setup failed" }

Get-Item "$root\dist\RangeCalculator.exe", "$root\dist\RangeCalculator-Setup.exe" | Format-Table Name, @{n="MB"; e={[math]::Round($_.Length / 1MB, 1)}}

if ($Release) {
    gh release create "v$ver" "$root\dist\RangeCalculator-Setup.exe" --title "Range Calculator $ver" --generate-notes
    if ($LASTEXITCODE) { throw "gh release failed" }
}
