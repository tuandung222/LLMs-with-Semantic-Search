FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uninstall current openai package and install a specific version
# that doesn't have the proxies issue
RUN pip uninstall -y openai && pip install --no-cache-dir openai==0.28.0

# Copy source code and configuration
COPY src/ src/
COPY setup.py .
# Create empty .env file if not exists
RUN touch .env
# COPY logging_config.json .

# Install the package in development mode
RUN pip install -e .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOAD_SAMPLE_DATA=false
ENV WEAVIATE_URL=http://weaviate:8080
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV LOG_LEVEL=INFO

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the search server
CMD ["uvicorn", "src.search_server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 