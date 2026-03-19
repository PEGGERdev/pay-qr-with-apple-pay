# GitHub Actions Secrets

Configure these repository secrets for `N3on00/pay-qr-with-apple-pay`.

## Required

- `DEPLOY_HOST`: `89.167.118.25`
- `DEPLOY_USER`: `deploy`
- `DEPLOY_SSH_KEY`: private key content for the deploy user
- `DEPLOY_PROD_APP_DIR`: `/opt/pay-qr-with-apple-pay`
- `DEPLOY_STAGING_APP_DIR`: `/opt/pay-qr-with-apple-pay-dev`

## Recommended

- `DEPLOY_SSH_PORT`: `22`
- `DEPLOY_HOST_FINGERPRINT`: output of `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` from the server

## Branch Mapping

- `main` -> production -> `pegger.dev`
- `develop` -> staging -> `dev.pegger.dev`

## Notes

- Do not use `root` in GitHub Actions deployment.
- The `deploy` user should remain in the `docker` group.
- Production and staging must use separate server checkouts.
