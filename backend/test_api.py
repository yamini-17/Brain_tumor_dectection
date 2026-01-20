"""
Test Client for Brain Tumor Detection System
Provides examples of how to use the API programmatically.

Usage:
    python test_api.py
"""

import requests
import json
from pathlib import Path
from typing import Dict, Optional
import time

# Configuration
API_BASE_URL = "http://localhost:5000"
TEST_IMAGE_PATH = "test_image.jpg"  # Provide your test image

class BrainTumorAPIClient:
    """Client for interacting with Brain Tumor Detection API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        """
        Initialize API client.
        
        Args:
            base_url (str): Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        print(f"✓ API Client initialized: {self.base_url}")
    
    def health_check(self) -> Dict:
        """
        Check API health status.
        
        Returns:
            Dict: Health status response
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            return {
                "status": "success",
                "data": response.json(),
                "http_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_status(self) -> Dict:
        """
        Get system status and configuration.
        
        Returns:
            Dict: System status response
        """
        try:
            response = self.session.get(f"{self.base_url}/status", timeout=10)
            return {
                "status": "success",
                "data": response.json(),
                "http_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def predict(self, image_path: str) -> Dict:
        """
        Upload image and get tumor detection prediction.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict: Prediction results
        """
        try:
            # Validate file exists
            if not Path(image_path).exists():
                return {
                    "status": "error",
                    "error": f"Image file not found: {image_path}"
                }
            
            # Open and send file
            with open(image_path, 'rb') as f:
                files = {'image': f}
                
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/predict",
                    files=files,
                    timeout=120
                )
                elapsed_time = time.time() - start_time
            
            return {
                "status": "success",
                "data": response.json(),
                "http_code": response.status_code,
                "request_time_ms": round(elapsed_time * 1000, 2)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


def print_response(title: str, response: Dict):
    """
    Pretty print API response.
    
    Args:
        title (str): Response title
        response (Dict): Response data
    """
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)
    
    if response.get("status") == "error":
        print(f"❌ ERROR: {response.get('error')}")
    else:
        print(f"✓ HTTP Status: {response.get('http_code')}")
        if "request_time_ms" in response:
            print(f"✓ Request Time: {response['request_time_ms']}ms")
        
        data = response.get("data", {})
        print(json.dumps(data, indent=2))


def test_api():
    """Run comprehensive API tests."""
    
    print("\n" + "="*70)
    print("  BRAIN TUMOR DETECTION SYSTEM - API TEST SUITE")
    print("="*70)
    
    client = BrainTumorAPIClient()
    
    # Test 1: Health Check
    print("\n[1/4] Testing Health Check Endpoint...")
    health_response = client.health_check()
    print_response("Health Check Response", health_response)
    
    if health_response.get("status") == "error":
        print("\n❌ API server is not running!")
        print(f"   Error: {health_response.get('error')}")
        print("\n   Run the server first:")
        print("   $ python app.py")
        return
    
    # Test 2: System Status
    print("\n[2/4] Testing System Status Endpoint...")
    status_response = client.get_status()
    print_response("System Status Response", status_response)
    
    # Test 3: Prediction with Test Image
    print("\n[3/4] Testing Prediction Endpoint...")
    
    if not Path(TEST_IMAGE_PATH).exists():
        print(f"\n⚠️  Test image not found: {TEST_IMAGE_PATH}")
        print("   To test predictions, provide a valid MRI image.")
        print("\n   Usage:")
        print("   1. Place your MRI image in the backend directory")
        print("   2. Update TEST_IMAGE_PATH variable in this script")
        print("   3. Run this script again")
    else:
        prediction_response = client.predict(TEST_IMAGE_PATH)
        print_response("Prediction Response", prediction_response)
        
        if prediction_response.get("status") == "success":
            data = prediction_response.get("data", {})
            print("\n📊 PREDICTION SUMMARY:")
            print(f"   Tumor Detected: {'✓ YES' if data.get('tumor_detected') else '✗ NO'}")
            print(f"   Confidence: {data.get('confidence')}%")
            print(f"   Bounding Box: {data.get('bounding_box')}")
            print(f"   Processing Time: {data.get('processing_time_ms')}ms")
    
    # Test 4: Error Handling
    print("\n[4/4] Testing Error Handling...")
    print("\nTesting invalid file extension...")
    
    # Create a dummy file with invalid extension
    invalid_file = "test.txt"
    with open(invalid_file, 'w') as f:
        f.write("This is not an image")
    
    error_response = client.predict(invalid_file)
    print_response("Error Handling Response", error_response)
    
    # Cleanup
    Path(invalid_file).unlink()
    
    # Final Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    print("✓ API Tests Complete!")
    print("\nNext Steps:")
    print("1. Integrate the API with your frontend")
    print("2. Configure CORS settings if needed")
    print("3. Deploy to production using Gunicorn/Nginx")
    print("\nFor detailed documentation, see README.md")
    print("="*70 + "\n")


def demonstrate_api_usage():
    """Show example usage patterns."""
    
    print("\n" + "="*70)
    print("  API USAGE EXAMPLES")
    print("="*70)
    
    print("\n1. Using Python Requests:")
    print("""
    import requests
    
    # Prediction
    with open('mri_image.jpg', 'rb') as f:
        files = {'image': f}
        response = requests.post('http://localhost:5000/predict', files=files)
        print(response.json())
    """)
    
    print("\n2. Using cURL:")
    print("""
    curl -X POST http://localhost:5000/predict \\
      -F "image=@mri_image.jpg"
    """)
    
    print("\n3. Using JavaScript/Fetch:")
    print("""
    const formData = new FormData();
    formData.append('image', imageFile);
    
    fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => console.log(data));
    """)
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    try:
        # Show usage examples
        demonstrate_api_usage()
        
        # Run tests
        test_api()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
