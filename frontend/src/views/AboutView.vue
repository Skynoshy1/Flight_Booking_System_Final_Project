<template>
  <div class="about-page-wrapper">
    <div class="about-main-container">
      
      <!-- Part 1: Hero and Philosophy Cards -->
      <div class="about-card-section first-card-container">
        <!-- Section 1: Hero Banner Header -->
        <section class="hero-section">
          <div class="container-inner">
            <h1 class="hero-main-title">Traveloka - Booking Service</h1>
            
            <div class="hero-grid">
              <!-- Left Column: Flight Line-Art Sketch Vector -->
              <div class="hero-left-col">
                <div class="vector-sketch-container">
                  <svg viewBox="120 100 300 380" class="retro-hero-vector" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                      <!-- Diagonal Crosshatch Pattern for Shading -->
                      <pattern id="shading-crosshatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                        <line x1="0" y1="0" x2="0" y2="8" stroke="#03121A" stroke-width="1.2" opacity="0.45" />
                      </pattern>
                    </defs>

                    <!-- Background Hills & Ground Line from image_a5425e.png -->
                    <path d="M 50 400 Q 150 250 250 400" fill="#F2F7FA" stroke="#03121A" stroke-width="2"/>
                    <path d="M 250 400 Q 350 220 450 400" fill="#F2F7FA" stroke="#03121A" stroke-width="2"/>
                    <line x1="30" y1="400" x2="470" y2="400" stroke="#03121A" stroke-width="2" stroke-dasharray="4,4"/>

                    <!-- Luggage Base Stack Structure -->
                    <!-- Base Box 1 (Bottom Large) -->
                    <polygon points="200,430 300,430 330,400 230,400" fill="#FFFFFF" stroke="#03121A" stroke-width="2"/>
                    <polygon points="200,430 200,450 300,450 300,430" fill="#FFFFFF" stroke="#03121A" stroke-width="2"/>
                    <polygon points="300,430 300,450 330,420 330,400" fill="#FFFFFF" stroke="#03121A" stroke-width="2"/>

                    <!-- Base Box 2 (Middle) -->
                    <polygon points="220,380 290,380 315,355 245,355" fill="#FFFFFF" stroke="#03121A" stroke-width="2"/>
                    <polygon points="220,380 220,400 290,400 290,380" fill="#FFFFFF" stroke="#03121A" stroke-width="2"/>
                    <polygon points="290,380 290,400 315,375 315,355" fill="#FFFFFF" stroke="#03121A" stroke-width="2"/>

                    <!-- CONNECTED 3D ISOMETRIC LETTER F (Solid Structure rising from the base) -->
                    <!-- 1. Background Depth / Extrusions (Shaded Blue #0178C9) -->
                    <!-- Vertical Stem Right Side Side Face -->
                    <polygon points="265,350 280,335 280,165 265,180" fill="#0178C9" stroke="#03121A" stroke-width="2"/>
                    <polygon points="265,350 280,335 280,165 265,180" fill="url(#shading-crosshatch)"/>
                    
                    <!-- Vertical Stem Top Face -->
                    <polygon points="240,180 265,180 280,165 255,165" fill="#0178C9" stroke="#03121A" stroke-width="2"/>
                    <polygon points="240,180 265,180 280,165 255,165" fill="url(#shading-crosshatch)"/>

                    <!-- 2. Front Faces (Traveloka Blue #0194F3) -->
                    <!-- Main Vertical Stem Front Face -->
                    <polygon points="240,350 265,350 265,180 240,180" fill="#0194F3" stroke="#03121A" stroke-width="2"/>
                    <!-- Middle Horizontal Bar Front Face -->
                    <polygon points="265,260 310,260 310,280 265,280" fill="#0194F3" stroke="#03121A" stroke-width="2"/>

                    <!-- 3. Foreground Depth / Extrusions (Middle Bar) -->
                    <!-- Middle Bar Top Face -->
                    <polygon points="265,260 310,260 325,245 280,245" fill="#0178C9" stroke="#03121A" stroke-width="2"/>
                    <polygon points="265,260 310,260 325,245 280,245" fill="url(#shading-crosshatch)"/>

                    <!-- Middle Bar Right Side Face -->
                    <polygon points="310,260 325,245 325,265 310,280" fill="#0178C9" stroke="#03121A" stroke-width="2"/>
                    <polygon points="310,260 325,245 325,265 310,280" fill="url(#shading-crosshatch)"/>

                    <!-- 3. Floating Top Bar Piece (Premium Accent Orange #FF5E1F) (Bobbing Group) -->
                    <g class="floating-top-bar">
                      <!-- Floating Top Bar Front Face -->
                      <polygon points="240,150 330,150 330,170 240,170" fill="#FF5E1F" stroke="#03121A" stroke-width="2"/>
                      <!-- Floating Top Bar Top Face -->
                      <polygon points="240,150 255,135 345,135 330,150" fill="#FF844F" stroke="#03121A" stroke-width="2"/>
                      <!-- Floating Top Bar Right Side Face -->
                      <polygon points="330,150 345,135 345,155 330,170" fill="#E54812" stroke="#03121A" stroke-width="2"/>
                      <polygon points="330,150 345,135 345,155 330,170" fill="url(#shading-crosshatch)"/>
                    </g>
                  </svg>
                </div>
              </div>

              <!-- Right Column: Narrative Block -->
              <div class="hero-right-col">
                <p class="hero-narrative">  
                  We are a team of aviation tech engineers who go above and beyond average ticket mapping to make sure your flight itinerary is built exclusively for you. We make sure your tracking strategy is savvy, stable, and automated.
                </p>
                <div class="hero-action-container">
                  <router-link to="/flights" class="retro-action-btn-blue">
                    Explore Flights <span>→</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Section 2: Core Philosophy Soft Cards -->
        <section class="philosophy-section">
          <div class="container-inner">
            <div class="philosophy-grid">
              <!-- Card A: Mission -->
              <div class="philosophy-card">
                <div class="card-header-icon blue-tint">
                  <i class="bi bi-flag-fill"></i>
                </div>
                <h3 class="card-title">Mission</h3>
                <p class="card-desc">
                  To make your flight booking journey better, plain and simple.
                </p>
              </div>

              <!-- Card B: Vision -->
              <div class="philosophy-card">
                <div class="card-header-icon blue-tint">
                  <i class="bi bi-eye-fill"></i>
                </div>
                <h3 class="card-title">Vision</h3>
                <p class="card-desc">
                  The automated travel ecosystem you picture; the future data accuracy you deserve.
                </p>
              </div>

              <!-- Card C: Values -->
              <div class="philosophy-card">
                <div class="card-header-icon orange-tint">
                  <i class="bi bi-compass"></i>
                </div>
                <h3 class="card-title">Values</h3>
                <p class="card-desc">
                  Speed, relational security, system simplicity, and a few laughs along the way.
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Part 1.5: Airlines Showcase Card -->
      <div class="about-card-section airlines-card-container">
        <div class="container-inner">
          <h2 class="airlines-main-title-custom text-center">Airlines in Our System</h2>
          
          <div class="airlines-interactive-layout">
            <!-- 2x2 Grid of Boxes -->
            <div class="airlines-grid">
              <div 
                v-for="(airline, index) in airlines" 
                :key="airline.name"
                class="airline-box"
                :class="{ active: selectedAirlineIndex === index }"
                @click="selectedAirlineIndex = index"
              >
                <div class="airline-box-bg" :style="{ backgroundImage: `url(${airline.image})` }"></div>
                <div class="airline-box-overlay"></div>
                <span class="airline-box-name">{{ airline.name }}</span>
              </div>
            </div>

            <!-- Dynamic Description Card -->
            <div class="airline-description-display">
              <h3 class="selected-airline-title">{{ airlines[selectedAirlineIndex].name }}</h3>
              <p class="selected-airline-desc">{{ airlines[selectedAirlineIndex].description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Part 2: Rest of Content (Asymmetric Functional Profiles Grid) -->
      <div class="about-card-section second-card-container">
        <!-- Section 3: Asymmetric Functional Profiles Grid -->
        <section class="profiles-section">
          <div class="container-inner">
            <h2 class="profiles-main-title">You need more than a system. You need a Guide.</h2>

            <div class="asymmetric-layout">
              <!-- Block 1: Left Image, Right Text -->
              <div class="profile-block">
                <div class="profile-image-col">
                  <div class="sketch-image-wrapper-clean">
                    <img src="./Flight.png" alt="Aviation Tech Map Preview" class="profile-image-contain" />
                  </div>
                </div>
                <div class="profile-text-col">
                  <span class="block-subtitle">01/ Services</span>
                  <h3 class="block-title">What We Do</h3>
                  <p class="block-desc">
                    We deliver a smart, comprehensive flight search and booking platform designed for modern travelers. By ensuring real-time pricing accuracy and optimized route suggestions, we provide a seamless, transparent experience that helps you discover and secure the best travel options effortlessly.
                  </p>
                  <div>
                    <router-link to="/news" class="retro-action-btn-blue">
                      Explore <span>→</span>
                    </router-link>
                  </div>
                </div>
              </div>

              <!-- Block 2: Left Text, Right Image -->
              <div class="profile-block alternate">
                <div class="profile-text-col">
                  <span class="block-subtitle">02 / How Can We Help You</span>
                  <h3 class="block-title">Who We Are</h3>
                  <p class="block-desc">
                    We are your ultimate digital flight companion and dedicated travel service provider. Our platform is engineered to simplify your travel planning by connecting you instantly with a vast network of major airlines across the entire country. We bring real-time schedules and seamless booking management straight to your fingertips, empowering you to secure your flight tickets and enjoy a premium travel discovery experience right from the comfort of your own home. By transforming the traditional booking workflow, we eliminate the hassle of long queues, removing the need to visit ticket counters or travel directly to the airport just to arrange your trip. We handle the system complexities seamlessly so you can focus entirely on the joy of your next journey.
                  </p>
                </div>
                <div class="profile-image-col">
                  <div class="sketch-image-wrapper">
                    <div class="vector-scene-box">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 250" class="editorial-diagram-svg">
                        <rect x="10" y="10" width="330" height="230" rx="12" fill="#F2F7FA" stroke="#03121A" stroke-width="2" />
                        <!-- Circle Grid -->
                        <circle cx="80" cy="80" r="40" fill="#FFFFFF" stroke="#03121A" stroke-width="2" />
                        <line x1="80" y1="40" x2="80" y2="120" stroke="#0194F3" stroke-width="2" />
                        <line x1="40" y1="80" x2="120" y2="80" stroke="#0194F3" stroke-width="2" />
                        
                        <!-- Code tags -->
                        <rect x="160" y="50" width="140" height="20" rx="5" fill="#FFFFFF" stroke="#03121A" stroke-width="1.5" />
                        <line x1="170" y1="60" x2="280" y2="60" stroke="#03121A" stroke-width="3" />
                        
                        <rect x="160" y="80" width="120" height="20" rx="5" fill="#FFFFFF" stroke="#03121A" stroke-width="1.5" />
                        <line x1="170" y1="90" x2="250" y2="90" stroke="#FF5E1F" stroke-width="3" />

                        <!-- Connection paths -->
                        <path d="M 80 120 C 80 180, 180 180, 180 140" fill="none" stroke="#03121A" stroke-width="2" stroke-dasharray="4 4" />
                        
                        <!-- Sub-badge -->
                        <rect x="160" y="130" width="130" height="50" rx="8" fill="#FFFFFF" stroke="#03121A" stroke-width="2" />
                        <text x="175" y="160" font-family="'Inter', sans-serif" font-weight="700" font-size="13" fill="#03121A">&lt;daemon.sync/&gt;</text>
                      </svg>
                    </div>
                    <div class="image-sketch-border"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Part 3: Interactive Passenger Info & Scene Selector -->
      <div class="about-card-section interactive-card">
        <section class="interactive-section">
          <h2 class="section-title">Passenger Workspace</h2>
          <p class="section-desc">Personalize your boarding profile and customize your upcoming travel theme.</p>
          
          <div class="interactive-grid">
            <!-- Left Area: Welcome Message & Inputs -->
            <div class="interactive-box passenger-form-box">
              <h3 class="box-title">Create Welcome Boarding Pass</h3>
              
              <div class="form-inputs-group">
                <div class="input-field">
                  <label for="firstName" class="field-label">First Name</label>
                  <input 
                    id="firstName"
                    type="text" 
                    v-model="firstName" 
                    placeholder="Enter first name" 
                    class="retro-input"
                  />
                </div>
                <div class="input-field">
                  <label for="lastName" class="field-label">Last Name</label>
                  <input 
                    id="lastName"
                    type="text" 
                    v-model="lastName" 
                    placeholder="Enter last name" 
                    class="retro-input"
                  />
                </div>
              </div>

              <!-- Welcome Ticket Badge -->
              <div class="welcome-pass-container">
                <div class="boarding-pass-card">
                  <div class="boarding-pass-header">
                    <span class="pass-tag">BOARDING PASS</span>
                    <span class="pass-logo">✈️ Traveloka</span>
                  </div>
                  <div class="boarding-pass-body">
                    <div class="pass-row">
                      <div class="pass-cell">
                        <span class="cell-label">PASSENGER NAME</span>
                        <div class="cell-value">
                          {{ fullName || 'Valued Guest' }}
                        </div>
                      </div>
                      <div class="pass-cell status-cell">
                        <span class="cell-label">CLASS</span>
                        <div class="cell-value class-vip">FIRST CLASS VIP</div>
                      </div>
                    </div>
                    
                    <div class="pass-welcome-msg">
                      <span class="welcome-label">WELCOME MESSAGE:</span>
                      <p class="welcome-text">
                        Welcome aboard, <strong class="highlight-name">{{ fullName || 'Valued Guest' }}</strong>! Your premium flight network is ready for departure.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Area: Radio Button Image Selector -->
            <div class="interactive-box scene-selector-box">
              <h3 class="box-title">View Your Aircraft</h3>
              <p class="box-desc">Select an airline to view their signature passenger aircraft.</p>
              
              <div class="radio-options-group">
                <label class="retro-radio-label">
                  <input 
                    type="radio" 
                    name="airlinePlane" 
                    value="vietnam" 
                    v-model="selectedPlane" 
                    class="retro-radio"
                  />
                  <span class="radio-custom-box"></span>
                  <span class="radio-text-label">Vietnam Airlines</span>
                </label>
                
                <label class="retro-radio-label">
                  <input 
                    type="radio" 
                    name="airlinePlane" 
                    value="bamboo" 
                    v-model="selectedPlane" 
                    class="retro-radio"
                  />
                  <span class="radio-custom-box"></span>
                  <span class="radio-text-label">Bamboo Airways</span>
                </label>

                <label class="retro-radio-label">
                  <input 
                    type="radio" 
                    name="airlinePlane" 
                    value="vietjet" 
                    v-model="selectedPlane" 
                    class="retro-radio"
                  />
                  <span class="radio-custom-box"></span>
                  <span class="radio-text-label">VietJet Air</span>
                </label>

                <label class="retro-radio-label">
                  <input 
                    type="radio" 
                    name="airlinePlane" 
                    value="vietravel" 
                    v-model="selectedPlane" 
                    class="retro-radio"
                  />
                  <span class="radio-custom-box"></span>
                  <span class="radio-text-label">Vietravel Airlines</span>
                </label>
              </div>

              <!-- Travel Scene Image Display -->
              <div class="scene-image-frame">
                <transition name="fade-scale" mode="out-in">
                  <div :key="selectedPlane" class="scene-image-container">
                    <img 
                      :src="planeImageSrc" 
                      :alt="selectedPlane"
                      class="scene-img"
                    />
                    <div class="scene-caption-badge">
                      {{ planeCaption }}
                    </div>
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </section>
      </div>

    </div>
  </div>
</template>

<script>
import vietnamAirlinesImg from '../assets/images/vietnam_airlines.png';
import bambooAirwaysImg from '../assets/images/bamboo_airways.png';
import vietjetAirImg from '../assets/images/vietjet_air.png';
import vietravelAirlinesImg from '../assets/images/vietravel_airlines.png';

export default {
  name: 'AboutView',
  data() {
    return {
      selectedAirlineIndex: 0,
      firstName: '',
      lastName: '',
      selectedPlane: 'vietnam',
      airlines: [
        {
          name: 'Vietnam Airlines',
          image: vietnamAirlinesImg,
          description: 'Vietnam Airlines is the national flag carrier of Vietnam. Known for its premium service, modern wide-body fleet, and high safety standards, it connects Vietnam to key destinations across Asia, Europe, and Australia with signature lotus hospitality.'
        },
        {
          name: 'Bamboo Airways',
          image: bambooAirwaysImg,
          description: 'Bamboo Airways is a premium Vietnamese airline that offers high-quality hybrid flight services. Combining friendly hospitality, new aircraft, and excellent on-time performance, Bamboo Airways strives to deliver more than just a flight.'
        },
        {
          name: 'VietJet Air',
          image: vietjetAirImg,
          description: 'VietJet Air is a dynamic low-cost carrier in Vietnam, famous for its energetic branding, extensive network, and affordable pricing. It has revolutionized air travel in the region, making flights accessible to millions of travelers.'
        },
        {
          name: 'Vietravel Airlines',
          image: vietravelAirlinesImg,
          description: "Vietravel Airlines is a newer carrier backed by Vietnam's leading tour operator. It offers tourism-focused scheduled and charter flights, aiming to seamlessly bridge travel exploration, aviation safety, and cultural hospitality."
        }
      ]
    };
  },
  computed: {
    fullName() {
      const first = (this.firstName || '').trim();
      const last = (this.lastName || '').trim();
      if (!first && !last) return '';
      return `${first} ${last}`.trim();
    },
    planeImageSrc() {
      const urls = {
        vietnam: 'https://global.discourse-cdn.com/infiniteflight/original/4X/4/8/3/483b3033469b780aa80407bdc981ccbeb6008a8b.jpeg',
        bamboo: 'https://www.voyages-d-affaires.com/wp-content/uploads/2022/02/bamboo-airways.jpg',
        vietjet: 'https://travelobiz.com/wp-content/uploads/2022/06/Vietjet-Air-1.jpg',
        vietravel: 'https://flytime.vn/upload/images/vietravel-airlines-07273947.jpeg'
      };
      return urls[this.selectedPlane] || urls.vietnam;
    },
    planeCaption() {
      const captions = {
        vietnam: '✈️ Vietnam Airlines - National Flag Carrier',
        bamboo: '✈️ Bamboo Airways - Premium Hybrid Carrier',
        vietjet: '✈️ VietJet Air - Dynamic Budget Carrier',
        vietravel: '✈️ Vietravel Airlines - Travel Integration Carrier'
      };
      return captions[this.selectedPlane] || captions.vietnam;
    }
  }
}
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;0,800;1,700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

.about-page-wrapper {
  font-family: 'Inter', system-ui, sans-serif;
  background-color: #FAF4EE; /* Light brown background */
  color: #4B5563;
  line-height: 1.65;
  padding: 4rem 1.5rem;
  min-height: 100vh;
  overflow-x: hidden;
}

.about-main-container {
  max-width: 1140px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

.about-card-section {
  background-color: #FFFFFF;
  border: 2px solid #03121A;
  border-radius: 24px; /* Curved borders */
  padding: 4rem 3rem;
  /* Glow + retro offset shadow */
  box-shadow: 6px 6px 0px #03121A, 0px 0px 25px rgba(1, 148, 243, 0.12);
  transition: box-shadow 0.3s ease;

  &:hover {
    box-shadow: 8px 8px 0px #03121A, 0px 0px 30px rgba(1, 148, 243, 0.18);
  }

  @media (max-width: 768px) {
    padding: 2.5rem 1.5rem;
  }
}

.container-inner {
  width: 100%;
}

/* Retro Accent Buttons Style */
.retro-action-btn-blue {
  background-color: #0194F3;
  color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 50px;
  padding: 15px 34px;
  font-size: 1.15rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 4px 4px 0px #03121A; /* Solid sketch shadow styling offset parameter */
  transition: all 0.2s ease;
  cursor: pointer;
  text-decoration: none;
  font-family: 'Inter', system-ui, sans-serif;

  span {
    transition: transform 0.2s ease;
  }
}

.retro-action-btn-orange {
  background-color: #FF5E1F;
  color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 50px;
  padding: 15px 34px;
  font-size: 1.15rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 4px 4px 0px #03121A;
  transition: all 0.2s ease;
  cursor: pointer;
  text-decoration: none;
  font-family: 'Inter', system-ui, sans-serif;

  span {
    transition: transform 0.2s ease;
  }
}

.retro-action-btn-blue:hover, .retro-action-btn-orange:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px #03121A;

  span {
    transform: translateX(3px);
  }
}

/* Section 1: Hero Banner Header */
.hero-section {
  padding: 0 0 3.5rem;
  border-bottom: 2px solid #03121A;
  background-color: #FFFFFF;
}

.hero-main-title {
  font-family: 'Playfair Display', 'Georgia', serif;
  font-weight: 800;
  font-size: 4rem;
  color: #03121A;
  margin-bottom: 3.5rem;
  text-align: center;
  letter-spacing: -0.02em;

  @media (max-width: 768px) {
    font-size: 2.75rem;
    margin-bottom: 2rem;
  }
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 4rem;
  align-items: center;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

.hero-left-col {
  display: flex;
  justify-content: center;
}

.vector-sketch-container {
  width: 100%;
  max-width: 500px;
  background-color: #FFFFFF;
  border: 2px solid #03121A;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 6px 6px 0px #03121A;
}

.retro-hero-vector {
  width: 100%;
  height: auto;
  max-width: 485px;
  display: block;
  margin: 0 auto;
}

.floating-top-bar {
  animation: bobbing 3s ease-in-out infinite;
}

@keyframes bobbing {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-8px);
  }
  100% {
    transform: translateY(0px);
  }
}

.hero-right-col {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-narrative {
  font-size: 1.6rem;
  font-weight: 400;
  font-family: 'Playfair Display', 'Georgia', serif;
  color: #03121A;
  line-height: 1.6;
  margin-bottom: 2rem;
  letter-spacing: -0.01em;

  @media (max-width: 768px) {
    font-size: 1.3rem;
  }
}

.hero-action-container {
  display: flex;
}

/* Section 2: Core Philosophy Soft Cards */
.philosophy-section {
  padding: 3.5rem 0 0;
  background-color: #FFFFFF;
}

.philosophy-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

.philosophy-card {
  background-color: #F2F7FA;
  border: 2px solid #03121A;
  border-radius: 16px;
  padding: 2.5rem 2rem;
  box-shadow: 4px 4px 0px #03121A;
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px #03121A;
  }

  .card-header-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    border: 2px solid #03121A;
    font-size: 1.35rem;
    margin-bottom: 1.5rem;

    &.blue-tint {
      background-color: rgba(1, 148, 243, 0.12);
      color: #0194F3;
    }

    &.orange-tint {
      background-color: rgba(255, 94, 31, 0.12);
      color: #FF5E1F;
    }
  }

  .card-title {
    font-family: 'Playfair Display', 'Georgia', serif;
    font-weight: 700;
    font-size: 1.5rem;
    color: #03121A;
    margin-bottom: 0.75rem;
  }

  .card-desc {
    font-size: 0.95rem;
    color: #4B5563;
    line-height: 1.6;
    margin: 0;
  }
}

/* Section 3: Asymmetric Functional Profiles Grid */
.profiles-section {
  padding: 0;
  background-color: #FFFFFF;
}

.profiles-main-title {
  font-family: 'Playfair Display', 'Georgia', serif;
  font-weight: 800;
  font-size: 2.5rem;
  color: #03121A;
  text-align: center;
  margin-bottom: 5rem;
  letter-spacing: -0.015em;

  @media (max-width: 768px) {
    font-size: 2rem;
    margin-bottom: 3rem;
  }
}

.asymmetric-layout {
  display: flex;
  flex-direction: column;
  gap: 6rem;
}

.profile-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
  align-items: center;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  &.alternate {
    @media (min-width: 901px) {
      .profile-image-col {
        order: 2;
      }
      .profile-text-col {
        order: 1;
      }
    }
  }
}

.profile-image-col {
  display: flex;
  justify-content: center;
}

.sketch-image-wrapper-clean {
  width: 100%;
  max-width: 460px;
  display: flex;
  justify-content: center;
  align-items: center;

  .profile-image-contain {
    width: 100%;
    height: auto;
    max-height: 320px;
    object-fit: contain;
    display: block;
    transition: transform 0.2s ease;
  }
}

.sketch-image-wrapper {
  position: relative;
  width: 100%;
  max-width: 460px;

  .profile-image {
    width: 100%;
    height: 300px;
    object-fit: cover;
    border-radius: 20px;
    border: 2px solid #03121A;
    display: block;
    position: relative;
    z-index: 2;
  }

  .vector-scene-box {
    width: 100%;
    height: 300px;
    border-radius: 20px;
    border: 2px solid #03121A;
    overflow: hidden;
    position: relative;
    z-index: 2;
    background-color: #FFFFFF;
  }

  .editorial-diagram-svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  .image-sketch-border {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    background-color: #03121A;
    z-index: 1;
  }
}

.profile-text-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.block-subtitle {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #FF5E1F;
}

.block-title {
  font-family: 'Playfair Display', 'Georgia', serif;
  font-weight: 700;
  font-size: 2rem;
  color: #03121A;
  margin: 0;
}

.block-desc {
  font-size: 1rem;
  color: #4B5563;
  line-height: 1.7;
  margin: 0 0 1rem 0;
}

/* Airlines Showcase Card Styles */
.airlines-card-container {
  background-color: #FFFFFF;
}

.airlines-main-title-custom {
  font-family: 'Playfair Display', 'Georgia', serif;
  font-weight: 800;
  font-size: 2.5rem;
  color: #03121A;
  margin-bottom: 3.5rem;
}

.airlines-subtitle {
  font-size: 1.1rem;
  color: #6B7280;
  margin-bottom: 3rem;
}

.airlines-interactive-layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 3.5rem;
  align-items: stretch;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

.airlines-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 120px);
  gap: 1.25rem;
}

