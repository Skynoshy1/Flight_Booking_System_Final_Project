<template>
  <div class="flight-table-container">
    <div class="table-responsive-wrapper">

      <table class="flight-table">
        <thead>
          <tr>
            <th>Flight #</th>
            <th>Route</th>
            <th>Departure</th>
            <th>Total Seats</th>
            <th>Available</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="flight in paginatedFlights" :key="flight.id" class="flight-row">
            <td class="flight-number">{{ flight.flight_number || flight.flightNumber }}</td>
            <td class="route">{{ flight.origin }} ➔ {{ flight.destination }}</td>
            <td class="departure">
              {{ flight.departure_date }} 
              ({{ new Date(flight.departure_time || flight.departureDate).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }})
            </td>
            <td class="seats">{{ flight.total_seats || 180 }}</td>
            <td class="available">
              <span class="badge" :class="{ low: (flight.available_seats !== undefined ? flight.available_seats : (flight.available !== undefined ? flight.available : 8)) < 5 }">
                {{ flight.available_seats !== undefined ? flight.available_seats : (flight.available !== undefined ? flight.available : 8) }}
              </span>
            </td>
            <td class="status">
              <span class="status-badge" :class="(flight.status || 'ON TIME').toString().toLowerCase().replace(/\s+/g, '-')">
                {{ flight.status || 'ON TIME' }}
              </span>
            </td>

            <td class="action">
              <button class="btn-edit" @click="openEditModal(flight)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>


    <nav v-if="totalPages > 1" class="pagination-nav" aria-label="Flights Pagination">
      <button
        class="pagination-btn"
        :disabled="currentPage === 1"
        @click="currentPage = 1"
        aria-label="First page"
      >
        &laquo; First
      </button>
      <button
        class="pagination-btn"
        :disabled="currentPage === 1"
        @click="currentPage--"
        aria-label="Previous page"
      >
        &lsaquo; Prev
      </button>

      <div class="page-numbers">
        <button
          v-for="page in displayedPages"
          :key="page"
          class="pagination-btn page-num-btn"
          :class="{ 'active-page': currentPage === page }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>

      <button
        class="pagination-btn"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
        aria-label="Next page"
      >
        Next &rsaquo;
      </button>
      <button
        class="pagination-btn"
        :disabled="currentPage === totalPages"
        @click="currentPage = totalPages"
        aria-label="Last page"
      >
        Last &raquo;
      </button>
    </nav>


    <!-- Edit Flight Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card">
          <div class="modal-header">
            <div class="header-title-box">
              <span class="modal-icon">✈️</span>
              <div>
                <h3>Edit Flight #{{ editForm.flight_number }}</h3>
                <p class="route-subtitle">{{ editForm.origin }} ➔ {{ editForm.destination }}</p>
              </div>
            </div>
            <button class="close-btn" @click="closeModal">&times;</button>
          </div>

          <form @submit.prevent="saveFlight" class="modal-body">
            <!-- Departure Date & Time -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">📅</span> Departure Date
                </label>
                <input 
                  type="date" 
                  v-model="editForm.departure_date" 
                  class="custom-input" 
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">⏰</span> Departure Time
                </label>
                <input 
                  type="time" 
                  v-model="editForm.departure_time" 
                  class="custom-input" 
                  required
                />
              </div>
            </div>

            <!-- Total Seats & Available Seats -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">💺</span> Total Seats
                </label>
                <input 
                  type="number" 
                  v-model.number="editForm.total_seats" 
                  @input="handleTotalSeatsChange"
                  min="1" 
                  max="600" 
                  class="custom-input" 
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">✅</span> Available Seats
                </label>
                <input 
                  type="number" 
                  v-model.number="editForm.available_seats" 
                  min="0" 
                  :max="editForm.total_seats" 
                  class="custom-input" 
                  required
                />
              </div>
            </div>

            <!-- Status Custom Dropdown Menu -->
            <div class="form-group">
              <label class="form-label">
                <span class="icon">🚦</span> Flight Status
              </label>
              <div class="custom-dropdown-container" @click.stop>
                <div class="custom-select-trigger" @click="statusDropdownOpen = !statusDropdownOpen">
                  <span class="status-badge-preview" :class="editForm.status.toLowerCase().replace(/\s+/g, '-')">
                    {{ editForm.status }}
                  </span>
                  <span class="dropdown-chevron">▼</span>
                </div>

                <transition name="dropdown-slide">
                  <div v-if="statusDropdownOpen" class="custom-dropdown-menu">
                    <div 
                      class="custom-option" 
                      :class="{ selected: editForm.status === 'ON TIME' }"
                      @click="selectStatus('ON TIME')"
                    >
                      <span class="status-badge-preview on-time">ON TIME</span>
                      <span class="status-desc">Flight is on schedule</span>
                    </div>

                    <div 
                      class="custom-option" 
                      :class="{ selected: editForm.status === 'DELAY' }"
                      @click="selectStatus('DELAY')"
                    >
                      <span class="status-badge-preview delay">DELAY</span>
                      <span class="status-desc">Flight schedule delayed</span>
                    </div>

                    <div 
                      class="custom-option" 
                      :class="{ selected: editForm.status === 'CANCELED' }"
                      @click="selectStatus('CANCELED')"
                    >
                      <span class="status-badge-preview canceled">CANCELED</span>
                      <span class="status-desc">Flight has been canceled</span>
                    </div>
                  </div>
                </transition>
              </div>
            </div>

            <!-- Error Notification -->
            <div v-if="saveError" class="error-msg">
              ⚠️ {{ saveError }}
            </div>

            <!-- Modal Action Footer -->
            <div class="modal-footer">
              <button type="button" class="btn-cancel" @click="closeModal" :disabled="isSubmitting">Cancel</button>
              <button type="submit" class="btn-save" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner">🌀</span>
                <span v-else>Save Changes</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Add Flight Modal -->
    <Teleport to="body">
      <div v-if="showAddModal" class="modal-overlay" @click.self="closeAddModal">
        <div class="modal-card">
          <div class="modal-header" style="background: linear-gradient(135deg, #FF5E1F 0%, #E54812 100%)">
            <div class="header-title-box">
              <span class="modal-icon">✈️</span>
              <div>
                <h3>Add New Flight</h3>
                <p class="route-subtitle">Create a brand new flight entry</p>
              </div>
            </div>
            <button class="close-btn" @click="closeAddModal">&times;</button>
          </div>

          <form @submit.prevent="submitAddFlight" class="modal-body">
            <!-- Trip Type Selector -->
            <div class="form-group">
              <label class="form-label">Trip Type</label>
              <div class="trip-type-btn-group">
                <button 
                  type="button" 
                  class="trip-type-btn one-way-btn" 
                  :class="{ active: addForm.trip_type === 'one-way' }"
                  @click="addForm.trip_type = 'one-way'"
                >
                  One-way
                </button>
                <button 
                  type="button" 
                  class="trip-type-btn round-trip-btn" 
                  :class="{ active: addForm.trip_type === 'round-trip' }"
                  @click="addForm.trip_type = 'round-trip'"
                >
                  Round-trip
                </button>
              </div>
            </div>

            <!-- Airline Selection -->
            <div class="form-group">
              <label class="form-label">
                <span class="icon">🏢</span> Airline
              </label>
              <div class="custom-dropdown-container" @click.stop>
                <div class="custom-select-trigger" @click="airlineDropdownOpen = !airlineDropdownOpen; originDropdownOpen = false; destinationDropdownOpen = false">
                  <span>{{ addForm.airline }}</span>
                  <span class="dropdown-chevron">▼</span>
                </div>
                <transition name="dropdown-slide">
                  <div v-if="airlineDropdownOpen" class="custom-dropdown-menu">
                    <div 
                      v-for="airlineName in airlinesList" 
                      :key="airlineName" 
                      class="custom-option"
                      :class="{ selected: addForm.airline === airlineName }"
                      @click="addForm.airline = airlineName; airlineDropdownOpen = false;"
                    >
                      <span>{{ airlineName }}</span>
                    </div>
                  </div>
                </transition>
              </div>
            </div>

            <!-- Flight Number & Price -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">🔢</span> Flight Number
                </label>
                <input 
                  type="text" 
                  v-model="addForm.flight_number" 
                  placeholder="e.g. VJ-666" 
                  class="custom-input"
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">💵</span> Ticket Price ($)
                </label>
                <input 
                  type="number" 
                  v-model.number="addForm.base_price" 
                  min="1" 
                  class="custom-input"
                  required
                />
              </div>
            </div>

            <!-- Origin & Destination Dropdowns (Traveloka Search Panel Style) -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">🛫</span> Start (Origin)
                </label>
                <div class="custom-dropdown-container" @click.stop>
                  <div class="custom-select-trigger" @click="originDropdownOpen = !originDropdownOpen; destinationDropdownOpen = false; airlineDropdownOpen = false">
                    <span>{{ addForm.origin }}</span>
                    <span class="dropdown-chevron">▼</span>
                  </div>
                  <transition name="dropdown-slide">
                    <div v-if="originDropdownOpen" class="custom-dropdown-menu">
                      <div 
                        v-for="ap in localAirports" 
                        :key="ap.code" 
                        class="custom-option"
                        :class="{ selected: addForm.origin === ap.code }"
                        @click="selectAddOrigin(ap.code)"
                      >
                        <span class="option-city-code">{{ ap.city || ap.name }} ({{ ap.code }})</span>
                      </div>
                    </div>
                  </transition>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <span class="icon">🛬</span> Destination
                </label>
                <div class="custom-dropdown-container" @click.stop>
                  <div class="custom-select-trigger" @click="destinationDropdownOpen = !destinationDropdownOpen; originDropdownOpen = false; airlineDropdownOpen = false">
                    <span>{{ addForm.destination }}</span>
                    <span class="dropdown-chevron">▼</span>
                  </div>
                  <transition name="dropdown-slide">
                    <div v-if="destinationDropdownOpen" class="custom-dropdown-menu">
                      <div 
                        v-for="ap in localAirports" 
                        :key="ap.code" 
                        class="custom-option"
                        :class="{ selected: addForm.destination === ap.code }"
                        @click="selectAddDestination(ap.code)"
                      >
                        <span class="option-city-code">{{ ap.city || ap.name }} ({{ ap.code }})</span>
                      </div>
                    </div>
                  </transition>
                </div>
              </div>
            </div>

            <!-- Departure Date & Departure Time -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">📅</span> Departure Date
                </label>
                <input 
                  type="date" 
                  v-model="addForm.departure_date" 
                  class="custom-input" 
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">⏰</span> Departure Time
                </label>
                <input 
                  type="time" 
                  v-model="addForm.departure_time" 
                  class="custom-input" 
                  required
                />
              </div>
            </div>

            <!-- Return Date (only if Round-trip) & Total Seats -->
            <div class="form-row">
              <div class="form-group" v-if="addForm.trip_type === 'round-trip'">
                <label class="form-label">
                  <span class="icon">🔄</span> Return Date
                </label>
                <input 
                  type="date" 
                  v-model="addForm.return_date" 
                  :min="addForm.departure_date" 
                  class="custom-input" 
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">
                  <span class="icon">💺</span> Total Seats
                </label>
                <input 
                  type="number" 
                  v-model.number="addForm.total_seats" 
                  min="1" 
                  max="600" 
                  class="custom-input" 
                  required
                />
              </div>
            </div>

            <!-- Error Notification -->
            <div v-if="saveError" class="error-msg">
              ⚠️ {{ saveError }}
            </div>

            <!-- Modal Action Footer -->
            <div class="modal-footer">
              <button type="button" class="btn-cancel" @click="closeAddModal" :disabled="isSubmitting">Cancel</button>
              <button type="submit" class="btn-save" :disabled="isSubmitting" style="background: linear-gradient(135deg, #FF5E1F 0%, #E54812 100%); border-color: transparent;">
                <span v-if="isSubmitting" class="spinner">🌀</span>
                <span v-else>Add Flight</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Success Notification Modal -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="showSuccessNotification" class="success-notification-overlay" @click="showSuccessNotification = false">
          <div class="success-notification-card">
            <div class="success-tick-circle">
              <span class="tick-icon">✓</span>
            </div>
            <h3>Success!</h3>
            <p>{{ successMessage }}</p>
            <button class="btn-ok" @click="showSuccessNotification = false">OK</button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  flights: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['flight-updated']);

