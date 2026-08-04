<template>
  <div class="booking-view">
    <!-- Header -->
    <section v-if="selectedFlight" class="booking-header">
      <div class="container">
        <div class="header-actions">
          <button class="cancel-booking-trigger" @click="showCancelModal = true">❌ Cancel Booking</button>
          <button class="archive-booking-trigger" @click="showArchiveModal = true">📦 Archive your ticket</button>
        </div>
        <h1>Complete Your Booking</h1>
        <p class="subtitle">Confirm your flight details and select your seat</p>
      </div>
    </section>

    <!-- Content -->
    <section v-if="selectedFlight" class="booking-content">
      <div class="container">
        <div class="booking-grid">
          <!-- Flight Summary -->
          <div class="booking-card">
            <h2 class="card-title">Flight Details</h2>
            <div class="flight-summary">
              <div class="summary-row">
                <span class="label">Route:</span>
                <span class="value">{{ origin }} → {{ destination }}</span>
              </div>
              <div class="summary-row">
                <span class="label">Airline:</span>
                <span class="value">{{ airline }}</span>
              </div>
              <div class="summary-row">
                <span class="label">Flight Number:</span>
                <span class="value">{{ flightNumber }}</span>
              </div>
              <div class="summary-row">
                <span class="label">Departure:</span>
                <span class="value">{{ formatTime(departureTime) }} - {{ formatTime(arrivalTime) }}</span>
              </div>
              <div class="summary-row">
                <span class="label">Passengers:</span>
                <span class="value">{{ passengerCount }} {{ passengerCount === 1 ? 'Passenger' : 'Passengers' }}</span>
              </div>
              <div class="summary-divider"></div>
              <div class="summary-row price-row">
                <span class="label">Base Price (per passenger):</span>
                <span class="value">${{ baseFlightPrice.toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <!-- Seating Chart -->
          <div class="booking-card full-width">
            <SeatingChart 
              v-model="selectedSeats" 
              :other-occupied="otherOccupiedSeats" 
              :user-booked="userBookedSeats" 
              :locked-seats="otherUsersLockedSeats"
              :total-seats="selectedFlight?.total_seats || 180"
            />
          </div>


          <!-- Pricing Summary -->
          <div class="booking-card">
            <h2 class="card-title">Price Summary</h2>
            <div class="pricing">
              <div class="pricing-row">
                <span>Base Fare ({{ passengerCount }} {{ passengerCount === 1 ? 'Passenger' : 'Passengers' }})</span>
                <span>${{ (baseFlightPrice * passengerCount).toFixed(2) }}</span>
              </div>
              
              <!-- Itemized Seat Surcharges -->
              <template v-if="selectedSeats.length > 0">
                <div v-if="firstClassCount > 0" class="pricing-row sub-row">
                  <span class="indent-label">↳ First Class Surcharge (x{{ firstClassCount }})</span>
                  <span class="selected">+${{ (firstClassCount * 100).toFixed(2) }}</span>
                </div>
                <div v-if="businessClassCount > 0" class="pricing-row sub-row">
                  <span class="indent-label">↳ Business Class Surcharge (x{{ businessClassCount }})</span>
                  <span class="selected">+${{ (businessClassCount * 50).toFixed(2) }}</span>
                </div>
                <div v-if="economyClassCount > 0" class="pricing-row sub-row">
                  <span class="indent-label">↳ Economy Class Surcharge (x{{ economyClassCount }})</span>
                  <span>+$0.00</span>
                </div>
              </template>
              <div v-else class="pricing-row">
                <span>Seat Selection</span>
                <span>$0.00</span>
              </div>

              <div class="pricing-row">
                <span>Taxes & Fees (10%)</span>
                <span>${{ taxesAndFees.toFixed(2) }}</span>
              </div>

              <!-- Options Surcharges -->
              <div v-if="addInsurance" class="pricing-row">
                <span>Trip Insurance ({{ passengerCount }} pax)</span>
                <span class="selected">+${{ insurancePrice.toFixed(2) }}</span>
              </div>
              <div v-if="addMeal" class="pricing-row">
                <span>Meal Preference ({{ passengerCount }} pax)</span>
                <span class="selected">+${{ mealPrice.toFixed(2) }}</span>
              </div>
              <div v-if="addBaggage" class="pricing-row">
                <span>Extra Baggage ({{ passengerCount }} pax)</span>
                <span class="selected">+${{ baggagePrice.toFixed(2) }}</span>
              </div>

              <div v-if="discountRate > 0" class="loyalty-discount-alert">
                🎉 Loyalty Benefit: As a {{ tierName }}, you get a {{ (discountRate * 100).toFixed(0) }}% discount on this flight!
              </div>

              <div class="pricing-divider"></div>

              <template v-if="discountRate > 0">
                <div class="pricing-row original-price-row">
                  <span>Subtotal Price:</span>
                  <span>${{ originalPrice.toFixed(2) }}</span>
                </div>
                <div class="pricing-row discount-row">
                  <span class="loyalty-label">↳ {{ tierName }} Discount ({{ (discountRate * 100).toFixed(0) }}%):</span>
                  <span class="discount-applied-text">-${{ discountAmount.toFixed(2) }}</span>
                </div>
              </template>

              <div class="pricing-row total">
                <span>Total Price:</span>
                <span class="total-amount">${{ finalPrice.toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <!-- Booking Options -->
          <div class="booking-card">
            <h2 class="card-title">Additional Options</h2>
            <div class="options">
              <label class="option-item">
                <input type="checkbox" v-model="addInsurance" :disabled="passengerCount === 0" />
                <span>Trip Insurance (+$8.99/pax)</span>
              </label>
              <label class="option-item">
                <input type="checkbox" v-model="addMeal" :disabled="passengerCount === 0" />
                <span>Add Meal Preference (+$15.00/pax)</span>
              </label>
              <label class="option-item">
                <input type="checkbox" v-model="addBaggage" :disabled="passengerCount === 0" />
                <span>Extra Baggage (+$25.00/pax)</span>
              </label>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="booking-actions">
            <router-link to="/flights" class="btn-secondary">
              ← Back to Flights
            </router-link>
            <button class="btn-primary" @click="showConfirmModal = true" :disabled="passengerCount === 0">
              Confirm Booking
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Empty Booking State -->
    <div v-else class="empty-booking-state">
      <div class="empty-icon" style="font-size: 3rem; margin-bottom: 1rem;">✈️</div>
      <h2>Please make your booking</h2>
      <p>You haven't selected any flight passes yet. Head back to the flights directory to choose your trip!</p>
      <router-link to="/flights" class="btn-primary" style="display: inline-block; margin-top: 1.5rem; text-decoration: none;">Go to Flights</router-link>
    </div>

    <!-- Modal 1: Confirmation Box -->
    <div v-if="showConfirmModal" class="modal-overlay">
      <div class="modal-dialog">
        <h3 class="modal-header">Confirm your booking</h3>
        <p class="modal-body">Are you sure you want to confirm your booking for {{ passengerCount }} seat(s)?</p>
        <div class="modal-actions">
          <button @click="showConfirmModal = false" class="btn-modal-cancel">Cancel</button>
          <button @click="submitBookingToDatabase" class="btn-modal-confirm">Confirm</button>
        </div>
      </div>
    </div>

    <!-- Modal 2: Success Box -->
    <div v-if="showSuccessModal" class="modal-overlay">
      <div class="modal-dialog success-dialog">
        <div class="success-icon">✓</div>
        <h3 class="modal-header">Your ticket has been booked successfully</h3>
        <div class="modal-actions centered">
          <button @click="handleSuccessOk" class="btn-modal-confirm">OK</button>
        </div>
      </div>
    </div>

    <!-- Cancel Confirmation Modal -->
    <div v-if="showCancelModal" class="modal-overlay">
      <div class="glow-modal-box">
        <h3>Cancel & Delete Booking?</h3>
        <p>Are you sure you want to delete this pending booking? This cannot be undone.</p>
        <div class="modal-actions">
          <button class="modal-btn quit-btn" @click="deleteAndQuitBooking">Delete Booking</button>
          <button class="modal-btn continue-glow-btn" @click="showCancelModal = false">Continue</button>
        </div>
      </div>
    </div>

    <!-- Archive Confirmation Modal -->
    <div v-if="showArchiveModal" class="modal-overlay">
      <div class="glow-modal-box">
        <h3>Archive Booking?</h3>
        <p>Would you like to temporarily archive your booking so you can explore other options? You can resume it later from Your Tickets section.</p>
        <div class="modal-actions">
          <button class="modal-btn continue-glow-btn" @click="archiveBooking">Archive</button>
          <button class="modal-btn quit-btn" @click="showArchiveModal = false">Continue Booking</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import SeatingChart from '../components/booking/SeatingChart.vue';
import { supabase } from '@/supabase';
import apiClient from '../utils/apiClient.js';

const showConfirmModal = ref(false);
const showSuccessModal = ref(false);

const router = useRouter();
const route = useRoute();

const selectedSeats = ref([]);
const otherUsersSeatsMap = ref({});
const otherUsersLockedSeats = computed(() => {
  return Object.values(otherUsersSeatsMap.value).flat();
});
let seatSyncChannel = null;

const storedUser = JSON.parse(localStorage.getItem('user') || 'null');
const currentUser = {
  id: storedUser ? (storedUser.user_id || storedUser.id || storedUser.user?.id || storedUser.user_metadata?.sub) : null
} || { id: `anon-${Math.random().toString(36).substring(2, 9)}` };
if (!currentUser.id) {
  currentUser.id = `anon-${Math.random().toString(36).substring(2, 9)}`;
}

const addInsurance = ref(false);
const addMeal = ref(false);
const addBaggage = ref(false);

const otherOccupiedSeats = ref([]);
const userBookedSeats = ref([]);

const currentBookingId = ref(route.query.booking_id || null);

const fetchOccupiedSeats = async () => {
  if (!selectedFlight.value) return;
  try {
    const storedUser = JSON.parse(localStorage.getItem('user') || 'null');
    const currentUserId = storedUser ? (storedUser.user_id || storedUser.id || storedUser.user?.id || storedUser.user_metadata?.sub) : null;
    
    let url = `/flights/${selectedFlight.value.id}/occupied_seats`;
    if (currentUserId) {
      url += `?user_id=${currentUserId}`;
    }
    const res = await apiClient.get(url);
    if (res && res.data) {
      otherOccupiedSeats.value = res.data.other_occupied || [];
      userBookedSeats.value = res.data.user_booked || [];
    }
  } catch (error) {
    console.error('Error fetching occupied seats:', error);
  }
};

onMounted(async () => {
  const flightIdFromQuery = route.query.flight_id || route.query.id;
  const bookingIdFromQuery = route.query.booking_id;
  
  if (bookingIdFromQuery) {
    currentBookingId.value = bookingIdFromQuery;
  }
  
  if (!selectedFlight.value && flightIdFromQuery) {
    try {
      const res = await apiClient.get(`/flights/${flightIdFromQuery}`);
      if (res && res.data) {
        const flight = res.data;
        if (flight) {
          selectedFlight.value = {
            id: flight.id,
            airline: flight.airline,
            flightNumber: flight.flight_number || flight.flightNumber,
            origin: flight.origin,
            destination: flight.destination,
            base_price: flight.base_price || flight.price,
            departureTime: flight.departure_time || flight.departureTime,
            arrivalTime: flight.arrival_time || flight.arrivalTime
          };
          localStorage.setItem('selected_flight', JSON.stringify(selectedFlight.value));
        }
      }
    } catch (e) {
      console.error('Error fetching flight details:', e);
    }
  }
  
  await fetchOccupiedSeats();
  
  // Create pending booking if not exists
  if (!currentBookingId.value && selectedFlight.value) {
    const storedUser = JSON.parse(localStorage.getItem('user') || 'null');
    const currentUserId = storedUser ? (storedUser.user_id || storedUser.id || storedUser.user?.id || storedUser.user_metadata?.sub) : null;
    
    try {
      const response = await apiClient.post('/bookings', {
        flight_id: selectedFlight.value.id,
        user_id: currentUserId,
        total_price: baseFlightPrice.value,
        passenger_count: 1
      });
      if (response && response.data && response.data.received_data && response.data.received_data.id) {
        currentBookingId.value = response.data.received_data.id;
        router.replace({
          path: route.path,
          query: {
            ...route.query,
            booking_id: currentBookingId.value
          }
        });
      }
    } catch (error) {
      console.error('Error creating pending booking:', error);
    }
  }

  // Connect to a specific room for this flight ID
  if (flightIdFromQuery && currentUser.id) {
    seatSyncChannel = supabase.channel(`flight-room-${flightIdFromQuery}`, {
      config: { presence: { key: currentUser.id } }
    });

    seatSyncChannel
      // A: Listen for instant click/unclick updates from other users via Broadcast
      .on('broadcast', { event: 'seat-update' }, ({ payload }) => {
        if (payload.user_id !== currentUser.id) {
          if (payload.seats && payload.seats.length > 0) {
            otherUsersSeatsMap.value[payload.user_id] = payload.seats;
          } else {
            delete otherUsersSeatsMap.value[payload.user_id];
          }
        }
      })
      // B: Handle tab closures or sudden disconnects using Presence leave event
      .on('presence', { event: 'leave' }, ({ leftPresences }) => {
        leftPresences.forEach((presence) => {
          const disconnectedUserId = presence.presenceKey;
          if (disconnectedUserId && disconnectedUserId !== currentUser.id) {
            delete otherUsersSeatsMap.value[disconnectedUserId];
          }
        });
      })
      // C: Listen for completed bookings to move these seats to occupied permanently
      .on('broadcast', { event: 'booking-complete' }, ({ payload }) => {
        if (payload.user_id !== currentUser.id) {
          if (payload.booked_seats) {
            payload.booked_seats.forEach(seat => {
              if (!otherOccupiedSeats.value.includes(seat)) {
                otherOccupiedSeats.value.push(seat);
              }
            });
          }
          delete otherUsersSeatsMap.value[payload.user_id];
        }
      })
      // D: Listen for sync requests from newly connected clients
      .on('broadcast', { event: 'request-sync' }, ({ payload }) => {
        if (payload.requester_id !== currentUser.id && selectedSeats.value.length > 0) {
          seatSyncChannel.send({
            type: 'broadcast',
            event: 'seat-update',
            payload: { user_id: currentUser.id, seats: selectedSeats.value }
          });
        }
      })

      // E: Handle user join to sync state immediately
      .on('presence', { event: 'join' }, ({ newPresences }) => {
        // When anyone joins, re-broadcast our currently selected seats to ensure they have it
        if (selectedSeats.value.length > 0) {
          seatSyncChannel.send({
            type: 'broadcast',
            event: 'seat-update',
            payload: { user_id: currentUser.id, seats: selectedSeats.value }
          });
        }
      })
      .on('presence', { event: 'sync' }, () => {
        // Re-announce state on complete sync
        if (selectedSeats.value.length > 0) {
          seatSyncChannel.send({
            type: 'broadcast',
            event: 'seat-update',
            payload: { user_id: currentUser.id, seats: selectedSeats.value }
          });
        }
      })

      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          // Broadcast current initial selections immediately upon joining
          seatSyncChannel.send({
            type: 'broadcast',
            event: 'seat-update',
            payload: { user_id: currentUser.id, seats: selectedSeats.value }
          });
          // Request other users to broadcast their active seats for sync
          seatSyncChannel.send({
            type: 'broadcast',
            event: 'request-sync',
            payload: { requester_id: currentUser.id }
          });
          // Also track presence for disconnect detection
          await seatSyncChannel.track({ user_id: currentUser.id, online_at: new Date().toISOString() });
        }
      });


  }
});

const getInitialFlight = () => {
  const flightIdFromQuery = route.query.flight_id || route.query.id;
  if (!flightIdFromQuery) {
    localStorage.removeItem('selected_flight');
    return null;
  }
  const stored = localStorage.getItem('selected_flight');
  if (stored) {
    try {
      const flightObj = JSON.parse(stored);
      if (flightObj && flightObj.id == flightIdFromQuery) {
        return flightObj;
      }
    } catch (e) {}
  }
  return null;
};

// Watch for route query changes to handle empty state and reset details correctly
watch(() => route.fullPath, async () => {
  const flightIdFromQuery = route.query.flight_id || route.query.id;
  const bookingIdFromQuery = route.query.booking_id;
  
  currentBookingId.value = bookingIdFromQuery || null;
  
  if (!flightIdFromQuery) {
    selectedFlight.value = null;
    selectedSeats.value = [];
    localStorage.removeItem('selected_flight');
  } else {
    const stored = localStorage.getItem('selected_flight');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        if (parsed.id == flightIdFromQuery) {
          selectedFlight.value = parsed;
        } else {
          selectedFlight.value = null;
        }
      } catch (e) {
        selectedFlight.value = null;
      }
    }
    
    if (!selectedFlight.value) {
      try {
        const res = await apiClient.get(`/flights/${flightIdFromQuery}`);
        if (res && res.data) {
          const flight = res.data;
          selectedFlight.value = {
            id: flight.id,
            airline: flight.airline,
            flightNumber: flight.flight_number || flight.flightNumber,
            origin: flight.origin,
            destination: flight.destination,
            base_price: flight.base_price || flight.price,
            departureTime: flight.departure_time || flight.departureTime,
            arrivalTime: flight.arrival_time || flight.arrivalTime
          };
          localStorage.setItem('selected_flight', JSON.stringify(selectedFlight.value));
        }
      } catch (e) {
        console.error(e);
      }
    }
  }
  
  await fetchOccupiedSeats();
});

