<template>
  <div class="home-view">
    <!-- Hero Section with Search -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Find & Book Flights</h1>
          <p class="hero-subtitle">Search millions of flights at the best prices</p>
        </div>
        <FlightSearch :key="searchKey" @search="handleSearch" />
      </div>
    </section>

    <!-- Results Section -->
    <section class="results-section">
      <div class="container">
        <!-- Filters & Sort -->
        <div class="filter-bar">
          <div class="filter-group">
            <span class="filter-label">Sort by:</span>
            <div class="input-wrapper custom-dropdown" :class="{ 'custom-dropdown-open': sortDropdownOpen }">
              <div @click="toggleSortDropdown" class="filter-select custom-select-trigger">
                {{ currentSortLabel }}
              </div>
              
              <transition name="dropdown-slide">
                <div v-show="sortDropdownOpen" class="custom-options-container">
                  <div 
                    class="custom-option"
                    :class="{ selected: sortBy === 'price-asc' }"
                    @click.stop="selectSort('price-asc')"
                  >
                    <span class="option-name">Price: Low to High</span>
                  </div>
                  <div 
                    class="custom-option"
                    :class="{ selected: sortBy === 'price-desc' }"
                    @click.stop="selectSort('price-desc')"
                  >
                    <span class="option-name">Price: High to Low</span>
                  </div>
                  <div 
                    class="custom-option"
                    :class="{ selected: sortBy === 'duration' }"
                    @click.stop="selectSort('duration')"
                  >
                    <span class="option-name">Duration</span>
                  </div>
                  <div 
                    class="custom-option"
                    :class="{ selected: sortBy === 'departure' }"
                    @click.stop="selectSort('departure')"
                  >
                    <span class="option-name">Departure Time</span>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <div class="filter-group">
            <span class="filter-label">Max Price: ${{ maxPrice }}</span>
            <input 
              type="range" 
              v-model="maxPrice" 
              min="0" 
              max="500" 
              class="filter-slider"
            />
          </div>

          <div class="filter-group">
            <label class="checkbox">
              <input type="checkbox" v-model="directFlightsOnly" />
              <span>Direct flights only</span>
            </label>
          </div>
        </div>

        <!-- Results Count -->
        <div class="results-header">
          <p class="results-count">
            <span class="count">{{ filteredFlights.length }}</span>
            flight{{ filteredFlights.length !== 1 ? 's' : '' }} found
          </p>
        </div>

        <!-- Flight List (matches found) -->
        <div v-if="filteredFlights.length > 0">
          <div class="flights-list">
            <FlightCard
              v-for="flight in paginatedFlights"
              :key="flight.id"
              :flight="flight"
              @select="handleSelectFlight"
            />
          </div>

          <!-- Pagination Controls (News page design) -->
          <nav v-if="totalPages > 1" class="pagination-nav" aria-label="Flights Pagination">
            <button
              class="pagination-btn"
              :disabled="currentPage === 1"
              @click="changePage(1)"
              aria-label="First page"
            >
              « First
            </button>
            <button
              class="pagination-btn"
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
              aria-label="Previous page"
            >
              ‹ Prev
            </button>

            <div class="page-numbers">
              <button
                v-for="page in displayedPages"
                :key="page"
                class="pagination-btn page-num-btn"
                :class="{ 'active-page': currentPage === page }"
                @click="changePage(page)"
              >
                {{ page }}
              </button>
            </div>

            <button
              class="pagination-btn"
              :disabled="currentPage === totalPages"
              @click="changePage(currentPage + 1)"
              aria-label="Next page"
            >
              Next ›
            </button>
            <button
              class="pagination-btn"
              :disabled="currentPage === totalPages"
              @click="changePage(totalPages)"
              aria-label="Last page"
            >
              Last »
            </button>
          </nav>

          <!-- Results Summary -->
          <div v-if="filteredFlights.length > 0" class="results-summary">
            Showing {{ resultsStart }} - {{ resultsEnd }} of {{ filteredFlights.length }} flights
          </div>

          <!-- Other Flights Badge Section (only when active search was made) -->
          <div v-if="hasActiveSearch && limitedFallbackFlights.length > 0" class="other-flights-badge-section">
            <div class="other-flights-badge-header">
              <span class="other-flights-badge">Other flights you might be interested in</span>
              <p class="other-flights-subtitle">Explore more available routes and discover great deals</p>
            </div>
          </div>

          <div v-if="hasActiveSearch && limitedFallbackFlights.length > 0" class="flights-list fallback-list">
            <FlightCard
              v-for="flight in limitedFallbackFlights"
              :key="flight.id"
              :flight="flight"
              @select="handleSelectFlight"
            />
          </div>
        </div>

        <!-- No Results / Fallback List -->
        <div v-else class="no-results-fallback">
          <div class="no-results-message">
            <div class="no-results-icon">✈️</div>
            <h3>No exact matches found for this specific route/date.</h3>
            <p>Here are all other available flights instead:</p>
          </div>
          
          <div class="flights-list fallback-list">
            <FlightCard
              v-for="flight in fallbackFlights"
              :key="flight.id"
              :flight="flight"
              @select="handleSelectFlight"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Auth Warning Modal -->
    <div v-if="showAuthModal" class="auth-gate-overlay">
      <div class="auth-warning-box">
        <div class="auth-alert-icon">🔒</div>
        <h3>Access Denied</h3>
        <p class="auth-message-text">Please sign in to book your ticket</p>
        <div class="auth-action-row">
          <button class="auth-btn back-gray-btn" @click="showAuthModal = false">Back</button>
          <button class="auth-btn signin-orange-btn" @click="router.push('/signin'); showAuthModal = false;">Sign In</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import FlightSearch from '../components/booking/FlightSearch.vue';
