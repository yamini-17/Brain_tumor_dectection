# Brain Tumor Detection System - Installation & Startup Guide

## 📋 System Requirements

- **Python:** 3.10 or higher
- **RAM:** 4GB minimum (8GB+ recommended)
- **Storage:** 5GB for model and dependencies
- **GPU:** Optional (NVIDIA GPU with CUDA for faster inference)
- **OS:** Windows, macOS, or Linux

## ⚡ Quick Installation (Automated)

### Windows
```batch
python setup.py
```

### macOS / Linux
```bash
python3 setup.py
```

This will automatically:
- ✓ Verify Python version
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Create necessary directories
- ✓ Check for model file

## 🔧 Manual Installation

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask 2.3.2 - Web framework
- Flask-CORS 4.0.0 - Cross-origin support
- OpenCV 4.8.0 - Image processing
- PyTorch 2.0.1 - Deep learning framework
- YOLOv9 (ultralytics 8.0.207) - Object detection
- NumPy 1.24.3 - Numerical computing
- Plus additional dependencies

### 3. Download Model (Optional - Auto-downloads)

The model will auto-download on first inference. For manual download:

```bash
# Using Python
python -c "from ultralytics import YOLO; YOLO('yolov9.pt')"

# Or download from GitHub
# https://github.com/ultralytics/yolov9/releases
# Place the .pt file in the model/ directory
```

### 4. Verify Installation

```bash
python -c "import torch, cv2, ultralytics; print('✓ All packages installed')"
```

## 🚀 Starting the Server

### Method 1: Direct Python (Development)
```bash
python app.py
```

**Expected Output:**
```
========================================================================
INITIALIZING BRAIN TUMOR DETECTION SYSTEM
========================================================================
✓ Image Preprocessor initialized
✓ YOLOv9 Detector initialized
✓ Inference device: cuda:0 (or cpu)
========================================================================
INITIALIZATION COMPLETE - SYSTEM READY
========================================================================
Starting Flask server on 0.0.0.0:5000
 * Running on http://0.0.0.0:5000
```

### Method 2: Gunicorn (Production)
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn --workers=4 --threads=2 --worker-class=gthread \
  --bind=0.0.0.0:5000 \
  --timeout=120 \
  --access-logfile=logs/access.log \
  --error-logfile=logs/error.log \
  app:app
```

### Method 3: Docker (Production)
```bash
docker-compose up --build
```

## 📡 Testing the API

### In a New Terminal (Keep Server Running)

```bash
# Test 1: Health Check
curl http://localhost:5000/health

# Test 2: System Status
curl http://localhost:5000/status

# Test 3: Make Prediction (replace path with actual image)
curl -X POST http://localhost:5000/predict \
  -F "image=@path/to/mri_image.jpg"
```

### Using Python Test Script
```bash
python test_api.py
```

This will:
- ✓ Check health endpoint
- ✓ Get system status
- ✓ Test predictions
- ✓ Validate error handling

### Using Python Requests
```python
import requests

# Make prediction
with open('mri_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    print(response.json())
```

## ✅ Verification Checklist

After startup, verify:

- [ ] Server runs without errors
- [ ] No "Model not loaded" messages
- [ ] GPU detected (if available)
- [ ] Health check returns 200
- [ ] Status shows model_loaded: true
- [ ] Prediction endpoint accepts images
- [ ] Response includes tumor_detected and confidence

## 🐛 Common Issues & Solutions

### Issue 1: "Python 3.10+ required"
**Solution:** Install Python 3.10+
```bash
python --version  # Check current version
# Download from python.org or use package manager
```

### Issue 2: "Module not found: 'torch'"
**Solution:** Reinstall dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue 3: "CUDA out of memory"
**Solution:** Use CPU instead
```bash
# Add to app.py or set environment variable
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### Issue 4: "Model file not found"
**Solution:** Model auto-downloads on first inference
- Or manually download from: https://github.com/ultralytics/yolov9/releases
- Place in: `backend/model/yolov9.pt`

### Issue 5: "Port 5000 already in use"
**Solution:** Change port in `.env`
```env
FLASK_PORT=5001
```

### Issue 6: "Permission denied" (macOS/Linux)
**Solution:** Make script executable
```bash
chmod +x setup.py
python3 setup.py
```

## 📊 Performance Expectations

### Inference Speed
- **GPU (RTX 3090):** 15-25ms
- **GPU (RTX 2080):** 30-50ms
- **CPU (i7):** 200-500ms

### Memory Usage
- **GPU:** 2-4GB VRAM
- **CPU:** 500MB-1GB RAM

### First Run
- Model download: 2-3 minutes
- First inference: May be slower (compilation)

## 🔒 Security Notes

1. **File Upload Limit:** 10MB (configurable)
2. **Allowed Formats:** JPG, PNG, BMP, GIF, TIFF
3. **CORS:** Enabled for all origins (restrict in production)
4. **Error Logging:** Detailed logs in `logs/` directory

## 📚 Documentation Files

- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick reference
- **INSTALLATION.md** - This file

## 🆘 Getting Help

### Check Logs
```bash
# View recent logs
tail -f logs/app_*.log

# Search for errors
grep ERROR logs/app_*.log
```

### Common Log Messages

**✓ Success:**
```
✓ Image Preprocessor initialized
✓ YOLOv9 Detector initialized
✓ INITIALIZATION COMPLETE
```

**❌ Error:**
```
✗ Model file not found
✗ Failed to load YOLOv9 model
✗ Error during inference
```

## 🎯 Next Steps

1. **Development:**
   - Run `python app.py`
   - Test with `python test_api.py`
   - Check `logs/` for debugging

2. **Production:**
   - Use `gunicorn` with multiple workers
   - Set up `nginx` as reverse proxy
   - Configure CORS properly
   - Use `docker-compose` for deployment

3. **Integration:**
   - Connect frontend to `/predict` endpoint
   - Handle responses (tumor_detected, confidence, bounding_box)
   - Display results in UI

## 📞 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health status check |
| `/status` | GET | System configuration |
| `/predict` | POST | Brain tumor detection |

## ⚙️ Configuration

Edit `.env` to customize:

```env
FLASK_HOST=0.0.0.0              # Server address
FLASK_PORT=5000                 # Server port
FLASK_DEBUG=False               # Debug mode
MODEL_PATH=model/yolov9.pt      # Model location
CONFIDENCE_THRESHOLD=0.5        # Detection threshold
IOU_THRESHOLD=0.45              # NMS threshold
MAX_IMAGE_SIZE=10485760         # 10MB upload limit
```

## ✨ Tips & Tricks

- **Speed up startup:** Pre-download model before first use
- **Save bandwidth:** Use ONNX format for inference (optional)
- **Monitor performance:** Check logs for inference times
- **Debug issues:** Enable DEBUG=True in .env
- **Batch processing:** Multiple requests handled by threading

---

**Status:** ✅ Ready to Deploy  
**Version:** 1.0.0  
**Last Updated:** 2024

For detailed API usage, see **README.md**
