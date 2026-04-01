import { describe, expect, it } from 'vitest'
import { parseInvoicePayload } from '../models/invoiceParser'
import { jsonInvoiceScenario, lineInvoiceScenario, uriInvoiceScenario } from './data/scenarios'

describe('parseInvoicePayload', () => {
  it('parses JSON invoice payloads', () => {
    const invoice = parseInvoicePayload(jsonInvoiceScenario())

    expect(invoice.invoiceId).toBe('INV-1')
    expect(invoice.amountMinor).toBe(1250)
    expect(invoice.currency).toBe('EUR')
  })

  it('parses URI invoice payloads', () => {
    const invoice = parseInvoicePayload(uriInvoiceScenario())

    expect(invoice.merchantName).toBe('Cafe')
    expect(invoice.invoiceId).toBe('ABC-1')
    expect(invoice.amountMinor).toBe(1000)
  })

  it('parses line-based invoice payloads through the shared field catalog', () => {
    const invoice = parseInvoicePayload(lineInvoiceScenario())

    expect(invoice.merchantName).toBe('Cafe')
    expect(invoice.invoiceId).toBe('INV-LINE')
    expect(invoice.amountMinor).toBe(1840)
  })
})
