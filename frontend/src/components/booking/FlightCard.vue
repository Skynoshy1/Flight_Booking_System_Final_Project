<template>
  <div 
    class="flight-premium-card" 
    :style="{ backgroundImage: `url(${getDestinationImage(flight.destination)})` }"
    @click="selectFlight"
  >
    <!-- Overlay Mask -->
    <div class="overlay-mask"></div>

    <div class="ticket-header">
      <div class="brand-info">
        <div v-if="getAirlineLogo(flight.airline)" class="airline-logo-bubble">
          <img :src="getAirlineLogo(flight.airline)" :alt="flight.airline" class="airline-brand-logo" />
        </div>
        <div v-else class="logo-wrapper" :class="getAirlineBrandClass(flight.airline)">
          {{ getAirlineShortName(flight.airline) }}
        </div>
        <div class="flight-meta-block">
          <h3 v-if="!getAirlineLogo(flight.airline)" class="airline-name">{{ flight.airline }}</h3>
          <p class="flight-number">Flight {{ flight.flightNumber }}</p>
        </div>
      </div>
      <span class="trip-type-badge">{{ flight.trip_type === 'round-trip' ? 'ROUND-TRIP' : 'ONE-WAY' }}</span>
    </div>



    <!-- Ticket Middle: Travel Metrics & Details -->
    <div class="ticket-body">
      <div class="timeline-glass-wrapper">
        <div class="time-section-vertical">
          <div class="timeline-point">
            <span class="time-label">{{ formatTime(flight.departureTime) }}</span>
            <span class="airport-label">{{ flight.origin }}</span>
          </div>

          <div class="duration-connector">
            <span class="plane-icon">✈️</span>
            <div class="connector-line"></div>
            <span class="duration-label">{{ flight.duration }}</span>
          </div>

          <div class="timeline-point">
            <span class="time-label">{{ formatTime(flight.arrivalTime) }}</span>
            <span class="airport-label">{{ flight.destination }}</span>
          </div>
        </div>
      </div>

      <!-- Dynamic Date Panel -->
      <div class="flight-duration-dates-area">
        <!-- One-Way Layout: Perfectly Centered Single Line -->
        <div v-if="flight.trip_type !== 'round-trip'" class="oneway-date-text">
          📅 Departure Date: {{ flight.departure_date }}
        </div>
        
        <!-- Round-Trip Layout: Two Clean, Structured Rows -->
        <div v-else class="roundtrip-dates-grid">
          <div class="date-row">🛫 Departure: {{ flight.departure_date }}</div>
          <div class="date-row">🛬 Return: {{ flight.return_date }}</div>
        </div>
      </div>
    </div>

    <!-- Tear-off Separator Stub -->
    <div class="ticket-tear-line"></div>

    <!-- Ticket Bottom: Price Stub & CTA -->
    <div class="ticket-bottom">
      <div class="price-stub">
        <p class="price-lbl">Fare Price</p>
        <div class="price-tag-premium">
          <span class="currency">$</span>
          <span class="amount">{{ flight.base_price }}</span>
        </div>
      </div>
      <button class="btn-select-premium" :class="{ 'selected': isSelected }">
        <span v-if="!isSelected">Select</span>
        <span v-else>✓ Selected</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  flight: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['select']);
const isSelected = ref(false);

const formatTime = (time) => {
  if (typeof time === 'string') {
    const parts = time.split(':');
    if (parts.length >= 2) {
      return `${parts[0]}:${parts[1]}`;
    }
  }
  return time;
};

const selectFlight = () => {
  isSelected.value = !isSelected.value;
  emit('select', props.flight);
};

