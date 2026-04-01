import { reactive } from 'vue'
import { loadPersistedSession, persistSession } from './sessionState'

export function createAppState() {
  const session = loadPersistedSession()
  return reactive({
    config: {
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
      stripePublishableKey: import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || '',
      demoMode: String(import.meta.env.VITE_DEMO_MODE || 'true').toLowerCase() === 'true',
    },
    session,
    invoice: {
      rawPayload: '',
      current: null,
      lastScanAt: '',
      parseError: '',
    },
    payment: {
      walletAvailable: false,
      walletLabel: '',
      processing: false,
      demoMode: false,
      lastResult: null,
      error: '',
      history: [],
    },
  })
}

export { persistSession }
