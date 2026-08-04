<template>
  <div class="analytics-card">
    <div class="card-header">
      <div class="card-title">{{ title }}</div>
      <div class="icon-wrapper">{{ icon }}</div>
    </div>
    
    <div class="card-body">
      <div class="value">{{ value }}</div>
      <div class="change" :class="trend">
        <span v-if="trend === 'up'">↑</span>
        <span v-else>↓</span>
        {{ change }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: String,
  change: String,
  trend: {
    type: String,
    default: 'up'
  },
  icon: String
});
</script>

<style scoped>
.analytics-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #E5E7EB;
  transition: all 0.3s ease;
}

.analytics-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(1, 148, 243, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.icon-wrapper {
  font-size: 1.5rem;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.value {
  font-size: 2rem;
  font-weight: 700;
  color: #03121A;
}

.change {
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.change.up {
  color: #10B981;
}

.change.down {
  color: #EF4444;
}
</style>
