import base64
import io
from PIL import Image

# Read the test_annotated image and verify it has a red box drawn
img = Image.open('c:\\Users\\91636\\Downloads\\test_annotated.png')

# Convert to RGB if needed
if img.mode == 'L':
    img = img.convert('RGB')

# Get pixels and check for red color (255, 0, 0)
pixels = img.load()
width, height = img.size

red_pixels = 0
# Check the area where we expect the bounding box [138, 255, 150, 128]
x_start, y_start = 138, 255
x_end = x_start + 150
y_end = y_start + 128

# Count red pixels in and around the bounding box area
for x in range(max(0, x_start - 5), min(width, x_end + 5)):
    for y in range(max(0, y_start - 5), min(height, y_end + 5)):
        r, g, b = pixels[x, y][:3] if len(pixels[x, y]) >= 3 else pixels[x, y]
        if r > 200 and g < 100 and b < 100:  # Red-ish
            red_pixels += 1

print(f'Image size: {width} x {height}')
print(f'Bounding box area: [{x_start}, {y_start}, {x_end}, {y_end}]')
print(f'Red pixels found in/around bounding box: {red_pixels}')
print(f'')
if red_pixels > 100:
    print('✓ SUCCESS: Bounding box is drawn INSIDE the image in red!')
else:
    print('✗ ISSUE: Red pixels not found where expected')
