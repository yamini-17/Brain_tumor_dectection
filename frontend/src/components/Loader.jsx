/**
 * Loader Component
 * Displays loading animation during API calls
 */

import React from 'react';
import '../styles/Loader.css';

const Loader = ({ message = 'Processing...' }) => {
  return (
    <div className="loader-overlay">
      <div className="loader-content">
        <div className="spinner">
          <div className="spinner-ring" />
          <div className="spinner-ring" />
          <div className="spinner-ring" />
          <div className="spinner-ring" />
        </div>
        <p className="loader-message">{message}</p>
        <p className="loader-subtext">Analyzing MRI image...</p>
      </div>
    </div>
  );
};

export default Loader;
