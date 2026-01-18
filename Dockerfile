# Tsunami Early Warning System - Docker Support

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libhdf5-dev \
    libnetcdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data/raw data/processed data/cache models/checkpoints

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py
ENV PORT=5000

# Create health check script
RUN echo '#!/bin/bash\nPORT=${PORT:-5000}\npython -c "import requests; requests.get(\"http://localhost:$PORT/health\", timeout=5)"' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

# Health check - increased start period for model loading
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD /app/healthcheck.sh

# Default command - use bash to substitute PORT variable
CMD bash -c "python main.py --host 0.0.0.0 --port \$PORT"
