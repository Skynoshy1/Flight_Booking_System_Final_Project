# Development Guide

Complete guide for developing the Weather-News Monorepo locally.

---

## 🛠️ Local Setup

### Prerequisites Check

```bash
# Check Node.js version (need 18+)
node --version

# Check npm version
npm --version

# Check Python version (need 3.10+)
python --version
```

### Initial Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd weather-news-monorepo

# Initialize git (if not cloned)
git init

# Create local branches
git checkout -b develop
```

---

## 📦 Frontend Development

### Installation

```bash
cd frontend

# Install dependencies
npm install

# Optional: Use specific package manager
yarn install
# or
pnpm install
```

### Scripts Available

```json
{
  "dev": "vite",                    // Start dev server
  "build": "vite build",            // Build for production
  "preview": "vite preview",        // Preview production build
  "lint": "eslint . --fix",         // Lint and fix
  "type-check": "vue-tsc --noEmit"  // Type checking
}
```

### Development Workflow

```bash
# 1. Start dev server
npm run dev

# 2. Browser opens automatically at http://localhost:5173
# 3. Make changes - hot reload happens automatically
# 4. Open browser DevTools (F12) to debug
```

### Environment Variables

Create `.env.local` in `frontend/`:

```env
# API Configuration
VITE_API_URL=http://localhost:8000/api

# App Settings
VITE_APP_NAME=Meridian
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_ADMIN_PANEL=true
```

### Project Structure

```
frontend/src/
├── components/
│   ├── common/          # Shared components (Navbar, Footer)
│   ├── news/            # News-specific components
│   ├── weather/         # Weather widgets
│   └── event/           # Event management components
│
├── views/
│   ├── NewsView.vue     # Main news homepage
│   ├── Assignment1View.vue
│   ├── WeatherView.vue
│   └── AdminView.vue
│
├── router/
│   └── index.js         # Route definitions
│
├── utils/
│   ├── composables.js   # Vue composables
│   ├── validators.js    # Validation functions
│   └── dateFormatter.js # Date utilities
│
├── assets/
│   ├── css/             # Custom styles
│   └── images/          # Images and logos
│
├── App.vue              # Root component
└── main.js              # Entry point
```

### Component Creation Guide

**1. Create new component** (e.g., `ArticleCard.vue`):

```vue
<template>
  <article class="article-card" @click="handleClick">
    <img :src="article.image" :alt="article.title" class="card-image">
    <h3 class="card-title">{{ article.title }}</h3>
    <p class="card-meta">{{ formattedDate }} • {{ article.readTime }} min</p>
  </article>
</template>

<script setup>
import { computed } from 'vue';
import { formatRelativeTime } from '@/utils/dateFormatter';

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['click']);

const formattedDate = computed(() => {
  return formatRelativeTime(props.article.publishedAt);
});

const handleClick = () => {
  emit('click', props.article.id);
};
</script>

