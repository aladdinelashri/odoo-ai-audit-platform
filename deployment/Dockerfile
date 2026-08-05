# Multi-stage build for Odoo AI Audit Platform
FROM python:3.11-slim as builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r odoaudit && useradd -r -g odoaudit odoaudit

# Copy installed packages from builder
COPY --from=builder /root/.local /home/odoaudit/.local
ENV PATH=/home/odoaudit/.local/bin:$PATH

# Copy application code
COPY --chown=odoaudit:odoaudit . .

# Create storage directory
RUN mkdir -p database/storage && chown -R odoaudit:odoaudit database/storage

USER odoaudit

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["gunicorn", "-c", "deployment/gunicorn.conf.py", "api.main:app"]
