from typing import List

import cv2
import mediapipe as mp
import numpy as np
from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: float
    y: float
    w: float
    h: float


class StreamFaceDetector:
    def __init__(self) -> None:
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
                relative_bbox = detection.location_data.relative_bounding_box

                # Convert normalized coordinates to pixel coordinates
                x = int(relative_bbox.xmin * width)
                y = int(relative_bbox.ymin * height)
                w = int(relative_bbox.width * width)
                h = int(relative_bbox.height * height)

                # Ensure coordinates are non-negative
                x = max(0, x)
                y = max(0, y)
                w = max(0, w)
                h = max(0, h)

                bounding_boxes.append(BoundingBox(x=x, y=y, w=w, h=h))

        return bounding_boxes

    def close(self) -> None:
        """Clean up resources."""
        if hasattr(self, 'face_detection') and self.face_detection:
            self.face_detection.close()
