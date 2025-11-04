# Admin Panel Dockerfile for Railway (Updated: 2025-11-03)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY admin-panel-server.py .
COPY admin-panel-ui-modern.html .
COPY 1.svg .

# Expose port (Railway uses PORT env var)
EXPOSE 8080

# Environment variables will be set in Railway
ENV FLASK_APP=admin-panel-server.py
ENV PYTHONUNBUFFERED=1

# Start command
CMD ["python", "-u", "admin-panel-server.py"]

