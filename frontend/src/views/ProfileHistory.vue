<template>
  <div class="profile-page-wrapper">
    <div class="profile-container">
      
      <!-- LEFT SIDEBAR -->
      <aside class="profile-sidebar">
        <!-- Top User Card -->
        <div class="user-sidebar-card">
          <div class="avatar-container">
            <img v-if="user && user.avatar_url" :src="user.avatar_url" class="user-sidebar-avatar" alt="User Avatar" />
            <div v-else class="avatar-placeholder">{{ userInitials }}</div>
          </div>
          <div class="user-meta">
            <h3 class="user-fullname">{{ profileUsername || 'Guest Explorer' }}</h3>
            <span class="user-subtitle">Verified Account</span>
          </div>
        </div>
        
        <!-- Tier Badge -->
        <div class="tier-badge-container" :class="loyaltyTier.class">
          <span class="badge-icon">{{ loyaltyTier.icon }}</span>
          <span class="badge-text">{{ loyaltyTier.text }}</span>
          <!-- Tooltip Popup -->
          <div class="tier-tooltip">
            <span class="tooltip-arrow"></span>
            <div class="tooltip-header">{{ loyaltyTier.name }} Benefit</div>
            <div class="tooltip-body">
              Enjoy a <span class="discount-value-highlight">{{ loyaltyTier.discount }}%</span> discount on all flights!
            </div>
          </div>
        </div>
        
        <!-- Navigation Menu List -->
        <nav class="sidebar-nav">
          <ul>
            <li v-for="item in menuItems" :key="item.name" :class="{ active: item.active }">
              <a href="#" @click.prevent="setActiveMenu(item.name)">
                <span class="menu-icon">{{ item.icon }}</span>
                <span class="menu-label">
                  <template v-if="item.name === 'Points (0)'">
                    {{ userPoints }} Points
                  </template>
                  <template v-else>
                    {{ item.name }}
                  </template>
                </span>
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- RIGHT MAIN CONTENT AREA -->
      <main class="profile-main-content">
        <h1 v-if="activeSubTab !== 'bookings'" class="main-title">Settings</h1>
        <h1 v-else class="main-title">Active E-tickets & Vouchers</h1>
        
        <!-- Section Tabs -->
        <div v-if="activeSubTab !== 'bookings'" class="section-tabs">
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'account' }"
            @click="activeTab = 'account'; activeSubTab = 'account'; setActiveMenu('My Account')"
          >
            Account Information
          </button>
          <button 
            class="tab-btn" 
            :class="{ active: activeTab === 'security' }"
            @click="activeTab = 'security'"
          >
            Password & Security
          </button>
        </div>

        <!-- Personal Data Card -->
        <div v-if="activeTab === 'account'" class="content-card">
          <h2 v-if="activeSubTab === 'account'" class="card-title">Personal Data</h2>
          
          <div v-if="activeSubTab === 'account'">
            <form @submit.prevent="saveProfile" class="personal-data-form">
              <!-- Full Name -->
              <div class="form-group full-width">
                <label for="fullname">Full Name</label>
                <input 
                  type="text" 
                  id="fullname" 
                  v-model="profileUsername" 
                  class="form-input" 
                  placeholder="Enter your full name" 
                />
                <span class="helper-text">Your full name will also appear as your profile name</span>
              </div>

              <!-- Email (Disabled) -->
              <div class="form-group full-width">
                <label for="email">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="profileEmail" 
                  class="form-input" 
                  disabled 
                  placeholder="email@example.com" 
                />
                <span class="helper-text">Registered account email cannot be changed.</span>
              </div>

              <!-- Gender & Birthdate Row -->
              <div class="form-row">
                <!-- Gender -->
                <div class="form-group gender-group">
                  <label for="gender">Gender</label>
                  <select id="gender" v-model="profileGender" class="form-select">
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>

                <!-- Birthdate -->
                <div class="form-group birthdate-group">
                  <label>Birthdate</label>
                  <div class="birthdate-selects">
                    <select v-model="birthDay" class="form-select day-select">
                      <option v-for="d in days" :key="d" :value="d">{{ d }}</option>
                    </select>
                    <select v-model="birthMonth" class="form-select month-select">
                      <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
                    </select>
                    <select v-model="birthYear" class="form-select year-select">
                      <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- City of Residence -->
              <div class="form-group full-width">
                <label for="city">City of Residence</label>
                <input 
                  type="text" 
                  id="city" 
                  v-model="profileCity" 
                  class="form-input" 
                  placeholder="e.g. Jakarta, Saigon, Bangkok" 
                />
              </div>

              <!-- Action Footer -->
              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="resetForm">Maybe later</button>
                <button type="submit" class="btn-primary">Save Changes</button>
              </div>
            </form>
          </div>

          <div v-else-if="activeSubTab === 'bookings'" class="traveloka-mini-dashboard">
            
            
            <div v-if="personalTickets.length === 0" class="no-bookings-banner new-no-bookings-banner">
              <img :src="noBookingImg" class="no-booking-img" alt="No Booking" />
              <div class="no-bookings-text-wrapper">
                <h3 class="banner-title"><strong>No Active Bookings Found</strong></h3>
                <p class="banner-text">Anything you booked shows up here, but it seems like you haven’t made any. Let’s create one via homepage!</p>
              </div>
            </div>
            
            <div v-else class="tickets-list">
              <div v-for="t in personalTickets" :key="t.id" class="premium-horizontal-ticket">
                <!-- Blurred background image -->
                <img 
                  v-if="t.flights?.airports?.image_url" 
                  :src="t.flights.airports.image_url" 
                  class="ticket-bg-blur" 
                  alt="Destination Backdrop"
                />
                
                <!-- Ticket Content Layer -->
                <div class="ticket-content-layer">
                  <!-- Left Section: Departure Details -->
                  <div class="ticket-col ticket-col-left">
                    <span class="city-name">{{ t.flights?.origin_city || t.flights?.origin }}</span>
                    <span class="airport-code">{{ t.flights?.origin }}</span>
                    <span class="time-text">{{ formatTime(t.flights?.departure_time) }}</span>
                    <span class="date-text">{{ formatDate(t.flights?.departure_time) }}</span>
                  </div>
                  
                  <!-- Center Section: Flight Connection Status Ribbon -->
                  <div class="ticket-col ticket-col-middle">
                    <div class="connection-line">
                      <span class="duration-badge">{{ getDurationString(t.flights?.departure_time, t.flights?.arrival_time) }}</span>
                      <div class="plane-line">
                        <span class="plane-icon">✈️</span>
                      </div>
                      <span class="flight-type-badge">{{ t.seat_class || 'Economy' }}</span>
                    </div>
                  </div>
                  
                  <!-- Right Section: Destination Details & Return path details -->
                  <div class="ticket-col ticket-col-right">
                    <span class="city-name">{{ t.flights?.destination_city || t.flights?.destination }}</span>
                    <span class="airport-code">{{ t.flights?.destination }}</span>
                    <span class="time-text">{{ formatTime(t.flights?.arrival_time) }}</span>
                    
                    <!-- Return path badge if round-trip -->
                    <div v-if="t.trip_type === 'round-trip'" class="return-leg-badge">
                      <span class="badge-label">🔄 Return Leg</span>
                      <span class="badge-val">{{ formatDate(t.return_date) }}</span>
                    </div>
                  </div>
                  
                  <!-- Edge Section: Booking Ref and Price -->
                  <div class="ticket-stub-segment">
                    <div class="stub-divider"></div>
                    <div class="stub-details">
                      <div class="ref-container">
                        <span class="ref-label">BOOKING REF</span>
                        <span class="ref-value">{{ t.booking_reference || ('TRV-' + t.id) }}</span>
                      </div>
                      <div class="price-container">
                        <span class="price-label">TOTAL PAID</span>
                        <span class="price-value">${{ t.total_price }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'security'" class="security-section-wrapper">
          <!-- Security & Authentication Card -->
          <div class="content-card security-card">
            <h2 class="card-title text-start">Security & Authentication</h2>
            <!-- Change Password Section -->
            <div class="change-password-section">
              <h3 class="subsection-title text-start">Change Password</h3>
              <form @submit.prevent="changePassword" class="password-form">
                <div class="form-group full-width text-start">
                  <label for="new-password">New Password</label>
                  <input 
                    type="password" 
                    id="new-password" 
                    v-model="newPassword" 
                    class="form-input" 
                    placeholder="Enter your new password" 
                    required
                  />
                </div>
                <div class="form-group full-width text-start">
                  <label for="confirm-password">Confirm Password</label>
                  <input 
                    type="password" 
                    id="confirm-password" 
                    v-model="confirmPassword" 
                    class="form-input" 
                    placeholder="Confirm your new password" 
                    required
                  />
                </div>
                <div class="form-actions-simple">
                  <button type="submit" class="btn-primary">Save Password</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Delete Account Card -->
          <div class="content-card delete-account-card">
            <div class="delete-account-flex">
              <div class="delete-info text-start">
                <h3 class="delete-title">Delete Account</h3>
                <p class="delete-subtext">Once your account is deleted, you will not be able to restore your account or data.</p>
              </div>
              <button class="delete-btn" @click="showDeleteModal = true">Delete</button>
            </div>
          </div>

          <!-- Delete Confirmation Modal -->
          <div v-if="showDeleteModal" class="modal-overlay">
            <div class="confirm-modal">
              <h3 class="modal-title">Delete Account?</h3>
              <p class="modal-message">Are you sure you want to delete your account? This action cannot be undone and you will lose all bookings, reviews, and profile data.</p>
              <div class="modal-buttons">
                <button class="modal-btn-cancel" @click="showDeleteModal = false">Cancel</button>
                <button class="modal-btn-delete" :disabled="isDeleting" @click="deleteAccount">
                  {{ isDeleting ? 'Deleting...' : 'Delete' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
      
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '../utils/apiClient.js';
import noBookingImg from './no booking.jpg';

const user = ref(JSON.parse(localStorage.getItem('user')) || null);
const route = useRoute();
const router = useRouter();

const profileUsername = ref('');
const profileEmail = ref('');
const profileGender = ref('');
const profileCity = ref('');
const birthDay = ref('1');
const birthMonth = ref('January');
const birthYear = ref('2000');

const newPassword = ref('');
const confirmPassword = ref('');
const showDeleteModal = ref(false);
const isDeleting = ref(false);


const activeTab = ref('account');
const activeSubTab = ref('account'); // Tracks 'account' vs 'bookings'
const personalTickets = ref([]);

const menuItems = ref([
  { name: 'Points (0)', icon: '🪙', active: false },
  { name: 'My Booking', icon: '🎫', active: false },
  { name: 'My Account', icon: '👤', active: true }
]);

const days = Array.from({ length: 31 }, (_, i) => String(i + 1));
const months = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];
const years = Array.from({ length: 100 }, (_, i) => String(new Date().getFullYear() - i));

const userPoints = computed(() => {
  return user.value?.points || 0;
});

const loyaltyTier = computed(() => {
  const points = userPoints.value;
  if (points >= 5000) {
    return {
      name: "Gold Priority",
      class: "gold-tier",
      text: "You're our Gold Priority >",
      icon: "👑",
      discount: 10
    };
  } else if (points >= 2000) {
    return {
      name: "Silver Priority",
      class: "silver-tier",
      text: "You're our Silver Priority >",
      icon: "🥈",
      discount: 5
    };
  } else if (points >= 1000) {
    return {
      name: "Bronze Priority",
      class: "bronze-tier",
      text: "You're our Bronze Priority >",
      icon: "🥉",
      discount: 3
    };
  } else {
    return {
      name: "Explorer",
      class: "explorer-tier",
      text: "Start earning points to level up! >",
      icon: "✈️",
      discount: 0
    };
  }
});

const userInitials = computed(() => {
  if (profileUsername.value) {
    const parts = profileUsername.value.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return profileUsername.value.substring(0, 2).toUpperCase();
  }
  return 'TK';
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

const fetchUserActiveBookings = async () => {
  try {
    const response = await apiClient.get('/bookings/my_summary');
    personalTickets.value = response.data.completed || [];
  } catch (error) {
    console.error('Error fetching bookings:', error);
  }
};

const setActiveMenu = (name) => {
  menuItems.value.forEach(item => {
    item.active = item.name === name;
  });
  if (name === 'My Account') {
    activeSubTab.value = 'account';
    activeTab.value = 'account';
  } else if (name === 'My Booking' || name === 'Đặt chỗ của tôi') {
    activeSubTab.value = 'bookings';
    activeTab.value = 'account';
    fetchUserActiveBookings();
  }
};

const loadUserSettings = async () => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      const parsed = JSON.parse(storedUser);
      user.value = parsed;
      profileUsername.value = parsed.username || '';
      profileEmail.value = parsed.email || '';
      profileGender.value = parsed.gender || '';
      profileCity.value = parsed.city || '';
      birthDay.value = parsed.birthDay || '1';
      birthMonth.value = parsed.birthMonth || 'January';
      birthYear.value = parsed.birthYear || '2000';
    } catch (e) {
      console.error('Failed to parse user from local storage', e);
    }
  }

  try {
    const response = await apiClient.get('/auth/me');
    if (response && response.data && response.data.user_info) {
      const updatedUser = {
        ...user.value,
        ...response.data.user_info
      };
      user.value = updatedUser;
      localStorage.setItem('user', JSON.stringify(updatedUser));
      profileUsername.value = updatedUser.username || '';
      profileEmail.value = updatedUser.email || '';
      if (updatedUser.gender) profileGender.value = updatedUser.gender;
      if (updatedUser.city) profileCity.value = updatedUser.city;
      if (updatedUser.birthDay) birthDay.value = updatedUser.birthDay;
      if (updatedUser.birthMonth) birthMonth.value = updatedUser.birthMonth;
      if (updatedUser.birthYear) birthYear.value = updatedUser.birthYear;
    }
  } catch (error) {
    console.error('Error fetching fresh user settings:', error);
  }
};

const saveProfile = async () => {
  if (!user.value) {
    user.value = {};
  }
  
  const payload = {
    username: profileUsername.value,
    gender: profileGender.value,
    city: profileCity.value,
    birthDay: birthDay.value,
    birthMonth: birthMonth.value,
    birthYear: birthYear.value
  };

  try {
    const response = await apiClient.put('/auth/me', payload);
    if (response.data && response.data.status === 'success') {
      user.value = {
        ...user.value,
        ...response.data.user_info
      };
      localStorage.setItem('user', JSON.stringify(user.value));
      // Dispatch custom storage event for Navbar to update immediately
      window.dispatchEvent(new Event('storage'));
      alert('Profile updated successfully!');
    } else {
      alert('Failed to update profile.');
    }
  } catch (error) {
    console.error('Error saving profile changes:', error);
    alert('An error occurred while saving profile changes.');
  }
};

const resetForm = () => {
  loadUserSettings();
};

const changePassword = async () => {
  if (!newPassword.value || !confirmPassword.value) {
    alert('Please fill in all fields.');
    return;
  }
  if (newPassword.value !== confirmPassword.value) {
    alert('Passwords do not match.');
    return;
  }
  if (newPassword.value.length < 6) {
    alert('Password must be at least 6 characters long.');
    return;
  }

  try {
    const response = await apiClient.put('/auth/password', {
      new_password: newPassword.value
    });
    if (response.data && response.data.status === 'success') {
      alert('Password changed successfully!');
      newPassword.value = '';
      confirmPassword.value = '';
    } else {
      alert('Failed to change password.');
    }
  } catch (error) {
    console.error('Error changing password:', error);
    const msg = error.response?.data?.detail || 'An error occurred while changing password.';
    alert(msg);
  }
};

const deleteAccount = async () => {
  isDeleting.value = true;
  try {
    const response = await apiClient.delete('/auth/me');
    if (response.data && response.data.status === 'success') {
      alert('Your account has been deleted successfully.');
      // Clear session data
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      // Dispatch storage event to update navbar/UI immediately
      window.dispatchEvent(new Event('storage'));
      // Route back to home page
      router.push('/');
    } else {
      alert('Failed to delete account.');
    }
  } catch (error) {
    console.error('Error deleting account:', error);
    alert('An error occurred while deleting your account.');
  } finally {
    isDeleting.value = false;
    showDeleteModal.value = false;
  }
};


const handleTabQuery = () => {
  const tabFromQuery = route.query.tab;
  if (tabFromQuery === 'bookings' || tabFromQuery === 'booking') {
    activeSubTab.value = 'bookings';
    activeTab.value = 'account';
    setActiveMenu('My Booking');
    fetchUserActiveBookings();
  }
};

onMounted(() => {
  loadUserSettings();
  fetchUserActiveBookings();
  handleTabQuery();
  window.addEventListener('storage', loadUserSettings);
});

watch(() => route.query.tab, () => {
  handleTabQuery();
});

onUnmounted(() => {
  window.removeEventListener('storage', loadUserSettings);
});
</script>

<style scoped lang="scss">
.profile-page-wrapper {
  background-color: #f7f9fa;
  min-height: 100vh;
  padding: 40px 0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.profile-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 992px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}

/* Sidebar Styles */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-sidebar-card {
  background: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.avatar-container {
  width: 56px;
  height: 56px;
  flex-shrink: 0;
}

.user-sidebar-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid #e1e1e1;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background-color: #0194F3;
  color: #ffffff;
  font-weight: 700;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-fullname {
  font-size: 1rem;
  font-weight: 600;
  color: #030303;
  margin: 0;
}

.user-subtitle {
  font-size: 0.8rem;
  color: #687176;
  margin-top: 2px;
}

.tier-badge-container {
  position: relative; /* Crucial for absolute positioning of tooltip */
  border-radius: 8px;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  .badge-text {
    color: #ffffff;
  }

  &:hover {
    .tier-tooltip {
      visibility: visible;
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }
}

.tier-tooltip {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: #1e293b;
  color: #ffffff;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
  z-index: 100;
  width: 220px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);

  .tooltip-arrow {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 6px;
    border-style: solid;
    border-color: #1e293b transparent transparent transparent;
  }

  .tooltip-header {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 4px;
  }

  .tooltip-body {
    font-size: 0.85rem;
    font-weight: 500;
    color: #f1f5f9;
    line-height: 1.4;
  }

  .discount-value-highlight {
    color: #4ade80 !important; /* Green color */
    font-weight: 700;
    font-size: 1rem;
    text-shadow: 0 0 8px rgba(74, 222, 128, 0.6); /* Slightly glowing green */
    display: inline-block;
  }
}

.tier-badge-container.bronze-tier {
  background: linear-gradient(135deg, #cd7f32, #a05822);
  border: 1px solid #80400b;
  &:hover {
    background: linear-gradient(135deg, #dd8f42, #b06832);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(160, 88, 34, 0.25);
  }
}

.tier-badge-container.silver-tier {
  background: linear-gradient(135deg, #94a3b8, #475569);
  border: 1px solid #334155;
  &:hover {
    background: linear-gradient(135deg, #a8b8cc, #5c6b80);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(71, 85, 105, 0.25);
  }
}

.tier-badge-container.gold-tier {
  background: linear-gradient(135deg, #fbbf24, #d97706);
  border: 1px solid #b45309;
  &:hover {
    background: linear-gradient(135deg, #fcd34d, #ea580c);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25);
  }
}

.tier-badge-container.explorer-tier {
  background: linear-gradient(135deg, #4ade80, #16a34a);
  border: 1px solid #15803d;
  &:hover {
    background: linear-gradient(135deg, #86efac, #15803d);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
  }
}

.badge-icon {
  font-size: 1.1rem;
}

.badge-text {
  font-size: 0.85rem;
  font-weight: 600;
}

.sidebar-nav {
  background: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 12px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav li {
  margin: 4px 12px;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  text-decoration: none;
  border-radius: 8px;
  color: #687176;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.sidebar-nav a:hover {
  background: #f7f9fa;
  color: #030303;
}

.sidebar-nav li.active a {
  background-color: #0194F3;
  color: #ffffff;
}

/* Main Content Styles */
.profile-main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.main-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #030303;
  margin: 0;
}

.section-tabs {
  display: flex;
  border-bottom: 1px solid #e1e1e1;
  gap: 24px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 12px 4px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #687176;
  cursor: pointer;
  position: relative;
  transition: color 0.2s ease;
}

.tab-btn:hover {
  color: #030303;
}

.tab-btn.active {
  color: #0194F3;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #0194F3;
  border-radius: 3px 3px 0 0;
}

.content-card {
  background: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #030303;
  margin-top: 0;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f2f2f2;
}

.personal-data-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group.full-width {
  width: 100%;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 16px;
}

@media (max-width: 576px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #030303;
}

.form-input, .form-select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #ffffff;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-input:focus, .form-select:focus {
  border-color: #0194F3;
  box-shadow: 0 0 0 3px rgba(1, 148, 243, 0.12);
}

.form-input:disabled {
  background-color: #f7f9fa;
  color: #909697;
  cursor: not-allowed;
}

.helper-text {
  font-size: 0.8rem;
  color: #687176;
  margin-top: 2px;
}

.birthdate-selects {
  display: flex;
  gap: 8px;
}

.day-select {
  width: 80px;
}

.month-select {
  flex: 2;
}

.year-select {
  width: 100px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 12px;
  padding-top: 20px;
  border-top: 1px solid #f2f2f2;
}

.btn-primary {
  background-color: #0194F3;
  color: #ffffff;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: #007ccb;
}

.btn-secondary {
  background-color: transparent;
  color: #0194F3;
  font-weight: 700;
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background-color: #f0f8ff;
}

.security-placeholder-text {
  color: #687176;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Switch toggle styling */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e2e8f0;
  transition: .3s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
}
input:checked + .slider {
  background-color: #0194F3;
}
input:checked + .slider:before {
  transform: translateX(20px);
}
.slider.round {
  border-radius: 24px;
}
.slider.round:before {
  border-radius: 50%;
}

.security-section-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.security-option-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
}
.option-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.option-label {
  font-size: 1rem;
  font-weight: 600;
  color: #030303;
}
.option-subtext {
  font-size: 0.85rem;
  color: #687176;
}
.security-divider {
  border: 0;
  height: 1px;
  background-color: #e1e1e1;
  margin: 16px 0;
}
.change-password-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}
.subsection-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #030303;
  margin: 0 0 8px 0;
}
.password-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-actions-simple {
  display: flex;
  justify-content: flex-start;
  margin-top: 8px;
}

.delete-account-card {
  border: 1px solid #fecaca;
  background-color: #fffafb;
}
.delete-account-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}
.delete-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ef4444;
  margin: 0;
}
.delete-subtext {
  font-size: 0.9rem;
  color: #687176;
  margin: 4px 0 0 0;
}
.delete-btn {
  background-color: transparent;
  color: #0194F3;
  font-weight: 700;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  padding: 8px 16px;
  transition: color 0.2s ease;
}
.delete-btn:hover {
  color: #007ccb;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}
.confirm-modal {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  text-align: center;
  animation: scaleIn 0.2s ease-out;
}
.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin-top: 0;
  margin-bottom: 12px;
}
.modal-message {
  font-size: 0.95rem;
  color: #475569;
  line-height: 1.5;
  margin-bottom: 24px;
}
.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.modal-btn-cancel {
  background-color: #ffffff;
  color: #64748b;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.modal-btn-cancel:hover {
  border-color: #0194F3;
  color: #0194F3;
  box-shadow: 0 0 8px rgba(1, 148, 243, 0.4);
}
.modal-btn-delete {
  background-color: #ef4444;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.modal-btn-delete:hover {
  background-color: #dc2626;
}
.modal-btn-delete:disabled {
  background-color: #fca5a5;
  cursor: not-allowed;
}

.text-start {
  text-align: start;
}

@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}


/* Premium Tickets Dashboard & Perforated Ticket Styling */
.traveloka-mini-dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.no-bookings-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background-color: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
  text-align: center;
  gap: 12px;
}

.sleepy-folder-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 48px 24px;
  
  .sleepy-folder-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 2s infinite ease-in-out;
  }
  
  .banner-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.5rem;
  }
  
  .banner-text {
    font-size: 0.9rem;
    color: #64748b;
    max-width: 420px;
    line-height: 1.5;
  }
}

