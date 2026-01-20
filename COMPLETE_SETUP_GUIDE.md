# 🚀 BRAIN TUMOR DETECTION - COMPLETE SETUP & RUN GUIDE

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ **Python 3.8+** - Download from https://www.python.org
- ✅ **Node.js 16+** - Download from https://nodejs.org
- ✅ **Git** (optional) - Download from https://git-scm.com

### Verify Installation

```bash
python --version          # Should show Python 3.8+
node --version           # Should show Node 16+
npm --version            # Should show npm 7+
```

---

## 🎯 Option 1: Automated Setup (Windows Batch File)

### Quick Start (Recommended)
1. Double-click `START_SYSTEM.bat` in the project root
2. Wait for both servers to start
3. Opens automatically on http://localhost:3000

This batch script will:
✅ Verify Node.js and Python are installed
✅ Install frontend dependencies
✅ Install backend dependencies
✅ Start Flask backend on port 5000
✅ Start React frontend on port 3000

---

## 🎯 Option 2: Manual Setup (Command Line)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production deployment.
```

### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

**Expected output:**
```
  VITE v4.3.9 dev server running at:
  
  ➜ Local: http://localhost:3000/
```

### Step 3: Open Browser

Navigate to **http://localhost:3000**

---

## ✅ Verification Checklist

### Backend Status
```bash
# In backend folder, test API connection:
curl http://localhost:5000/health
```

**Expected response:**
```json
{"status": "ok", "message": "Server is running"}
```

### Frontend Status
- [ ] Page loads at http://localhost:3000
- [ ] Upload component visible
- [ ] No console errors (F12)
- [ ] Can select/drag images

### System Test
- [ ] Upload a test image
- [ ] Click "Analyze MRI Image"
- [ ] Results display within 30 seconds
- [ ] No errors in console

---

## 📱 Testing the Application

### Test Image Locations
- Backend: `backend/test_images/` folder
- Use any `.jpg`, `.png`, `.bmp` format
- Recommended: 512x512 to 1024x1024 resolution

### Test Workflow
1. Go to http://localhost:3000
2. Click upload area or drag image
3. Select test image
4. Wait for analysis
5. View results:
   - Detection status (Positive/Negative)
   - Confidence percentage
   - Bounding box coordinates
   - Processing time

---

## 🔧 Configuration

### Backend Settings
**File:** `backend/.env`

```env
FLASK_ENV=development
FLASK_DEBUG=1
MODEL_PATH=model/best.pt
MAX_FILE_SIZE=10485760
```

### Frontend Settings
**File:** `frontend/.env`

```env
REACT_APP_API_URL=http://localhost:5000
```

For production, change to:
```env
REACT_APP_API_URL=/api
```

---

## 🐛 Troubleshooting

### Port Already in Use

**Backend (Port 5000)**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (Port 3000)**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Backend Won't Start
```bash
# Clear cache and reinstall
cd backend
rm -rf __pycache__
pip install -r requirements.txt --force-reinstall
python app.py
```

### Frontend Dependencies Issue
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API Connection Error
- ✅ Verify backend is running on port 5000
- ✅ Check `REACT_APP_API_URL` in `.env`
- ✅ Check CORS is enabled in `app.py`
- ✅ Check firewall settings

### Model Not Loading
```bash
# Verify model exists
cd backend
ls -la model/

# Download if missing
python utils/download_model.py
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│           BRAIN TUMOR DETECTION SYSTEM              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐        ┌──────────────────┐  │
│  │   React Frontend │        │  Flask Backend   │  │
│  │  (Port 3000)     │◄──────►│  (Port 5000)     │  │
│  │                  │        │                  │  │
│  │ • Upload UI      │        │ • API Server     │  │
│  │ • Preview        │        │ • Image Process  │  │
│  │ • Results Display│        │ • YOLOv9 Model   │  │
│  │ • Error Handling │        │ • Inference      │  │
│  └──────────────────┘        └──────────────────┘  │
│           │                           │             │
│           │      HTTP/REST API        │             │
│           └───────────────────────────┘             │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │         YOLOv9 Detection Model               │  │
│  │    (Requires GPU or CPU - TorchVision)       │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Production Deployment

### Build Frontend for Production
```bash
cd frontend
npm run build
# Output: dist/ folder (ready to deploy)
```

