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
})

const amount = computed(() => formatInvoiceAmount(props.invoice))
</script>

<template>
  <section class="panel">
    <div class="pill">Step 2 · Review the invoice</div>
    <h2>Invoice preview</h2>
    <p v-if="!invoice && !parseError">A validated invoice appears here after a successful scan.</p>
    <p class="status-danger" v-if="parseError">{{ parseError }}</p>

    <div class="invoice-summary" v-if="invoice">
      <div class="invoice-card">
        <span>{{ invoice.merchantName }}</span>
        <strong>{{ amount }}</strong>
        <p>{{ invoice.description }}</p>
      </div>

      <div class="list">
        <div class="list-item">
          <span class="list-badge">#</span>
          <div>
            <strong>{{ invoice.invoiceId }}</strong>
            <p>Invoice reference</p>
          </div>
        </div>
        <div class="list-item">
          <span class="list-badge">{{ invoice.currency }}</span>
          <div>
            <strong>{{ invoice.countryCode }}</strong>
            <p>Settlement country and currency</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
