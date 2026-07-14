<script setup>
import { computed, onMounted } from 'vue'
import SlotScreenLayout from '../components/layouts/SlotScreenLayout.vue'
import { useApp } from '../core/injection'

const props = defineProps({
  screen: { type: String, required: true },
})

const app = useApp()

const layout = computed(() => app.screenRegistry.getLayout(props.screen))
const lifecycle = computed(() => app.screenRegistry.getLifecycle(props.screen))
const screenCtx = computed(() => ({ app, screen: props.screen }))

onMounted(async () => {
  const onEnter = lifecycle.value?.onEnter
  if (typeof onEnter === 'function') {
    await onEnter(screenCtx.value)
  }
})
</script>

<template>
  <SlotScreenLayout
    :screen="layout.screen"
    :screen-ctx="screenCtx"
    :slots="layout.slots"
    :screen-class="layout.screenClass"
  />
</template>
