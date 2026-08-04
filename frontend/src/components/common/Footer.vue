<template>
  <footer class="footer-tika">
    <div class="container">
      <div class="footer-content">
        <!-- Brand Segment -->
        <div class="footer-section brand-column">
          <div class="footer-logo-wrapper">
            <svg width="36" height="36" viewBox="0 0 32 32" fill="none" class="tika-logo-svg">
              <circle cx="16" cy="16" r="16" fill="#0194F3"/>
              <path d="M16 8L22 14L16 20L10 14L16 8Z" fill="white"/>
            </svg>
            <span class="footer-brand-name">Tika</span>
          </div>
          <p class="brand-tagline">
            Experience the future of aviation ticketing. Rapid search, real-time updates, and elegant booking management all in one place.
          </p>
          <div class="social-links-grid">
            <a href="https://www.facebook.com/thienkhang.nguyenhuu" target="_blank" rel="noopener noreferrer" class="social-neo-btn" aria-label="Facebook">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3v3h-3v6.95c4.56-.93 8-4.96 8-9.8z"/>
              </svg>
            </a>
            <a href="https://www.instagram.com/skynoshy/" target="_blank" rel="noopener noreferrer" class="social-neo-btn" aria-label="Instagram">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.051.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/>
              </svg>
            </a>
            <a href="https://github.com/Skynoshy1/Flight_Booking_System_Final_Project" target="_blank" rel="noopener noreferrer" class="social-neo-btn" aria-label="GitHub">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Links Columns -->
        <div class="footer-section btn-column">
          <router-link to="/about" class="footer-neo-link-btn">
            About Tika
          </router-link>
          <p class="btn-column-desc">
            Discover our core mission, team values, and how we build a high-performance booking system for travelers worldwide.
          </p>
        </div>

        <div class="footer-section btn-column">
          <router-link to="/news" class="footer-neo-link-btn">
            Explore Us
          </router-link>
          <p class="btn-column-desc">
            Read the latest aviation news, flight journals, and expert travel tips to prepare for your next adventures.
          </p>
        </div>

        <div class="footer-section cta-column">
          <div class="footer-cta-card">
            <h4>Ready to fly?</h4>
            <p>Book your flight now with us!</p>
            <router-link to="/flights" class="footer-cta-btn">
              Search Flights ➔
            </router-link>
          </div>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom">
        <div class="footer-info-row">
          <p class="copyright">&copy; 2026 Tika Ticketing System. All rights reserved.</p>
          <p class="tech-badge">Powered by Vue 3 + FastAPI + Supabase</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped lang="scss">
@import '@/assets/scss/variables.scss';

.footer-tika {
  background: #0D161F;
  color: #ffffff;
  padding: 4.5rem 1.5rem 2rem;
  margin-top: 5rem;
  border-top: 5px solid #03121A;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  position: relative;
  overflow: hidden;
}

.footer-tika::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: repeating-linear-gradient(
    45deg,
    #FF5E1F,
    #FF5E1F 10px,
    #0194F3 10px,
    #0194F3 20px
  );
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem;
  margin-bottom: 3.5rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;

  h4 {
    font-size: 1.05rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #FF5E1F;
    margin: 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #03121A;
    display: inline-block;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;

    li {
      a {
        color: #9CA3AF;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        display: inline-block;

        &:hover {
          color: #0194F3;
          transform: translateX(4px);
        }
      }
    }
  }
}

/* Brand Column styling */
.brand-column {
  gap: 1rem;
}

.footer-logo-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.tika-logo-svg {
  filter: drop-shadow(2px 2px 0px #03121A);
}

.footer-brand-name {
  font-size: 1.6rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.brand-tagline {
  color: #9CA3AF;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
  max-width: 320px;
}

/* Neo-Brutalist Social buttons */
.social-links-grid {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.social-neo-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  background-color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 8px;
  color: #03121A;
  text-decoration: none;
  box-shadow: 3px 3px 0px #03121A;
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);

  &:hover {
    transform: translate(-2px, -2px);
    box-shadow: 5px 5px 0px #FF5E1F;
    background-color: #FF5E1F;
    color: #ffffff;
  }

  &:active {
    transform: translate(1px, 1px);
    box-shadow: 1px 1px 0px #03121A;
  }
}

.footer-neo-link-btn {
  display: inline-block;
  text-align: center;
  background-color: #FF5E1F;
  color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  box-shadow: 4px 4px 0px #03121A;
  transition: all 0.2s ease;
  margin-top: 1rem;
  width: 100%;
  max-width: 200px;
}

.footer-neo-link-btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0px #0194F3;
  background-color: #FF733B;
  color: #ffffff;
}

.footer-neo-link-btn:active {
  transform: translate(1px, 1px);
  box-shadow: 2px 2px 0px #03121A;
}

.btn-column-desc {
  color: #9CA3AF;
  font-size: 0.9rem;
  line-height: 1.55;
  margin: 0.8rem 0 0 0;
  max-width: 220px;
}

.footer-cta-card {
  background: #111E2B;
  border: 2px solid #FF5E1F;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 4px 4px 0px #03121A;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  max-width: 250px;
  margin-top: 0.5rem;

  h4 {
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: 800;
    margin: 0;
    text-transform: uppercase;
  }

  p {
    color: #9CA3AF;
    font-size: 0.95rem;
    line-height: 1.4;
    margin: 0;
  }
}

.footer-cta-btn {
  display: inline-block;
  text-align: center;
  background-color: #0194F3;
  color: #ffffff;
  border: 2px solid #03121A;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 2px 2px 0px #03121A;
  transition: all 0.2s ease;
  width: fit-content;

  &:hover {
    transform: translate(-1px, -1px);
    box-shadow: 3px 3px 0px #FF5E1F;
    background-color: #1aa2ff;
    color: #ffffff;
  }
}

/* Footer Bottom Section */
.footer-bottom {
  border-top: 2px solid #1F2937;
  padding-top: 2rem;
  position: relative;
}

.footer-info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.copyright {
  margin: 0;
  color: #6B7280;
  font-size: 0.9rem;
  font-weight: 500;
}

.tech-badge {
  margin: 0;
  background-color: #1F2937;
  color: #0194F3;
  border: 1px solid #374151;
  padding: 0.35rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

/* Responsiveness */
@media (max-width: 992px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
  }
}

@media (max-width: 576px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer-info-row {
    flex-direction: column;
    text-align: center;
  }
}
</style>
