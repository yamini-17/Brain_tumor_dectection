# Brain Tumor Detection System - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.10+
- pip or conda
- 4GB+ RAM (8GB+ recommended)
- GPU optional but recommended for production

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Server
```bash
python app.py
```

Expected output:
```
========================================================================
INITIALIZING BRAIN TUMOR DETECTION SYSTEM
========================================================================
✓ Image Preprocessor initialized
✓ YOLOv9 Detector initialized
✓ Inference device: cuda (or cpu)
========================================================================
INITIALIZATION COMPLETE - SYSTEM READY
========================================================================
Starting Flask server on 0.0.0.0:5000
```

### Step 5: Test the API
```bash
# In another terminal
python test_api.py
```

---

## 📋 API Quick Reference

### Health Check
```bash
curl http://localhost:5000/health
```

### System Status
```bash
curl http://localhost:5000/status
```

### Make Prediction
```bash
curl -X POST http://localhost:5000/predict -F "image=@path/to/mri.jpg"
```

---

## 🐳 Docker Quick Start

### Build and Run
```bash
docker-compose up --build
```

### Access API
```bash
curl http://localhost:5000/health
```

### View Logs
```bash
docker-compose logs -f brain-tumor-api
```

---

## 📁 Project Files

```
backend/
├── app.py                 # Main Flask application ⭐
├── config.py              # Configuration settings
├── test_api.py            # API testing script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── Dockerfile             # Docker container setup
├── docker-compose.yml     # Docker Compose orchestration
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── logs/                  # Application logs (auto-created)
├── model/                 # YOLOv9 model directory
│   └── [Download yolov9.pt here]
└── utils/
    ├── preprocess.py      # Image preprocessing
    └── inference.py       # Model inference
```

---

## ⚙️ Configuration

Edit `.env` file to configure:

```env
# Server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Model
MODEL_PATH=model/yolov9.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45

# Upload limits
MAX_IMAGE_SIZE=10485760  # 10MB in bytes
```

---

## 🐛 Troubleshooting

### Issue: "Model file not found"
**Solution:** Download yolov9.pt and place in `model/` directory
```bash
# The model will auto-download on first inference, OR
# manually download from: https://github.com/ultralytics/yolov9/releases
```

### Issue: "GPU not detected"
**Solution:** Verify CUDA installation
```bash
nvidia-smi  # Check GPU
```

### Issue: "Port 5000 already in use"
**Solution:** Change port in `.env`
```env
FLASK_PORT=5001  # Or any available port
```

### Issue: Module import errors
**Solution:** Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## 📊 Performance Tips

1. **GPU Usage:** Automatically enabled if CUDA available
2. **CPU Mode:** Install PyTorch CPU version if no GPU
3. **Memory:** Models loaded once at startup
4. **Inference:** ~20-50ms on GPU, ~200-500ms on CPU

---

## 🔒 Security

- ✓ File type validation
- ✓ File size limits (10MB default)
- ✓ CORS enabled for frontend integration
- ✓ Error logging without sensitive data exposure
- ✓ Input validation on all endpoints

---

## 📦 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn --workers=4 --threads=2 --worker-class=gthread \
  --bind=0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker-compose up -d
```

### Using Systemd (Linux)
Create `/etc/systemd/system/brain-tumor-api.service`:
```ini
[Unit]
Description=Brain Tumor Detection API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/backend
ExecStart=/path/to/venv/bin/gunicorn --workers=4 --bind=0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable brain-tumor-api
sudo systemctl start brain-tumor-api
```

---

## 📝 Example Usage

### Python
```python
import requests

with open('mri.jpg', 'rb') as f:
    response = requests.post('http://localhost:5000/predict', 
                           files={'image': f})
    print(response.json())
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('image', imageFile);

fetch('http://localhost:5000/predict', {
  method: 'POST',
  body: formData
})
.then(r => r.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@mri.jpg"
```

---

## 📞 Support

For full documentation, see [README.md](README.md)

For issues:
1. Check `logs/` directory for error details
2. Verify configuration in `.env`
3. Ensure all dependencies installed
4. Check GPU availability if using GPU

---

**Status:** ✅ Production Ready
**Version:** 1.0.0
**Last Updated:** 2024
