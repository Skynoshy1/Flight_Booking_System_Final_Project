<template>
  <div class="flight-history-container">
    <header class="page-header">
      <div class="header-icon">🎫</div>
      <div class="header-info">
        <h1>Your Tickets</h1>
        <p class="subtitle">View your booked tickets and active checkout operations</p>
      </div>
    </header>

    <!-- Tab Toggle Navigation UI -->
    <div class="history-tabs-nav">
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'tickets' }" 
        @click="activeTab = 'tickets'"
      >
        Your Tickets 
        <span class="tab-badge ticket-badge">{{ activeTicketsList.length }}</span>
      </button>
      <button 
        class="nav-tab" 
        :class="{ active: activeTab === 'pending' }" 
        @click="activeTab = 'pending'"
      >
        On-Pending Bookings 
        <span class="tab-badge pending-badge">{{ pendingBookingsList.length }}</span>
      </button>
    </div>

    <main class="page-content">
      <div v-if="loading" class="loading-state">
        <p>Loading your tickets...</p>
      </div>
      <div v-else-if="displayedBookings.length === 0" class="empty-state">
        <p v-if="activeTab === 'tickets'">No active tickets found. Explore and book your next trip now!</p>
        <p v-else>No pending bookings found.</p>
      </div>
      <div v-else class="tickets-grid">
        <div 
          v-for="booking in displayedBookings" 
          :key="booking.id" 
          class="flight-premium-card"
          :class="{ 'pending-card-interactive': activeTab === 'pending' }"
          :style="{ backgroundImage: `url(${getDestinationImage(booking.flights?.destination)})` }"
          @click="activeTab === 'pending' ? resumeCheckout(booking) : null"
        >
          <!-- Overlay Mask -->
          <div class="overlay-mask"></div>

          <!-- Ticket Top: Airline Header & Badge -->
          <div class="ticket-header">
            <div class="brand-info">
              <div v-if="getAirlineLogo(booking.flights?.airline)" class="airline-logo-bubble">
                <img :src="getAirlineLogo(booking.flights?.airline)" :alt="booking.flights?.airline" class="airline-brand-logo" />
              </div>
              <div v-else class="logo-wrapper" :class="getAirlineBrandClass(booking.flights?.airline)">
                {{ getAirlineShortName(booking.flights?.airline) }}
              </div>
              <div class="airline-text">
                <h3 v-if="!getAirlineLogo(booking.flights?.airline)" class="airline-name">{{ booking.flights?.airline }}</h3>
                <p class="flight-number">Flight {{ booking.flights?.flight_number || booking.flights?.flightNumber }}</p>
                <p class="flight-date">{{ booking.flights?.departure_date }}</p>
              </div>
            </div>
            <span class="trip-type-badge">ONE-WAY</span>
          </div>

          <!-- Ticket Middle: Travel Metrics & Details -->
          <div class="ticket-body">
            <div class="timeline-glass-wrapper">
              <div class="time-section-vertical">
                <div class="timeline-point">
                  <span class="time-label">{{ formatTime(booking.flights?.departure_time || booking.flights?.departureTime) }}</span>
                  <span class="airport-label">{{ booking.flights?.origin }}</span>
                </div>

                <div class="duration-connector">
                  <span class="plane-icon">✈️</span>
                  <div class="connector-line"></div>
                  <span class="duration-label">{{ booking.flights?.duration || '1h 45m' }}</span>
                </div>

                <div class="timeline-point">
                  <span class="time-label">{{ formatTime(booking.flights?.arrival_time || booking.flights?.arrivalTime) }}</span>
                  <span class="airport-label">{{ booking.flights?.destination }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Tear Line Separator Stub -->
          <div class="ticket-tear-line"></div>

          <!-- Ticket Bottom: Price Stub & Action -->
          <div class="ticket-bottom">
            <div class="price-stub">
              <p class="price-lbl">Fare Price</p>
              <div class="price-tag-premium">
                <span class="currency">$</span>
                <span class="amount">{{ booking.total_price || booking.flights?.base_price }}</span>
              </div>
            </div>
            
            <div class="actions-wrapper">
              <template v-if="activeTab === 'tickets'">
                <span class="status-capsule upcoming">Upcoming</span>
              </template>
              <template v-else-if="activeTab === 'pending'">
                <span class="status-capsule pending-status">Pending Payment</span>
              </template>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Rating Modal -->
    <div v-if="showModal" class="modal-overlay-rating" @click.self="showModal = false">
      <div class="modal-content">
        <h2>Rate Flight {{ selectedTicket?.flights?.flight_number }}</h2>
        <p class="modal-subtitle">How was your journey from {{ selectedTicket?.flights?.origin }} to {{ selectedTicket?.flights?.destination }}?</p>
        
        <div class="stars-rating">
          <span 
            v-for="star in 5" 
            :key="star" 
            class="star" 
            :class="{ active: star <= rating }"
            @click="rating = star"
          >
            ★
          </span>
        </div>

        <div class="feedback-input">
          <label for="comment-text">Tell us more about your experience:</label>
          <textarea 
            id="comment-text" 
            v-model="comment" 
            placeholder="Share details of your flight..."
            rows="4"
          ></textarea>
        </div>

        <div class="modal-actions">
          <button class="btn-cancel" @click="showModal = false">Cancel</button>
          <button class="btn-submit" :disabled="rating === 0" @click="submitReview">Submit Review</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../utils/apiClient.js';

const router = useRouter();
const activeTab = ref('tickets');
const activeTicketsList = ref([]);
const pendingBookingsList = ref([]);
const loading = ref(true);

const displayedBookings = computed(() => {
  return activeTab.value === 'tickets' ? activeTicketsList.value : pendingBookingsList.value;
});

const formatTime = (timeStr) => {
  if (!timeStr) return '';
  if (timeStr.includes('T')) {
    const timePart = timeStr.split('T')[1];
    if (timePart) {
      const parts = timePart.split(':');
      if (parts.length >= 2) {
        return `${parts[0]}:${parts[1]}`;
      }
    }
  }
  return timeStr;
};

const showModal = ref(false);
const selectedTicket = ref(null);
const rating = ref(0);
const comment = ref('');

const submitReview = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        booking_id: selectedTicket.value.id,
        rating: rating.value,
        comment: comment.value
      })
    });
    if (!response.ok) throw new Error('Failed to submit review');
    alert('Review submitted successfully!');
    showModal.value = false;
  } catch (error) {
    console.error('Error submitting review:', error);
    alert('Failed to submit review. Please try again.');
  }
};

