@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "SPECS_DIR=%SCRIPT_DIR%specs"
set "OUTPUT_FILE=%SPECS_DIR%\specs.txt"

if not exist "%SPECS_DIR%" mkdir "%SPECS_DIR%"

systeminfo > "%OUTPUT_FILE%"
echo Saved specs to: "%OUTPUT_FILE%"
echo.
type "%OUTPUT_FILE%"

endlocal
