<script setup>
defineProps({
  invoiceReady: { type: Boolean, required: true },
  isAuthenticated: { type: Boolean, required: true },
  isDemoMode: { type: Boolean, required: true },
  currentStep: { type: Number, required: true },
  onReset: { type: Function, required: true },
})
</script>

<template>
  <div class="hero-copy">
    <div class="eyebrow">Pay in seconds, not minutes</div>
    <h1>Scan. Confirm. Done.</h1>
    <p>
      Point your phone at any invoice QR code to pay instantly with Apple Pay.
      No account needed to preview — just scan and go.
    </p>
  </div>

  <div class="hero-status">
    <div class="quick-status">
      <div class="status-indicator" :class="{ 'ready': invoiceReady }">
        <span class="status-icon">{{ invoiceReady ? '✓' : '⏳' }}</span>
        <span class="status-label">{{ invoiceReady ? 'Invoice loaded' : 'Waiting for scan' }}</span>
      </div>
      <div class="status-indicator" :class="{ 'ready': isAuthenticated }">
        <span class="status-icon">{{ isAuthenticated ? '✓' : '⏳' }}</span>
        <span class="status-label">{{ isAuthenticated ? 'Signed in' : 'Guest mode' }}</span>
      </div>
    </div>

    <div class="progress-preview">
      <div class="progress-label">Your payment progress</div>
      <div class="progress-dots">
        <div class="dot" :class="{ 'active': currentStep >= 1, 'current': currentStep === 1 }"></div>
        <div class="dot" :class="{ 'active': currentStep >= 2, 'current': currentStep === 2 }"></div>
        <div class="dot" :class="{ 'active': currentStep >= 3, 'current': currentStep === 3 }"></div>
        <div class="dot" :class="{ 'active': currentStep >= 4, 'current': currentStep === 4 }"></div>
      </div>
    </div>

    <div class="button-row">
      <button class="button-text" type="button" @click="onReset" :disabled="!invoiceReady">
        Start over
      </button>
    </div>
  </div>
</template>

<style scoped>
.quick-status {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(84, 61, 35, 0.1);
  transition: all 0.25s ease;
}

.status-indicator.ready {
  background: rgba(22, 101, 52, 0.1);
  border-color: rgba(22, 101, 52, 0.25);
}

.status-indicator.ready .status-icon {
  color: var(--success);
}

.status-icon {
  font-size: 1.1rem;
  color: var(--muted);
}

.status-label {
  font-size: 0.92rem;
  font-weight: 500;
}

.progress-preview {
  margin-top: 8px;
}

.progress-label {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 10px;
}

.progress-dots {
  display: flex;
  gap: 10px;
  align-items: center;
}

.dot {
  flex: 1;
  height: 6px;
  border-radius: 999px;
  background: rgba(84, 61, 35, 0.15);
  transition: all 0.3s ease;
}

.dot.active {
  background: var(--accent);
}

.dot.current {
  background: var(--accent-strong);
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2);
}

.button-text {
  background: none;
  border: none;
  color: var(--muted);
  font-size: 0.9rem;
  padding: 8px 0;
  cursor: pointer;
  text-decoration: underline;
}

.button-text:hover {
  color: var(--text);
}

.button-text:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  text-decoration: none;
}
</style>
