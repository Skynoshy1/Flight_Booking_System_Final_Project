<template>
  <div class="news-page-wrapper">
    <div class="news-main-container">
      
      <!-- Header Section -->
      <header class="news-header">
        <h1 class="news-main-title">Aviation Journal & Insights</h1>
        <p class="news-main-subtitle">Stay updated with the latest in aviation technology, trends, and global travel news.</p>
      </header>

      <!-- Search & Filter Controls -->
      <div class="filter-card">
        <div class="filter-grid">
          <!-- Text Search -->
          <div class="filter-group">
            <label for="searchQuery" class="filter-label">Search Keywords</label>
            <div class="input-with-icon">
              <span class="input-icon">🔍</span>
              <input 
                id="searchQuery"
                type="text" 
                v-model="searchQuery" 
                placeholder="Search title or content..." 
                class="filter-input"
                @input="resetPagination"
              />
            </div>
          </div>

          <!-- Category Filter -->
          <div class="filter-group">
            <label for="categoryFilter" class="filter-label">Category</label>
            <select 
              id="categoryFilter"
              v-model="selectedCategory" 
              class="filter-select"
              @change="resetPagination"
            >
              <option value="">All Categories</option>
              <option v-for="cat in uniqueCategories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>

          <!-- Date Filter -->
          <div class="filter-group">
            <label for="dateFilter" class="filter-label">Publish Date</label>
            <input 
              id="dateFilter"
              type="date" 
              v-model="selectedDate" 
              class="filter-input"
              @change="resetPagination"
            />
          </div>

          <!-- Clear Button -->
          <div class="filter-group clear-btn-group">
            <button class="btn-clear-filters" @click="clearFilters">
              Reset Filters
            </button>
          </div>
        </div>
      </div>

      <!-- News Feed Grid -->
      <div v-if="paginatedArticles.length > 0" class="news-grid-3col">
        <article 
          v-for="article in paginatedArticles" 
          :key="article.id" 
          class="news-vertical-card"
        >
          <div class="card-image-wrapper">
            <img :src="article.image" :alt="article.title" class="card-img-fit" />
            <span class="card-category-badge">{{ article.category }}</span>
          </div>
          <div class="card-text-content">
            <div class="card-meta-header">
              <span class="card-date">{{ formatDateString(article.date) }}</span>
              <button 
                class="like-button-heart" 
                :class="{ 'is-liked': article.liked }" 
                @click="toggleLike(article)"
                aria-label="Like article"
              >
                {{ article.liked ? '❤️' : '🤍' }}
              </button>
            </div>
            <h3 class="card-headline-title">{{ article.title }}</h3>
            <p class="card-excerpt-text">{{ article.summary }}</p>
            <div class="card-footer">
              <span class="card-author">By {{ article.author }}</span>
            </div>
          </div>
        </article>
      </div>

      <!-- No Results State -->
      <div v-else class="no-results-card">
        <div class="no-results-icon">✈️</div>
        <h3>No Articles Found</h3>
        <p>We couldn't find any articles matching your search criteria. Try clearing some filters or using different keywords.</p>
        <button class="btn-clear-filters" @click="clearFilters">Clear All Filters</button>
      </div>

      <!-- Pagination Controls -->
      <nav v-if="totalPages > 1" class="pagination-nav" aria-label="News Pagination">
        <button 
          class="pagination-btn" 
          :disabled="currentPage === 1" 
          @click="changePage(1)"
          aria-label="First page"
        >
          « First
        </button>
        <button 
          class="pagination-btn" 
          :disabled="currentPage === 1" 
          @click="changePage(currentPage - 1)"
          aria-label="Previous page"
        >
          ‹ Prev
        </button>
        
        <div class="page-numbers">
          <button 
            v-for="page in totalPages" 
            :key="page" 
            class="pagination-btn page-num-btn"
            :class="{ 'active-page': currentPage === page }"
            @click="changePage(page)"
          >
            {{ page }}
          </button>
        </div>

        <button 
          class="pagination-btn" 
          :disabled="currentPage === totalPages" 
          @click="changePage(currentPage + 1)"
          aria-label="Next page"
        >
          Next ›
        </button>
        <button 
          class="pagination-btn" 
          :disabled="currentPage === totalPages" 
          @click="changePage(totalPages)"
          aria-label="Last page"
        >
          Last »
        </button>
      </nav>

      <!-- Results Summary -->
      <div class="results-summary">
        Showing {{ resultsStart }} - {{ resultsEnd }} of {{ filteredArticles.length }} articles
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const selectedCategory = ref('');
const selectedDate = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(6); // Shows 6 articles per page for a beautiful 3-column layout grid

