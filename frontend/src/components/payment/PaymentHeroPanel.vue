<script setup>
defineProps({
  invoiceReady: { type: Boolean, required: true },
  isAuthenticated: { type: Boolean, required: true },
  apiBaseUrl: { type: String, required: true },
  isDemoMode: { type: Boolean, required: true },
  onReset: { type: Function, required: true },
})
</script>

<template>
  <div class="hero-copy">
    <div class="eyebrow">Vue + Stripe + Apple Pay</div>
    <h1>Scan invoice QR codes and pay in one motion.</h1>
    <p>
      This app turns payment QR payloads into a clean checkout flow with a mobile-first Vue interface,
      a SpotOnSight-inspired FastAPI backend, and Stripe-powered wallet confirmation.
    </p>
  </div>

  <div class="hero-status">
    <div>
      <div class="pill">SpotOnSight-inspired modular structure</div>
      <div class="metric-grid" style="margin-top: 18px;">
        <div class="metric">
          <span>QR status</span>
          <strong>{{ invoiceReady ? 'Parsed' : 'Waiting' }}</strong>
        </div>
        <div class="metric">
          <span>Session</span>
          <strong>{{ isAuthenticated ? 'Active' : 'Guest' }}</strong>
        </div>
        <div class="metric">
          <span>API target</span>
          <strong>{{ apiBaseUrl }}</strong>
        </div>
        <div class="metric">
          <span>Mode</span>
          <strong>{{ isDemoMode ? 'Demo-friendly' : 'Live-ready' }}</strong>
        </div>
      </div>
    </div>

    <div class="button-row">
      <button class="button-secondary" type="button" @click="onReset">Reset invoice</button>
    </div>
  </div>
</template>
