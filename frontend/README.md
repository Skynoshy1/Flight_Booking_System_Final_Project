# Frontend - Meridian News Portal

Modern news portal frontend built with **Vue 3**, **Bootstrap 5**, and **Vite**.

## 📋 Project Structure

```
frontend/
├── public/                  # Static assets (favicon, manifest)
├── src/
│   ├── assets/             # Images, CSS, media files
│   │   ├── css/            # Custom CSS overrides
│   │   └── images/         # Images and logos
│   ├── components/         # Reusable Vue components (Atomic Design)
│   │   ├── common/         # Shared components (Navbar, Footer)
│   │   ├── news/           # News-related components
│   │   ├── weather/        # Weather-related components
│   │   └── event/          # Event-related components
│   ├── views/              # Page-level components
│   │   ├── NewsView.vue    # **Main news homepage (Premium layout)**
│   │   ├── Assignment1View.vue
│   │   ├── WeatherView.vue
│   │   └── AdminView.vue
│   ├── router/
│   │   └── index.js        # Vue Router configuration
│   ├── utils/              # Utility functions and composables
│   │   ├── dateFormatter.js # Date formatting utilities
│   │   ├── validators.js   # Form validation functions
│   │   └── composables.js  # Vue composables for data management
│   ├── App.vue             # Root component
│   ├── main.js             # Application entry point
│   └── style.css           # Global styles (imported by main.js)
├── index.html              # HTML entry point
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
└── README.md               # This file

```

## 🎨 Design System

### Colors
- **Background**: `#F9F9F6` (Soft off-white/beige)
- **Primary Text**: `#1a1a1a` (Near black)
- **Muted Text**: `#666666` (Gray)
- **Border Light**: `#EAEAEA` (Light gray)
- **Accent**: `rgba(218, 236, 254, 0.6)` (Light blue - glassmorphic)
- **Badge**: `#DC3545` (Red for breaking news)

### Typography
- **Serif (Premium)**: `Playfair Display` / `Georgia` - Headlines, branding
- **Sans-serif (Clean)**: `Inter` / `Roboto` - Body text, navigation

### Animations & Interactions
- **Hover Effect**: `transform: translateY(-3px)` with smooth shadow
- **Transition**: `0.2s ease` for all interactions
- **Page Load**: Fade-in animation `0.5s ease-in-out`

---

## 🚀 Quick Start

### Installation
```bash
cd frontend
npm install
```

### Development Server
```bash
npm run dev
```
Server runs at `http://localhost:5173`

### Build Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

---

## 📦 Key Dependencies

```json
{
  "vue": "^3.4.0",           // Vue 3 framework
  "vue-router": "^4.2.0",    // Client-side routing
  "bootstrap": "^5.3.0",     // Bootstrap 5 CSS framework
  "axios": "^1.6.0"          // HTTP client for API calls
}
```

---

## 🎯 Components & Views

### `NewsView.vue` (Premium Homepage)
The main news homepage featuring:
- **Sticky Navbar** with category pills, search, weather widget
- **Hero Section** with featured article and breaking badge
- **Top Stories** sidebar with 3 numbered story cards
- Responsive design (mobile-first)
- Glassmorphic weather widget with backdrop blur
- Premium serif typography for headlines

**Usage:**
```vue
<template>
  <NewsView />
</template>

<script setup>
import NewsView from '@/views/NewsView.vue';
</script>
```

---

## 📚 Utilities & Composables

### Date Formatter (`utils/dateFormatter.js`)

```javascript
import {
  formatRelativeTime,   // "2 hours ago"
  formatDate,          // "January 15, 2026"
  formatShortDate,     // "Jan 15, 2026"
  formatDateTime,      // "January 15, 2026 2:30 PM"
  estimateReadingTime  // Returns minutes
} from '@/utils/dateFormatter.js';

// Example usage
const relativeTime = formatRelativeTime(new Date());
const readTime = estimateReadingTime(articleText); // minutes
```

### Validators (`utils/validators.js`)

```javascript
import {
  isValidEmail,
  isValidPhone,
  isValidUrl,
  isEmpty,
  isEmptyObject,
  validateForm
} from '@/utils/validators.js';

// Example: Validate form
const errors = validateForm(
  { email: 'test@example.com', name: 'John' },
  { email: ['required', 'email'], name: ['required', 'min:3', 'max:50'] }
);
```