const selectedFlight = ref(getInitialFlight());
const showCancelModal = ref(false);
const showArchiveModal = ref(false);

const archiveBooking = () => {
  localStorage.removeItem('selected_flight');
  selectedFlight.value = null;
  selectedSeats.value = [];
  currentBookingId.value = null;
  showArchiveModal.value = false;
  router.push('/booking');
};

const deleteAndQuitBooking = async () => {
  if (currentBookingId.value) {
    try {
      await apiClient.delete(`/bookings/${currentBookingId.value}`);
    } catch (error) {
      console.error('Error deleting pending booking:', error);
    }
  }
  localStorage.removeItem('selected_flight');
  selectedFlight.value = null;
  selectedSeats.value = [];
  currentBookingId.value = null;
  showCancelModal.value = false;
  
  if (route.query.from_pending === 'true') {
    router.push('/your-tickets');
  } else {
    router.push('/');
  }
};

const flightId = computed(() => selectedFlight.value?.id || null);
const airline = computed(() => selectedFlight.value?.airline || '');
const flightNumber = computed(() => selectedFlight.value?.flightNumber || '');
const origin = computed(() => selectedFlight.value?.origin || '');
const destination = computed(() => selectedFlight.value?.destination || '');
const baseFlightPrice = computed(() => parseFloat(selectedFlight.value?.base_price || 0));
const departureTime = computed(() => selectedFlight.value?.departureTime || '');
const arrivalTime = computed(() => selectedFlight.value?.arrivalTime || '');

