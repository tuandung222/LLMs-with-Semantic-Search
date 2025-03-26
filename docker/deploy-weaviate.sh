#!/bin/bash

# Stop any existing containers
echo "Stopping any existing Weaviate containers..."
docker-compose -f docker/docker-compose.weaviate.yml down

# Start Weaviate in detached mode
echo "Starting Weaviate in detached mode..."
docker-compose -f docker/docker-compose.weaviate.yml up -d

# Function to check if Weaviate is ready
check_weaviate_health() {
    if curl -s -f "http://localhost:8082/v1/meta" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Poll until Weaviate is ready
echo "Waiting for Weaviate to be ready..."
max_attempts=30
attempt=0
ready=false

while [ "$ready" = false ] && [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    echo "Attempt $attempt of $max_attempts..."
    
    if check_weaviate_health; then
        ready=true
        echo "Weaviate is ready!"
    else
        echo "Weaviate is not ready yet. Waiting 10 seconds..."
        sleep 10
    fi
done

if [ "$ready" = false ]; then
    echo "Failed to start Weaviate after $max_attempts attempts."
    exit 1
fi

echo "Weaviate deployment completed successfully!" 