FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-glibc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs model

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)"

# Run application with Gunicorn
CMD ["gunicorn", \
     "--workers=4", \
     "--threads=2", \
     "--worker-class=gthread", \
     "--bind=0.0.0.0:5000", \
     "--timeout=120", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "app:app"]
