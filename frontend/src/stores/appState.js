import { reactive } from 'vue'

const SESSION_KEY = 'pay_qr_session_v1'

function loadSession() {
  try {
    const raw = localStorage.getItem(SESSION_KEY)
    if (!raw) {
      return { token: '', user: null }
    }
    const parsed = JSON.parse(raw)
    return {
      token: typeof parsed.token === 'string' ? parsed.token : '',
      user: parsed.user && typeof parsed.user === 'object' ? parsed.user : null,
    }
  } catch {
    return { token: '', user: null }
  }
}

export function createAppState() {
  const session = loadSession()
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

export function persistSession(state) {
  localStorage.setItem(
    SESSION_KEY,
    JSON.stringify({
      token: state.session.token,
      user: state.session.user,
    }),
  )
}
