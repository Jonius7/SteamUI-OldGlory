@echo off

echo You are about to add steam-library's CSS to SteamUI-OldGlory's CSS.
echo Please make sure you have libraryroot.custom.css, config.css, and steam-library_compat.css in folder
echo You only need to do this once.
setlocal
set/P AREYOUSURE=Would you like to continue (Y/N)? 
if /I "%AREYOUSURE%" NEQ "Y" goto END
endlocal
echo ========================
set "libraryroot=libraryroot.custom.css"
set "compat=steam-library_compat.css"
set "temp=hybrid.temp.css"

::Just so it won't keep adding the compat text if you've done it already
if exist %libraryroot%.backup echo libraryroot.custom.css.backup exists, skipping. Delete or rename the file if you want to add the CSS.
::if exist %libraryroot%.backup goto AFTER
set /p firstline=< %libraryroot%
set "compareline=!!! DO NOT EDIT THESE !!!"

::if not "x!firstline:%compareline%=!"=="x%firstline%" echo libraryroot.custom.css has already been patched, skipping.
::if not "x!firstline:%compareline%=!"=="x%firstline%" goto AFTER

echo.%firstline%|findstr /C:"%compareline%" >nul 2>&1
if not errorlevel 1 (
   echo libraryroot.custom.css already has steam-library's CSS, skipping.
   goto AFTER
) else (
	type %compat% >> %temp%
	echo. >> %temp%
	echo. >> %temp%
	type %libraryroot% >> %temp%
	rename %libraryroot% %libraryroot%.backup
	rename %temp% %libraryroot%
	echo CSS Added.
	echo A backup of your library CSS has been saved to libraryroot.custom.css.backup
)

:AFTER

::Modify steam-library's config.css

echo Some values in steam-library's config.css will now be changed

set "textfile=config.css"
set "tempfile=config-temp.css"

set "search1=--FontSize: 15px;"
set "replace1=--FontSize: 13px;"
set "search2=--YourLibraryName: "YOUR LIBRARY""
set "replace2=--YourLibraryName: "HOME""
set "search3=--LetterSpacing: 3px"
set "replace3=--LetterSpacing: 0px"
set "search4=--ButtonPlayHover: #70d61d;"
set "replace4=--ButtonPlayHover: var^(--libraryhome^)^;"
set "search5=--ButtonPlayHover2: #01a75b;"
set "replace5=--ButtonPlayHover2: var^(--libraryhome^)^;"
set "search6=--ButtonInstallHover: #47bfff;"
set "replace6=--ButtonInstallHover: var^(--libraryhome^)^;"
set "search7=--ButtonInstallHover2: #1a44c2;"
set "replace7=--ButtonInstallHover2: var^(--libraryhome^)^;"
set "searchA=--GameIcons: none;"
set "replaceA=--GameIcons: block;"

(for /f "delims=" %%L in ('findstr /n "^" "%textfile%"') do (
	set line=%%L
	setlocal enabledelayedexpansion
	set line=!line:%search1%=%replace1%!
	set line=!line:%search2%=%replace2%!
	set line=!line:%search3%=%replace3%!
	set line=!line:%search4%=%replace4%!
	set line=!line:%search5%=%replace5%!
	set line=!line:%search6%=%replace6%!
	set line=!line:%search7%=%replace7%!
	set line=!line:%searchA%=%replaceA%!
	set line=!line:*:=!
	echo(!line!
	endlocal
))>"%tempfile%"

if exist %textfile%.backup del %textfile%
if not exist %textfile%.backup rename %textfile% %textfile%.backup
rename %tempfile% %textfile%

:END
endlocal
pause