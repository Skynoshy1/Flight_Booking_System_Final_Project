<template>
  <div id="app" class="app-container">
    <Navbar />
    <router-view v-slot="{ Component }">
      <transition name="page-fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import Navbar from './components/common/Navbar.vue';
import Footer from './components/common/Footer.vue';

onMounted(() => {
  console.log('✈️ Traveloka Flight Booking System initialized');
});
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-container {
  flex: 1;
}

/* Page Transition Animation */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}

.page-fade-enter-to,
.page-fade-leave-from {
  opacity: 1;
}
</style>

<style>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');
/* Global Styles - Traveloka Flight Booking System */
:root {
  --primary-blue: #0194F3;
  --primary-orange: #FF5E1F;
  --sky-bg: #FAF4EE; /* Light brown/beige background */
  --dark-text: #03121A;
  --gray-text: #4B5563;
  --light-gray: #9CA3AF;
  --white: #FFFFFF;
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --transition-base: 0.2s ease-in-out;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  background-color: var(--sky-bg) !important;
  color: var(--dark-text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: var(--sky-bg);
}

::-webkit-scrollbar-thumb {
  background: #B0BEC5;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #78909C;
}

/* Global Page Layout Adaptations to Editorial Containers */

/* HomeView Page Layout */
.home-view {
  background-color: var(--sky-bg) !important;
  padding: 4rem 1.5rem !important;
  min-height: 100vh;
}
.home-view .hero-section {
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1360px !important;
  margin: 0 auto 3rem !important;
  padding: 4rem 1rem 3rem 1rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.home-view .results-section {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1140px;
  margin: 0 auto 3rem !important;
  padding: 3rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.home-view .hero-section:hover,
.home-view .results-section:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}

/* BookingView Page Layout */
.booking-view {
  background-color: var(--sky-bg) !important;
  padding: 4rem 1.5rem !important;
  min-height: 100vh;
}
.booking-view .booking-header,
.booking-view .booking-content {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1140px;
  margin: 0 auto 3rem !important;
  padding: 3rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.booking-view .booking-header:hover,
.booking-view .booking-content:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}

/* AdminView Page Layout */
.admin-view {
  background-color: var(--sky-bg) !important;
  padding: 4rem 1.5rem !important;
  min-height: 100vh;
}
.admin-view .admin-header,
.admin-view .admin-content {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1140px;
  margin: 0 auto 3rem !important;
  padding: 3rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.admin-view .admin-header:hover,
.admin-view .admin-content:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}

/* AdminRegionalBookingsView (Booking Distribution) Layout */
.regional-analytics-container {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1140px;
  margin: 4rem auto !important;
  padding: 3rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.regional-analytics-container:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}

/* FlightHistoryView & YourTicketView Layout */
.flight-history-container {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1140px;
  margin: 4rem auto !important;
  padding: 3rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.flight-history-container:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}

/* ProfileHistory Layout */
.profile-page-wrapper {
  background-color: var(--sky-bg) !important;
  padding: 4rem 1.5rem !important;
  min-height: 100vh;
}
.profile-container {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  max-width: 1140px;
  margin: 0 auto !important;
  padding: 3rem !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.profile-container:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}

/* SignIn & Register Cards */
.signin-container, .register-container {
  background-color: var(--sky-bg) !important;
  min-height: 100vh;
  padding: 4rem 1.5rem !important;
}
.signin-card, .register-card {
  background-color: var(--white) !important;
  border: 2px solid var(--dark-text) !important;
  border-radius: 24px !important;
  box-shadow: 6px 6px 0px var(--dark-text), 0px 0px 25px rgba(1, 148, 243, 0.12) !important;
  transition: box-shadow 0.3s ease;
}
.signin-card:hover, .register-card:hover {
  box-shadow: 8px 8px 0px var(--dark-text), 0px 0px 30px rgba(1, 148, 243, 0.18) !important;
}
</style>
