import { loadStripe } from '@stripe/stripe-js'
import { API_ENDPOINTS } from '../api/registry'
import { ApiStateService } from './baseService'

export class PaymentService extends ApiStateService {
  constructor(api, state) {
    super(api, state, { serviceName: 'payment' })
    this._stripe = null
  }

  async stripe() {
    if (this._stripe) return this._stripe

    const key = String(this.state.config.stripePublishableKey || '').trim()
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
    return this.api.request(API_ENDPOINTS.PAYMENTS_CREATE, {
      body: { invoice },
    })
  }

  async loadHistory() {
    try {
      const history = await this.api.request(API_ENDPOINTS.PAYMENTS_HISTORY)
      this.state.payment.history = Array.isArray(history) ? history : []
      return this.state.payment.history
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
        currency: String(invoice.currency || 'EUR').toLowerCase(),
        total: {
          label: invoice.merchantName || 'Invoice payment',
          amount: invoice.amountMinor,
        },
        requestPayerName: true,
        requestPayerEmail: true,
      })

      const wallet = await paymentRequest.canMakePayment()
      this.state.payment.walletAvailable = Boolean(wallet)
      this.state.payment.walletLabel = wallet?.applePay
        ? 'Apple Pay ready'
        : wallet?.googlePay
          ? 'Google Pay ready'
          : wallet
            ? 'Supported wallet ready'
            : ''

      return {
        stripe,
        paymentRequest,
        wallet,
      }
    } catch (error) {
      this.captureError(error, 'Unable to initialize Apple Pay.')
      this.state.payment.error = this.lastError()
      throw error
    }
  }

  async confirmWalletPayment({ invoice, paymentMethodId }) {
    this.clearError()
    this.state.payment.processing = true
    this.state.payment.error = ''

    try {
      const stripe = await this.stripe()
      const intent = await this.createIntent(invoice)
      this.state.payment.demoMode = Boolean(intent.demoMode)

      if (intent.demoMode) {
        const result = {
          status: 'demo_success',
          message: 'Demo mode completed. Add Stripe keys for a real Apple Pay charge.',
          paymentIntentId: intent.paymentIntentId,
        }
        this.state.payment.lastResult = result
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

      const result = {
        status: confirmation.paymentIntent?.status || 'succeeded',
        message: 'Payment completed successfully.',
        paymentIntentId: confirmation.paymentIntent?.id || intent.paymentIntentId,
      }
      this.state.payment.lastResult = result
      await this.loadHistory()
      return result
    } catch (error) {
      this.captureError(error, 'Payment failed.')
      this.state.payment.error = this.lastError()
      throw error
    } finally {
      this.state.payment.processing = false
    }
  }
}
