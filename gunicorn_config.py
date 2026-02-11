"""Gunicorn configuration file for Django application - optimized for production"""
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes - optimized for production
# Use environment variable if provided, otherwise calculate based on CPU
workers_env = os.getenv('GUNICORN_WORKERS')
if workers_env:
    workers = int(workers_env)
else:
    workers = min(multiprocessing.cpu_count() * 2 + 1, 8)  # Cap at 8 workers

worker_class = "gevent"
worker_connections = 1000
max_requests = 1000  # Restart workers after 1000 requests to prevent memory leaks
max_requests_jitter = 100  # Add jitter to prevent all workers restarting at once
timeout = 30  # Reduced from 120 for faster failure detection
graceful_timeout = 30
keepalive = 5

# Preload app for faster worker spawn and shared memory
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "library_gunicorn"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Worker lifecycle hooks for better performance
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Gunicorn server...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Gunicorn...")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info(f"Server is ready. Spawning {workers} workers...")

def worker_int(worker):
    """Called when a worker receives SIGINT or SIGQUIT."""
    worker.log.info("Worker received SIGINT or SIGQUIT")

def worker_exit(server, worker):
    """Called when a worker is exited."""
    server.log.info(f"Worker {worker.pid} exited")
