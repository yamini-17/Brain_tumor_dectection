import requests, io
from PIL import Image
import numpy as np

tumor_detected_count = 0
print("Testing 10 MRI images...")
for i in range(10):
    img_array = np.zeros((640, 640), dtype=np.uint8)
    img_array[:, :] = np.random.randint(140, 180, (640, 640), dtype=np.uint8)
    img_array[100:540, 100:540] = np.random.randint(120, 160, (440, 440), dtype=np.uint8)
    img_array[280:360, 280:360] = np.random.randint(200, 240, (80, 80), dtype=np.uint8)
    
    img = Image.fromarray(img_array, mode='L')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {'image': ('test.png', img_bytes, 'image/png')}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    
    tumor = result.get('tumor_detected')
    conf = result.get('confidence')
    
    if tumor:
        tumor_detected_count += 1
        print(f"Test {i+1}: TUMOR (conf: {conf:.3f})")
    else:
        print(f"Test {i+1}: no tumor (conf: {conf:.3f})")

print(f"\nResult: {tumor_detected_count}/10 detected ({tumor_detected_count*10}%)")
print(f"Expected: ~80% (8 out of 10)")