.airline-box {
  position: relative;
  border: 2px solid #03121A;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 4px 4px 0px #03121A;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px #03121A;
  }

  &.active {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px #0194F3, 0 0 16px rgba(1, 148, 243, 0.4);
    border-color: #0194F3;
    
    .airline-box-name {
      color: #ffffff;
      text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
      font-weight: 800;
    }
  }
}

.airline-box-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(4px) brightness(0.65);
  transition: filter 0.3s ease;
  z-index: 1;
}

.airline-box:hover .airline-box-bg {
  filter: blur(2px) brightness(0.75);
}

.airline-box.active .airline-box-bg {
  filter: blur(1px) brightness(0.8);
}

.airline-box-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(3, 18, 26, 0.25);
  z-index: 2;
  transition: background-color 0.3s ease;
}

.airline-box:hover .airline-box-overlay {
  background-color: rgba(3, 18, 26, 0.15);
}

.airline-box-name {
  position: relative;
  z-index: 3;
  color: #FFFFFF;
  font-weight: 700;
  font-size: 1.15rem;
  text-align: center;
  padding: 10px;
  font-family: 'Inter', system-ui, sans-serif;
  letter-spacing: -0.01em;
}

.airline-description-display {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #F2F7FA;
  border: 2px solid #03121A;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 4px 4px 0px #03121A;
  min-height: 250px;
  transition: all 0.3s ease;
  text-align: start;

  .selected-airline-title {
    font-family: 'Playfair Display', 'Georgia', serif;
    font-size: 2.25rem;
    font-weight: 800;
    color: #03121A;
    margin: 0 0 1rem 0;
    letter-spacing: -0.015em;
  }

  .selected-airline-desc {
    font-size: 1.1rem;
    color: #4B5563;
    line-height: 1.75;
    margin: 0;
  }
}

