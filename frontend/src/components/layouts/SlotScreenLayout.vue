<script setup>
import SlotHost from '../core/SlotHost.vue'

defineProps({
  screen: { type: String, required: true },
  screenCtx: { type: Object, required: true },
  slots: { type: Array, required: true },
  screenClass: { type: String, default: '' },
})
</script>

<template>
  <main :class="screenClass">
    <section class="hero" v-if="slots.includes('header')">
      <SlotHost :screen="screen" slot="header" :screen-ctx="screenCtx" />
    </section>

    <section class="content-grid" v-if="slots.includes('main')">
      <SlotHost :screen="screen" slot="main" :screen-ctx="screenCtx" />
    </section>

    <section v-if="slots.includes('footer')">
      <SlotHost :screen="screen" slot="footer" :screen-ctx="screenCtx" />
    </section>
  </main>
</template>
