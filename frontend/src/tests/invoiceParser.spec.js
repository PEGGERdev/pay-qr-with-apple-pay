import { describe, expect, it } from 'vitest'
import { parseInvoicePayload } from '../models/invoiceParser'

describe('parseInvoicePayload', () => {
  it('parses JSON invoice payloads', () => {
    const invoice = parseInvoicePayload(JSON.stringify({
      invoiceId: 'INV-1',
      merchantName: 'Cafe',
      amount: 12.5,
      currency: 'EUR',
    }))

    expect(invoice.invoiceId).toBe('INV-1')
    expect(invoice.amountMinor).toBe(1250)
    expect(invoice.currency).toBe('EUR')
  })

  it('parses URI invoice payloads', () => {
    const invoice = parseInvoicePayload('upi://pay?pn=Cafe&am=10.00&cu=eur&tr=ABC-1')

    expect(invoice.merchantName).toBe('Cafe')
    expect(invoice.invoiceId).toBe('ABC-1')
    expect(invoice.amountMinor).toBe(1000)
  })
})
