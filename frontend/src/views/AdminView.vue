<template>
  <div class="admin-view">
    <!-- Header -->
    <section class="admin-header">
      <div class="container">
        <h1>Admin Dashboard</h1>
        <p class="subtitle">Manage flights, bookings, and revenue analytics</p>
      </div>
    </section>

    <!-- Content -->
    <section class="admin-content">
      <div class="container">
        <!-- Stats Cards -->
        <div class="stats-grid">
          <AnalyticsCard
            title="Total Revenue"
            :value="'$' + (stats.total_revenue || 0).toLocaleString()"
            change="+12.5%"
            trend="up"
            icon="💰"
          />
          <AnalyticsCard
            title="Active Flights"
            :value="String(stats.active_flights || 0)"
            change="+3"
            trend="up"
            icon="✈️"
          />
          <AnalyticsCard
            title="Total Bookings"
            :value="String(stats.total_bookings || 0)"
            change="+8.2%"
            trend="up"
            icon="🎫"
          />
          <AnalyticsCard
            title="Avg. Booking Value"
            :value="'$' + (stats.avg_booking_value || 0).toFixed(2)"
            change="+4.3%"
            trend="up"
            icon="📊"
          />
        </div>

        <!-- Tabs -->
        <div class="admin-tabs">
          <button 
            v-for="tab in ['Flights', 'Bookings', 'Revenue', 'Analytics']"
            :key="tab"
            :class="['tab-btn', { active: activeTab === tab }]"
            @click="activeTab = tab"
          >
            {{ tab }}
          </button>
        </div>

        <!-- Flights Table -->
        <div v-if="activeTab === 'Flights'" class="admin-card">
          <div class="card-header">
            <h2>Flight Management</h2>
            <button class="btn-add" @click="flightTableRef?.openAddModal()">+ Add New Flight</button>
          </div>
          <FlightTable ref="flightTableRef" :flights="adminFlights" @flight-updated="handleFlightUpdated" />
        </div>

        <!-- Bookings Table -->
        <div v-if="activeTab === 'Bookings'" class="admin-card">
          <div class="card-header">
            <h2>Recent Bookings</h2>
          </div>
          <div class="table-responsive-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Booking ID</th>
                  <th>Passenger</th>
                  <th>Flight</th>
                  <th>Date</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="b in paginatedBookings" :key="b.id">
                  <td>{{ b.booking_reference || ('BK00' + b.id) }}</td>
                  <td>{{ b.profiles?.full_name || b.profiles?.email || 'Anonymous User' }}</td>
                  <td>{{ b.flights?.flight_number || 'N/A' }}</td>
                  <td>{{ new Date(b.created_at).toLocaleDateString('en-CA') }}</td>
                  <td>${{ b.total_price }}</td>
                  <td>
                    <span class="badge status-confirmed">CONFIRMED</span>
                  </td>
                  <td>
                    <button class="action-view-btn" @click="openBookingModal(b)">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>


          <nav v-if="bookingTotalPages > 1" class="pagination-nav" aria-label="Bookings Pagination">
            <button
              class="pagination-btn"
              :disabled="bookingCurrentPage === 1"
              @click="bookingCurrentPage = 1"
              aria-label="First page"
            >
              « First
            </button>
            <button
              class="pagination-btn"
              :disabled="bookingCurrentPage === 1"
              @click="bookingCurrentPage--"
              aria-label="Previous page"
            >
              ‹ Prev
            </button>

            <div class="page-numbers">
              <button
                v-for="page in bookingTotalPages"
                :key="page"
                class="pagination-btn page-num-btn"
                :class="{ 'active-page': bookingCurrentPage === page }"
                @click="bookingCurrentPage = page"
              >
                {{ page }}
              </button>
            </div>

            <button
              class="pagination-btn"
              :disabled="bookingCurrentPage === bookingTotalPages"
              @click="bookingCurrentPage++"
              aria-label="Next page"
            >
              Next ›
            </button>
            <button
              class="pagination-btn"
              :disabled="bookingCurrentPage === bookingTotalPages"
              @click="bookingCurrentPage = bookingTotalPages"
              aria-label="Last page"
            >
              Last »
            </button>
          </nav>
        </div>

        <!-- Revenue Chart -->
        <div v-if="activeTab === 'Revenue'" class="admin-card">
          <div class="card-header">
            <h2>Revenue Analytics</h2>
          </div>
          <div class="chart-container">
            <div v-if="!revenueChartData" class="loading-container">
              <span class="spinner">🌀</span>
              <p>Loading revenue data...</p>
            </div>
            <div v-else class="chart-box" style="height: 350px; position: relative;">
              <Bar :data="revenueChartData" :options="revenueChartOptions" />
            </div>
          </div>
        </div>

        <!-- Analytics Chart Cards -->
        <div v-if="activeTab === 'Analytics'" class="admin-card">
          <div class="card-header">
            <h2>Airline Performance Analytics</h2>
          </div>
          <div v-if="!analyticsData" class="loading-container">
            <span class="spinner">🌀</span>
            <p>Loading analytics data from backend...</p>
          </div>
          <div v-else class="analytics-charts-grid">
            <div class="chart-wrapper">
              <h3>Flight Type Popularity</h3>
              <div class="chart-box">
                <Doughnut v-if="flightTypeData" :data="flightTypeData" :options="flightTypeOptions" :plugins="[doughnutLabelsPlugin]" />
              </div>
            </div>
            <div class="chart-wrapper">
              <h3>Airlines Performance</h3>
              <div class="chart-box">
                <Bar :data="chart2Data" :options="chart2Options" :plugins="[datalabelsPlugin, glowPlugin]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- View Booking Details Modal -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="showBookingModal && selectedBooking" class="modal-overlay-booking" @click.self="closeBookingModal">
          <div class="booking-modal-card">
            <!-- Header -->
            <div class="booking-modal-header">
              <div class="header-main">
                <span class="header-icon">🎫</span>
                <div>
                  <h3>Booking Details</h3>
                  <p class="ref-sub">REF: {{ selectedBooking.booking_reference || ('BK00' + selectedBooking.id) }}</p>
                </div>
              </div>
              <button class="modal-close-btn" @click="closeBookingModal">✕</button>
            </div>

            <!-- Body -->
            <div class="booking-modal-body">
              <!-- Grid Container -->
              <div class="booking-details-grid">
                
                <!-- Section 1: Passenger Info -->
                <div class="details-section">
                  <h4 class="section-title">👤 Passenger Information</h4>
                  <div class="details-card">
                    <div class="detail-row">
                      <span class="detail-label">Full Name:</span>
                      <span class="detail-val">{{ selectedBooking.profiles?.full_name || selectedBooking.profiles?.username || 'N/A' }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Email:</span>
                      <span class="detail-val">{{ selectedBooking.profiles?.email || 'N/A' }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Gender:</span>
                      <span class="detail-val capitalize">{{ selectedBooking.profiles?.gender || 'N/A' }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">City:</span>
                      <span class="detail-val">{{ selectedBooking.profiles?.city || 'N/A' }}</span>
                    </div>
                  </div>
                </div>

                <!-- Section 2: Booking Info -->
                <div class="details-section">
                  <h4 class="section-title">💳 Fare & Ticket Details</h4>
                  <div class="details-card">
                    <div class="detail-row">
                      <span class="detail-label">Passenger Count:</span>
                      <span class="detail-val">{{ selectedBooking.passenger_count }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Total Price:</span>
                      <span class="detail-val price-val-highlight">${{ selectedBooking.total_price }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Discount Applied:</span>
                      <span class="detail-val">${{ selectedBooking.discount_applied || 0.0 }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Selected Seats:</span>
                      <span class="detail-val seats-badge-list">
                        <span v-for="seat in (selectedBooking.selected_seats || [])" :key="seat" class="seat-badge">
                          {{ seat }}
                        </span>
                        <span v-if="!selectedBooking.selected_seats || selectedBooking.selected_seats.length === 0" class="detail-val">
                          None
                        </span>
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Section 3: Flight Info -->
                <div class="details-section span-full">
                  <h4 class="section-title">✈️ Flight Information</h4>
                  <div class="details-card flight-info-card">
                    <div class="flight-grid">
                      <div class="detail-row">
                        <span class="detail-label">Airline:</span>
                        <span class="detail-val font-bold">{{ selectedBooking.flights?.airline || 'N/A' }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">Flight Number:</span>
                        <span class="detail-val font-bold text-sky">{{ selectedBooking.flights?.flight_number || 'N/A' }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">Trip Type:</span>
                        <span class="detail-val capitalize">{{ selectedBooking.flights?.trip_type || 'one-way' }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">Route:</span>
                        <span class="detail-val route-span">
                          {{ selectedBooking.flights?.origin || 'N/A' }} ➔ {{ selectedBooking.flights?.destination || 'N/A' }}
                        </span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">Departure Date:</span>
                        <span class="detail-val">{{ selectedBooking.flights?.departure_date || 'N/A' }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">Departure Time:</span>
                        <span class="detail-val">
                          {{ selectedBooking.flights?.departure_time ? new Date(selectedBooking.flights?.departure_time).toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit', hour12: false}) : 'N/A' }}
                        </span>
                      </div>
                      <div class="detail-row" v-if="selectedBooking.flights?.trip_type === 'round-trip'">
                        <span class="detail-label">Return Date:</span>
                        <span class="detail-val">{{ selectedBooking.flights?.return_date || 'N/A' }}</span>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

            <!-- Footer with Red Close Button -->
            <div class="booking-modal-footer">
              <button class="btn-close-red" @click="closeBookingModal">Close Menu</button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import AnalyticsCard from '../components/admin/AnalyticsCard.vue';
import FlightTable from '../components/admin/FlightTable.vue';
import apiClient from '../utils/apiClient.js';
import { supabase } from '../supabase.js';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { Bar, Doughnut } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const activeTab = ref('Flights');
const flightTableRef = ref(null);
const analyticsData = ref(null);
const flightTypePopularity = ref({ one_way: 0, round_trip: 0, total: 0 });
let realtimeChannel = null;

const fetchFlightTypePopularity = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/analytics/flight-type-popularity');
    if (!response.ok) throw new Error('Failed to fetch flight type popularity');
    flightTypePopularity.value = await response.json();
  } catch (error) {
    console.error('Error fetching flight type popularity:', error);
  }
};

const flightTypeData = computed(() => {
  if (!flightTypePopularity.value) return null;
  return {
    labels: ['One-way', 'Round-trip'],
    datasets: [
      {
        data: [flightTypePopularity.value.one_way || 0, flightTypePopularity.value.round_trip || 0],
        backgroundColor: ['#0194F3', '#EF4444'],
        hoverBackgroundColor: ['#0077C8', '#DC2626'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }
    ]
  };
});

const flightTypeOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        font: {
          size: 13,
          weight: '600'
        },
        padding: 15,
        usePointStyle: true,
        pointStyle: 'circle'
      }
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || '';
          const value = context.raw || 0;
          const total = flightTypePopularity.value.total || (flightTypePopularity.value.one_way + flightTypePopularity.value.round_trip) || 1;
          const percentage = Math.round((value / total) * 100);
          return ` ${label}: ${value} bookings (${percentage}%)`;
        }
      }
    }
  },
  cutout: '60%'
};

const doughnutLabelsPlugin = {
  id: 'doughnutLabels',
  afterDatasetsDraw(chart) {
    const { ctx, data } = chart;
    const meta = chart.getDatasetMeta(0);
    if (!meta || !meta.data) return;

    ctx.save();
    ctx.font = 'bold 13px sans-serif';
    ctx.fillStyle = '#FFFFFF';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    meta.data.forEach((element, index) => {
      const value = data.datasets[0].data[index];
      if (value > 0) {
        const { x, y } = element.tooltipPosition();
        ctx.fillText(value, x, y);
      }
    });
    ctx.restore();
  }
};


const likesSummary = ref([]);

const fetchLikesSummary = async () => {
  try {
    const response = await apiClient.get('/likes/summary');
    likesSummary.value = response.data || [];
  } catch (error) {
    console.error('Error fetching likes summary:', error);
  }
};

const chart2Data = computed(() => {
  if (!likesSummary.value || likesSummary.value.length === 0) {
    return {
      labels: [],
      datasets: [
        {
          label: 'Likes',
          backgroundColor: [],
          data: [],
          borderRadius: 6
        }
      ]
    };
  }
  
  const labels = likesSummary.value.map(item => item.airline);
  const data = likesSummary.value.map(item => item.like_count);
  
  const defaultColors = [
    '#0194F3', // Blue
    '#F59E0B', // Amber
    '#10B981', // Emerald
    '#6366F1', // Indigo
    '#EC4899', // Pink
    '#8B5CF6', // Purple
    '#0EA5E9'  // Cyan
  ];
  
  const bgColors = labels.map((_, index) => {
    return defaultColors[index % defaultColors.length];
  });
  
  return {
    labels,
    datasets: [
      {
        label: 'Likes',
        backgroundColor: bgColors,
        data: data,
        borderRadius: 6
      }
    ]
  };
});

const revenueChartData = computed(() => {
  if (!weeklyRevenue.value || weeklyRevenue.value.length === 0) return null;
  return {
    labels: weeklyRevenue.value.map(item => item.date),
    datasets: [
      {
        label: 'Weekly Revenue ($)',
        backgroundColor: '#0194F3',
        data: weeklyRevenue.value.map(item => item.amount)
      }
    ]
  };
});

const revenueChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Revenue ($)'
      }
    }
  }
};

const chart2Options = computed(() => {
  const dataVals = likesSummary.value.map(item => item.like_count);
  const maxVal = dataVals.length > 0 ? Math.max(...dataVals) : 0;
  const suggestedMax = maxVal > 0 ? Math.ceil(maxVal * 1.2) : 10;
  
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Airlines',
          font: {
            weight: 'bold',
            size: 13
          }
        },
        ticks: {
          maxRotation: 25,
          minRotation: 25
        }
      },
      y: {
        beginAtZero: true,
        suggestedMax: suggestedMax,
        title: {
          display: true,
          text: 'Likes',
          font: {
            weight: 'bold',
            size: 13
          }
        },
        ticks: {
          precision: 0
        }
      }
    }
  };
});

