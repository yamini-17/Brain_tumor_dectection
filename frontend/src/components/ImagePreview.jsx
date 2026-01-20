/**
 * Image Preview Component
 * Displays the uploaded image and draws detection bounding boxes
 */

import React, { useEffect, useRef, useState } from 'react';
import '../styles/ImagePreview.css';

const ImagePreview = ({ image, detectionResult, isLoading }) => {
  const canvasRef = useRef(null);
  const imgRef = useRef(null);
  const [imageDimensions, setImageDimensions] = useState(null);

  // Draw image and bounding box on canvas
  useEffect(() => {
    if (!image || !canvasRef.current || !imgRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    imgRef.current.onload = () => {
      // Set canvas dimensions
      canvas.width = imgRef.current.naturalWidth;
      canvas.height = imgRef.current.naturalHeight;

      setImageDimensions({
        width: imgRef.current.naturalWidth,
        height: imgRef.current.naturalHeight,
      });

      // Clear and draw image
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(imgRef.current, 0, 0);

      // Draw bounding box if tumor detected
      if (
        detectionResult &&
        detectionResult.tumor_detected &&
        detectionResult.bounding_box
      ) {
        drawBoundingBox(
          ctx,
          detectionResult.bounding_box,
          detectionResult.confidence
        );
      }
    };

    // Trigger load if image is already cached
    if (imgRef.current.complete) {
      imgRef.current.onload();
    }
  }, [image, detectionResult]);

  const drawBoundingBox = (ctx, bbox, confidence) => {
    const [x, y, width, height] = bbox;

    // Draw rectangle
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, width, height);

    // Draw filled rectangle for label background
    const labelText = `Tumor: ${confidence.toFixed(1)}%`;
    ctx.font = 'bold 14px Arial';
    const textMetrics = ctx.measureText(labelText);
    const textHeight = 20;
    const padding = 4;

    ctx.fillStyle = '#00ff00';
    ctx.fillRect(
      x,
      y - textHeight - padding * 2,
      textMetrics.width + padding * 2,
      textHeight + padding * 2
    );

    // Draw text
    ctx.fillStyle = '#000000';
    ctx.fillText(labelText, x + padding, y - padding - 4);
  };

  return (
    <div className="preview-container">
      <div className="preview-wrapper">
        {image ? (
          <>
            <img
              ref={imgRef}
              src={URL.createObjectURL(image)}
              alt="Preview"
              className="preview-image hidden"
              crossOrigin="anonymous"
            />
            <canvas
              ref={canvasRef}
              className="preview-canvas"
              role="img"
              aria-label="MRI image with detection overlay"
            />
          </>
        ) : (
          <div className="preview-placeholder">
            <p>No image selected</p>
            <p className="placeholder-text">Upload an MRI image to begin</p>
          </div>
        )}
      </div>

      {/* Image info */}
      {image && imageDimensions && (
        <div className="image-info">
          <p>
            <strong>File:</strong> {image.name}
          </p>
          <p>
            <strong>Size:</strong> {(image.size / 1024 / 1024).toFixed(2)} MB
          </p>
          <p>
            <strong>Dimensions:</strong> {imageDimensions.width} × {imageDimensions.height}
          </p>
        </div>
      )}

      {isLoading && (
        <div className="processing-overlay">
          <div className="processing-text">Processing...</div>
        </div>
      )}
    </div>
  );
};

export default ImagePreview;
