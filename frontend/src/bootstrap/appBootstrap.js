import { AppContext } from '../core/context'
import { createAppState, persistSession } from '../stores/appState'
import { ApiClient } from '../services/apiClient'
import { AuthService } from '../services/authService'
import { InvoiceService } from '../services/invoiceService'
import { PaymentService } from '../services/paymentService'

export function buildAppContext() {
  const state = createAppState()

  function handleUnauthorized() {
    state.session.token = ''
    state.session.user = null
    persistSession(state)
  }

  const ctx = new AppContext({
    state,
    serviceFactories: {
      apiClient: (ctx) => new ApiClient(ctx.state.config.apiBaseUrl, { onUnauthorized: handleUnauthorized }),
      authService: (ctx) => new AuthService(ctx.service('apiClient'), ctx.state, { persistSession }),
      invoice: (ctx) => new InvoiceService(ctx.state),
      payment: (ctx) => new PaymentService(ctx.service('apiClient'), ctx.state),
    },
  })

  return ctx
}
