<template>
  <div class="cover-page-wrapper">
    <!-- Main Cover Section -->
    <main class="cover-container">
      <div class="cover-grid">
        <!-- Left content column -->
        <div class="content-col">
          <!-- Top Badge -->
          <div class="badge-pill">
            <span class="shield-icon">
              <svg width="14" height="16" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 0L0 3V8C0 12.3 3.0 16 7 16C11 16 14 12.3 14 8V3L7 0ZM5.6 11.4L2.8 8.6L4.2 7.2L5.6 8.6L9.8 4.4L11.2 5.8L5.6 11.4Z" fill="#FF5E1F"/>
              </svg>
            </span>
            <span class="badge-text">Licensed & Insured in All 50 States</span>
          </div>

          <!-- Main Hero Title -->
          <h1 class="hero-title">
            <span class="title-line-1">Moving Made</span>
            <div class="flip-container">
              <transition name="flip" mode="out-in">
                <span :key="currentQuote" class="title-line-2">{{ currentQuote }}</span>
              </transition>
            </div>
          </h1>

          <!-- Description -->
          <p class="hero-description">
            From local domestic routes to international journeys, our smart booking system handles all the details so you can focus on enjoying your trip.
          </p>

          <!-- Call to Action Buttons -->
          <div class="cta-buttons">
            <router-link to="/flights" class="btn-primary-cta">
              Book Your Flight! <span class="arrow-icon">→</span>
            </router-link>
            
            <a href="tel:+840867902406" class="btn-secondary-cta">
              <span class="phone-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20.01 15.38C18.78 15.38 17.59 15.18 16.48 14.82C16.13 14.7 15.74 14.79 15.47 15.06L13.9 17.03C11.07 15.68 8.42 13.13 7.01 10.2L8.96 8.54C9.23 8.26 9.31 7.87 9.2 7.52C8.83 6.41 8.64 5.22 8.64 3.99C8.64 3.45 8.19 3 7.65 3H4.19C3.65 3 3 3.24 3 3.99C3 13.28 10.73 21 20.01 21C20.72 21 21 20.37 21 19.82V16.37C21 15.83 20.55 15.38 20.01 15.38Z" fill="#3B82F6"/>
                </svg>
              </span>
              Call (84) 0867902406
            </a>
          </div>

          <!-- Statistics Section -->
          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-number">{{ flightCount }}+</div>
              <div class="stat-label">Flights Available</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">98%</div>
              <div class="stat-label">Satisfaction Rate</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">10+</div>
              <div class="stat-label">Years Experience</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">Always</div>
              <div class="stat-label">Available</div>
            </div>
          </div>
        </div>

        <!-- Right image column -->
        <div class="image-col">
          <div class="image-wrapper">
            <img 
              src="https://www.thestartupfounder.com/wp-content/uploads/2023/08/Global-Commercial-Aircraft-Collision-Avoidance-Systems-ACAS-Market-1024x582-1.jpg" 
              alt="Global Commercial Aircraft" 
              class="hero-image"
            />
            <!-- Floating Badge -->
            <div class="floating-badge">
              <span class="badge-icon-check">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" fill="#10B981"/>
                </svg>
              </span>
              <div class="badge-info">
                <div class="badge-title">Fully Insured</div>
                <div class="badge-desc">All bookings secured</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Wave Divider -->
    <div class="wave-container">
      <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Background filled wave -->
        <path d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z" 
              :fill="isSectionVisible ? '#F5EDE4' : 'var(--sky-bg)'" 
              style="transition: fill 3s ease;" />
        <!-- Curved Border Line -->
        <path d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64" 
              stroke="var(--dark-text)" 
              stroke-width="2.5" 
              stroke-linecap="round" />
      </svg>
    </div>

    <!-- Services Section -->
    <section class="services-section" ref="servicesSectionRef" :class="{ 'is-active': isSectionVisible }">
      <!-- Animated Flying Planes (flying behind content) -->
      <div class="flying-plane plane-orange" :class="{ 'fly-away': isSectionVisible }">
        <svg width="150" height="150" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z" fill="#FF5E1F"/>
        </svg>
      </div>
      <div class="flying-plane plane-blue" :class="{ 'fly-away': isSectionVisible }">
        <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z" fill="#0194F3"/>
        </svg>
      </div>
      <div class="flying-plane plane-teal" :class="{ 'fly-away': isSectionVisible }">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 16V14L13 9V3.5C13 2.67 12.33 2 11.5 2C10.67 2 10 2.67 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5L21 16Z" fill="#10B981"/>
        </svg>
      </div>

      <div class="services-container">
        <div class="services-header">
          <span class="services-badge">Services</span>
          <h2 class="services-title">Flight Solutions for Every Journey</h2>
          <p class="services-subtitle">
            Whether you are traveling for business, family, or adventure, we have the features and care to get you there comfortably.
          </p>
        </div>

        <div class="services-grid">
          <!-- Card 1 -->
          <div class="service-card">
            <div class="service-icon-wrapper">
              <span class="service-icon">✈️</span>
            </div>
            <h3 class="service-card-title">Domestic Flights</h3>
            <p class="service-card-text">
              Quick weekend getaways or city trips. We connect all major domestic hubs with daily direct flights and priority scheduling.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="service-card">
            <div class="service-icon-wrapper">
              <span class="service-icon">🌐</span>
            </div>
            <h3 class="service-card-title">International Routes</h3>
            <p class="service-card-text">
              Fly worldwide with our global partner network. Find multi-city deals and long-haul comfort with premium flag carriers.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="service-card">
            <div class="service-icon-wrapper">
              <span class="service-icon">👥</span>
            </div>
            <h3 class="service-card-title">Group Travel</h3>
            <p class="service-card-text">
              Planning a corporate retreat, sports tour, or family reunion? Get customized quotes and flexible booking policies.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="service-card">
            <div class="service-icon-wrapper">
              <span class="service-icon">💺</span>
            </div>
            <h3 class="service-card-title">Seat Selection</h3>
            <p class="service-card-text">
              Choose your perfect seat. From extra legroom in Business and Premium classes to forward seats for faster boarding.
            </p>
          </div>

          <!-- Card 5 -->
          <div class="service-card">
            <div class="service-icon-wrapper">
              <span class="service-icon">🎒</span>
            </div>
            <h3 class="service-card-title">Baggage & Extras</h3>
            <p class="service-card-text">
              Add extra checked bags, travel insurance protection, or pre-book gourmet meals easily during your booking check-out.
            </p>
          </div>

          <!-- Card 6 -->
          <div class="service-card">
            <div class="service-icon-wrapper">
              <span class="service-icon">🛡️</span>
            </div>
            <h3 class="service-card-title">Refunds & Reschedule</h3>
            <p class="service-card-text">
              Plans change, and we understand. Enjoy peace of mind with our easy refund applications and flexible rescheduling policies.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="steps-section">
      <div class="steps-container">
        <div class="steps-header">
          <span class="steps-badge">How It Works</span>
          <h2 class="steps-title">Your Flight in 4 Easy Steps</h2>
          <p class="steps-subtitle">
            We have streamlined the flight booking process to make it as simple and transparent as possible.
          </p>
        </div>

        <div class="steps-timeline-wrapper">
          <div class="timeline-line"></div>
          
          <div class="steps-grid">
            <!-- Step 1 -->
            <div class="step-item">
              <div class="step-number-circle">01</div>
              <h3 class="step-item-title">Choose Your Flight</h3>
              <p class="step-item-desc">
                Explore hundreds of destinations and find the perfect flight schedule that fits your travel plans.
              </p>
            </div>

            <!-- Step 2 -->
            <div class="step-item">
              <div class="step-number-circle">02</div>
              <h3 class="step-item-title">Pick Your Seat</h3>
              <p class="step-item-desc">
                Select your preferred seat class, customize baggage options, and add travel insurance.
              </p>
            </div>

            <!-- Step 3 -->
            <div class="step-item">
              <div class="step-number-circle">03</div>
              <h3 class="step-item-title">We Handle Everything</h3>
              <p class="step-item-desc">
                Our system instantly issues your ticket, secures your seat, and coordinates check-in details.
              </p>
            </div>

            <!-- Step 4 -->
            <div class="step-item">
              <div class="step-number-circle">04</div>
              <h3 class="step-item-title">Have A Safe Flight</h3>
              <p class="step-item-desc">
                Receive your boarding pass, head to the airport, and enjoy a comfortable and safe journey.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Tickets Section -->
    <section class="tickets-section">
      <div class="tickets-container">
        <div class="tickets-header">
          <span class="tickets-badge">Why Us</span>
          <h2 class="tickets-title">Travel With Confidence</h2>
          <p class="tickets-subtitle">
            We provide everything you need for a seamless and delightful journey from takeoff to landing.
          </p>
        </div>

        <div class="tickets-grid">
          <!-- Ticket 1 -->
          <div class="ticket-box">
            <!-- Top Image Area -->
            <div class="ticket-image-wrapper">
              <img src="https://lp-cms-production.imgix.net/image_browser/Happy%20passengers.jpg?auto=format&q=75" alt="Why Choose Us" class="ticket-image" />
            </div>

            <!-- Dashed Divider -->
            <div class="ticket-divider"></div>
            <!-- Bottom Notch Grab Hole -->
            <div class="ticket-notch-bottom"></div>

            <!-- Bottom Content Area -->
            <div class="ticket-content">
              <h3 class="ticket-box-title">Why you should choose us?</h3>
              <p class="ticket-box-desc">
                Discover why millions of travelers trust us for their journeys. From top-tier customer service to seamless booking experiences, we put your convenience first.
              </p>
            </div>
          </div>

          <!-- Ticket 2 -->
          <div class="ticket-box">
            <!-- Top Image Area -->
            <div class="ticket-image-wrapper">
              <img src="https://tds.indianeagle.com/wp-content/uploads/2022/08/Best-flight-deals.jpg" alt="Discounts & Offers" class="ticket-image" />
            </div>

            <!-- Dashed Divider -->
            <div class="ticket-divider"></div>
            <!-- Bottom Notch Grab Hole -->
            <div class="ticket-notch-bottom"></div>

            <!-- Bottom Content Area -->
            <div class="ticket-content">
              <h3 class="ticket-box-title">Various discounts and offers</h3>
              <p class="ticket-box-desc">
                Save big on your next trip! Access exclusive promotions, seasonal airline discounts, and rewards points that make flying comfortable and affordable.
              </p>
            </div>
          </div>

          <!-- Ticket 3 -->
          <div class="ticket-box">
            <!-- Top Image Area -->
            <div class="ticket-image-wrapper">
              <img src="https://www.wfs.aero/wp-content/uploads/2022/08/0003_SVQ_23072021_120-scaled.jpg" alt="Fast & Reliable" class="ticket-image" />
            </div>

            <!-- Dashed Divider -->
            <div class="ticket-divider"></div>
            <!-- Bottom Notch Grab Hole -->
            <div class="ticket-notch-bottom"></div>

            <!-- Bottom Content Area -->
            <div class="ticket-content">
              <h3 class="ticket-box-title">Fast & Reliable services</h3>
              <p class="ticket-box-desc">
                Experience speed and dependability. Book flight tickets in seconds with instant confirmation, secure payments, and 24/7 priority support.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Service Areas Section -->
    <section class="service-areas-section">
      <div class="service-areas-container">
        <div class="service-areas-header">
          <span class="service-areas-badge">Service Areas</span>
          <h2 class="service-areas-title">We Fly You Anywhere</h2>
          <p class="service-areas-subtitle">
            From local regional flights to major international destinations, check our route travel durations.
          </p>
        </div>

        <div class="service-areas-content">
          <!-- HCMC Flights Box -->
          <div class="service-card-box">
            <div class="service-card-header">
              <div class="service-icon-circle">
                <span class="service-header-icon">✈️</span>
              </div>
              <div class="service-header-text">
                <h3 class="service-card-title">Flights from Ho Chi Minh City</h3>
                <p class="service-card-subtitle">Direct connections and regional flights from HCMC (SGN)</p>
              </div>
            </div>

            <div class="service-routes-list">
              <div v-for="(route, index) in localRoutes" :key="index" class="route-item">
                <div class="route-left">
                  <span class="route-check-icon">✓</span>
                  <span class="route-name">{{ route.name }}</span>
                </div>
                <span class="route-duration">{{ route.duration }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Bottom Cookie Consent Banner -->
    <div v-if="showCookies" class="cookie-banner">
      <div class="cookie-content">
        <p class="cookie-text">
          We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.
        </p>
        <div class="cookie-actions">
          <button @click="acceptCookies" class="btn-cookie-decline">Decline</button>
          <button @click="acceptCookies" class="btn-cookie-accept">Accept All</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { API_URL } from '@/utils/apiClient';

const showCookies = ref(true);
const flightCount = ref('1,000');
const localRoutes = ref([]);

const quotes = ['Fast & Secure', 'Fast & Reliable'];
const currentQuoteIndex = ref(0);
const currentQuote = ref(quotes[0]);
let quoteInterval = null;

const servicesSectionRef = ref(null);
const isSectionVisible = ref(false);

const acceptCookies = () => {
  showCookies.value = false;
  localStorage.setItem('cookiesAccepted', 'true');
};

const fetchLocalRoutes = async () => {
  const defaultRoutes = [
    { name: 'Ha Noi', duration: '~2.0 hr flight' },
    { name: 'Da Nang', duration: '~1.2 hr flight' },
    { name: 'Phu Quoc', duration: '~1.0 hr flight' },
    { name: 'Nha Trang', duration: '~1.0 hr flight' },
    { name: 'Hue', duration: '~1.3 hr flight' },
    { name: 'Singapore', duration: '~2.0 hr flight' },
    { name: 'Bangkok', duration: '~1.5 hr flight' },
    { name: 'Seoul', duration: '~5.0 hr flight' }
  ];

  try {
    const res = await fetch(`${API_URL}/flights`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        // Filter flights originating from HCMC (SGN)
        const hcmcOrigin = ['sgn', 'ho chi minh', 'ho chi minh city', 'hcmc'];
        const hcmcFlights = data.filter(f => {
          const origin = (f.origin || '').toLowerCase();
          const originCity = (f.origin_city || '').toLowerCase();
          return hcmcOrigin.includes(origin) || hcmcOrigin.some(val => originCity.includes(val));
        });

        // Parse unique destinations and format durations
        const iataMap = {
          'SGN': 'Ho Chi Minh City',
          'HAN': 'Ha Noi',
          'DAD': 'Da Nang',
          'CXR': 'Nha Trang',
          'PQC': 'Phu Quoc',
          'HUI': 'Hue',
          'VCA': 'Can Tho',
          'VCL': 'Chu Lai',
          'BMV': 'Buon Ma Thuot',
          'UIH': 'Qui Nhon',
          'VDH': 'Dong Hoi',
          'VII': 'Vinh',
          'HPH': 'Hai Phong',
          'TBB': 'Tuy Hoa',
          'DIN': 'Dien Bien Phu',
          'PXU': 'Pleiku',
          'VCS': 'Con Dao',
          'DLI': 'Da Lat',
          'CAH': 'Ca Mau',
          'VKG': 'Rach Gia',
          'VDO': 'Quang Ninh',
          'SIN': 'Singapore',
          'BKK': 'Bangkok',
          'ICN': 'Seoul',
          'NRT': 'Tokyo',
          'KUL': 'Kuala Lumpur'
        };

        // Parse unique destinations and format durations
        const destinationsMap = new Map();
        hcmcFlights.forEach(f => {
          const rawDest = (f.destination_city || f.destination || 'Unknown Destination').trim();
          const destName = iataMap[rawDest.toUpperCase()] || rawDest;
          const durationMinutes = f.duration_minutes || 105;
          const hours = (durationMinutes / 60).toFixed(1);
          destinationsMap.set(destName.toLowerCase(), {
            name: destName,
            duration: `~${hours} hr flight`
          });
        });

        const dbRoutes = Array.from(destinationsMap.values());
        
        // Merge with default routes to ensure coverage
        const combined = [...dbRoutes];
        defaultRoutes.forEach(r => {
          if (!combined.some(c => c.name.toLowerCase() === r.name.toLowerCase())) {
            combined.push(r);
          }
        });

        // Shuffle & select 6 random routes
        localRoutes.value = combined.sort(() => 0.5 - Math.random()).slice(0, 6);
        return;
      }
    }
  } catch (err) {
    console.error('Failed to load flights for service areas:', err);
  }
  
  // Fallback to default routes shuffled
  localRoutes.value = defaultRoutes.sort(() => 0.5 - Math.random()).slice(0, 6);
};

