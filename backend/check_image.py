from PIL import Image
import numpy as np

# Read the annotated image
img = Image.open('c:\\Users\\91636\\Downloads\\test_annotated.png')
print(f'Image mode: {img.mode}')
print(f'Image size: {img.size}')

# Convert to array
img_array = np.array(img)
print(f'Array shape: {img_array.shape}')
print(f'Array dtype: {img_array.dtype}')
print(f'Array value range: {img_array.min()} - {img_array.max()}')

# Check if it's grayscale or RGB
if len(img_array.shape) == 2:
    print('Image is GRAYSCALE')
    # Check expected bbox area [138, 255, 150, 128]
    x_start, y_start, w, h = 138, 255, 150, 128
    x_end, y_end = x_start + w, y_start + h
    bbox_area = img_array[y_start:y_end, x_start:x_end]
    print(f'Bounding box area: [{x_start}:{x_end}, {y_start}:{y_end}]')
    print(f'Pixel values in bbox area: min={bbox_area.min()}, max={bbox_area.max()}, mean={bbox_area.mean():.1f}')
    
    # Check edges where the box should be drawn
    print(f'\nEdge pixels (should be darker for box outline):')
    print(f'  Top edge: {img_array[y_start, x_start:x_start+20]}')
    print(f'  Left edge: {img_array[y_start:y_start+20, x_start]}')
    print(f'  Bottom edge: {img_array[y_end-1, x_start:x_start+20]}')
    print(f'  Right edge: {img_array[y_start:y_start+20, x_end-1]}')
elif len(img_array.shape) == 3:
    print(f'Image is RGB/RGBA with {img_array.shape[2]} channels')
