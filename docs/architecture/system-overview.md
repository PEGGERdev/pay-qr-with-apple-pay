# System Overview

- The Vue frontend handles scanning, invoice preview, and wallet readiness.
- The FastAPI backend exposes auth, payment intent, payment history, and Stripe webhook endpoints.
- The backend keeps a generic router orchestration layer, with auth and payment features composed through thin route modules.
- Stripe owns payment confirmation and Apple Pay token processing.
- Demo mode keeps the UI usable before real Stripe credentials are added.