const formatTime = (timeStr) => {
  if (!timeStr) return '';
  if (timeStr.includes('T')) {
    const timePart = timeStr.split('T')[1];
    if (timePart) {
      const parts = timePart.split(':');
      if (parts.length >= 2) {
        return formatTimeStr(`${parts[0]}:${parts[1]}`);
      }
    }
  }
  return formatTimeStr(timeStr);
};

const formatTimeStr = (timeStr) => {
  const parts = timeStr.split(':');
  if (parts.length >= 2) {
    let hour = parseInt(parts[0], 10);
    const minute = parts[1];
    const ampm = hour >= 12 ? 'PM' : 'AM';
    hour = hour % 12;
    hour = hour ? hour : 12;
    const strHour = hour < 10 ? `0${hour}` : hour;
    return `${strHour}:${minute} ${ampm}`;
  }
  return timeStr;
};

const passengerCount = computed(() => selectedSeats.value.length);

const firstClassCount = computed(() => {
  return selectedSeats.value.filter(seatId => parseInt(seatId.split('-')[0]) <= 2).length;
});

const businessClassCount = computed(() => {
  return selectedSeats.value.filter(seatId => {
    const row = parseInt(seatId.split('-')[0]);
    return row >= 3 && row <= 6;
  }).length;
});

