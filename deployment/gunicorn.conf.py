"""Gunicorn configuration for production."""
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
errorlog = "-"
accesslog = "-"
loglevel = "info"

# Process naming
proc_name = "odoo-audit-platform"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"

# Max requests before worker restart (prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30
