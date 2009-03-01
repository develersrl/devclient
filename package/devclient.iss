; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{2AFF7E77-E12D-42F7-880D-A52E2372B3E8}
AppName=DevClient
AppVerName=DevClient 0.8
AppPublisher=Develer s.r.l.
AppPublisherURL=http://www.develer.com
AppSupportURL=http://www.develer.com
AppUpdatesURL=http://www.develer.com
DefaultDirName={pf}\devclient
DefaultGroupName=DevClient
AllowNoIcons=yes
OutputBaseFilename=DevClient Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\*"; Excludes: "\src\test*,\resources\images*,\package*,\data\storage\*,\src\update\test*,*.ts,*.pyc,*.svn*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\DevClient"; Filename: "{app}\src\start.exe"
Name: "{commondesktop}\DevClient"; Filename: "{app}\src\start.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\DevClient"; Filename: "{app}\src\start.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\src\start.exe"; Description: "{cm:LaunchProgram,DevClient}"; Flags: nowait postinstall skipifsilent