const economyClassCount = computed(() => {
  return selectedSeats.value.filter(seatId => parseInt(seatId.split('-')[0]) >= 7).length;
});

const seatPremiumTotal = computed(() => {
  return (firstClassCount.value * 100) + (businessClassCount.value * 50);
});

const insurancePrice = computed(() => addInsurance.value ? 8.99 * passengerCount.value : 0);
const mealPrice = computed(() => addMeal.value ? 15.00 * passengerCount.value : 0);
const baggagePrice = computed(() => addBaggage.value ? 25.00 * passengerCount.value : 0);

const taxesAndFees = computed(() => (baseFlightPrice.value * passengerCount.value) * 0.1);

const user = ref(JSON.parse(localStorage.getItem('user')) || null);

const loyaltyTier = computed(() => {
  const points = user.value?.points || 0;
  if (points >= 5000) {
    return { name: "Gold Priority", discountRate: 0.10 };
  } else if (points >= 2000) {
    return { name: "Silver Priority", discountRate: 0.05 };
  } else if (points >= 1000) {
    return { name: "Bronze Priority", discountRate: 0.03 };
  } else {
    return { name: "Explorer", discountRate: 0.00 };
  }
});

const discountRate = computed(() => loyaltyTier.value.discountRate);
const tierName = computed(() => loyaltyTier.value.name);

