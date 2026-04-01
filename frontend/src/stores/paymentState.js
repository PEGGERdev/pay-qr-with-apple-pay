export function clearPaymentOutcomeState(state) {
  state.payment.lastResult = null
  state.payment.error = ''
}

export function clearPaymentHistoryState(state) {
  state.payment.history = []
}

export function applyPaymentHistoryState(state, history) {
  state.payment.history = Array.isArray(history) ? history : []
  return state.payment.history
}

export function beginPaymentState(state) {
  state.payment.processing = true
  state.payment.error = ''
}

export function finishPaymentState(state) {
  state.payment.processing = false
}

export function applyPaymentOutcomeState(state, result) {
  state.payment.lastResult = result
  return result
}

export function applyPaymentErrorState(state, message) {
  state.payment.error = message
}

export function applyWalletAvailabilityState(state, wallet) {
  state.payment.walletAvailable = Boolean(wallet)
  state.payment.walletLabel = wallet?.applePay
    ? 'Apple Pay ready'
    : wallet?.googlePay
      ? 'Google Pay ready'
      : wallet
        ? 'Supported wallet ready'
        : ''
}

export function applyDemoModeState(state, demoMode) {
  state.payment.demoMode = Boolean(demoMode)
}

export function applyParsedInvoiceState(state, { rawPayload, invoice, lastScanAt }) {
  state.invoice.rawPayload = rawPayload
  state.invoice.current = invoice
  state.invoice.lastScanAt = lastScanAt
  state.invoice.parseError = ''
  clearPaymentOutcomeState(state)
}

export function clearInvoiceState(state) {
  state.invoice.rawPayload = ''
  state.invoice.current = null
  state.invoice.lastScanAt = ''
  state.invoice.parseError = ''
  clearPaymentOutcomeState(state)
}
