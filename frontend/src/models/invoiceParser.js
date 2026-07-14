function normalizeAmount(value) {
  const amount = Number.parseFloat(value)
  if (!Number.isFinite(amount) || amount <= 0) {
    throw new Error('Invoice amount is missing or invalid.')
  }
  return Math.round(amount * 100) / 100
}

function parseJsonPayload(raw) {
  const parsed = JSON.parse(raw)
  return {
    invoiceId: parsed.invoiceId || parsed.id || parsed.reference || 'QR-INVOICE',
    merchantName: parsed.merchantName || parsed.merchant || parsed.payee || 'Invoice merchant',
    description: parsed.description || parsed.label || 'Scanned QR invoice',
    currency: String(parsed.currency || parsed.ccy || 'EUR').toUpperCase(),
    countryCode: String(parsed.countryCode || parsed.country || 'DE').toUpperCase(),
    amount: normalizeAmount(parsed.amount),
  }
}

function parseUriPayload(raw) {
  const queryIndex = raw.indexOf('?')
  const query = queryIndex >= 0 ? raw.slice(queryIndex + 1) : raw
  const params = new URLSearchParams(query)
  return {
    invoiceId: params.get('tr') || params.get('ref') || 'QR-INVOICE',
    merchantName: params.get('pn') || params.get('merchant') || 'Invoice merchant',
    description: params.get('tn') || params.get('description') || 'Scanned QR invoice',
    currency: String(params.get('cu') || params.get('currency') || 'EUR').toUpperCase(),
    countryCode: String(params.get('country') || 'DE').toUpperCase(),
    amount: normalizeAmount(params.get('am') || params.get('amount')),
  }
}

function parseLinePayload(raw) {
  const entries = raw
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.split(/\s*:\s*/, 2))
    .reduce((acc, [key, value]) => {
      if (key && value) {
        acc[key.trim().toLowerCase()] = value.trim()
      }
      return acc
    }, {})

  return {
    invoiceId: entries.invoiceid || entries.reference || 'QR-INVOICE',
    merchantName: entries.merchant || entries.merchantname || 'Invoice merchant',
    description: entries.description || entries.note || 'Scanned QR invoice',
    currency: String(entries.currency || 'EUR').toUpperCase(),
    countryCode: String(entries.country || 'DE').toUpperCase(),
    amount: normalizeAmount(entries.amount),
  }
}

export function parseInvoicePayload(rawPayload) {
  const raw = String(rawPayload || '').trim()
  if (!raw) {
    throw new Error('Scan a QR code or paste an invoice payload first.')
  }

  let invoice
  if (raw.startsWith('{')) {
    invoice = parseJsonPayload(raw)
  } else if (raw.includes('?') || raw.startsWith('upi://') || raw.startsWith('pay://')) {
    invoice = parseUriPayload(raw)
  } else {
    invoice = parseLinePayload(raw)
  }

  return {
    ...invoice,
    amountMinor: Math.round(invoice.amount * 100),
    createdAt: new Date().toISOString(),
    rawPayload: raw,
  }
}

export function formatInvoiceAmount(invoice) {
  if (!invoice) return '--'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: invoice.currency || 'EUR',
  }).format(invoice.amount || 0)
}
