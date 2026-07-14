# Pegger Project Status

## Current Focus

| ID | Item | Source | Status | Files | Evidence | Remaining Risk |
|---|---|---|---|---|---|---|
| PEG-001 | Add E2E coverage for the guided invoice-to-payment flow | User request | Verified | `frontend/tests/pegger.e2e.spec.js`, `frontend/src/components/payment/InvoiceScannerCard.vue`, `frontend/src/features/home/featureRegistration.js` | `npm run test:e2e`: 3 passed | None identified |
| PEG-002 | Add optical screenshot verification for desktop and mobile payment layouts | User request | Verified | `frontend/tests/pegger.optical.spec.js`, `frontend/tests/pegger.optical.spec.js-snapshots/` | `npm run test:optical`: 2 passed | Baselines are Chromium/Windows snapshots |
| PEG-003 | Keep unknown routes inside the Pegger payment experience | Discovered during E2E setup | Verified | `frontend/src/router/registry.js` | `npm run test:e2e`: unknown route redirects to `/` | None identified |
| PEG-004 | Track implementation and verification status locally | `opencode.md` requirement | Verified | `project_status.md` | Status file created and updated with implementation evidence | None identified |

## Verification Log

| Command | Result | Notes |
|---|---|---|
| `npm install` | Passed | Added `@playwright/test` and updated `frontend/package-lock.json`. Reported existing audit findings: 8 vulnerabilities. |
| `npm run test:run` | Passed | 6 files, 10 unit tests passed after Vitest was scoped to `src/tests/**/*.spec.js`. |
| `npm run build` | Passed | Vite production build completed. |
| `npm run test:e2e` | Passed | 3 Chromium E2E tests passed. |
| `npx playwright test tests/pegger.optical.spec.js --update-snapshots` | Passed | Created desktop and mobile screenshot baselines. |
| `npm run test:optical` | Passed | 2 Chromium optical tests passed against baselines. |

## Architecture Notes

| Area | Boundary Preserved |
|---|---|
| Frontend routes | Route declarations still map feature route definitions to `RegisteredScreenView`; fallback routing stays in the router registry. |
| Frontend UI | Payment components remain presentational and continue emitting intent through props/actions. |
| Tests | E2E and optical tests exercise the runtime app through browser-visible behavior rather than component internals. |
