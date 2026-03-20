#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/pay-qr-with-apple-pay}"
BRANCH="${BRANCH:-main}"
ENV_FILE="${ENV_FILE:-.env.production}"
COMPOSE_FILE="${COMPOSE_FILE:-deploy/docker-compose.prod.yml}"
PROJECT_NAME="${PROJECT_NAME:-payqr-prod}"

if [ ! -d "$APP_DIR/.git" ]; then
  echo "Missing git checkout in $APP_DIR" >&2
  exit 1
fi

if [ ! -f "$APP_DIR/$ENV_FILE" ]; then
  EXAMPLE_FILE="${APP_DIR}/${ENV_FILE}.example"
  if [ -f "$EXAMPLE_FILE" ]; then
    echo "Creating $APP_DIR/$ENV_FILE from example file"
    cp "$EXAMPLE_FILE" "$APP_DIR/$ENV_FILE"
  else
    echo "Missing environment file $APP_DIR/$ENV_FILE" >&2
    exit 1
  fi
fi

git -C "$APP_DIR" fetch origin
git -C "$APP_DIR" stash --include-untracked || true
git -C "$APP_DIR" checkout "$BRANCH" --force
git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
git -C "$APP_DIR" stash drop || true

docker compose -p "$PROJECT_NAME" --env-file "$APP_DIR/$ENV_FILE" -f "$APP_DIR/$COMPOSE_FILE" down
docker compose -p "$PROJECT_NAME" --env-file "$APP_DIR/$ENV_FILE" -f "$APP_DIR/$COMPOSE_FILE" up -d --build --remove-orphans
