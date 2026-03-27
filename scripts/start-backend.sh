#!/bin/bash
set -a
. "$(dirname "$0")/../.env" 2>/dev/null
set +a

if (echo > /dev/tcp/localhost/8080) 2>/dev/null; then
  echo "Error: port 8080 is already in use. Stop the existing backend before starting a new one." >&2
  exit 1
fi

# Kill the entire process group (including JVM child) on any catchable exit.
# Note: SIGKILL cannot be trapped — if the process is force-killed, port 8080
# will remain occupied and the startup check above will catch it on next run.
trap 'kill 0' EXIT INT TERM

cd "$(dirname "$0")/../backend"
./gradlew bootRun
