# Keystone container. Build: docker build -t keystone .
# Run:   docker run --rm -p 8080:8080 keystone  then open http://localhost:8080
FROM python:3.12.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Install the locked dependencies.
COPY requirements.lock requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy source and run as an unprivileged user.
RUN useradd --create-home --uid 10001 student
COPY --chown=student:student . .

# Writable data directory for the SQLite database (owned by the runtime user).
ENV DATABASE=/app/data/keystone.sqlite3 \
    UPLOAD_DIR=/app/data/uploads \
    PORT=8080
# /app is owned by root (from WORKDIR); create_app() always makes app.instance_path
# (/app/instance), so that dir and the data dir must be writable by the runtime user.
RUN mkdir -p /app/data /app/instance && chown -R student:student /app/data /app/instance
USER student

EXPOSE 8080
CMD ["python", "wsgi.py"]
