import base64
import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Literal, Optional

import cv2
from aio_pika import DeliveryMode, Message, connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
QUEUE_NAME = "frame_processing_queue"
QUEUE_TTL_MS = 3600000  # 1 hour
JPEG_QUALITY = 85
RABBITMQ_DEFAULT_HOST = "rabbitmq"
RABBITMQ_DEFAULT_PORT = 5672
RABBITMQ_DEFAULT_USER = "guest"
RABBITMQ_DEFAULT_PASSWORD = "guest"

# Global variables for RabbitMQ connection
rabbitmq_connection: Optional[AbstractRobustConnection] = None
rabbitmq_channel: Optional[AbstractChannel] = None


class AnalyzeRequest(BaseModel):
    file_path: str = Field(..., description="Path to the video file")
    fps: Literal[2, 4] = Field(..., description="Target FPS for frame extraction (2 or 4)")


class AnalyzeResponse(BaseModel):
    status: str
    video_id: str
    frames_processed: int
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app initialization and cleanup."""
    global rabbitmq_connection, rabbitmq_channel

    # Startup: Initialize RabbitMQ connection
    rabbitmq_host = os.getenv("RABBITMQ_HOST", RABBITMQ_DEFAULT_HOST)
    rabbitmq_port = int(os.getenv("RABBITMQ_PORT", str(RABBITMQ_DEFAULT_PORT)))
    rabbitmq_user = os.getenv("RABBITMQ_USER", RABBITMQ_DEFAULT_USER)
    rabbitmq_password = os.getenv(
        "RABBITMQ_PASSWORD", RABBITMQ_DEFAULT_PASSWORD
    )

    logger.info(f"Connecting to RabbitMQ at {rabbitmq_host}:{rabbitmq_port}")

    try:
        rabbitmq_connection = await connect_robust(
            host=rabbitmq_host,
            port=rabbitmq_port,
            login=rabbitmq_user,
            password=rabbitmq_password,
        )
        rabbitmq_channel = await rabbitmq_connection.channel()

        # Declare durable queue with configuration
        queue = await rabbitmq_channel.declare_queue(
            QUEUE_NAME,
            durable=True,
            arguments={
                "x-message-ttl": QUEUE_TTL_MS,
            },
        )

        logger.info(f"RabbitMQ connected. Queue '{queue.name}' ready.")

        yield

    finally:
        # Shutdown: Close RabbitMQ connection
        if rabbitmq_channel:
            await rabbitmq_channel.close()
        if rabbitmq_connection:
            await rabbitmq_connection.close()
        logger.info("RabbitMQ connection closed.")


app = FastAPI(
    title="VideoAnalyzer Service",
    description="Extracts frames from videos and publishes to RabbitMQ",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "video_analyzer"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze video endpoint: Extract frames at specified FPS and publish.

    Extracts frames from the video at the specified rate and publishes each
    frame to RabbitMQ for downstream face detection processing.

    Args:
        request: AnalyzeRequest with file_path and fps (2 or 4)

    Returns:
        AnalyzeResponse with processing status

    Raises:
        HTTPException: 404 if file not found, 500 for processing errors
    """
    file_path = request.file_path
    target_fps = request.fps

    # Validate file exists
    if not os.path.exists(file_path):
        logger.error(f"Video file not found: {file_path}")
        raise HTTPException(
            status_code=404, detail=f"Video file not found: {file_path}"
        )

    # Generate video_id from filename
    video_id = os.path.basename(file_path)

    logger.info(f"Starting analysis for video: {video_id} with fps={target_fps}")

    try:
        # Open video with OpenCV
        video_capture = cv2.VideoCapture(file_path)

        if not video_capture.isOpened():
            raise HTTPException(
                status_code=500, detail=f"Failed to open video file: {file_path}"
            )

        # Get source video FPS
        source_fps = video_capture.get(cv2.CAP_PROP_FPS)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        if source_fps == 0:
            video_capture.release()
            raise HTTPException(
                status_code=500, detail="Unable to determine video FPS"
            )

        logger.info(f"Video metadata: source_fps={source_fps}, total_frames={total_frames}")

        # Calculate frame interval
        frame_interval = source_fps / target_fps

        frame_index = 0
        frames_extracted = 0
        current_position = 0.0

        while current_position < total_frames:
            # Calculate which frame to read
            target_frame_number = int(current_position)

            # Set video position to target frame
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame_number)

            # Read frame
            ret, frame = video_capture.read()

            if not ret:
                logger.warning(
                    f"Failed to read frame at position {target_frame_number}, "
                    f"stopping extraction"
                )
                break

            # Encode frame as JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
            _, buffer = cv2.imencode(".jpg", frame, encode_param)

            # Convert to base64
            frame_data_base64 = base64.b64encode(buffer).decode("utf-8")

            # Prepare message
            message_body = {
                "video_id": video_id,
                "frame_index": frame_index,
                "frame_data": frame_data_base64,
                "fps": target_fps,
            }

            # Publish to RabbitMQ
            message = Message(
                body=json.dumps(message_body).encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json",
            )

            await rabbitmq_channel.default_exchange.publish(
                message, routing_key=QUEUE_NAME
            )

            frames_extracted += 1
            frame_index += 1
            current_position += frame_interval

        video_capture.release()

        logger.info(f"Completed analysis: {frames_extracted} frames extracted and published")   

        return AnalyzeResponse(
            status="success",
            video_id=video_id,
            frames_processed=frames_extracted,
            message=f"Successfully extracted and published {frames_extracted} frames"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error processing video: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