const articles = ref([
  {
    id: 1,
    title: "The Future of Autonomous Air Mobility",
    summary: "How next-generation drone corridors and automated air traffic control are paving the way for urban eVTOL networks.",
    image: "https://images.unsplash.com/photo-1540962351504-03099e0a754b?auto=format&fit=crop&q=80&w=600",
    date: "2026-07-05",
    category: "Tech Trends",
    author: "Evelyn Vance",
    liked: false
  },
  {
    id: 2,
    title: "Revolutionizing Real-Time Route Optimization",
    summary: "Monorepos and distributed systems are enabling airlines to compute fuel-efficient trajectories instantly in response to weather shifts.",
    image: "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&q=80&w=600",
    date: "2026-06-28",
    category: "Data Systems",
    author: "Marcus Brody",
    liked: false
  },
  {
    id: 3,
    title: "Sustainability in Jet Propulsion Systems",
    summary: "A deep dive into sustainable aviation fuels (SAF) and hydrogen engines currently entering passenger fleet trials.",
    image: "https://images.unsplash.com/photo-1517976487492-5750f3195933?auto=format&fit=crop&q=80&w=600",
    date: "2026-06-15",
    category: "Green Tech",
    author: "Sarah Jenkins",
    liked: false
  },
  {
    id: 4,
    title: "Smart Airport Terminals of 2030",
    summary: "Biometrics, seamless baggage routing, and automated security scans are redefining the traveler experience globally.",
    image: "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?auto=format&fit=crop&q=80&w=600",
    date: "2026-06-02",
    category: "Infrastructure",
    author: "Evelyn Vance",
    liked: false
  },
  {
    id: 5,
    title: "Global Supply Chain Hurdles in Aerospace",
    summary: "How critical raw material shortages and chip bottlenecks are delaying fleet modernization schedules for major airlines.",
    image: "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&q=80&w=600",
    date: "2026-05-25",
    category: "Economics",
    author: "Marcus Brody",
    liked: false
  },
  {
    id: 6,
    title: "Rethinking In-Flight Digital Services",
    summary: "Airlines are partnering with low-Earth-orbit satellite networks to deliver ultra-fast, free Wi-Fi to passenger cabins.",
    image: "https://images.unsplash.com/photo-1519074002996-a69e7ac46a42?auto=format&fit=crop&q=80&w=600",
    date: "2026-05-10",
    category: "Cabin Tech",
    author: "Sarah Jenkins",
    liked: false
  },
  {
    id: 7,
    title: "Abnormal Math Scores Under Regional Audit",
    summary: "Authorities have launched a comprehensive audit following anomalies identified during the regional mathematics examinations.",
    image: "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?auto=format&fit=crop&q=80&w=600",
    date: "2026-07-06",
    category: "Aviation News",
    author: "Evelyn Vance",
    liked: false
  },
  {
    id: 8,
    title: "Global Aviation Accord Seeks Unified Standards",
    summary: "Representatives from over fifty countries signed a memorandum to implement stricter carbon thresholds for transcontinental air travel pipelines.",
    image: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=600",
    date: "2026-07-04",
    category: "Green Tech",
    author: "Marcus Brody",
    liked: false
  },
  {
    id: 9,
    title: "Next-Gen Flight Tracking Protocols Verified",
    summary: "Satellite transceiver modules successfully tracked mock commercial flight vectors over northern polar coordinates.",
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=600",
    date: "2026-06-30",
    category: "Tech Trends",
    author: "Sarah Jenkins",
    liked: false
  },
  {
    id: 10,
    title: "Rising Jet Fuel Costs Strain Budget Carriers",
    summary: "Fluctuating global crude prices force regional low-cost airlines to adjust luggage pricing and seasonal flight schedules.",
    image: "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&q=80&w=600",
    date: "2026-05-18",
    category: "Economics",
    author: "Marcus Brody",
    liked: false
  },
  {
    id: 11,
    title: "New Premium Lounges Open at HCMC Airport",
    summary: "Tan Son Nhat airport reveals premium eco-friendly transit lounges featuring sleep pods and smart checkout stations.",
    image: "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&q=80&w=600",
    date: "2026-04-29",
    category: "Infrastructure",
    author: "Evelyn Vance",
    liked: false
  },
  {
    id: 12,
    title: "Airlines Adopt AI for Baggage Tracking",
    summary: "Computer vision nodes and real-time scanning systems cut missing baggage rates by over 45% during peak holiday travel.",
    image: "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=600",
    date: "2026-04-12",
    category: "Data Systems",
    author: "Sarah Jenkins",
    liked: false
  },
  {
    id: 13,
    title: "Supersonic Commercial Flights Seek Green Light",
    summary: "Aerospace firms complete noise reduction trials over offshore corridors, hoping to halve transatlantic transit times.",
    image: "https://images.unsplash.com/photo-1473830394358-91588751b241?auto=format&fit=crop&q=80&w=600",
    date: "2026-03-24",
    category: "Tech Trends",
    author: "Marcus Brody",
    liked: false
  },
  {
    id: 14,
    title: "Aviation Museum Expands Historic Fleet",
    summary: "A beautifully restored Boeing 707 from the golden era of commercial flight goes on permanent display next week.",
    image: "https://images.unsplash.com/photo-1512288094938-363287817259?auto=format&fit=crop&q=80&w=600",
    date: "2026-03-05",
    category: "Aviation News",
    author: "Evelyn Vance",
    liked: false
  },
  {
    id: 15,
    title: "Smart Tags Reusable Baggage Pilots Succeed",
    summary: "Passengers praise the electronic ink smart luggage tags that update routes automatically via Bluetooth linkages.",
    image: "https://images.unsplash.com/photo-1556909212-d5b604dadb72?auto=format&fit=crop&q=80&w=600",
    date: "2026-02-18",
    category: "Cabin Tech",
    author: "Sarah Jenkins",
    liked: false
  },
  {
    id: 16,
    title: "Clean Air Protocols Set for Aircraft Cabins",
    summary: "New HEPA filter layouts and carbon-neutral air circulation units guarantee mountain-fresh cabin air during long-hauls.",
    image: "https://images.unsplash.com/photo-1483450388369-9ed95738483c?auto=format&fit=crop&q=80&w=600",
    date: "2026-01-22",
    category: "Green Tech",
    author: "Marcus Brody",
    liked: false
  }
]);

