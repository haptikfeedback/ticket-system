FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirement pins first for better layer caching
COPY apps/backend/requirements /app/requirements
# Install dev deps (includes base)
RUN pip install -r /app/requirements/dev.txt

# App code will be mounted at runtime for hot reload
EXPOSE 8000
