# System Overview

- The Vue frontend handles scanning, invoice preview, and wallet readiness.
- The FastAPI backend exposes health, auth, and payment endpoints through a declared feature registry.
- Stripe owns payment confirmation and Apple Pay token processing.
- Demo mode keeps the UI usable before real Stripe credentials are added.
