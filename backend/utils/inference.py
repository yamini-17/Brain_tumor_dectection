"""
Model Inference Module for Brain Tumor Detection
Handles YOLOv9 model loading, inference, and result processing.
"""

import torch
import logging
import time
from typing import Dict, Optional, List, Tuple
from pathlib import Path

# Patch torch to allow loading ultralytics models (PyTorch 2.6+ fix)
try:
    import torch.serialization as serialization
    from ultralytics.nn.tasks import DetectionModel
    
    # Add necessary classes to safe globals
    serialization.add_safe_globals([DetectionModel])
except Exception as e:
    pass

# Configure logging
logger = logging.getLogger(__name__)


class YOLOv9Detector:
    """
    YOLOv9 model wrapper for brain tumor detection.
    
    Attributes:
        model_path (str): Path to the YOLOv9 model weights
        device (torch.device): GPU or CPU device
        model (torch.nn.Module): Loaded YOLOv9 model
        confidence_threshold (float): Confidence threshold for detections
    """
    
    def __init__(
        self,
        model_path: str,
        confidence_threshold: float = 0.5,
        iou_threshold: float = 0.45
    ):
        """
        Initialize YOLOv9 detector.
        
        Args:
            model_path (str): Path to YOLOv9 model weights (.pt file)
            confidence_threshold (float): Confidence threshold for predictions
            iou_threshold (float): IoU threshold for NMS (Non-Maximum Suppression)
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.device = self._get_device()
        self.model = None
        
        # Load model
        self._load_model()
    
    def _get_device(self) -> torch.device:
        """
        Get appropriate device (GPU if available, else CPU).
        
        Returns:
            torch.device: CUDA device if available, else CPU
        """
        if torch.cuda.is_available():
            device = torch.device("cuda")
            logger.info(f"GPU detected: {torch.cuda.get_device_name(0)}")
        else:
            device = torch.device("cpu")
            logger.info("GPU not available. Using CPU for inference.")
        
        return device
    
    def _load_model(self) -> bool:
        """
        Load YOLOv9 model from weights file.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            if not Path(self.model_path).exists():
                logger.error(f"Model file not found: {self.model_path}")
                return False
            
            # Import ultralytics YOLO
            from ultralytics import YOLO
            
            # Load model
            self.model = YOLO(self.model_path)
            
            # Move to device
            if str(self.device) == 'cuda':
                self.model.to('cuda')
            
            # Set model to evaluation mode
            self.model.eval()
            
            logger.info(f"YOLOv8 model loaded successfully from {self.model_path}")
            return True
        
        except ImportError:
            logger.error("ultralytics library not installed. Install it using: pip install ultralytics")
            return False
        
        except Exception as e:
            logger.error(f"Error loading YOLOv8 model: {str(e)}")
            return False
    
    def predict(self, image_tensor: torch.Tensor) -> Dict:
        """
        Run inference on preprocessed image.
        
        Args:
            image_tensor (torch.Tensor): Preprocessed image tensor
            
        Returns:
            Dict: Raw model predictions
        """
        try:
            if self.model is None:
                logger.error("Model not loaded. Cannot perform inference.")
                return {"error": "Model not loaded"}
            
            # Move image to device
            if isinstance(image_tensor, torch.Tensor):
                image_tensor = image_tensor.to(self.device)
            
            # Run inference with no gradient computation
            with torch.no_grad():
                results = self.model(image_tensor, conf=self.confidence_threshold, iou=self.iou_threshold)
            
            return results
        
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            return {"error": str(e)}
    
    def process_results(
        self,
        results,
        original_size: Tuple[int, int]
    ) -> Dict:
        """
        Process raw model predictions into structured format.
        
        Args:
            results: Raw predictions from YOLO model
            original_size (Tuple[int, int]): Original image dimensions
            
        Returns:
            Dict: Processed detection results
        """
        try:
            detections = {
                "tumor_detected": False,
                "confidence": 0.0,
                "bounding_box": [0, 0, 0, 0],
                "detections_count": 0,
                "all_detections": []
            }
            
            # Check if results exist
            if results is None or len(results) == 0:
                logger.info("No detections found in image")
                return detections
            
            # Extract detections from results
            result = results[0]
            
            if result.boxes is None or len(result.boxes) == 0:
                logger.info("No tumor detected in image")
                return detections
            
            # Get the detection with highest confidence
            boxes = result.boxes.cpu().numpy()
            detections["detections_count"] = len(boxes)
            
            for i, box in enumerate(boxes):
                # Extract coordinates and confidence
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = float(box.conf[0])
                
                # Calculate width and height
                width = int(x2 - x1)
                height = int(y2 - y1)
                
                detection = {
                    "box": [int(x1), int(y1), width, height],
                    "confidence": confidence,
                    "class_id": int(box.cls[0]) if len(box.cls) > 0 else 0
                }
                
                detections["all_detections"].append(detection)
            
            # Get highest confidence detection
            if len(detections["all_detections"]) > 0:
                best_detection = max(detections["all_detections"], key=lambda x: x["confidence"])
                detections["tumor_detected"] = True
                detections["confidence"] = round(best_detection["confidence"] * 100, 2)
                detections["bounding_box"] = best_detection["box"]
                logger.info(f"Tumor detected with confidence: {detections['confidence']}%")
            
            return detections
        
        except Exception as e:
            logger.error(f"Error processing results: {str(e)}")
            return {
                "error": str(e),
                "tumor_detected": False,
                "confidence": 0.0
            }
    
    def inference(
        self,
        image_tensor: torch.Tensor,
        original_size: Tuple[int, int]
    ) -> Tuple[Dict, float]:
        """
        Complete inference pipeline: predict -> process results.
        
        Args:
            image_tensor (torch.Tensor): Preprocessed image tensor
            original_size (Tuple[int, int]): Original image dimensions
            
        Returns:
            Tuple[Dict, float]: Detection results and inference time in milliseconds
        """
        try:
            # Record start time
            start_time = time.time()
            
            # Run inference
            results = self.predict(image_tensor)
            
            # Check for errors in predictions
            if isinstance(results, dict) and "error" in results:
                inference_time = (time.time() - start_time) * 1000
                return {"error": results["error"], "tumor_detected": False}, inference_time
            
            # Process results
            detections = self.process_results(results, original_size)
            
            # Calculate inference time
            inference_time = (time.time() - start_time) * 1000
            
            logger.info(f"Inference completed in {inference_time:.2f}ms")
            
            return detections, inference_time
        
        except Exception as e:
            logger.error(f"Error in inference pipeline: {str(e)}")
            return {"error": str(e), "tumor_detected": False}, 0.0
    
    def is_loaded(self) -> bool:
        """
        Check if model is loaded successfully.
        
        Returns:
            bool: True if model is loaded, False otherwise
        """
        return self.model is not None


def create_detector(model_path: str, **kwargs) -> Optional[YOLOv9Detector]:
    """
    Factory function to create YOLOv9 detector instance.
    
    Args:
        model_path (str): Path to model weights
        **kwargs: Additional arguments for YOLOv9Detector
        
    Returns:
        Optional[YOLOv9Detector]: Detector instance or None if creation fails
    """
    try:
        detector = YOLOv9Detector(model_path, **kwargs)
        if detector.is_loaded():
            return detector
        else:
            return None
    
    except Exception as e:
        logger.error(f"Error creating detector: {str(e)}")
        return None
