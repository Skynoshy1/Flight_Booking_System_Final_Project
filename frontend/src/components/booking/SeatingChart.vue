<template>
  <div class="seating-chart">
    <div class="chart-header">
      <h3>Select Your Seat</h3>
      <div class="legend">
        <div class="legend-item">
          <div class="seat-indicator available"></div>
          <span>Available</span>
        </div>
        <div class="legend-item">
          <div class="seat-indicator occupied"></div>
          <span>Occupied</span>
        </div>
        <div class="legend-item">
          <div class="seat-indicator selected"></div>
          <span>Selected</span>
        </div>
        <div class="legend-item">
          <div class="seat-indicator user-booked"></div>
          <span>You have booked this seat</span>
        </div>
        <div class="legend-item">
          <div class="seat-indicator locked-by-others"></div>
          <span>Locked by another user</span>
        </div>
      </div>
    </div>

    <div class="layout-container">
      <div class="airplane-container">
        <div class="fuselage">
          <!-- Cockpit -->
          <div class="cockpit">
            <div class="cockpit-window">✈️</div>
            <span class="cockpit-label">COCKPIT</span>
          </div>

          <!-- Seating Area -->
          <div class="seating-area">
            <div v-for="row in totalRows" :key="row" class="seat-row">
              <!-- Left Section (A, B, C) -->
              <div class="seat-section left">
                <span class="row-number">{{ String.fromCharCode(64 + row) }}</span>
                <div class="seats">
                  <button
                    v-for="col in 3"
                    :key="`${row}-${col}`"
                    class="seat"
                    :class="getSeatClass(row, col)"
                    @click="selectSeat(row, col)"
                    :disabled="isSeatOccupied(row, col)"
                  >
                    <span class="seat-label">{{ col }}</span>
                  </button>
                </div>
              </div>

              <!-- Aisle -->
              <div class="aisle"></div>

              <!-- Right Section (D, E, F) -->
              <div class="seat-section right">
                <div class="seats">
                  <button
                    v-for="col in 3"
                    :key="`${row}-${col + 3}`"
                    class="seat"
                    :class="getSeatClass(row, col + 3)"
                    @click="selectSeat(row, col + 3)"
                    :disabled="isSeatOccupied(row, col + 3)"
                  >
                    <span class="seat-label">{{ col + 3 }}</span>
                  </button>
                </div>
                <span class="row-number">{{ String.fromCharCode(64 + row) }}</span>
              </div>
            </div>
          </div>

          <!-- Emergency Exit -->
          <div class="emergency-exit">
            <span>EMERGENCY EXIT</span>
          </div>
        </div>
      </div>

      <!-- Sidebar Class Legend -->
      <div class="sidebar-legend">
        <h4>Seat Classes</h4>
        <div class="legend-class-item">
          <span class="class-dot first-class"></span>
          <div class="class-info">
            <span class="class-name">First Class</span>
            <span class="class-rows">Rows 1-2</span>
            <span class="class-price">$350</span>
          </div>
        </div>
        <div class="legend-class-item">
          <span class="class-dot business-class"></span>
          <div class="class-info">
            <span class="class-name">Business Class</span>
            <span class="class-rows">Rows 3-6</span>
            <span class="class-price">$220</span>
          </div>
        </div>
        <div class="legend-class-item">
          <span class="class-dot economy-class"></span>
          <div class="class-info">
            <span class="class-name">Economy Class</span>
            <span class="class-rows">Rows 7-{{ totalRows }}</span>
            <span class="class-price">$120</span>
          </div>
        </div>
      </div>

    </div>

    <div class="seat-info">
      <div v-if="modelValue && modelValue.length > 0" class="selected-seat-info">
        <span class="info-label">Selected Seat(s):</span>
        <span class="seat-number">{{ selectedSeatsDisplay }}</span>
        <span class="info-label">Price:</span>
        <span class="seat-price">${{ seatPrice }}</span>
      </div>
      <div v-else class="no-seat-info">
        <p>Click on a seat to select it</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  otherOccupied: {
    type: Array,
    default: () => []
  },
  userBooked: {
    type: Array,
    default: () => []
  },
  lockedSeats: {
    type: Array,
    default: () => []
  },
  totalSeats: {
    type: Number,
    default: 180
  }
});


const totalRows = computed(() => {
  const count = props.totalSeats && props.totalSeats > 0 ? props.totalSeats : 180;
  return Math.ceil(count / 6);
});


const emit = defineEmits(['update:modelValue']);

