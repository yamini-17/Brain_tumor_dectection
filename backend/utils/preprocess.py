"""
Image Preprocessing Module for Brain Tumor Detection
Handles image loading, resizing, normalization, and format conversion.
"""

import cv2
import numpy as np
import logging
from pathlib import Path
from typing import Tuple, Optional

# Configure logging
logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """
    Preprocesses MRI brain images for YOLOv9 model inference.
    
    Attributes:
        target_size (Tuple[int, int]): Target image size for model input (default: 640x640)
        mean (np.ndarray): Mean values for normalization (ImageNet standard)
        std (np.ndarray): Standard deviation values for normalization
    """
    
    def __init__(self, target_size: Tuple[int, int] = (640, 640)):
        """
        Initialize the image preprocessor.
        
        Args:
            target_size (Tuple[int, int]): Target image dimensions
        """
        self.target_size = target_size
        # ImageNet normalization values
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        logger.info(f"ImagePreprocessor initialized with target size: {target_size}")
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image from file path.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Optional[np.ndarray]: Loaded image array or None if loading fails
        """
        try:
            if not Path(image_path).exists():
                logger.error(f"Image file not found: {image_path}")
                return None
            
            image = cv2.imread(image_path)
            
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return None
            
            logger.debug(f"Image loaded successfully: {image_path} (shape: {image.shape})")
            return image
        
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {str(e)}")
            return None
    
    def load_image_from_bytes(self, image_bytes: bytes) -> Optional[np.ndarray]:
        """
        Load image from bytes (used for file uploads).
        
        Args:
            image_bytes (bytes): Image data in bytes
            
        Returns:
            Optional[np.ndarray]: Loaded image array or None if loading fails
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                logger.error("Failed to decode image from bytes")
                return None
            
            logger.debug(f"Image loaded from bytes (shape: {image.shape})")
            return image
        
        except Exception as e:
            logger.error(f"Error loading image from bytes: {str(e)}")
            return None
    
    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image to target size.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Resized image
        """
        try:
            resized = cv2.resize(image, self.target_size, interpolation=cv2.INTER_LINEAR)
            logger.debug(f"Image resized to {self.target_size}")
            return resized
        
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise
    
    def convert_to_rgb(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image from BGR (OpenCV default) to RGB.
        
        Args:
            image (np.ndarray): Input image in BGR format
            
        Returns:
            np.ndarray: Image in RGB format
        """
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            logger.debug("Image converted from BGR to RGB")
            return rgb_image
        
        except Exception as e:
            logger.error(f"Error converting image to RGB: {str(e)}")
            raise
    
    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize image using ImageNet statistics.
        
        Args:
            image (np.ndarray): Input image (values 0-255)
            
        Returns:
            np.ndarray: Normalized image (values normalized by ImageNet stats)
        """
        try:
            # Convert to float32 and normalize to 0-1
            image_float = image.astype(np.float32) / 255.0
            
            # Apply ImageNet normalization
            normalized = (image_float - self.mean) / self.std
            
            logger.debug("Image normalized using ImageNet statistics")
            return normalized
        
        except Exception as e:
            logger.error(f"Error normalizing image: {str(e)}")
            raise
    
    def preprocess(self, image_bytes: bytes) -> Tuple[Optional[np.ndarray], Optional[Tuple[int, int]]]:
        """
        Complete preprocessing pipeline: load -> convert -> resize -> normalize.
        
        Args:
            image_bytes (bytes): Raw image bytes from file upload
            
        Returns:
            Tuple[Optional[np.ndarray], Optional[Tuple[int, int]]]: 
                Preprocessed image array and original size (or None if preprocessing fails)
        """
        try:
            # Load image from bytes
            image = self.load_image_from_bytes(image_bytes)
            if image is None:
                return None, None
            
            # Store original size for later reference
            original_size = image.shape[:2]
            
            # Convert BGR to RGB
            image = self.convert_to_rgb(image)
            
            # Resize to target size
            image = self.resize_image(image)
            
            # Normalize
            image = self.normalize_image(image)
            
            # Convert to torch-compatible format (C, H, W)
            image = np.transpose(image, (2, 0, 1))
            
            logger.info(f"Preprocessing complete. Original size: {original_size}, Target size: {self.target_size}")
            return image, original_size
        
        except Exception as e:
            logger.error(f"Error in preprocessing pipeline: {str(e)}")
            return None, None
    
    def denormalize_box_coordinates(
        self,
        box_coords: Tuple[float, float, float, float],
        original_size: Tuple[int, int]
    ) -> Tuple[int, int, int, int]:
        """
        Convert normalized/resized box coordinates back to original image coordinates.
        
        Args:
            box_coords (Tuple[float, float, float, float]): Box coordinates [x, y, w, h] in normalized format
            original_size (Tuple[int, int]): Original image height and width
            
        Returns:
            Tuple[int, int, int, int]: Box coordinates scaled to original image size
        """
        try:
            h, w = original_size
            x, y, box_w, box_h = box_coords
            
            # Scale coordinates from normalized space to original image space
            x_scaled = int(x * w / self.target_size[0])
            y_scaled = int(y * h / self.target_size[1])
            w_scaled = int(box_w * w / self.target_size[0])
            h_scaled = int(box_h * h / self.target_size[1])
            
            return (x_scaled, y_scaled, w_scaled, h_scaled)
        
        except Exception as e:
            logger.error(f"Error denormalizing box coordinates: {str(e)}")
            return (0, 0, 0, 0)
