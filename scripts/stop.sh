#!/bin/bash
# CodeOpt Stop Script
# This script stops services running on specified ports

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Default ports
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -b, --backend-port PORT   Backend server port to stop (default: 8000)"
    echo "  -f, --frontend-port PORT Frontend server port to stop (default: 5173)"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                              # Stop default ports (8000, 5173)"
    echo "  $0 -b 8080                      # Stop backend on port 8080"
    echo "  $0 -b 8080 -f 3000              # Stop custom ports"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--backend-port)
            BACKEND_PORT="$2"
            shift 2
            ;;
        -f|--frontend-port)
            FRONTEND_PORT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

echo -e "${YELLOW}Stopping CodeOpt services...${NC}"

# Find and stop processes on the specified ports
PORTS=("$BACKEND_PORT" "$FRONTEND_PORT")
STOPPED=false

for PORT in "${PORTS[@]}"; do
    # Find PIDs listening on the port
    PIDS=$(lsof -t -i :$PORT 2>/dev/null || true)

    if [ ! -z "$PIDS" ]; then
        for PID in $PIDS; do
            kill $PID 2>/dev/null || true
            echo -e "${GREEN}Stopped process on port $PORT (PID: $PID)${NC}"
            STOPPED=true
        done
    fi
done

if [ "$STOPPED" = false ]; then
    echo -e "${GRAY}No services found running on ports $BACKEND_PORT or $FRONTEND_PORT${NC}"
fi

echo -e "${GREEN}Done.${NC}"