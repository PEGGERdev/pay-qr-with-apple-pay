# Deployment

## CI/CD Secrets

Configure these GitHub Actions secrets:

- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_SSH_KEY`
- `DEPLOY_APP_DIR`

## Server Layout

Recommended path:

- `/opt/pay-qr-with-apple-pay`
- staging path: `/opt/pay-qr-with-apple-pay-dev`

Suggested hostnames:

- production frontend: `pegger.dev`
- development frontend: `dev.pegger.dev`
- backend is exposed behind the same hostname via `/api`

Expected steps on the server:

1. Install Docker and Docker Compose.
2. Clone the repository into `/opt/pay-qr-with-apple-pay`.
3. Create `.env.production` with production values in `/opt/pay-qr-with-apple-pay`.
4. Create `.env.staging` with staging values in `/opt/pay-qr-with-apple-pay-dev`.
4. Make `deploy/deploy.sh` executable.
5. Add the Pegger host blocks to the shared Caddy config and reload Caddy.
6. Use separate Compose project names for prod and staging, for example `payqr-prod` and `payqr-dev`.
7. Keep separate git checkouts for `main` and `develop`.

## Reverse Proxy

Recommended:

- `pegger.dev` -> `pegger-prod-frontend:80` and `/api/*` -> `pegger-prod-backend:8000`
- `dev.pegger.dev` -> `pegger-dev-frontend:80` and `/api/*` -> `pegger-dev-backend:8000`

## Security Notes

- Do not expose the backend directly without TLS.
- Do not keep `DEMO_MODE=true` in production.
- Restrict SSH access and avoid password logins for root.
- Prefer a dedicated deploy user with limited privileges over root for CI.
- Keep the shared `spotonsight_proxy` Docker network available for reverse proxy routing.
