# System Overview

- The Vue frontend handles scanning, invoice preview, and wallet readiness.
- The Node backend only exposes health and payment intent endpoints.
- Stripe owns payment confirmation and Apple Pay token processing.
- Demo mode keeps the UI usable before real Stripe credentials are added.
