import { BaseController } from './baseController'

export class PaymentController extends BaseController {
  constructor(ctx) {
    super(ctx, 'payment')
  }

  createPaymentRequest(invoice) {
    return this.service().createPaymentRequest(invoice)
  }

  confirmWalletPayment(payload) {
    return this.service().confirmWalletPayment(payload)
  }

  loadHistory() {
    return this.service().loadHistory()
  }

  getCurrentStep() {
    const invoice = this._ctx.state.invoice.current
    const session = this._ctx.state.session
    const payment = this._ctx.state.payment

    if (invoice && payment.lastResult) {
      return 4
    }
    if (invoice && session.token) {
      return 3
    }
    if (invoice && !session.token) {
      return 2
    }
    return 1
  }
}
