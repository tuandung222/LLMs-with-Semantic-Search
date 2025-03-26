FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and configuration
COPY src/ src/
# Create empty .env file if not exists
RUN touch .env
# COPY logging_config.json .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the demo app
CMD ["streamlit", "run", "src/demo_app/app.py", "--server.address=0.0.0.0", "--server.port=8501"] 