.text-center {
  text-align: center;
}

/* Part 3: Interactive Workspace styling */
.interactive-card {
  margin-top: 2rem;
}

.interactive-section {
  .section-title {
    font-family: 'Playfair Display', 'Georgia', serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #03121A;
    margin-bottom: 0.5rem;
    letter-spacing: -0.015em;
  }
  
  .section-desc {
    font-size: 1.1rem;
    color: #4B5563;
    margin-bottom: 3rem;
  }
}

.interactive-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 3rem;

  @media (max-width: 991px) {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

.interactive-box {
  background-color: #FFFFFF;
  border: 2px solid #03121A;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 4px 4px 0px #03121A;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  .box-title {
    font-family: 'Playfair Display', 'Georgia', serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #03121A;
    margin: 0;
  }

  .box-desc {
    font-size: 0.95rem;
    color: #4B5563;
    margin: 0;
    line-height: 1.5;
  }
}

/* Forms and Inputs */
.form-inputs-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;

  @media (max-width: 575px) {
    grid-template-columns: 1fr;
  }
}

.input-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: start;

  .field-label {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #03121A;
    letter-spacing: 0.05em;
  }
}

.retro-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #03121A;
  border-radius: 8px;
  background-color: #F2F7FA;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  color: #03121A;
  outline: none;
  transition: all 0.2s ease;

  &:focus {
    background-color: #FFFFFF;
    border-color: #FF5E1F;
    box-shadow: 2px 2px 0px #03121A;
  }
}