const occupiedSeats = ref([
  '1-1', '1-2', '2-1', '2-5',
  '5-3', '5-4', '5-5', '5-6',
  '10-1', '10-2', '10-3', '10-4', '10-5',
  '15-2', '15-4',
  '20-3', '20-4', '20-5'
]);

const selectedSeatsDisplay = computed(() => {
  if (!props.modelValue || props.modelValue.length === 0) return '';
  return props.modelValue.map(seatId => {
    const [row, col] = seatId.split('-');
    const rowLetter = String.fromCharCode(64 + parseInt(row));
    const colNumber = parseInt(col);
    const colLetter = String.fromCharCode(64 + colNumber);
    return `${rowLetter}${colLetter}`;
  }).join(', ');
});

const seatPrice = computed(() => {
  if (!props.modelValue || props.modelValue.length === 0) return 0;
  return props.modelValue.reduce((total, seatId) => {
    const row = parseInt(seatId.split('-')[0]);
    if (row <= 2) return total + 350;
    if (row <= 6) return total + 220;
    return total + 120;
  }, 0);
});

const isUserBooked = (row, col) => {
  const seatId = `${row}-${col}`;
  return props.userBooked.includes(seatId);
};

const isSeatLocked = (row, col) => {
  const seatId = `${row}-${col}`;
  return props.lockedSeats && props.lockedSeats.includes(seatId);
};

const isSeatOccupied = (row, col) => {
  const seatId = `${row}-${col}`;
  return props.otherOccupied.includes(seatId) || props.userBooked.includes(seatId) || occupiedSeats.value.includes(seatId) || isSeatLocked(row, col);
};

const getSeatClass = (row, col) => {
  const seatId = `${row}-${col}`;
  if (isUserBooked(row, col)) return 'user-booked';
  if (props.modelValue && props.modelValue.includes(seatId)) return 'selected';
  if (isSeatLocked(row, col)) return 'occupied locked-by-others is being selected by another customer';
  if (isSeatOccupied(row, col)) return 'occupied';
  
  if (row <= 2) return 'available first-class';
  if (row <= 6) return 'available business-class';
  return 'available economy-class';
};

const selectSeat = (row, col) => {
  if (isSeatOccupied(row, col)) return;
  
  const seatId = `${row}-${col}`;
  let newSelected = props.modelValue ? [...props.modelValue] : [];
  if (newSelected.includes(seatId)) {
    newSelected = newSelected.filter(id => id !== seatId);
  } else {
    newSelected.push(seatId);
  }
  emit('update:modelValue', newSelected);
};
</script>

<style scoped>
.seating-chart {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #E5E7EB;
}

.chart-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #03121A;
  margin: 0;
}

.legend {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.seat-indicator {
  width: 24px;
  height: 24px;
  border-radius: 4px;
}

.seat-indicator.available {
  background: #E0F2FE;
  border: 1px solid #BAE6FD;
}

.seat-indicator.occupied {
  background: #E5E7EB;
  border: 1px solid #D1D5DB;
}

.seat-indicator.selected {
  background: #FF5E1F;
  border: 1px solid #E54812;
  box-shadow: 0 0 12px rgba(255, 94, 31, 0.4);
}

.layout-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 2rem;
}

.airplane-container {
  display: flex;
  justify-content: center;
  overflow-x: auto;
  padding: 1rem 0;
  flex: 1;
}

