<template>
  <nav class="navbar-traveloka">
    <div class="container">
      <div class="navbar-content">
        <!-- Logo -->
        <router-link to="/" class="navbar-brand">
          <div class="logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="16" fill="#0194F3"/>
              <path d="M16 8L22 14L16 20L10 14L16 8Z" fill="white"/>
            </svg>
            <span class="brand-name">Tika</span>
          </div>
        </router-link>

        <!-- Navigation Links -->
        <div class="nav-links">
          <router-link to="/flights" class="nav-link" active-class="active">
            <i class="icon">✈️</i>
            <span>Flights</span>
          </router-link>
          <router-link 
            v-if="isAdmin" 
            to="/admin/booking-distribution" 
            class="nav-link"
            active-class="active"
          >
            <i class="icon">📊</i>
            <span>Booking Distribution</span>
          </router-link>
          <router-link 
            v-else 
            to="/booking" 
            class="nav-link"
            active-class="active"
          >
            <i class="icon">🎫</i>
            <span>My Bookings</span>
          </router-link>
          <router-link to="/about" class="nav-link" active-class="active">
            <i class="icon">ℹ️</i>
            <span>About</span>
          </router-link>
          <router-link to="/news" class="nav-link" active-class="active">
            <i class="icon">📰</i>
            <span>News</span>
          </router-link>
          <router-link v-if="isAdmin" to="/admin" class="nav-link" active-class="active">
            <i class="icon">⚙️</i>
            <span>Admin</span>
          </router-link>
        </div>

        <!-- Mobile Hamburger Button -->
        <button class="mobile-toggle-btn" @click="isMobileMenuOpen = !isMobileMenuOpen" aria-label="Toggle navigation">
          <span class="hamburger-bar"></span>
          <span class="hamburger-bar"></span>
          <span class="hamburger-bar"></span>
        </button>

        <!-- Right Section -->
        <div class="navbar-right">
          <!-- Geolocation Widget -->
          <div class="location-widget">
            <i class="icon">📍</i>
            <span class="location-text">{{ nearestAirport }}</span>
          </div>

          <!-- User Profile -->
          <div class="user-profile">
            <template v-if="!user">
              <router-link to="/signin" class="profile-btn">
                <i class="icon">👤</i>
                <span>Sign In</span>
              </router-link>
            </template>
            <template v-else>
              <div 
                class="profile-dropdown-container"
                :class="{ 'is-active': isDropdownOpen }"
                @mouseenter="isDropdownOpen = true"
                @mouseleave="isDropdownOpen = false"
                @click="isDropdownOpen = !isDropdownOpen"
              >
                <div class="user-info-trigger">
                  <div class="avatar-circle">
                    <img v-if="user.avatar_url" :src="user.avatar_url" class="user-avatar-img" alt="Avatar" />
                    <template v-else>✈️</template>
                  </div>
                  <span class="username">{{ user.username }}</span>
                  <i class="chevron">▼</i>
                </div>
                <div class="dropdown-menu">
                  <div class="dropdown-header" :style="loyaltyTier.style">
                    <h4 class="dropdown-user-name">{{ user.username || 'Explorer' }}</h4>
                    <span class="dropdown-priority-text">
                      <span class="header-badge-icon">{{ loyaltyTier.icon }}</span>
                      {{ loyaltyTier.text }} &gt;
                    </span>
                  </div>
                  <div class="dropdown-item points-item">
                    <i class="icon">🪙</i>
                    <span class="points-label">{{ userPoints }} Points</span>
                  </div>
                  <router-link to="/profile" class="dropdown-item">
                    <i class="icon">👤</i>
                    <span>My Profile</span>
                  </router-link>
                  <router-link to="/profile?tab=bookings" class="dropdown-item">
                    <i class="icon">🎫</i>
                    <span>My Booking</span>
                  </router-link>
                   <router-link to="/your-tickets" class="dropdown-item">
                    <i class="icon">🎫</i>
                    <span>Your Ticket</span>
                  </router-link>
                  <router-link to="/flighthistory" class="dropdown-item">
                    <i class="icon">📜</i>
                    <span>Flight History</span>
                  </router-link>
                  <button @click="logout" class="dropdown-item sign-out-btn">
                    <i class="icon">🚪</i>
                    <span>Log Out</span>
                  </button>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Mobile Off-Canvas Drawer -->
      <transition name="slide-down">
        <div v-if="isMobileMenuOpen" class="mobile-drawer">
          <div class="mobile-nav-links">
            <router-link to="/flights" class="mobile-nav-link" @click="isMobileMenuOpen = false">
              <i class="icon">✈️</i> Flights
            </router-link>
            <router-link v-if="isAdmin" to="/admin/booking-distribution" class="mobile-nav-link" @click="isMobileMenuOpen = false">
              <i class="icon">📊</i> Booking Distribution
            </router-link>
            <router-link v-else to="/booking" class="mobile-nav-link" @click="isMobileMenuOpen = false">
              <i class="icon">🎫</i> My Bookings
            </router-link>
            <router-link to="/about" class="mobile-nav-link" @click="isMobileMenuOpen = false">
              <i class="icon">ℹ️</i> About
            </router-link>
            <router-link to="/news" class="mobile-nav-link" @click="isMobileMenuOpen = false">
              <i class="icon">📰</i> News
            </router-link>
            <router-link v-if="isAdmin" to="/admin" class="mobile-nav-link" @click="isMobileMenuOpen = false">
              <i class="icon">⚙️</i> Admin
            </router-link>
          </div>
        </div>
      </transition>
    </div>
  </nav>

