# Quick Reference Guide

Fast lookup guide for common tasks and frequently used code patterns.

---

## 🎯 Component Locations

```
NewsView (Premium Homepage)        → frontend/src/views/NewsView.vue
Utilities                          → frontend/src/utils/
  - composables.js                 → useNews(), useWeather()
  - validators.js                  → Form validation functions
  - dateFormatter.js               → Date formatting utilities
  - apiClient.js                   → API client for backend
```

---

## 🚀 Common Tasks

### 1. Import & Use a Composable

```javascript
import { useNews } from '@/utils/composables.js';

export default {
  setup() {
    const { articles, filteredArticles, fetchArticles } = useNews();
    
    onMounted(() => {
      fetchArticles();
    });

    return { articles, filteredArticles };
  }
};
```

### 2. Make API Call to Backend

```javascript
import { newsAPI, handleAPIError } from '@/utils/apiClient.js';
import { ref } from 'vue';

export default {
  setup() {
    const articles = ref([]);
    const isLoading = ref(false);

    const loadArticles = async () => {
      try {
        isLoading.value = true;
        const response = await newsAPI.getArticles({ limit: 10 });
        articles.value = response.data;
      } catch (error) {
        const { message } = handleAPIError(error);
        console.error(message);
      } finally {
        isLoading.value = false;
      }
    };

    return { articles, isLoading, loadArticles };
  }
};
```

### 3. Format Date in Template

```vue
<template>
  <p>Published: {{ formatDate(article.publishedAt) }}</p>
  <p>{{ formatRelativeTime(article.publishedAt) }}</p>
  <p>Read time: {{ estimateReadingTime(article.content) }} min</p>
</template>

<script setup>
import {
  formatDate,
  formatRelativeTime,
  estimateReadingTime
} from '@/utils/dateFormatter.js';

defineProps({
  article: Object
});
</script>
```

### 4. Validate Form

```javascript
import { validateForm } from '@/utils/validators.js';
import { ref } from 'vue';

export default {
  setup() {
    const formData = ref({
      email: '',
      password: '',
      name: ''
    });

    const errors = ref({});

    const validateAndSubmit = () => {
      errors.value = validateForm(formData.value, {
        email: ['required', 'email'],
        password: ['required', 'min:8'],
        name: ['required', 'min:3', 'max:50']
      });

      if (Object.keys(errors.value).length === 0) {
        // Form is valid, submit
        submitForm();
      }
    };

    return { formData, errors, validateAndSubmit };
  }
};
```

### 5. Create Responsive Grid Layout

```vue
<template>
  <div class="container my-5">
    <div class="row g-4">
      <!-- Main column: 8/12 on desktop, full on mobile -->
      <div class="col-lg-8">
        <h2>Main Content</h2>
      </div>

      <!-- Sidebar: 4/12 on desktop, full on mobile -->
      <div class="col-lg-4">
        <h2>Sidebar</h2>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
}
</style>
```

### 6. Add Hover Animation

```vue
<template>
  <div class="card-hover">Hover me</div>
</template>

<style scoped>
.card-hover {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-hover:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}
</style>
```

---

## 📋 Composables Reference

### useNews()

```javascript
const {
  articles,           // Array: All articles
  isLoading,          // Boolean: Loading state
  error,              // String: Error message
  selectedCategory,   // String: Active category filter
  searchQuery,        // String: Search query
  filteredArticles,   // Computed: Filtered results
  featuredArticle,    // Computed: Featured article
  topStories,         // Computed: Top 3 stories
  fetchArticles,      // Function: Fetch articles
  filterByCategory,   // Function: Filter by category
  searchArticles      // Function: Search articles
} = useNews();
```

### useWeather()

```javascript
const {
  weatherData,   // Object: { temperature, city, condition, humidity, windSpeed }
  isLoading,     // Boolean: Loading state
  error,         // String: Error message
  fetchWeather   // Function: Fetch weather data
} = useWeather();

// Usage
fetchWeather(10.7769, 106.7009); // Ho Chi Minh City coordinates
```

---

## 🔌 API Client Reference

### News API

```javascript
import { newsAPI } from '@/utils/apiClient.js';

// Get all articles
const response = await newsAPI.getArticles({ 
  category: 'Climate',
  skip: 0,
  limit: 10 
});

// Get single article
const article = await newsAPI.getArticle(1);

// Create article
await newsAPI.createArticle({
  title: 'My Article',
  content: 'Content here',
  category: 'Climate'
});

// Update article
await newsAPI.updateArticle(1, { title: 'Updated Title' });

// Delete article
await newsAPI.deleteArticle(1);

// Search articles
const results = await newsAPI.searchArticles('climate change');
```

### Weather API

```javascript
import { weatherAPI } from '@/utils/apiClient.js';

// Current weather
const current = await weatherAPI.getCurrentWeather(10.7769, 106.7009);

// Forecast (7 days)
const forecast = await weatherAPI.getForecast(10.7769, 106.7009, 7);

// Historical data
const historical = await weatherAPI.getHistoricalData(
  10.7769, 
  106.7009, 
  '2026-06-01'
);

// Weather alerts
const alerts = await weatherAPI.getAlerts(10.7769, 106.7009);
```

### Authentication API

