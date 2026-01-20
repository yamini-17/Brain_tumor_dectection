import requests
import io
from PIL import Image
import numpy as np

print("Testing improved detection algorithm (75% rate for MRI images)")
print("=" * 70)

tumor_count = 0
non_tumor_count = 0

for test_num in range(10):
    # Create high-contrast realistic MRI image
    img_array = np.zeros((640, 640), dtype=np.uint8)
    # White matter background with good contrast
    img_array[:, :] = np.random.randint(140, 180, (640, 640), dtype=np.uint8)
    # Gray matter
    img_array[100:540, 100:540] = np.random.randint(120, 160, (440, 440), dtype=np.uint8)
    # Bright spots (tumor-like regions)
    img_array[280:360, 280:360] = np.random.randint(200, 240, (80, 80), dtype=np.uint8)
    
    # Convert to image
    img = Image.fromarray(img_array, mode='L')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Upload to backend
    files = {'image': ('test.png', img_bytes, 'image/png')}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    tumor_detected = result.get('tumor_detected')
    confidence = result.get('confidence')
    
    if tumor_detected:
        tumor_count += 1
        status = "✓ TUMOR DETECTED"
    else:
        non_tumor_count += 1
        status = "✗ NO TUMOR"
    
    print(f"Test {test_num + 1:2d}: {status:18} | Confidence: {confidence:.3f}")

print("=" * 70)
print(f"RESULTS: {tumor_count}/10 detected as tumor ({tumor_count * 10}%)")
print(f"         {non_tumor_count}/10 detected as non-tumor")
print(f"Expected: ~75% (7-8 out of 10)")
if tumor_count >= 7:
    print("✓ IMPROVED DETECTION WORKING WELL!")
elif tumor_count >= 5:
    print("⚠ IMPROVED BUT COULD BE BETTER")
else:
    print("✗ DETECTION STILL TOO LOW")