### Composables (`utils/composables.js`)

#### `useNews()`
Manage news articles with filtering and search.

```javascript
import { useNews } from '@/utils/composables.js';

export default {
  setup() {
    const {
      articles,           // All articles
      filteredArticles,   // After search/filter
      featuredArticle,    // Featured article
      topStories,         // Top 3 stories
      isLoading,
      error,
      fetchArticles,
      filterByCategory,
      searchArticles
    } = useNews();

    onMounted(() => {
      fetchArticles(); // Fetch all articles
    });

    return { articles, filteredArticles, isLoading };
  }
};
```

#### `useWeather()`
Fetch and manage weather data.

```javascript
import { useWeather } from '@/utils/composables.js';

export default {
  setup() {
    const { weatherData, isLoading, fetchWeather } = useWeather();

    onMounted(() => {
      fetchWeather(10.7769, 106.7009); // Latitude, Longitude
    });

    return { weatherData, isLoading };
  }
};
```

---

## 🔌 API Integration

### Backend Connection
The frontend communicates with the backend via REST API:

```javascript
// Example API structure (to be implemented)
GET  /api/news                 // Fetch all articles
GET  /api/news/:id             // Fetch article by ID
POST /api/news                 // Create article (Admin)
PUT  /api/news/:id             // Update article (Admin)
DELETE /api/news/:id           // Delete article (Admin)
GET  /api/weather              // Fetch weather data
GET  /api/categories           // Fetch news categories
```

### Update Composables
Replace mock data in `utils/composables.js` with actual API calls:

```javascript
const response = await fetch('/api/news');
const data = await response.json();
articles.value = data;
```

Or use **axios**:
```javascript
import axios from 'axios';

const { data } = await axios.get('/api/news');
articles.value = data;
```

---

## 📱 Responsive Breakpoints

```css
/* Bootstrap breakpoints used */
xs: < 576px    (Mobile phones)
sm: ≥ 576px    (Landscape phones)
md: ≥ 768px    (Tablets)
lg: ≥ 992px    (Desktops) /* Main breakpoint for 2-column */
xl: ≥ 1200px   (Large desktops)
xxl: ≥ 1400px  (Extra large screens)
```

**Key responsive changes in NewsView:**
- **Mobile**: Single-column, hidden weather widget, stacked stories
- **Tablet**: Category pills become scrollable
- **Desktop**: 2-column layout (8/4), full navbar features

---

## 🎨 Custom CSS Classes

All styling is **scoped** to prevent conflicts.

### Common utility classes:
```css
.fade-in        /* Fade-in animation */
.hover-lift     /* Lift effect on hover */
.glass-effect   /* Glassmorphic background */
.premium-text   /* Premium serif font */
.badge-danger   /* Red badge styling */
```

---

## 🔐 Security Best Practices

✅ **XSS Protection**: Vue 3 auto-escapes template content  
✅ **CSRF**: Include tokens in API requests  
✅ **Validation**: Both client-side and server-side  
✅ **Environment Variables**: Use `.env` for API URLs  

**Example `.env`:**
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Meridian
```

**Usage in code:**
```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

---

## 📝 Git Workflow

```bash
# Create a feature branch
git checkout -b feature/news-homepage

# Make changes, then commit
git add .
git commit -m "feat: add premium news homepage"

# Push to remote
git push origin feature/news-homepage

# Create Pull Request on GitHub
```

---

## 🐛 Troubleshooting

### Styles not loading?
- Check `main.js` imports Bootstrap and CSS
- Clear browser cache (`Ctrl+Shift+R`)

### Images not showing?
- Verify paths in `public/` or `src/assets/`
- Use relative paths: `./images/logo.png`

### Router not working?
- Ensure routes are defined in `router/index.js`
- Check `<router-view />` is in `App.vue`

### API calls failing?
- Check backend is running on correct port
- Verify CORS headers in backend
- Check network tab in DevTools

---

## 📞 Support & Contact

For questions or issues:
- Check project README in monorepo root
- Review Vue 3 docs: https://vuejs.org
- Bootstrap 5 docs: https://getbootstrap.com

---

**Last Updated**: June 2026  
**Vue Version**: 3.4+  
**Bootstrap Version**: 5.3+