const getDestinationImage = (destinationCode) => {
  const mapping = {
    'HAN': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQ6YnKJ8kE02X_Pe_xOgBqbftsMLu8AqnEwNOH0MEjwqJxlZd-Ji8iO0aZ5euEh7AZ4W2THGGQYKb_oc70',
    'SGN': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRC_4LXSay4j_y4tIhlbSZGMilHMWOIxm4WVWA8pjva39aqKHNQZlNbCN39jJj0dv9AZuR0Z_S118pKNmM',
    'DAD': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSh5nWfheh4fBjHHzi4uqVyMXmKoLMRIcq6iUYtGZnAPw8otTMsNeZhc5VLbmPr',
    'CXR': 'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTuFSX8HC_fstNxaAVDcGNJJa31LuCBtGZUfcVr2hSJwdlQIBmc4UjyXhB6NzVJdtyL4xFEbxgzcTWPp4Y',
    'PQC': 'https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSMsyHK-GkpgBgDehQgvLpvM22PExi8KGXZRfjGnWscHiwEpdO2jbKTaodXSZ7z7PBnUxjva0pdWS3GzRs',
    'VKG': 'https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQS1D1poweQFdQbOIIwrLkgLUcoGBlWoxn-wbImDu3p9PC8IQeRc0dVaktQ9DwEukAZtJefTJgZUQkiqFg',
    'VDO': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcT9Ny5f31bHazSwuui89eCCsRRzQrOv1wFsSRIz29uq4tzaY7iEjnP5Rns6z-zrf7FmGC3P5-sO22QCf9U',
    'DLI': 'https://dalatnews.net/wp-content/uploads/2025/01/hinh-anh-san-bay-lien-khuong-tai-da-lat.webp',
    'HUI': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQUHiL4QMkbvKrxAi1r33WNyEk_Jk5U5Cf0fhtqNGgRElQOA4Lpxv4_A_aK12TUecddOmMz6mraNNk1PhY',
    'UIH': 'https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQ4aySdJb1ZhIgAc0pHfkLI8gyV_glYP4ljhtG0pY7vbqZ9pEUN5jjichodSKKTr5uENwQpR2kLmcUhdv8',
    'VCS': 'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTmuRE8TqDIlUgobysZPOuXjfKEkdrBM3ad3Shzp2qW1bxlcHz2Sy-KSaa8oQBvuvbiFjN7dzSzBN5NM4k',
    'VII': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRUYCKRNT6NoZ1qBwm4SG_QLuXu4uCsH-h6lnYhhzdwnokVIkqoLHJlzeW_uyzB-F5HAVkCO37NiK8tfg4',
    'HPH': 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTxETxFDsZvluEHinY7gAsohU_VfBex1qNF3iY-LbxgXqw_y95DB5UERaFdJTR-w3H18EhV6Mt8EsbvZDs',
    'SIN': 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTNloQM7FiWpGrN0vBX8xWbDOCjpDp_a1vrCtCX7wAEXeIpM9GvxSulVpvmVh1AIn1IZG9UjILdCBT4b7o'
  };
  return mapping[destinationCode] || 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=600&q=80';
};