onMounted(async () => {
  if (localStorage.getItem('cookiesAccepted') === 'true') {
    showCookies.value = false;
  }

  quoteInterval = setInterval(() => {
    currentQuoteIndex.value = (currentQuoteIndex.value + 1) % quotes.length;
    currentQuote.value = quotes[currentQuoteIndex.value];
  }, 10000);

  // Fetch local HCMC routes
  fetchLocalRoutes();

  // Fetch flight count dynamically
  try {
    const res = await fetch(`${API_URL}/flights`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        flightCount.value = data.length.toLocaleString();
      }
    }
  } catch (err) {
    console.error('Failed to load flights from database:', err);
  }

  // Setup Intersection Observer for scrolling animation
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        isSectionVisible.value = true;
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15
  });

  if (servicesSectionRef.value) {
    observer.observe(servicesSectionRef.value);
  }
});

onUnmounted(() => {
  if (quoteInterval) {
    clearInterval(quoteInterval);
  }
});
</script>

<style scoped>
/* Scoped styles to isolate the premium dark theme for the cover page */
.cover-page-wrapper {
  background-color: var(--sky-bg);
  color: var(--dark-text);
  min-height: calc(100vh - 60px); /* Leave space for navbar if active */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  padding: 4rem 2rem;
  position: relative;
  overflow: hidden;
}

