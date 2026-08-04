<template>
  <div class="digital-ticket" v-if="ticket">
    <!-- Main Pass (Left) -->
    <div class="ticket-main">
      <div class="ticket-header">
        <div class="airline-info">
          <span class="plane-icon">✈️</span>
          <span class="airline-name">{{ ticket.flights?.airline || 'Unknown Airline' }}</span>
        </div>
        <div class="class-tier">
          <span>BOARDING PASS</span>
          <span class="class-type">{{ ticket.flights?.flight_class || 'Economy Class' }}</span>
        </div>
      </div>

      <div class="route-section">
        <div class="airport">
          <span class="code">{{ ticket.flights?.origin || 'SGN' }}</span>
          <span class="city">{{ ticket.flights?.origin_city || 'Ho Chi Minh' }}</span>
        </div>
        <div class="route-icon">
          <span class="path-line"></span>
          <span class="plane-mid">✈️</span>
        </div>
        <div class="airport text-right">
          <span class="code">{{ ticket.flights?.destination || 'HAN' }}</span>
          <span class="city">{{ ticket.flights?.destination_city || 'Ha Noi' }}</span>
        </div>
      </div>

      <div class="details-grid">
        <div class="detail-item">
          <span class="label">PASSENGER</span>
          <span class="value">{{ ticket.passenger_name || 'John Doe' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">FLIGHT</span>
          <span class="value">{{ ticket.flights?.flight_number || 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">SEAT(S)</span>
          <span class="value">{{ formatSeats(ticket.selected_seats) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">DATE / TIME</span>
          <span class="value">{{ formatDateTime(ticket.flights?.departure_time) }}</span>
        </div>
      </div>

      <!-- Pseudo Barcode -->
      <div class="barcode-container">
        <div class="barcode-bars">
          <div v-for="n in 36" :key="n" class="bar" :style="{ width: getBarWidth(n) }"></div>
        </div>
        <span class="barcode-text">REF: {{ ticket.booking_reference || 'TLA-83921' }}</span>
      </div>
      
      <!-- Circle notches for stub connecting area -->
      <div class="notch top-notch"></div>
      <div class="notch bottom-notch"></div>
    </div>

    <!-- Tear-off Stub (Right) -->
    <div class="ticket-stub">
      <div class="stub-header">
        <span class="airline-short">{{ ticket.flights?.airline || 'Airline' }}</span>
        <span class="flight-short">{{ ticket.flights?.flight_number || 'N/A' }}</span>
      </div>
      
      <div class="stub-route">
        <span class="stub-code">{{ ticket.flights?.origin || 'SGN' }}</span>
        <span class="stub-arrow">➔</span>
        <span class="stub-code">{{ ticket.flights?.destination || 'HAN' }}</span>
      </div>

      <div class="stub-details">
        <div class="stub-item">
          <span class="stub-label">PASSENGER</span>
          <span class="stub-val truncate">{{ ticket.passenger_name || 'John Doe' }}</span>
        </div>
        <div class="stub-item">
          <span class="stub-label">SEATS</span>
          <span class="stub-val">{{ formatSeats(ticket.selected_seats) }}</span>
        </div>
        <div class="stub-item">
          <span class="stub-label">GATE</span>
          <span class="stub-val">G12</span>
        </div>
      </div>

      <div class="stub-footer">
        <span class="price-label">Price Paid</span>
        <span class="price-val">${{ ticket.total_price || '0.00' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  ticket: {
    type: Object,
    required: true
  }
});

const formatSeats = (seats) => {
  if (!seats) return 'Any';
  if (Array.isArray(seats)) return seats.join(', ');
  if (typeof seats === 'string') return seats;
  return 'Any';
};

const formatDateTime = (isoString) => {
  if (!isoString) return 'N/A';
  try {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
  } catch (e) {
    return isoString;
  }
};

const getBarWidth = (index) => {
  // Generate pseudo-random barcode line thicknesses
  const widths = ['1px', '2px', '3px', '4px', '1px', '3px', '2px', '1px'];
  return widths[index % widths.length];
};
</script>

<style scoped>
.digital-ticket {
  display: flex;
  width: 100%;
  max-width: 750px;
  background: #fcfbf7;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  overflow: hidden;
  margin: 1.5rem auto;
  border: 1px solid #e5e5d8;
}

/* Main Ticket Area */
.ticket-main {
  flex: 3;
  padding: 1.5rem;
  position: relative;
  border-right: 2px dashed #d1d5db;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.airline-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  color: #1e293b;
  font-family: sans-serif;
  font-size: 1.1rem;
}

.class-tier {
  text-align: right;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.class-type {
  display: block;
  font-weight: 700;
  color: #0284c7;
  font-size: 0.8rem;
  margin-top: 0.1rem;
}

.route-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.airport .code {
  display: block;
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
}

.airport .city {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
  font-family: sans-serif;
}

.route-icon {
  position: relative;
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 1.5rem;
}

.path-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: #cbd5e1;
}

.plane-mid {
  font-size: 1.1rem;
  z-index: 1;
  background: #fcfbf7;
  padding: 0 0.5rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.65rem;
  color: #94a3b8;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.value {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
  margin-top: 0.2rem;
}

.barcode-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  margin-top: auto;
  padding-top: 0.5rem;
}

.barcode-bars {
  display: flex;
  align-items: stretch;
  height: 35px;
  background: #0f172a;
  padding: 2px;
  background: transparent;
  gap: 2px;
}

.bar {
  background: #0f172a;
  height: 100%;
}

.barcode-text {
  font-size: 0.65rem;
  color: #64748b;
  letter-spacing: 0.1em;
}

/* Rounded Notches on Connecting Line */
.notch {
  position: absolute;
  right: -8px;
  width: 16px;
  height: 16px;
  background: #f1f5f9; /* Matches background of container */
  border-radius: 50%;
  border: 1px solid #e5e5d8;
  z-index: 2;
}

.top-notch {
  top: -8px;
}

.bottom-notch {
  bottom: -8px;
}

/* Tear-off Stub Area */
.ticket-stub {
  flex: 1.1;
  padding: 1.5rem;
  background: #f7f6ef;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  border-left: 1px dashed transparent;
}

.stub-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  font-weight: 700;
  color: #475569;
}

.stub-route {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 800;
  font-size: 1.1rem;
  color: #0f172a;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.75rem;
}

.stub-arrow {
  color: #0284c7;
  font-size: 0.9rem;
}

.stub-details {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.stub-item {
  display: flex;
  flex-direction: column;
}

.stub-label {
  font-size: 0.6rem;
  color: #94a3b8;
  font-weight: 700;
}

.stub-val {
  font-size: 0.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-top: 0.1rem;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stub-footer {
  margin-top: auto;
  border-top: 1px solid #e2e8f0;
  padding-top: 0.75rem;
  display: flex;
  flex-direction: column;
}

.price-label {
  font-size: 0.6rem;
  color: #94a3b8;
  font-weight: 700;
}

.price-val {
  font-size: 1.1rem;
  font-weight: 800;
  color: #0284c7;
}

.text-right {
  text-align: right;
}

@media (max-width: 640px) {
  .digital-ticket {
    flex-direction: column;
    max-width: 1000px;
  }
  
  .ticket-main {
    border-right: none;
    border-bottom: 2px dashed #d1d5db;
  }
  
  .notch {
    display: none;
  }
  
  .ticket-stub {
    border-left: none;
    background: #fcfbf7;
  }
}
</style>