const currentPage = ref(1);
const itemsPerPage = 10;
const showModal = ref(false);
const statusDropdownOpen = ref(false);
const isSubmitting = ref(false);
const saveError = ref('');
const showSuccessNotification = ref(false);
const successMessage = ref('');

// Add Flight States & Dropdowns
const showAddModal = ref(false);
const originDropdownOpen = ref(false);
const destinationDropdownOpen = ref(false);
const airlineDropdownOpen = ref(false);
const localAirports = ref([]);
const airlinesList = [
  'Vietnam Airlines',
  'VietJet Air',
  'Bamboo Airways',
  'Vietravel Airlines'
];

const addForm = ref({
  airline: 'Vietnam Airlines',
  flight_number: '',
  trip_type: 'one-way',
  origin: 'SGN',
  destination: 'HAN',
  departure_date: '',
  departure_time: '08:00',
  return_date: '',
  total_seats: 180,
  base_price: 100
});

const editForm = ref({
  id: null,
  flight_number: '',
  origin: '',
  destination: '',
  departure_date: '',
  departure_time: '',
  total_seats: 180,
  available_seats: 180,
  status: 'ON TIME'
});

const openEditModal = (flight) => {
  let depDate = flight.departure_date || '';
  let depTime = '08:00';
  
  const rawTime = flight.departure_time || flight.departureTime;
  if (rawTime) {
    if (rawTime.includes('T')) {
      const parts = rawTime.split('T');
      if (!depDate) depDate = parts[0];
      depTime = parts[1].substring(0, 5);
    } else if (rawTime.includes(':')) {
      depTime = rawTime.substring(0, 5);
    }
  }
  if (!depDate) {
    depDate = new Date().toISOString().split('T')[0];
  }

  const origTotal = flight.total_seats || 180;
  const origAvail = flight.available_seats !== undefined ? flight.available_seats : (flight.available !== undefined ? flight.available : 8);

  editForm.value = {
    id: flight.id,
    flight_number: flight.flight_number || flight.flightNumber || `FL-${flight.id}`,
    origin: flight.origin || 'SGN',
    destination: flight.destination || 'HAN',
    departure_date: depDate,
    departure_time: depTime,
    total_seats: origTotal,
    available_seats: origAvail,
    status: flight.status || 'ON TIME',
    originalTotal: origTotal,
    originalAvail: origAvail
  };
  saveError.value = '';
  statusDropdownOpen.value = false;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  statusDropdownOpen.value = false;
};

