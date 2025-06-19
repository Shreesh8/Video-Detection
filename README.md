# Video Object Detection

A web application that uses YOLOv8 to detect objects in uploaded videos and infer activities.

## Features

- Upload video files (MP4, AVI, MOV, MKV, WMV)
- Object detection using YOLOv8
- Activity inference based on detected objects
- Modern React frontend with Material-UI
- FastAPI backend with comprehensive error handling

## Quick Start

### Option 1: Run Both Servers Together (Recommended)

```bash
python run_app.py
```

This will start both the backend and frontend servers automatically.

### Option 2: Run Servers Separately

#### Backend (API Server)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

#### Frontend (React App)

```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check with model status
- `POST /predict` - Upload video for object detection

## Recent Fixes & Improvements

- ✅ Fixed frontend API endpoint to connect to local backend
- ✅ Added proper error handling and cleanup for temporary files
- ✅ Added health check endpoints
- ✅ Improved CORS configuration
- ✅ Created automated startup script
- ✅ **IMPROVED OBJECT DETECTION ACCURACY:**
  - Lowered confidence threshold (0.3) for more detections
  - Better frame sampling strategy (beginning, middle, end)
  - Frame quality filtering (skips very dark/bright frames)
  - Improved activity inference with confidence thresholds
  - Enhanced detection filtering for common objects
  - Better confidence calculation and averaging
- ✅ **ENHANCED USER EXPERIENCE:**
  - Shows processing statistics (frames processed, total objects)
  - More detailed activity descriptions
  - Better error messages and logging
  - Improved frontend display of results

## Requirements

- Python 3.8+
- Node.js 16+
- npm

## Dependencies

### Backend

- FastAPI
- Uvicorn
- OpenCV
- Ultralytics (YOLOv8)
- NumPy

### Frontend

- React
- Material-UI
- Axios

## Usage

1. Open the application in your browser at `http://localhost:3000`
2. Click "Select Video" to choose a video file
3. Click "Analyze Video" to process the video
4. View the detected objects and inferred activity

## Troubleshooting

- If you get CORS errors, make sure the backend is running on `http://localhost:8000`
- If the model fails to load, check that `yolov8n.pt` is in the backend directory
- For video processing issues, ensure the video format is supported (MP4, AVI, MOV, MKV, WMV)