const originalPrice = computed(() => {
  if (passengerCount.value === 0) return 0;
  const baseTotal = baseFlightPrice.value * passengerCount.value;
  return baseTotal + seatPremiumTotal.value + insurancePrice.value + mealPrice.value + baggagePrice.value + taxesAndFees.value;
});

const discountAmount = computed(() => {
  return originalPrice.value * discountRate.value;
});

const finalPrice = computed(() => {
  return originalPrice.value - discountAmount.value;
});

const totalPrice = finalPrice; // maintain compatibility if referenced elsewhere

// selectedFlight ref is defined above

const submitBookingToDatabase = async () => {
  if (passengerCount.value === 0) {
    alert('Please select at least one seat before completing your booking.');
    return;
  }
  
  const storedUser = JSON.parse(localStorage.getItem('user') || 'null');
  const currentUser = {
    id: storedUser ? (storedUser.user_id || storedUser.id || storedUser.user?.id || storedUser.user_metadata?.sub) : null
  };

  try {
    const response = currentBookingId.value 
      ? await apiClient.put(`/bookings/${currentBookingId.value}/complete`, {
          flight_id: selectedFlight.value.id,
          user_id: currentUser.id,
          total_price: totalPrice.value,
          passenger_count: passengerCount.value || 1,
          selected_seats: selectedSeats.value,
          seat_class: selectedSeats.value.length > 0 ? (firstClassCount.value > 0 ? 'First' : businessClassCount.value > 0 ? 'Business' : 'Economy') : 'Economy'
        })
      : await apiClient.post('/bookings', {
          flight_id: selectedFlight.value.id,
          user_id: currentUser.id,
          total_price: totalPrice.value,
          passenger_count: passengerCount.value || 1,
          selected_seats: selectedSeats.value,
          seat_class: selectedSeats.value.length > 0 ? (firstClassCount.value > 0 ? 'First' : businessClassCount.value > 0 ? 'Business' : 'Economy') : 'Economy'
        });

    const data = response.data;
    if (data && data.status === 'error') {
      throw new Error(data.message || 'Backend failed to complete booking');
    }
    if (data && data.new_total_points !== undefined && storedUser) {
      storedUser.points = data.new_total_points;
      localStorage.setItem('user', JSON.stringify(storedUser));
    }

    if (seatSyncChannel) {
      seatSyncChannel.send({
        type: 'broadcast',
        event: 'booking-complete',
        payload: {
          user_id: currentUser.id,
          booked_seats: selectedSeats.value
        }
      });
    }

    showConfirmModal.value = false;
    showSuccessModal.value = true;
  } catch (error) {
    console.error('Error submitting booking:', error);
    alert('Failed to submit booking. Please try again.');
  }
};

