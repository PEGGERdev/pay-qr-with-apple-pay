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
  <section class="panel preview-panel" :class="{ 'has-data': invoice }">
    <div class="step-badge" v-if="invoice">Confirmed</div>
    <div class="step-badge pending" v-else>Step 2</div>

    <template v-if="invoice">
      <h2>Invoice details</h2>
      <p class="step-hint">Verify these details before paying.</p>

      <div class="invoice-display">
        <div class="merchant-row">
          <span class="merchant-label">From</span>
          <span class="merchant-name">{{ invoice.merchantName }}</span>
        </div>

        <div class="amount-display">
          <span class="amount-value">{{ amount }}</span>
        </div>

        <div class="description-row" v-if="invoice.description">
          <span class="description-label">For</span>
          <span class="description-text">{{ invoice.description }}</span>
        </div>
      </div>

      <div class="invoice-meta">
        <div class="meta-item">
          <span class="meta-label">Invoice #</span>
          <span class="meta-value">{{ invoice.invoiceId }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Currency</span>
          <span class="meta-value">{{ invoice.currency }} ({{ invoice.countryCode }})</span>
        </div>
      </div>
    </template>

    <template v-else-if="parseError">
      <h2>Could not read invoice</h2>
      <p class="error-message">{{ parseError }}</p>
      <p class="hint">Try scanning again or use a different QR code.</p>
    </template>

    <template v-else>
      <h2>Invoice preview</h2>
      <p class="empty-state">
        Scan a QR code to see the invoice details here.
      </p>
    </template>
  </section>
</template>

<style scoped>
.preview-panel {
  background: linear-gradient(180deg, rgba(15, 118, 110, 0.04), rgba(255, 255, 255, 0.8));
}

.preview-panel.has-data {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.88));
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

.step-badge.pending {
  background: rgba(84, 61, 35, 0.08);
  color: var(--muted);
}

.step-badge.success,
.preview-panel.has-data .step-badge {
  background: rgba(22, 101, 52, 0.12);
  color: var(--success);
}

.preview-panel h2 {
  margin: 12px 0 6px;
  font-size: 1.5rem;
}

.step-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.invoice-display {
  padding: 20px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(15, 118, 110, 0.08), rgba(15, 118, 110, 0.04));
  border: 1px solid rgba(15, 118, 110, 0.15);
  margin-bottom: 16px;
}

.merchant-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 16px;
}

.merchant-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.merchant-name {
  font-size: 1.1rem;
  font-weight: 600;
}

.amount-display {
  margin-bottom: 16px;
}

.amount-value {
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--accent-strong);
  line-height: 1;
}

.description-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.description-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.description-text {
  font-size: 0.95rem;
  color: var(--text);
}

.invoice-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.meta-value {
  font-size: 0.95rem;
  font-weight: 500;
}

.empty-state {
  padding: 32px 16px;
  text-align: center;
  color: var(--muted);
  background: rgba(84, 61, 35, 0.04);
  border-radius: 16px;
  border: 1px dashed rgba(84, 61, 35, 0.12);
}

.error-message {
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(185, 28, 28, 0.08);
  color: var(--danger);
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.hint {
  font-size: 0.85rem;
  color: var(--muted);
}
</style>
