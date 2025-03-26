# Semantic Search with Generative AI

A semantic search application that combines vector embeddings and Large Language Models to provide intelligent question answering and information retrieval over custom document collections.

## Architecture Overview

```
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│                   │      │                   │      │                   │
│   Demo Frontend   │<─────│   Search Server   │<─────│  Vector Database  │
│   (Streamlit)     │      │   (FastAPI)       │      │   (Weaviate)      │
│                   │      │                   │      │                   │
└───────────────────┘      └───────────────────┘      └───────────────────┘
         ▲                          ▲                          ▲
         │                          │                          │
         │                          │                          │
         │                          ▼                          │
         │                 ┌───────────────────┐              │
         │                 │                   │              │
         └─────────────────│   OpenAI API      │──────────────┘
                           │                   │
                           └───────────────────┘
```

This architecture consists of:

1. **Vector Database (Weaviate)**: Stores text documents as vectors using OpenAI embeddings
2. **Search Server (FastAPI)**: Handles document processing, vector searches, and question answering
3. **Demo Frontend (Streamlit)**: Provides a user interface for document uploads and querying
4. **OpenAI API**: Generates embeddings and answers questions based on retrieved contexts

## Project Highlights

- **Designed and implemented a full-stack Retrieval Augmented Generation (RAG) system** using FastAPI, Weaviate vector database, and OpenAI language models
- **Architected a containerized microservices solution** with Docker Compose for seamless deployment and scaling
- **Engineered text processing pipeline** that optimally chunks documents and maintains semantic relationships between sections
- **Integrated OpenAI embedding models** to convert text into high-dimensional vectors for semantic search capabilities
- **Developed REST API endpoints** for document processing, semantic search, and AI-powered question answering
- **Created resilient error handling and fallback mechanisms** ensuring system stability even during API outages
- **Optimized vector search performance** by fine-tuning embedding parameters and database configurations
- **Implemented compatibility fixes** for different versions of the OpenAI SDK, ensuring future maintainability
- **Executed comprehensive end-to-end testing** of all system components, from document ingestion to question answering
- **Documented system architecture and API endpoints** with clear examples for developers and end-users

## Features

- **Semantic Search**: Uses text embeddings from OpenAI to find relevant content based on meaning, not just keywords
- **Document Processing**: Chunks, processes, and indexes documents for efficient retrieval
- **Question Answering**: Generates answers based on relevant contexts retrieved from your document collection
- **Multi-Document Support**: Processes multiple documents and maintains their relationships
- **RESTful API**: Simple endpoints for processing text and asking questions
- **Docker Containerization**: Easy deployment with Docker and Docker Compose
- **Scalable Vector Database**: Uses Weaviate for efficient vector storage and retrieval

## Key Components

### Semantic Search Engine

The core functionality consists of:

- **Text Processor**: Splits documents into manageable chunks with appropriate overlap
- **Embedding Manager**: Generates vector embeddings using OpenAI's text-embedding-3-small model
- **Generative Search**: Combines search results with OpenAI's language models to generate accurate answers

### API Endpoints

- `/process-text`: Process and index new text
- `/ask-question`: Ask questions against the indexed documents
- `/search`: Perform semantic search over indexed documents
- `/clear-database`: Clear all indexed content
- `/health`: Check the health of the system
- `/database-contents`: Retrieve a list of all indexed text chunks

## Sample Data

The system comes preloaded with sample data covering diverse topics (50-100 words each):

- Technology (Quantum Computing, AI, Blockchain, VR)
- Science (Space Exploration, Genetic Engineering, Deep Sea Ecosystems)
- Environment (Climate Change, Renewable Energy, Biodiversity)
- Healthcare (Mediterranean Diet, Mindfulness Meditation)
- Arts & Humanities (History of Jazz, Japanese Gardens, Photography)
- Psychology & Social Sciences (Decision-Making Psychology)

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key

### Environment Setup

1. Create an `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Create API key files:
   ```bash
   echo "your_openai_api_key" > openai_api_key.txt
   echo "your_weaviate_api_key" > weaviate_api_key.txt
   ```

### Docker Deployment (Recommended)

1. Run the full deployment with sample data:
   ```bash
   docker-compose -f docker/docker-compose.full.yml up -d
   ```

2. Access the services:
   - API: http://localhost:8000
   - Demo Interface: http://localhost:8501
   - Weaviate Console: http://localhost:8082/v1/console

### API Usage

Process a document:
```bash
curl -X POST http://localhost:8000/process-text \
  -H "Content-Type: application/json" \
  -d '{"text":"Your document text here"}'
