#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local max_attempts=${2:-30}
    local delay_seconds=${3:-2}
    local attempts=0

    echo -e "${YELLOW}⏳ Waiting for service to be ready at $url${NC}"
    
    while [ $attempts -lt $max_attempts ]; do
        if curl -s -f "$url" > /dev/null; then
            echo -e "${GREEN}✅ Service is ready at $url${NC}"
            return 0
        fi
        echo -e "${YELLOW}⏳ Waiting for service to be ready... (Attempt $((attempts + 1))/$max_attempts)${NC}"
        sleep $delay_seconds
        attempts=$((attempts + 1))
    done
    return 1
}

# Print header
echo -e "${GREEN}🚀 Starting Semantic Search Application Deployment and Testing...${NC}"

# Step 1: Start Docker containers
echo -e "\n${CYAN}📦 Starting Docker containers...${NC}"
docker-compose up -d

# Wait for Weaviate to be ready
if ! wait_for_service "http://localhost:8082/v1/meta"; then
    echo -e "${RED}❌ Weaviate failed to start${NC}"
    exit 1
fi

# Step 2: Start the search server
echo -e "\n${CYAN}🚀 Starting the search server...${NC}"
python -m uvicorn src.search_server.main:app --reload --port 8000 &
SERVER_PID=$!

# Wait for the search server to be ready
if ! wait_for_service "http://localhost:8000/health"; then
    echo -e "${RED}❌ Search server failed to start${NC}"
    kill $SERVER_PID
    exit 1
fi

# Step 3: Run tests
echo -e "\n${CYAN}🧪 Running tests...${NC}"
python -m pytest test_api.py -v
TEST_RESULT=$?

if [ $TEST_RESULT -ne 0 ]; then
    echo -e "${RED}❌ Tests failed${NC}"
    kill $SERVER_PID
    exit 1
fi

# Step 4: Start the demo app
echo -e "\n${CYAN}🎯 Starting the demo app...${NC}"
streamlit run src/demo_app/app.py &
DEMO_PID=$!

# Wait for the demo app to be ready
if ! wait_for_service "http://localhost:8501" 60; then
    echo -e "${RED}❌ Demo app failed to start${NC}"
    kill $SERVER_PID $DEMO_PID
    exit 1
fi

# Print success message and URLs
echo -e "\n${GREEN}✨ Deployment and testing completed successfully!${NC}"
echo -e "\n${CYAN}📝 Application URLs:${NC}"
echo -e "${WHITE}- Search Server: http://localhost:8000${NC}"
echo -e "${WHITE}- Demo App: http://localhost:8501${NC}"
echo -e "${WHITE}- Weaviate: http://localhost:8082${NC}"
echo -e "\n${YELLOW}💡 Press Ctrl+C to stop all services${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping services...${NC}"
    kill $SERVER_PID 2>/dev/null
    kill $DEMO_PID 2>/dev/null
    docker-compose down
    echo -e "${GREEN}✅ Services stopped${NC}"
    exit 0
}

# Set up trap for cleanup on script termination
trap cleanup SIGINT SIGTERM

# Keep the script running
while true; do
    sleep 1
done 