import { AppContext } from '../core/context'
import { createAppState, persistSession } from '../stores/appState'
import { ApiClient } from '../services/apiClient'
import { ApiGatewayService } from '../services/apiGatewayService'
import { AuthService } from '../services/authService'
import { InvoiceService } from '../services/invoiceService'
import { PaymentService } from '../services/paymentService'
import { AuthController } from '../controllers/authController'
import { InvoiceController } from '../controllers/invoiceController'
import { PaymentController } from '../controllers/paymentController'
import { registerUi } from './uiRegistrations'

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
      apiGateway: (ctx) => new ApiGatewayService(ctx.service('apiClient'), ctx.state),
      authService: (ctx) => new AuthService(ctx.service('apiGateway'), ctx.state),
      invoice: (ctx) => new InvoiceService(ctx.state),
      payment: (ctx) => new PaymentService(ctx.service('apiGateway'), ctx.state),
    },
    controllerFactories: {
      auth: (ctx) => new AuthController(ctx),
      invoice: (ctx) => new InvoiceController(ctx),
      payment: (ctx) => new PaymentController(ctx),
    },
  })

  registerUi()
  return ctx
}
