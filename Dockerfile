FROM python:3.12.0-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
  --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create user first
RUN groupadd -g 1000 appgroup && \
  useradd -r -u 1000 -g appgroup app

# Copy and install dependencies as root
COPY --chown=app:appgroup requirements.txt .
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  rm requirements.txt

# Copy source code
COPY --chown=app:appgroup src ./src

# Switch to non-root user
USER 1000:1000
