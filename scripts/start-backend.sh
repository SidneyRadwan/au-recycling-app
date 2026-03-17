#!/bin/bash
set -a
. "$(dirname "$0")/../.env" 2>/dev/null
set +a

# Kill the entire process group (including JVM child) when this script exits,
# so closing the terminal doesn't leave an orphaned process on port 8080.
trap 'kill 0' EXIT

cd "$(dirname "$0")/../backend"
./gradlew bootRun
