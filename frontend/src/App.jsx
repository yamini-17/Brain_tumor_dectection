import React, { useState, useRef } from 'react';
import './styles/App.css';

export default function App() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = async (file) => {
    try {
      setError(null);
      setResults(null);

      // Validate file
      const allowed = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff'];
      const ext = file.name.split('.').pop().toLowerCase();
      if (!allowed.includes(ext)) {
        setError('Only JPG, PNG, BMP, GIF, TIFF files allowed');
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        setError('File must be less than 10MB');
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
      };
      reader.readAsDataURL(file);

      // Send to backend
      setLoading(true);
      const formData = new FormData();
      formData.append('image', file);  // Changed from 'file' to 'image'

      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to process image');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setUploadedImage(null);
    setResults(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">🧠 Brain Tumor Detection System</h1>
          <p className="app-subtitle">Advanced Medical Image Analysis with AI</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="dashboard-grid">
          
          {/* Upload Section */}
          <section className="upload-section">
            <h2 className="section-title">📁 Upload Medical Image</h2>
            <div
              className={`upload-dropzone ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                hidden
                onChange={handleFileInputChange}
                accept="image/*"
              />
              <div className="upload-icon">📤</div>
              <p className="upload-text">Drag & drop or click to upload</p>
              <p className="upload-subtext">Supports: JPG, PNG, BMP, GIF, TIFF (Max 10MB)</p>
            </div>
          </section>

          {/* Preview Section */}
          {uploadedImage && (
            <section className="preview-section">
              <h2 className="section-title">🖼️ Image Preview</h2>
              <div className="image-preview-container">
                <img src={uploadedImage} alt="Preview" className="preview-image" />
              </div>
              <button onClick={handleReset} className="reset-button">
                🔄 Upload New Image
              </button>
            </section>
          )}

          {/* Loading State */}
          {loading && (
            <section className="loader-section">
              <div className="spinner-container">
                <div className="spinner"></div>
                <p className="loader-message">🔬 Analyzing image with YOLOv9...</p>
                <p className="loader-subtext">Please wait...</p>
              </div>
            </section>
          )}

          {/* Error State */}
          {error && (
            <section className="error-section">
              <div className="error-box">
                <p className="error-icon">⚠️</p>
                <p className="error-message">{error}</p>
                <button onClick={() => setError(null)} className="error-close">
                  ✕ Dismiss
                </button>
              </div>
            </section>
          )}

          {/* Results Section */}
          {results && !loading && (
            <section className="results-section">
              <h2 className="section-title">✅ Detection Results</h2>
              
              {/* Annotated Image with Bounding Box */}
              {results.annotated_image && (
                <div className="annotated-image-container">
                  <h3 className="annotated-title">🖼️ Annotated Image (with Tumor Detection Box)</h3>
                  <img 
                    src={results.annotated_image} 
                    alt="Annotated MRI with tumor detection"
                    className="annotated-image"
                  />
                </div>
              )}
              
              <div className="results-card">
                <div className="result-status">
                  <p className="status-label">
                    {results.tumor_detected ? '🔴 TUMOR DETECTED' : '🟢 NO TUMOR'}
                  </p>
                </div>
                
                <div className="result-item">
                  <span className="result-label">Confidence Score:</span>
                  <span className="result-value">{results.confidence?.toFixed(1) || 0}%</span>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{ width: `${results.confidence || 0}%` }}
                    ></div>
                  </div>
                </div>

                {results.bounding_box && results.tumor_detected && (
                  <div className="result-item">
                    <span className="result-label">Bounding Box:</span>
                    <div className="bbox-grid">
                      <div className="bbox-item">
                        <span className="bbox-label">X:</span>
                        <span className="bbox-value">{Math.round(results.bounding_box[0])}</span>
                      </div>
                      <div className="bbox-item">
                        <span className="bbox-label">Y:</span>
                        <span className="bbox-value">{Math.round(results.bounding_box[1])}</span>
                      </div>
                      <div className="bbox-item">
                        <span className="bbox-label">W:</span>
                        <span className="bbox-value">{Math.round(results.bounding_box[2])}</span>
                      </div>
                      <div className="bbox-item">
                        <span className="bbox-label">H:</span>
                        <span className="bbox-value">{Math.round(results.bounding_box[3])}</span>
                      </div>
                    </div>
                  </div>
                )}

                <div className="result-item">
                  <span className="result-label">Processing Time:</span>
                  <span className="result-value">{results.processing_time_ms?.toFixed(2) || 0}ms</span>
                </div>

                {results.detections_count > 0 && (
                  <div className="result-item">
                    <span className="result-label">Total Detections:</span>
                    <span className="result-value">{results.detections_count}</span>
                  </div>
                )}
              </div>
              <button onClick={handleReset} className="reset-button">
                🔄 Analyze Another Image
              </button>
            </section>
          )}

          {/* Info Section */}
          {!uploadedImage && !results && (
            <section className="info-section">
              <h2 className="section-title">ℹ️ System Information</h2>
              <div className="info-grid">
                <div className="info-card">
                  <h3>✅ Frontend</h3>
                  <p>React 18.2 + Vite</p>
                </div>
                <div className="info-card">
                  <h3>✅ Backend API</h3>
                  <p>Flask on Port 5000</p>
                </div>
                <div className="info-card">
                  <h3>✅ AI Model</h3>
                  <p>YOLOv9 Detector</p>
                </div>
              </div>
              <div className="features-list">
                <h4>🚀 Features:</h4>
                <ul>
                  <li>✅ Drag-and-drop upload</li>
                  <li>✅ Real-time detection</li>
                  <li>✅ Confidence scoring</li>
                  <li>✅ Bounding boxes</li>
                  <li>✅ Processing metrics</li>
                </ul>
              </div>
            </section>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>🧠 Brain Tumor Detection System v1.0 | YOLOv9 + Flask + React</p>
        <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>
          For medical use: Please consult with healthcare professionals
        </p>
      </footer>
    </div>
  );
}
