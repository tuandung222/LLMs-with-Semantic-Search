# Docker Deployment Options

This directory contains different Docker Compose configurations for deploying the application and database components. You can choose to deploy them separately or together based on your needs.

## Prerequisites

1. Docker and Docker Compose installed
2. Environment variables set up (copy `.env.example` to `.env` and fill in the required values)
3. OpenAI API key configured in the environment

## Deployment Options

### 1. Database Only Deployment

To deploy only the Weaviate vector database:

```bash
docker-compose -f docker-compose.db.yml up -d
```

This will:
- Start Weaviate on port 8080
- Create a persistent volume for data storage
- Set up the required network

### 2. Application Only Deployment

To deploy only the application components (API and demo):

```bash
# First ensure the database is running
docker-compose -f docker-compose.db.yml up -d

# Then start the application
docker-compose -f docker-compose.app.yml up -d
```

This will:
- Start the API service on port 8000
- Start the demo interface on port 8501
- Connect to the existing Weaviate instance

### 3. Combined Deployment

To deploy everything together:

```bash
docker-compose up -d
```

This will:
- Start Weaviate on port 8080
- Start the API service on port 8000
- Start the demo interface on port 8501
- Set up all required networks and dependencies

## Accessing the Services

- Weaviate API: http://localhost:8080
- Application API: http://localhost:8000
- Demo Interface: http://localhost:8501

## Stopping Services

To stop services, use the same commands as above but replace `up -d` with `down`:

```bash
# Stop database only
docker-compose -f docker-compose.db.yml down

# Stop application only
docker-compose -f docker-compose.app.yml down

# Stop everything
docker-compose down
```

## Notes

- The database deployment must be running before starting the application deployment
- Environment variables must be properly configured in the `.env` file
- The Weaviate network is shared between deployments to allow communication
- Data persistence is maintained through Docker volumes 