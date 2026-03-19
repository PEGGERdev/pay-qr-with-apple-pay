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
const walletMessage = ref('Scan an invoice to initialize Apple Pay.')

let mountedElement = null

const publishableKeyMissing = computed(() => !String(props.stripePublishableKey || '').trim())

function teardownWallet() {
  if (mountedElement) {
    mountedElement.unmount()
    mountedElement = null
  }
}

async function initializeWallet(invoice) {
  teardownWallet()

  if (!invoice) {
    walletMessage.value = 'Scan an invoice to initialize Apple Pay.'
    return
  }

  if (!props.isAuthenticated) {
    walletMessage.value = 'Sign in first to create a protected payment intent.'
    return
  }

  if (publishableKeyMissing.value) {
    walletMessage.value = 'Add VITE_STRIPE_PUBLISHABLE_KEY to enable Apple Pay in the browser.'
    return
  }

  try {
    const { stripe, paymentRequest, wallet } = await props.createPaymentRequest(invoice)
    if (!wallet) {
      walletMessage.value = 'Apple Pay is only available on supported Apple devices and Safari.'
      return
    }

    await nextTick()
    const elements = stripe.elements()
    const element = elements.create('paymentRequestButton', {
      paymentRequest,
      style: {
        paymentRequestButton: {
          theme: 'dark',
          height: '52px',
          type: 'donate',
        },
      },
    })

    if (walletTarget.value) {
      element.mount(walletTarget.value)
      mountedElement = element
      walletMessage.value = wallet.applePay
        ? 'Apple Pay is ready. Authenticate on your device to complete the invoice.'
        : 'A supported wallet is ready on this device.'
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
    walletMessage.value = error instanceof Error ? error.message : 'Wallet setup failed.'
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
  <section class="panel">
    <div class="pill">Step 3 · Confirm with Apple Pay</div>
    <h2>Wallet checkout</h2>
    <p>
      Stripe Payment Request exposes Apple Pay on supported Apple hardware and keeps card details off your server.
    </p>

    <div class="wallet-box">
      <div class="wallet-target" ref="walletTarget"></div>
      <p class="mini-note">{{ walletMessage }}</p>
      <p class="mini-note status-warning" v-if="props.paymentState.demoMode">
        Demo mode returned a simulated success because backend Stripe keys are not configured.
      </p>
    </div>

    <div class="result-box" v-if="props.paymentState.lastResult">
      <strong>{{ props.paymentState.lastResult.message }}</strong>
      <p>
        Status: {{ props.paymentState.lastResult.status }}
        <span v-if="props.paymentState.lastResult.paymentIntentId">
          · Intent {{ props.paymentState.lastResult.paymentIntentId }}
        </span>
      </p>
    </div>

    <p class="mini-note status-danger" v-if="props.paymentState.error">{{ props.paymentState.error }}</p>
    <p class="mini-note" v-if="props.paymentState.history.length">
      {{ props.paymentState.history.length }} payment session{{ props.paymentState.history.length === 1 ? '' : 's' }} recorded.
    </p>
    <p class="mini-note status-warning" v-if="publishableKeyMissing">
      Stripe is not wired yet. Add `VITE_STRIPE_PUBLISHABLE_KEY` in `.env`.
    </p>
  </section>
</template>
