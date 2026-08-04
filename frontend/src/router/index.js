import { createRouter, createWebHistory } from 'vue-router';
import Flights from '../views/Flights.vue';
import BookingView from '../views/BookingView.vue';
import AdminView from '../views/AdminView.vue';
import ProfileHistory from '../views/ProfileHistory.vue';

import SignInView from '../views/SignInView.vue';
import FlightHistoryView from '../views/FlightHistoryView.vue';
import YourTicketView from '../views/YourTicketView.vue';

const routes = [
  {
    path: '/',
    name: 'Cover',
    component: () => import('../views/Home.vue'),
    meta: {
      title: 'Welcome to Traveloka'
    }
  },
  {
    path: '/flights',
    name: 'Home',
    component: Flights,
    meta: {
      title: 'Traveloka Flight Booking - Search & Book Flights'
    }
  },
  {
    path: '/booking',
    name: 'Booking',
    component: BookingView,
    meta: {
      title: 'My Bookings - Traveloka'
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: {
      title: 'Admin Dashboard - Traveloka'
    }
  },
  {
    path: '/profile',
    name: 'ProfileHistory',
    component: ProfileHistory,
    meta: {
      title: 'My Profile - Traveloka'
    }
  },
  {
    path: '/flighthistory',
    name: 'FlightHistory',
    component: FlightHistoryView,
    meta: {
      title: 'Flight History - Traveloka'
    }
  },
  {
    path: '/your-tickets',
    name: 'YourTickets',
    component: YourTicketView,
    meta: {
      title: 'Your Tickets - Traveloka'
    }
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: SignInView,
    meta: {
      title: 'Sign In - Traveloka'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: {
      title: 'Register - Traveloka'
    }
  },
  {
    path: '/admin/booking-distribution',
    name: 'AdminRegionalBookings',
    component: () => import('../views/AdminRegionalBookingsView.vue'),
    meta: {
      title: 'Booking Distribution - Traveloka'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue'),
    meta: {
      title: 'About Us - Traveloka'
    }
  },
  {
    path: '/news',
    name: 'News',
    component: () => import('../views/NewsView.vue'),
    meta: {
      title: 'Aviation Journal & Insights - Traveloka'
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
});

router.beforeEach((to, from, next) => {
  let hasActiveToken = !!localStorage.getItem('authToken');
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      const parsed = JSON.parse(storedUser);
      if (parsed && (parsed.access_token || parsed.token)) {
        hasActiveToken = true;
      }
    } catch (e) {}
  }

  if (to.path === '/flighthistory') {
    if (hasActiveToken) {
      next();
    } else {
      next('/signin');
    }
  } else {
    next();
  }
});

// Update page title on route change
router.afterEach((to) => {
  document.title = to.meta.title || 'Traveloka Flight Booking';
});

export default router;