import FlightCard from '../components/booking/FlightCard.vue';

const router = useRouter();
const sortBy = ref('price-asc');
const maxPrice = ref(500);
const directFlightsOnly = ref(false);
const selectedFlight = ref(null);
const showAuthModal = ref(false);
const flights = ref([]);
const currentSearchCriteria = ref(null);
const searchKey = ref(0);
const currentTimeTrigger = ref(Date.now());

const sortDropdownOpen = ref(false);
const currentSortLabel = computed(() => {
  switch (sortBy.value) {
    case 'price-asc': return 'Price: Low to High';
    case 'price-desc': return 'Price: High to Low';
    case 'duration': return 'Duration';
    case 'departure': return 'Departure Time';
    default: return 'Price: Low to High';
  }
});
const toggleSortDropdown = (e) => {
  e.stopPropagation();
  sortDropdownOpen.value = !sortDropdownOpen.value;
};
const selectSort = (value) => {
  sortBy.value = value;
  sortDropdownOpen.value = false;
};
const closeSortDropdown = () => {
  sortDropdownOpen.value = false;
};

const currentPage = ref(1);
const itemsPerPage = ref(9);

const paginatedFlights = computed(() => {
  return filteredFlights.value.slice((currentPage.value - 1) * itemsPerPage.value, currentPage.value * itemsPerPage.value);
});

const totalPages = computed(() => {
  return Math.ceil(filteredFlights.value.length / itemsPerPage.value);
});

const displayedPages = computed(() => {
  const total = totalPages.value; // Total page count integer
  const current = currentPage.value; // Active page reference
  
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }
  
  let start = current - 2;
  let end = current + 2;
  
  if (start < 1) {
    start = 1;
    end = 5;
  } else if (end > total) {
    end = total;
    start = total - 4;
  }
  
  return Array.from({ length: (end - start) + 1 }, (_, i) => start + i);
});

watch([sortBy, maxPrice, directFlightsOnly, currentSearchCriteria], () => {
  currentPage.value = 1;
});

// Page summary index counts (matches NewsView design)
const resultsStart = computed(() => {
  if (filteredFlights.value.length === 0) return 0;
  return (currentPage.value - 1) * itemsPerPage.value + 1;
});

