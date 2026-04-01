export const INVOICE_FIELD_DEFINITIONS = {
  invoiceId: {
    aliases: ['invoiceId', 'id', 'reference', 'tr', 'ref', 'invoiceid'],
    fallback: 'QR-INVOICE',
  },
  merchantName: {
    aliases: ['merchantName', 'merchant', 'payee', 'pn', 'merchantname'],
    fallback: 'Invoice merchant',
  },
  description: {
    aliases: ['description', 'label', 'tn', 'note'],
    fallback: 'Scanned QR invoice',
  },
  currency: {
    aliases: ['currency', 'ccy', 'cu'],
    fallback: 'EUR',
  },
  countryCode: {
    aliases: ['countryCode', 'country'],
    fallback: 'DE',
  },
  amount: {
    aliases: ['amount', 'am'],
  },
}

export const INVOICE_PAYLOAD_FORMATS = [
  {
    name: 'json',
    matches(raw) {
      return raw.startsWith('{')
    },
  },
  {
    name: 'uri',
    matches(raw) {
      return raw.includes('?') || raw.startsWith('upi://') || raw.startsWith('pay://')
    },
  },
  {
    name: 'lines',
    matches() {
      return true
    },
  },
]
