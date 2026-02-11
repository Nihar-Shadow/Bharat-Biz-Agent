# ==========================================
# 🚀 Nurothon AI - "App in a Box" Dockerfile
# ==========================================
# This Dockerfile builds a SINGLE container running both 
# the FastAPI Backend and Nginx Frontend using Supervisor.
# Perfect for demos and judges! 
# Usage: docker build -t nurothon . && docker run -p 80:80 nurothon

FROM python:3.11-slim

# -----------------------------------------------------
# 1. Install System Dependencies (Nginx, Supervisor, OCR)
# -----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    libtesseract-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# -----------------------------------------------------
# 2. Install Python Dependencies
# -----------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------
# 3. Setup Backend Code
# -----------------------------------------------------
COPY app ./app
COPY *.py ./
RUN mkdir -p invoices data

# -----------------------------------------------------
# 4. Setup Frontend (Static Files)
# -----------------------------------------------------
# Create web root and clean default nginx files
RUN rm -rf /usr/share/nginx/html/*
COPY frontend /usr/share/nginx/html

# -----------------------------------------------------
# 5. Configure Nginx & Supervisor
# -----------------------------------------------------
# Copy our custom Nginx config for single-container setup
COPY nginx-standalone.conf /etc/nginx/sites-available/default

# Copy Supervisor config to manage both processes
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# -----------------------------------------------------
# 6. Finalize & Run
# -----------------------------------------------------
# Expose HTTP port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start Supervisor (Runs Nginx + Uvicorn)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