```javascript
import { authAPI } from '@/utils/apiClient.js';

// Login
const login = await authAPI.login('user@example.com', 'password');

// Register
await authAPI.register({
  email: 'newuser@example.com',
  password: 'password',
  name: 'John Doe'
});

// Get profile
const profile = await authAPI.getProfile();

// Update profile
await authAPI.updateProfile({ name: 'Jane Doe' });

// Logout
await authAPI.logout();
```

---

## ✅ Validators Reference

```javascript
import {
  isValidEmail,
  isValidPhone,
  isValidUrl,
  isEmpty,
  isEmptyObject,
  validateForm
} from '@/utils/validators.js';

// Individual validators
isValidEmail('user@example.com');        // true/false
isValidPhone('+1-234-567-8900');        // true/false
isValidUrl('https://example.com');      // true/false
isEmpty('   ');                         // true
isEmptyObject({});                      // true

// Form validation
const errors = validateForm(
  { email: '', password: '', name: 'John' },
  {
    email: ['required', 'email'],
    password: ['required', 'min:8', 'max:32'],
    name: ['required', 'min:3', 'max:50']
  }
);
// Returns: { email: 'email is required', password: 'password is required' }
```

---

## 📅 Date Formatter Reference

```javascript
import {
  formatRelativeTime,
  formatDate,
  formatShortDate,
  formatDateTime,
  estimateReadingTime
} from '@/utils/dateFormatter.js';

// Relative time
formatRelativeTime(new Date(Date.now() - 2 * 60 * 60 * 1000));
// "2 hours ago"

// Full date
formatDate('2026-06-01');
// "June 1, 2026"

// Short date
formatShortDate('2026-06-01');
// "Jun 1, 2026"

// Date and time
formatDateTime('2026-06-01T14:30:00');
// "June 1, 2026 2:30 PM"

// Reading time
estimateReadingTime(articleText, 200);  // 200 words per minute
// 5
```

---

## 🎨 Bootstrap Classes Quick Reference

### Grid System
```html
<!-- 2-column layout: 8/4 on desktop, full on mobile -->
<div class="row g-4">
  <div class="col-lg-8">Main</div>
  <div class="col-lg-4">Sidebar</div>
</div>

<!-- 3-column grid -->
<div class="row">
  <div class="col-md-4">Column 1</div>
  <div class="col-md-4">Column 2</div>
  <div class="col-md-4">Column 3</div>
</div>
```

### Utilities
```html
<!-- Spacing: m (margin), p (padding) -->
<div class="m-4">Margin all sides</div>
<div class="mt-3">Margin top</div>
<div class="px-4">Padding left/right</div>

<!-- Text -->
<h1 class="text-center">Centered heading</h1>
<p class="text-muted">Muted gray text</p>
<p class="text-danger">Red text</p>

<!-- Display -->
<div class="d-flex justify-content-between align-items-center">
  Content
</div>

<!-- Responsive display -->
<div class="d-none d-lg-block">Visible only on desktop</div>
```

### Common Components
```html
<!-- Button -->
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-outline-secondary">Secondary</button>

<!-- Badge -->
<span class="badge bg-success">Success</span>
<span class="badge bg-danger">Danger</span>

<!-- Card -->
<div class="card">
  <div class="card-body">Content</div>
</div>
```

---

## 🐛 Error Handling Pattern

```javascript
import { handleAPIError } from '@/utils/apiClient.js';
import { ref } from 'vue';

export default {
  setup() {
    const isLoading = ref(false);
    const error = ref(null);

    const fetchData = async () => {
      try {
        isLoading.value = true;
        error.value = null;
        
        const response = await someAPICall();
        return response.data;
      } catch (err) {
        const { message } = handleAPIError(err);
        error.value = message;
        console.error('API Error:', message);
      } finally {
        isLoading.value = false;
      }
    };

    return { isLoading, error, fetchData };
  }
};
```

---

## 📁 File Organization

**When to create new files:**
- ✅ Reusable components → `components/` folder
- ✅ Page layouts → `views/` folder
- ✅ Utility functions → `utils/` folder
- ✅ Styles → `assets/css/` folder
- ✅ Images → `assets/images/` folder

**Naming conventions:**
- Components: `PascalCase.vue` (e.g., `ArticleCard.vue`)
- Composables: `camelCase.js` (e.g., `useNews.js`)
- Other utils: `camelCase.js` (e.g., `validators.js`)
- Views: `PascalCaseView.vue` (e.g., `NewsView.vue`)

---

## 🚀 Deployment Checklist

- [ ] All env variables set in `.env.local`
- [ ] No console.log() left in code
- [ ] Images optimized and paths correct
- [ ] API calls use environment variables
- [ ] Forms validated on both client & server
- [ ] Error handling implemented
- [ ] Mobile responsive tested
- [ ] Build succeeds: `npm run build`
- [ ] Production preview works: `npm run preview`

---

## 📞 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Module not found | Check import path, run `npm install` |
| Styles not loading | Restart dev server, clear browser cache |
| API 404 errors | Verify backend is running, check endpoint URL |
| CORS errors | Add to backend CORS middleware |
| Props not updating | Use `ref()` or `computed()` for reactivity |
| Event not firing | Check `@click` vs `@keydown`, use event modifiers |

---

**Last Updated**: June 2026  
**Status**: Ready for Development
