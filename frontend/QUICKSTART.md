# Quick Start Guide - Brain Tumor Detection Frontend

## ⚡ 5-Minute Setup

### Prerequisites
- Node.js 14+ installed
- Backend running on http://localhost:5000

### Quick Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

**That's it!** App opens at http://localhost:3000

## 🚀 Using the Application

1. **Upload Image**
   - Drag & drop MRI image OR click to select
   - Supported: JPG, PNG, BMP, GIF, TIFF
   - Max size: 10MB

2. **View Results**
   - Tumor detection status
   - Confidence percentage
   - Bounding box overlay
   - Processing time

3. **Analyze Again**
   - Click "Re-analyze" button
   - Or upload new image

## 📦 Build for Production

```bash
npm run build
npm run preview
```

Output: `dist/` folder ready to deploy

## 🐛 Troubleshooting

### "Cannot connect to API"
- Check backend is running: `python app.py`
- Verify port 5000 is open
- Check `.env` file: `REACT_APP_API_URL=http://localhost:5000`

### "Port 3000 already in use"
- Edit `vite.config.js`: Change port to 3001
- Or kill process: `lsof -ti:3000 | xargs kill -9`

### "npm install fails"
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📚 Documentation

- **Full docs**: README.md
- **API integration**: utils/api.js
- **Components**: src/components/

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Start dev server
3. ✅ Upload test image
4. ✅ Build for production

---

**Status**: Ready to Use ✅
