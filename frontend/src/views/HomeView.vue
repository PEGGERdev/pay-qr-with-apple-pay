<script setup>
import { computed, onMounted } from 'vue'
import AuthCard from '../components/payment/AuthCard.vue'
import InvoiceScannerCard from '../components/payment/InvoiceScannerCard.vue'
import InvoicePreviewCard from '../components/payment/InvoicePreviewCard.vue'
import ApplePayCheckoutCard from '../components/payment/ApplePayCheckoutCard.vue'
import PaymentTimelineCard from '../components/payment/PaymentTimelineCard.vue'
import PaymentHeroPanel from '../components/payment/PaymentHeroPanel.vue'
import FooterNote from '../components/payment/FooterNote.vue'
import { useApp } from '../core/injection'

const app = useApp()

const authService = app.service('authService')
const invoiceService = app.service('invoice')
const paymentService = app.service('payment')

const state = app.state
const isAuthenticated = computed(() => Boolean(state.session.token))
const authError = computed(() => authService.lastError())
const isDemoMode = computed(() => state.payment.demoMode || state.config.demoMode)

async function login(usernameOrEmail, password) {
  const ok = await authService.login(usernameOrEmail, password)
  if (ok) {
    await paymentService.loadHistory()
  }
  return ok
}

async function register(input) {
  const ok = await authService.register(input)
  if (ok) {
    await paymentService.loadHistory()
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
    await paymentService.loadHistory()
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
        :on-reset="resetInvoice"
      />
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
          :create-payment-request="(invoice) => paymentService.createPaymentRequest(invoice)"
          :confirm-wallet-payment="(payload) => paymentService.confirmWalletPayment(payload)"
        />
      </div>

      <div class="stack">
        <InvoicePreviewCard
          :invoice="state.invoice.current"
          :parse-error="state.invoice.parseError"
        />

        <PaymentTimelineCard
          :invoice="state.invoice.current"
          :payment="state.payment"
          :session="state.session"
        />
      </div>
    </section>

    <FooterNote />
  </main>
</template>