const resultsEnd = computed(() => {
  const potentialEnd = currentPage.value * itemsPerPage.value;
  return potentialEnd > filteredFlights.value.length ? filteredFlights.value.length : potentialEnd;
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const clearSearch = () => {
  currentSearchCriteria.value = null;
  searchKey.value += 1;
};

// Mock flight data
const mockFlights = [
  {
    id: 1,
    airline: 'Vietnam Airlines',
    flightNumber: 'VN101',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '08:30',
    arrivalTime: '10:15',
    duration: '1h 45m',
    stops: 0,
    price: 129,
    availableSeats: 12,
    features: ['Free Meal', 'Extra Baggage', 'Seat Selection']
  },
  {
    id: 2,
    airline: 'Vietjet Air',
    flightNumber: 'BL106',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '09:00',
    arrivalTime: '10:45',
    duration: '1h 45m',
    stops: 0,
    price: 89,
    availableSeats: 8,
    features: ['Budget Friendly', 'Fast Boarding']
  },
  {
    id: 3,
    airline: 'Bamboo Airways',
    flightNumber: 'BA223',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '10:30',
    arrivalTime: '12:30',
    duration: '2h',
    stops: 1,
    price: 99,
    availableSeats: 15,
    features: ['Comfort Seat', 'Free Drinks']
  },
  {
    id: 4,
    airline: 'Vietnam Airlines',
    flightNumber: 'VN315',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '12:45',
    arrivalTime: '14:30',
    duration: '1h 45m',
    stops: 0,
    price: 139,
    availableSeats: 5,
    features: ['Business Class', 'Premium Meal', 'Priority Boarding']
  },
  {
    id: 5,
    airline: 'Vietjet Air',
    flightNumber: 'BL212',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '14:00',
    arrivalTime: '15:45',
    duration: '1h 45m',
    stops: 0,
    price: 85,
    availableSeats: 20,
    features: ['Budget Friendly', 'Quick Check-in']
  },
  {
    id: 6,
    airline: 'Bamboo Airways',
    flightNumber: 'BA445',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '16:00',
    arrivalTime: '17:45',
    duration: '1h 45m',
    stops: 0,
    price: 109,
    availableSeats: 18,
    features: ['Free Checked Bag', 'Seat Selection']
  },
  {
    id: 7,
    airline: 'Vietnam Airlines',
    flightNumber: 'VN512',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '17:30',
    arrivalTime: '19:15',
    duration: '1h 45m',
    stops: 0,
    price: 149,
    availableSeats: 3,
    features: ['First Class', 'Lounge Access', 'Premium Meal']
  },
  {
    id: 8,
    airline: 'Vietjet Air',
    flightNumber: 'BL408',
    origin: 'SGN',
    destination: 'HAN',
    departureTime: '18:00',
    arrivalTime: '19:45',
    duration: '1h 45m',
    stops: 0,
    price: 79,
    availableSeats: 25,
    features: ['Evening Flight', 'Budget Friendly']
  }
];

// Computed properties for filtering and sorting
const filteredFlights = computed(() => {
  let result = flights.value.filter(flight => {
    if (String(flight.status || '').toUpperCase() === 'CANCELED' || String(flight.status || '').toUpperCase() === 'CANCELLED') return false;
    if (flight.base_price > maxPrice.value) return false;
    if (directFlightsOnly.value && flight.stops > 0) return false;
    
    // Check if expired (real-time comparison)
    const now = new Date(currentTimeTrigger.value);
    if (flight.departure_time) {
      if (new Date(flight.departure_time) < now) return false;
    } else if (flight.departureDate && flight.departureTime) {
      if (new Date(`${flight.departureDate}T${flight.departureTime}`) < now) return false;
    }
    return true;
  });


  // Apply search criteria if present and not untouched defaults
  if (currentSearchCriteria.value) {
    const { origin, destination, departureDate, flightNumber } = currentSearchCriteria.value;
    const isUntouchedDefault = origin === 'SGN' && destination === 'HAN' && (!departureDate || departureDate === '') && (!flightNumber || flightNumber === '');
    
    if (!isUntouchedDefault) {
      result = result.filter(flight => {
        if (flightNumber && flightNumber !== '') {
          const fn = String(flight.flightNumber || flight.flight_number || '').toLowerCase();
          if (!fn.includes(flightNumber.toLowerCase())) return false;
        }
        if (origin && flight.origin !== origin) return false;
        if (destination && flight.destination !== destination) return false;
        // If departureDate is empty, ignore date filter
        if (departureDate && departureDate !== '' && flight.departureDate && flight.departureDate !== departureDate) return false;
        return true;
      });
    }
  }

  // Sort
  switch (sortBy.value) {
    case 'price-asc':
      result.sort((a, b) => a.base_price - b.base_price);
      break;
    case 'price-desc':
      result.sort((a, b) => b.base_price - a.base_price);
      break;
    case 'duration':
      result.sort((a, b) => {
        const durationA = parseInt(a.duration);
        const durationB = parseInt(b.duration);
        return durationA - durationB;
      });
      break;
    case 'departure':
      result.sort((a, b) => a.departureTime.localeCompare(b.departureTime));
      break;
  }

  return result;
});

const fallbackFlights = computed(() => {
  let result = flights.value.filter(flight => {
    if (String(flight.status || '').toUpperCase() === 'CANCELED' || String(flight.status || '').toUpperCase() === 'CANCELLED') return false;
    if (flight.base_price > maxPrice.value) return false;
    if (directFlightsOnly.value && flight.stops > 0) return false;
    
    // Check if expired (real-time comparison)
    const now = new Date(currentTimeTrigger.value);
    if (flight.departure_time) {
      if (new Date(flight.departure_time) < now) return false;
    } else if (flight.departureDate && flight.departureTime) {
      if (new Date(`${flight.departureDate}T${flight.departureTime}`) < now) return false;
    }
    return true;
  });

  // Sort
  switch (sortBy.value) {
    case 'price-asc':
      result.sort((a, b) => a.base_price - b.base_price);
      break;
    case 'price-desc':
      result.sort((a, b) => b.base_price - a.base_price);
      break;
    case 'duration':
      result.sort((a, b) => {
        const durationA = parseInt(a.duration);
        const durationB = parseInt(b.duration);
        return durationA - durationB;
      });
      break;
    case 'departure':
      result.sort((a, b) => a.departureTime.localeCompare(b.departureTime));
      break;
  }

  return result;
});

// True only when the user has actively submitted a real search (non-default)
const hasActiveSearch = computed(() => {
  if (!currentSearchCriteria.value) return false;
  const { origin, destination, departureDate, flightNumber } = currentSearchCriteria.value;
  const isUntouchedDefault = origin === 'SGN' && destination === 'HAN' && (!departureDate || departureDate === '') && (!flightNumber || flightNumber === '');
  return !isUntouchedDefault;
});

// Fallback capped at 6 items, excluding flights already shown as matches
const limitedFallbackFlights = computed(() => {
  const matchedIds = new Set(filteredFlights.value.map(f => f.id));
  return fallbackFlights.value
    .filter(f => !matchedIds.has(f.id))
    .slice(0, 6);
});

const handleSearch = async (searchCriteria) => {
  console.log('Search criteria:', searchCriteria);
  currentSearchCriteria.value = searchCriteria;
  try {
    const tripTypeParam = searchCriteria && searchCriteria.tripType === 'roundTrip' ? 'round-trip' : 'one-way';
    const response = await fetch(`http://127.0.0.1:8000/api/v1/flights/public?trip_type=${tripTypeParam}`);
    if (!response.ok) throw new Error('Failed to fetch flights');
    const data = await response.json();
    flights.value = data.map(f => ({
      id: f.id,
      airline: f.airline,
      flightNumber: f.flightNumber || f.flight_number,
      origin: f.origin,
      destination: f.destination,
      departure_date: f.departure_date || (f.departure_time ? f.departure_time.split('T')[0] : ''),
      departure_time: f.departure_time || null,
      trip_type: f.trip_type || 'one-way',
      return_date: f.return_date || null,
      departureDate: f.departure_time ? f.departure_time.split('T')[0] : '',
      departureTime: f.departureTime || (f.departure_time ? f.departure_time.split('T')[1]?.substring(0, 5) || f.departure_time : ''),
      arrivalTime: f.arrivalTime || (f.arrival_time ? f.arrival_time.split('T')[1]?.substring(0, 5) || f.arrival_time : ''),
      duration: f.duration || (f.duration_minutes ? `${Math.floor(f.duration_minutes/60)}h ${f.duration_minutes%60}m` : '1h 45m'),
      stops: f.stops !== undefined ? f.stops : 0,
      base_price: f.base_price !== undefined ? f.base_price : (f.price || f.price_economy || 0),
      availableSeats: f.available_seats !== undefined ? f.available_seats : (f.availableSeats || 180),
      available_seats: f.available_seats !== undefined ? f.available_seats : 180,
      total_seats: f.total_seats || 180,
      status: f.status || 'ON TIME',
      features: f.features || [

        f.wifi_available ? 'WiFi Available' : null,
        f.meal_service ? 'Meal Service' : null,
        'Seat Selection'
      ].filter(Boolean)
    }));
  } catch (error) {
    console.error('Error searching flights, falling back to mock:', error);
    flights.value = mockFlights.map(f => ({ ...f, base_price: f.price || 0, departureDate: '2026-06-01' }));
  }
};

const handleSelectFlight = (flight) => {
  const isLoggedIn = !!localStorage.getItem('user') || !!localStorage.getItem('sb-access-token'); 
  
  if (!isLoggedIn) {
    showAuthModal.value = true;
    return;
  }
  
  selectedFlight.value = flight;
  console.log('Selected flight:', flight);
  localStorage.setItem('selected_flight', JSON.stringify(flight));
  router.push({
    path: '/booking',
    query: {
      id: flight.id,
      airline: flight.airline,
      flightNumber: flight.flightNumber,
      origin: flight.origin,
      destination: flight.destination,
      price: flight.base_price,
      departureTime: flight.departureTime,
      arrivalTime: flight.arrivalTime
    }
  });
};

import { supabase } from '../supabase.js';

let flightsRealtimeChannel = null;

const loadPublicFlights = async () => {
  try {
    const tripTypeParam = currentSearchCriteria.value && currentSearchCriteria.value.tripType === 'roundTrip' ? 'round-trip' : 'one-way';
    const response = await fetch(`http://127.0.0.1:8000/api/v1/flights/public?trip_type=${tripTypeParam}`);
    if (!response.ok) throw new Error('Failed to fetch flights');
    const data = await response.json();
    flights.value = data.map(f => ({
      id: f.id,
      airline: f.airline,
      flightNumber: f.flightNumber || f.flight_number,
      origin: f.origin,
      destination: f.destination,
      departure_date: f.departure_date || (f.departure_time ? f.departure_time.split('T')[0] : ''),
      departure_time: f.departure_time || null,
      trip_type: f.trip_type || 'one-way',
      return_date: f.return_date || null,
      departureDate: f.departure_time ? f.departure_time.split('T')[0] : '',
      departureTime: f.departureTime || (f.departure_time ? f.departure_time.split('T')[1]?.substring(0, 5) || f.departure_time : ''),
      arrivalTime: f.arrivalTime || (f.arrival_time ? f.arrival_time.split('T')[1]?.substring(0, 5) || f.arrival_time : ''),
      duration: f.duration || (f.duration_minutes ? `${Math.floor(f.duration_minutes/60)}h ${f.duration_minutes%60}m` : '1h 45m'),
      stops: f.stops !== undefined ? f.stops : 0,
      base_price: f.base_price !== undefined ? f.base_price : (f.price || f.price_economy || 0),
      availableSeats: f.available_seats !== undefined ? f.available_seats : (f.availableSeats || 180),
      available_seats: f.available_seats !== undefined ? f.available_seats : 180,
      total_seats: f.total_seats || 180,
      status: f.status || 'ON TIME',
      features: f.features || [
        f.wifi_available ? 'WiFi Available' : null,
        f.meal_service ? 'Meal Service' : null,
        'Seat Selection'
      ].filter(Boolean)
    }));
  } catch (error) {
    console.error('Error fetching public flights:', error);
  }
};

let expiryTimer = null;

onMounted(async () => {
  await loadPublicFlights();
  document.addEventListener('click', closeSortDropdown);

  // Real-time expiry tick to update reactive timer every 10 seconds
  expiryTimer = setInterval(() => {
    currentTimeTrigger.value = Date.now();
  }, 10000);

  try {
    flightsRealtimeChannel = supabase
      .channel('public-flights-realtime')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'flights' },
        () => {
          loadPublicFlights();
        }
      )
      .subscribe();
  } catch (err) {
    console.error('Error setting up flights realtime listener:', err);
  }
});