const datalabelsPlugin = {
  id: 'datalabels',
  afterDatasetsDraw(chart) {
    const { ctx, data } = chart;
    ctx.save();
    ctx.font = 'bold 12px sans-serif';
    ctx.fillStyle = '#0f172a';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    
    const meta = chart.getDatasetMeta(0);
    if (meta && meta.data && data.datasets && data.datasets[0] && data.datasets[0].data) {
      meta.data.forEach((bar, index) => {
        const value = data.datasets[0].data[index];
        if (value !== undefined) {
          ctx.fillText(value, bar.x, bar.y - 5);
        }
      });
    }
    ctx.restore();
  }
};

const glowPlugin = {
  id: 'glow',
  beforeDatasetsDraw(chart) {
    const { ctx, data } = chart;
    const meta = chart.getDatasetMeta(0);
    if (!meta || !meta.data || !data.datasets || !data.datasets[0]) return;
    
    const dataVals = data.datasets[0].data;
    if (!dataVals || dataVals.length === 0) return;
    
    const maxVal = Math.max(...dataVals);
    if (maxVal === 0) return;
    
    meta.data.forEach((bar, index) => {
      if (dataVals[index] === maxVal) {
        ctx.save();
        ctx.shadowColor = '#FFD700'; // Golden glow
        ctx.shadowBlur = 20;
        ctx.fillStyle = data.datasets[0].backgroundColor[index] || '#0194F3';
        ctx.fillRect(bar.x - bar.width / 2, bar.y, bar.width, bar.base - bar.y);
        ctx.restore();
      }
    });
  }
};

