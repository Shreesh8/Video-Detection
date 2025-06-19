# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Start Both Servers (Easiest)

```bash
python run_app.py
```

### 2. Open Your Browser

Go to: http://localhost:3000

### 3. Test the Application

- Click "Select Video" to choose a video file
- Click "Analyze Video" to process it
- View the detected objects and activities

## 🧪 Test the API

```bash
python test_detection.py
```

## 📁 What's New in This Version

### Improved Object Detection

- **Better Accuracy**: Lower confidence thresholds and improved filtering
- **Smart Frame Sampling**: Takes frames from beginning, middle, and end of video
- **Quality Filtering**: Skips poor quality frames automatically
- **Enhanced Activities**: More detailed activity descriptions

### Better User Experience

- **Processing Stats**: Shows frames processed and total objects detected
- **Detailed Results**: Up to 5 most common objects with confidence scores
- **Better Error Handling**: Clear error messages and logging

## 🔧 Troubleshooting

### Backend Issues

- Make sure you're in the backend directory: `cd backend`
- Check if model is loaded: `curl http://localhost:8000/health`

### Frontend Issues

- Make sure backend is running on port 8000
- Check browser console for CORS errors

### Video Issues

- Supported formats: MP4, AVI, MOV, MKV, WMV
- Video should be clear and well-lit for best results
- Longer videos are processed more thoroughly

## 📊 Expected Results

The improved detection should now:

- Detect more objects with higher accuracy
- Provide better activity descriptions
- Show processing statistics
- Handle various video qualities better