const getAirlineLogo = (airlineName) => {
  const name = (airlineName || '').toLowerCase();
  if (name.includes('vietjet')) return 'https://1000logos.net/wp-content/uploads/2021/04/VietJet-Air-logo.png';
  if (name.includes('bamboo')) return 'https://tse3.mm.bing.net/th/id/OIP.bQcgyMuhw4v-aOX3In-BPAHaHk?rs=1&pid=ImgDetMain&o=7&rm=3';
  if (name.includes('vietravel')) return 'https://tse2.mm.bing.net/th/id/OIP.xA4mFIV99UhSmZKiSP0ufgHaHa?rs=1&pid=ImgDetMain&o=7&rm=3';
  if (name.includes('vietnam')) return 'https://tse4.mm.bing.net/th/id/OIP.6sDY5mRcgNsLb7BhLQdEpAHaFi?rs=1&pid=ImgDetMain&o=7&rm=3';
  return '';
};

const getAirlineBrandClass = (airline) => {
  const name = (airline || '').toLowerCase();
  if (name.includes('vietnam')) return 'brand-vietnam';
  if (name.includes('vietjet')) return 'brand-vietjet';
  if (name.includes('bamboo')) return 'brand-bamboo';
  return 'brand-default';
};

const getAirlineShortName = (airline) => {
  const name = (airline || '').toLowerCase();
  if (name.includes('vietnam')) return 'VN';
  if (name.includes('vietjet')) return 'VJ';
  if (name.includes('bamboo')) return 'BA';
  if (name.includes('vietravel')) return 'VA';
  return 'FL';
};

const resumeCheckout = (ticket) => {
  router.push(`/booking?flight_id=${ticket.flight_id}&booking_id=${ticket.id}&from_pending=true`);
};