const selectStatus = (statusVal) => {
  editForm.value.status = statusVal;
  statusDropdownOpen.value = false;
};

const handleTotalSeatsChange = () => {
  const diff = editForm.value.total_seats - (editForm.value.originalTotal || 180);
  const newAvail = (editForm.value.originalAvail || 0) + diff;
  editForm.value.available_seats = Math.max(0, Math.min(newAvail, editForm.value.total_seats));
};

const closeDropdownOnOutside = () => {
  statusDropdownOpen.value = false;
  originDropdownOpen.value = false;
  destinationDropdownOpen.value = false;
  airlineDropdownOpen.value = false;
};

const fetchAirports = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/airports/all');
    if (response.ok) {
      localAirports.value = await response.json();
    }
  } catch (err) {
    console.error('Error fetching airports:', err);
    localAirports.value = [
      { code: 'SGN', city: 'Ho Chi Minh City', name: 'Tan Son Nhat International Airport' },
      { code: 'HAN', city: 'Hanoi', name: 'Noi Bai International Airport' },
      { code: 'DAD', city: 'Da Nang', name: 'Da Nang International Airport' },
      { code: 'CXR', city: 'Nha Trang', name: 'Cam Ranh International Airport' },
      { code: 'DLI', city: 'Da Lat', name: 'Lien Khuong Airport' }
    ];
  }
};

