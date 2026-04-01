import { BaseService } from './baseService'
import { parseInvoicePayload } from '../models/invoiceParser'
import { applyParsedInvoiceState, clearInvoiceState } from '../stores/paymentState'

export class InvoiceService extends BaseService {
  constructor(state) {
    super({ serviceName: 'invoice' })
    this.state = state
  }

  parse(rawPayload) {
    this.clearError()
    try {
      const invoice = parseInvoicePayload(rawPayload)
      applyParsedInvoiceState(this.state, {
        rawPayload,
        invoice,
        lastScanAt: new Date().toISOString(),
      })
      return invoice
    } catch (error) {
      this.captureError(error, 'Could not parse invoice payload.')
      this.state.invoice.parseError = this.lastError()
      throw error
    }
  }

  clear() {
    clearInvoiceState(this.state)
  }
}