const handleSuccessOk = () => {
  localStorage.removeItem('selected_flight');
  selectedFlight.value = null;
  selectedSeats.value = [];
  currentBookingId.value = null;
  showSuccessModal.value = false;
  router.push('/your-tickets');
};

watch(selectedSeats, (newSeats) => {
  if (seatSyncChannel) {
    seatSyncChannel.send({
      type: 'broadcast',
      event: 'seat-update',
      payload: { user_id: currentUser.id, seats: newSeats }
    });
  }
}, { deep: true });

onUnmounted(() => {
  if (seatSyncChannel) {
    supabase.removeChannel(seatSyncChannel);
  }
});
</script>

<style scoped lang="scss">
.booking-view {
  min-height: 100vh;
  background: var(--sky-bg);
  padding-bottom: 3rem;
}

.booking-header {
  background: linear-gradient(135deg, #0194F3 0%, #0178C9 100%);
  color: white;
  padding: 2rem 1rem;
  text-align: center;
}

.booking-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.booking-header .subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
}

.booking-content {
  padding: 3rem 1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
  box-sizing: border-box;
}

.booking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.booking-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #E5E7EB;
  max-width: 100%;
  box-sizing: border-box;
}

.booking-card.full-width {
  grid-column: 1 / -1;
  max-width: 100%;
  box-sizing: border-box;
}


