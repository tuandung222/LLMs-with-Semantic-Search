#!/usr/bin/env pwsh
# Script to run Docker Compose with proper environment variables

# Load environment variables from .env file
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Write-Host "Loading environment variables from $envFile"
    Get-Content $envFile | Where-Object { $_ -match '^[^#]' } | ForEach-Object {
        $key, $value = $_ -split '=', 2
        if ($key -and $value) {
            [Environment]::SetEnvironmentVariable($key, $value)
            Write-Host "Set $key environment variable"
        }
    }
} else {
    Write-Error ".env file not found at $envFile"
    exit 1
}

# Verify key environment variables
if (-not [Environment]::GetEnvironmentVariable("OPENAI_API_KEY")) {
    Write-Error "OPENAI_API_KEY is not set in the .env file or is empty"
    exit 1
}

# Change to docker directory
$dockerDir = Join-Path $PSScriptRoot "docker"
Set-Location $dockerDir

# Run Docker Compose
Write-Host "Starting Docker Compose..."
docker-compose -f docker-compose.full.yml down
docker-compose -f docker-compose.full.yml up --build 