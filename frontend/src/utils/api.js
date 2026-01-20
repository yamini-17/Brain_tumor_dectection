/**
 * API Service Module
 * Handles all API requests to the Flask backend
 */

import axios from 'axios';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 120 second timeout for long inference
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    return Promise.reject(error);
  }
);

/**
 * Check API health status
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message ||
      error.message ||
      'Failed to connect to API'
    );
  }
};

/**
 * Get system status and configuration
 * @returns {Promise<Object>} System status
 */
export const getSystemStatus = async () => {
  try {
    const response = await apiClient.get('/status');
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message ||
      error.message ||
      'Failed to get system status'
    );
  }
};

/**
 * Send image to API for tumor detection
 * @param {File} imageFile - The image file to process
 * @param {Function} onUploadProgress - Progress callback
 * @returns {Promise<Object>} Detection results
 */
export const predictTumor = async (imageFile, onUploadProgress = null) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    if (onUploadProgress) {
      config.onUploadProgress = onUploadProgress;
    }

    const response = await apiClient.post('/predict', formData, config);

    // Check for errors in response
    if (response.data.status === 'error') {
      throw new Error(response.data.error || 'Prediction failed');
    }

    return response.data;
  } catch (error) {
    if (error.response?.status === 413) {
      throw new Error('File size exceeds maximum limit (10MB)');
    } else if (error.response?.status === 503) {
      throw new Error('Model not loaded. Please restart the server.');
    } else if (error.response?.status === 400) {
      throw new Error(
        error.response.data.error || 'Invalid image format or file'
      );
    } else if (error.message === 'Network Error') {
      throw new Error('Cannot connect to API server. Is it running?');
    } else {
      throw new Error(
        error.response?.data?.error ||
        error.message ||
        'Prediction failed'
      );
    }
  }
};

/**
 * Set custom API base URL
 * @param {string} url - New API base URL
 */
export const setApiBaseUrl = (url) => {
  apiClient.defaults.baseURL = url;
};

/**
 * Get current API base URL
 * @returns {string} Current API base URL
 */
export const getApiBaseUrl = () => {
  return apiClient.defaults.baseURL;
};

export default apiClient;