.new-no-bookings-banner {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background-color: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
  text-align: left;

  .no-booking-img {
    width: 140px;
    height: 140px;
    object-fit: cover;
    border-radius: 8px;
    flex-shrink: 0;
  }

  .no-bookings-text-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .banner-title {
    font-size: 1.25rem;
    color: #1e293b;
    margin: 0;
  }

  .banner-text {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
    margin: 0;
  }
}

@media (max-width: 600px) {
  .new-no-bookings-banner {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
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
  padding: 1.5rem;
  min-height: 135px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e2e8f0;
}

/* Perforated side cuts styling design specs */
.premium-horizontal-ticket::before,
.premium-horizontal-ticket::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 18px;
  height: 18px;
  background-color: #f7f9fa; /* Synchronized to match page background #f7f9fa */
  border-radius: 50%;
  transform: translateY(-50%);
  z-index: 10;
  border: 1px solid #e2e8f0;
}
.premium-horizontal-ticket::before { left: -10px; }
.premium-horizontal-ticket::after { right: -10px; }

/* Blurred overlay background styling wrapper */
.ticket-bg-blur {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0.14;
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
  font-weight: 500;
}

.connection-line {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.duration-badge {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  background-color: #f1f5f9;
  padding: 4px 8px;
  border-radius: 12px;
  margin-bottom: 6px;
}

.plane-line {
  width: 100%;
  height: 2px;
  background: repeating-linear-gradient(to right, #cbd5e1 0, #cbd5e1 4px, transparent 4px, transparent 8px);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 8px 0;
}

.plane-icon {
  position: absolute;
  background: white;
  padding: 0 8px;
  font-size: 1rem;
}

.flight-type-badge {
  font-size: 0.75rem;
  font-weight: 700;
  color: #0194F3;
  border: 1px solid #0194F3;
  padding: 2px 8px;
  border-radius: 10px;
  text-transform: uppercase;
  margin-top: 6px;
}

.return-leg-badge {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 6px 10px;
  border-radius: 8px;
  margin-top: 8px;
  
  .badge-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #166534;
    text-transform: uppercase;
  }
  
  .badge-val {
    font-size: 0.8rem;
    font-weight: 600;
    color: #14532d;
  }
}

.ticket-stub-segment {
  display: flex;
  align-items: center;
  flex: 3;
  padding-left: 24px;
}

.stub-divider {
  width: 1px;
  height: 90px;
  border-left: 2px dashed #e2e8f0;
  margin-right: 24px;
}

.stub-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.ref-container, .price-container {
  display: flex;
  flex-direction: column;
}

.ref-label, .price-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

.ref-value {
  font-family: monospace;
  font-size: 0.95rem;
  font-weight: 700;
  color: #334155;
}

.price-value {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 0.8; }
}

@media (max-width: 768px) {
  .ticket-content-layer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .ticket-col-right {
    align-items: flex-start;
    text-align: left;
  }
  
  .return-leg-badge {
    align-items: flex-start;
  }
  
  .ticket-stub-segment {
    padding-left: 0;
  }
  
  .stub-divider {
    display: none;
  }
  
  .premium-horizontal-ticket::before,
  .premium-horizontal-ticket::after {
    display: none;
  }
}
</style>
