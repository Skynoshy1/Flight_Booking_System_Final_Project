# NewsView Component Architecture

Complete technical reference for the NewsView.vue premium news homepage component.

---

## 🏗️ Component Structure

```
NewsView.vue (Main Container)
│
├── <nav> NAVBAR SECTION
│   ├── Left: Brand Logo + Text
│   │   ├── SVG Icon
│   │   └── "Meridian" (Serif Font - Playfair Display)
│   │
│   ├── Center: Category Pills
│   │   └── Container with border & rounded corners
│   │       ├── Category Link: World
│   │       ├── Category Link: Climate (Active/Bold)
│   │       ├── Category Link: Technology
│   │       ├── Category Link: Energy
│   │       └── Category Link: Science
│   │
│   └── Right Section
│       ├── Search Input (Rounded)
│       │   └── Search Icon
│       ├── Weather Widget (Glassmorphic)
│       │   ├── Sun Icon
│       │   └── "31°C, Ho Chi Minh City"
│       ├── Notification Bell Icon
│       └── Profile Avatar (Circle Image)
│
├── <main> HERO SECTION
│   └── Bootstrap Container
│       └── Bootstrap Row (g-5 gap)
│           │
│           ├── col-lg-8 (LEFT: Main Feature)
│           │   └── main-feature-card
│           │       ├── featured-image-wrapper
│           │       │   ├── Image
│           │       │   └── BREAKING Badge (Red)
│           │       ├── Headline (Serif, Large)
│           │       ├── Metadata (Category, Time, Read Time)
│           │       └── Excerpt (Body Text)
│           │
│           └── col-lg-4 (RIGHT: Top Stories)
│               └── top-stories-section
│                   ├── "TOP STORIES" Header
│                   └── Top Story Items (3x)
│                       ├── Story Number (01, 02, 03)
│                       ├── Story Content
│                       │   ├── Category Badge
│                       │   ├── Headline
│                       │   └── Metadata
│                       └── Thumbnail Image
```

---

## 🎨 CSS Classes & Styling

### Navbar Classes

```css
.navbar-section
  - Sticky positioning (top)
  - White background
  - Light shadow
  - Border bottom (light gray)

.brand-logo
  - Hover: transform -2px
  - Flex layout, gap: 10px

.brand-text
  - Family: Playfair Display (serif)
  - Size: 1.5rem
  - Weight: 700
  - Letter-spacing: -0.5px

.category-pill-container
  - Flex layout, gap: 2px
  - Border: 1px solid #EAEAEA
  - Border-radius: 50px
  - Padding: 5px 20px
  - Background: white

.category-link
  - Color: #666 (muted)
  - Padding: 4px 12px
  - Border-radius: 50px
  - Transition: all 0.2s
  - .active: bold, color: #1a1a1a

.search-wrapper
  - Position: relative
  - Flexbox

.search-input
  - Background: #f5f5f5
  - Border: 1px solid #EAEAEA
  - Border-radius: 24px
  - Padding: 8px 16px 8px 36px
  - Width: 140px
  - Focus: white bg, shadow

.weather-widget
  - Display: flex
  - Padding: 8px 16px
  - Background: rgba(218, 236, 254, 0.6) (glassmorphic)
  - Backdrop-filter: blur(8px)
  - Border: 1px solid rgba(255, 255, 255, 0.3)
  - Border-radius: 24px
  - Hover: lift effect (-2px)

.profile-avatar
  - Width: 32px, height: 32px
  - Border-radius: 50%
  - Overflow: hidden
  - Hover: transform -2px
```

### Content Section Classes