/* Welcome Boarding Pass Card */
.welcome-pass-container {
  margin-top: 1rem;
}

.boarding-pass-card {
  background-color: #FFFFFF;
  border: 2px solid #03121A;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 3px 3px 0px #03121A;
  text-align: start;
}

.boarding-pass-header {
  background-color: #0194F3;
  color: #FFFFFF;
  border-bottom: 2px solid #03121A;
  padding: 0.75rem 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .pass-tag {
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.1em;
  }

  .pass-logo {
    font-size: 0.85rem;
    font-weight: 700;
  }
}

.boarding-pass-body {
  padding: 1.25rem;
  background-color: #FAF4EE;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;

  .pass-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
  }

  .pass-cell {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .cell-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #4B5563;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .cell-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: #03121A;
  }

  .class-vip {
    color: #FF5E1F;
    font-size: 0.95rem;
    font-weight: 800;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.05em;
  }

  .pass-welcome-msg {
    border-top: 1px dashed #03121A;
    padding-top: 1rem;

    .welcome-label {
      font-size: 0.7rem;
      font-weight: 700;
      color: #FF5E1F;
      display: block;
      margin-bottom: 0.25rem;
    }

    .welcome-text {
      font-size: 0.95rem;
      margin: 0;
      color: #4B5563;
      line-height: 1.5;
    }

    .highlight-name {
      color: #0194F3;
      font-weight: 800;
    }
  }
}

/* Radios and Scene Selection */
.radio-options-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  text-align: start;
}

.retro-radio-label {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  font-weight: 600;
  color: #03121A;
  font-size: 0.95rem;

  input[type="radio"] {
    display: none;
  }
}

.radio-custom-box {
  width: 20px;
  height: 20px;
  border: 2px solid #03121A;
  border-radius: 50%;
  background-color: #FFFFFF;
  position: relative;
  transition: all 0.2s ease;

  &::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #FF5E1F;
    transition: transform 0.2s ease;
  }
}

.retro-radio:checked + .radio-custom-box {
  background-color: #F2F7FA;
  border-color: #03121A;

  &::after {
    transform: translate(-50%, -50%) scale(1);
  }
}

/* Scene Image Frame */
.scene-image-frame {
  border: 2px solid #03121A;
  border-radius: 12px;
  overflow: hidden;
  height: 250px;
  position: relative;
  box-shadow: 3px 3px 0px #03121A;
}

.scene-image-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.scene-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.scene-caption-badge {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  background-color: rgba(3, 18, 26, 0.85);
  color: #FFFFFF;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
}

/* Vue Transitions */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}

.fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.fade-scale-leave-to {
  opacity: 0;
  transform: scale(1.02);
}
</style>