// Extract unique categories from articles
const uniqueCategories = computed(() => {
  const categories = articles.value.map(a => a.category);
  return [...new Set(categories)].sort();
});

// Reactively filter articles based on search criteria
const filteredArticles = computed(() => {
  return articles.value.filter(article => {
    // Text search (Title or Content/Summary)
    const textMatch = !searchQuery.value || 
      article.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      article.summary.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    // Category filter
    const categoryMatch = !selectedCategory.value || 
      article.category.toLowerCase() === selectedCategory.value.toLowerCase();
    
    // Date filter
    const dateMatch = !selectedDate.value || 
      article.date === selectedDate.value;
    
    return textMatch && categoryMatch && dateMatch;
  });
});

// Paginated subset of filtered articles
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredArticles.value.slice(start, end);
});

// Calculate total pages dynamically
const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / itemsPerPage.value) || 1;
});

// Page summary index counts
const resultsStart = computed(() => {
  if (filteredArticles.value.length === 0) return 0;
  return (currentPage.value - 1) * itemsPerPage.value + 1;
});

const resultsEnd = computed(() => {
  const potentialEnd = currentPage.value * itemsPerPage.value;
  return potentialEnd > filteredArticles.value.length ? filteredArticles.value.length : potentialEnd;
});

// Page controls
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const resetPagination = () => {
  currentPage.value = 1;
};

const clearFilters = () => {
  searchQuery.value = '';
  selectedCategory.value = '';
  selectedDate.value = '';
  resetPagination();
};

const toggleLike = (article) => {
  article.liked = !article.liked;
};

// Date Formatter: YYYY-MM-DD to Month DD, YYYY
const formatDateString = (dateStr) => {
  if (!dateStr) return '';
  const dateObj = new Date(dateStr);
  return dateObj.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });
};
</script>