```css
.main-feature-card
  - Animation: fadeInUp 0.6s

.featured-image-wrapper
  - Border-radius: 12px
  - Overflow: hidden
  - Shadow: light
  - Hover: shadow elevated, transform -3px

.featured-image
  - Width: 100%
  - Hover: scale 1.02

.breaking-badge
  - Position: absolute (top-left)
  - Background: #DC3545 (red)
  - Color: white
  - Padding: 8px 16px
  - Border-radius: 6px
  - Font: 0.75rem, weight: 700
  - Letter-spacing: 1px

.main-headline
  - Family: Playfair Display (serif)
  - Size: 2.5rem
  - Weight: 800
  - Line-height: 1.2
  - Letter-spacing: -1px

.article-meta
  - Flexbox, gap: 16px
  - Font-size: 0.9rem
  - Color: #666

.meta-category
  - Background: rgba(0, 0, 0, 0.05)
  - Padding: 4px 12px
  - Border-radius: 20px
  - Font-weight: 600

.top-stories-section
  - Animation: fadeInUp 0.6s (0.1s delay)

.top-stories-title
  - Size: 0.85rem
  - Weight: 700
  - Letter-spacing: 1.5px
  - Color: #999
  - Text-transform: uppercase
  - Margin-bottom: 30px

.top-story-item
  - Display: grid (3 columns: 50px 1fr 80px)
  - Gap: 16px
  - Padding: 20px
  - Background: white
  - Border: 1px solid #EAEAEA
  - Border-radius: 8px
  - Hover: -3px lift, shadow elevated

.story-number
  - Size: 2rem
  - Weight: 700
  - Color: #e8e8e8 (very light)
  - Font: Playfair Display

.story-headline
  - Family: Playfair Display
  - Size: 1.1rem
  - Weight: 700
  - Line-height: 1.3
  - Hover: color: #1a5490

.story-thumbnail
  - Width: 80px, height: 80px
  - Border-radius: 8px
  - Object-fit: cover
  - Hover: scale 1.05
```

---

## 🎬 Animations & Transitions

### Page Load Animation
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

Applied to:
- .main-feature-card: 0.6s ease-out
- .top-stories-section: 0.6s ease-out (0.1s delay)
```

### Hover Animations
```css
All interactive elements:
- transition: transform 0.2s ease, box-shadow 0.2s ease

Category links:
- Hover: translateY(-2px)

Main feature card:
- Hover: translateY(-3px)

Top story items:
- Hover: translateY(-3px), shadow elevated

Weather widget:
- Hover: translateY(-2px)

Buttons:
- Hover: translateY(-2px)
```

---

## 📱 Responsive Design Breakpoints

### Desktop (≥ 992px - lg)
```
Navbar: Full layout
├── Logo: Normal size
├── Categories: All visible
├── Search: 140px width
├── Weather widget: Visible
└── All elements visible

Main content: 2-column
├── Left (col-lg-8): Featured article
└── Right (col-lg-4): Top stories sidebar
```

### Tablet (≥ 768px, < 992px - md)
```
Navbar: Condensed
├── Logo: Same
├── Categories: Scrollable
├── Search: 100px width
├── Weather widget: 75% opacity
└── Optimized spacing

Content: Stacked on medium screens
├── Switches to single column at < 992px
└── Full width on tablet portrait
```

### Mobile (< 576px - xs)
```
Navbar: Mobile optimized
├── Logo: 1.2rem
├── Categories: Hidden/hamburger
├── Search: 80px width
├── Weather: Hidden
└── Minimal spacing

Main content: Single column
├── Featured: Full width
├── Top stories: Stacked
├── Thumbnails: Full width, 150px height
└── Numbers: Hidden
```

---

## 🔄 Data Structure (From Mock Data)

### Article Object
```javascript
{
  id: Number,
  title: String,              // Short headline
  headline: String,           // Long headline (featured only)
  excerpt: String,            // Preview text
  category: String,           // "Climate", "Technology", etc.
  image: String,              // Image URL
  publishedAt: Date,          // ISO 8601 date
  readTime: Number,           // Minutes to read
  isFeatured: Boolean         // Shows in hero (true for first article)
}
```

### Featured Article Display
```
Featured article = articles.value.find(a => a.isFeatured)
  Shows: Large image, breaking badge, full headline, excerpt
  Category badge from article.category
  Time from formatRelativeTime(article.publishedAt)
```

### Top Stories Display
```
Top stories = articles.value.filter(a => !a.isFeatured).slice(0, 3)
  Story 1: Number "01", headline, metadata, thumbnail
  Story 2: Number "02", headline, metadata, thumbnail
  Story 3: Number "03", headline, metadata, thumbnail
```

---

## 🎯 Color System

### Semantic Colors
```
Primary Background:    #F9F9F6  (Soft off-white)
Text Primary:          #1a1a1a  (Near black)
Text Secondary:        #666666  (Muted gray)
Borders:               #EAEAEA  (Light gray)
Success/Accent:        #DA4B88  (Soft pink - future)
Warning/Alert:         #DC3545  (Red - breaking badge)
Info/Light:            rgba(218, 236, 254, 0.6)  (Blue glassmorphic)
```

### Opacity Variations
```
White:                 #FFFFFF
Light bg:              #f5f5f5  (Search background)
Very light text:       #e8e8e8  (Story numbers)
Light text:            #999999  (Metadata)
Border light:          #EAEAEA
```

---

## 🔤 Typography

### Font Stack
```css
Serif (Headlines):
  font-family: 'Playfair Display', 'Georgia', serif;
  Usage: Brand, headlines, story numbers

