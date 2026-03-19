# Development Setup

## Install

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

cd ../frontend && npm install
```

## Run Locally

Backend:

```bash
cd backend
python main.py
```

Frontend:

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

## Test From Phone

1. Run `ipconfig` and note the IPv4 address of your active adapter.
2. Update `.env` so `VITE_API_BASE_URL` points to `http://<your-ip>:8000`.
3. Restart both servers.
4. Open `http://<your-ip>:5173` from the phone.
5. For Apple Pay, use Safari on a real Apple device and configure the domain in Stripe.

## Stripe Notes

- `VITE_STRIPE_PUBLISHABLE_KEY` is required in the frontend for wallet initialization.
- `STRIPE_SECRET_KEY` enables live PaymentIntent creation in `backend/services/payment/payment_service.py`.
- `DEMO_MODE=true` keeps the backend in demo mode even if Stripe is installed, which is useful while shaping the UI and auth flow.
- Turn `DEMO_MODE=false` and provide both Stripe keys to exercise the real Apple Pay path.
- For a deployment checklist, see `docs/development/apple-pay-checklist.md`.

## Auth Notes

- Register at `/auth/register` or log in at `/auth/login`.
- The backend returns a bearer token and a normalized user payload.
- `/payments` and `/payments/history` require the bearer token.