<style scoped>
.news-page-wrapper {
  font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--sky-bg); /* Use general beige background */
  color: var(--dark-text);
  line-height: 1.65;
  padding: 4rem 1.5rem;
  min-height: 100vh;
}

.news-main-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.news-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.news-main-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.news-main-subtitle {
  font-size: 1.25rem;
  color: var(--gray-text);
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Filter Card Styling */
.filter-card {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 4px 4px 0px var(--dark-text);
}

.filter-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 1.5rem;
  align-items: flex-end;
}

@media (max-width: 991px) {
  .filter-grid {
    grid-template-columns: 1fr 1fr;
  }
  .clear-btn-group {
    grid-column: span 2;
  }
}

@media (max-width: 575px) {
  .filter-grid {
    grid-template-columns: 1fr;
  }
  .clear-btn-group {
    grid-column: span 1;
  }
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--dark-text);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-with-icon {
  position: relative;
  width: 100%;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.1rem;
  pointer-events: none;
}

.filter-input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2.5rem;
  border: 2px solid var(--dark-text);
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 500;
  color: var(--dark-text);
  background-color: #f8fafc;
  outline: none;
  transition: border-color 0.2s ease;
}

.filter-input:focus {
  border-color: #FF5E1F;
}

input[type="date"].filter-input {
  padding-left: 1.2rem;
}

.filter-select {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 2px solid var(--dark-text);
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  color: var(--dark-text);
  background-color: #f8fafc;
  outline: none;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231e293b' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  background-size: 16px;
  transition: border-color 0.2s ease;
}

.filter-select:focus {
  border-color: #FF5E1F;
}

.btn-clear-filters {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 10px;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: var(--dark-text);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px var(--dark-text);
  width: 100%;
  text-align: center;
}

.btn-clear-filters:hover {
  transform: translateY(-2px);
  box-shadow: 4px 4px 0px var(--dark-text);
  background-color: #f1f5f9;
}

/* News Grid */
.news-grid-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem 2rem;
}

@media (max-width: 991px) {
  .news-grid-3col {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 639px) {
  .news-grid-3col {
    grid-template-columns: 1fr;
  }
}

/* Vertical Card */
.news-vertical-card {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 4px 0px var(--dark-text);
  transition: all 0.3s ease;
}

.news-vertical-card:hover {
  transform: translateY(-6px);
  box-shadow: 8px 8px 0px var(--dark-text);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-bottom: 2px solid var(--dark-text);
}

.card-img-fit {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.news-vertical-card:hover .card-img-fit {
  transform: scale(1.05);
}

.card-category-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  background-color: #FF5E1F;
  color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 50px;
  padding: 0.3rem 0.8rem;
  font-size: 0.75rem;
  font-weight: 800;
  box-shadow: 2px 2px 0px var(--dark-text);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.card-text-content {
  padding: 1.8rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-meta-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.card-date {
  font-size: 0.8rem;
  color: #FF5E1F;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.like-button-heart {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  transition: transform 0.2s ease;
  padding: 0;
  line-height: 1;
}

.like-button-heart:hover {
  transform: scale(1.2);
}

.card-headline-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
  line-height: 1.3;
}

.card-excerpt-text {
  font-size: 0.95rem;
  color: var(--gray-text);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.card-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px dashed #cbd5e1;
  font-size: 0.85rem;
  color: var(--gray-text);
  font-weight: 700;
}

/* No Results Card */
.no-results-card {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 20px;
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: 4px 4px 0px var(--dark-text);
}

.no-results-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.no-results-card h3 {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--dark-text);
  margin-bottom: 1rem;
}

.no-results-card p {
  color: var(--gray-text);
  max-width: 480px;
  margin: 0 auto 2rem;
}

/* Pagination Nav */
.pagination-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
}

.pagination-btn {
  background-color: var(--white);
  border: 2px solid var(--dark-text);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--dark-text);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 2px 2px 0px var(--dark-text);
}

.pagination-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 4px 4px 0px var(--dark-text);
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
  color: var(--white);
  box-shadow: inset 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.results-summary {
  text-align: center;
  font-size: 0.9rem;
  color: var(--gray-text);
  font-weight: 700;
  margin-top: -1rem;
}
</style>
