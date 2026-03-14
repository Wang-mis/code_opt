# CodeOpt Start Script
# This script starts both the frontend and backend services

$ErrorActionPreference = "Stop"

Write-Host "Starting CodeOpt services..." -ForegroundColor Green

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Start backend
Write-Host "Starting backend server..." -ForegroundColor Yellow
$BackendPath = Join-Path $ProjectRoot "backend"
Start-Process -FilePath "uv" -ArgumentList "run", "uvicorn", "app.main:app", "--reload", "--port", "8000" -WorkingDirectory $BackendPath -WindowStyle Normal

# Wait a bit for backend to start
Start-Sleep -Seconds 2

# Start frontend
Write-Host "Starting frontend server..." -ForegroundColor Yellow
$FrontendPath = Join-Path $ProjectRoot "frontend"
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory $FrontendPath -WindowStyle Normal

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Services started successfully!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to stop all services..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Stop services when key is pressed
Write-Host "Stopping services..." -ForegroundColor Yellow

# Find and stop processes on ports 8000 and 5173
$ports = @(8000, 5173)
foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
    foreach ($conn in $connections) {
        $pid = ($conn -split '\s+')[-1]
        if ($pid -match '^\d+$') {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process on port $port (PID: $pid)" -ForegroundColor Gray
        }
    }
}

Write-Host "Services stopped." -ForegroundColor Green