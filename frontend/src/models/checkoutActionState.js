function outcomeTone(payment) {
  if (payment?.error) {
    return 'danger'
  }
  if (payment?.processing) {
    return 'active'
  }
  if (payment?.lastResult) {
    return ['succeeded', 'demo_success'].includes(payment.lastResult.status) ? 'success' : 'warning'
  }
  return 'neutral'
}

function checkoutActionState({ phase, tone, title, message, nextAction, ready, canInitializeWallet }) {
  return {
    phase,
    tone,
    title,
    message,
    nextAction,
    ready,
    canInitializeWallet,
  }
}

export function buildCheckoutActionState({ invoice, session, payment, hasPublishableKey }) {
  if (!invoice) {
    return checkoutActionState({
      phase: 'invoice_required',
      tone: 'neutral',
      title: 'Scan an invoice first',
      message: 'No payment can start until the invoice QR payload has been captured and reviewed.',
      nextAction: 'Scan or paste the invoice payload.',
      ready: false,
      canInitializeWallet: false,
    })
  }

  if (!session?.user) {
    return checkoutActionState({
      phase: 'session_required',
      tone: 'neutral',
      title: 'Authorize the payment session',
      message: 'Sign in before creating the protected payment intent for this invoice.',
      nextAction: 'Complete sign-in or registration.',
      ready: false,
      canInitializeWallet: false,
    })
  }

  if (!hasPublishableKey) {
    return checkoutActionState({
      phase: 'publishable_key_required',
      tone: 'warning',
      title: 'Add Stripe browser configuration',
      message: 'Apple Pay cannot render in the browser until the publishable key is available.',
      nextAction: 'Set VITE_STRIPE_PUBLISHABLE_KEY and reload the app.',
      ready: false,
      canInitializeWallet: false,
    })
  }

  if (payment?.processing) {
    return checkoutActionState({
      phase: 'processing',
      tone: 'active',
      title: 'Processing wallet confirmation',
      message: 'The wallet authorization is in progress. Keep this screen open until the final status appears.',
      nextAction: 'Wait for the payment result.',
      ready: true,
      canInitializeWallet: false,
    })
  }

  if (payment?.error) {
    return checkoutActionState({
      phase: 'retry_required',
      tone: 'danger',
      title: 'Retry the wallet confirmation',
      message: payment.error,
      nextAction: 'Review the invoice and try Apple Pay again.',
      ready: false,
      canInitializeWallet: true,
    })
  }

  if (payment?.lastResult) {
    const successful = ['succeeded', 'demo_success'].includes(payment.lastResult.status)
    return checkoutActionState({
      phase: successful ? 'completed' : 'result_attention',
      tone: successful ? 'success' : 'warning',
      title: successful ? 'Payment completed' : 'Payment needs attention',
      message: payment.lastResult.message,
      nextAction: successful ? 'You can review history or scan another invoice.' : 'Review the result and retry if needed.',
      ready: successful,
      canInitializeWallet: !successful,
    })
  }

  if (payment?.walletAvailable) {
    return checkoutActionState({
      phase: 'wallet_ready',
      tone: 'success',
      title: 'Apple Pay is ready',
      message: payment.walletLabel || 'The wallet is available on this device.',
      nextAction: 'Use the Apple Pay button to confirm the invoice.',
      ready: true,
      canInitializeWallet: true,
    })
  }

  return checkoutActionState({
    phase: 'wallet_pending',
    tone: outcomeTone(payment),
    title: 'Prepare wallet confirmation',
    message: 'Apple Pay appears on supported Safari and Apple devices after invoice review and secure sign-in.',
    nextAction: 'Open the app on a supported device or continue once wallet support is detected.',
    ready: false,
    canInitializeWallet: true,
  })
}
