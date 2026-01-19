import numpy as np
from typing import List
from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: float
    y: float
    w: float
    h: float

class StreamFaceDetector:
    def __init__(self):
        pass
    
    def detect_faces(self, frame: np.ndarray) -> List[BoundingBox]:
        """
        This is a mock function, in reality this function
        would perform an heavy ML model inference.
        """
        return [
            BoundingBox(x=0, y=0, w=100, h=100),
            BoundingBox(x=100, y=100, w=100, h=100)
            ]
