# Semantic Search with Generative AI

A production-ready semantic search application that combines vector embeddings and Large Language Models to provide intelligent question answering and information retrieval over custom document collections.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Highlights](#project-highlights)
- [Features](#features)
- [Key Components](#key-components)
- [Getting Started](#getting-started)
- [API Usage](#api-usage)
- [Deployment Options](#deployment-options)
  - [Docker Deployment](#docker-deployment-recommended)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Cloud Infrastructure with Terraform](#terraform-infrastructure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

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
    
    subgraph External["External Services"]
        VecDB["Vector Database<br>(Weaviate)"]
        OpenAI["OpenAI API"]
        SampleData["Sample Data<br>Text Samples & Metadata"]
    end
    
    DocUI --> TextProc
    QuesUI --> EmbMgr
    GenSearch --> ResUI
    
    TextProc <-- Raw Text --> SampleData
    EmbMgr <-- Vectors --> VecDB
    GenSearch <-- Prompts --> OpenAI
    
    classDef frontend fill:#e6f7ff,stroke:#0099cc
    classDef server fill:#e6ffe6,stroke:#00cc66
    classDef external fill:#fff0e6,stroke:#ff9933
    
    class Frontend frontend
    class Server server
    class External external
```

### Core Components and Data Flow

1. **Search Server (FastAPI)**

   - **TextProcessor**: Document preprocessing and chunking
   - **EmbeddingManager**: Vector operations and caching
   - **GenerativeSearch**: Search and answer generation

2. **Vector Database (Weaviate)**

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
