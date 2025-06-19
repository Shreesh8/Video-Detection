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

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Video Object Detection API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}

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

def extract_frames(video_path: str, max_frames: int = 15) -> List[np.ndarray]:
    """Extract frames from video with improved error handling and better sampling"""
    try:
        logger.info(f"Opening video file: {video_path}")
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error("Failed to open video file")
            raise HTTPException(status_code=400, detail="Could not open video file")
            
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if total_frames == 0:
            logger.error("Video file has no frames")
            raise HTTPException(status_code=400, detail="Video file has no frames")
            
        logger.info(f"Total frames in video: {total_frames}, FPS: {fps}")
        
        # Improved frame sampling strategy
        if total_frames <= max_frames:
            # If video is short, take all frames
            step = 1
        else:
            # Take frames from beginning, middle, and end for better coverage
            step = max(1, total_frames // max_frames)
        
        frame_positions = []
        
        # Get frames from different parts of the video
        if total_frames <= max_frames:
            frame_positions = list(range(total_frames))
        else:
            # Take frames from beginning (30%), middle (40%), and end (30%)
            start_frames = int(max_frames * 0.3)
            middle_frames = int(max_frames * 0.4)
            end_frames = max_frames - start_frames - middle_frames
            
            # Beginning frames
            for i in range(start_frames):
                frame_positions.append(i * total_frames // start_frames)
            
            # Middle frames
            middle_start = total_frames // 4
            middle_end = 3 * total_frames // 4
            for i in range(middle_frames):
                frame_positions.append(middle_start + i * (middle_end - middle_start) // middle_frames)
            
            # End frames
            for i in range(end_frames):
                frame_positions.append(total_frames - (end_frames - i) * total_frames // end_frames)
        
        # Extract frames
        for pos in frame_positions:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"Failed to read frame at position {pos}")
                continue
                
            # Skip very dark or very bright frames (likely to be poor quality)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            if 20 < mean_brightness < 235:  # Skip very dark or very bright frames
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
    """Detect objects in a single frame using YOLOv8 with improved accuracy"""
    try:
        # Preprocess frame for better detection
        # Resize frame if it's too large (improves performance and accuracy)
        height, width = frame.shape[:2]
        if width > 1920 or height > 1080:
            scale = min(1920/width, 1080/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Run YOLOv8 inference with confidence threshold
        results = model(frame, verbose=False, conf=0.3, iou=0.5)[0]  # Lower confidence threshold for more detections
        
        # Process results with better filtering
        detections = []
        if results.boxes is not None and len(results.boxes) > 0:
            for r in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                
                # Filter out very low confidence detections
                if score < 0.3:
                    continue
                    
                class_name = results.names[int(class_id)]
                
                # Filter out some common false positives
                if class_name in ['person', 'car', 'truck', 'bus', 'motorcycle', 'bicycle', 
                                'tv', 'laptop', 'cell phone', 'dog', 'cat', 'chair', 'table']:
                    detections.append({
                        "class": class_name,
                        "confidence": float(score),
                        "bbox": [float(x1), float(y1), float(x2), float(y2)]
                    })
        
        return detections
        
    except Exception as e:
        logger.error(f"Error detecting objects: {str(e)}")
        return []

def infer_activity(all_detections):
    """Infer activity from all detections with improved logic"""
    if not all_detections:
        return "No objects detected"
    
    # Count occurrences of each class
    class_counts = {}
    class_confidences = {}
    
    for detection in all_detections:
        class_name = detection['class']
        confidence = detection['confidence']
        
        if class_name not in class_counts:
            class_counts[class_name] = 0
            class_confidences[class_name] = []
        
        class_counts[class_name] += 1
        class_confidences[class_name].append(confidence)
    
    # Calculate average confidence for each class
    avg_confidences = {}
    for class_name, confidences in class_confidences.items():
        avg_confidences[class_name] = sum(confidences) / len(confidences)
    
    # Activity inference with confidence thresholds
    activities = []
    
    # Person-related activities
    if 'person' in class_counts and class_counts['person'] >= 2:  # At least 2 person detections
        person_conf = avg_confidences.get('person', 0)
        
        if person_conf > 0.5:  # High confidence person detection
            if 'tv' in class_counts and class_counts['tv'] >= 1:
                activities.append("Person watching TV")
            if 'laptop' in class_counts and class_counts['laptop'] >= 1:
                activities.append("Person using laptop")
            if 'cell phone' in class_counts and class_counts['cell phone'] >= 1:
                activities.append("Person using phone")
            if 'dog' in class_counts and class_counts['dog'] >= 1:
                activities.append("Person with dog")
            if 'cat' in class_counts and class_counts['cat'] >= 1:
                activities.append("Person with cat")
            if 'car' in class_counts and class_counts['car'] >= 1:
                activities.append("Person near car")
            if 'bicycle' in class_counts and class_counts['bicycle'] >= 1:
                activities.append("Person with bicycle")
            if 'chair' in class_counts and class_counts['chair'] >= 1:
                activities.append("Person sitting")
            if 'table' in class_counts and class_counts['table'] >= 1:
                activities.append("Person at table")
    
    # Vehicle-related activities
    if 'car' in class_counts and class_counts['car'] >= 2:
        activities.append("Multiple cars present")
    if 'truck' in class_counts and class_counts['truck'] >= 1:
        activities.append("Truck present")
    if 'bus' in class_counts and class_counts['bus'] >= 1:
        activities.append("Bus present")
    if 'motorcycle' in class_counts and class_counts['motorcycle'] >= 1:
        activities.append("Motorcycle present")
    
    # Pet-related activities
    if 'dog' in class_counts and class_counts['dog'] >= 2:
        activities.append("Multiple dogs present")
    if 'cat' in class_counts and class_counts['cat'] >= 2:
        activities.append("Multiple cats present")
    
    # If no specific activities found, return general description
    if not activities:
        detected_objects = [f"{count} {class_name}" for class_name, count in class_counts.items() if count > 0]
        if detected_objects:
            return f"Detected: {', '.join(detected_objects)}"
        else:
            return "No specific activity detected"
    
    return "; ".join(activities)

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
            frames = extract_frames(temp_path, max_frames=15)
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

            # Get most common detections with improved processing
            if all_detections:
                from collections import Counter
                class_counts = Counter(d["class"] for d in all_detections)
                
                # Calculate average confidence for each class
                class_confidences = {}
                for detection in all_detections:
                    class_name = detection["class"]
                    if class_name not in class_confidences:
                        class_confidences[class_name] = []
                    class_confidences[class_name].append(detection["confidence"])
                
                # Get top detected objects (up to 5 instead of 3)
                most_common_objects = class_counts.most_common(5)
                
                result = {
                    "detections": [
                        {
                            "class": obj_class,
                            "count": count,
                            "confidence": sum(class_confidences[obj_class]) / len(class_confidences[obj_class]),
                            "total_detections": len(all_detections)
                        }
                        for obj_class, count in most_common_objects
                    ]
                }
                
                # Infer activity
                result["activity"] = infer_activity(all_detections)
                result["frames_processed"] = len(frames)
                result["total_objects_detected"] = len(all_detections)
                
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
                # Try to remove with a different approach if needed
                try:
                    import shutil
                    shutil.rmtree(temp_path, ignore_errors=True)
                except:
                    pass
            
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}") 