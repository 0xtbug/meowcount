#!/bin/bash

# MeowCount - Docker Deployment Script

MODE=${1:-}

if [[ -z "$MODE" ]]; then
  echo "Select deployment mode:"
  echo "  [1] Development (meowcount-dev, http://localhost:3001)"
  echo "  [2] Production  (meowcount,    http://localhost:3000)"
  read -rp "Enter 1 or 2 [2]: " CHOICE
  case "${CHOICE,,}" in
    1|dev|development) MODE="dev" ;;
    2|""|prod|production) MODE="prod" ;;
    *) echo "Invalid choice: $CHOICE" ; exit 1 ;;
  esac
fi

if [[ "$MODE" != "dev" && "$MODE" != "prod" ]]; then
  echo "Invalid mode: $MODE (use 'dev' or 'prod')"
  exit 1
fi

SERVICE="meowcount"
PORT=3000
if [[ "$MODE" == "dev" ]]; then
  SERVICE="meowcount-dev"
  PORT=3001
fi

echo "Starting MeowCount deployment in $MODE mode (service: $SERVICE)"

# Check if .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found!"
  echo "Create .env with CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SECRET_KEY"
  exit 1
fi

# Pull latest changes (if using git)
if [ -d .git ]; then
  echo "Pulling latest changes..."
  git pull
fi

# Build and start selected service
echo "Building and starting $SERVICE..."
docker compose up -d --build "$SERVICE"

echo "Waiting for service to start..."
sleep 10

# Check if the service is running
if docker compose ps "$SERVICE" | grep -q "Up"; then
  echo "Deployment successful!"
  echo "App is running at: http://localhost:$PORT"
  echo "View logs with: docker compose logs -f $SERVICE"
else
  echo "Deployment failed!"
  echo "Check logs with: docker compose logs $SERVICE"
  exit 1
fi
