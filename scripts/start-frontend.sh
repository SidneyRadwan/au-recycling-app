#!/bin/bash
export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8080}"

trap 'kill 0' EXIT

cd "$(dirname "$0")/../frontend"
npm run dev
