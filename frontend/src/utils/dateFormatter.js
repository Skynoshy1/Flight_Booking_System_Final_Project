/**
 * Date and Time Utilities
 */

/**
 * Format date to relative time (e.g., "2 hours ago")
 * @param {Date | string | number} date - The date to format
 * @returns {string} Relative time string
 */
export function formatRelativeTime(date) {
  const now = new Date();
  const then = new Date(date);
  const seconds = Math.floor((now - then) / 1000);

  let interval = Math.floor(seconds / 31536000);
  if (interval > 1) return `${interval} years ago`;

  interval = Math.floor(seconds / 2592000);
  if (interval > 1) return `${interval} months ago`;

  interval = Math.floor(seconds / 86400);
  if (interval > 1) return `${interval} days ago`;

  interval = Math.floor(seconds / 3600);
  if (interval > 1) return `${interval} hours ago`;

  interval = Math.floor(seconds / 60);
  if (interval > 1) return `${interval} minutes ago`;

  return 'just now';
}

/**
 * Format date to readable format (e.g., "January 15, 2026")
 * @param {Date | string | number} date - The date to format
 * @returns {string} Formatted date string
 */
export function formatDate(date) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(date).toLocaleDateString('en-US', options);
}

/**
 * Format date to short format (e.g., "Jan 15, 2026")
 * @param {Date | string | number} date - The date to format
 * @returns {string} Formatted date string
 */
export function formatShortDate(date) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(date).toLocaleDateString('en-US', options);
}

/**
 * Format date and time (e.g., "January 15, 2026 2:30 PM")
 * @param {Date | string | number} date - The date to format
 * @returns {string} Formatted date and time string
 */
export function formatDateTime(date) {
  const dateOptions = { year: 'numeric', month: 'long', day: 'numeric' };
  const timeOptions = { hour: 'numeric', minute: '2-digit', hour12: true };
  const dateStr = new Date(date).toLocaleDateString('en-US', dateOptions);
  const timeStr = new Date(date).toLocaleTimeString('en-US', timeOptions);
  return `${dateStr} ${timeStr}`;
}

/**
 * Estimate reading time based on word count
 * @param {string} text - The text to estimate reading time for
 * @param {number} wordsPerMinute - Average reading speed (default: 200)
 * @returns {number} Estimated reading time in minutes
 */
export function estimateReadingTime(text, wordsPerMinute = 200) {
  const wordCount = text.trim().split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
}
