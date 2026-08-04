/**
 * API Client for communicating with backend
 * Centralizes all API calls and handles errors
 */

import axios from 'axios';

// Ensure fallback and environment variables both explicitly route to v1
const baseEndpoint = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const API_URL = baseEndpoint.endsWith('/v1') ? baseEndpoint : `${baseEndpoint}/v1`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL, // Strictly enforces the global /api/v1 endpoint architecture
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Request interceptor - Add auth token if available
 */
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token to request headers if available
    let token = localStorage.getItem('authToken');
    if (!token) {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const parsed = JSON.parse(storedUser);
          if (parsed && (parsed.access_token || parsed.token)) {
            token = parsed.access_token || parsed.token;
          }
        } catch (e) {}
      }
    }
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Response interceptor - Handle errors globally
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - clear token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user'); // Crucial fix: prevents user avatar headers from showing when logged out
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

/**
 * NEWS ENDPOINTS
 */
export const newsAPI = {
  /**
   * Get all articles
   * @param {Object} params - Query parameters
   * @param {string} params.category - Filter by category
   * @param {number} params.skip - Pagination offset
   * @param {number} params.limit - Pagination limit
   */
  getArticles: (params = {}) =>
    apiClient.get('/news', { params }),

  /**
   * Get single article by ID
   * @param {number} id - Article ID
   */
  getArticle: (id) =>
    apiClient.get(`/news/${id}`),

  /**
   * Create new article (admin only)
   * @param {Object} data - Article data
   */
  createArticle: (data) =>
    apiClient.post('/news', data),

  /**
   * Update existing article (admin only)
   * @param {number} id - Article ID
   * @param {Object} data - Updated article data
   */
  updateArticle: (id, data) =>
    apiClient.put(`/news/${id}`, data),

  /**
   * Delete article (admin only)
   * @param {number} id - Article ID
   */
  deleteArticle: (id) =>
    apiClient.delete(`/news/${id}`),

  /**
   * Search articles
   * @param {string} query - Search query
   */
  searchArticles: (query) =>
    apiClient.get('/news/search', { params: { q: query } })
};

/**
 * WEATHER ENDPOINTS
 */
export const weatherAPI = {
  /**
   * Get current weather
   * @param {number} latitude - Latitude
   * @param {number} longitude - Longitude
   */
  getCurrentWeather: (latitude, longitude) =>
    apiClient.get('/weather/current', {
      params: { lat: latitude, lon: longitude }
    }),

  /**
   * Get weather forecast
   * @param {number} latitude - Latitude
   * @param {number} longitude - Longitude
   * @param {number} days - Number of days (default: 7)
   */
  getForecast: (latitude, longitude, days = 7) =>
    apiClient.get('/weather/forecast', {
      params: { lat: latitude, lon: longitude, days }
    }),

  /**
   * Get historical weather data
   * @param {number} latitude - Latitude
   * @param {number} longitude - Longitude
   * @param {string} date - Date in YYYY-MM-DD format
   */
  getHistoricalData: (latitude, longitude, date) =>
    apiClient.get('/weather/historical', {
      params: { lat: latitude, lon: longitude, date }
    }),

  /**
   * Get weather alerts
   * @param {number} latitude - Latitude
   * @param {number} longitude - Longitude
   */
  getAlerts: (latitude, longitude) =>
    apiClient.get('/weather/alerts', {
      params: { lat: latitude, lon: longitude }
    })
};

/**
 * AUTHENTICATION ENDPOINTS
 */
export const authAPI = {
  /**
   * User login
   * @param {string} email - User email
   * @param {string} password - User password
   */
  login: (email, password) =>
    apiClient.post('/auth/login', { email, password }),

  /**
   * User logout
   */
  logout: () =>
    apiClient.post('/auth/logout'),

  /**
   * User registration
   * @param {Object} data - User registration data
   */
  register: (data) =>
    apiClient.post('/auth/register', data),

  /**
   * Get current user profile
   */
  getProfile: () =>
    apiClient.get('/auth/profile'),

  /**
   * Update user profile
   * @param {Object} data - Updated profile data
   */
  updateProfile: (data) =>
    apiClient.put('/auth/profile', data)
};

/**
 * CATEGORY ENDPOINTS
 */
export const categoryAPI = {
  /**
   * Get all categories
   */
  getCategories: () =>
    apiClient.get('/categories'),

  /**
   * Create new category (admin only)
   * @param {string} name - Category name
   */
  createCategory: (name) =>
    apiClient.post('/categories', { name })
};

/**
 * Error handler utility
 * Provides user-friendly error messages
 */
export function handleAPIError(error) {
  if (error.response) {
    // Backend responded with error status
    const { status, data } = error.response;
    const message = data?.message || data?.detail || 'An error occurred';

    switch (status) {
      case 400:
        return { status: 'error', message: `Bad request: ${message}` };
      case 401:
        return { status: 'error', message: 'Please log in to continue' };
      case 403:
        return { status: 'error', message: 'You do not have permission' };
      case 404:
        return { status: 'error', message: 'Resource not found' };
      case 422:
        return { status: 'error', message: `Validation error: ${message}` };
      case 500:
        return { status: 'error', message: 'Server error. Please try again.' };
      default:
        return { status: 'error', message };
    }
  } else if (error.request) {
    // Request made but no response
    return { status: 'error', message: 'No response from server' };
  } else {
    // Error during request setup
    return { status: 'error', message: error.message };
  }
}

/**
 * AIRLINE LIKES ENDPOINTS
 */
export const likesAPI = {
  getLikesSummary: () =>
    apiClient.get('/likes/summary'),
  getLikeStatus: (userId, airlineName) =>
    apiClient.get('/likes/status', { params: { user_id: userId, airline_name: airlineName } })
};

export default apiClient;
