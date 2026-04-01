<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { formatInvoiceAmount } from '../../models/invoiceParser'
import { asText } from '../../utils/sanitizers'

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
  checkoutAction: {
    type: Object,
    required: true,
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

const publishableKeyMissing = computed(() => !asText(props.stripePublishableKey))
const invoiceAmount = computed(() => formatInvoiceAmount(props.invoice))

function teardownWallet() {
  if (mountedElement) {
    mountedElement.unmount()
    mountedElement = null
  }
}

async function initializeWallet(invoice) {
  teardownWallet()

  if (!props.checkoutAction.canInitializeWallet || !invoice) {
    walletMessage.value = props.checkoutAction.message
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
  () => [props.invoice, props.checkoutAction.phase],
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
    <div class="pill">Step 4 · Confirm with Apple Pay</div>
    <h2>Review readiness, then confirm with Apple Pay</h2>
    <p>
      Apple Pay is exposed through Stripe Payment Request on supported Apple devices. The final payment confirmation happens in the wallet sheet, not in a custom card form.
    </p>

    <div class="checkout-summary" v-if="props.invoice">
      <div>
        <span>Ready to pay</span>
        <strong>{{ invoiceAmount }}</strong>
      </div>
      <div>
        <span>Merchant</span>
        <strong>{{ props.invoice.merchantName }}</strong>
      </div>
    </div>

    <div class="detail-grid compact-grid readiness-grid">
      <div class="detail-item">
        <span>Invoice</span>
        <strong>{{ props.invoice ? 'Checked' : 'Required' }}</strong>
      </div>
      <div class="detail-item">
        <span>Session</span>
        <strong>{{ props.isAuthenticated ? 'Authorized' : 'Sign in first' }}</strong>
      </div>
      <div class="detail-item">
        <span>Wallet availability</span>
        <strong>{{ props.paymentState.walletAvailable ? 'Ready on this device' : 'Pending device support' }}</strong>
      </div>
      <div class="detail-item">
        <span>History</span>
        <strong>{{ props.paymentState.history.length }} saved</strong>
      </div>
    </div>

    <div class="wallet-box" :data-tone="props.checkoutAction.tone">
      <div class="wallet-target" ref="walletTarget"></div>
      <p class="mini-note">{{ walletMessage }}</p>
      <div class="result-box result-box-inline" :data-tone="props.checkoutAction.tone">
        <strong>{{ props.checkoutAction.title }}</strong>
        <p>{{ props.checkoutAction.message }}</p>
        <span>{{ props.checkoutAction.nextAction }}</span>
      </div>
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
      {{ props.paymentState.history.length }} payment session{{ props.paymentState.history.length === 1 ? '' : 's' }} recorded in your history.
    </p>
    <p class="mini-note status-warning" v-if="publishableKeyMissing">
      Stripe is not wired yet. Add `VITE_STRIPE_PUBLISHABLE_KEY` in `.env`.
    </p>
  </section>
</template>
