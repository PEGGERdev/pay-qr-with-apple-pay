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
    <div class="pill">Step 1 · Capture the invoice</div>
    <h2>Scan or paste a QR invoice</h2>
    <p>
      Use the device camera for live scanning or paste the payload directly while building the flow locally.
    </p>

    <div class="button-row" style="margin-top: 18px;">
      <button class="button" type="button" @click="startScanner" :disabled="scanning">
        {{ scanning ? 'Scanner active' : 'Start camera scan' }}
      </button>
      <button class="button-secondary" type="button" @click="stopScanner" :disabled="!scanning">
        Stop scanner
      </button>
      <button class="button-secondary" type="button" @click="loadExample">
        Load sample invoice
      </button>
    </div>

    <div class="scanner-shell" v-if="scanning || scannerError">
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
        Parse invoice
      </button>
    </div>
  </section>
</template>
