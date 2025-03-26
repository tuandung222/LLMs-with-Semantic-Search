# Semantic Search with Generative AI

A production-ready semantic search application that combines vector embeddings and Large Language Models to provide intelligent question answering and information retrieval over custom document collections. The system features a self-hosted Weaviate vector database for complete control over your data, without relying on external vector database services.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Highlights](#project-highlights)
- [Features](#features)
- [Key Components](#key-components)
- [Getting Started](#getting-started)
- [API Usage](#api-usage)
- [API Reference](#api-reference)
- [Deployment Options](#deployment-options)
  - [Docker Deployment](#docker-deployment-recommended)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Cloud Infrastructure with Terraform](#terraform-infrastructure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## 🏗️ Architecture Overview

```mermaid
flowchart TB
    subgraph Frontend["Demo Frontend (Streamlit)"]
        DocUI["Document Upload UI"]
        QuesUI["Question Input UI"]
        ResUI["Results Display UI"]
    end

    subgraph Server["Search Server (FastAPI)"]
        TextProc["TextProcessor<br>Clean & Chunk Text"]
        EmbMgr["EmbeddingManager<br>Create & Cache Embeddings"]
        GenSearch["GenerativeSearch<br>Answer Gen. with Context"]
        
        TextProc --> EmbMgr
        EmbMgr --> GenSearch
    end
    
    subgraph SelfHosted["Self-Hosted Infrastructure"]
        VecDB["Vector Database<br>(Weaviate)"]
        SampleData["Sample Data<br>Text Samples & Metadata"]
    end
    
    subgraph External["External Services"]
        OpenAI["OpenAI API"]
    end
    
    DocUI --> TextProc
    QuesUI --> EmbMgr
    GenSearch --> ResUI
    
    TextProc <-- Raw Text --> SampleData
    EmbMgr <-- Vectors --> VecDB
    GenSearch <-- Prompts --> OpenAI
    
    classDef frontend fill:#e6f7ff,stroke:#0099cc
    classDef server fill:#e6ffe6,stroke:#00cc66
    classDef selfhosted fill:#e6e6ff,stroke:#6666cc
    classDef external fill:#fff0e6,stroke:#ff9933
    
    class Frontend frontend
    class Server server
    class SelfHosted selfhosted
    class External external
```

> **IMPORTANT:** Unlike many other RAG solutions that rely on cloud-based vector databases, this system includes a **self-hosted Weaviate vector database** deployed alongside the application components. This architectural choice provides full control over your data, eliminates external dependencies, and enhances privacy and security.

### Core Components and Data Flow

1. **Search Server (FastAPI)**

   - **TextProcessor**: Document preprocessing and chunking
   - **EmbeddingManager**: Vector operations and caching
   - **GenerativeSearch**: Search and answer generation

2. **Self-Hosted Vector Database (Weaviate)**

   - Containerized vector database deployed with the application
   - Full control over vector data storage and configuration
   - No external cloud vector database dependencies
   - Scalable vector storage and search
   - Document metadata management
   - Real-time similarity search

3. **OpenAI Integration**

   - Embedding Generation (text-embedding-3-small)
   - Text Generation (GPT-3.5 Turbo)
   - Configurable parameters

4. **Data Pipelines**

   ```
   Document Processing:
   Raw Text → TextProcessor → Chunks → EmbeddingManager → Vectors → Weaviate

   Question Answering:
   Question → EmbeddingManager → Similar Chunks → GenerativeSearch → Answer

   Sample Data:
   Sample Data → TextProcessor → EmbeddingGenerator → Cached Vectors → Weaviate
   ```

## ✨ Features

### Core Capabilities

- **Advanced Semantic Search**

  - Meaning-based content discovery
  - Multi-document context awareness
  - Configurable search parameters

- **Intelligent Document Processing**

  - Automatic text chunking
  - Semantic relationship preservation
  - Multiple document format support

- **AI-Powered Question Answering**
  - Context-aware responses
  - Multiple generation options
  - Confidence scoring

### Technical Features

- **Production-Ready Architecture**

  - Fault tolerance and fallbacks
  - Efficient caching system
  - Comprehensive monitoring
  - Secure key management

- **Developer-Friendly API**

  - RESTful endpoints
  - Comprehensive documentation
  - Example implementations

- **Robust Data Management**
  - Vector database optimization
  - Efficient data indexing
  - Backup and recovery options

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- OpenAI API key
- (Optional) Kubernetes cluster for k8s deployment
- (Optional) GCP account for Terraform deployment

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/tuandung12092002/semantic-search.git
   cd semantic-search
   ```

2. **Set up environment**

   ```bash
   # Create environment files
   cp .env.example .env
   echo "your_openai_api_key" > openai_api_key.txt
   echo "your_weaviate_api_key" > weaviate_api_key.txt
   ```

3. **Start the application**

   ```bash
   docker-compose -f docker/docker-compose.full.yml up -d
   ```

4. **Access the services**
   - Demo UI: http://localhost:8501
   - API Docs: http://localhost:8000/docs
   - Weaviate Console: http://localhost:8082/v1/console

## 🔧 API Usage

### Process Documents

```bash
curl -X POST http://localhost:8000/process-text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your document content here",
    "metadata": {
      "source": "example.pdf",
      "author": "John Doe"
    }
  }'
```

### Ask Questions

   ```bash
curl -X POST http://localhost:8000/ask-question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is semantic search?",
    "num_search_results": 3,
    "num_generations": 1,
    "temperature": 0.7
  }'
```

### Search Documents

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "quantum computing applications",
    "limit": 5
  }'
```

## 🔄 CI/CD Pipeline

### ✅ Build Status

[![Build and Push Docker Images](https://github.com/tuandung12092002/semantic-search/actions/workflows/docker-build-push.yml/badge.svg)](https://github.com/tuandung12092002/semantic-search/actions/workflows/docker-build-push.yml)
[![Lint and Test](https://github.com/tuandung12092002/semantic-search/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/tuandung12092002/semantic-search/actions/workflows/lint-and-test.yml)
[![Test Deployment](https://github.com/tuandung12092002/semantic-search/actions/workflows/test-deployment.yml/badge.svg)](https://github.com/tuandung12092002/semantic-search/actions/workflows/test-deployment.yml)

All CI/CD pipelines for this project are **successfully passing**. The Docker images have been built, tested, and pushed to the [Docker Hub Registry](https://hub.docker.com/r/tuandung12092002/semantic-search-server/tags). Each component has undergone rigorous testing to ensure reliability and performance.

- **Docker Images**: [tuandung12092002/semantic-search-server](https://hub.docker.com/r/tuandung12092002/semantic-search-server/tags) and [tuandung12092002/semantic-search-demo](https://hub.docker.com/r/tuandung12092002/semantic-search-demo/tags)
- **API Testing**: All endpoints have been tested for functionality and performance
- **Integration Testing**: Full system integration tests passed successfully
- **Security Scanning**: Container and dependency vulnerabilities checked

You can verify the CI/CD pipeline status by checking the [GitHub Actions tab](https://github.com/tuandung12092002/semantic-search/actions) in the repository.

### Workflow Overview

- **Automated Testing**: Unit and integration tests
- **Docker Image Building**: Multi-stage builds with caching
- **Deployment**: Automated deployment to staging/production
- **Security Scans**: Dependency and container scanning

### Configuration

1. **Required Secrets**

   - `DOCKERHUB_TOKEN`: Docker Hub access token
   - `OPENAI_API_KEY`: OpenAI API key
   - `WEAVIATE_API_KEY`: Weaviate API key

2. **Workflow Triggers**
   - Push to main/master
   - Pull requests
   - Manual dispatch

## 🔌 API Reference

### API Overview

The semantic search application exposes a RESTful API that enables interaction with the search functionality. All endpoints are available at `http://localhost:8000` when running locally.

### Authentication

Currently, the API uses API key authentication. Include your API key in the request headers:

```
X-API-Key: your_api_key_here
```

### Base URL

```
http://localhost:8000
```

In production environments with Kubernetes, the base URL depends on your ingress configuration.

### Endpoints

#### 1. Health Check

```
GET /health
```

Verify that the API server is running and healthy.

**Response Example:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2023-03-26T12:34:56Z"
}
```

#### 2. Process Text

```
POST /process-text
```

Process and index a document in the vector database.

**Request Body:**

```json
{
  "text": "Your document content here. This can be a long text that will be chunked automatically.",
  "metadata": {
    "source": "example.pdf",
    "author": "John Doe",
    "title": "Example Document",
    "date": "2023-03-26"
  }
}
```

**Response Example:**

```json
{
  "success": true,
  "message": "Document processed successfully",
  "chunks": 5,
  "vector_ids": ["id1", "id2", "id3", "id4", "id5"]
}
```

**Status Codes:**
- `200 OK`: Document processed successfully
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Processing error

#### 3. Ask Question

```
POST /ask-question
```

Ask a question and get an AI-generated answer based on the indexed documents.

**Request Body:**

```json
{
  "question": "What is semantic search?",
  "num_search_results": 3,
  "num_generations": 1,
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Parameters:**
- `question`: The question to answer
- `num_search_results`: Number of relevant text chunks to retrieve (default: 3)
- `num_generations`: Number of different answers to generate (default: 1)
- `temperature`: Creativity of the response (0.0-1.0, default: 0.7)
- `max_tokens`: Maximum response length (default: 500)

**Response Example:**

```json
{
  "answers": [
    "Semantic search is a search technique that understands the contextual meaning of the search terms, rather than just matching keywords. It uses vector embeddings to represent the meaning of text and finds results based on semantic similarity."
  ],
  "documents": [
    "Semantic search represents a significant advancement over traditional keyword-based search methods. By leveraging vector representations of text, it can understand the meaning and context of search queries.",
    "Unlike keyword search, semantic search can identify related concepts even when the exact words don't match. This is achieved through vector embeddings that capture semantic relationships.",
    "Modern semantic search systems often combine machine learning, natural language processing, and vector databases to deliver relevant results based on meaning rather than exact word matches."
  ],
  "relevance_scores": [0.92, 0.87, 0.81]
}
```

**Status Codes:**
- `200 OK`: Question answered successfully
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Processing error

#### 4. Search Documents

```
POST /search
```

Search for documents in the vector database without generating an answer.

**Request Body:**

```json
{
  "query": "quantum computing applications",
  "limit": 5,
  "with_vectors": false
}
```

**Parameters:**
- `query`: The search query
- `limit`: Maximum number of results to return (default: 5)
- `with_vectors`: Whether to include vector embeddings in response (default: false)

**Response Example:**

```json
{
  "results": [
    {
      "text": "Quantum computing applications span many fields including cryptography, optimization problems, and drug discovery. The ability to process multiple states simultaneously offers exponential speedups for certain algorithms.",
      "metadata": {
        "source": "quantum_overview.pdf",
        "page": 12
      },
      "relevance": 0.95
    },
    {
      "text": "In financial modeling, quantum algorithms can analyze market data and portfolio optimization scenarios faster than classical computers, potentially revolutionizing trading strategies.",
      "metadata": {
        "source": "quantum_finance.pdf",
        "page": 4
      },
      "relevance": 0.88
    }
  ],
  "total_results": 2,
  "query_vector_id": "query_12345"
}
```

**Status Codes:**
- `200 OK`: Search completed successfully
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Search error

#### 5. Get Database Contents

```
GET /database-contents?limit=100
```

Retrieve the contents stored in the vector database.

**Parameters:**
- `limit`: Maximum number of documents to return (default: 100)

**Response Example:**

```json
{
  "contents": [
    {
      "text": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
      "metadata": {
        "source": "ai_intro.pdf"
      }
    },
    {
      "text": "Machine learning is a subset of artificial intelligence...",
      "metadata": {
        "source": "ml_basics.pdf"
      }
    }
  ],
  "total_count": 2
}
```

### Error Responses

All endpoints return standard error responses:

```json
{
  "error": true,
  "message": "Detailed error message",
  "code": "ERROR_CODE"
}
```

### Rate Limiting

The API implements rate limiting to prevent abuse:

- 100 requests per minute per IP address
- 5 requests per minute for `/process-text` endpoint

### OpenAPI Documentation

The complete API documentation is available via Swagger UI at:

```
http://localhost:8000/docs
```

Or ReDoc at:

```
http://localhost:8000/redoc
```

## 🛠️ Development Guide

### Local Development

1. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Install development dependencies**

   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Maintain test coverage

## ❗ Troubleshooting

### Common Issues and Solutions

1. **OpenAI API Issues**

   - **Error**: Authentication failed
     ```
     Solution: Check API key in .env and secrets
     ```
   - **Error**: Rate limit exceeded
     ```
     Solution: Implement request throttling or upgrade API tier
     ```

2. **Docker Issues**

   - **Error**: Container fails to start
     ```
     Solution: Check logs with `docker-compose logs`
     ```
   - **Error**: Memory limits
     ```
     Solution: Adjust Docker resource allocation
     ```

3. **Vector Database Issues**
   - **Error**: Connection timeout
     ```
     Solution: Verify Weaviate container health
     ```
   - **Error**: Index corruption
     ```
     Solution: Rebuild index with provided script
     ```

## 📚 Additional Resources

- [API Documentation](https://github.com/tuandung12092002/semantic-search/wiki/API-Documentation)
- [Development Guide](https://github.com/tuandung12092002/semantic-search/wiki/Development-Guide)
- [Deployment Guide](https://github.com/tuandung12092002/semantic-search/wiki/Deployment-Guide)
- [Contributing Guidelines](https://github.com/tuandung12092002/semantic-search/blob/main/CONTRIBUTING.md)
- [Change Log](https://github.com/tuandung12092002/semantic-search/blob/main/CHANGELOG.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI team for their excellent API and models
- Weaviate team for the vector database
- FastAPI and Streamlit teams for their frameworks
- The open-source community for their contributions

## 📁 Project Structure

```
semantic-search/
├── .github/                      # GitHub configuration 
│   └── workflows/                # GitHub Actions CI/CD workflows
│       ├── docker-build-push.yml # Workflow for building and pushing Docker images
│       ├── lint-and-test.yml     # Workflow for code linting and testing
│       └── test-deployment.yml   # Workflow for testing the deployment
│
├── docker/                       # Docker configuration
│   ├── demo_app.Dockerfile       # Dockerfile for Streamlit demo frontend
│   ├── search_server.Dockerfile  # Dockerfile for FastAPI search server
│   └── docker-compose.full.yml   # Docker Compose configuration for all services
│
├── src/                          # Source code
│   ├── demo_app/                 # Streamlit frontend application
│   │   └── app.py                # Main Streamlit app entry point
│   │
│   ├── search_server/            # FastAPI server application
│   │   ├── api/                  # API endpoints definitions
│   │   └── main.py               # FastAPI server entry point
│   │
│   └── semantic_search/          # Core semantic search functionality
│       ├── config.py             # Configuration and settings
│       ├── embedding_manager.py  # Vector embeddings generation and management
│       ├── generative_search.py  # Combines search with LLM generation
│       ├── sample_data.py        # Example data for demonstration
│       ├── search_interface.py   # Main interface for search operations
│       └── text_processor.py     # Text chunking and preprocessing
│
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests for individual components
│   └── integration/              # Integration tests across components
│
├── .env.example                  # Example environment variables
├── CONTRIBUTING.md               # Contribution guidelines
├── DEVELOPMENT.md                # Development setup and guidelines
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── setup.py                      # Package installation script
```

### Key Components

#### 1. Docker Configuration
- **demo_app.Dockerfile**: Containerizes the Streamlit frontend
- **search_server.Dockerfile**: Containerizes the FastAPI backend
- **docker-compose.full.yml**: Orchestrates all services (Weaviate, Search Server, Demo App)

#### 2. Source Code
- **demo_app**: Interactive Streamlit frontend for document uploading and question answering
- **search_server**: FastAPI backend exposing REST endpoints for semantic search operations
- **semantic_search**: Core library implementing vector search and LLM integration

#### 3. CI/CD Pipeline
- **docker-build-push.yml**: Builds and publishes Docker images
- **lint-and-test.yml**: Verifies code quality and runs automated tests
- **test-deployment.yml**: Validates deployment functionality

#### 4. Documentation
- **README.md**: Main project documentation
- **DEVELOPMENT.md**: Guide for developers
- **CONTRIBUTING.md**: Guidelines for contributors

### Service Architecture

The project consists of three main services, all running in Docker containers:

1. **Self-Hosted Weaviate Vector Database**: 
   - Deployed as a containerized service alongside your application
   - Stores document embeddings and enables similarity search
   - Provides complete control over your vector data
   - Eliminates dependency on external vector database services
   - Configured for optimal performance with your specific data needs

2. **Search Server (FastAPI)**: 
   - Processes documents, generates embeddings, and serves search requests
   - Communicates directly with the self-hosted Weaviate instance
   - Handles all vector operations without external dependencies

3. **Demo Frontend (Streamlit)**: 
   - Provides a user-friendly interface for interacting with the system
   - Connects to the Search Server API for document processing and querying

## 🌟 Project Highlights

- **Designed and implemented a full-stack RAG system** using FastAPI, Weaviate, and OpenAI
- **Architected a containerized microservices solution** with Docker Compose for local development
- **Deployed a fully self-hosted vector database** for complete data control and privacy
- **Implemented CI/CD pipelines with GitHub Actions** for automated testing, building, and deployment
- **Created Kubernetes manifests for production deployment** with scalability and high availability
- **Configured Terraform IaC** for reproducible cloud infrastructure provisioning
- **Set up automated Docker image publishing** to Docker Hub registry with versioning
- **Engineered an intelligent text processing pipeline** for optimal document chunking
- **Developed comprehensive REST API endpoints** with OpenAPI documentation
- **Implemented secure secrets management** across local and cloud environments
- **Optimized vector search performance** through database configuration and query tuning
- **Created resilient error handling mechanisms** with fallbacks for all external dependencies

## Deployment Options

### Docker Deployment (Recommended)

This is covered in the [Getting Started](#getting-started) section.

### Kubernetes Deployment

Deploy the semantic search application on Kubernetes for production environments with enhanced scalability and resilience.

#### Prerequisites

- Kubernetes cluster (GKE, EKS, AKS, or local cluster like Minikube/Kind)
- kubectl CLI configured to access your cluster
- Helm v3+

#### Deployment Steps

1. **Create Kubernetes Secret for API Keys**

   ```bash
   kubectl create namespace semantic-search

   # Create secrets for API keys
   kubectl create secret generic api-keys \
     --from-file=openai-api-key=./openai_api_key.txt \
     --from-file=weaviate-api-key=./weaviate_api_key.txt \
     -n semantic-search
   ```

2. **Deploy Vector Database (Weaviate)**

   ```bash
   kubectl apply -f k8s/weaviate-deployment.yaml -n semantic-search
   kubectl apply -f k8s/weaviate-service.yaml -n semantic-search
   
   # Wait for Weaviate to be ready
   kubectl wait --for=condition=ready pod -l app=weaviate -n semantic-search --timeout=180s
   ```

3. **Deploy Search Server**

   ```bash
   kubectl apply -f k8s/search-server-deployment.yaml -n semantic-search
   kubectl apply -f k8s/search-server-service.yaml -n semantic-search
   
   # Wait for search server to be ready
   kubectl wait --for=condition=ready pod -l app=search-server -n semantic-search --timeout=180s
   ```

4. **Deploy Demo Frontend**

   ```bash
   kubectl apply -f k8s/demo-app-deployment.yaml -n semantic-search
   kubectl apply -f k8s/demo-app-service.yaml -n semantic-search
   ```

5. **Create Ingress (Optional)**

   ```bash
   kubectl apply -f k8s/ingress.yaml -n semantic-search
   ```

6. **Verify Deployment**

   ```bash
   kubectl get pods,svc,ingress -n semantic-search
   ```

#### Scaling Configuration

The application components can be scaled independently based on workload:

- **Vector Database**: Scale with StatefulSet for data persistence
   ```bash
   kubectl scale statefulset weaviate --replicas=3 -n semantic-search
   ```

- **Search Server**: Scale to handle more concurrent API requests
   ```bash
   kubectl scale deployment search-server --replicas=5 -n semantic-search
   ```

- **Demo Frontend**: Scale based on user traffic
   ```bash
   kubectl scale deployment demo-app --replicas=2 -n semantic-search
   ```

#### Monitoring and Maintenance

- **View Logs**
   ```bash
   kubectl logs -f deployment/search-server -n semantic-search
   kubectl logs -f deployment/demo-app -n semantic-search
   kubectl logs -f statefulset/weaviate -n semantic-search
   ```

- **Port Forwarding for Local Access**
   ```bash
   # Access Search Server API
   kubectl port-forward svc/search-server 8000:8000 -n semantic-search
   
   # Access Demo Frontend
   kubectl port-forward svc/demo-app 8501:8501 -n semantic-search
   
   # Access Weaviate directly
   kubectl port-forward svc/weaviate 8082:8080 -n semantic-search
   ```

### Terraform Infrastructure

Provision and manage your cloud infrastructure for the semantic search application using Terraform.

#### Prerequisites

- Terraform CLI installed (v1.0.0+)
- Cloud provider CLI configured (gcloud, aws, az)
- Cloud provider credentials configured

#### Supported Cloud Providers

- Google Cloud Platform (GCP)
- Amazon Web Services (AWS)
- Microsoft Azure

#### Deployment Steps

1. **Initialize Terraform**

   ```bash
   cd terraform
   
   # Choose your cloud provider directory
   cd gcp  # or aws, azure
   
   # Initialize Terraform
   terraform init
   ```

2. **Configure Variables**

   Create a `terraform.tfvars` file:

   ```
   # Common variables
   project_name = "semantic-search"
   environment = "production"
   region = "us-central1"  # Change as needed
   
   # Kubernetes variables
   k8s_node_count = 3
   k8s_node_type = "e2-standard-2"
   
   # Application variables
   create_registry = true
   deploy_application = true
   ```

3. **Plan Deployment**

   ```bash
   terraform plan -out=tfplan
   ```

4. **Apply Configuration**

   ```bash
   terraform apply tfplan
   ```

   This will:
   - Create a Kubernetes cluster
   - Set up a Container Registry
   - Configure networking
   - Create storage for persistence
   - Output access information

5. **Configure kubectl**

   ```bash
   # For GCP
   gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
   
   # For AWS
   aws eks update-kubeconfig --name $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)
   
   # For Azure
   az aks get-credentials --resource-group $(terraform output -raw resource_group_name) --name $(terraform output -raw kubernetes_cluster_name)
   ```

6. **Deploy Application on Kubernetes**

   Follow the Kubernetes deployment steps above, or use the automated deployment:

   ```bash
   # The Terraform script can trigger the Kubernetes deployment
   cd ../..
   ./local_scripts/deploy_to_k8s.sh
   ```

7. **Cleanup Resources (When Needed)**

   ```bash
   terraform destroy
   ```

#### Terraform Modules

The Terraform configuration is organized into modular components:

- **Network**: VPC, subnets, firewall rules
- **Kubernetes**: Managed Kubernetes cluster
- **Storage**: Persistent storage for Weaviate
- **Registry**: Container registry for Docker images
- **IAM**: Service accounts and permissions
- **Monitoring**: Logging and alerting setup

#### Customization

Modify `variables.tf` to adjust:

- Cluster size and machine types
- Network configuration
- Storage options
- Multi-region deployment
- High availability settings
