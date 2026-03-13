#!/usr/bin/env bash
set -euo pipefail

# Frontend dependencies
cd /workspace/frontend && npm install --prefer-offline

# Git hooks
cd /workspace && pre-commit install && pre-commit install-hooks
