
from typing import List
from pydantic import BaseModel
from stream_detector.detector import BoundingBox


class RespObject(BaseModel):
    faces: List[BoundingBox]
    video_id: str
    frame_id: int

def send_results_next_service(results: List[RespObject]):
    """
    You can assume that this function sends the results to the next
    Service in the pipeline.
    """
    pass
