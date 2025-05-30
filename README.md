# Video Object Detection

A web application that performs object detection and activity recognition on uploaded videos.

## Features

- Video upload and processing
- Object detection with confidence scores
- Activity recognition
- Modern React frontend with Material-UI
- FastAPI backend

## Project Structure

- `frontend/`: React application with Material-UI
- `backend/`: FastAPI server for video processing

## Setup

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
uvicorn main:app --reload
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload a video file
3. Click "Analyze Video" to process the video
4. View the detection results and activity recognition output 