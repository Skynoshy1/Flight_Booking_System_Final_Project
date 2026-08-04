# Weather-News Monorepo 🌍📰

A modern full-stack monorepo for a **climate-focused news portal** with real-time weather integration. Built for **Assignment 1, 2, and 3** of COS30043.

**Tech Stack:**
- **Frontend**: Vue 3 + Bootstrap 5 + Vite
- **Backend**: FastAPI (Python)
- **Data**: Mock JSON + OpenMeteo Weather API
- **Deployment**: Ready for Azure

---

## 📁 Project Structure

```
weather-news-monorepo/
│
├── frontend/                      # Vue 3 frontend (Assignment 1 & 2)
│   ├── src/
│   │   ├── views/
│   │   │   ├── NewsView.vue       # ⭐ Premium news homepage
│   │   │   ├── Assignment1View.vue
│   │   │   ├── WeatherView.vue
│   │   │   └── AdminView.vue
│   │   ├── components/            # Reusable components (Atomic Design)
│   │   │   ├── common/            # Navbar, Footer
│   │   │   ├── news/              # News cards, articles
│   │   │   ├── weather/           # Weather widgets
│   │   │   └── event/             # Event components
│   │   ├── router/                # Vue Router
│   │   ├── utils/                 # Composables & utilities
│   │   │   ├── composables.js     # useNews(), useWeather()
│   │   │   ├── validators.js      # Form validation
│   │   │   └── dateFormatter.js   # Date utilities
│   │   └── App.vue                # Root component
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── backend/                       # FastAPI backend (Assignment 2-3)
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── api/
│   │   │   ├── weather.py         # Weather endpoints
│   │   │   └── news.py            # News CRUD endpoints
│   │   ├── models/                # Database models
│   │   ├── services/              # Business logic & external APIs
│   │   └── core/                  # Config & security
│   ├── requirements.txt
│   └── README.md
│
├── shared-data/                   # Mock data for prototyping
│   ├── events.json                # Event data (Assignment 1)
│   └── news.json                  # News articles (Assignment 2+)
│
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend - optional for frontend-only dev)

### Frontend Only (Assignment 1)

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### Full Stack (Assignment 2-3)

```bash
# Terminal 1: Frontend
cd frontend
npm install
npm run dev

# Terminal 2: Backend
cd backend
pip install -r requirements.txt
python app/main.py

