# Use OpenAPI Generator to generate Python API client
# Usage: ./run_api_generator.ps1 [OpenAPI file path] [output directory] [package name]

param (
    [string]$OpenApiFile = "./openapi/binance/openapi.yaml",
    
    [string]$OutputDir = "./generated/binance_client",
    
    [string]$PackageName = "binance_client"
)

# Check if the OpenAPI file exists, if not, show error and exit
if (-not (Test-Path $OpenApiFile)) {
    Write-Host "Error: OpenAPI file $OpenApiFile not found" -ForegroundColor Red
    exit 1
}

# Check if OpenAPI Generator CLI is installed
try {
    $generatorVersion = openapi-generator-cli version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "OpenAPI Generator CLI is not installed"
    }
    Write-Host "OpenAPI Generator CLI installed: $generatorVersion" -ForegroundColor Green
} 
catch {
    Write-Host "OpenAPI Generator CLI not found, trying to install using npm..." -ForegroundColor Yellow
    npm install @openapitools/openapi-generator-cli -g
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install OpenAPI Generator CLI, please install it manually and try again" -ForegroundColor Red
        exit 1
    }
}

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -Path $OutputDir -ItemType Directory | Out-Null
    Write-Host "Created output directory: $OutputDir" -ForegroundColor Yellow
}

# Run OpenAPI Generator to generate Python client
Write-Host "Starting to generate Python API client..." -ForegroundColor Cyan

$cmdArgs = @(
    "generate",
    "-i", $OpenApiFile,
    "-g", "python",
    "-o", $OutputDir,
    "--package-name", $PackageName,
    "--skip-validate-spec"
)

Write-Host "Running command: openapi-generator-cli $($cmdArgs -join ' ')" -ForegroundColor Gray
openapi-generator-cli $cmdArgs

# Check the result
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuccessfully generated Python API client to: $OutputDir" -ForegroundColor Green
    Write-Host "Generated package name: $PackageName" -ForegroundColor Green
    
    Write-Host "`nUsage:" -ForegroundColor Cyan
    Write-Host "cd $OutputDir" -ForegroundColor White
    Write-Host "pip install -e ." -ForegroundColor White
    Write-Host "import $PackageName" -ForegroundColor White
} 
else {
    Write-Host "An error occurred during generation" -ForegroundColor Red
    exit 1
} 