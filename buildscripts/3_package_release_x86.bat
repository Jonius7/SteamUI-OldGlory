@echo off

set /p version=Enter Release Number:

7z a releases/SteamUI-OldGlory-Release_%version%.zip ./dist/old_glory_32.exe old_glory_data.json libraryroot.custom.css variables.css fixes.txt images/ themes/ scss/ README.md -xr!*.backup*