const stats = ref({ total_revenue: 0, active_flights: 0, total_bookings: 0, avg_booking_value: 0 });
const weeklyRevenue = ref([]);

const fetchWeeklyRevenue = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/analytics/revenue-weekly');
    if (!response.ok) throw new Error('Failed to fetch weekly revenue');
    weeklyRevenue.value = await response.json();
  } catch (error) {
    console.error("Failed to load live weekly revenue:", error);
  }
};

const fetchDashboardStats = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/analytics/dashboard-stats');
    if (!response.ok) throw new Error('Failed to fetch dashboard stats');
    stats.value = await response.json();
  } catch (error) {
    console.error("Failed to load live dashboard metrics:", error);
  }
};

const adminFlights = ref([]);

const fetchAdminFlights = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/flights');
    if (!response.ok) throw new Error('Failed to fetch flights');
    const freshData = await response.json();
    
    adminFlights.value = freshData.map(fresh => {
      const existing = adminFlights.value.find(f => f.id === fresh.id);
      // Prioritize existing modified status if backend status is null/undefined/'ON TIME'
      let finalStatus = fresh.status;
      if (!finalStatus && existing && existing.status) {
        finalStatus = existing.status;
      } else if (existing && existing.status && existing.status !== 'ON TIME' && (!fresh.status || fresh.status === 'ON TIME')) {
        finalStatus = existing.status;
      }
      return {
        ...fresh,
        status: finalStatus || 'ON TIME'
      };
    });
  } catch (error) {
    console.error("Failed to load live admin flights:", error);
  }
};