onMounted(async () => {
  document.addEventListener('click', closeDropdownOnOutside);
  await fetchAirports();
});

onUnmounted(() => {
  document.removeEventListener('click', closeDropdownOnOutside);
});

const getAirlinePrefix = (airline) => {
  switch (airline) {
    case 'Vietnam Airlines': return 'VN-';
    case 'VietJet Air': return 'VJ-';
    case 'Bamboo Airways': return 'BA-';
    case 'Vietravel Airlines': return 'VA-';
    default: return 'FL-';
  }
};

watch(() => addForm.value.airline, (newAirline, oldAirline) => {
  const newPrefix = getAirlinePrefix(newAirline);
  const oldPrefix = oldAirline ? getAirlinePrefix(oldAirline) : '';
  
  let currentVal = addForm.value.flight_number || '';
  
  if (oldPrefix && currentVal.startsWith(oldPrefix)) {
    addForm.value.flight_number = newPrefix + currentVal.slice(oldPrefix.length);
  } else {
    const digitsOnly = currentVal.replace(/^\D+/, '');
    addForm.value.flight_number = newPrefix + digitsOnly;
  }
});

const openAddModal = () => {
  addForm.value = {
    airline: 'Vietnam Airlines',
    flight_number: 'VN-',
    trip_type: 'one-way',
    origin: 'SGN',
    destination: 'HAN',
    departure_date: new Date().toISOString().split('T')[0],
    departure_time: '08:00',
    return_date: '',
    total_seats: 180,
    base_price: 100
  };
  showAddModal.value = true;
  saveError.value = '';
};

