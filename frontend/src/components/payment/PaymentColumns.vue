<script setup>
defineProps({
  left: { type: Array, required: true },
  right: { type: Array, required: true },
})
</script>

<template>
  <div class="stack">
    <component :is="item.component" v-for="item in left" :key="item.id" v-bind="item.props" />
  </div>
  <div class="stack">
    <component :is="item.component" v-for="item in right" :key="item.id" v-bind="item.props" />
  </div>
</template>