# Frontend at http://localhost:5173
# Backend API at http://localhost:8000
# API Docs at http://localhost:8000/docs
```

---

## ⭐ Featured: Premium News Homepage

**NewsView.vue** - A high-fidelity news portal inspired by MSN News & Dân Trí:

### Design Highlights
✨ **Sticky Navbar**
- Brand logo with serif typography
- Category pills (World, Climate, Technology, Energy, Science)
- Search with glassmorphic weather widget
- Notification bell & profile avatar

📰 **Hero Section**
- Large featured image with "BREAKING" badge
- Massive serif headline with premium typography
- Article metadata (category, time, read time)
- Article excerpt

📋 **Top Stories Sidebar**
- 3 numbered story cards (01, 02, 03)
- Category badges for each story
- Metadata (time ago, read time)
- Thumbnail images

### Visual Design
- **Background**: Soft off-white (#F9F9F6)
- **Fonts**: Playfair Display (serif) + Inter (sans-serif)
- **Hover Effects**: Smooth lift animation (translateY -3px)
- **Animations**: Fade-in on page load

### Responsive
- ✅ Mobile (< 576px)
- ✅ Tablet (< 992px)
- ✅ Desktop (≥ 992px)

---

## 🎯 Assignment Breakdown

### **ASSIGNMENT 1**: Event Portal
**Status**: ✅ View-level Complete | ⏳ Integration Pending

**Deliverable**: Responsive event management website
- Event table with sorting/filtering
- Event registration form with dropdowns
- Responsive grid design

**View**: `frontend/src/views/Assignment1View.vue`

### **ASSIGNMENT 2**: News Portal
**Status**: 🔄 In Progress

**Deliverable**: Full CRUD news system with admin panel
- Article listing & filtering (NewsView.vue)
- Journalist/Admin article editor
- Real-time updates via API

**Backend Endpoints**:
```
GET    /api/news              # List articles
GET    /api/news/{id}         # Get article
POST   /api/news              # Create (admin)
PUT    /api/news/{id}         # Update (admin)
DELETE /api/news/{id}         # Delete (admin)
```

### **ASSIGNMENT 3**: Weather Dashboard
**Status**: ⏳ Planned

**Deliverable**: Real-time weather analytics with Azure deployment
- Weather charts & forecasts (Chart.js)
- Historical data analysis
- Azure Container Apps ready

**Backend Endpoints**:
```
GET    /api/weather/current           # Current conditions
GET    /api/weather/forecast          # 7-day forecast
GET    /api/weather/historical/{date} # Historical data
```

---

## 📦 Available Utilities

### Composables (`utils/composables.js`)

**useNews()**
```javascript
const {
  articles,          // All articles
  filteredArticles,  // After search
  featuredArticle,   // Featured article
  topStories,        // Top 3 stories
  isLoading,
  error,
  fetchArticles,
  filterByCategory,
  searchArticles
} = useNews();
```

**useWeather()**
```javascript
const {
  weatherData,  // { temperature, city, condition, ... }
  isLoading,
  error,
  fetchWeather
} = useWeather();
```

### Validators (`utils/validators.js`)
```javascript
isValidEmail(email)         // true/false
isValidPhone(phone)         // true/false
isValidUrl(url)             // true/false
validateForm(data, rules)   // { errors object }
```

### Date Utilities (`utils/dateFormatter.js`)
```javascript
formatRelativeTime(date)   // "2 hours ago"
formatDate(date)           // "January 15, 2026"
formatShortDate(date)      // "Jan 15, 2026"
formatDateTime(date)       // "January 15, 2026 2:30 PM"
estimateReadingTime(text)  // minutes (number)
```

---

## 🔌 Integration Guide

### Connect Frontend to Backend

**1. Set API URL** (`frontend/.env.local`):
```
VITE_API_URL=http://localhost:8000/api
```

**2. Update composables** (`frontend/src/utils/composables.js`):
```javascript
// Replace mock data with API calls
const response = await fetch(`${import.meta.env.VITE_API_URL}/news`);
const data = await response.json();
articles.value = data;
```

**3. Use in component**:
```javascript
import { useNews } from '@/utils/composables.js';

const { articles, fetchArticles } = useNews();
onMounted(() => fetchArticles());
```

---

## 📝 Development Commands

### Frontend
```bash
cd frontend

npm run dev        # Start dev server (http://localhost:5173)
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Lint code
```

### Backend (when ready)
```bash
cd backend

# Run with hot reload
uvicorn app.main:app --reload

# Access API documentation
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

---

## 📖 Key Files Reference

| File | Purpose |
|------|---------|
| `frontend/src/views/NewsView.vue` | Premium news homepage |
| `frontend/src/router/index.js` | Route configuration |
| `frontend/src/utils/composables.js` | Data management |
| `frontend/App.vue` | Root component |
| `backend/app/main.py` | FastAPI application |
| `shared-data/news.json` | Mock news data |

---

## ☁️ Azure Deployment

Frontend ready for **Azure Static Web Apps**:
```bash
cd frontend
npm run build
# Deploy dist/ folder
```

Backend ready for **Azure Container Apps**:
```bash
cd backend
# Build Docker image and deploy
```

---

## 🐛 Troubleshooting

**Port already in use?**
```bash
npx kill-port 5173    # Frontend
npx kill-port 8000    # Backend
```

**CORS errors?** Add to backend:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"])
```

**Styles not loading?** Clear cache & rebuild:
```bash
rm -rf frontend/node_modules
cd frontend && npm install && npm run dev
```

---

## 📚 Resources

- [Vue 3 Documentation](https://vuejs.org)
- [Bootstrap 5](https://getbootstrap.com)
- [FastAPI](https://fastapi.tiangolo.com)
- [Vite](https://vitejs.dev)

---

## 📅 Timeline

| Phase | Status | Deadline |
|-------|--------|----------|
| Assignment 1 (Event Portal) | ✅ View complete | - |
| Assignment 2 (News Portal) | 🔄 In Progress | - |
| Assignment 3 (Weather + Azure) | ⏳ Planned | - |

---

**Last Updated**: June 2026 | **Status**: 🚀 In Development | **Course**: COS30043