.cover-container {
  max-width: 1280px;
  width: 100%;
  margin: auto;
}

.cover-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 4rem;
  align-items: center;
}

@media (max-width: 991px) {
  .cover-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
    text-align: center;
  }
  
  .content-col {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .cta-buttons {
    justify-content: center;
  }
}

/* Badge Pill Styling */
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  background-color: rgba(255, 94, 31, 0.15);
  border: 1px solid rgba(255, 94, 31, 0.4);
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  margin-bottom: 2rem;
  box-shadow: 0 0 15px rgba(255, 94, 31, 0.3);
  animation: orange-badge-pulse 2s infinite ease-in-out;
}

.shield-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-text {
  color: #FF5E1F;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.025em;
}

/* Hero Title Styling */
.hero-title {
  font-size: 4.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  letter-spacing: -0.02em;
}

@media (max-width: 1199px) {
  .hero-title {
    font-size: 3.5rem;
  }
}

.title-line-1 {
  color: var(--dark-text);
}

.title-line-2 {
  background: linear-gradient(135deg, #3B82F6 0%, #FF5E1F 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.flip-container {
  perspective: 1000px;
  display: inline-block;
  min-height: 1.25em;
}

/* Flip animation */
.flip-enter-active,
.flip-leave-active {
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.6s ease;
}

.flip-enter-from {
  transform: rotateX(-90deg) translateY(20px);
  opacity: 0;
}

.flip-leave-to {
  transform: rotateX(90deg) translateY(-20px);
  opacity: 0;
}

/* Hero Description Styling */
.hero-description {
  font-size: 1.15rem;
  line-height: 1.6;
  color: var(--gray-text);
  margin-bottom: 2.5rem;
  max-width: 540px;
}

/* CTA Buttons Styling */
.cta-buttons {
  display: flex;
  gap: 1.2rem;
  align-items: center;
  flex-wrap: wrap;
}

.btn-primary-cta {
  background-color: #FF5E1F;
  color: #ffffff;
  font-weight: 600;
  padding: 1rem 2rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1.05rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.25s ease;
  box-shadow: 0 4px 14px rgba(255, 94, 31, 0.4);
}

.btn-primary-cta:hover {
  background-color: #e54d12;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 94, 31, 0.6);
}

.arrow-icon {
  transition: transform 0.2s ease;
}

.btn-primary-cta:hover .arrow-icon {
  transform: translateX(4px);
}

.btn-secondary-cta {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  color: var(--dark-text);
  font-weight: 600;
  padding: 1rem 2rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1.05rem;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.25s ease;
}

.btn-secondary-cta:hover {
  background-color: #f3f4f6;
  transform: translateY(-2px);
}

.phone-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Image Column Styling */
.image-wrapper {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  aspect-ratio: 1024 / 582;
  background-color: #0b1120;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Cookie Banner Styling */
.cookie-banner {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - 4rem);
  max-width: 1200px;
  background-color: rgba(11, 17, 32, 0.95);
  border: 1px solid rgba(148, 163, 184, 0.1);
  backdrop-filter: blur(12px);
  padding: 1.25rem 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.cookie-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.cookie-text {
  font-size: 0.95rem;
  color: #94a3b8;
  line-height: 1.5;
  margin: 0;
}

.cookie-actions {
  display: flex;
  gap: 1rem;
  flex-shrink: 0;
}

.btn-cookie-decline {
  background: transparent;
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cookie-decline:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #ffffff;
}

.btn-cookie-accept {
  background-color: #3B82F6;
  border: none;
  color: #ffffff;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cookie-accept:hover {
  background-color: #2563eb;
}

@media (max-width: 767px) {
  .cookie-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  
  .cookie-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

/* Statistics Row Styling */
.stats-row {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 2.5rem;
  margin-top: 3.5rem;
  width: 100%;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 100px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--dark-text);
  line-height: 1.1;
  margin-bottom: 0.4rem;
  letter-spacing: -0.02em;
}

.stat-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--gray-text);
  line-height: 1.25;
}

