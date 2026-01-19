import numpy as np
from typing import List
from pydantic import BaseModel
import mediapipe as mp
import cv2


class BoundingBox(BaseModel):
    x: float
    y: float
    w: float
    h: float


class StreamFaceDetector:
    def __init__(self):
        """Initialize Mediapipe Face Detection model."""
        # Initialize Mediapipe Face Detection with short-range model
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,  # 0 for short-range detection (within 2 meters)
            min_detection_confidence=0.5
        )
    
    def detect_faces(self, frame: np.ndarray) -> List[BoundingBox]:
        """
        Detect faces in the provided frame using Mediapipe Face Detection.
        
        Args:
            frame: Input frame as numpy array in BGR format (OpenCV default)
        
        Returns:
            List of BoundingBox objects containing face locations
        """
        # Convert BGR to RGB (Mediapipe expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Process the frame with Mediapipe
        results = self.face_detection.process(rgb_frame)
        
        bounding_boxes = []
        
        # Extract bounding boxes if faces are detected
        if results.detections:
            for detection in results.detections:
                # Get bounding box from detection
                bboxC = detection.location_data.relative_bounding_box
                
                # Convert normalized coordinates to pixel coordinates
                x = int(bboxC.xmin * width)
                y = int(bboxC.ymin * height)
                w = int(bboxC.width * width)
                h = int(bboxC.height * height)
                
                # Ensure coordinates are non-negative
                x = max(0, x)
                y = max(0, y)
                w = max(0, w)
                h = max(0, h)
                
                bounding_boxes.append(BoundingBox(x=x, y=y, w=w, h=h))
        
        return bounding_boxes
    
    def close(self):
        """Clean up resources."""
        if hasattr(self, 'face_detection') and self.face_detection:
            self.face_detection.close()
