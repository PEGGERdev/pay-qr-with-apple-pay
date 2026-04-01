<script setup>
import { computed } from 'vue'
import { formatInvoiceAmount } from '../../models/invoiceParser'

const props = defineProps({
  invoice: {
    type: Object,
    default: null,
  },
  parseError: {
    type: String,
    default: '',
  },
  reviewAction: {
    type: Object,
    required: true,
  },
})

const amount = computed(() => formatInvoiceAmount(props.invoice))
const capturedAt = computed(() => {
  if (!props.invoice?.createdAt) {
    return ''
  }

  return new Date(props.invoice.createdAt).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })
})
</script>

<template>
  <section class="panel">
    <div class="pill">Step 3 · Review the invoice</div>
    <h2>Confirm the merchant and amount before paying</h2>
    <p>{{ reviewAction.message }}</p>

    <div class="result-box result-box-inline" :data-tone="reviewAction.tone">
      <strong>{{ reviewAction.title }}</strong>
      <p>{{ reviewAction.message }}</p>
      <span>{{ reviewAction.nextAction }}</span>
    </div>

    <div class="invoice-summary" v-if="invoice">
      <div class="invoice-card">
        <span class="invoice-card-label">Paying</span>
        <span>{{ invoice.merchantName }}</span>
        <strong>{{ amount }}</strong>
        <p>{{ invoice.description }}</p>
      </div>

      <div class="detail-grid">
        <div class="detail-item">
          <span>Invoice reference</span>
          <strong>{{ invoice.invoiceId }}</strong>
        </div>
        <div class="detail-item">
          <span>Currency</span>
          <strong>{{ invoice.currency }}</strong>
        </div>
        <div class="detail-item">
          <span>Settlement country</span>
          <strong>{{ invoice.countryCode }}</strong>
        </div>
        <div class="detail-item">
          <span>Source captured</span>
          <strong>{{ capturedAt }}</strong>
        </div>
      </div>

      <div class="result-box result-box-soft">
        Check these values before confirming with Apple Pay. If anything looks wrong, clear the invoice and scan again.
      </div>
    </div>
  </section>
</template>
