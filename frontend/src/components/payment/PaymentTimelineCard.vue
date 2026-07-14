<script setup>
import { computed } from 'vue'

const props = defineProps({
  invoice: {
    type: Object,
    default: null,
  },
  payment: {
    type: Object,
    required: true,
  },
  session: {
    type: Object,
    required: true,
  },
})

const steps = computed(() => [
  {
    title: 'Invoice captured',
    text: props.invoice ? 'A QR payload was validated and normalized.' : 'Waiting for a scan or manual payload.',
  },
  {
    title: 'Authenticated session',
    text: props.session.user
      ? `Signed in as ${props.session.user.displayName || props.session.user.username}.`
      : 'No bearer session yet. Payment intent creation is protected.',
  },
  {
    title: 'Wallet prepared',
    text: props.payment.walletAvailable
      ? props.payment.walletLabel || 'Wallet available on this device.'
      : 'Open on Safari/iPhone to surface Apple Pay when supported.',
  },
  {
    title: 'Payment confirmed',
    text: props.payment.lastResult
      ? `${props.payment.lastResult.message} (${props.payment.lastResult.status})`
      : 'No payment has been submitted yet.',
  },
])
</script>

<template>
  <section class="panel">
    <div class="pill">Operational flow</div>
    <h3>Payment timeline</h3>
    <div class="list">
      <div v-for="(step, index) in steps" :key="step.title" class="list-item">
        <span class="list-badge">{{ index + 1 }}</span>
        <div>
          <strong>{{ step.title }}</strong>
          <p>{{ step.text }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
