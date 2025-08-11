#!/usr/bin/env bash
set -e

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <host> [<port>]"
  exit 1
fi

HOST="$1"
PORT="${2:-5432}"
COMMAND="${@:3}"
# Default command to run if none is provided
if [ -z "$COMMAND" ]; then
  COMMAND="scripts/."
fi

# Function to check if PostgreSQL is ready
check_postgres() {
  pg_isready -h "$HOST" -p "$PORT" -U PostgreSQL
}

# Wait for PostgreSQL to become available
echo "Waiting for PostgreSQL at $HOST:$PORT..."
while ! check_postgres; do
  sleep 1
done

echo "PostgreSQL is ready at $HOST:$PORT"

echo "Executing command: $COMMAND"

eval "$COMMAND"

echo "Command executed successfully."

exit 0
