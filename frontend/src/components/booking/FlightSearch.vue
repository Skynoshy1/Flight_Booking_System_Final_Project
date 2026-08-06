<template>
  <div class="flight-search-widget">
    <!-- Trip Type Selector - 2 Separate Boxes -->
    <div class="trip-type-boxes">
      <label class="trip-box" :class="{ active: tripType === 'oneWay' }">
        <input type="radio" v-model="tripType" value="oneWay" />
        <span class="trip-box-icon">↔️</span>
        <span class="trip-box-text">One-way</span>
      </label>
      <label class="trip-box" :class="{ active: tripType === 'roundTrip' }">
        <input type="radio" v-model="tripType" value="roundTrip" />
        <span class="trip-box-icon">🔄</span>
        <span class="trip-box-text">Round-trip</span>
      </label>
    </div>

    <div class="search-container">
      <!-- Search Form -->
      <div class="search-form" :class="{ 'round-trip-form': tripType === 'roundTrip' }">
        <div class="form-group">
          <label class="form-label">From</label>
          <div class="input-wrapper custom-dropdown" :class="{ 'custom-dropdown-open': originDropdownOpen }">
            <span class="icon">✈️</span>
            <div @click="toggleOriginDropdown" class="search-input custom-select-trigger">
              {{ currentOriginLabel }}
            </div>
            
            <transition name="dropdown-slide">
              <div v-show="originDropdownOpen" class="custom-options-container">
                <div 
                  v-for="ap in localAirports" 
                  :key="ap.code" 
                  class="custom-option"
                  :class="{ selected: origin === ap.code }"
                  @click.stop="selectOrigin(ap.code)"
                >
                  <span class="option-city-code">{{ ap.city || ap.name }} ({{ ap.code }})</span>
                  <span class="option-airport-name">{{ ap.name }}</span>
                </div>
              </div>
            </transition>
          </div>
          <small class="hint">{{ selectedOriginInfo }}</small>
        </div>

        <div class="form-group">
          <label class="form-label">To</label>
          <div class="input-wrapper custom-dropdown" :class="{ 'custom-dropdown-open': destinationDropdownOpen }">
            <span class="icon">📍</span>
            <div @click="toggleDestinationDropdown" class="search-input custom-select-trigger">
              {{ currentDestinationLabel }}
            </div>
            
            <transition name="dropdown-slide">
              <div v-show="destinationDropdownOpen" class="custom-options-container">
                <div 
                  v-for="ap in localAirports" 
                  :key="ap.code" 
                  class="custom-option"
                  :class="{ selected: destination === ap.code }"
                  @click.stop="selectDestination(ap.code)"
                >
                  <span class="option-city-code">{{ ap.city || ap.name }} ({{ ap.code }})</span>
                  <span class="option-airport-name">{{ ap.name }}</span>
                </div>
              </div>
            </transition>
          </div>
          <small class="hint">{{ selectedDestinationInfo }}</small>
        </div>

        <div class="form-group">
          <label class="form-label">Departure</label>
          <div class="input-wrapper">
            <span class="icon">📅</span>
            <input 
              type="date" 
              v-model="departureDate" 
              class="search-input"
              :min="today"
            />
          </div>
        </div>

        <div class="form-group" v-if="tripType === 'roundTrip'">
          <label class="form-label">Return</label>
          <div class="input-wrapper">
            <span class="icon">🔄</span>
            <input 
              type="date" 
              v-model="returnDate" 
              class="search-input"
              :min="departureDate"
            />
          </div>
        </div>

        <div class="form-group compact-field" style="flex: 1 1 180px; min-width: 150px;">
          <label class="form-label">Flight ID</label>
          <div class="input-wrapper">
            <span class="icon">🔢</span>
            <input 
              type="text" 
              v-model="flightNumberQuery" 
              placeholder="e.g. VJ-666" 
              class="search-input"
            />
          </div>
        </div>

        <div class="form-group button-group">
          <button @click="searchFlights" class="btn-search">
            <span class="btn-icon">🔍</span>
            Search Flights
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { API_URL } from '@/utils/apiClient';

const emit = defineEmits(['search']);

