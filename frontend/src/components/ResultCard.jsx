/**
 * Results Card Component
 * Displays detection results in a professional format
 */

import React from 'react';
import { CheckCircle, AlertCircle, Clock } from 'lucide-react';
import '../styles/ResultCard.css';

const ResultCard = ({ detectionResult, isLoading }) => {
  if (isLoading) return null;
  
  const data = detectionResult || {};
  const tumor_detected = data.tumor_detected ?? false;
  const confidence = data.confidence ?? 0;
  const processing_time_ms = data.processing_time_ms ?? 0;
  const bounding_box = data.bounding_box ?? [0, 0, 0, 0];
  const detections_count = data.detections_count ?? 0;

  return (
    <div className="result-card">
      <div className="result-header">
        <h2 className="result-title">Detection Results</h2>
      </div>

      <div className="result-content">
        {/* Tumor Status */}
        <div className="result-section">
          <div className="status-indicator">
            {tumor_detected ? (
              <>
                <AlertCircle size={28} className="status-icon alert" />
                <span className="status-text">Tumor Detected</span>
              </>
            ) : (
              <>
                <CheckCircle size={28} className="status-icon success" />
                <span className="status-text">No Tumor Detected</span>
              </>
            )}
          </div>
        </div>

        {/* Confidence */}
        <div className="result-section">
          <label className="result-label">Confidence Score</label>
          <div className="confidence-container">
            <div className="confidence-value">
              <span className="confidence-number">{confidence.toFixed(1)}%</span>
            </div>
            <div className="confidence-bar-wrapper">
              <div
                className={`confidence-bar ${
                  confidence > 80 ? 'high' : confidence > 60 ? 'medium' : 'low'
                }`}
                style={{ width: `${confidence}%` }}
              />
            </div>
          </div>
        </div>

        {/* Detection Details */}
        {tumor_detected && bounding_box && (
          <div className="result-section">
            <label className="result-label">Bounding Box Coordinates</label>
            <div className="bbox-grid">
              <div className="bbox-item">
                <span className="bbox-label">X</span>
                <span className="bbox-value">{bounding_box[0]}</span>
              </div>
              <div className="bbox-item">
                <span className="bbox-label">Y</span>
                <span className="bbox-value">{bounding_box[1]}</span>
              </div>
              <div className="bbox-item">
                <span className="bbox-label">Width</span>
                <span className="bbox-value">{bounding_box[2]}</span>
              </div>
              <div className="bbox-item">
                <span className="bbox-label">Height</span>
                <span className="bbox-value">{bounding_box[3]}</span>
              </div>
            </div>
          </div>
        )}

        {/* Processing Info */}
        <div className="result-section">
          <div className="processing-info">
            <Clock size={20} className="info-icon" />
            <div className="info-text">
              <span className="info-label">Processing Time:</span>
              <span className="info-value">{processing_time_ms.toFixed(2)}ms</span>
            </div>
          </div>
          {detections_count > 0 && (
            <p className="detection-count">
              Total detections found: {detections_count}
            </p>
          )}
        </div>

        {/* Status Badge */}
        <div className="result-footer">
          <div
            className={`status-badge ${tumor_detected ? 'positive' : 'negative'}`}
          >
            {tumor_detected ? 'POSITIVE' : 'NEGATIVE'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