const closeAddModal = () => {
  showAddModal.value = false;
  originDropdownOpen.value = false;
  destinationDropdownOpen.value = false;
  airlineDropdownOpen.value = false;
};

const selectAddOrigin = (code) => {
  addForm.value.origin = code;
  originDropdownOpen.value = false;
  if (addForm.value.origin === addForm.value.destination) {
    addForm.value.destination = addForm.value.origin === 'HAN' ? 'SGN' : 'HAN';
  }
};

const selectAddDestination = (code) => {
  addForm.value.destination = code;
  destinationDropdownOpen.value = false;
  if (addForm.value.destination === addForm.value.origin) {
    addForm.value.origin = addForm.value.destination === 'HAN' ? 'SGN' : 'HAN';
  }
};

const submitAddFlight = async () => {
  isSubmitting.value = true;
  saveError.value = '';
  try {
    const fullDepartureTime = `${addForm.value.departure_date}T${addForm.value.departure_time}:00`;
    
    const payload = {
      airline: addForm.value.airline,
      flight_number: addForm.value.flight_number || null,
      origin: addForm.value.origin,
      destination: addForm.value.destination,
      departure_date: addForm.value.departure_date,
      departure_time: fullDepartureTime,
      trip_type: addForm.value.trip_type,
      return_date: addForm.value.trip_type === 'round-trip' ? addForm.value.return_date : null,
      total_seats: Number(addForm.value.total_seats),
      available_seats: Number(addForm.value.total_seats),
      base_price: Number(addForm.value.base_price),
      status: 'ON TIME'
    };

    const response = await fetch('http://127.0.0.1:8000/api/v1/flights', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Failed to create flight');
    }

    emit('flight-updated');
    closeAddModal();
    
    // Trigger Success Notification Modal
    successMessage.value = 'Flight successfully added to the system!';
    showSuccessNotification.value = true;
  } catch (err) {
    console.error('Error adding flight:', err);
    saveError.value = err.message || 'Error adding flight';
  } finally {
    isSubmitting.value = false;
  }
};