onMounted(async () => {
  loading.value = true;
  try {
    const resData = await apiClient.get('/bookings/my_summary');
    activeTicketsList.value = resData.data.completed || [];
    pendingBookingsList.value = resData.data.pending || [];
  } catch (error) {
    console.error('Error fetching tickets:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.flight-history-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.history-tabs-nav {
  display: flex;
  gap: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
}

.nav-tab {
  background: none;
  border: none;
  font-size: 1.1rem;
  font-weight: 600;
  color: #64748b;
  padding: 0.5rem 1rem;
  cursor: pointer;
  position: relative;
  transition: color 0.2s ease, transform 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-tab:hover {
  color: #0f172a;
}

.nav-tab.active {
  color: #0194F3;
}

.nav-tab.active::after {
  content: '';
  position: absolute;
  bottom: -0.625rem;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #0194F3;
  border-radius: 2px;
  transform: scaleX(1);
  transition: transform 0.2s ease;
}

.tab-badge {
  background-color: #e2e8f0;
  color: #475569;
  font-size: 0.8rem;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-weight: 700;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-tab.active .tab-badge {
  background-color: #0194F3;
  color: white;
}

.flight-date {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 0.25rem;
  font-weight: 500;
}

.status-capsule.upcoming {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.header-icon {
  font-size: 3rem;
  background: #e0f2fe;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.header-info h1 {
  font-size: 2rem;
  color: #0f172a;
  margin: 0;
}

.subtitle {
  color: #64748b;
  margin-top: 0.25rem;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  background: #f8fafc;
  border-radius: 12px;
  color: #64748b;
  border: 1px dashed #e2e8f0;
}

.tickets-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  justify-content: space-between;
}

@media (max-width: 992px) {
  .tickets-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .tickets-grid {
    grid-template-columns: 1fr;
  }
}

/* Vertical Ticket Card Panel */
.flight-premium-card {
  position: relative;
  background-size: cover;
  background-position: center;
  border-radius: 16px;
  overflow: visible;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.flight-premium-card::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 24px;
  background-color: #f8fafc; /* Matches background */
  border-radius: 50%;
  z-index: 2;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.overlay-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.85) 100%);
  border-radius: 16px;
  z-index: 1;
}

/* Header Section */
.ticket-header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.brand-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.airline-logo-bubble {
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 10px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  height: 44px;
}

.airline-brand-logo {
  max-height: 35px;
  max-width: 110px;
  object-fit: contain;
}

.logo-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.1rem;
  color: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.brand-vietnam {
  background: linear-gradient(135deg, #003057 0%, #005a9c 100%);
  border: 1px solid #005a9c;
}

.brand-vietjet {
  background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
}

.brand-bamboo {
  background: linear-gradient(135deg, #10b981 0%, #064e3b 100%);
}

.brand-default {
  background: #4b5563;
}

.airline-text {
  display: flex;
  flex-direction: column;
}

.airline-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.flight-number {
  font-size: 1.2rem;
  color: #cbd5e1;
  margin: 2px 0 0 0;
  font-weight: 600;
}

.trip-type-badge {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  padding: 6px 14px;
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  backdrop-filter: blur(4px);
}

/* Middle Section */
.ticket-body {
  position: relative;
  z-index: 2;
  margin-top: 1rem;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.timeline-glass-wrapper {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  padding: 12px 18px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.time-section-vertical {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.timeline-point {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.time-label {
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
}

.airport-label {
  font-size: 1.1rem;
  color: #cbd5e1;
  font-weight: 600;
  margin-top: 2px;
  letter-spacing: 0.5px;
}

.duration-connector {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.connector-line {
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.3);
  margin: 6px 0;
}

.plane-icon {
  font-size: 0.8rem;
  color: #ffffff;
}

.duration-label {
  font-size: 1.15rem;
  color: #cbd5e1;
  font-weight: 600;
}

/* Tear Line */
.ticket-tear-line {
  position: relative;
  height: 1px;
  border-top: 2px dashed rgba(255, 255, 255, 0.25);
  margin: 0.75rem 0;
  z-index: 2;
  width: 100%;
}

/* Bottom Section */
.ticket-bottom {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-bottom: 4px;
}

.price-stub {
  display: flex;
  flex-direction: column;
}

.price-lbl {
  font-size: 1rem;
  color: #cbd5e1;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.price-tag-premium {
  color: #FF5E1F;
  font-weight: 800;
  display: flex;
  align-items: baseline;
  gap: 1px;
}

.price-tag-premium .currency {
  font-size: 1.5rem;
  font-weight: 700;
}

.price-tag-premium .amount {
  font-size: 2.4rem;
}

.actions-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-capsule {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 700;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
}

.pending-badge {
  background-color: #ff5e1f !important;
  color: white !important;
  box-shadow: 0 0 8px rgba(255, 94, 31, 0.4);
}

.pending-card-interactive {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.pending-card-interactive:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(255, 94, 31, 0.3);
}

.status-capsule.pending-status {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}
</style>