const handleFlightUpdated = async () => {
  await fetchAdminFlights();
  await fetchDashboardStats();
};

const adminBookings = ref([]);
const bookingCurrentPage = ref(1);
const bookingItemsPerPage = 10;
const showBookingModal = ref(false);
const selectedBooking = ref(null);

const openBookingModal = (booking) => {
  selectedBooking.value = booking;
  showBookingModal.value = true;
};

const closeBookingModal = () => {
  showBookingModal.value = false;
  selectedBooking.value = null;
};

const fetchAllUserBookings = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/bookings/admin_all');
    if (!response.ok) throw new Error('Failed to fetch bookings');
    adminBookings.value = await response.json();
  } catch (error) {
    console.error("Failed to load live system bookings:", error);
  }
};

const paginatedBookings = computed(() => {
  const start = (bookingCurrentPage.value - 1) * bookingItemsPerPage;
  const end = start + bookingItemsPerPage;
  return adminBookings.value.slice(start, end);
});

const bookingTotalPages = computed(() => Math.ceil(adminBookings.value.length / bookingItemsPerPage));

onMounted(async () => {
  fetchAdminFlights();
  fetchAllUserBookings();
  fetchDashboardStats();
  fetchWeeklyRevenue();
  fetchLikesSummary();
  fetchFlightTypePopularity();
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/analytics/admin');
    if (!response.ok) throw new Error('Failed to load analytics');
    analyticsData.value = await response.json();
  } catch (error) {
    console.error('Error fetching analytics:', error);
  }

  // Set up Supabase Realtime subscription for live chart & table updates
  try {
    realtimeChannel = supabase
      .channel('admin-analytics-realtime')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'bookings' },
        () => {
          fetchFlightTypePopularity();
          fetchDashboardStats();
          fetchWeeklyRevenue();
        }
      )
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'flights' },
        () => {
          fetchAdminFlights();
          fetchDashboardStats();
        }
      )
      .subscribe();
  } catch (err) {
    console.error('Realtime subscription error:', err);
  }
});


