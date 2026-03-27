FROM ghcr.io/astral-sh/uv:0.11.2 AS uv
FROM oven/bun:1.3.11 AS bun
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG JAVA_VERSION=25
ARG PYTHON_VERSION=3.12
ARG DOCKER_VERSION=28.4.0

# Base tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    gnupg \
    unzip \
    zip \
    sudo \
    locales \
    openssh-client \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

# Create non-root user
RUN useradd -m -s /bin/bash -G sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Java 25 (Temurin) — symlink to arch-independent path so JAVA_HOME is stable
RUN curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public \
    | gpg --dearmor -o /usr/share/keyrings/adoptium.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb jammy main" \
    > /etc/apt/sources.list.d/adoptium.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends temurin-${JAVA_VERSION}-jdk \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf "$(find /usr/lib/jvm -maxdepth 1 -name "temurin-${JAVA_VERSION}*" -type d | head -1)" /usr/lib/jvm/temurin-${JAVA_VERSION}

ENV JAVA_HOME=/usr/lib/jvm/temurin-${JAVA_VERSION}
ENV PATH=$JAVA_HOME/bin:$PATH

# Bun — JavaScript runtime and package manager
COPY --from=bun /usr/local/bin/bun /usr/local/bin/bun
RUN ln -s /usr/local/bin/bun /usr/local/bin/bunx

# Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python3 \
    && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python

# uv — fast Python package manager
COPY --from=uv /uv /uvx /usr/local/bin/

# Google Cloud SDK (gcloud)
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    > /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# Terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg \
    | gpg --dearmor -o /usr/share/keyrings/hashicorp.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp.gpg] https://apt.releases.hashicorp.com noble main" \
    > /etc/apt/sources.list.d/hashicorp.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends terraform \
    && rm -rf /var/lib/apt/lists/*

# Docker CLI (docker-outside-of-docker — talks to host daemon via mounted socket)
RUN curl -fksSL "https://download.docker.com/linux/static/stable/$(uname -m)/docker-${DOCKER_VERSION}.tgz" \
    -o /tmp/docker.tgz \
    && tar -zxf /tmp/docker.tgz -C /tmp \
    && mv /tmp/docker/docker /usr/local/bin/docker \
    && rm -rf /tmp/docker.tgz /tmp/docker \
    && groupadd docker \
    && usermod -aG docker vscode

# pre-commit (manages git hooks for all languages in this repo)
RUN pip install --break-system-packages pre-commit

# Claude Code — installed globally via Bun, shebang patched to use bun runtime (no node required)
RUN BUN_INSTALL=/usr/local bun install -g @anthropic-ai/claude-code \
    && sed -i '1s|#!/usr/bin/env node|#!/usr/bin/env bun|' /usr/local/bin/claude

# Playwright + Chromium
RUN bunx playwright install-deps chromium \
    && bunx playwright install chromium

# --- Pre-install project dependencies (cached unless lock files change) ---

# Backend: Gradle dependencies
COPY backend/gradlew backend/gradlew.bat backend/build.gradle backend/settings.gradle /tmp/backend/
COPY backend/gradle /tmp/backend/gradle/
RUN chmod +x /tmp/backend/gradlew \
    && cd /tmp/backend \
    && ./gradlew dependencies --quiet --no-daemon \
    && rm -rf /tmp/backend

# Pre-create volume mount points so named volumes inherit vscode ownership on first mount
RUN mkdir -p \
    /home/vscode/.cache/bun \
    /home/vscode/.cache/gradle \
    /home/vscode/.cache/uv \
    /home/vscode/.cache/uv-python \
    /home/vscode/.claude \
    /commandhistory \
    /workspace/frontend/node_modules \
    /workspace/frontend/.next \
    /workspace/scraper/.venv \
    /workspace/scraper/output \
    && chown -R vscode:vscode /home/vscode/.cache /home/vscode/.claude /commandhistory /workspace

USER vscode
ENV PATH=/home/vscode/.local/bin:$PATH
WORKDIR /workspace
