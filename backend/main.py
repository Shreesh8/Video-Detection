import io
import os
import cv2
import numpy as np
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None

@app.on_event("startup")
async def startup_event():
    """Load the YOLO model when the server starts"""
    global model
    try:
        logger.info("Loading YOLOv8 model...")
        model = YOLO('yolov8n.pt')  # Using YOLOv8 nano model
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise Exception("Failed to load model")

def load_model():
    """Get the loaded model"""
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return model

def validate_video_file(file: UploadFile) -> None:
    """Validate the uploaded video file"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided")
    
    # Check file extension
    allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
        )

def extract_frames(video_path: str, max_frames: int = 10) -> List[np.ndarray]:
    """Extract frames from video with improved error handling"""
    try:
        logger.info(f"Opening video file: {video_path}")
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error("Failed to open video file")
            raise HTTPException(status_code=400, detail="Could not open video file")
            
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            logger.error("Video file has no frames")
            raise HTTPException(status_code=400, detail="Video file has no frames")
            
        logger.info(f"Total frames in video: {total_frames}")
        
        # Calculate frame sampling rate
        step = max(1, total_frames // max_frames)
        
        for i in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"Failed to read frame at position {i}")
                continue
                
            frames.append(frame)
            
            if len(frames) >= max_frames:
                break
                
        cap.release()
        
        if not frames:
            logger.error("No frames could be extracted from video")
            raise HTTPException(status_code=400, detail="No frames could be extracted from video")
            
        logger.info(f"Successfully extracted {len(frames)} frames")
        return frames
        
    except Exception as e:
        logger.error(f"Error extracting frames: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

def detect_objects(frame: np.ndarray) -> List[Dict[str, Any]]:
    """Detect objects in a single frame using YOLOv8"""
    try:
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=False)[0]
        
        # Process results
        detections = []
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            class_name = results.names[int(class_id)]
            detections.append({
                "class": class_name,
                "confidence": float(score),
                "bbox": [float(x1), float(y1), float(x2), float(y2)]
            })
        
        return detections
        
    except Exception as e:
        logger.error(f"Error detecting objects: {str(e)}")
        return []

def infer_activity(detections):
    classes = set(d['class'] for d in detections)
    if 'person' in classes and 'tv' in classes:
        return "person is watching TV"
    if 'person' in classes and 'cell phone' in classes:
        return "person is using a phone"
    if 'person' in classes and 'dog' in classes:
        return "person is with a dog"
    if 'person' in classes and 'laptop' in classes:
        return "person is using a laptop"
    if 'person' in classes and 'car' in classes:
        return "person is near a car"
    if 'person' in classes and 'bicycle' in classes:
        return "person is riding a bicycle"
    # Add more rules as needed
    return "No specific activity inferred"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Handle video prediction with comprehensive error handling"""
    try:
        # Validate input file
        validate_video_file(file)
        logger.info(f"Received video file: {file.filename}")
        
        # Load model if not already loaded
        try:
            load_model()
        except Exception as e:
            logger.error(f"Model loading error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
        
        # Save uploaded video to disk
        temp_path = f"temp_{file.filename}"
        try:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file received")
                
            with open(temp_path, "wb") as f:
                f.write(content)
            logger.info(f"Video saved to {temp_path}")
            
        except Exception as e:
            logger.error(f"Error saving video file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to save video file: {str(e)}")

        try:
            # Extract frames
            frames = extract_frames(temp_path, max_frames=10)
            logger.info(f"Successfully extracted {len(frames)} frames")
            
            # Detect objects in frames
            all_detections = []
            for i, frame in enumerate(frames):
                detections = detect_objects(frame)
                if detections:
                    all_detections.extend(detections)
                    logger.info(f"Frame {i+1}: Detected {len(detections)} objects")
                else:
                    logger.warning(f"No objects detected in frame {i+1}")
                logger.info(f"Processed frame {i+1}/{len(frames)}")

            # Get most common detections
            if all_detections:
                from collections import Counter
                class_counts = Counter(d["class"] for d in all_detections)
                most_common_objects = class_counts.most_common(3)  # Top 3 detected objects
                
                result = {
                    "detections": [
                        {
                            "class": obj_class,
                            "count": count,
                            "confidence": sum(d["confidence"] for d in all_detections if d["class"] == obj_class) / count
                        }
                        for obj_class, count in most_common_objects
                    ]
                }
                # Infer activity
                result["activity"] = infer_activity(all_detections)
                logger.info(f"Final detections: {result}")
                return result
            else:
                logger.error("No objects detected in any frames")
                raise HTTPException(status_code=400, detail="No objects detected in the video")
                
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
            
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    logger.info("Temporary file removed")
            except Exception as e:
                logger.warning(f"Error removing temporary file: {str(e)}")
            
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") 