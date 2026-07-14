<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

const props = defineProps({
  rawPayload: { type: String, default: '' },
  onScan: { type: Function, required: true },
})

const manualPayload = ref('')
const scannerId = `qr-reader-${Math.random().toString(36).slice(2)}`
const scanning = ref(false)
const scannerError = ref('')
let scanner = null

const hasPayload = computed(() => Boolean(manualPayload.value.trim()))

watch(
  () => props.rawPayload,
  (rawPayload) => {
    manualPayload.value = rawPayload || ''
  },
  { immediate: true },
)

async function startScanner() {
  scannerError.value = ''

  try {
    scanner = new Html5Qrcode(scannerId)
    await scanner.start(
      { facingMode: 'environment' },
      { fps: 10, qrbox: { width: 220, height: 220 } },
      async (decodedText) => {
        props.onScan(decodedText)
        manualPayload.value = decodedText
        await stopScanner()
      },
    )
    scanning.value = true
  } catch (error) {
    scannerError.value = error instanceof Error
      ? error.message
      : 'Camera access could not be started.'
  }
}

const fileInputRef = ref(null)

function openGalleryPicker() {
  fileInputRef.value?.click()
}

async function handleGalleryFile(event) {
  const file = event.target.files?.[0]
  if (!file) return

  scannerError.value = ''
  try {
    const galleryScanner = new Html5Qrcode(scannerId)
    const decodedText = await galleryScanner.scanFile(file, false)
    props.onScan(decodedText)
    manualPayload.value = decodedText
  } catch (error) {
    scannerError.value = error instanceof Error
      ? error.message
      : 'No QR code found in the selected image.'
  }
  event.target.value = ''
}

async function stopScanner() {
  if (!scanner) return
  try {
    await scanner.stop()
    await scanner.clear()
  } catch {
  } finally {
    scanner = null
    scanning.value = false
  }
}

function submitManualPayload() {
  props.onScan(manualPayload.value)
}

function loadExample() {
  manualPayload.value = JSON.stringify(
    {
      invoiceId: 'INV-2026-0007',
      merchantName: 'Northline Cafe',
      description: 'Lunch invoice',
      amount: 18.4,
      currency: 'EUR',
      countryCode: 'DE',
    },
    null,
    2,
  )
}

onBeforeUnmount(async () => {
  await stopScanner()
})
</script>

<template>
  <section class="panel scanner-panel">
    <div class="step-badge">Step 1</div>
    <h2>Scan your invoice</h2>
    <p class="step-hint">
      Point your camera at the QR code on your invoice.
    </p>

    <div class="scan-actions">
      <button class="button button-scan" type="button" @click="startScanner" :disabled="scanning">
        <span class="button-icon">📷</span>
        {{ scanning ? 'Scanning...' : 'Scan QR Code' }}
      </button>

      <div class="alt-actions">
        <button class="link-button" type="button" @click="openGalleryPicker">
          Choose from gallery
        </button>
        <span class="divider">or</span>
        <button class="link-button" type="button" @click="loadExample">
          Try a sample
        </button>
      </div>
    </div>

    <input
      ref="fileInputRef"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleGalleryFile"
    />

    <div class="scanner-shell" v-if="scanning || scannerError">
      <div :id="scannerId" class="scanner-region"></div>
    </div>

    <p class="error-message" v-if="scannerError">{{ scannerError }}</p>

    <div class="manual-section">
      <p class="manual-label">Can't scan? Paste the invoice data:</p>
      <textarea
        class="textarea"
        v-model="manualPayload"
        placeholder='{"invoiceId": "INV-001", "amount": 29.99, ...}'
      ></textarea>
      <button class="button-secondary" type="button" @click="submitManualPayload" :disabled="!hasPayload">
        Continue with this data
      </button>
    </div>
  </section>
</template>

<style scoped>
.scanner-panel {
  background: linear-gradient(180deg, rgba(15, 118, 110, 0.04), rgba(255, 255, 255, 0.8));
}

.step-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-strong);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.scanner-panel h2 {
  margin: 12px 0 6px;
  font-size: 1.5rem;
}

.step-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.scan-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
}

.button-scan {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 24px;
  font-size: 1.1rem;
  font-weight: 600;
}

.button-icon {
  font-size: 1.3rem;
}

.alt-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.divider {
  color: var(--muted);
  font-size: 0.85rem;
}

.link-button {
  background: none;
  border: none;
  color: var(--accent-strong);
  font-size: 0.9rem;
  cursor: pointer;
  text-decoration: underline;
  padding: 4px 0;
}

.link-button:hover {
  color: var(--accent);
}

.manual-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px dashed rgba(84, 61, 35, 0.15);
}

.manual-label {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 10px;
}

.error-message {
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 12px;
  background: rgba(185, 28, 28, 0.08);
  color: var(--danger);
  font-size: 0.9rem;
}
</style>
