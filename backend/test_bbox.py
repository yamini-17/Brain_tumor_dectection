import requests
import io
from PIL import Image
import numpy as np
import base64

# Create high-contrast MRI image
print('Creating high-contrast MRI image...')
img_array = np.zeros((640, 640), dtype=np.uint8)
img_array[:, :] = np.random.randint(140, 180, (640, 640), dtype=np.uint8)
img_array[100:540, 100:540] = np.random.randint(120, 160, (440, 440), dtype=np.uint8)
img_array[280:360, 280:360] = np.random.randint(200, 240, (80, 80), dtype=np.uint8)

img = Image.fromarray(img_array, mode='L')
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Upload and get annotated image
print('Uploading to backend...')
files = {'image': ('test.png', img_bytes, 'image/png')}
response = requests.post('http://localhost:5000/predict', files=files)
result = response.json()

print(f'Tumor detected: {result["tumor_detected"]}')
print(f'Confidence: {result["confidence"]:.3f}')

if result.get('annotated_image'):
    # Extract base64 from data URI
    annot_b64 = result['annotated_image'].split(',')[1]
    annot_img = Image.open(io.BytesIO(base64.b64decode(annot_b64)))
    annot_img.save('c:\\Users\\91636\\Downloads\\test_annotated.png')
    print('✓ Annotated image saved to c:\\Users\\91636\\Downloads\\test_annotated.png')
    print(f'Image size: {annot_img.size}')
    
    # Also print bbox info
    print(f'Bounding box: {result.get("bounding_box")}')
