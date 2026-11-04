; Inno Setup script: wraps dist\RangeCalculator.exe into dist\RangeCalculator-Setup.exe.
; Asks for admin up front (UAC), defaults to Program Files, and lets the user pick any folder on the directory page.
#define AppName "Range Calculator"
#ifndef AppVersion
  #define AppVersion "0.0"  ; build.ps1 passes the real one from RangeCalculator.pyw via /DAppVersion=
#endif
#define AppExe "RangeCalculator.exe"

[Setup]
AppId={{3B9E6C1A-8D42-4F7E-B5A1-6E2D9C0F4A83}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Jadan Duffin
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
PrivilegesRequired=admin
DisableDirPage=no
OutputDir=..\dist
OutputBaseFilename=RangeCalculator-Setup
SetupIconFile=..\src\RangeCalculator.ico
UninstallDisplayIcon={app}\{#AppExe}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{userappdata}\RangeCalculator.json"