defineExpose({
  openAddModal
});

const saveFlight = async () => {
  isSubmitting.value = true;
  saveError.value = '';

  try {
    const fullDepartureTime = `${editForm.value.departure_date}T${editForm.value.departure_time}:00`;
    
    const payload = {
      departure_date: editForm.value.departure_date,
      departure_time: fullDepartureTime,
      total_seats: Number(editForm.value.total_seats),
      available_seats: Number(editForm.value.available_seats),
      status: editForm.value.status
    };

    let updatedData = null;
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/flights/${editForm.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        updatedData = await response.json();
      }
    } catch (netErr) {
      console.warn('Network request skipped or failed, updating local state:', netErr);
    }

    // Always update local flight object so UI reflects status change immediately
    const targetFlight = props.flights.find(f => f.id === editForm.value.id);
    if (targetFlight) {
      targetFlight.status = editForm.value.status;
      targetFlight.total_seats = Number(editForm.value.total_seats);
      targetFlight.available_seats = Number(editForm.value.available_seats);
      targetFlight.available = Number(editForm.value.available_seats);
      targetFlight.departure_date = editForm.value.departure_date;
      targetFlight.departure_time = fullDepartureTime;
      targetFlight.departureDate = editForm.value.departure_date;
    }

    emit('flight-updated');
    closeModal();
  } catch (err) {
    console.error('Error updating flight:', err);
    saveError.value = err.message || 'Error updating flight';
  } finally {
    isSubmitting.value = false;
  }
};



watch(() => props.flights, () => {
  currentPage.value = 1;
});

const paginatedFlights = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return props.flights.slice(start, end);
});

const totalPages = computed(() => Math.ceil(props.flights.length / itemsPerPage));

const displayedPages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  
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

</script>

<style scoped>
.flight-table-container {
  overflow-x: auto;
}

.flight-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.flight-table thead {
  background: #F2F7FA;
}

.flight-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #6B7280;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #E5E7EB;
}

.flight-table td {
  padding: 1rem;
  border-bottom: 1px solid #F0F1F3;
  color: #6B7280;
}

.flight-row:hover {
  background: #F9FAFB;
}

.flight-number {
  font-weight: 700;
  color: #0194F3;
}

.route {
  font-weight: 600;
  color: #03121A;
}

.departure {
  color: #03121A;
  font-weight: 500;
}

.seats,
.available {
  text-align: center;
  font-weight: 600;
}

.available {
  color: #10B981;
}

.badge {
  display: inline-block;
  background: #DCFCE7;
  color: #10B981;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.low {
  background: #FEE2E2;
  color: #EF4444;
}

.status {
  text-align: center;
}

.status-badge {
  display: inline-block;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.on-time {
  background: #DCFCE7;
  color: #10B981;
}

.status-badge.delay,
.status-badge.delayed {
  background: #FEF3C7;
  color: #D97706;
}

.status-badge.canceled,
.status-badge.cancelled {
  background: #FEE2E2;
  color: #EF4444;
}

.action {
  text-align: center;
}

.btn-edit {
  background: #0194F3;
  color: #ffffff;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(1, 148, 243, 0.3);
}

.btn-edit:hover {
  background: #0178C9;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(1, 148, 243, 0.4);
}


/* Edit Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-card {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 540px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: visible;
  animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid #e2e8f0;
}

@keyframes modalPop {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  background: linear-gradient(135deg, #0194F3 0%, #0178C9 100%);
  color: white;
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 16px 16px 0 0;
}

.header-title-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-icon {
  font-size: 1.75rem;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
}

.route-subtitle {
  margin: 2px 0 0 0;
  font-size: 0.85rem;
  opacity: 0.9;
  font-weight: 500;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.35);
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  overflow-y: auto;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 6px;
}

.custom-input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #0f172a;
  background: #f8fafc;
  outline: none;
  transition: all 0.2s ease;
}

.custom-input:focus {
  border-color: #0194F3;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(1, 148, 243, 0.15);
}

/* Custom Dropdown Styling (Traveloka Search Panel Style) */
.custom-dropdown-container {
  position: relative;
  width: 100%;
}

.custom-select-trigger {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
}

.custom-select-trigger:hover {
  border-color: #0194F3;
  background: #ffffff;
}

.dropdown-chevron {
  font-size: 0.75rem;
  color: #64748b;
  transition: transform 0.2s ease;
}

.custom-dropdown-menu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow-y: auto;
  max-height: 220px;
  padding: 4px;
}


