import { loadStripe } from '@stripe/stripe-js'
import { asLowerText, asText } from '../utils/sanitizers'
import {
  applyDemoModeState,
  applyPaymentErrorState,
  applyPaymentHistoryState,
  applyPaymentOutcomeState,
  applyWalletAvailabilityState,
  beginPaymentState,
  finishPaymentState,
} from '../stores/paymentState'
import { ApiStateService } from './baseService'

export class PaymentService extends ApiStateService {
  constructor(api, state) {
    super(api, state, { serviceName: 'payment' })
    this._stripe = null
  }

  async stripe() {
    if (this._stripe) return this._stripe

    const key = asText(this.state.config.stripePublishableKey)
    if (!key) {
      throw new Error('Stripe publishable key is missing.')
    }

    this._stripe = await loadStripe(key)
    if (!this._stripe) {
      throw new Error('Stripe failed to initialize.')
    }
    return this._stripe
  }

  async createIntent(invoice) {
    return this.api.post('/payments', { invoice }, { token: this.token() })
  }

  async loadHistory() {
    try {
      const history = await this.api.get('/payments/history', { token: this.token() })
      return applyPaymentHistoryState(this.state, history)
    } catch (error) {
      this.captureError(error, 'Could not load payment history.')
      return []
    }
  }

  async createPaymentRequest(invoice) {
    this.clearError()
    try {
      const stripe = await this.stripe()
      const paymentRequest = stripe.paymentRequest({
        country: invoice.countryCode || 'DE',
        currency: asLowerText(invoice.currency || 'EUR'),
        total: {
          label: invoice.merchantName || 'Invoice payment',
          amount: invoice.amountMinor,
        },
        requestPayerName: true,
        requestPayerEmail: true,
      })

      const wallet = await paymentRequest.canMakePayment()
      applyWalletAvailabilityState(this.state, wallet)

      return {
        stripe,
        paymentRequest,
        wallet,
      }
    } catch (error) {
      this.captureError(error, 'Unable to initialize Apple Pay.')
      applyPaymentErrorState(this.state, this.lastError())
      throw error
    }
  }

  async confirmWalletPayment({ invoice, paymentMethodId }) {
    this.clearError()
    beginPaymentState(this.state)

    try {
      const stripe = await this.stripe()
      const intent = await this.createIntent(invoice)
      applyDemoModeState(this.state, intent.demoMode)

      if (intent.demoMode) {
        const result = applyPaymentOutcomeState(this.state, {
          status: 'demo_success',
          message: 'Demo mode completed. Add Stripe keys for a real Apple Pay charge.',
          paymentIntentId: intent.paymentIntentId,
        })
        await this.loadHistory()
        return result
      }

      let confirmation = await stripe.confirmCardPayment(
        intent.clientSecret,
        { payment_method: paymentMethodId },
        { handleActions: false },
      )

      if (confirmation.error) {
        throw confirmation.error
      }

      if (confirmation.paymentIntent?.status === 'requires_action') {
        confirmation = await stripe.confirmCardPayment(intent.clientSecret)
        if (confirmation.error) {
          throw confirmation.error
        }
      }

      const result = applyPaymentOutcomeState(this.state, {
        status: confirmation.paymentIntent?.status || 'succeeded',
        message: 'Payment completed successfully.',
        paymentIntentId: confirmation.paymentIntent?.id || intent.paymentIntentId,
      })
      await this.loadHistory()
      return result
    } catch (error) {
      this.captureError(error, 'Payment failed.')
      applyPaymentErrorState(this.state, this.lastError())
      throw error
    } finally {
      finishPaymentState(this.state)
    }
  }
}
