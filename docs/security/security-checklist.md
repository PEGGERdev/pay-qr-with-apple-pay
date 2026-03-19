# Security Checklist

- Set `APP_ENV=production`
- Set `DEMO_MODE=false`
- Set a strong `JWT_SECRET`
- Use HTTPS for frontend and backend
- Set strict `ALLOWED_HOSTS`
- Set HTTPS-only `CORS_ORIGINS`
- Restrict Stripe keys to the intended environment
- Use SSH keys instead of password auth
- Prefer a non-root deploy user for automation
- Rotate credentials regularly
- Review retention and privacy notices before launch