```

Ask a question:
```bash
curl -X POST http://localhost:8000/ask-question \
  -H "Content-Type: application/json" \
  -d '{"question":"Your question here", "num_search_results":3, "num_generations":1}'
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment to automatically build, test, and push Docker images to Docker Hub.

### Workflow Overview

The CI/CD pipeline consists of two main jobs:

1. **Build and Push**: Builds the Docker images for the search server and demo app, then pushes them to Docker Hub
2. **Test Deployment**: Deploys the application with Docker Compose and runs integration tests to verify functionality

### GitHub Actions Configuration

The workflow is triggered on:
- Pushes to main/master branches
- Pull requests to main/master branches
- Manual triggers via the GitHub Actions UI

### Docker Hub Images

The pipeline publishes the following images:
- `tuandung12092002/semantic-search-server`: The FastAPI backend service
- `tuandung12092002/semantic-search-demo`: The Streamlit frontend application

### Setting Up CI/CD

To use this CI/CD pipeline in your own fork:

1. Create the following secrets in your GitHub repository:
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token
   - `OPENAI_API_KEY`: Your OpenAI API key for testing

2. Push to the main/master branch or create a pull request to trigger the workflow

3. Monitor the workflow execution in the "Actions" tab of your GitHub repository

## OpenAI Version Compatibility

This project has been tested with the following OpenAI versions:
- OpenAI Python SDK v0.28.0 (Legacy API)

If you encounter issues with newer versions of the OpenAI library, the system is configured to fall back to using dummy vectors.

## Troubleshooting

### Common Issues

1. **OpenAI API Authentication Errors**:
   - Verify your API key is correctly set in the environment variables
   - Check OpenAI API usage limits and billing status

2. **Vector Database Connection Issues**:
   - Ensure Weaviate container is running and healthy
   - Check network connectivity between containers

3. **Search Returns Poor Results**:
   - Add more diverse and relevant documents to your collection
   - Experiment with different chunk sizes in the text processor

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the embedding and language models
- [Weaviate](https://weaviate.io/) for the vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Streamlit](https://streamlit.io/) for the demo interface

## Kubernetes Deployment

The application can be deployed to Kubernetes using the provided manifests in the `k8s/` directory.

### Prerequisites

- Kubernetes cluster (v1.19+)
- `kubectl` command-line tool
- Docker images pushed to your registry

### Deployment Steps

1. Create a namespace:
   ```bash
   kubectl create namespace semantic-search
   ```

2. Create secrets:
   ```bash
   kubectl create secret generic semantic-search-secrets \
     --from-literal=openai-api-key=your_openai_api_key \
     --from-literal=weaviate-api-key=your_weaviate_api_key \
     -n semantic-search
   ```

3. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f k8s/base/ -n semantic-search
   ```

4. Verify deployment:
   ```bash
   kubectl get pods -n semantic-search
   kubectl get services -n semantic-search
   ```

### Accessing the Application

- Search Server API: `http://semantic-search-server:8000`
- Demo Interface: Use the external IP of the `semantic-search-demo` service
- Weaviate Console: `http://weaviate:8080/v1/console`

## Terraform Infrastructure

The project includes Terraform configurations to set up the infrastructure on Google Cloud Platform (GCP).

### Prerequisites

- Terraform installed (v1.0+)
- Google Cloud SDK installed
- GCP project with billing enabled
- Service account with necessary permissions

### Infrastructure Components

- Google Kubernetes Engine (GKE) cluster
- Node pool with e2-standard-4 machines
- Persistent storage for Weaviate
- Network configuration and security settings

### Deployment Steps

1. Initialize Terraform:
   ```bash
   cd terraform
   terraform init
   ```

2. Configure variables:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

3. Apply the infrastructure:
   ```bash
   terraform plan
   terraform apply
   ```

4. Configure kubectl:
   ```bash
   gcloud container clusters get-credentials $(terraform output -raw cluster_name) --region $(terraform output -raw region)
   ```

### Cleanup

To remove the infrastructure:
```bash
terraform destroy
``` 