.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #03121A;
  margin: 0 0 1.5rem 0;
  padding-bottom: 1rem;
  border-bottom: 2px solid #E5E7EB;
}

.flight-summary {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-row .label {
  color: #6B7280;
  font-weight: 500;
}

.summary-row .value {
  color: #03121A;
  font-weight: 600;
}

.summary-divider {
  height: 1px;
  background: #E5E7EB;
  margin: 0.5rem 0;
}

.summary-row.price-row {
  font-size: 1.1rem;
}

.pricing {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pricing-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #F0F1F3;
}

.pricing-row.sub-row {
  border-bottom: 1px dashed #F0F1F3;
  padding: 0.5rem 0;
}

.indent-label {
  padding-left: 1rem;
  font-size: 0.85rem;
  color: #6B7280;
}

.pricing-row .selected {
  color: #10B981;
  font-weight: 600;
}

.pricing-divider {
  height: 2px;
  background: #E5E7EB;
  margin: 0.5rem 0;
}

.pricing-row.total {
  border-bottom: none;
  font-size: 1.1rem;
  font-weight: 700;
  color: #03121A;
}

.total-amount {
  color: #FF5E1F;
  font-size: 1.5rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #F2F7FA;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-item:hover {
  background: #E0F2FE;
}

.option-item input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #0194F3;
}

.option-item span {
  color: #6B7280;
  font-weight: 500;
}

.booking-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  text-align: center;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-secondary {
  background: white;
  color: #0194F3;
  border: 2px solid #0194F3;
}

.btn-secondary:hover {
  background: #F2F7FA;
  transform: translateY(-2px);
}