</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../../utils/apiClient.js';

const nearestAirport = ref('SGN - Ho Chi Minh');
const user = ref(null);
const router = useRouter();
const isDropdownOpen = ref(false);
const isMobileMenuOpen = ref(false);


const userPoints = computed(() => {
  return user.value?.points || 0;
});

const loyaltyTier = computed(() => {
  const points = userPoints.value;
  if (points >= 5000) {
    return {
      name: "Gold Priority",
      class: "gold-tier",
      text: "You're our Gold Priority",
      icon: "👑",
      style: "background: linear-gradient(135deg, #fbbf24, #d97706); color: #ffffff;"
    };
  } else if (points >= 2000) {
    return {
      name: "Silver Priority",
      class: "silver-tier",
      text: "You're our Silver Priority",
      icon: "🥈",
      style: "background: linear-gradient(135deg, #94a3b8, #475569); color: #ffffff;"
    };
  } else if (points >= 1000) {
    return {
      name: "Bronze Priority",
      class: "bronze-tier",
      text: "You're our Bronze Priority",
      icon: "🥉",
      style: "background: linear-gradient(135deg, #cd7f32, #a05822); color: #ffffff;"
    };
  } else {
    return {
      name: "Explorer",
      class: "explorer-tier",
      text: "Explorer Tier",
      icon: "✈️",
      style: "background: linear-gradient(135deg, #4ade80, #16a34a); color: #ffffff;"
    };
  }
});

const alertPlaceholder = (section) => {
  alert(`${section} section will be available soon!`);
};

const isAdmin = computed(() => {
  if (!user.value) return false;
  return user.value.role === 'admin' || user.value.user_metadata?.role === 'admin' || user.value.user?.role === 'admin';
});

const checkUser = async () => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      const parsed = JSON.parse(storedUser);
      if (parsed && parsed.access_token) {
        user.value = parsed;
        
        // Fetch fresh profile data including points
        try {
          const response = await apiClient.get('/auth/me');
          if (response && response.data && response.data.user_info) {
            const updatedUser = {
              ...user.value,
              ...response.data.user_info
            };
            user.value = updatedUser;
            localStorage.setItem('user', JSON.stringify(updatedUser));
          }
        } catch (error) {
          console.error('Error fetching user points in Navbar:', error);
        }
      } else {
        localStorage.removeItem('user');
        user.value = null;
      }
    } catch (e) {
      localStorage.removeItem('user');
      user.value = null;
    }
  } else {
    user.value = null;
  }
};

const logout = () => {
  localStorage.removeItem('user');
  user.value = null;
  router.push('/');
};

onMounted(() => {
  const cachedAirport = localStorage.getItem('user_nearest_airport');
  if (cachedAirport) {
    nearestAirport.value = cachedAirport;
  } else {
    fetch('https://ipapi.co/json/')
      .then(res => res.json())
      .then(data => {
        const country = (data.country_name || '').toLowerCase();
        const city = (data.city || '').toLowerCase();
        if (country.includes('vietnam') || city.includes('ho chi minh') || city.includes('saigon')) {
          nearestAirport.value = 'SGN - Ho Chi Minh';
        } else if (city.includes('hanoi')) {
          nearestAirport.value = 'HAN - Hanoi';
        } else if (country.includes('singapore')) {
          nearestAirport.value = 'SIN - Singapore';
        } else if (country.includes('thailand') || city.includes('bangkok')) {
          nearestAirport.value = 'BKK - Bangkok';
        } else {
          nearestAirport.value = 'SGN - Ho Chi Minh';
        }
        localStorage.setItem('user_nearest_airport', nearestAirport.value);
      })
      .catch(err => {
        console.error('IP Geolocation failed:', err);
        nearestAirport.value = 'SGN - Ho Chi Minh';
        localStorage.setItem('user_nearest_airport', nearestAirport.value);
      });
  }

  checkUser();
  window.addEventListener('storage', checkUser);
});

onUnmounted(() => {
  window.removeEventListener('storage', checkUser);
});
</script>

<style scoped lang="scss">
@import '@/assets/scss/variables.scss';

.navbar-traveloka {
  background: $white;
  box-shadow: $shadow-md;
  position: sticky;
  top: 0;
  z-index: 100;
  padding: $spacing-md 0;
  overflow: visible !important;
}

.container {
  overflow: visible !important;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: $spacing-xl;
  overflow: visible !important;
}

.navbar-brand {
  text-decoration: none;
  
  .logo {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    
    .brand-name {
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: $traveloka-blue;
    }
  }
}

