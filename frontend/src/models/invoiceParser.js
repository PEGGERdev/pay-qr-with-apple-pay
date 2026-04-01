import { INVOICE_FIELD_DEFINITIONS, INVOICE_PAYLOAD_FORMATS } from './invoiceCatalog'
import { asText, asUpperText } from '../utils/sanitizers'

function normalizeAmount(value) {
  const amount = Number.parseFloat(value)
  if (!Number.isFinite(amount) || amount <= 0) {
    throw new Error('Invoice amount is missing or invalid.')
  }
  return Math.round(amount * 100) / 100
}

function readJsonSource(raw) {
  return JSON.parse(raw)
}

function readUriSource(raw) {
  const queryIndex = raw.indexOf('?')
  const query = queryIndex >= 0 ? raw.slice(queryIndex + 1) : raw
  return new URLSearchParams(query)
}

function readLineSource(raw) {
  return raw
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
}

function sourceValue(source, formatName, key) {
  if (formatName === 'uri') {
    return source.get(key)
  }
  return source?.[key]
}

function readField(source, formatName, definition) {
  for (const alias of definition.aliases) {
    const value = asText(sourceValue(source, formatName, alias))
    if (value) {
      return value
    }
  }
  return definition.fallback
}

function buildInvoice(source, formatName) {
  return {
    invoiceId: readField(source, formatName, INVOICE_FIELD_DEFINITIONS.invoiceId),
    merchantName: readField(source, formatName, INVOICE_FIELD_DEFINITIONS.merchantName),
    description: readField(source, formatName, INVOICE_FIELD_DEFINITIONS.description),
    currency: asUpperText(readField(source, formatName, INVOICE_FIELD_DEFINITIONS.currency), 'EUR'),
    countryCode: asUpperText(readField(source, formatName, INVOICE_FIELD_DEFINITIONS.countryCode), 'DE'),
    amount: normalizeAmount(readField(source, formatName, INVOICE_FIELD_DEFINITIONS.amount)),
  }
}

function parsePayloadSource(raw, formatName) {
  if (formatName === 'json') {
    return readJsonSource(raw)
  }
  if (formatName === 'uri') {
    return readUriSource(raw)
  }
  return readLineSource(raw)
}

export function parseInvoicePayload(rawPayload) {
  const raw = asText(rawPayload)
  if (!raw) {
    throw new Error('Scan a QR code or paste an invoice payload first.')
  }

  const format = INVOICE_PAYLOAD_FORMATS.find((candidate) => candidate.matches(raw))
  const source = parsePayloadSource(raw, format.name)
  const invoice = buildInvoice(source, format.name)

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