.btn-primary {
  background: linear-gradient(135deg, #FF5E1F 0%, #E54812 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(255, 94, 31, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 94, 31, 0.4);
}

.btn-primary:disabled {
  background: #D1D5DB;
  cursor: not-allowed;
  box-shadow: none;
}

@media (max-width: 768px) {
  .booking-header h1 {
    font-size: 1.75rem;
  }

  .booking-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .booking-actions {
    flex-direction: column;
  }

  .btn-secondary,
  .btn-primary {
    width: 100%;
  }
}

.loyalty-discount-alert {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.discount-row {
  color: #166534;
  font-weight: 500;
}

.discount-applied-text {
  color: #166534;
  font-weight: 600;
}

.loyalty-label {
  color: #166534;
}

.original-price-row {
  color: #6b7280;
  text-decoration: line-through;
  font-size: 0.9rem;
}

.modal-overlay {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog {
  position: relative;
  z-index: 9999;
  pointer-events: auto;
  background: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
}

.success-dialog {
  text-align: center;
}

.success-icon {
  width: 60px;
  height: 60px;
  background: #e6f4ea;
  color: #137333;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  margin: 0 auto 1.5rem auto;
  font-weight: bold;
}

.modal-header {
  margin: 0 0 1rem 0;
  color: #0f172a;
  font-size: 1.25rem;
  font-weight: 700;
}

.modal-body {
  color: #64748b;
  font-size: 0.95rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
}

.modal-actions.centered {
  justify-content: center;
}

.btn-modal-cancel {
  background: none;
  border: none;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 16px;
  font-size: 0.95rem;
}

.btn-modal-cancel:hover {
  color: #334155;
}

.btn-modal-confirm {
  background: #0194F3;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.95rem;
  box-shadow: 0 0 12px rgba(0, 145, 255, 0.45);
  transition: all 0.3s ease-in-out;
}

.btn-modal-confirm:hover {
  background-color: #0082f0;
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 145, 255, 0.75);
}

.btn-modal-confirm:active {
  transform: translateY(0);
  box-shadow: 0 0 8px rgba(0, 145, 255, 0.5);
}

.empty-booking-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border: 2px solid #03121A;
  border-radius: 20px;
  box-shadow: 4px 4px 0px #03121A;
  margin: 4rem auto;
  max-width: 600px;
  transition: all 0.3s ease;
}

.empty-booking-state:hover {
  transform: translateY(-6px);
  box-shadow: 8px 8px 0px #03121A;
}
.header-actions {
  display: flex;
  gap: 12px;
  float: right;
  margin: 1rem;
}
.cancel-booking-trigger {
  background: #ef4444;
  color: #ffffff;
  border: none;
  padding: 8px 16px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
}
.archive-booking-trigger {
  background: #4b5563;
  color: #ffffff;
  border: none;
  padding: 8px 16px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  &:hover {
    background: #374151;
  }
}
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex; justify-content: center; align-items: center;
  z-index: 9999;
}
.glow-modal-box {
  background: #1e293b;
  color: #ffffff;
  padding: 2rem;
  border-radius: 16px;
  width: 400px;
  text-align: center;
  border: 1px solid rgba(255,255,255,0.1);
}
.modal-actions {
  display: flex; justify-content: space-around; margin-top: 1.5rem; gap: 12px;
}
.modal-btn {
  padding: 10px 24px; font-weight: 700; border-radius: 8px; border: none; cursor: pointer; flex: 1;
}
.quit-btn { background: #475569; color: #cbd5e1; }
.continue-glow-btn {
  background: #0194F3;
  color: #ffffff;
  box-shadow: 0 0 15px #0194F3, 0 0 30px #0194F3; /* High-tech premium glow feature */
  animation: glow-pulse 1.8s infinite;
}
@keyframes glow-pulse {
  0% { box-shadow: 0 0 10px #0194F3; }
  50% { box-shadow: 0 0 25px #0194F3, 0 0 40px #0194F3; }
  100% { box-shadow: 0 0 10px #0194F3; }
}
@media (max-width: 768px) {
  .header-actions {
    float: none;
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0 0 1rem 0;
    gap: 8px;
  }
  
  .cancel-booking-trigger, .archive-booking-trigger {
    width: 100%;
    text-align: center;
  }

  .booking-header h1 {
    font-size: 1.8rem;
  }

  .booking-content {
    padding: 1.5rem 0.5rem;
  }

  .booking-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .booking-card {
    padding: 1.25rem;
  }

  .booking-card.full-width {
    grid-column: span 1;
    width: 100%;
    box-sizing: border-box;
  }
}
</style>