onUnmounted(() => {
  document.removeEventListener('click', closeSortDropdown);
  if (expiryTimer) {
    clearInterval(expiryTimer);
  }
  if (flightsRealtimeChannel) {
    supabase.removeChannel(flightsRealtimeChannel);
  }
});
</script>


<style scoped>
.no-results-message {
  text-align: center;
  padding: 2rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
  margin-bottom: 2rem;
}
.no-results-message h3 {
  margin: 0.5rem 0;
  color: #0f172a;
}
.no-results-message p {
  color: #64748b;
  margin: 0;
}
.no-results-message .no-results-icon {
  font-size: 2.5rem;
}
.home-view {
  min-height: 100vh;
  padding-bottom: 3rem;
}

.hero-section {
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.1) 100%), url('/mountain-bg.jpg') center/cover no-repeat;
  padding: 4rem 1rem 3rem 1rem;
  position: relative;
  overflow: visible;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.1"/><circle cx="80" cy="80" r="2" fill="white" opacity="0.1"/><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>');
  opacity: 0.5;
  pointer-events: none;
}

.hero-section .container {
  position: relative;
  z-index: 1;
}

.hero-content {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin: 0;
  opacity: 0.95;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.results-section {
  padding: 3rem 1rem;
  background: var(--sky-bg);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-bar {
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 20px;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 2rem;
  box-shadow: 4px 4px 0px #03121A;
  border: 2px solid #03121A;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: #03121A;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.filter-select {
  padding: 0.6rem 2.5rem 0.6rem 1rem;
  border: 2px solid #03121A;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #03121A;
  background-color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
}

.custom-select-trigger {
  user-select: none;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  height: 44px;
  line-height: 40px;
  padding-top: 0;
  padding-bottom: 0;
}

.custom-select-trigger::after {
  content: "";
  position: absolute;
  right: 1.25rem;
  top: 50%;
  width: 0.5rem;
  height: 0.5rem;
  border-right: 2px solid #03121A;
  border-bottom: 2px solid #03121A;
  transform: translateY(-50%) rotate(45deg);
  transition: transform 0.2s ease;
}

.custom-dropdown-open .custom-select-trigger::after {
  transform: translateY(-50%) rotate(-135deg);
}

.custom-options-container {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background-color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 12px;
  max-height: 250px;
  overflow-y: auto;
  z-index: 9999;
  box-shadow: 4px 4px 0px #03121A;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}


.custom-option {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  transition: all 0.2s ease;
  text-align: left;
}

.custom-option:hover {
  background-color: #F2F7FA;
  transform: translateX(4px);
}

.custom-option.selected {
  background-color: rgba(255, 94, 31, 0.1);
  border-left: 4px solid #FF5E1F;
  padding-left: 0.75rem;
}

.option-name {
  font-weight: 700;
  color: #03121A;
  font-size: 0.9rem;
}

/* Dropdown Slide Transition */
.dropdown-slide-enter-active,
.dropdown-slide-leave-active {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.dropdown-slide-enter-from {
  opacity: 0;
  transform: translateY(8px) scale(0.98);
}

.dropdown-slide-leave-to {
  opacity: 0;
  transform: translateY(4px) scale(0.99);
}

.filter-select:focus {
  outline: none;
  border-color: #FF5E1F;
}

.filter-slider {
  width: 150px;
  cursor: pointer;
  accent-color: #FF5E1F;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 700;
  color: #03121A;
}

.checkbox input {
  cursor: pointer;
  accent-color: #FF5E1F;
  width: 20px;
  height: 20px;
  border: 2px solid #03121A;
}

.results-header {
  margin-bottom: 1.5rem;
}

.results-count {
  font-size: 0.9rem;
  color: #6B7280;
  margin: 0;
}

.count {
  font-weight: 700;
  color: #0194F3;
  font-size: 1.1rem;
}

.flights-list {
  animation: slideIn 0.4s ease-out;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  width: 100%;
  box-sizing: border-box;
}


@media (max-width: 992px) {
  .flights-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .flights-list {
    grid-template-columns: 1fr;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-results h3 {
  font-size: 1.5rem;
  color: #03121A;
  margin: 0 0 0.5rem 0;
}

.no-results p {
  color: #6B7280;
  margin: 0;
}

/* Other Flights pill-badge section — matches Home.vue services-badge design */
.other-flights-badge-section {
  margin: 2.5rem 0 1.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.other-flights-badge-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
}

.other-flights-badge {
  background-color: rgba(255, 94, 31, 0.15);
  border: 1px solid rgba(255, 94, 31, 0.4);
  color: #FF5E1F;
  padding: 0.4rem 1.4rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
  box-shadow: 0 0 15px rgba(255, 94, 31, 0.3);
  animation: orange-badge-pulse 2s infinite ease-in-out;
}

.other-flights-subtitle {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0;
}

@keyframes orange-badge-pulse {
  0%   { box-shadow: 0 0 8px rgba(255, 94, 31, 0.2); transform: scale(1); }
  50%  { box-shadow: 0 0 18px rgba(255, 94, 31, 0.55); transform: scale(1.05); }
  100% { box-shadow: 0 0 8px rgba(255, 94, 31, 0.2); transform: scale(1); }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-section {
    padding: 2rem 1rem;
  }

  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select,
  .filter-slider {
    width: 100%;
  }
}

/* Pagination — exact copy of News page design */
.pagination-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.35rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.pagination-btn {
  background-color: var(--white, #ffffff);
  border: 2px solid var(--dark-text, #03121A);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--dark-text, #03121A);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px var(--dark-text, #03121A);
}

.pagination-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 3px 3px 0px var(--dark-text, #03121A);
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
    box-shadow: 1px 1px 0px var(--dark-text, #03121A);
  }
}


.results-summary {
  text-align: center;
  font-size: 0.9rem;
  color: #6B7280;
  font-weight: 700;
  margin-top: 0.75rem;
}

.auth-gate-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center;
  z-index: 10000;
}
.auth-warning-box {
  background: #ffffff;
  color: #1e293b;
  padding: 2.5rem 2rem;
  border-radius: 16px;
  width: 380px;
  text-align: center;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
}
.auth-alert-icon {
  font-size: 2.5rem; margin-bottom: 0.5rem;
}
.auth-warning-box h3 {
  font-size: 1.3rem; font-weight: 700; color: #ef4444; margin-bottom: 0.5rem;
}
.auth-message-text {
  font-size: 0.95rem; font-weight: 500; color: #64748b; margin-bottom: 1.5rem;
}
.auth-action-row {
  display: flex; gap: 12px; justify-content: center;
}
.auth-btn {
  padding: 10px 20px; font-weight: 700; border-radius: 8px; border: none; cursor: pointer; flex: 1; font-size: 0.9rem; transition: all 0.2s ease;
}
.back-gray-btn {
  background: #f1f5f9; color: #475569;
}
.back-gray-btn:hover {
  background: #e2e8f0;
}
.signin-orange-btn {
  background: #ff5e1f; color: #ffffff;
  box-shadow: 0 4px 12px rgba(255, 94, 31, 0.2);
}
.signin-orange-btn:hover {
  background: #e04f1a;
  transform: translateY(-1px);
}
</style>