const getDestinationImage = (destinationCode) => {
  const mapping = {
    'HAN': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQ6YnKJ8kE02X_Pe_xOgBqbftsMLu8AqnEwNOH0MEjwqJxlZd-Ji8iO0aZ5euEh7AZ4W2THGGQYKb_oc70',
    'SGN': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRC_4LXSay4j_y4tIhlbSZGMilHMWOIxm4WVWA8pjva39aqKHNQZlNbCN39jJj0dv9AZuR0Z_S118pKNmM',
    'DAD': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSh5nWfheh4fBjHHzi4uqVyMXmKoLMRIcq6iUYtGZnAPw8otTMsNeZhc5VLbmPr',
    'CXR': 'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTuFSX8HC_fstNxaAVDcGNJJa31LuCBtGZUfcVr2hSJwdlQIBmc4UjyXhB6NzVJdtyL4xFEbxgzcTWPp4Y',
    'PQC': 'https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcSMsyHK-GkpgBgDehQgvLpvM22PExi8KGXZRfjGnWscHiwEpdO2jbKTaodXSZ7z7PBnUxjva0pdWS3GzRs',
    'VKG': 'https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQS1D1poweQFdQbOIIwrLkgLUcoGBlWoxn-wbImDu3p9PC8IQeRc0dVaktQ9DwEukAZtJefTJgZUQkiqFg',
    'VDO': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcT9Ny5f31bHazSwuui89eCCsRRzQrOv1wFsSRIz29uq4tzaY7iEjnP5Rns6z-zrf7FmGC3P5-sO22QCf9U',
    'DLI': 'https://dalatnews.net/wp-content/uploads/2025/01/hinh-anh-san-bay-lien-khuong-tai-da-lat.webp',
    'HUI': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQUHiL4QMkbvKrxAi1r33WNyEk_Jk5U5Cf0fhtqNGgRElQOA4Lpxv4_A_aK12TUecddOmMz6mraNNk1PhY',
    'UIH': 'https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQ4aySdJb1ZhIgAc0pHfkLI8gyV_glYP4ljhtG0pY7vbqZ9pEUN5jjichodSKKTr5uENwQpR2kLmcUhdv8',
    'VCS': 'https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTmuRE8TqDIlUgobysZPOuXjfKEkdrBM3ad3Shzp2qW1bxlcHz2Sy-KSaa8oQBvuvbiFjN7dzSzBN5NM4k',
    'VII': 'https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRUYCKRNT6NoZ1qBwm4SG_QLuXu4uCsH-h6lnYhhzdwnokVIkqoLHJlzeW_uyzB-F5HAVkCO37NiK8tfg4',
    'HPH': 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTxETxFDsZvluEHinY7gAsohU_VfBex1qNF3iY-LbxgXqw_y95DB5UERaFdJTR-w3H18EhV6Mt8EsbvZDs',
    'SIN': 'https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTNloQM7FiWpGrN0vBX8xWbDOCjpDp_a1vrCtCX7wAEXeIpM9GvxSulVpvmVh1AIn1IZG9UjILdCBT4b7o'
  };
  return mapping[destinationCode] || 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=600&q=80';
};

const getAirlineLogo = (airlineName) => {
  const name = (airlineName || '').toLowerCase();
  if (name.includes('vietjet')) return 'https://1000logos.net/wp-content/uploads/2021/04/VietJet-Air-logo.png';
  if (name.includes('bamboo')) return 'https://tse3.mm.bing.net/th/id/OIP.bQcgyMuhw4v-aOX3In-BPAHaHk?rs=1&pid=ImgDetMain&o=7&rm=3';
  if (name.includes('vietravel')) return 'https://tse2.mm.bing.net/th/id/OIP.xA4mFIV99UhSmZKiSP0ufgHaHa?rs=1&pid=ImgDetMain&o=7&rm=3';
  if (name.includes('vietnam')) return 'https://tse4.mm.bing.net/th/id/OIP.6sDY5mRcgNsLb7BhLQdEpAHaFi?rs=1&pid=ImgDetMain&o=7&rm=3';
  return '';
};

const getAirlineBrandClass = (airline) => {
  const name = (airline || '').toLowerCase();
  if (name.includes('vietnam')) return 'brand-vietnam';
  if (name.includes('vietjet')) return 'brand-vietjet';
  if (name.includes('bamboo')) return 'brand-bamboo';
  return 'brand-default';
};

const getAirlineShortName = (airline) => {
  const name = (airline || '').toLowerCase();
  if (name.includes('vietnam')) return 'VN';
  if (name.includes('vietjet')) return 'VJ';
  if (name.includes('bamboo')) return 'BA';
  if (name.includes('vietravel')) return 'VA';
  return 'FL';
};
</script>

<style scoped>
.flight-premium-card {
  position: relative;
  background-size: cover;
  background-position: center;
  border-radius: 16px;
  overflow: hidden;
  padding: 1.5rem;
  width: 100%;
  box-sizing: border-box;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.flight-premium-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
  border-color: #0194F3;
}

/* Semi-circle cutout hole illusion centered on the bottom edge */
.flight-premium-card::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 24px;
  background-color: #f7f9fa;
  border-radius: 50%;
  z-index: 2;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.overlay-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.85) 100%);
  border-radius: 16px;
  z-index: 1;
}

