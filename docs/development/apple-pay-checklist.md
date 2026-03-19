# Apple Pay Checklist

Use this checklist to move from local demo mode to real Apple Pay payments.

## 1. Stripe Setup

- Create or use an existing Stripe account.
- Copy the publishable key into `VITE_STRIPE_PUBLISHABLE_KEY`.
- Copy the secret key into `STRIPE_SECRET_KEY`.
- Set `DEMO_MODE=false` and `VITE_DEMO_MODE=false`.

## 2. Domain Requirements

Apple Pay requires a domain that Stripe can verify.

- Choose the domain that will host the frontend.
- Production target: `pegger.dev`
- Development target: `dev.pegger.dev`
- In Stripe Dashboard, register that domain for Apple Pay.
- Complete Stripe's domain verification flow.
- Make sure the frontend is actually served from that verified domain.

## 3. HTTPS Requirements

Apple Pay will not work from an unsecured site.

- Serve the frontend over HTTPS.
- Serve the backend over HTTPS or behind a trusted reverse proxy.
- Make sure `VITE_API_BASE_URL` points to the HTTPS backend URL.

## 4. Device Requirements

- Use a real Apple device.
- Open the app in Safari.
- Make sure Apple Pay is configured on the device with a valid card.
- Do not rely on desktop Chrome or Android for Apple Pay verification.

## 5. Application Settings

Frontend:

- `VITE_API_BASE_URL=https://api.your-domain.com`
- `VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...`
- `VITE_DEMO_MODE=false`

Backend:

- `CORS_ORIGINS=https://your-domain.com`
- `JWT_SECRET=<long random secret>`
- `DEMO_MODE=false`
- `STRIPE_SECRET_KEY=sk_live_...`

## 6. Smoke Test Flow

1. Open the deployed frontend in Safari on the iPhone.
2. Register a user or sign in.
3. Load the sample invoice or scan a QR payload.
4. Confirm the wallet button appears.
5. Submit a payment.
6. Check Stripe Dashboard for the PaymentIntent.
7. Check `/payments/history` behavior through the UI.

## 7. Failure Checklist

If Apple Pay does not appear:

- Confirm Safari is being used.
- Confirm the domain is verified in Stripe.
- Confirm HTTPS is active.
- Confirm `VITE_STRIPE_PUBLISHABLE_KEY` is live/test as intended.
- Confirm `DEMO_MODE=false`.
- Confirm the device has Apple Pay configured.
