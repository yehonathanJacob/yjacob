import os
import base64
import json
import logging
import asyncio
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import cv2
import numpy as np
from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from fastapi import FastAPI

from detector import StreamFaceDetector
from detector_response_handling import RespObject, send_results_next_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
rabbitmq_connection: Optional[AbstractRobustConnection] = None
rabbitmq_channel: Optional[AbstractChannel] = None
face_detector: Optional[StreamFaceDetector] = None
consumer_task: Optional[asyncio.Task] = None


async def process_frame_message(message: IncomingMessage) -> None:
    """
    Process incoming frame messages from RabbitMQ queue.

    Args:
        message: Incoming message containing frame data
    """
    async with message.process():
        try:
            # Parse message body
            message_data = json.loads(message.body.decode())
            
            video_id = message_data["video_id"]
            frame_index = message_data["frame_index"]
            frame_data_base64 = message_data["frame_data"]
            fps = message_data["fps"]
            
            logger.info(f"Processing frame {frame_index} from video {video_id} (fps={fps})")
            
            # Decode base64 frame data
            frame_bytes = base64.b64decode(frame_data_base64)
            frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            if frame is None:
                logger.error(f"Failed to decode frame {frame_index} from video {video_id}")
                return
            
            # Detect faces using Mediapipe
            detected_faces = face_detector.detect_faces(frame)
            
            logger.info(f"Detected {len(detected_faces)} faces in frame {frame_index}")
            
            # Construct RespObject
            resp_object = RespObject(
                video_id=video_id,
                frame_id=frame_index,
                faces=detected_faces
            )
            
            # Send results to next service (placeholder function)
            send_results_next_service([resp_object])
            
            logger.info(f"Successfully processed frame {frame_index} from video {video_id}")
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            # Re-raise to trigger message requeue or DLQ handling
            raise


async def start_consumer() -> None:
    """Start consuming messages from RabbitMQ queue."""
    global rabbitmq_channel
    
    try:
        # Get queue
        queue = await rabbitmq_channel.get_queue("frame_processing_queue")
        
        # Set prefetch count for backpressure control
        await rabbitmq_channel.set_qos(prefetch_count=1)
        
        logger.info("Starting to consume messages from frame_processing_queue")
        
        # Start consuming
        await queue.consume(process_frame_message)
        
    except Exception as e:
        logger.error(f"Error in consumer: {str(e)}", exc_info=True)
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app initialization and cleanup."""
    global rabbitmq_connection, rabbitmq_channel, face_detector, consumer_task
    
    # Startup: Initialize resources
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    rabbitmq_port = int(os.getenv("RABBITMQ_PORT", "5672"))
    
    logger.info(f"Connecting to RabbitMQ at {rabbitmq_host}:{rabbitmq_port}")
    
    try:
        # Initialize Mediapipe Face Detector
        logger.info("Initializing Mediapipe Face Detection model...")
        face_detector = StreamFaceDetector()
        logger.info("Mediapipe Face Detection model initialized successfully")
        
        # Connect to RabbitMQ
        rabbitmq_connection = await connect_robust(
            host=rabbitmq_host,
            port=rabbitmq_port,
            login="guest",
            password="guest",
        )
        rabbitmq_channel = await rabbitmq_connection.channel()
        
        # Declare queue (ensure it exists)
        queue = await rabbitmq_channel.declare_queue(
            "frame_processing_queue",
            durable=True,
            arguments={
                "x-message-ttl": 3600000,  # 1 hour TTL
            }
        )
        
        logger.info(f"RabbitMQ connected. Queue '{queue.name}' ready.")
        
        # Start consumer as background task
        consumer_task = asyncio.create_task(start_consumer())
        logger.info("Consumer task started")
        
        yield
        
    finally:
        # Shutdown: Clean up resources
        logger.info("Shutting down StreamDetector service...")
        
        if consumer_task:
            consumer_task.cancel()
            try:
                await consumer_task
            except asyncio.CancelledError:
                pass
        
        if rabbitmq_channel:
            await rabbitmq_channel.close()
        
        if rabbitmq_connection:
            await rabbitmq_connection.close()
        
        if face_detector:
            face_detector.close()
        
        logger.info("StreamDetector service shut down complete")


app = FastAPI(
    title="StreamDetector Service",
    description="Consumes frames from RabbitMQ and performs face detection",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "stream_detector",
        "detector_initialized": face_detector is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

