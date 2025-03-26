# Development Guide

This guide provides detailed information for developers who want to contribute to or modify the Semantic Search project.

## 🔧 Development Environment Setup

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Git
- Your favorite IDE (VS Code recommended)
- OpenAI API key

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/semantic-search.git
   cd semantic-search
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 🏗️ Project Structure

```
semantic-search/
├── src/                      # Source code
│   ├── semantic_search/      # Main package
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration
│   │   ├── embedding_manager.py
│   │   ├── text_processor.py
│   │   └── generative_search.py
│   └── api/                  # API endpoints
├── tests/                    # Test files
├── docker/                   # Docker configurations
├── k8s/                     # Kubernetes manifests
├── terraform/               # Infrastructure as Code
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

## 🧪 Testing

### Running Tests

1. **Unit tests**
   ```bash
   pytest tests/unit/
   ```

2. **Integration tests**
   ```bash
   pytest tests/integration/
   ```

3. **Coverage report**
   ```bash
   pytest --cov=src tests/
   ```

### Writing Tests

- Place tests in the appropriate directory under `tests/`
- Follow the naming convention: `test_*.py`
- Use fixtures for common setup
- Mock external services (OpenAI, Weaviate)

Example test:
```python
def test_embedding_generation():
    manager = EmbeddingManager()
    text = "Test document"
    embedding = manager.get_embedding(text)
    assert len(embedding) == 1536  # OpenAI embedding dimension
```

## 📝 Code Style

### Guidelines

1. **PEP 8**
   - Use 4 spaces for indentation
   - Maximum line length: 88 characters (Black default)
   - Use meaningful variable names

2. **Type Hints**
   ```python
   def process_text(text: str, chunk_size: int = 1000) -> List[str]:
       """
       Process and chunk text.

       Args:
           text: Input text to process
           chunk_size: Size of each chunk

       Returns:
           List of text chunks
       """
       # Implementation
   ```

3. **Documentation**
   - Add docstrings to all functions and classes
   - Include examples in docstrings
   - Keep README.md up to date

### Code Quality Tools

1. **Black** for code formatting
   ```bash
   black src/ tests/
   ```

2. **isort** for import sorting
   ```bash
   isort src/ tests/
   ```

3. **flake8** for linting
   ```bash
   flake8 src/ tests/
   ```

4. **mypy** for type checking
   ```bash
   mypy src/
   ```

## 🔄 Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. **Run tests and quality checks**
   ```bash
   # Run all checks
   ./scripts/run_checks.sh
   ```

4. **Push changes and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create PR through GitHub interface
   ```

## 🐳 Docker Development

### Local Development with Docker

1. **Build images**
   ```bash
   docker-compose -f docker/docker-compose.dev.yml build
   ```

2. **Start services**
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d
   ```

3. **View logs**
   ```bash
   docker-compose -f docker/docker-compose.dev.yml logs -f
   ```

### Debugging in Docker

1. **Attach debugger**
   - Use VS Code's Docker extension
   - Configure `launch.json` for remote debugging

2. **Access container shell**
   ```bash
   docker exec -it semantic-search-server bash
   ```

## 📦 Release Process

1. **Update version**
   - Update version in `setup.py`
   - Update CHANGELOG.md

2. **Create release branch**
   ```bash
   git checkout -b release/v1.0.0
   ```

3. **Run release checks**
   ```bash
   ./scripts/release_checks.sh
   ```

4. **Create GitHub release**
   - Tag version
   - Write release notes
   - Attach artifacts

## 🔍 Monitoring and Debugging

### Logging

- Use the configured logger
- Include context in log messages
- Set appropriate log levels

```python
from semantic_search.logger import get_logger

logger = get_logger(__name__)

def process_document(doc_id: str) -> None:
    logger.info(f"Processing document: {doc_id}")
    try:
        # Processing logic
        logger.debug("Document processed successfully")
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
```

### Metrics

- Monitor API endpoints
- Track embedding generation time
- Watch memory usage

### Debugging Tips

1. **Enable debug logging**
   ```bash
   export LOG_LEVEL=DEBUG
   ```

2. **Use debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

3. **Profile code**
   ```python
   import cProfile
   cProfile.run('function_to_profile()')
   ```

## 🔐 Security Best Practices

1. **API Keys**
   - Never commit API keys
   - Use environment variables
   - Rotate keys regularly

2. **Dependencies**
   - Keep dependencies updated
   - Run security scans
   - Use dependency lockfiles

3. **Input Validation**
   - Validate all inputs
   - Sanitize user data
   - Use proper error handling

## 📚 Additional Resources

- [Project Wiki](https://github.com/yourusername/semantic-search/wiki)
- [API Documentation](http://localhost:8000/docs)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md) 