@media (max-width: 767px) {
  .stats-row {
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    margin-top: 2.5rem;
  }
  
  .stat-item {
    align-items: center;
    text-align: center;
  }
}

/* Floating Badge inside image-wrapper */
.floating-badge {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  background-color: rgba(11, 17, 32, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  padding: 0.8rem 1.2rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  z-index: 10;
  animation: floatUp 0.6s ease-out;
}

.badge-icon-check {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(16, 185, 129, 0.15);
  border-radius: 50%;
  padding: 0.25rem;
}

.badge-info {
  display: flex;
  flex-direction: column;
}

.badge-title {
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 700;
  line-height: 1.2;
}

.badge-desc {
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 500;
  line-height: 1.2;
}

@keyframes floatUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Wave Divider */
.wave-container {
  width: 100%;
  line-height: 0;
  margin-top: auto;
  background-color: var(--sky-bg);
}

.wave-container svg {
  width: 100%;
  height: auto;
}

/* Services Section */
.services-section {
  background-color: var(--sky-bg);
  transition: background-color 3s ease;
  position: relative;
  overflow: hidden;
  padding: 5rem 2rem 7rem;
  width: 100%;
}

.services-section.is-active {
  background-color: #F5EDE4;
}

/* Flying Plane Animation Styles */
.flying-plane {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1; /* Fly behind card boxes */
  pointer-events: none;
}

.plane-orange.fly-away {
  offset-path: path('M -150,50 L 100,150 C 150,100 200,50 250,50 C 350,50 400,150 400,250 C 400,350 480,420 550,480 C 620,420 700,350 700,250 C 700,150 750,50 850,50 C 900,50 950,100 1000,150 C 1150,250 1300,200 1600,200');
  animation: flyHeartRotate-orange 17s cubic-bezier(0.25, 1, 0.5, 1) infinite;
}

.plane-blue.fly-away {
  offset-path: path('M -150,50 L 100,150 C 150,100 200,50 250,50 C 350,50 400,150 400,250 C 400,350 480,420 550,480 C 620,420 700,350 700,250 C 700,150 750,50 850,50 C 900,50 950,100 1000,150 C 1150,250 1300,200 1600,200');
  animation: flyHeartRotate-blue 17s cubic-bezier(0.25, 1, 0.5, 1) 0.5s infinite;
}

.plane-teal.fly-away {
  offset-path: path('M -150,50 L 100,150 C 150,100 200,50 250,50 C 350,50 400,150 400,250 C 400,350 480,420 550,480 C 620,420 700,350 700,250 C 700,150 750,50 850,50 C 900,50 950,100 1000,150 C 1150,250 1300,200 1600,200');
  animation: flyHeartRotate-teal 17s cubic-bezier(0.25, 1, 0.5, 1) 1s infinite;
}

@keyframes flyHeartRotate-orange {
  0% {
    offset-distance: 0%;
    offset-rotate: auto 90deg;
    opacity: 0;
    transform: scale(0.9);
  }
  2% {
    opacity: 0.6;
  }
  20.58% {
    offset-distance: 100%;
    offset-rotate: auto 90deg;
    opacity: 0.6;
    transform: scale(0.9);
  }
  49.9% {
    offset-distance: 100%;
    offset-rotate: auto 90deg;
    opacity: 0.6;
    transform: scale(0.9);
  }
  50% {
    offset-distance: 100%;
    offset-rotate: auto 270deg; /* Rotate 180 degrees to face left */
    opacity: 0.6;
    transform: scale(0.9);
  }
  70.58% {
    offset-distance: 0%;
    offset-rotate: auto 270deg;
    opacity: 0.6;
    transform: scale(0.9);
  }
  99.9% {
    offset-distance: 0%;
    offset-rotate: auto 270deg;
    opacity: 0.6;
    transform: scale(0.9);
  }
  100% {
    offset-distance: 0%;
    offset-rotate: auto 90deg; /* Reset to face right */
    opacity: 0;
    transform: scale(0.9);
  }
}

@keyframes flyHeartRotate-blue {
  0% {
    offset-distance: 0%;
    offset-rotate: auto 90deg;
    opacity: 0;
    transform: scale(0.7);
  }
  2% {
    opacity: 0.5;
  }
  20.58% {
    offset-distance: 100%;
    offset-rotate: auto 90deg;
    opacity: 0.5;
    transform: scale(0.7);
  }
  49.9% {
    offset-distance: 100%;
    offset-rotate: auto 90deg;
    opacity: 0.5;
    transform: scale(0.7);
  }
  50% {
    offset-distance: 100%;
    offset-rotate: auto 270deg; /* Rotate 180 degrees to face left */
    opacity: 0.5;
    transform: scale(0.7);
  }
  70.58% {
    offset-distance: 0%;
    offset-rotate: auto 270deg;
    opacity: 0.5;
    transform: scale(0.7);
  }
  99.9% {
    offset-distance: 0%;
    offset-rotate: auto 270deg;
    opacity: 0.5;
    transform: scale(0.7);
  }
  100% {
    offset-distance: 0%;
    offset-rotate: auto 90deg; /* Reset to face right */
    opacity: 0;
    transform: scale(0.7);
  }
}

@keyframes flyHeartRotate-teal {
  0% {
    offset-distance: 0%;
    offset-rotate: auto 90deg;
    opacity: 0;
    transform: scale(0.5);
  }
  2% {
    opacity: 0.4;
  }
  20.58% {
    offset-distance: 100%;
    offset-rotate: auto 90deg;
    opacity: 0.4;
    transform: scale(0.5);
  }
  49.9% {
    offset-distance: 100%;
    offset-rotate: auto 90deg;
    opacity: 0.4;
    transform: scale(0.5);
  }
  50% {
    offset-distance: 100%;
    offset-rotate: auto 270deg; /* Rotate 180 degrees to face left */
    opacity: 0.4;
    transform: scale(0.5);
  }
  70.58% {
    offset-distance: 0%;
    offset-rotate: auto 270deg;
    opacity: 0.4;
    transform: scale(0.5);
  }
  99.9% {
    offset-distance: 0%;
    offset-rotate: auto 270deg;
    opacity: 0.4;
    transform: scale(0.5);
  }
  100% {
    offset-distance: 0%;
    offset-rotate: auto 90deg; /* Reset to face right */
    opacity: 0;
    transform: scale(0.5);
  }
}

.services-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 3; /* Displays content cards on top of planes */
}

