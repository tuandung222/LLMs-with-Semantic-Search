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

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Demo Frontend (Streamlit)                      │
│                                                                         │
│   ┌─────────────────┐  ┌────────────────┐  ┌────────────────────┐     │
│   │  Document       │  │   Question     │  │    Results         │     │
│   │  Upload UI      │  │   Input UI     │  │    Display UI      │     │
│   └────────┬────────┘  └───────┬────────┘  └────────┬───────────┘     │
└────────────┼────────────────────┼────────────────────┼─────────────────┘
             │                     │                    │
             ▼                     ▼                    ▲
┌────────────────────────────────────────────────────────────────────────┐
│                        Search Server (FastAPI)                          │
│                                                                        │
│  ┌──────────────────┐   ┌──────────────────┐   ┌─────────────────┐   │
│  │  TextProcessor   │   │  EmbeddingManager │   │ GenerativeSearch│   │
│  │ ┌──────────────┐│   │ ┌──────────────┐ │   │ ┌─────────────┐ │   │
│  │ │Clean & Chunk ││   │ │Create & Cache │ │   │ │Answer Gen.  │ │   │
│  │ │Text          ││──►│ │Embeddings    │ │──►│ │with Context │ │   │
│  │ └──────────────┘│   │ └──────────────┘ │   │ └─────────────┘ │   │
│  └──────────────────┘   └────────┬─────────┘   └─────────┬───────┘   │
│           ▲                       │                        │           │
└───────────┼───────────────────────┼────────────────────────┼──────────┘
            │                       │                         │
     Raw Text│                      │Vectors                  │Prompts
            │                       ▼                         │
┌───────────────────┐    ┌──────────────────┐      ┌────────────────┐
│   Sample Data     │    │Vector Database   │      │   OpenAI API   │
│  ┌─────────────┐ │    │   (Weaviate)     │      │ ┌────────────┐ │
│  │Text Samples │ │    │ │Vector Store  │ │      │ │Text-to-Vec │ │
│  │& Metadata   │ │    │ │& Search Index│ │      │ └────────────┘ │
│  └─────────────┘ │    │ │& Search Index│ │      │
└───────────────────┘    └──────────────────┘      └────────────────┘

```

### Core Components

1. **Search Server (FastAPI)**
   - **TextProcessor**: Handles document preprocessing
     - Intelligent text chunking with configurable overlap
     - Paragraph splitting and cleaning
     - Maintains semantic coherence between chunks
   
   - **EmbeddingManager**: Manages vector operations
     - Creates and caches OpenAI embeddings
     - Handles vector similarity search
     - Manages Weaviate database operations
     - Implements fallback mechanisms
   
   - **GenerativeSearch**: Orchestrates search and generation
     - Combines semantic search with LLM generation
     - Manages context-aware question answering
     - Handles multiple generation requests
     - Implements error handling and fallbacks

2. **Vector Database (Weaviate)**
   - Scalable vector storage and retrieval
   - Real-time similarity search
   - Schema management for document metadata
   - Batch processing capabilities
   - Data persistence and backup

3. **OpenAI Integration**
   - **Embedding Generation**: text-embedding-3-small model
   - **Text Generation**: GPT-3.5 Turbo for QA
   - Configurable parameters:
     - Temperature control
     - Token limits
     - Model selection
     - Batch processing

4. **Demo Frontend (Streamlit)**
   - Interactive document upload interface
   - Real-time question answering
   - Search result visualization
   - Error handling and user feedback

### Data Flow

1. **Document Processing Pipeline**:
   ```
   Raw Text → TextProcessor → Chunks → EmbeddingManager → Vectors → Weaviate
   ```

2. **Question Answering Pipeline**:
   ```
   Question → EmbeddingManager → Similar Chunks → GenerativeSearch → Answer
   ```

3. **Sample Data Pipeline**:
   ```
   Sample Data → TextProcessor → EmbeddingGenerator → Cached Vectors → Weaviate
   ```

### Key Features

- **Fault Tolerance**: Fallback mechanisms for API failures
- **Caching**: Efficient embedding storage and retrieval
- **Scalability**: Containerized services with Docker
- **Monitoring**: Comprehensive logging and error tracking
- **Security**: API key management and access control

## 🌟 Project Highlights

- **Designed and implemented a full-stack RAG system** using FastAPI, Weaviate, and OpenAI
- **Architected a containerized microservices solution** with Docker Compose
- **Engineered an intelligent text processing pipeline** for optimal document chunking
- **Integrated OpenAI's latest embedding models** for semantic search
- **Developed comprehensive REST API endpoints** with full documentation
- **Created resilient error handling mechanisms** for system stability
- **Optimized vector search performance** through fine-tuning
- **Implemented cross-version compatibility** for OpenAI SDK
- **Executed thorough end-to-end testing** of all components
- **Provided detailed documentation** for developers and users

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
  - Containerized deployment
  - Kubernetes support
  - Cloud infrastructure with Terraform

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
   git clone https://github.com/yourusername/semantic-search.git
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

- [API Documentation](http://localhost:8000/docs)
- [OpenAI Documentation](https://platform.openai.com/docs)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI team for their excellent API and models
- Weaviate team for the vector database
- FastAPI and Streamlit teams for their frameworks
- The open-source community for their contributions 