.nav-links {
  display: flex;
  gap: $spacing-lg;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-sm $spacing-md;
  border-radius: $border-radius-md;
  text-decoration: none;
  color: $gray-text;
  font-weight: $font-weight-medium;
  transition: all $transition-base;

  .icon {
    font-size: $font-size-lg;
  }

  &:hover {
    background: $sky-blue-bg;
    color: $traveloka-blue;
  }

  &.active {
    background: $traveloka-blue;
    color: $white;
  }
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  overflow: visible !important;
}

.user-profile {
  overflow: visible !important;
}

.location-widget {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-sm $spacing-md;
  background: $sky-blue-bg;
  border-radius: $border-radius-md;
  font-size: $font-size-sm;
  color: $dark-text;

  .icon {
    font-size: $font-size-base;
  }

  .location-text {
    font-weight: $font-weight-medium;
  }
}

.profile-btn {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-sm $spacing-lg;
  background: $traveloka-orange;
  color: $white;
  border: none;
  border-radius: $border-radius-md;
  font-weight: $font-weight-semibold;
  cursor: pointer;
  transition: all $transition-base;
  text-decoration: none;

  .icon {
    font-size: $font-size-lg;
  }

  &:hover {
    background: darken($traveloka-orange, 8%);
    transform: translateY(-2px);
    box-shadow: $shadow-md;
  }
}

.profile-dropdown-container {
  position: relative;
  display: inline-block;
  overflow: visible !important;

  &:hover {
    .user-info-trigger {
      background: #f0fdf4;
    }
    .dropdown-menu {
      display: block !important;
      opacity: 1 !important;
      visibility: visible !important;
    }
  }
}

.user-info-trigger {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-md;
  border-radius: $border-radius-pill;
  cursor: pointer;
  transition: all $transition-base;
  border: 1px solid rgba(0, 0, 0, 0.05);

  .avatar-circle {
    width: 32px;
    height: 32px;
    background: $traveloka-blue;
    color: $white;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: $font-size-sm;
    overflow: hidden;
  }

  .user-avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }

  .username {
    font-weight: $font-weight-semibold;
    color: $dark-text;
    font-size: $font-size-sm;
  }

  .chevron {
    font-size: 10px;
    color: $gray-text;
    transition: transform $transition-base;
  }
}

.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  background: #ffffff;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  min-width: 240px;
  z-index: 9999;
  pointer-events: auto;
  overflow: hidden;
  padding: 0;

  &::before {
    content: '';
    position: absolute;
    top: -20px;
    left: 0;
    width: 100%;
    height: 20px;
    background: transparent;
  }

  .dropdown-header {
    padding: 16px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    gap: 4px;
    box-sizing: border-box;

    .dropdown-user-name {
      margin: 0;
      font-size: 1rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.2;
    }

    .dropdown-priority-text {
      font-size: 0.8rem;
      font-weight: 600;
      color: rgba(255, 255, 255, 0.95);
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 2px;
    }

    .header-badge-icon {
      font-size: 0.9rem;
    }
  }

  .dropdown-item {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    padding: $spacing-sm $spacing-md;
    text-decoration: none;
    color: $dark-text;
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    background: none;
    border: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    box-sizing: border-box;
    transition: background-color $transition-fast;

    &:hover {
      background: $sky-blue-bg;
      color: $traveloka-blue;
    }

    &.points-item {
      border-bottom: 1px solid rgba(0, 0, 0, 0.05);
      cursor: default !important;
      background: #f8fafc !important;
      color: #0f172a !important;
      font-weight: 600 !important;
      
      &:hover {
        background: #f8fafc !important;
        color: #0f172a !important;
      }
    }

    &.sign-out-btn {
      border-top: 1px solid rgba(0, 0, 0, 0.05);
      color: $error;

      &:hover {
        background: #FEF2F2;
        color: $error;
      }
    }
  }
}

.mobile-toggle-btn {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 28px;
  height: 20px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;

  .hamburger-bar {
    width: 100%;
    height: 3px;
    background-color: $dark-text;
    border-radius: 2px;
    transition: all $transition-fast;
  }
}

.mobile-drawer {
  display: block;
  background: #ffffff;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border-radius: 0 0 16px 16px;

  .mobile-nav-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .mobile-nav-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: $dark-text;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 8px;
    transition: background $transition-fast;

    &:hover, &.router-link-active {
      background: $sky-blue-bg;
      color: $traveloka-blue;
    }
  }
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease-out;
}
.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: $breakpoint-lg) {
  .nav-links {
    display: none;
  }

  .mobile-toggle-btn {
    display: flex;
  }
}

@media (max-width: $breakpoint-md) {
  .location-widget {
    padding: 4px 8px;
    background: rgba(1, 148, 243, 0.05);
    border-radius: 20px;
    gap: 2px;
  }
  
  .location-widget .location-text {
    font-size: 0.75rem;
    max-width: 90px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .profile-btn span {
    display: none;
  }
}

</style>

