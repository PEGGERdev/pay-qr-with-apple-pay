<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({
  invoice: {
    type: Object,
    default: null,
  },
  paymentState: {
    type: Object,
    required: true,
  },
  isAuthenticated: {
    type: Boolean,
    required: true,
  },
  stripePublishableKey: {
    type: String,
    default: '',
  },
  createPaymentRequest: {
    type: Function,
    required: true,
  },
  confirmWalletPayment: {
    type: Function,
    required: true,
  },
})

const walletTarget = ref(null)

const publishableKeyMissing = computed(() => !String(props.stripePublishableKey || '').trim())

const currentState = computed(() => {
  if (!props.invoice) return 'waiting'
  if (!props.isAuthenticated) return 'auth-required'
  if (props.paymentState.processing) return 'processing'
  if (props.paymentState.lastResult) return 'complete'
  if (publishableKeyMissing.value) return 'config-missing'
  return 'ready'
})

const stateMessage = computed(() => {
  switch (currentState.value) {
    case 'waiting':
      return 'Scan an invoice to continue'
    case 'auth-required':
      return 'Sign in to enable payment'
    case 'processing':
      return 'Processing your payment...'
    case 'complete':
      return props.paymentState.lastResult?.message || 'Payment complete!'
    case 'config-missing':
      return 'Contact support to enable payments'
    default:
      return 'Ready to pay'
  }
})

const stateIcon = computed(() => {
  switch (currentState.value) {
    case 'complete':
      return '✓'
    case 'processing':
      return '⟳'
    default:
      return '⏳'
  }
})

let mountedElement = null

function teardownWallet() {
  if (mountedElement) {
    mountedElement.unmount()
    mountedElement = null
  }
}

async function initializeWallet(invoice) {
  teardownWallet()

  if (!invoice || !props.isAuthenticated || publishableKeyMissing.value) {
    return
  }

  try {
    const { stripe, paymentRequest, wallet } = await props.createPaymentRequest(invoice)
    if (!wallet) {
      return
    }

    await nextTick()
    const elements = stripe.elements()
    const element = elements.create('paymentRequestButton', {
      paymentRequest,
      style: {
        paymentRequestButton: {
          theme: 'dark',
          height: '56px',
          type: 'donate',
        },
      },
    })

    if (walletTarget.value) {
      element.mount(walletTarget.value)
      mountedElement = element
    }

    paymentRequest.on('paymentmethod', async (event) => {
      try {
        await props.confirmWalletPayment({
          invoice,
          paymentMethodId: event.paymentMethod.id,
        })
        event.complete('success')
      } catch {
        event.complete('fail')
      }
    })
  } catch (error) {
    console.error('Wallet setup failed:', error)
  }
}

watch(
  () => [props.invoice, props.isAuthenticated],
  async ([invoice]) => {
    await initializeWallet(invoice)
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  teardownWallet()
})
</script>

<template>
  <section class="panel checkout-panel" :class="{ 'is-complete': currentState === 'complete' }">
    <div class="step-badge" v-if="currentState === 'complete'">Complete</div>
    <div class="step-badge" v-else>Step 3</div>

    <h2>Pay with Apple Pay</h2>

    <div v-if="currentState === 'complete'" class="result-display">
      <div class="success-icon">✓</div>
      <p class="result-message">{{ props.paymentState.lastResult?.message }}</p>
      <p class="result-status" v-if="props.paymentState.lastResult?.status">
        {{ props.paymentState.lastResult.status === 'demo_success' ? 'Demo payment' : props.paymentState.lastResult.status }}
      </p>
    </div>

    <div v-else-if="currentState === 'processing'" class="processing-display">
      <div class="spinner"></div>
      <p>Processing your payment...</p>
    </div>

    <template v-else>
      <p class="step-hint">
        {{ stateMessage }}
      </p>

      <div class="wallet-box" v-if="currentState === 'ready'">
        <div class="wallet-target" ref="walletTarget"></div>
      </div>

      <div class="requirements" v-if="currentState !== 'ready'">
        <div class="req-item" :class="{ met: props.invoice }">
          <span class="req-icon">{{ props.invoice ? '✓' : '○' }}</span>
          <span>Invoice loaded</span>
        </div>
        <div class="req-item" :class="{ met: props.isAuthenticated }">
          <span class="req-icon">{{ props.isAuthenticated ? '✓' : '○' }}</span>
          <span>Account connected</span>
        </div>
      </div>
    </template>

    <p class="error-message" v-if="props.paymentState.error">{{ props.paymentState.error }}</p>
    <p class="error-message" v-if="currentState === 'config-missing'">Contact support to enable payments</p>
  </section>
</template>

<style scoped>
.checkout-panel {
  background: linear-gradient(180deg, rgba(15, 118, 110, 0.04), rgba(255, 255, 255, 0.8));
}

.checkout-panel.is-complete {
  background: linear-gradient(180deg, rgba(22, 101, 52, 0.06), rgba(255, 255, 255, 0.9));
}

.step-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(84, 61, 35, 0.08);
  color: var(--muted);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.checkout-panel.is-complete .step-badge {
  background: rgba(22, 101, 52, 0.12);
  color: var(--success);
}

.checkout-panel h2 {
  margin: 12px 0 6px;
  font-size: 1.5rem;
}

.step-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.wallet-box {
  min-height: 60px;
}

.wallet-target {
  padding: 8px 0;
}

.requirements {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  border-radius: 14px;
  background: rgba(84, 61, 35, 0.05);
}

.req-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: var(--muted);
}

.req-item.met {
  color: var(--success);
}

.req-icon {
  font-size: 0.85rem;
}

.result-display {
  text-align: center;
  padding: 24px 16px;
}

.success-icon {
  width: 64px;
  height: 64px;
  border-radius: 999px;
  background: rgba(22, 101, 52, 0.15);
  color: var(--success);
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.result-message {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 6px;
}

.result-status {
  font-size: 0.85rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.processing-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 32px 16px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(15, 118, 110, 0.15);
  border-top-color: var(--accent);
  border-radius: 999px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  margin-top: 16px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(185, 28, 28, 0.08);
  color: var(--danger);
  font-size: 0.9rem;
}
</style>
