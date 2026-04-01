function statusTone(completed, active) {
  if (completed) {
    return 'success'
  }
  if (active) {
    return 'active'
  }
  return 'idle'
}

export function buildPaymentJourney({ invoice, session, payment, invoiceReviewAction, checkoutAction }) {
  const hasInvoice = Boolean(invoice)
  const hasSession = Boolean(session?.user)
  const walletReady = Boolean(payment?.walletAvailable)
  const hasResult = Boolean(payment?.lastResult)
  const paymentSucceeded = ['succeeded', 'demo_success'].includes(payment?.lastResult?.status)

  const steps = [
    {
      key: 'capture',
      title: 'Capture invoice',
      description: invoiceReviewAction.message,
      completed: invoiceReviewAction.ready,
      active: !invoiceReviewAction.ready,
    },
    {
      key: 'identity',
      title: 'Secure your session',
      description: hasSession
        ? `Signed in as ${session.user.displayName || session.user.username}. Protected payment creation is ready.`
        : 'Sign in or register so the payment intent can be created securely.',
      completed: hasSession,
      active: hasInvoice && !hasSession,
    },
    {
      key: 'wallet',
      title: 'Confirm with Apple Pay',
      description: checkoutAction.message,
      completed: walletReady,
      active: hasInvoice && hasSession && !hasResult && ['wallet_pending', 'wallet_ready', 'publishable_key_required'].includes(checkoutAction.phase),
    },
    {
      key: 'result',
      title: 'Payment result',
      description: hasResult || checkoutAction.phase === 'processing'
        ? checkoutAction.message
        : 'You will see the final payment status here after wallet confirmation.',
      completed: paymentSucceeded,
      active: payment?.processing || (hasResult && !paymentSucceeded),
    },
  ].map((step) => ({
    ...step,
    tone: statusTone(step.completed, step.active),
  }))

  const currentStep = steps.find((step) => step.active) || steps.find((step) => !step.completed) || steps[steps.length - 1]

  return {
    steps,
    currentStep,
    summary: paymentSucceeded ? 'Payment completed' : currentStep.title,
  }
}
