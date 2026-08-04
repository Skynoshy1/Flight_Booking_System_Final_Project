<template>
  <div class="regional-analytics-container">
    <div 
      class="analytics-header-banner" 
      :style="activeAirport?.image_url ? { 
        backgroundImage: `linear-gradient(rgba(1, 148, 243, 0.45), rgba(15, 23, 42, 0.85)), url(${activeAirport.image_url})` 
      } : {}"
    >
      <h2>🗺️ Regional Booking Distribution Management</h2>
      <p>Analyze regional booking densities and track geographic customer volumes across hubs.</p>
    </div>

    <!-- Hub Selection Filter Panel -->
    <div class="filter-card">
      <label for="hub-select">📍 Select Target Departure Hub (Airport Region):</label>
      <select id="hub-select" v-model="selectedHub" @change="filterBookingsByRegion">
        <option v-for="ap in airportList" :key="ap.code" :value="ap.code">
          {{ ap.code }} - {{ ap.name }}
        </option>
      </select>
    </div>

    <!-- Statistics Metrics Panel -->
    <div class="metrics-grid">
      <div class="metric-box">
        <h3>Active Hub Volume</h3>
        <p class="counter-text">{{ filteredBookings.length }} Bookings</p>
        <span class="subtext">Total active check-ins matching region {{ selectedHub }}</span>
      </div>
    </div>

    <!-- Region Passenger Breakdown Table -->
    <div class="table-wrapper">
      <table class="regional-data-table">
        <thead>
          <tr>
            <th>REF #</th>
            <th>PASSENGER NAME</th>
            <th>CONTACT INFORMATION</th>
            <th>FLIGHT ROUTE</th>
            <th>TOTAL AMOUNT</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in filteredBookings" :key="b.id">
            <td><strong>{{ b.booking_reference || ('BK-' + b.id) }}</strong></td>
            <td>{{ b.profiles?.full_name || 'Not Provided' }}</td>
            <td>
              <div class="contact-details">
                <span>📧 {{ b.profiles?.email }}</span>
                <span v-if="b.profiles?.phone">📞 {{ b.profiles?.phone }}</span>
              </div>
            </td>
            <td><span class="route-tag">{{ b.flights?.origin }} ➔ {{ b.flights?.destination }}</span></td>
            <td class="price-highlight">${{ b.total_price }}</td>
          </tr>
          <tr v-if="filteredBookings.length === 0">
            <td colspan="5" class="empty-table-text">No active bookings registered for hub {{ selectedHub }} currently.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const selectedHub = ref('SGN');
const activeAirport = computed(() => {
  return airportList.value.find(ap => ap.code === selectedHub.value) || null;
});
const allGlobalBookings = ref([]);
const filteredBookings = ref([]);
const airportList = ref([]);

const fetchLiveAirports = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/airports/all');
    if (!response.ok) throw new Error('Failed to fetch airports');
    airportList.value = await response.json();
    if (airportList.value.length > 0) {
      selectedHub.value = airportList.value.find(ap => ap.code === 'SGN')?.code || airportList.value[0].code;
    }
    filterBookingsByRegion();
  } catch (error) {
    console.error("Failed to fetch database airports lookup table:", error);
  }
};

const loadGlobalRecords = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/bookings/admin_all');
    if (!response.ok) throw new Error('Failed to fetch regional telemetry');
    allGlobalBookings.value = await response.json();
    filterBookingsByRegion();
  } catch (error) {
    console.error("Failed to compile regional telemetry:", error);
  }
};

const filterBookingsByRegion = () => {
  filteredBookings.value = allGlobalBookings.value.filter(
    b => b.flights?.origin === selectedHub.value
  );
};

onMounted(() => {
  fetchLiveAirports();
  loadGlobalRecords();
});
</script>

<style scoped>
.regional-analytics-container { padding: 2rem; max-width: 1200px; margin: 0 auto; color: #1e293b; }
.analytics-header-banner {
  background-color: #0194F3;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: #ffffff;
  padding: 3rem 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  transition: background-image 0.4s ease-in-out; /* Premium fluid UI switch transition effect */
}
.filter-card { background: #ffffff; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; }
.filter-card select { padding: 10px 16px; border-radius: 6px; border: 1px solid #cbd5e1; font-weight: 600; font-size: 0.95rem; }
.metrics-grid { margin-bottom: 2rem; }
.metric-box { background: #ffffff; padding: 1.5rem; border-radius: 10px; width: 280px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border-left: 5px solid #0194F3; }
.counter-text { font-size: 2rem; font-weight: 800; color: #0194F3; margin: 0.5rem 0; }
.subtext { font-size: 0.75rem; color: #64748b; }
.table-wrapper { background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.regional-data-table { width: 100%; border-collapse: collapse; text-align: left; }
.regional-data-table th { background: #f8fafc; padding: 1rem; font-size: 0.85rem; color: #475569; border-bottom: 2px solid #e2e8f0; }
.regional-data-table td { padding: 1rem; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
.route-tag { background: #f0f9ff; color: #0194F3; padding: 4px 8px; border-radius: 4px; font-weight: 700; }
.price-highlight { font-weight: 700; color: #ff5e1f; }
.contact-details { display: flex; flex-direction: column; gap: 2px; font-size: 0.8rem; color: #475569; }
.empty-table-text { text-align: center; padding: 3rem; color: #94a3b8; font-weight: 500; }
</style>
