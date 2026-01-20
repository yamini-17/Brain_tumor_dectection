/**
 * Image Upload Component
 * Handles image file selection and preview
 */

import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';
import '../styles/ImageUpload.css';

const ImageUpload = ({ onImageUpload, disabled }) => {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff'];
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

  const validateFile = (file) => {
    // Check file type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
      alert(`Invalid file type. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}`);
      return false;
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      alert('File size exceeds 10MB limit');
      return false;
    }

    return true;
  };

  const handleFileSelect = (file) => {
    if (validateFile(file)) {
      onImageUpload(file);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="upload-container">
      <div
        className={`upload-box ${dragActive ? 'drag-active' : ''} ${
          disabled ? 'disabled' : ''
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="upload-content">
          <Upload size={48} className="upload-icon" />
          <h3 className="upload-title">Upload MRI Image</h3>
          <p className="upload-subtitle">
            Drag and drop your image here, or click to select
          </p>
          <p className="upload-info">
            Supported formats: JPG, PNG, BMP, GIF, TIFF (Max 10MB)
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".jpg,.jpeg,.png,.bmp,.gif,.tiff"
            onChange={handleInputChange}
            disabled={isLoading || disabled}
            className="file-input"
            aria-label="Upload MRI image"
          />
        </div>

        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isLoading || disabled}
          className="upload-button"
        >
          {isLoading ? 'Processing...' : 'Select Image'}
        </button>
      </div>
    </div>
  );
};

export default ImageUpload;