### Deploy Options

**Option 1: Docker (Recommended)**
```bash
# Backend
cd backend
docker build -t brain-tumor-backend .
docker run -p 5000:5000 brain-tumor-backend

# Frontend
cd frontend
docker build -t brain-tumor-frontend .
docker run -p 80:3000 brain-tumor-frontend
```

**Option 2: Cloud Deployment**
- **Frontend:** Vercel, Netlify, AWS S3 + CloudFront
- **Backend:** Heroku, AWS EC2, Google Cloud Run, DigitalOcean

**Option 3: Local Server**
```bash
# Backend
python app.py --host 0.0.0.0 --port 5000

# Frontend (with Node.js server)
npm run build
npx serve -s dist -l 3000
```

---

## 📈 System Requirements

### Minimum
- CPU: 4-core processor
- RAM: 8 GB
- Storage: 5 GB
- GPU: Optional (CPU mode supported)

### Recommended
- CPU: 8-core processor or higher
- RAM: 16 GB
- Storage: 10 GB SSD
- GPU: NVIDIA with CUDA 11.8+
- Bandwidth: 100 Mbps

---

## 📝 API Documentation

### Health Check
```bash
GET http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### Predict (Main Endpoint)
```bash
POST http://localhost:5000/predict
Content-Type: multipart/form-data

Body: file (image file)
```

**Response (Tumor Detected):**
```json
{
  "tumor_detected": true,
  "confidence": 95.8,
  "bounding_box": [120, 150, 200, 180],
  "processing_time_ms": 23.45,
  "detections_count": 1
}
```

**Response (No Tumor):**
```json
{
  "tumor_detected": false,
  "confidence": 0.0,
  "bounding_box": [],
  "processing_time_ms": 18.20,
  "detections_count": 0
}
```

### Error Response
```json
{
  "error": "File too large",
  "message": "Maximum file size is 10 MB"
}
```

---

## 🔑 Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Server health check |
| POST | `/predict` | Analyze MRI image |
| GET | `/status` | System status |
| GET | `/` | Serve API documentation |

---

## 💡 Tips & Best Practices

### Performance
- Use GPU when available (10-50x faster)
- Batch process images for bulk analysis
- Cache preprocessed images
- Use compression for file transfer

### Security
- Validate file types on backend
- Implement rate limiting
- Use HTTPS in production
- Store models securely
- Validate all inputs

### Development
- Use `.env` files for configuration
- Keep logs for debugging
- Use version control (Git)
- Write unit tests
- Document changes

---

## 📚 Additional Resources

### Documentation
- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [YOLOv9 Guide](https://docs.ultralytics.com/models/yolov9/)
- [Vite Guide](https://vitejs.dev)

### Model Training
- Custom training: See `backend/INSTALLATION.md`
- Transfer learning: Available in ultralytics
- Dataset formats: COCO, YOLOv8 format

### Community
- Report issues on GitHub
- Check existing solutions first
- Provide detailed error messages
- Include system info and steps to reproduce

---

## ❓ FAQ

**Q: Can I use CPU only?**
A: Yes, the model works on CPU but slower (30-60s vs 0.5-2s on GPU)

**Q: What image formats are supported?**
A: JPG, PNG, BMP, GIF, TIFF (auto-detected)

**Q: What's the maximum file size?**
A: 10 MB (configurable in backend/.env)

**Q: Can I use my own model?**
A: Yes, replace `backend/model/best.pt` with your trained model

**Q: How do I run both on same machine?**
A: Use ports 3000 (frontend) and 5000 (backend), or use docker-compose

**Q: Can I deploy to the cloud?**
A: Yes, see Production Deployment section

**Q: Is GPU required?**
A: No, but highly recommended for better performance

---

## 🎯 Next Steps

1. ✅ Install prerequisites (Python, Node.js)
2. ✅ Run `START_SYSTEM.bat` or follow manual steps
3. ✅ Open http://localhost:3000 in browser
4. ✅ Test with sample image
5. ✅ Review results and confidence scores
6. ✅ Deploy to production when ready

---

## 📞 Support

For issues:
1. Check troubleshooting section
2. Review console logs (F12 in browser)
3. Check terminal output for errors
4. Verify prerequisites are installed
5. Try restarting both services

---

**Happy analyzing! 🧠💙**