.fuselage {
  background: linear-gradient(135deg, #F8F9FB 0%, #F2F7FA 100%);
  border: 2px solid #0194F3;
  border-radius: 50px;
  padding: 2rem;
  min-width: fit-content;
}

.cockpit {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px dashed #0194F3;
}

.cockpit-window {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.cockpit-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #0194F3;
  letter-spacing: 1px;
}

.seating-area {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.seat-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.seat-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.seat-section.left {
  justify-content: flex-end;
}

.seat-section.right {
  justify-content: flex-start;
}

.row-number {
  font-weight: 600;
  color: #0194F3;
  font-size: 0.875rem;
  min-width: 24px;
  text-align: center;
}

.seats {
  display: flex;
  gap: 0.5rem;
}

.seat {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0;
}

.seat:hover:not(:disabled) {
  transform: translateY(-2px);
}

.seat.available.first-class {
  background: rgba(255, 215, 0, 0.15);
  border: 2px solid #FFD700;
  color: #B59410;
}

.seat.available.first-class:hover {
  background: rgba(255, 215, 0, 0.3);
  border-color: #FFD700;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

.seat.available.business-class {
  background: rgba(40, 167, 69, 0.15);
  border: 2px solid #28A745;
  color: #28A745;
}

.seat.available.business-class:hover {
  background: rgba(40, 167, 69, 0.3);
  border-color: #28A745;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.seat.available.economy-class {
  background: #E0F2FE;
  border: 2px solid #BAE6FD;
  color: #0194F3;
}

.seat.available.economy-class:hover {
  background: #BAE6FD;
  border-color: #0194F3;
  box-shadow: 0 4px 12px rgba(1, 148, 243, 0.2);
}

.seat.occupied {
  background: #E5E7EB;
  border: 2px solid #D1D5DB;
  color: #9CA3AF;
  cursor: not-allowed;
}

.seat.occupied::after {
  content: '✕';
  font-weight: bold;
}

.seat.selected {
  background: #FF5E1F;
  border: 2px solid #E54812;
  color: white;
  box-shadow: 0 0 16px rgba(255, 94, 31, 0.6);
  animation: pulse 2s infinite;
}

.seat-label {
  display: none;
}

.seat.available:hover .seat-label,
.seat.selected .seat-label {
  display: inline;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 16px rgba(255, 94, 31, 0.6);
  }
  50% {
    box-shadow: 0 0 20px rgba(255, 94, 31, 0.8);
  }
}

.aisle {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, #0194F3 0%, #FF5E1F 100%);
}

.emergency-exit {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 2px dashed #FF5E1F;
  font-weight: 700;
  color: #FF5E1F;
  font-size: 0.75rem;
  letter-spacing: 1px;
}

.sidebar-legend {
  background: #F8F9FB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 1.5rem;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.sidebar-legend h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: #03121A;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.legend-class-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.class-dot {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  flex-shrink: 0;
}

.class-dot.first-class {
  background: #FFD700;
  border: 1px solid #B59410;
}

.class-dot.business-class {
  background: #28A745;
  border: 1px solid #1E7E34;
}

.class-dot.economy-class {
  background: #0194F3;
  border: 1px solid #0076C2;
}

.class-info {
  display: flex;
  flex-direction: column;
}

.class-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #03121A;
}

.class-rows {
  font-size: 0.75rem;
  color: #6B7280;
  margin-top: 0.125rem;
}

.class-price {
  font-size: 0.75rem;
  font-weight: 700;
  color: #FF5E1F;
  margin-top: 0.125rem;
}

.seat-info {
  background: #F2F7FA;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.selected-seat-info,
.no-seat-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.info-label {
  font-size: 0.875rem;
  color: #6B7280;
  font-weight: 500;
}

.seat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0194F3;
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.seat-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #FF5E1F;
}

.no-seat-info {
  color: #9CA3AF;
  font-weight: 500;
}

@media (max-width: 768px) {
  .seating-chart {
    padding: 1rem;
  }

  .chart-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .legend {
    gap: 0.75rem;
    width: 100%;
  }

  .layout-container {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 100%;
  }

  .sidebar-legend {
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }

  .airplane-container {
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
    padding: 0.5rem 0;
    -webkit-overflow-scrolling: touch;
  }

  .fuselage {
    padding: 1.5rem 1rem;
    min-width: 320px;
    margin: 0 auto;
  }

  .seat-row {
    gap: 0.5rem;
  }

  .seat-section {
    gap: 0.35rem;
  }

  .seats {
    gap: 0.25rem;
  }

  .seat {
    width: 28px;
    height: 28px;
    font-size: 0.7rem;
  }

  .row-number {
    font-size: 0.75rem;
    min-width: 16px;
  }

  .aisle {
    width: 24px;
  }
}


.seat.user-booked {
  background: #FEF2F2;
  border: 2px solid #EF4444;
  color: #EF4444;
  cursor: not-allowed;
  box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
}

.seat.user-booked::after {
  content: '✓';
  font-weight: bold;
}

.seat-indicator.user-booked {
  background: #FEF2F2;
  border: 1px solid #EF4444;
  box-shadow: 0 0 12px rgba(239, 68, 68, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.seat-indicator.user-booked::after {
  content: '✓';
  color: #EF4444;
  font-size: 0.75rem;
  font-weight: bold;
}

.seat.locked-by-others,
.seat.is.being.selected.by.another.customer {
  background: #E5E7EB !important;
  border: 2px dashed #9CA3AF !important;
  color: #9CA3AF !important;
  cursor: not-allowed;
  opacity: 0.7;
}

.seat.locked-by-others::after,
.seat.is.being.selected.by.another.customer::after {
  content: '🔒' !important;
  font-size: 0.75rem;
}

.seat-indicator.locked-by-others {
  background: #E5E7EB;
  border: 1px dashed #9CA3AF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.seat-indicator.locked-by-others::after {
  content: '🔒';
  font-size: 0.6rem;
}
</style>
