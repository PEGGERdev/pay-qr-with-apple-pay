export function buildInvoiceReviewActionState({ invoice, parseError }) {
  if (parseError) {
    return {
      tone: 'danger',
      title: 'Invoice needs another scan',
      message: parseError,
      nextAction: 'Clear the payload or rescan the QR code with a cleaner source.',
      ready: false,
    }
  }

  if (!invoice) {
    return {
      tone: 'neutral',
      title: 'Waiting for invoice data',
      message: 'A validated invoice will appear here after a successful scan, upload, or manual payload submission.',
      nextAction: 'Capture the invoice payload to continue.',
      ready: false,
    }
  }

  return {
    tone: 'success',
    title: 'Invoice is ready for review',
    message: 'Merchant, amount, reference, and settlement values have been normalized for confirmation.',
    nextAction: 'Check the values, then continue to Apple Pay confirmation.',
    ready: true,
  }
}
