<template>
  <div class="flight-history-container">
    <header class="page-header">
      <div class="header-icon">📜</div>
      <div class="header-info">
        <h1>My Flight History</h1>
        <p class="subtitle">View your past journeys and active checkout operations</p>
      </div>
    </header>

    <!-- Statistics Section -->
    <div v-if="!loading && activeTicketsList.length > 0" class="history-stats-dashboard">
      <div class="stat-card">
        <div class="stat-icon">✈️</div>
        <div class="stat-details">
          <span class="stat-label">Total Flights Booked</span>
          <span class="stat-value">{{ totalFlights }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-details">
          <span class="stat-label">Total Money Spent</span>
          <span class="stat-value">${{ totalSpent }}</span>
        </div>
      </div>
    </div>

    <main class="page-content">
      <div v-if="loading" class="loading-state">
        <p>Loading flight history...</p>
      </div>
      <div v-else-if="activeTicketsList.length === 0" class="empty-state">
        <p>No active tickets found. Explore and book your next trip now!</p>
      </div>
      
      <!-- Horizontal Tickets List -->
      <div v-else class="tickets-list">
        <div 
          v-for="booking in activeTicketsList" 
          :key="booking.id" 
          class="premium-horizontal-ticket"
        >
          <!-- Blurred background image -->
          <img 
            :src="getDestinationImage(booking)" 
            class="ticket-bg-blur" 
            alt="Destination Backdrop"
          />
          
          <!-- Ticket Content Layer -->
          <div class="ticket-content-layer">
            <!-- Left Section: Departure Details -->
            <div class="ticket-col ticket-col-left">
              <span class="city-name">{{ booking.flights?.origin_city || booking.flights?.origin }}</span>
              <span class="airport-code">{{ booking.flights?.origin }}</span>
              <span class="time-text">{{ formatTime(booking.flights?.departure_time) }}</span>
              <span class="date-text">{{ formatDate(booking.flights?.departure_time) }}</span>
            </div>
            
            <!-- Center Section: Flight Connection Status Ribbon -->
            <div class="ticket-col ticket-col-middle">
              <div class="connection-line">
                <span class="duration-badge">{{ getDurationString(booking.flights?.departure_time, booking.flights?.arrival_time) }}</span>
                <div class="plane-line">
                  <span class="plane-icon">✈️</span>
                </div>
                <span class="flight-type-badge">{{ booking.seat_class || 'Economy' }}</span>
              </div>
            </div>
            
            <!-- Right Section: Destination Details & Return path details -->
            <div class="ticket-col ticket-col-right">
              <span class="city-name">{{ booking.flights?.destination_city || booking.flights?.destination }}</span>
              <span class="airport-code">{{ booking.flights?.destination }}</span>
              <span class="time-text">{{ formatTime(booking.flights?.arrival_time) }}</span>
              
              <!-- Return path badge if round-trip -->
              <div v-if="booking.trip_type === 'round-trip'" class="return-leg-badge">
                <span class="badge-label">🔄 Return Leg</span>
                <span class="badge-val">{{ formatDate(booking.return_date) }}</span>
              </div>
            </div>
            
            <!-- Edge Section: Booking Ref and Price -->
            <div class="ticket-stub-segment">
              <div class="stub-divider"></div>
              <div class="stub-details">
                <div class="ref-container">
                  <span class="ref-label">BOOKING REF</span>
                  <span class="ref-value">{{ booking.booking_reference || ('TRV-' + booking.id) }}</span>
                </div>
                <div class="price-container">
                  <span class="price-label">PRICE PAID</span>
                  <span class="price-value">${{ booking.total_price || booking.flights?.base_price }}</span>
                </div>
                <div class="status-container">
                  <span class="status-badge complete-badge">✓ Complete</span>
                </div>
              </div>
            </div>
            
            <!-- Flight Interaction Footer: Heart and Comment -->
            <div class="flight-interaction-controls">
              <button 
                class="like-button-heart" 
                :class="{ 'is-liked': booking.liked }" 
                @click.stop="toggleFlightLike(booking)"
              >
                {{ booking.liked ? '❤️' : '🤍' }}
              </button>
              <button class="flight-comments-button" @click.stop="openCommentsModal(booking)">
                <span>💬 {{ flightCommentCounts[booking.flights?.id] || 0 }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Facebook Style Comments Modal -->
    <div v-if="showCommentsModal" class="comments-modal-overlay" @click="closeCommentsModal">
      <div class="facebook-comments-modal" @click.stop>
        <header class="modal-header">
          <h2>Comments for {{ currentBookingForComments.flights?.airline || 'Flight' }}</h2>
          <button class="close-modal-btn" @click="closeCommentsModal">✕</button>
        </header>
        
        <!-- Scrollable comments list -->
        <div class="comments-list-scroll">
          <div v-if="loadingComments" class="comments-loading">
            <p>Loading comments...</p>
          </div>
          <div v-else-if="airlineCommentsList.length === 0" class="no-comments-yet">
            <p>No comments yet. Be the first to share your experience!</p>
          </div>
          <div v-else class="facebook-comments-wrapper">
            <div v-for="c in airlineCommentsList" :key="c.booking_id + c.created_at" class="fb-comment-item">
              <!-- Avatar -->
              <div class="fb-comment-avatar-container">
                <img v-if="c.avatar_url" :src="c.avatar_url" class="fb-comment-avatar" alt="Avatar" />
                <div v-else class="fb-avatar-placeholder">{{ getUserInitials(c.username) }}</div>
              </div>
              
              <!-- Bubble content -->
              <div class="fb-comment-bubble-wrapper">
                <div class="fb-comment-bubble">
                  <span class="fb-comment-user">{{ c.username }}</span>
                  <p class="fb-comment-text">{{ c.comment }}</p>
                </div>
                <!-- Time since -->
                <span class="fb-comment-time">{{ formatRelativeTime(c.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Write Comment Section -->
        <div class="comments-write-footer">
          <div class="write-avatar-container">
            <img v-if="currentUserAvatar" :src="currentUserAvatar" class="write-avatar" alt="My Avatar" />
            <div v-else class="fb-avatar-placeholder">{{ getUserInitials(currentUsername) }}</div>
          </div>
          <form @submit.prevent="submitFlightComment" class="write-comment-form">
            <input 
              type="text" 
              v-model="newCommentText" 
              placeholder="Write a comment..." 
              class="write-comment-input" 
              required
            />
            <button type="submit" class="send-comment-btn" :disabled="submittingComment">
              {{ submittingComment ? '...' : 'Post' }}
            </button>
          </form>
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

// Comments modal states
const showCommentsModal = ref(false);
const currentBookingForComments = ref(null);
const airlineCommentsList = ref([]);
const newCommentText = ref('');
const loadingComments = ref(false);
const submittingComment = ref(false);
const flightCommentCounts = ref({});

const currentUser = ref(JSON.parse(localStorage.getItem('user')) || null);
const currentUsername = computed(() => currentUser.value?.username || 'Explorer');
const currentUserAvatar = computed(() => currentUser.value?.avatar_url || '');

const displayedBookings = computed(() => {
  return activeTab.value === 'tickets' ? activeTicketsList.value : pendingBookingsList.value;
});

const totalFlights = computed(() => activeTicketsList.value.length);
const totalSpent = computed(() => {
  const sum = activeTicketsList.value.reduce((acc, booking) => {
    const price = booking.total_price || booking.flights?.base_price || 0;
    return acc + parseFloat(price);
  }, 0);
  return sum.toFixed(2);
});

const formatTime = (dateTimeStr) => {
  if (!dateTimeStr) return '';
  const date = new Date(dateTimeStr);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
};

const formatDate = (dateTimeStr) => {
  if (!dateTimeStr) return '';
  const date = new Date(dateTimeStr);
  return date.toLocaleDateString('en-US', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' });
};

const getDurationString = (dep, arr) => {
  if (!dep || !arr) return 'N/A';
  const diffMs = new Date(arr) - new Date(dep);
  if (diffMs <= 0) return 'N/A';
  const diffMins = Math.floor(diffMs / 60000);
  const hrs = Math.floor(diffMins / 60);
  const mins = diffMins % 60;
  return `${hrs}h ${mins}m`;
};

const getDestinationImage = (booking) => {
  const dbUrl = booking.flights?.airports?.image_url;
  const code = (booking.flights?.destination || '').toUpperCase();
  const mapping = {
    'HAN': 'https://images.unsplash.com/photo-1509030450996-dd1a26dda07a?auto=format&fit=crop&w=1280&q=80',
    'SGN': 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?auto=format&fit=crop&w=1280&q=80',
    'DAD': 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?auto=format&fit=crop&w=1280&q=80',
    'CXR': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1280&q=80',
    'PQC': 'https://images.unsplash.com/photo-1602524813043-91c6f7e00a51?auto=format&fit=crop&w=1280&q=80',
    'VKG': 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?auto=format&fit=crop&w=1280&q=80',
    'VDO': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1280&q=80',
    'DLI': 'https://dalatnews.net/wp-content/uploads/2025/01/hinh-anh-san-bay-lien-khuong-tai-da-lat.webp',
    'HUI': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?auto=format&fit=crop&w=1280&q=80',
    'UIH': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1280&q=80',
    'VCS': 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?auto=format&fit=crop&w=1280&q=80',
    'VII': 'https://images.unsplash.com/photo-1490349368154-73de9c9bc37c?auto=format&fit=crop&w=1280&q=80',
    'HPH': 'https://images.unsplash.com/photo-1528360983277-13d401cdc186?auto=format&fit=crop&w=1280&q=80',
    'BMV': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1280&q=80',
    'VDH': 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1280&q=80',
    'SIN': 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1280&q=80'
  };
  // Always prefer the local mapping (reliable open sources).
  // Fall back to the database URL only if it's not a blocked Google encrypted-tbn link.
  const isBlocked = (url) => !url || url.includes('encrypted-tbn') || url.includes('gstatic.com');
  return mapping[code]
    || (!isBlocked(dbUrl) ? dbUrl : null)
    || 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1280&q=80';
};

const resumeCheckout = (ticket) => {
  router.push(`/booking?flight_id=${ticket.flight_id}&booking_id=${ticket.id}&from_pending=true`);
};

const toggleFlightLike = async (booking) => {
  const newStatus = !booking.liked;
  booking.liked = newStatus;
  
  try {
    const airlineName = booking.flights?.airline || "Unknown Airline";
    await apiClient.post(`/bookings/${booking.id}/like`, {
      liked: newStatus,
      airline: airlineName
    });
  } catch (error) {
    console.error("Error toggling like:", error);
    booking.liked = !newStatus;
  }
};

const getUserInitials = (name) => {
  if (!name) return 'EX';
  const parts = name.trim().split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

const formatRelativeTime = (dateStr) => {
  if (!dateStr) return 'Just now';
  
  // SQLite timestamps are UTC e.g. "2026-07-13 04:20:00"
  let normalizedStr = dateStr;
  if (!dateStr.includes('T') && dateStr.includes(' ')) {
    normalizedStr = dateStr.replace(' ', 'T') + 'Z';
  }
  
  const commentTime = new Date(normalizedStr);
  const currentTime = new Date();
  
  const diffMs = currentTime - commentTime;
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  const diffWeeks = Math.floor(diffDays / 7);
  const diffMonths = Math.floor(diffDays / 30);
  
  if (diffSecs < 60) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  if (diffWeeks < 4) return `${diffWeeks}w ago`;
  return `${diffMonths}mo ago`;
};

const openCommentsModal = async (booking) => {
  currentBookingForComments.value = booking;
  showCommentsModal.value = true;
  loadingComments.value = true;
  newCommentText.value = '';
  
  try {
    const flightId = booking.flights?.id;
    const res = await apiClient.get(`/bookings/comments/list`, { params: { flight_id: flightId } });
    if (res.data && res.data.status === 'success') {
      airlineCommentsList.value = res.data.comments || [];
    }
  } catch (error) {
    console.error("Error fetching comments:", error);
  } finally {
    loadingComments.value = false;
  }
};

const closeCommentsModal = () => {
  showCommentsModal.value = false;
  currentBookingForComments.value = null;
  airlineCommentsList.value = [];
};

const submitFlightComment = async () => {
  if (!newCommentText.value.trim() || !currentBookingForComments.value) return;
  
  submittingComment.value = true;
  const booking = currentBookingForComments.value;
  const commentText = newCommentText.value;
  const airlineName = booking.flights?.airline || "Unknown Airline";
  const flightId = booking.flights?.id;
  
  try {
    await apiClient.post(`/bookings/${booking.id}/comment`, {
      comment: commentText,
      airline: airlineName
    });
    
    // Update local ticket comment state
    booking.comment = commentText;
    newCommentText.value = '';
    
    // Update comment counts locally
    if (flightId) {
      if (flightCommentCounts.value[flightId] === undefined) {
        flightCommentCounts.value[flightId] = 0;
      }
      flightCommentCounts.value[flightId] += 1;
    }
    
    // Refresh comments list
    await openCommentsModal(booking);
  } catch (error) {
    console.error("Error submitting comment:", error);
  } finally {
    submittingComment.value = false;
  }
};

onMounted(async () => {
  loading.value = true;
  try {
    const resData = await apiClient.get('/bookings/my_summary');
    activeTicketsList.value = resData.data.past || [];
    pendingBookingsList.value = resData.data.pending || [];
    flightCommentCounts.value = resData.data.comment_counts || {};
  } catch (error) {
    console.error('Error fetching flight history:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped lang="scss">
.flight-history-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
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
}

.tab-badge {
  background-color: #e2e8f0;
  color: #475569;
  font-size: 0.8rem;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-weight: 700;
}

.nav-tab.active .tab-badge {
  background-color: #0194F3;
  color: white;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 3rem;
  background: #f8fafc;
  border-radius: 12px;
  color: #64748b;
  border: 1px dashed #e2e8f0;
}

.tickets-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.premium-horizontal-ticket {
  position: relative;
  display: flex;
  background: #ffffff;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  padding: 1.2rem 2rem;
  min-height: 245px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e2e8f0;
}

.premium-horizontal-ticket::before,
.premium-horizontal-ticket::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 18px;
  height: 18px;
  background-color: #f8fafc;
  border-radius: 50%;
  transform: translateY(-50%);
  z-index: 10;
  border: 1px solid #e2e8f0;
}
.premium-horizontal-ticket::before { left: -10px; }
.premium-horizontal-ticket::after { right: -10px; }

.ticket-bg-blur {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0.12;
  filter: blur(2px);
  z-index: 1;
  pointer-events: none;
}

.ticket-content-layer {
  position: relative;
  z-index: 2;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.ticket-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.ticket-col-left {
  flex: 2;
  align-items: flex-start;
  padding-top: 55px;
}

.ticket-col-middle {
  flex: 3;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
}

.ticket-col-right {
  flex: 2;
  align-items: flex-end;
  text-align: right;
}

.city-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
}

.airport-code {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  background-color: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  margin-top: 2px;
  display: inline-block;
}

.time-text {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0194F3;
  margin-top: 6px;
}

.date-text {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 4px;
  font-weight: 500;
}

.connection-line {
  position: relative;
  width: 100%;
  max-width: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.connection-line::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  border-top: 2px dashed #cbd5e1;
  z-index: 1;
}

.duration-badge {
  background: #f1f5f9;
  color: #475569;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 600;
  z-index: 2;
  margin-bottom: 8px;
}

.plane-line {
  z-index: 2;
  background: #ffffff;
  padding: 0 8px;
}

.plane-icon {
  font-size: 1rem;
  color: #0194F3;
  display: inline-block;
  transform: rotate(90deg);
}

.flight-type-badge {
  font-size: 0.75rem;
  color: #0194F3;
  background: rgba(1, 148, 243, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 700;
  margin-top: 8px;
  z-index: 2;
}

.return-leg-badge {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 2px 8px;
  border-radius: 4px;
}

.return-leg-badge .badge-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #16a34a;
}

.return-leg-badge .badge-val {
  font-size: 0.75rem;
  font-weight: 600;
  color: #14532d;
}

.ticket-stub-segment {
  display: flex;
  align-items: center;
  flex: 3.5;
  padding-left: 24px;
}

.stub-divider {
  width: 1px;
  height: 150px;
  border-left: 2px dotted #e2e8f0;
  margin-right: 24px;
}

.stub-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.ref-container, .price-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.status-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.ref-label, .price-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.ref-value {
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  color: #0f172a;
  font-size: 0.95rem;
}

.price-value {
  font-size: 1.15rem;
  font-weight: 800;
  color: #ff5e1f;
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
}

.complete-badge {
  background-color: #f0fdf4;
  color: #16a34a;
}

.pending-badge {
  background-color: #fffbeb;
  color: #d97706;
}

.pending-card-interactive {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.pending-card-interactive:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(1, 148, 243, 0.15);
}

.flight-interaction-controls {
  position: absolute;
  top: 12px;
  left: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 15;
}

.like-button-heart {
  background: transparent !important;
  border: none !important;
  font-size: 1.25rem;
  cursor: pointer;
  transition: transform 0.2s ease;
  padding: 0 !important;
  line-height: 1;
  box-shadow: none !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  &:hover {
    transform: scale(1.2);
  }
}

.flight-comments-button {
  background-color: #F2F7FA !important;
  color: #0194F3 !important;
  border: 1.5px solid #03121A !important;
  padding: 4px 10px !important;
  padding-bottom: 4px !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  box-shadow: 2px 2px 0px #03121A !important;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: transform 0.1s ease, box-shadow 0.1s ease;

  &:hover {
    transform: translate(-1px, -1px);
    box-shadow: 3px 3px 0px #03121A !important;
  }
  &:active {
    transform: translate(0, 0);
    box-shadow: 1px 1px 0px #03121A !important;
  }
}

@keyframes pop {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.4);
  }
  100% {
    transform: scale(1);
  }
}

.history-stats-dashboard {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  
  .stat-card {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.25rem 1.75rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    }

    .stat-icon {
      font-size: 2.25rem;
      background: rgba(1, 148, 243, 0.08);
      width: 60px;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      color: #0194F3;
    }

    .stat-details {
      display: flex;
      flex-direction: column;
      
      .stat-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      
      .stat-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0.25rem;
      }
    }
  }
}

/* Facebook Style Comments Modal Overlay */
.comments-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

.facebook-comments-modal {
  background-color: #ffffff;
  border-radius: 12px;
  width: 100%;
  max-width: 580px;
  max-height: 80vh;
  box-shadow: 0 12px 28px 0 rgba(0, 0, 0, 0.2), 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e5e5;

  h2 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #050505;
    margin: 0;
  }

  .close-modal-btn {
    background: none;
    border: none;
    font-size: 1.25rem;
    color: #606770;
    cursor: pointer;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease;

    &:hover {
      background-color: #f2f2f2;
      color: #050505;
    }
  }
}

.comments-list-scroll {
  flex: 1;
  padding: 16px 20px;
  overflow-y: auto;
  background-color: #ffffff;
  min-height: 250px;
}

.comments-loading, .no-comments-yet {
  text-align: center;
  color: #606770;
  padding: 40px 0;
  font-size: 0.95rem;
}

.facebook-comments-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.fb-comment-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.fb-comment-avatar-container {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #0194F3;
  flex-shrink: 0;
}

.fb-comment-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.fb-avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.8rem;
}

.fb-comment-bubble-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.fb-comment-bubble {
  background-color: #f0f2f5;
  border-radius: 18px;
  padding: 8px 12px;
  display: inline-block;
  max-width: 440px;
  text-align: left;
}

.fb-comment-user {
  font-size: 0.85rem;
  font-weight: 700;
  color: #050505;
  display: block;
  margin-bottom: 2px;
}

.fb-comment-text {
  font-size: 0.93rem;
  color: #050505;
  margin: 0;
  line-height: 1.35;
  word-break: break-word;
}

.fb-comment-time {
  font-size: 0.75rem;
  color: #606770;
  margin-top: 4px;
  margin-left: 8px;
}

.comments-write-footer {
  padding: 12px 20px 20px 20px;
  border-top: 1px solid #e5e5e5;
  display: flex;
  gap: 12px;
  align-items: center;
  background-color: #ffffff;
}

.write-avatar-container {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #0194F3;
  flex-shrink: 0;
}

.write-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.write-comment-form {
  flex: 1;
  display: flex;
  align-items: center;
  background-color: #f0f2f5;
  border-radius: 20px;
  padding: 6px 12px;
  border: 1px solid transparent;
  transition: border-color 0.2s ease, background-color 0.2s ease;

  &:focus-within {
    border-color: #0194F3;
    background-color: #ffffff;
    box-shadow: 0 0 0 2px rgba(1, 148, 243, 0.1);
  }
}

.write-comment-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.93rem;
  color: #050505;
  padding: 2px 4px;
}

.send-comment-btn {
  background: none;
  border: none;
  color: #0194F3;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 2px 6px;
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.8;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

</style>
