import { BaseService } from './baseService'
import { parseInvoicePayload } from '../models/invoiceParser'

export class InvoiceService extends BaseService {
  constructor(state) {
    super({ serviceName: 'invoice' })
    this.state = state
  }

  parse(rawPayload) {
    this.clearError()
    try {
      const invoice = parseInvoicePayload(rawPayload)
      this.state.invoice.rawPayload = rawPayload
      this.state.invoice.current = invoice
      this.state.invoice.lastScanAt = new Date().toISOString()
      this.state.invoice.parseError = ''
      this.state.payment.lastResult = null
      this.state.payment.error = ''
      return invoice
    } catch (error) {
      this.captureError(error, 'Could not parse invoice payload.')
      this.state.invoice.parseError = this.lastError()
      throw error
    }
  }

  clear() {
    this.state.invoice.rawPayload = ''
    this.state.invoice.current = null
    this.state.invoice.lastScanAt = ''
    this.state.invoice.parseError = ''
    this.state.payment.lastResult = null
    this.state.payment.error = ''
  }
}
