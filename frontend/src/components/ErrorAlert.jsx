/**
 * Error Alert Component
 * Displays error messages to users
 */

import React from 'react';
import { AlertTriangle, X } from 'lucide-react';
import '../styles/ErrorAlert.css';

const ErrorAlert = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="error-alert">
      <div className="error-content">
        <AlertTriangle size={24} className="error-icon" />
        <div className="error-message-wrapper">
          <h3 className="error-title">⚠️ Error</h3>
          <p className="error-message">{message}</p>
        </div>
      </div>
      <button onClick={onClose} className="error-close" aria-label="Dismiss error">
        <X size={20} />
      </button>
    </div>
  );
};

export default ErrorAlert;
