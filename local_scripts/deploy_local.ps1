# PowerShell script for local deployment of search server and Streamlit demo app

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

# Function to start Weaviate if not running
function Start-Weaviate {
    Write-Host "Checking Weaviate status..."
    if (-not (Test-PortInUse 8082)) {
        Write-Host "Starting Weaviate..."
        docker-compose -f docker/docker-compose.weaviate.yml up -d
        Start-Sleep -Seconds 10  # Wait for Weaviate to start
    } else {
        Write-Host "Weaviate is already running"
    }
}

# Function to start the search server
function Start-SearchServer {
    Write-Host "Starting search server..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$(Get-Location)'; python -m uvicorn src.search_server.main:app --reload --host 0.0.0.0 --port 8000"
}

# Function to start the Streamlit demo app
function Start-StreamlitApp {
    Write-Host "Starting Streamlit demo app..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$(Get-Location)'; streamlit run src/demo_app/app.py"
}

# Main deployment process
Write-Host "Starting local deployment..."

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed or not in PATH"
    exit 1
}

# Check if Docker is running
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed or not in PATH"
    exit 1
}

# Check if required ports are available
$ports = @(8000, 8501, 8082)
foreach ($port in $ports) {
    if (Test-PortInUse $port) {
        Write-Host "Warning: Port $port is already in use. Please free up the port and try again."
        exit 1
    }
}

# Start Weaviate
Start-Weaviate

# Start the search server
Start-SearchServer

# Wait a moment for the search server to start
Start-Sleep -Seconds 5

# Start the Streamlit demo app
Start-StreamlitApp

Write-Host @"

Deployment completed! You can access:
- Search Server API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Streamlit Demo App: http://localhost:8501

Press Ctrl+C in each terminal window to stop the services.
"@ 