.services-header {
  text-align: center;
  margin-bottom: 4rem;
}

.services-badge {
  background-color: rgba(255, 94, 31, 0.15);
  border: 1px solid rgba(255, 94, 31, 0.4);
  color: #FF5E1F;
  padding: 0.4rem 1.2rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
  margin-bottom: 1rem;
  box-shadow: 0 0 15px rgba(255, 94, 31, 0.3);
  animation: orange-badge-pulse 2s infinite ease-in-out;
}

@keyframes orange-badge-pulse {
  0% {
    box-shadow: 0 0 8px rgba(255, 94, 31, 0.2);
    transform: scale(1);
  }
  50% {
    box-shadow: 0 0 18px rgba(255, 94, 31, 0.55);
    transform: scale(1.05);
  }
  100% {
    box-shadow: 0 0 8px rgba(255, 94, 31, 0.2);
    transform: scale(1);
  }
}

.services-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.services-subtitle {
  font-size: 1.1rem;
  color: var(--gray-text);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

/* Service Card */
.service-card {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 20px;
  padding: 2.5rem 2rem;
  transition: all 0.3s ease;
  box-shadow: 4px 4px 0px var(--dark-text);
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 6px 6px 0px var(--dark-text);
}

.service-icon-wrapper {
  background-color: rgba(1, 148, 243, 0.08);
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.service-icon {
  font-size: 1.5rem;
}

.service-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--dark-text);
  margin-bottom: 0.75rem;
}

