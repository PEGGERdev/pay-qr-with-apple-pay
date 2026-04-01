<script setup>
import { computed, onMounted } from 'vue'
import AuthCard from '../components/payment/AuthCard.vue'
import InvoiceScannerCard from '../components/payment/InvoiceScannerCard.vue'
import InvoicePreviewCard from '../components/payment/InvoicePreviewCard.vue'
import ApplePayCheckoutCard from '../components/payment/ApplePayCheckoutCard.vue'
import PaymentTimelineCard from '../components/payment/PaymentTimelineCard.vue'
import PaymentHeroPanel from '../components/payment/PaymentHeroPanel.vue'
import FooterNote from '../components/payment/FooterNote.vue'
import { buildCheckoutActionState } from '../models/checkoutActionState'
import { buildInvoiceReviewActionState } from '../models/invoiceReviewActionState'
import { buildPaymentJourney } from '../models/paymentJourney'
import { useApp } from '../core/injection'

const app = useApp()

const authService = app.service('authService')
const invoiceService = app.service('invoice')
const paymentService = app.service('payment')

const state = app.state
const isAuthenticated = computed(() => Boolean(state.session.token))
const authError = computed(() => authService.lastError())
const isDemoMode = computed(() => state.payment.demoMode || state.config.demoMode)
const invoiceReviewAction = computed(() => buildInvoiceReviewActionState({
  invoice: state.invoice.current,
  parseError: state.invoice.parseError,
}))
const checkoutAction = computed(() => buildCheckoutActionState({
  invoice: state.invoice.current,
  session: state.session,
  payment: state.payment,
  hasPublishableKey: Boolean(state.config.stripePublishableKey),
}))
const journey = computed(() => buildPaymentJourney({
  ...state,
  invoiceReviewAction: invoiceReviewAction.value,
  checkoutAction: checkoutAction.value,
}))

async function refreshPaymentHistory() {
  if (!state.session.token) {
    return []
  }
  return paymentService.loadHistory()
}

async function login(usernameOrEmail, password) {
  const ok = await authService.login(usernameOrEmail, password)
  if (ok) {
    await refreshPaymentHistory()
  }
  return ok
}

async function register(input) {
  const ok = await authService.register(input)
  if (ok) {
    await refreshPaymentHistory()
  }
  return ok
}

function logout() {
  authService.logout()
}

function parseInvoice(payload) {
  return invoiceService.parse(payload)
}

function handleScan(payload) {
  try {
    parseInvoice(payload)
  } catch {
    return false
  }
  return true
}

function resetInvoice() {
  invoiceService.clear()
}

onMounted(async () => {
  if (isAuthenticated.value) {
    await refreshPaymentHistory()
  }
})
</script>

<template>
  <main class="page-shell">
    <section class="hero">
      <PaymentHeroPanel
        :invoice-ready="Boolean(state.invoice.current)"
        :is-authenticated="isAuthenticated"
        :api-base-url="state.config.apiBaseUrl"
        :is-demo-mode="isDemoMode"
        :payment-state="state.payment"
        :session="state.session"
        :current-step="journey.currentStep"
        :checkout-action="checkoutAction"
        :on-reset="resetInvoice"
      />
    </section>

    <section class="journey-strip" aria-label="Payment progress overview">
      <article
        v-for="(step, index) in journey.steps"
        :key="step.key"
        class="journey-chip"
        :data-tone="step.tone"
      >
        <span class="journey-chip-index">{{ index + 1 }}</span>
        <div>
          <strong>{{ step.title }}</strong>
          <p>{{ step.description }}</p>
        </div>
      </article>
    </section>

    <section class="content-grid">
      <div class="stack">
        <AuthCard
          :auth-state="state.session"
          :auth-error="authError"
          :on-login="login"
          :on-register="register"
          :on-logout="logout"
        />

        <InvoiceScannerCard
          :on-scan="handleScan"
        />

        <ApplePayCheckoutCard
          :invoice="state.invoice.current"
          :payment-state="state.payment"
          :is-authenticated="isAuthenticated"
          :stripe-publishable-key="state.config.stripePublishableKey"
          :checkout-action="checkoutAction"
          :create-payment-request="(invoice) => paymentService.createPaymentRequest(invoice)"
          :confirm-wallet-payment="(payload) => paymentService.confirmWalletPayment(payload)"
        />
      </div>

      <div class="stack">
        <InvoicePreviewCard
          :invoice="state.invoice.current"
          :parse-error="state.invoice.parseError"
          :review-action="invoiceReviewAction"
        />

        <PaymentTimelineCard
          :payment="state.payment"
          :journey="journey"
        />
      </div>
    </section>

    <FooterNote />
  </main>
</template>