onUnmounted(() => {
  if (realtimeChannel) {
    supabase.removeChannel(realtimeChannel);
  }
});

</script>

<style scoped>
.admin-view {
  min-height: 100vh;
  background: var(--sky-bg);
  padding-bottom: 3rem;
}

.admin-header {
  background: linear-gradient(135deg, #0194F3 0%, #0178C9 100%);
  color: white;
  padding: 2rem 1rem;
  text-align: center;
}

.admin-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.admin-header .subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
}

.admin-content {
  padding: 3rem 1rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.admin-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #E5E7EB;
  background: white;
  border-radius: 12px 12px 0 0;
  padding: 0 1.5rem;
}

.tab-btn {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #6B7280;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.tab-btn:hover {
  color: #0194F3;
}

.tab-btn.active {
  color: #0194F3;
  border-bottom-color: #0194F3;
}

.admin-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #E5E7EB;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #E5E7EB;
}

.card-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #03121A;
  margin: 0;
}

.btn-add {
  background: linear-gradient(135deg, #FF5E1F 0%, #E54812 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 94, 31, 0.3);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #F2F7FA;
}

.data-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #6B7280;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #E5E7EB;
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid #F0F1F3;
  color: #6B7280;
}

.data-table tr:hover {
  background: #F9FAFB;
}

.booking-id {
  font-weight: 600;
  color: #0194F3;
}

.amount {
  font-weight: 600;
  color: #03121A;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status.Confirmed {
  background: #DBEAFE;
  color: #0194F3;
}

.status.Completed {
  background: #DCFCE7;
  color: #10B981;
}

.status.Pending {
  background: #FEF3C7;
  color: #D97706;
}

.btn-action {
  background: #0194F3;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.btn-action:hover {
  background: #0178C9;
}

.chart-container {
  padding: 2rem;
  background: #F9FAFB;
  border-radius: 12px;
}

.chart-placeholder {
  text-align: center;
  color: #9CA3AF;
}

