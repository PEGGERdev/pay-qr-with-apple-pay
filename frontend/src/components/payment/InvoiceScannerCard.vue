<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

const props = defineProps({
  onScan: { type: Function, required: true },
})

const manualPayload = ref('')
const scannerId = `qr-reader-${Math.random().toString(36).slice(2)}`
const scanning = ref(false)
const scannerError = ref('')
let scanner = null

const hasPayload = computed(() => Boolean(manualPayload.value.trim()))

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
    // ignored because camera instances can already be released by the browser
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
  <section class="panel">
    <div class="pill">Step 2 · Capture the invoice</div>
    <h2>Scan, upload, or paste the invoice QR payload</h2>
    <p>
      Start with the fastest source available on this device. The invoice is parsed immediately so the amount and merchant can be checked before payment.
    </p>

    <div class="button-row">
      <button class="button" type="button" @click="startScanner" :disabled="scanning">
        {{ scanning ? 'Camera is scanning' : 'Scan with camera' }}
      </button>
      <button class="button-secondary" type="button" @click="stopScanner" :disabled="!scanning">
        Stop camera
      </button>
      <button class="button-secondary" type="button" @click="openGalleryPicker">
        Upload QR image
      </button>
      <button class="button-secondary" type="button" @click="loadExample">
        Load sample payload
      </button>
    </div>

    <div class="support-strip">
      <div class="support-item">
        <strong>Best on mobile</strong>
        <span>Use the rear camera for the quickest scan.</span>
      </div>
      <div class="support-item">
        <strong>Fallback ready</strong>
        <span>Manual paste works for local testing and copied payloads.</span>
      </div>
    </div>

    <input
      ref="fileInputRef"
      type="file"
      accept="image/*"
      class="visually-hidden"
      @change="handleGalleryFile"
    />

    <div class="scanner-shell" v-if="scanning || scannerError">
      <div class="scanner-status-banner" v-if="scanning">Point the camera at the invoice QR code.</div>
      <div :id="scannerId" class="scanner-region"></div>
    </div>

    <p class="mini-note status-danger" v-if="scannerError">{{ scannerError }}</p>

    <div class="form-grid">
      <div class="field">
        <label for="manual-payload">Manual payload</label>
        <textarea
          id="manual-payload"
          class="textarea"
          v-model="manualPayload"
          placeholder="Paste JSON, URI, or key:value invoice data here"
        ></textarea>
      </div>
      <button class="button" type="button" @click="submitManualPayload" :disabled="!hasPayload">
        Review invoice
      </button>
    </div>
  </section>
</template>