<style scoped>
.article-card {
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.article-card:hover {
  transform: translateY(-4px);
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 12px;
}

.card-meta {
  font-size: 0.85rem;
  color: #666;
  margin: 0 12px 12px;
}
</style>
```

**2. Use in view**:

```javascript
import ArticleCard from '@/components/news/ArticleCard.vue';

const handleArticleClick = (id) => {
  router.push(`/article/${id}`);
};
```

---

## 🔌 Backend Development

### Installation

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# With auto-reload (recommended for development)
uvicorn app.main:app --reload

# Without reload
uvicorn app.main:app

# Access documentation:
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app initialization
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── news.py       # News endpoints
│   │   └── weather.py    # Weather endpoints
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── article.py    # Article model
│   │   └── weather.py    # Weather model
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── news_service.py      # Business logic
│   │   └── weather_service.py   # Weather API integration
│   │
│   └── core/
│       ├── __init__.py
│       ├── config.py    # Configuration
│       └── security.py  # Authentication
│
├── requirements.txt
└── README.md
```

### Creating an Endpoint

**Example: Get all news articles**

```python
# backend/app/api/news.py
from fastapi import APIRouter, Query
from typing import List

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/")
async def get_articles(
    category: str = Query(None),
    skip: int = 0,
    limit: int = 10
) -> List[dict]:
    """Get all news articles with optional filtering"""
    # TODO: Implement with database
    return [
        {
            "id": 1,
            "title": "Article Title",
            "category": "Climate",
            "publishedAt": "2026-06-01T10:00:00Z"
        }
    ]

@router.get("/{id}")
async def get_article(id: int) -> dict:
    """Get single article by ID"""
    return {"id": id, "title": "Article Title"}

@router.post("/")
async def create_article(article: dict) -> dict:
    """Create new article (admin only)"""
    return {"id": 1, "created": True}
```

**Include in main.py**:

```python
from app.api import news, weather

app.include_router(news.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
```

### CORS Configuration

```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔄 Git Workflow

### Creating Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/article-cards
# or
git checkout -b feat/article-cards

# Make changes...
git add .
git commit -m "feat: add reusable article card component"
git push origin feature/article-cards
```

### Commit Message Convention

```
feat: add new feature
fix: fix a bug
docs: documentation changes
style: code style changes (no logic)
refactor: code refactoring
test: add or update tests
chore: dependencies, build, etc.

Examples:
- feat: add premium news homepage layout
- fix: correct navbar hover animation timing
- docs: update setup instructions
```

### Creating Pull Request

```bash
# After pushing to remote
# Go to GitHub and click "Create Pull Request"

# Or use GitHub CLI:
gh pr create --title "Premium news homepage" --body "Adds NewsView.vue with..."
```

---

## 📊 Code Style & Linting

### ESLint Configuration

Create `.eslintrc.cjs` in frontend:

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2021: true },
  extends: ['plugin:vue/vue3-essential', 'eslint:recommended'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  rules: {
    'vue/multi-word-component-names': 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
};
```

### Prettier Configuration

Create `.prettierrc` in frontend:

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2
}
```

### Format Code

```bash
cd frontend

# Check formatting
npx prettier --check .

# Auto-format
npx prettier --write .

# Lint and fix
npm run lint
```

---

## 🧪 Testing (Future)

### Unit Testing with Vitest

```bash
npm install -D vitest @vue/test-utils
```

**Example test** (`tests/components/ArticleCard.spec.js`):

```javascript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import ArticleCard from '@/components/news/ArticleCard.vue';

describe('ArticleCard.vue', () => {
  it('renders article title', () => {
    const props = {
      article: {
        id: 1,
        title: 'Test Article',
        image: 'test.jpg',
        publishedAt: new Date(),
        readTime: 5
      }
    };

    const wrapper = mount(ArticleCard, { props });
    expect(wrapper.text()).toContain('Test Article');
  });
});
```

---

## 🔐 Security Best Practices

### Frontend
- ✅ Never store sensitive data in localStorage
- ✅ Use HTTPS for API calls in production
- ✅ Validate user input before sending to API
- ✅ Escape user-generated content (Vue auto-escapes)

### Backend
- ✅ Validate all incoming data
- ✅ Use environment variables for secrets
- ✅ Implement CORS properly
- ✅ Add authentication/authorization
- ✅ Rate limiting on public endpoints

### Secrets Management

```bash
# Create .env file (DO NOT COMMIT)
echo ".env" >> .gitignore

# .env example
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key-here
API_KEY=openweather-api-key
```

---

## 🐛 Debugging

### Frontend Debugging

```javascript
// Vue DevTools browser extension
// https://devtools.vuejs.org

// Console logging
console.log('Data:', data);
console.table(articles); // Table format

// Debugger statement
debugger; // Pauses execution

// Watch expressions in DevTools
```

### Backend Debugging

```python
# Use FastAPI automatic docs
# http://localhost:8000/docs

# FastAPI logger
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")

# Python debugger
import pdb; pdb.set_trace()
```

---

## 📱 Testing Responsiveness

### Chrome DevTools

```
F12 → Device Toolbar (Ctrl+Shift+M)
→ Select device or custom dimensions
```

### Responsive Breakpoints

```css
/* Mobile First */
xs: < 576px
sm: 576px - 767px
md: 768px - 991px
lg: 992px - 1199px
xl: 1200px - 1399px
xxl: > 1400px
```

### Test Across Browsers

- Chrome/Chromium (DevTools)
- Firefox (DevTools: F12)
- Safari (Develop menu: ⌘+Option+I)
- Mobile Safari (on Mac: Safari → Develop → iPhone Simulator)

---

## 🚀 Build & Deployment Preview

### Frontend Production Build

```bash
cd frontend

# Build
npm run build

# Output: dist/ folder
# Serve locally to test:
npm run preview

# Deploy to Azure Static Web Apps
# Or any static hosting (Vercel, Netlify, GitHub Pages)
```

### Backend Containerization

```bash
cd backend

# Build Docker image
docker build -t news-api:latest .

# Run container
docker run -p 8000:8000 news-api:latest
```

---

## 📚 Additional Resources

- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Bootstrap Grid System](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Vite Configuration](https://vitejs.dev/config/)

---

**Last Updated**: June 2026  
**Status**: Development Guide v1.0
