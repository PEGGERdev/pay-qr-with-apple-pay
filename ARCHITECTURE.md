# Architecture

This project borrows the same modular frontend/backend split used in SpotOnSight.

## Frontend

- `src/views/`: route-level screens
- `src/components/`: presentational and feature UI modules
- `src/stores/`: reactive application state and persisted session
- `src/services/`: API gateway, auth, invoice parsing, and Stripe orchestration
- `src/controllers/`: thin UI-facing orchestration layer
- `src/core/`: app context and dependency wiring
- `src/api/`: declarative endpoint registry used by the API gateway

## Backend

- `main.py`: HTTP entrypoint
- `core/application.py`: FastAPI wiring, lifecycle, CORS, and router composition
- `api/crud.py`: generic CRUD/authenticated-create/auth-session router builders adapted from SpotOnSight
- `api/routes/`: feature route modules that stay thin and delegate to services
- `services/auth/`: JWT issuing, password hashing, current-user resolution
- `services/payment/`: payment workflow logic
- `repositories/`: generic file-backed repository adapters with SpotOnSight-like interfaces
- `models/schemas.py`: Pydantic request and response schemas

## Flow

1. Camera scan or manual paste captures a QR payload.
2. `invoiceService` normalizes it into a displayable invoice model.
3. `authService` logs the user in through the generic API gateway stack.
4. `paymentService` initializes Stripe Payment Request on supported devices.
5. The backend creates a protected payment intent session and records it through a repository-backed service.
6. The UI updates the status timeline and payment history.