/* Top Section */
.ticket-header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.brand-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.airline-logo-bubble {
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 10px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  height: 44px;
}

.airline-brand-logo {
  max-height: 35px;
  max-width: 110px;
  object-fit: contain;
}

.logo-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.1rem;
  color: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.brand-vietnam {
  background: linear-gradient(135deg, #003057 0%, #005a9c 100%);
  border: 1px solid #005a9c;
}

.brand-vietjet {
  background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
}

.brand-bamboo {
  background: linear-gradient(135deg, #10b981 0%, #064e3b 100%);
}

.brand-default {
  background: #4b5563;
}

.flight-meta-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.airline-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.flight-number {
  font-size: 0.95rem;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
}

.flight-duration-dates-area {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin: 12px 0;
  padding: 8px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.oneway-date-text {
  font-size: 0.85rem;
  font-weight: 500;
  color: #ffffff;
  letter-spacing: 0.3px;
  text-align: center;
}
.roundtrip-dates-grid {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
  text-align: center;
}
.date-row {
  font-size: 0.82rem;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.return-date-tag {
  color: #38bdf8;
  font-weight: 600;
}

.trip-type-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  padding: 4px 8px;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  min-width: 80px;
  text-align: center;
}

/* Middle Section */
.ticket-body {
  position: relative;
  z-index: 2;
  margin-top: 1rem;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.timeline-glass-wrapper {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  padding: 12px 18px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.time-section-vertical {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.timeline-point {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.time-label {
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
}

.airport-label {
  font-size: 1.1rem;
  color: #cbd5e1;
  font-weight: 600;
  margin-top: 2px;
  letter-spacing: 0.5px;
}

.duration-connector {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.connector-line {
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.3);
  margin: 6px 0;
}

.plane-icon {
  font-size: 0.8rem;
  color: #ffffff;
}

.duration-label {
  font-size: 1.15rem;
  color: #cbd5e1;
  font-weight: 600;
}



/* Tear Line Separator Stub */
.ticket-tear-line {
  position: relative;
  height: 1px;
  border-top: 2px dashed rgba(255, 255, 255, 0.25);
  margin: 0.75rem 0;
  z-index: 2;
  width: 100%;
}

/* Bottom Section */
.ticket-bottom {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-bottom: 4px;
}

.price-stub {
  display: flex;
  flex-direction: column;
}

.price-lbl {
  font-size: 1rem;
  color: #cbd5e1;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.price-tag-premium {
  color: #FF5E1F;
  font-weight: 800;
  display: flex;
  align-items: baseline;
  gap: 1px;
}

.price-tag-premium .currency {
  font-size: 1.5rem;
  font-weight: 700;
}

.price-tag-premium .amount {
  font-size: 2.4rem;
}

.btn-select-premium {
  background: #0194F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.2rem;
}

.btn-select-premium:hover {
  background: #007ccb;
  transform: translateY(-1px);
}

.header-badges {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-badge-card {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge-card.on-time,
.status-badge-card.on\ time {
  background: rgba(16, 185, 129, 0.2);
  color: #10B981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.status-badge-card.delay,
.status-badge-card.delayed {
  background: rgba(245, 158, 11, 0.2);
  color: #F59E0B;
  border: 1px solid rgba(245, 158, 11, 0.4);
}

.status-badge-card.canceled,
.status-badge-card.cancelled {
  background: rgba(239, 68, 68, 0.2);
  color: #EF4444;
  border: 1px solid rgba(239, 68, 68, 0.4);
}


.btn-select-premium.selected {
  background: #10b981;
}

@media (max-width: 576px) {
  .flight-premium-card {
    padding: 1rem;
    min-height: auto;
  }

  .ticket-header {
    flex-wrap: wrap;
    gap: 8px;
  }

  .brand-info {
    width: 100%;
  }

  .trip-type-badge {
    margin-left: 0;
  }

  .time-label {
    font-size: 1.25rem;
  }

  .airport-label {
    font-size: 0.9rem;
  }

  .duration-label {
    font-size: 0.85rem;
  }

  .plane-icon {
    font-size: 0.75rem;
  }

  .timeline-glass-wrapper {
    padding: 10px 8px;
  }

  .ticket-footer {
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
    text-align: center;
  }

  .price-stub {
    align-items: center;
  }

  .btn-select-premium {
    width: 100%;
    font-size: 1rem;
    padding: 8px 16px;
  }

  .price-tag-premium .amount {
    font-size: 1.8rem;
  }
}
</style>


