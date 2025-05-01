@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM --- Get script directory ---
set "SCRIPT_DIR=%~dp0"

REM --- Settings ---
set INPUT_SPEC=openapi\binance\openapi.yaml
set OUTPUT_DIR=generated\binance_python_client

echo [INFO] Current directory: %CD%
echo [INFO] Script directory: %SCRIPT_DIR%
echo [INFO] OpenAPI specification file: %INPUT_SPEC%
echo [INFO] Output directory: %OUTPUT_DIR%

REM --- Check if Java is available ---
where java >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Java not found. Please install Java and add it to PATH.
    goto :eof
)

REM --- Check if openapi-generator-cli is available ---
where openapi-generator-cli >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] openapi-generator-cli not found.
    echo [TIP] Please install first: npm install @openapitools/openapi-generator-cli -g
    goto :eof
)

REM --- First run the split script ---
echo [INFO] Running split script to generate modular OpenAPI specification files...
python "%SCRIPT_DIR%split_endpoint.py"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to split OpenAPI specification files.
    goto :eof
)

REM --- Check if OpenAPI specification file exists ---
if not exist "%INPUT_SPEC%" (
    echo [ERROR] OpenAPI specification file not found: %INPUT_SPEC%
    goto :eof
)

REM --- Clean up old output directory (if exists) ---
if exist "%OUTPUT_DIR%" (
    echo [INFO] Cleaning up old output directory: %OUTPUT_DIR%
    rd /s /q "%OUTPUT_DIR%"
)

REM --- Generate Python client ---
echo [INFO] Using %INPUT_SPEC% to generate Binance Python client to %OUTPUT_DIR% ...

mkdir "%OUTPUT_DIR%" 2>nul

echo [INFO] Using openapi-generator-cli to generate code...
openapi-generator-cli generate -i %INPUT_SPEC% -g python -o %OUTPUT_DIR% --skip-validate-spec --additional-properties=packageName=binance_client,useTags=true,enumPropertyNaming=UPPERCASE

if %errorlevel% neq 0 (
    echo [ERROR] Failed to generate Binance Python client.
    goto :eof
)

echo.
echo [SUCCESS] Binance Python client has been successfully generated at: %OUTPUT_DIR%
echo [TIP] You can navigate to %OUTPUT_DIR% and follow the instructions to install and use.

endlocal
pause
exit /b 0

:eof
pause
exit /b 1
