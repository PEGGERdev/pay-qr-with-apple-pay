# Pay QR With Apple Pay

A Vue 3 + FastAPI application for scanning QR invoices and paying them with Apple Pay through Stripe, using a modular backend and frontend architecture.

Important: this repository can be made much safer and more production-ready in code, but no software repository alone can guarantee legal compliance. You still need jurisdiction-specific legal review, privacy notices, merchant onboarding, and operating procedures.

## Structure

The project follows a modular separation between frontend, backend, and deployment concerns:

- `frontend/` Vue app with `views`, `components`, `stores`, `services`, and `core`
- `backend/` FastAPI app with `api`, `core`, `services`, `repositories`, and `models`
- `docs/` architecture and setup notes
- `.env.example` shared environment template

## Features

- QR invoice scanning with camera access via `html5-qrcode`
- Invoice parsing for JSON, URI, and `key:value` QR payloads
- Apple Pay wallet flow powered by Stripe Payment Request
- Mobile-first responsive dashboard with manual paste fallback
- JWT-based auth flow for protected payment operations
- Live Stripe PaymentIntent support with demo fallback for local UI work
- Stripe webhook reconciliation for final payment status updates
- Production guardrails for JWT, host validation, HTTPS enforcement, and rate limiting
- CI/CD workflow and containerized deployment assets

## Local Setup

1. Copy `.env.example` to `.env` and fill in Stripe values when available.
2. Install backend dependencies:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend
npm install
```

4. Start the backend:

```bash
cd backend
python main.py
```

5. Start the frontend on all network interfaces:

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

## Environment Files

- Use `.env.example` for local/demo development.
- Use `.env.production.example` as the starting point for real Stripe and Apple Pay deployment.
- Real Apple Pay requires `DEMO_MODE=false`, valid Stripe keys, `STRIPE_WEBHOOK_SECRET`, HTTPS, and a Stripe-verified domain.
- Intended public domains: `pegger.dev` for production and `dev.pegger.dev` for development.
- Deployed frontend builds consume `VITE_*` values from the server env file at image build time.

## Mobile Device Testing

- Find your computer IP with `ipconfig`.
- Set `VITE_API_BASE_URL=http://YOUR_LOCAL_IP:8000` in `.env`.
- Open `http://YOUR_LOCAL_IP:5173` from the iPhone connected to the same network.
- Apple Pay only appears on supported Safari/iOS devices with a valid Stripe domain setup.

## Architecture Notes

- Backend auth uses `/auth/register` and `/auth/login`, issues bearer tokens, and protects `/payments` endpoints.
- Frontend API calls stay in focused services instead of a separate endpoint registry layer.
- Payment intent creation is routed through a reusable authenticated create router.

## Backend Module Layout

- `backend/api/crud.py` is the stable public facade for the generic router system.
- `backend/api/crud_base.py` contains the generic CRUD router engine and shared route registration logic.
- `backend/api/crud_authenticated.py` contains auth-aware router extensions such as authenticated create flows.
- `backend/api/auth_session_router.py` contains register/login session orchestration in the same generic router style.
- `backend/api/crud_types.py` and `backend/api/crud_validation.py` hold small supporting dataclasses and validation helpers.
- `backend/api/crud_factories.py` exposes the router factory helpers used by route modules.
- `backend/models/schemas.py` remains the compatibility import surface, while `backend/models/auth_schemas.py` and `backend/models/payment_schemas.py` split contracts by domain.

## Demo Invoice Payload

```json
{
  "invoiceId": "INV-2026-0007",
  "merchantName": "Northline Cafe",
  "description": "Lunch invoice",
  "amount": 18.40,
  "currency": "EUR",
  "countryCode": "DE"
}
```

More details live in `docs/development/setup.md`, `docs/architecture/system-overview.md`, and `ARCHITECTURE.md`.

For real-device Apple Pay rollout, use `docs/development/apple-pay-checklist.md`.

For security, deployment, and compliance preparation, use:

- `docs/security/security-checklist.md`
- `docs/operations/deployment.md`
- `docs/compliance/privacy-policy-template.md`
- `docs/compliance/terms-template.md`
