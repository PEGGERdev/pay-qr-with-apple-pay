<script setup>
import { computed } from 'vue'
import { getComponents } from '../../core/registry'

const props = defineProps({
  screen: { type: String, required: true },
  slot: { type: String, required: true },
  screenCtx: { type: Object, required: true },
})

const components = computed(() => getComponents(props.screen, props.slot))

function buildProps(spec) {
  if (typeof spec.buildProps !== 'function') return {}
  return spec.buildProps(props.screenCtx) || {}
}
</script>

<template>
  <template v-for="spec in components" :key="spec.id">
    <component :is="spec.component" v-bind="buildProps(spec)" />
  </template>
</template>
