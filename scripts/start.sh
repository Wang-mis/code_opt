#!/bin/bash
# CodeOpt Start Script
# This script starts both the frontend and backend services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
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
    echo "  -b, --backend-port PORT   Backend server port (default: 8000)"
    echo "  -f, --frontend-port PORT Frontend server port (default: 5173)"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                              # Use default ports (8000, 5173)"
    echo "  $0 -b 8080                      # Backend on port 8080"
    echo "  $0 -f 3000                      # Frontend on port 3000"
    echo "  $0 -b 8080 -f 3000              # Custom ports for both"
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

# Validate ports
if ! [[ "$BACKEND_PORT" =~ ^[0-9]+$ ]] || [ "$BACKEND_PORT" -lt 1 ] || [ "$BACKEND_PORT" -gt 65535 ]; then
    echo -e "${RED}Invalid backend port: $BACKEND_PORT${NC}"
    exit 1
fi

if ! [[ "$FRONTEND_PORT" =~ ^[0-9]+$ ]] || [ "$FRONTEND_PORT" -lt 1 ] || [ "$FRONTEND_PORT" -gt 65535 ]; then
    echo -e "${RED}Invalid frontend port: $FRONTEND_PORT${NC}"
    exit 1
fi

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${GREEN}Starting CodeOpt services...${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Stopping services...${NC}"

    # Kill backend process
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        echo -e "${GRAY}Stopped backend (PID: $BACKEND_PID)${NC}"
    fi

    # Kill frontend process
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo -e "${GRAY}Stopped frontend (PID: $FRONTEND_PID)${NC}"
    fi

    echo -e "${GREEN}Services stopped.${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${YELLOW}Starting backend server on port $BACKEND_PORT...${NC}"
cd "$PROJECT_ROOT/backend"
uv run uvicorn app.main:app --reload --port "$BACKEND_PORT" &
BACKEND_PID=$!
cd - > /dev/null

# Wait a bit for backend to start
sleep 2

# Start frontend
echo -e "${YELLOW}Starting frontend server on port $FRONTEND_PORT...${NC}"
cd "$PROJECT_ROOT/frontend"
VITE_BACKEND_PORT="$BACKEND_PORT" pnpm dev --port "$FRONTEND_PORT" &
FRONTEND_PID=$!
cd - > /dev/null

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Services started successfully!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${CYAN}Frontend: http://localhost:$FRONTEND_PORT${NC}"
echo -e "${CYAN}Backend:  http://localhost:$BACKEND_PORT${NC}"
echo -e "${CYAN}API Docs: http://localhost:$BACKEND_PORT/docs${NC}"
echo ""
echo -e "${GRAY}Press Ctrl+C to stop all services...${NC}"

# Wait for processes
wait