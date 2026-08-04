/**
 * Validation Utilities
 */

/**
 * Validate email address
 * @param {string} email - Email to validate
 * @returns {boolean} Whether email is valid
 */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate phone number (basic international format)
 * @param {string} phone - Phone number to validate
 * @returns {boolean} Whether phone is valid
 */
export function isValidPhone(phone) {
  const phoneRegex = /^[\d\s\-\+\(\)]+$/;
  return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

/**
 * Validate URL
 * @param {string} url - URL to validate
 * @returns {boolean} Whether URL is valid
 */
export function isValidUrl(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if string is empty or only whitespace
 * @param {string} str - String to check
 * @returns {boolean} Whether string is empty
 */
export function isEmpty(str) {
  return !str || str.trim().length === 0;
}

/**
 * Check if object is empty
 * @param {object} obj - Object to check
 * @returns {boolean} Whether object is empty
 */
export function isEmptyObject(obj) {
  return Object.keys(obj).length === 0;
}

/**
 * Validate form data object
 * @param {object} data - Form data to validate
 * @param {object} rules - Validation rules { fieldName: ['required', 'email', etc.] }
 * @returns {object} Object with errors { fieldName: 'error message' }
 */
export function validateForm(data, rules) {
  const errors = {};

  for (const [field, fieldRules] of Object.entries(rules)) {
    const value = data[field];

    for (const rule of fieldRules) {
      if (rule === 'required' && isEmpty(String(value))) {
        errors[field] = `${field} is required`;
        break;
      }

      if (rule === 'email' && value && !isValidEmail(value)) {
        errors[field] = `${field} must be a valid email`;
        break;
      }

      if (rule === 'url' && value && !isValidUrl(value)) {
        errors[field] = `${field} must be a valid URL`;
        break;
      }

      if (rule === 'phone' && value && !isValidPhone(value)) {
        errors[field] = `${field} must be a valid phone number`;
        break;
      }

      if (rule.startsWith('min:')) {
        const minLength = parseInt(rule.split(':')[1]);
        if (value && String(value).length < minLength) {
          errors[field] = `${field} must be at least ${minLength} characters`;
          break;
        }
      }

      if (rule.startsWith('max:')) {
        const maxLength = parseInt(rule.split(':')[1]);
        if (value && String(value).length > maxLength) {
          errors[field] = `${field} must not exceed ${maxLength} characters`;
          break;
        }
      }
    }
  }

  return errors;
}