const localAirports = ref([
  { code: 'SGN', city: 'Ho Chi Minh City', name: 'Tan Son Nhat International Airport' },
  { code: 'HAN', city: 'Hanoi', name: 'Noi Bai International Airport' },
  { code: 'DAD', city: 'Da Nang', name: 'Da Nang International Airport' },
  { code: 'BMV', city: 'Buon Ma Thuot', name: 'Buon Ma Thuot Airport' },
  { code: 'CXR', city: 'Nha Trang', name: 'Cam Ranh International Airport' }
]);
const originDropdownOpen = ref(false);
const destinationDropdownOpen = ref(false);

const toggleOriginDropdown = (e) => {
  e.stopPropagation();
  originDropdownOpen.value = !originDropdownOpen.value;
  destinationDropdownOpen.value = false;
};

const toggleDestinationDropdown = (e) => {
  e.stopPropagation();
  destinationDropdownOpen.value = !destinationDropdownOpen.value;
  originDropdownOpen.value = false;
};

const selectOrigin = (code) => {
  origin.value = code;
  originDropdownOpen.value = false;
  if (origin.value === destination.value) {
    destination.value = origin.value === 'HAN' ? 'SGN' : 'HAN';
  }
};

const selectDestination = (code) => {
  destination.value = code;
  destinationDropdownOpen.value = false;
  if (destination.value === origin.value) {
    origin.value = destination.value === 'HAN' ? 'SGN' : 'HAN';
  }
};

const closeDropdowns = () => {
  originDropdownOpen.value = false;
  destinationDropdownOpen.value = false;
};

const loadSearchAirports = async () => {
  try {
    const response = await fetch(`${API_URL}/airports/all`);
    if (!response.ok) throw new Error('Failed to fetch search airports');
    localAirports.value = await response.json();
  } catch (error) {
    console.error("Search input synchronization failed:", error);
    localAirports.value = [
      { code: 'SGN', city: 'Ho Chi Minh City', name: 'Tan Son Nhat International Airport' },
      { code: 'HAN', city: 'Hanoi', name: 'Noi Bai International Airport' },
      { code: 'DAD', city: 'Da Nang', name: 'Da Nang International Airport' },
      { code: 'BMV', city: 'Buon Ma Thuot', name: 'Buon Ma Thuot Airport' },
      { code: 'CXR', city: 'Nha Trang', name: 'Cam Ranh International Airport' }
    ];
  }
};

const tripType = ref('oneWay');

watch(tripType, () => {
  origin.value = 'SGN';
  destination.value = 'HAN';
  departureDate.value = '';
  returnDate.value = '';
  flightNumberQuery.value = '';
  searchFlights();
});
const origin = ref('SGN');
const destination = ref('HAN');
const departureDate = ref('');
const returnDate = ref('');
const flightNumberQuery = ref('');

onMounted(async () => {
  await loadSearchAirports();
  document.addEventListener('click', closeDropdowns);
  
  // Mock IP detection / Geolocation detection
  const mockGeoCities = [
    'Ho Chi Minh City',
    'Hanoi',
    'Da Nang',
    'Nha Trang'
  ];
  const detectedCity = mockGeoCities[Math.floor(Math.random() * mockGeoCities.length)];
  
  if (detectedCity && localAirports.value.length > 0) {
    const matchedAirport = localAirports.value.find(
      airport => (airport.city || airport.name || '').toLowerCase().includes(detectedCity.toLowerCase()) || 
                 detectedCity.toLowerCase().includes((airport.city || airport.name || '').toLowerCase())
    );
    if (matchedAirport) {
      origin.value = matchedAirport.code;
      if (origin.value === destination.value) {
        destination.value = origin.value === 'HAN' ? 'SGN' : 'HAN';
      }
    }
  }
});

onUnmounted(() => {
  document.removeEventListener('click', closeDropdowns);
});

const currentOriginLabel = computed(() => {
  const airport = localAirports.value.find(a => a.code === origin.value);
  return airport ? `${airport.city || airport.name} (${airport.code})` : 'Select Departure';
});

const currentDestinationLabel = computed(() => {
  const airport = localAirports.value.find(a => a.code === destination.value);
  return airport ? `${airport.city || airport.name} (${airport.code})` : 'Select Destination';
});

const selectedOriginInfo = computed(() => {
  const airport = localAirports.value.find(a => a.code === origin.value);
  return airport ? `${airport.city || airport.name || ''} (${airport.code})` : 'Select departure airport';
});