.service-card-text {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--gray-text);
}

/* Steps Section Styling */
.steps-section {
  background-color: var(--sky-bg);
  padding: 6rem 2rem 8rem;
  width: 100%;
  border-top: 2px solid var(--dark-text);
}

.steps-container {
  max-width: 1200px;
  margin: 0 auto;
}

.steps-header {
  text-align: center;
  margin-bottom: 5rem;
}

.steps-badge {
  background-color: rgba(255, 94, 31, 0.15);
  border: 1px solid rgba(255, 94, 31, 0.4);
  color: #FF5E1F;
  padding: 0.4rem 1.2rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
  margin-bottom: 1rem;
  box-shadow: 0 0 15px rgba(255, 94, 31, 0.3);
  animation: orange-badge-pulse 2s infinite ease-in-out;
}

.steps-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.steps-subtitle {
  font-size: 1.1rem;
  color: var(--gray-text);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Steps Timeline Layout */
.steps-timeline-wrapper {
  position: relative;
  width: 100%;
  margin-top: 2rem;
}

.timeline-line {
  position: absolute;
  top: 30px; /* Centered relative to circles */
  left: 12%;
  right: 12%;
  height: 4px;
  background-color: var(--dark-text);
  z-index: 1;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2.5rem;
  position: relative;
  z-index: 2;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.step-number-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--primary-blue);
  border: 3px solid var(--dark-text);
  color: var(--white);
  font-size: 1.35rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  box-shadow: 4px 4px 0px var(--dark-text);
  transition: all 0.3s ease;
}

