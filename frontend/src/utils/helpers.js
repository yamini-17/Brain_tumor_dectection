/**
 * Utility functions for the frontend
 */

/**
 * Format file size in human-readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
};

/**
 * Validate image file
 * @param {File} file - File to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validateImageFile = (file) => {
  const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff'];
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

  if (!file) {
    return { isValid: false, message: 'No file selected' };
  }

  // Check file type
  const fileExtension = file.name.split('.').pop().toLowerCase();
  if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
    return {
      isValid: false,
      message: `Invalid file type. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}`,
    };
  }

  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      isValid: false,
      message: `File size exceeds 10MB limit. Current size: ${formatFileSize(file.size)}`,
    };
  }

  return { isValid: true, message: 'File is valid' };
};

/**
 * Create image blob from canvas
 * @param {HTMLCanvasElement} canvas - Canvas element
 * @returns {Blob} Canvas content as blob
 */
export const canvasToBlob = (canvas) => {
  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      resolve(blob);
    }, 'image/png');
  });
};

/**
 * Download file from blob
 * @param {Blob} blob - Blob to download
 * @param {string} filename - Filename for download
 */
export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Format confidence score with color
 * @param {number} confidence - Confidence value (0-100)
 * @returns {Object} Color and formatted value
 */
export const getConfidenceColor = (confidence) => {
  if (confidence >= 80) return { color: '#10b981', level: 'High' };
  if (confidence >= 60) return { color: '#f59e0b', level: 'Medium' };
  return { color: '#ef4444', level: 'Low' };
};

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export const debounce = (func, delay) => {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Retry async function
 * @param {Function} fn - Async function to retry
 * @param {number} retries - Number of retries
 * @param {number} delay - Delay between retries in ms
 * @returns {Promise} Result of function
 */
export const retryAsync = async (fn, retries = 3, delay = 1000) => {
  try {
    return await fn();
  } catch (error) {
    if (retries <= 1) throw error;
    await new Promise((resolve) => setTimeout(resolve, delay));
    return retryAsync(fn, retries - 1, delay);
  }
};
