# Deploy and test script for Semantic Search application
Write-Host "🚀 Starting Semantic Search Application Deployment and Testing..." -ForegroundColor Green

# Function to check if a port is in use
function Test-PortInUse {
    param($port)
    $connection = New-Object System.Net.Sockets.TcpClient
    try {
        $connection.Connect("127.0.0.1", $port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to wait for a service to be ready
function Wait-ForService {
    param(
        [string]$url,
        [int]$maxAttempts = 30,
        [int]$delaySeconds = 2
    )
    
    $attempts = 0
    while ($attempts -lt $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri $url -Method GET -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Service is ready at $url" -ForegroundColor Green
                return $true
            }
        }
        catch {
            Write-Host "⏳ Waiting for service to be ready... (Attempt $($attempts + 1)/$maxAttempts)" -ForegroundColor Yellow
        }
        Start-Sleep -Seconds $delaySeconds
        $attempts++
    }
    return $false
}

# Step 1: Start Docker containers
Write-Host "`n📦 Starting Docker containers..." -ForegroundColor Cyan
docker-compose up -d

# Wait for Weaviate to be ready
Write-Host "`n⏳ Waiting for Weaviate to be ready..." -ForegroundColor Yellow
if (-not (Wait-ForService -url "http://localhost:8082/v1/meta")) {
    Write-Host "❌ Weaviate failed to start" -ForegroundColor Red
    exit 1
}

# Step 2: Start the search server
Write-Host "`n🚀 Starting the search server..." -ForegroundColor Cyan
$serverProcess = Start-Process python -ArgumentList "-m", "uvicorn", "src.search_server.main:app", "--reload", "--port", "8000" -PassThru -NoNewWindow

# Wait for the search server to be ready
Write-Host "`n⏳ Waiting for search server to be ready..." -ForegroundColor Yellow
if (-not (Wait-ForService -url "http://localhost:8000/health")) {
    Write-Host "❌ Search server failed to start" -ForegroundColor Red
    Stop-Process -Id $serverProcess.Id -Force
    exit 1
}

# Step 3: Run tests
Write-Host "`n🧪 Running tests..." -ForegroundColor Cyan
$testResult = python -m pytest test_api.py -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed" -ForegroundColor Red
    Stop-Process -Id $serverProcess.Id -Force
    exit 1
}

# Step 4: Start the demo app
Write-Host "`n🎯 Starting the demo app..." -ForegroundColor Cyan
$demoProcess = Start-Process streamlit -ArgumentList "run", "src/demo_app/app.py" -PassThru -NoNewWindow

# Wait for the demo app to be ready
Write-Host "`n⏳ Waiting for demo app to be ready..." -ForegroundColor Yellow
if (-not (Wait-ForService -url "http://localhost:8501" -maxAttempts 60)) {
    Write-Host "❌ Demo app failed to start" -ForegroundColor Red
    Stop-Process -Id $serverProcess.Id -Force
    Stop-Process -Id $demoProcess.Id -Force
    exit 1
}

Write-Host "`n✨ Deployment and testing completed successfully!" -ForegroundColor Green
Write-Host "`n📝 Application URLs:" -ForegroundColor Cyan
Write-Host "- Search Server: http://localhost:8000" -ForegroundColor White
Write-Host "- Demo App: http://localhost:8501" -ForegroundColor White
Write-Host "- Weaviate: http://localhost:8082" -ForegroundColor White
Write-Host "`n💡 Press Ctrl+C to stop all services" -ForegroundColor Yellow

# Keep the script running to maintain the services
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    # Cleanup on exit
    Write-Host "`n🛑 Stopping services..." -ForegroundColor Yellow
    Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $demoProcess.Id -Force -ErrorAction SilentlyContinue
    docker-compose down
    Write-Host "✅ Services stopped" -ForegroundColor Green
} 