.custom-option {
  padding: 0.65rem 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.15s ease;
}

.custom-option:hover {
  background: #f0f9ff;
}

.custom-option.selected {
  background: #e0f2fe;
}

.status-badge-preview {
  display: inline-block;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge-preview.on-time,
.status-badge-preview.on\ time {
  background: #DCFCE7;
  color: #10B981;
}

.status-badge-preview.delay,
.status-badge-preview.delayed {
  background: #FEF3C7;
  color: #D97706;
}

.status-badge-preview.canceled,
.status-badge-preview.cancelled {
  background: #FEE2E2;
  color: #EF4444;
}

.status-desc {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 500;
}

.error-msg {
  background: #fef2f2;
  color: #ef4444;
  padding: 0.65rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid #fecaca;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.btn-cancel {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover:not(:disabled) {
  background: #e2e8f0;
}

.btn-save {
  background: linear-gradient(135deg, #FF5E1F 0%, #E54812 100%);
  color: white;
  border: none;
  padding: 0.65rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(255, 94, 31, 0.25);
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(255, 94, 31, 0.35);
}

.btn-save:disabled, .btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.dropdown-slide-enter-active,
.dropdown-slide-leave-active {
  transition: all 0.2s ease;
}

.dropdown-slide-enter-from,
.dropdown-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Pagination — exact copy of Flights page design */
.pagination-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.pagination-btn {
  background-color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: #03121A;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px #03121A;
}

.pagination-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 4px 4px 0px #03121A;
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
  gap: 0.5rem;
}

.page-num-btn.active-page {
  background-color: #FF5E1F;
  color: #ffffff;
  box-shadow: inset 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.trip-type-btn-group {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.trip-type-btn {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.25s ease;
  font-size: 0.95rem;
  background: #f1f5f9;
  color: #475569;
}

.trip-type-btn.one-way-btn:hover {
  background: #e0f2fe;
  color: #0194F3;
  border-color: #0194F3;
}

.trip-type-btn.one-way-btn.active {
  background: #0194F3;
  color: white;
  box-shadow: 0 4px 12px rgba(1, 148, 243, 0.25);
}

.trip-type-btn.round-trip-btn:hover {
  background: #fee2e2;
  color: #ef4444;
  border-color: #ef4444;
}

.trip-type-btn.round-trip-btn.active {
  background: #ef4444;
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
}

.option-city-code {
  font-weight: 600;
  color: #0f172a;
}

/* Success Notification Styles */
.success-notification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  padding: 1rem;
}

.success-notification-card {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 380px;
  padding: 2.5rem 2rem;
  text-align: center;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  animation: scaleIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.success-tick-circle {
  width: 70px;
  height: 70px;
  background: #dcfce7;
  border: 3px solid #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem auto;
  box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);
}

.tick-icon {
  font-size: 2.2rem;
  color: #10b981;
  font-weight: bold;
}

.success-notification-card h3 {
  margin: 0 0 0.5rem 0;
  color: #0f172a;
  font-size: 1.5rem;
  font-weight: 700;
}

.success-notification-card p {
  margin: 0 0 1.5rem 0;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 500;
}

.btn-ok {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.65rem 2.5rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  width: 100%;
}

.btn-ok:hover {
  background: #059669;
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
  transform: translateY(-1px);
}

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.25s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
</style>


