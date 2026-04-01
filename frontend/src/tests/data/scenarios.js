export function authResponseScenario() {
  return {
    access_token: 'token-1',
    user: {
      id: 'user-1',
      username: 'demo',
      email: 'demo@example.com',
      display_name: 'Demo',
    },
  }
}

export function authStateScenario() {
  return {
    session: { token: '', user: null },
    payment: { history: [] },
  }
}

export function lineInvoiceScenario() {
  return 'merchant: Cafe\namount: 18.40\nreference: INV-LINE'
}

export function jsonInvoiceScenario() {
  return JSON.stringify({
    invoiceId: 'INV-1',
    merchantName: 'Cafe',
    amount: 12.5,
    currency: 'EUR',
  })
}

export function uriInvoiceScenario() {
  return 'upi://pay?pn=Cafe&am=10.00&cu=eur&tr=ABC-1'
}
