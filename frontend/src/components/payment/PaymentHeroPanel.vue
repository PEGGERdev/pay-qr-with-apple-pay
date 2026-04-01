<script setup>
defineProps({
  invoiceReady: { type: Boolean, required: true },
  isAuthenticated: { type: Boolean, required: true },
  apiBaseUrl: { type: String, required: true },
  isDemoMode: { type: Boolean, required: true },
  paymentState: { type: Object, required: true },
  session: { type: Object, required: true },
  currentStep: { type: Object, required: true },
  checkoutAction: { type: Object, required: true },
  onReset: { type: Function, required: true },
})
</script>

<template>
  <div class="hero-copy">
    <div class="eyebrow">QR invoice payments with Apple Pay</div>
    <h1>Pay scanned invoices fast, clearly, and with wallet-level trust.</h1>
    <p>
      Review the invoice, verify the merchant and amount, then confirm with Apple Pay on supported devices.
      The flow is designed to keep each step obvious and reduce uncertainty before money moves.
    </p>

    <div class="hero-trust-list">
      <div class="hero-trust-item">
        <strong>Protected payment intent</strong>
        <span>Authentication is required before checkout can start.</span>
      </div>
      <div class="hero-trust-item">
        <strong>Wallet-first confirmation</strong>
        <span>Apple Pay is surfaced through Stripe Payment Request on supported Safari devices.</span>
      </div>
      <div class="hero-trust-item">
        <strong>Visible invoice checks</strong>
        <span>Amount, reference, merchant, and settlement details stay visible before payment.</span>
      </div>
    </div>
  </div>

  <div class="hero-status">
    <div class="hero-status-block">
      <div class="pill">Current step · {{ currentStep.title }}</div>
      <h2>{{ currentStep.title }}</h2>
      <p>{{ currentStep.description }}</p>

      <div class="metric-grid hero-metrics">
        <div class="metric">
          <span>Invoice</span>
          <strong>{{ invoiceReady ? 'Ready' : 'Needed' }}</strong>
        </div>
        <div class="metric">
          <span>Session</span>
          <strong>{{ isAuthenticated ? 'Verified' : 'Sign in' }}</strong>
        </div>
        <div class="metric">
          <span>Checkout</span>
          <strong>{{ checkoutAction.ready ? 'Ready' : 'Pending' }}</strong>
        </div>
        <div class="metric">
          <span>Mode</span>
          <strong>{{ isDemoMode ? 'Demo' : 'Live' }}</strong>
        </div>
      </div>
    </div>

    <div class="hero-status-footer">
      <div class="hero-action-box" :data-tone="checkoutAction.tone">
        <strong>{{ checkoutAction.title }}</strong>
        <p>{{ checkoutAction.message }}</p>
        <span>{{ checkoutAction.nextAction }}</span>
      </div>
      <div class="hero-inline-note">
        <span class="status-dot" :data-live="!isDemoMode"></span>
        <span>
          {{ isDemoMode ? 'Demo mode is enabled for safe UI testing.' : 'Live mode is configured for real Stripe checkout.' }}
        </span>
      </div>
      <div class="hero-inline-note subtle">
        <span>{{ session.user ? session.user.email : apiBaseUrl }}</span>
      </div>
      <div class="button-row button-row-compact">
        <button class="button-secondary" type="button" @click="onReset">Clear invoice</button>
      </div>
    </div>
  </div>
</template>
