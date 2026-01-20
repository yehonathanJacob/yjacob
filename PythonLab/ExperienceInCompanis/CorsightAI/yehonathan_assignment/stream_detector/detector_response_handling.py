"""
Response handling module for face detection results.

Defines response models and placeholder function for sending results
to downstream services.
"""
from typing import List

from pydantic import BaseModel

from detector import BoundingBox


class RespObject(BaseModel):
    """Response object containing face detection results for a frame."""

    faces: List[BoundingBox]
    video_id: str
    frame_id: int


def send_results_next_service(results: List[RespObject]) -> None:
    """
    Send face detection results to the next service in the pipeline.

    This is a placeholder function that would normally send the detection
    results to a downstream service for further processing or storage.
    """
    pass
