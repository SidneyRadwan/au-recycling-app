FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

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
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

# Create non-root user
RUN useradd -m -s /bin/bash -G sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Java 21 (Temurin) — symlink to arch-independent path so JAVA_HOME is stable
RUN curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public \
    | gpg --dearmor -o /usr/share/keyrings/adoptium.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb jammy main" \
    > /etc/apt/sources.list.d/adoptium.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends temurin-21-jdk \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf "$(find /usr/lib/jvm -maxdepth 1 -name 'temurin-21*' -type d | head -1)" /usr/lib/jvm/temurin-21

ENV JAVA_HOME=/usr/lib/jvm/temurin-21
ENV PATH=$JAVA_HOME/bin:$PATH

# Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Python 3.12
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.12 /usr/local/bin/python3 \
    && ln -sf /usr/bin/python3.12 /usr/local/bin/python

# pre-commit (manages git hooks for all languages in this repo)
RUN pip install --break-system-packages pre-commit

# Global npm tools
RUN npm install -g @anthropic-ai/claude-code

# Playwright + Chromium — enables headless browser access for Claude Code
# (used for Figma page capture, smoke testing, etc.)
RUN npx --yes playwright install-deps chromium \
    && npx --yes playwright install chromium

# --- Pre-install project dependencies (cached unless lock files change) ---

# Backend: Gradle dependencies
COPY backend/gradlew backend/gradlew.bat backend/build.gradle backend/settings.gradle /tmp/backend/
COPY backend/gradle /tmp/backend/gradle/
RUN chmod +x /tmp/backend/gradlew \
    && cd /tmp/backend \
    && ./gradlew dependencies --quiet --no-daemon \
    && rm -rf /tmp/backend

# Frontend: npm dependencies
COPY frontend/package*.json /tmp/frontend/
RUN cd /tmp/frontend && npm install && rm -rf /tmp/frontend

# Scraper: pip dependencies
COPY scraper/requirements.txt /tmp/scraper/
RUN pip install --break-system-packages -r /tmp/scraper/requirements.txt \
    && rm -rf /tmp/scraper

USER vscode
ENV PATH=/home/vscode/.local/bin:$PATH
WORKDIR /workspace