.chart-placeholder p {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.chart-note {
  font-size: 0.875rem;
  color: #B0BEC5;
  margin-bottom: 2rem;
}

.chart-bars {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 200px;
  gap: 1rem;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.bar {
  width: 100%;
  background: linear-gradient(180deg, #0194F3 0%, #00A4EF 100%);
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(1, 148, 243, 0.2);
}

.bar:hover {
  background: linear-gradient(180deg, #FF5E1F 0%, #E54812 100%);
  box-shadow: 0 6px 16px rgba(255, 94, 31, 0.3);
}

.bar-item span {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

@media (max-width: 768px) {
  .admin-header h1 {
    font-size: 1.75rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .admin-tabs {
    flex-wrap: wrap;
    padding: 0;
  }

  .tab-btn {
    flex: 1;
    padding: 0.75rem;
    font-size: 0.9rem;
  }

  .data-table {
    font-size: 0.85rem;
  }

  .data-table th,
  .data-table td {
    padding: 0.75rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .btn-add {
    width: 100%;
  }
}

.analytics-charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.chart-wrapper {
  background: #F9FAFB;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
}

.chart-wrapper h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1.25rem 0;
  text-align: center;
}

.chart-box {
  position: relative;
  height: 350px;
  width: 100%;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #6B7280;
}

.spinner {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  animation: spin 1.5s linear infinite;
  display: inline-block;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 992px) {
  .analytics-charts-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    width: 100%;
    box-sizing: border-box;
    padding: 0;
    margin: 0;
  }
  
  .chart-wrapper {
    width: 100%;
    box-sizing: border-box;
    padding: 0.75rem 0.25rem;
    margin: 0;
  }

  .chart-box {
    height: 260px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
  }

  .admin-card {
    padding: 1rem 0.75rem;
    width: 100%;
    box-sizing: border-box;
  }
}




.admin-pagination-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}
.adm-page-btn, .adm-nav-btn {
  min-width: 36px;
  height: 36px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  font-weight: 600;
  font-size: 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}
.adm-page-btn:hover, .adm-nav-btn:hover:not(:disabled) {
  border-color: #0194F3;
  color: #0194F3;
  background: #f0f9ff;
}
.adm-page-btn.active {
  background: #0194F3;
  border-color: #0194F3;
  color: #ffffff;
}
.adm-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #f8fafc;
}

.badge.status-confirmed {
  background-color: #e0f2fe;
  color: #0369a1;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}
.action-view-btn {
  background: #e0f2fe;
  color: #0194F3;
  border: 1px solid #bae6fd;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.action-view-btn:hover {
  background: #0194F3;
  color: white;
  border-color: #0194F3;
  box-shadow: 0 4px 10px rgba(1, 148, 243, 0.25);
  transform: translateY(-1px);
}

/* Pagination styles copied from Flights.vue */
.pagination-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.35rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.pagination-btn {
  background-color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #03121A;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px #03121A;
}

.pagination-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 3px 3px 0px #03121A;
  background-color: #f1f5f9;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.page-numbers {
  display: flex;
  gap: 0.35rem;
}

.page-num-btn.active-page {
  background-color: #FF5E1F;
  color: #ffffff;
  box-shadow: inset 1px 1px 3px rgba(0, 0, 0, 0.2);
}

@media (max-width: 480px) {
  .pagination-nav {
    gap: 0.25rem;
  }
  .pagination-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.75rem;
    box-shadow: 1px 1px 0px #03121A;
  }
}

/* Booking Details Modal Styles */
.modal-overlay-booking {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 99999;
  padding: 1rem;
}

.booking-modal-card {
  background: #ffffff;
  border-radius: 20px;
  width: 100%;
  max-width: 650px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
  animation: scaleInBooking 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.15);
}

@keyframes scaleInBooking {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.booking-modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #0194F3 0%, #0178C9 100%);
  color: white;
}

.booking-modal-header .header-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.booking-modal-header .header-icon {
  font-size: 1.8rem;
}

.booking-modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
}

.booking-modal-header .ref-sub {
  margin: 0.2rem 0 0 0;
  font-size: 0.85rem;
  opacity: 0.9;
  font-family: monospace;
  font-weight: bold;
}

.booking-modal-header .modal-close-btn {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.booking-modal-header .modal-close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.booking-modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
  background: #f8fafc;
}

.booking-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.details-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.details-section.span-full {
  grid-column: span 2;
}

.section-title {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.details-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.detail-label {
  color: #64748b;
  font-weight: 500;
}

.detail-val {
  color: #0f172a;
  font-weight: 600;
}

.price-val-highlight {
  color: #FF5E1F;
  font-size: 1.1rem;
  font-weight: 800;
}

.seat-badge {
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  margin-left: 0.25rem;
}

.flight-info-card {
  border-left: 4px solid #0194F3;
}

.flight-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem 1.5rem;
}

.route-span {
  background: #f1f5f9;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 0.8rem;
}

.booking-modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  background: white;
}

.btn-close-red {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.65rem 2rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
  font-size: 0.9rem;
}

.btn-close-red:hover {
  background: #dc2626;
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.35);
  transform: translateY(-1px);
}

.capitalize {
  text-transform: capitalize;
}

.font-bold {
  font-weight: 700;
}

.text-sky {
  color: #0194F3;
}
</style>
