# Payment Workflow

This document defines the complete user payment flow for the QR-to-Apple-Pay application.

## Overview

The application enables users to pay for invoices by scanning QR codes using their mobile device's camera. The payment is processed via Apple Pay (with Stripe as the underlying payment processor).

## User Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PAYMENT JOURNEY                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   SCAN QR    │────▶│  REVIEW      │────▶│   AUTH       │────▶│   PAY        │
│   (Step 1)   │     │   INVOICE    │     │   (Step 3)   │     │   (Step 4)   │
│              │     │   (Step 2)   │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │                    │
       ▼                    ▼                    ▼                    ▼
  Capture QR         Validate &            Login/              Apple Pay
  payload from       display invoice      Register            Wallet
  camera or          details for          session             Payment
  manual input       user review
```

## Detailed Step-by-Step

### Step 1: Scan QR Code

**User Action:**
- Point mobile camera at QR code on invoice
- Or paste QR payload manually

**Technical Flow:**
1. `InvoiceScannerCard` captures QR payload via camera or paste
2. `invoiceService.parse(payload)` normalizes the QR data
3. Invoice is stored in `state.invoice.current`
4. UI displays invoice preview

**QR Payload Format:**
```json
{
  "invoiceId": "INV-2024-001234",
  "amount": 29.99,
  "currency": "USD",
  "merchant": "Merchant Name",
  "description": "Order #12345",
  "dueDate": "2024-12-31T23:59:59Z"
}
```

### Step 2: Review Invoice

**User Action:**
- Verify invoice details (amount, merchant, description)
- Confirm correct invoice before payment

**Technical Flow:**
1. `InvoicePreviewCard` displays invoice details
2. `invoiceReviewActionState` provides validation state
3. User confirms or rejects invoice

**Display Information:**
- Invoice ID
- Amount (formatted with currency)
- Merchant name
- Description
- Due date (if applicable)

### Step 3: Authentication

**User Action:**
- Login with existing account
- Or register new account

**Technical Flow:**
1. `AuthCard` provides login/register form
2. `authService.login()` or `authService.register()` 
3. Session token stored in `state.session`
4. Bearer token sent with subsequent requests

**Authentication Endpoints:**
- `POST /auth/register` - Create new account
- `POST /auth/login` - Authenticate existing account

**Session Management:**
- JWT token issued on successful auth
- Token persisted in frontend state
- Token included in Authorization header

### Step 4: Payment

**User Action:**
- Click "Pay with Apple Pay" button
- Confirm payment in Apple Pay sheet

**Technical Flow:**
1. `ApplePayCheckoutCard` initializes Stripe Payment Request
2. `paymentService.createPaymentRequest(invoice)` creates payment intent
3. Stripe Payment Request button shown on Apple Pay capable devices
4. User authorizes payment in wallet
5. `paymentService.confirmWalletPayment(payload)` confirms payment
6. Backend creates payment session via `payment_service.create_intent()`
7. Stripe webhook reconciles payment status

**Payment Endpoints:**
- `POST /payments/intents` - Create payment intent (authenticated)
- `GET /payments/history` - List payment history (authenticated)
- `POST /payments/webhooks/stripe` - Stripe webhook handler

## Backend Architecture

### Layer Responsibilities

```
┌─────────────────────────────────────────────────────────────────┐
│                     REQUEST FLOW                                  │
└─────────────────────────────────────────────────────────────────┘

  HTTP Request
       │
       ▼
  ┌─────────────┐
  │   Routes    │  ─── FastAPI router, validate & delegate
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │   Actions   │  ─── Business logic, orchestration
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │  Services   │  ─── Domain behavior, external integrations
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │ Repositories│  ─── Persistence, data access
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │  Database   │  ─── MongoDB
  └─────────────┘
