import { ref, computed } from 'vue';
import airportsData from '../../../shared-data/airports.json';

/**
 * Composable for managing airport data
 */
export function useAirports() {
  const airportsList = ref(airportsData);

  return {
    airportsList
  };
}


/**
 * Composable for managing news data
 * Handles fetching, filtering, and sorting of news articles
 */
export function useNews() {
  const articles = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const selectedCategory = ref(null);
  const searchQuery = ref('');

  /**
   * Fetch news articles from API or mock data
   */
  const fetchArticles = async (category = null) => {
    isLoading.value = true;
    error.value = null;

    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`/api/news?category=${category}`);
      // const data = await response.json();

      // Mock data for now
      const mockArticles = [
        {
          id: 1,
          title: 'Arctic Ice Sheet Collapses at Record Rate',
          headline: 'Arctic Ice Sheet Collapses at Record Rate as Global Temperatures Surge Past Critical Threshold',
          excerpt: 'Scientists report alarming findings from recent Arctic expeditions...',
          category: 'Climate',
          image: 'https://via.placeholder.com/700x400?text=Arctic+Ice',
          publishedAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
          readTime: 8,
          isFeatured: true
        },
        {
          id: 2,
          title: 'New AI Model Predicts Weather with 99% Accuracy',
          headline: 'New AI Model Predicts Weather with 99% Accuracy',
          excerpt: 'Researchers unveil breakthrough in weather forecasting technology...',
          category: 'Technology',
          image: 'https://via.placeholder.com/80x80?text=AI+Weather',
          publishedAt: new Date(Date.now() - 4 * 60 * 60 * 1000),
          readTime: 5
        },
        {
          id: 3,
          title: 'Ocean Acidification Reaches New Milestone',
          headline: 'Ocean Acidification Reaches New Milestone',
          excerpt: 'Marine ecosystems face unprecedented challenges from ocean acidification...',
          category: 'Environment',
          image: 'https://via.placeholder.com/80x80?text=Ocean',
          publishedAt: new Date(Date.now() - 6 * 60 * 60 * 1000),
          readTime: 7
        },
        {
          id: 4,
          title: 'Renewable Energy Surpasses Coal Production',
          headline: 'Renewable Energy Surpasses Coal Production Globally',
          excerpt: 'Global renewable energy capacity reaches all-time high...',
          category: 'Energy',
          image: 'https://via.placeholder.com/80x80?text=Renewable',
          publishedAt: new Date(Date.now() - 8 * 60 * 60 * 1000),
          readTime: 6
        }
      ];

      articles.value = category
        ? mockArticles.filter(a => a.category === category)
        : mockArticles;
    } catch (err) {
      error.value = 'Failed to fetch articles';
      console.error('Error fetching articles:', err);
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Filter articles based on category
   */
  const filterByCategory = (category) => {
    selectedCategory.value = category;
    fetchArticles(category);
  };

  /**
   * Search articles by title or excerpt
   */
  const searchArticles = (query) => {
    searchQuery.value = query.toLowerCase();
  };

  /**
   * Computed property for filtered articles
   */
  const filteredArticles = computed(() => {
    return articles.value.filter(article => {
      const matchesSearch =
        article.title.toLowerCase().includes(searchQuery.value) ||
        article.excerpt.toLowerCase().includes(searchQuery.value);
      return matchesSearch;
    });
  });

  /**
   * Get featured article
   */
  const featuredArticle = computed(() => {
    return articles.value.find(a => a.isFeatured) || articles.value[0] || null;
  });

  /**
   * Get top stories (excluding featured)
   */
  const topStories = computed(() => {
    return articles.value.filter(a => !a.isFeatured).slice(0, 3);
  });

  return {
    // State
    articles,
    isLoading,
    error,
    selectedCategory,
    searchQuery,

    // Computed
    filteredArticles,
    featuredArticle,
    topStories,

    // Methods
    fetchArticles,
    filterByCategory,
    searchArticles
  };
}

/**
 * Composable for managing weather data
 */
export function useWeather() {
  const weatherData = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  /**
   * Fetch weather data
   */
  const fetchWeather = async (latitude, longitude) => {
    isLoading.value = true;
    error.value = null;

    try {
      // TODO: Replace with actual API call to OpenMeteo or backend
      // const response = await fetch(
      //   `/api/weather?lat=${latitude}&lon=${longitude}`
      // );
      // const data = await response.json();

      // Mock data for now
      weatherData.value = {
        temperature: 31,
        city: 'Ho Chi Minh City',
        condition: 'Sunny',
        humidity: 65,
        windSpeed: 12
      };
    } catch (err) {
      error.value = 'Failed to fetch weather data';
      console.error('Error fetching weather:', err);
    } finally {
      isLoading.value = false;
    }
  };

  return {
    weatherData,
    isLoading,
    error,
    fetchWeather
  };
}