.step-item:hover .step-number-circle {
  transform: scale(1.1);
  background-color: #FF5E1F;
}

.step-item-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--dark-text);
  margin-bottom: 1rem;
}

.step-item-desc {
  font-size: 0.95rem;
  color: var(--gray-text);
  line-height: 1.6;
  max-width: 250px;
}

@media (max-width: 991px) {
  .steps-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 3.5rem 2.5rem;
  }
  .timeline-line {
    display: none; /* Hide horizontal line on wrap */
  }
}

@media (max-width: 575px) {
  .steps-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
}

/* Tickets Section Styling */
.tickets-section {
  background-color: var(--sky-bg); /* Match general background */
  padding: 6rem 2rem 8rem;
  width: 100%;
  border-top: 2px solid var(--dark-text);
}

.tickets-container {
  max-width: 1200px;
  margin: 0 auto;
}

.tickets-header {
  text-align: center;
  margin-bottom: 5rem;
}

.tickets-badge {
  background-color: rgba(255, 94, 31, 0.15);
  border: 1px solid rgba(255, 94, 31, 0.4);
  color: #FF5E1F;
  padding: 0.4rem 1.2rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
  margin-bottom: 1rem;
  box-shadow: 0 0 15px rgba(255, 94, 31, 0.3);
  animation: orange-badge-pulse 2s infinite ease-in-out;
}