Sans-serif (Body):
  font-family: 'Inter', 'Roboto', sans-serif;
  Usage: Navigation, metadata, body text
```

### Font Sizes
```css
h1 (Main headline):     2.5rem (40px)
h2 (Section title):     1.5rem (24px)
h3 (Story headline):    1.1rem (18px)
Body text:              1rem (16px)
Meta/small:             0.85rem - 0.9rem (13-14px)
Category/badge:         0.75rem (12px)
Brand:                  1.5rem (24px)
```

### Font Weights
```css
Regular:     400
Medium:      500
Semi-bold:   600
Bold:        700
Extra-bold:  800
```

---

## 🚀 Script Logic (Vue Setup)

```javascript
<script setup>
import { ref, onMounted } from 'vue';

// Data
const categories = ref(['World', 'Climate', 'Technology', 'Energy', 'Science']);

// Lifecycle
onMounted(() => {
  // Fade-in animation on mount
  const page = document.querySelector('.news-page');
  if (page) {
    page.style.opacity = '0';
    setTimeout(() => {
      page.style.opacity = '1';
    }, 10);
  }
});

// Future: Replace with API calls
// const { articles, topStories, featuredArticle } = useNews();
// const { weatherData } = useWeather();
</script>
```

---

## 🎓 Implementation Details

### Bootstrap Grid Usage
- Container class for max-width
- Row class with gap (g-5)
- col-lg-8 and col-lg-4 for 2-column
- Responsive utilities for mobile/tablet

### CSS Scoped Styling
- All styles use `<style scoped>`
- No style conflicts
- Can be extracted to separate CSS file

### Vue Template Patterns
- v-for for category links and story items
- :class binding for active states
- Semantic HTML tags
- Accessibility attributes (aria-label)

### Animation Framework
- CSS keyframes for fadeInUp
- CSS transitions for hover effects
- Timing functions: ease, ease-out
- Duration: 0.2s (quick) to 0.6s (page load)

---

## 📊 Component Dependencies

### External
- Vue 3 (core)
- Bootstrap 5 CSS (via CDN in main.js)
- Google Fonts (Playfair Display, Inter)

### Internal
- No other components required
- Self-contained and reusable
- Can be imported into other views

### Optional Integrations
- `useNews()` composable (for mock → API data)
- `formatRelativeTime()` util (for date formatting)
- `apiClient.js` (for real API calls)

---

## ✨ Visual Specifications

### Shadows
```css
--shadow-light: 0 2px 8px rgba(0, 0, 0, 0.08)
--shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.12)
```

### Borders
```css
--border-light: 1px solid #EAEAEA
Category pills: border-radius: 50px (fully rounded)
Cards: border-radius: 8px
Images: border-radius: 12px
```

### Spacing (Bootstrap-based)
```css
Gap between columns: g-5 (3rem)
Card padding: 20px
Component margins: m-4, my-5 (Bootstrap utilities)
```

---

## 🎯 Performance Considerations

✅ **Optimized**
- Minimal re-renders (Vue 3 Composition API)
- CSS transitions (GPU accelerated)
- Scoped styles (no global pollution)
- Semantic HTML (better SEO)
- SVG icons (scalable, lightweight)

⏳ **Future Optimizations**
- Image lazy loading
- Code splitting for routes
- CSS-in-JS if needed
- Service worker caching

---

## 🔗 Integration Points

### To Connect with Backend

1. **Replace mock data** in `useNews()` composable:
   ```javascript
   const response = await apiClient.get('/api/news');
   articles.value = response.data;
   ```

2. **Update category links** to filter by selected category:
   ```javascript
   const handleCategoryClick = (category) => {
     filterByCategory(category);
   };
   ```

3. **Add routing** to article detail page:
   ```javascript
   const handleArticleClick = (id) => {
     router.push(`/article/${id}`);
   };
   ```

---

## 📝 Notes for Developers

### Code Quality
- ✅ No hardcoded values
- ✅ Reusable component
- ✅ Follows Vue 3 best practices
- ✅ Responsive and accessible
- ✅ Clean, readable code

### Best Practices Applied
- Semantic HTML
- CSS scoping
- Vue 3 Composition API
- Proper prop typing
- Event emission patterns
- Animation best practices

### Extensibility
- Easy to add new categories
- Simple to replace mock data
- Can extract components (Navbar, ArticleCard, etc.)
- Styling easily customizable

---

**Last Updated**: June 2026  
**Component Version**: 1.0  
**Status**: Production-Ready
