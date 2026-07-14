# Architecture

This project uses a modular frontend/backend split designed for maintainability and reuse.

## Frontend

- `src/views/`: route-level screens
- `src/components/`: presentational and feature UI modules
- `src/stores/`: reactive application state and persisted session
- `src/services/`: API gateway, auth, invoice parsing, and Stripe orchestration
- `src/actions/`: UI-facing orchestration built from generic action helpers and feature-declared action factories
- `src/features/`: feature registrations that declare routes, screens, and slot components
- `src/core/`: app context and dependency wiring
- `src/api/`: declarative endpoint registry used by the API gateway

## Backend

- `main.py`: HTTP entrypoint
- `core/application.py`: FastAPI wiring, lifecycle, CORS, and feature router composition
- `api/crud.py`: generic CRUD/authenticated-create/auth-session router builders
- `api/feature_builders.py`: generic helpers for declared feature specs
- `api/features.py`: declared backend feature registry
- `api/routes/`: feature route modules that stay thin and delegate to services
- `services/auth/`: JWT issuing, password hashing, current-user resolution
- `services/payment/`: payment workflow logic
- `repositories/`: generic repository adapters and data access helpers
- `models/schemas.py`: Pydantic request and response schemas

## Flow

1. Camera scan or manual paste captures a QR payload.
2. `invoiceService` normalizes it into a displayable invoice model.
3. frontend auth and payment actions orchestrate login and history loading through the generic app context.
4. `paymentService` initializes Stripe Payment Request on supported devices.
5. The backend creates a protected payment intent session and records it through a repository-backed service.
6. The UI updates the status timeline and payment history.