.tickets-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.tickets-subtitle {
  font-size: 1.1rem;
  color: var(--gray-text);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Tickets Grid */
.tickets-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
}

@media (max-width: 991px) {
  .tickets-grid {
    grid-template-columns: 1fr;
    max-width: 500px;
    margin: 0 auto;
  }
}

/* Ticket Box Container */
.ticket-box {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  box-shadow: 4px 4px 0px var(--dark-text);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.ticket-box:hover {
  transform: translateY(-6px);
  box-shadow: 8px 8px 0px var(--dark-text);
}

.ticket-image-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.ticket-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.ticket-box:hover .ticket-image {
  transform: scale(1.05);
}

.ticket-notch-bottom {
  position: absolute;
  bottom: -14px; /* Centers the notch cutout on the bottom card border line */
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 24px;
  background-color: var(--dark-text); /* Black fill matching board theme */
  border: 2px solid var(--dark-text);
  border-bottom: none; /* Removes outer border to create a clean gap on the bottom line */
  border-radius: 50%;
  z-index: 4;
}

/* Ticket Divider Line */
.ticket-divider {
  position: absolute;
  top: 215px; /* Moved down to sit perfectly between image and text content */
  left: 45px; /* Shorter than text padding width */
  right: 45px;
  height: 0px;
  border-top: 2px dashed var(--dark-text);
  z-index: 3;
}

.ticket-content {
  padding: 3.2rem 2rem 2.5rem; /* Increased top padding to prevent blending with dot line */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.ticket-box-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.ticket-box-desc {
  font-size: 0.95rem;
  color: var(--gray-text);
  line-height: 1.6;
}

/* Service Areas Section CSS */
.service-areas-section {
  background-color: var(--sky-bg); /* Match general beige background */
  padding: 6rem 2rem;
  width: 100%;
  border-top: 2px solid var(--dark-text);
  color: var(--dark-text);
}

.service-areas-container {
  max-width: 1200px;
  margin: 0 auto;
}

.service-areas-header {
  text-align: center;
  margin-bottom: 4rem;
}

.service-areas-badge {
  background-color: rgba(255, 94, 31, 0.15);
  border: 1px solid rgba(255, 94, 31, 0.4);
  color: #FF5E1F;
  padding: 0.4rem 1.2rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
  margin-bottom: 1rem;
  box-shadow: 0 0 15px rgba(255, 94, 31, 0.3);
  animation: orange-badge-pulse 2s infinite ease-in-out;
}

.service-areas-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.service-areas-subtitle {
  font-size: 1.1rem;
  color: var(--gray-text);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.6;
}

.service-areas-content {
  max-width: 600px;
  margin: 0 auto;
}

/* Service Card Box */
.service-card-box {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 4px 4px 0px var(--dark-text); /* Neo-brutalist shadow */
}

.service-card-header {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 2rem;
}

.service-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: rgba(255, 94, 31, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.service-header-icon {
  font-size: 1.4rem;
}

.service-card-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 0.25rem;
}

.service-card-subtitle {
  font-size: 0.9rem;
  color: var(--gray-text);
}

/* Routes List */
.service-routes-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.route-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.2rem;
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.route-item:hover {
  background-color: #f8fafc;
  transform: translateX(4px);
}

.route-left {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.route-check-icon {
  color: #FF5E1F; /* Traveloka Orange checkmark */
  font-weight: bold;
}

.route-name {
  font-weight: 700;
  color: var(--dark-text);
}

.route-duration {
  font-size: 0.9rem;
  color: var(--gray-text);
  font-weight: 600;
}
</style>