```

### Backend Layers

| Layer | Responsibility |
|-------|---------------|
| Routes | HTTP surface, validation, delegation |
| Services | Business logic, Stripe integration, JWT |
| Repositories | MongoDB persistence, queries |
| Models | Schema validation, DTO shaping |

### Key Modules

| Module | Path | Responsibility |
|--------|------|----------------|
| Auth Router | `api/auth_session_router.py` | Register/login endpoints |
| Payment Router | `api/routes/payments.py` | Payment intent, history, webhooks |
| Auth Service | `services/auth/` | JWT issuing, password hashing |
| Payment Service | `services/payment/` | Stripe orchestration, webhook handling |
| Auth Repository | `repositories/auth_repository.py` | User CRUD |
| Payment Repository | `repositories/payment_repository.py` | Payment session CRUD |

## Frontend Architecture

### Layer Responsibilities

```
┌─────────────────────────────────────────────────────────────────┐
│                   FRONTEND FLOW                                  │
└─────────────────────────────────────────────────────────────────┘

  User Interaction
       │
       ▼
  ┌─────────────┐
  │ Components  │  ─── UI rendering, emit intent
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │    Views    │  ─── Screen composition, action binding
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │   Services  │  ─── HTTP calls, external IO
  └─────────────┘
       │
       ▼
  ┌─────────────┐
  │   Stores    │  ─── Reactive state, mutations
  └─────────────┘
```

### Frontend Layers

| Layer | Responsibility |
|-------|---------------|
| Components | UI rendering, event emission |
| Views | Screen composition, action orchestration |
| Services | API calls, payment processing |
| Stores | Reactive state management |

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| HomeView | `views/HomeView.vue` | Main payment screen |
| PaymentHeroPanel | `components/payment/PaymentHeroPanel.vue` | Hero section, trust signals |
| AuthCard | `components/payment/AuthCard.vue` | Login/register form |
| InvoiceScannerCard | `components/payment/InvoiceScannerCard.vue` | QR code scanning |
| InvoicePreviewCard | `components/payment/InvoicePreviewCard.vue` | Invoice display |
| ApplePayCheckoutCard | `components/payment/ApplePayCheckoutCard.vue` | Apple Pay button |
| PaymentTimelineCard | `components/payment/PaymentTimelineCard.vue` | Payment history |

### Action State Models

| Model | File | Purpose |
|-------|------|---------|
| checkoutActionState | `models/checkoutActionState.js` | Checkout button state |
| invoiceReviewActionState | `models/invoiceReviewActionState.js` | Invoice validation state |
| paymentJourney | `models/paymentJourney.js` | Journey progress display |

## State Management

### Application State

```javascript
{
  session: {
    token: string | null,
    user: User | null,
  },
  invoice: {
    current: Invoice | null,
    rawPayload: string,
    parseError: string,
    lastScanAt: timestamp,
  },
  payment: {
    processing: boolean,
    error: string,
    lastResult: PaymentResult | null,
    walletAvailable: boolean,
    walletLabel: string,
    demoMode: boolean,
    history: PaymentRecord[],
  },
  config: {
    apiBaseUrl: string,
    stripePublishableKey: string,
    demoMode: boolean,
  }
}
```

## Security

### Authentication
- JWT tokens with configurable expiration
- Password hashing via bcrypt
- Token in Authorization header

### Payment Security
- Stripe Payment Request for PCI compliance
- Webhook signature verification
- Rate limiting on payment endpoints

### API Security
- CORS configuration
- Trusted host middleware
- HTTPS enforcement (production)

## Error Handling

### Error Categories

| Category | Source | User Message |
|----------|--------|--------------|
| Invalid QR | Scanner | "Invalid QR code. Please scan a valid invoice." |
| Auth Failed | Login | "Incorrect username/email or password" |
| Auth Conflict | Register | "Username or email already exists" |
| Payment Failed | Apple Pay | "Payment failed. Please try again." |
| Network Error | API | "Connection error. Please check your internet." |

### Error State Flow

```
Error Occurs
     │
     ▼
Service captures error
     │
     ▼
Store updates error state
     │
     ▼
Component displays error
     │
     ▼
User takes corrective action
```

## Testing Strategy

### Unit Tests
- Invoice parsing normalization
- Authentication flow
- Payment state transitions

### Integration Tests
- API endpoint workflows
- Service/repository interactions

### E2E Tests (Manual)
- Complete payment journey
- Error recovery flows

## Deployment

### Production Flow
1. Build frontend: `npm run build`
2. Deploy to hosting (Vercel/netlify)
3. Backend to cloud provider (Railway/Render)
4. Configure environment variables
5. Enable Stripe webhooks

### Environment Variables

**Backend:**
- `MONGODB_URI` - MongoDB connection
- `JWT_SECRET_KEY` - JWT signing
- `STRIPE_SECRET_KEY` - Stripe API
- `STRIPE_WEBHOOK_SECRET` - Webhook verification

**Frontend:**
- `VITE_API_BASE_URL` - Backend API URL
- `VITE_STRIPE_PUBLISHABLE_KEY` - Stripe public key
