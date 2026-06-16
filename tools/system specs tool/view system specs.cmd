@echo off
setlocal

set "OUTPUT_FILE=%~dp0specs\specs.txt"

if not exist "%OUTPUT_FILE%" (
    echo Specs file not found: "%OUTPUT_FILE%"
    echo Run system_dump first to generate it.
    exit /b 1
)

echo Viewing specs from: "%OUTPUT_FILE%"
echo.
type "%OUTPUT_FILE%"

endlocal
