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
}
