# CodeOpt Stop Script
# This script stops all services running on ports 8000 and 5173

Write-Host "Stopping CodeOpt services..." -ForegroundColor Yellow

# Find and stop processes on ports 8000 and 5173
$ports = @(8000, 5173)
$stopped = $false

foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
    foreach ($conn in $connections) {
        $pid = ($conn -split '\s+')[-1]
        if ($pid -match '^\d+$') {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process on port $port (PID: $pid)" -ForegroundColor Green
            $stopped = $true
        }
    }
}

if (-not $stopped) {
    Write-Host "No services found running on ports 8000 or 5173" -ForegroundColor Gray
}

Write-Host "Done." -ForegroundColor Green