const selectedDestinationInfo = computed(() => {
  const airport = localAirports.value.find(a => a.code === destination.value);
  return airport ? `${airport.city || airport.name || ''} (${airport.code})` : 'Select destination airport';
});

const today = computed(() => {
  const date = new Date();
  return date.toISOString().split('T')[0];
});

const searchFlights = () => {
  const searchParams = {
    tripType: tripType.value,
    origin: origin.value,
    destination: destination.value,
    departureDate: departureDate.value,
    returnDate: tripType.value === 'roundTrip' ? returnDate.value : '',
    flightNumber: flightNumberQuery.value
  };

  console.log(searchParams);
  
  // Emit event to parent Vue component
  emit('search', searchParams);
  
  // Dispatch window event for backward compatibility
  const event = new CustomEvent('search', {
    detail: searchParams
  });
  window.dispatchEvent(event);
};
</script>

<style scoped>
.flight-search-widget {
  margin-top: 2rem;
  position: relative;
}

/* Trip Type Selector - 2 Boxes */
.trip-type-boxes {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.trip-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 0 0 auto;
  font-weight: 600;
  color: #6B7280;
  position: relative;
}

.trip-box input[type="radio"] {
  display: none;
}

.trip-box:hover {
  background: rgba(255, 255, 255, 1);
  border-color: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.trip-box.active {
  background: #0194F3;
  color: white;
  border-color: #0194F3;
}

.trip-box-icon {
  font-size: 1.5rem;
}

.trip-box-text {
  font-size: 0.9rem;
  font-weight: 600;
}

.search-container {
  background: white;
  border: 2px solid #03121A;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 4px 4px 0px #03121A;
  position: relative;
  z-index: 10;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
  padding-bottom: 1.25rem;
  flex: 1 1 240px;
  min-width: 200px;
}

.button-group {
  flex: 1 1 200px;
  min-width: 180px;
}

.form-label {
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
  width: 100%;
}

.icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.1rem;
  pointer-events: none;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2rem;
  border: 2px solid #03121A;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 500;
  color: #03121A;
  background-color: #f8fafc;
  outline: none;
  transition: border-color 0.2s ease;
  font-family: inherit;
  height: 48px;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #FF5E1F;
}

.search-input::placeholder {
  color: #9CA3AF;
}

.hint {
  position: absolute;
  bottom: 0;
  left: 0;
  color: #9CA3AF;
  font-size: 0.75rem;
}

.btn-search {
  background-color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 10px;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: #03121A;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px #03121A;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: 48px;
  box-sizing: border-box;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 4px 4px 0px #03121A;
  background-color: #f1f5f9;
}

.btn-search:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 1.25rem;
}

@media (max-width: 1024px) {
  .form-group {
    flex: 1 1 calc(50% - 1rem);
  }
}

@media (max-width: 768px) {
  .flight-search-widget {
    margin-top: 1rem;
  }

  .search-container {
    padding: 1.25rem;
  }

  .search-form {
    flex-direction: column;
    gap: 1rem;
  }

  .form-group, .button-group {
    flex: 1 1 100%;
    width: 100%;
    min-width: 100%;
  }

  .btn-search {
    width: 100%;
  }

  .trip-type-boxes {
    flex-direction: row;
    width: 100%;
  }

  .trip-box {
    flex: 1;
    text-align: center;
  }
}


/* Custom Dropdown Styling */
.custom-dropdown {
  position: relative;
  width: 100%;
}

.custom-select-trigger {
  cursor: pointer;
  background-color: #ffffff;
  display: block;
  user-select: none;
  border: 2px solid #03121A;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 2.5rem;
  height: 48px;
  line-height: 44px;
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
  max-height: 238px;
  overflow-y: auto;
  z-index: 9999;
  box-shadow: 4px 4px 0px #03121A; /* Neo-brutalist solid shadow */
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
  transform: translateX(4px); /* Premium animated list effect */
}

.custom-option.selected {
  background-color: rgba(1, 148, 243, 0.1);
  border-left: 4px solid #0194F3;
  padding-left: 0.75rem;
}

.option-city-code {
  font-weight: 700;
  color: #03121A;
  font-size: 0.9rem;
}

.option-airport-name {
  font-size: 0.75rem;
  color: #6B7280;
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
</style>
