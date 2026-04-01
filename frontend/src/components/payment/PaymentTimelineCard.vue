<script setup>
defineProps({
  payment: {
    type: Object,
    required: true,
  },
  journey: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <section class="panel">
    <div class="pill">Payment progress</div>
    <h3>Stay oriented through the full flow</h3>
    <p>
      Each stage below reflects the current payment state so the next required action is always visible.
    </p>

    <div class="list">
      <div v-for="(step, index) in journey.steps" :key="step.key" class="timeline-item" :data-tone="step.tone">
        <span class="list-badge">{{ index + 1 }}</span>
        <div>
          <strong>{{ step.title }}</strong>
          <p>{{ step.description }}</p>
        </div>
      </div>
    </div>

    <div class="detail-grid compact-grid" v-if="payment.history.length">
      <div class="detail-item">
        <span>Last status</span>
        <strong>{{ payment.history[0].status }}</strong>
      </div>
      <div class="detail-item">
        <span>Recent invoice</span>
        <strong>{{ payment.history[0].invoice_id }}</strong>
      </div>
    </div>
  </section>
</template>
