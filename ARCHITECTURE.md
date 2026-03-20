# Architecture

This project uses a pragmatic frontend/backend split focused on a single QR-to-wallet payment flow.

## Frontend

- `src/views/`: direct product screens, with `HomeView.vue` owning the payment flow
- `src/components/`: presentational and feature UI modules
- `src/stores/`: reactive application state and persisted session
- `src/services/`: auth, invoice parsing, API calls, and Stripe orchestration
- `src/core/`: app context and dependency wiring

## Backend

- `main.py`: HTTP entrypoint
- `core/application.py`: FastAPI wiring, lifecycle, CORS, and router composition
- `api/crud.py`: stable facade that re-exports the generic router system
- `api/crud_base.py`: base generic CRUD router implementation
- `api/crud_authenticated.py`: authenticated router extensions layered on the base router
- `api/auth_session_router.py`: auth session router that keeps register/login in the same orchestration style
- `api/crud_types.py`, `api/crud_validation.py`, `api/crud_factories.py`: supporting route config types, validation helpers, and factory entrypoints
- `api/routes/`: feature route modules that stay thin and delegate to services
- `services/auth/`: JWT issuing, password hashing, current-user resolution
- `services/payment/`: payment workflow logic and Stripe webhook reconciliation
- `repositories/`: generic repository adapters and data access helpers
- `models/schemas.py`: compatibility facade for schema imports
- `models/auth_schemas.py`, `models/payment_schemas.py`: domain-split Pydantic contracts

## Backend Layering

- `crud_base` defines the reusable framework primitive.
- `crud_authenticated` extends that primitive for protected routes.
- `auth_session_router` applies the same orchestration model to auth-specific session flows.
- `crud.py` keeps the external import surface stable so the rest of the backend can stay clean and consistent.

## Flow

1. Camera scan or manual paste captures a QR payload.
2. `invoiceService` normalizes it into a displayable invoice model.
3. `authService` logs the user in and persists the bearer session.
4. `paymentService` initializes Stripe Payment Request on supported devices.
5. The backend creates a protected payment intent session and records it through a repository-backed service.
6. Stripe webhook events reconcile final payment status back into stored payment sessions.
7. The UI updates the status timeline and payment history.
