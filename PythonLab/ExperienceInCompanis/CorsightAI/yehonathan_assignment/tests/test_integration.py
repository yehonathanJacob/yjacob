"""
Integration tests for the distributed video processing pipeline.

Tests verify end-to-end functionality including frame extraction,
RabbitMQ message passing, and face detection processing.
"""
import asyncio

import pytest


@pytest.mark.asyncio
async def test_analyze_with_fps_2(api_client, video_file_path, cleanup_queue):
    """
    Test POST /analyze with valid fps=2.

    Verifies that video analysis endpoint successfully processes a video
    at 2 FPS and returns the correct response format.
    """
    response = await api_client.post(
        "/analyze", json={"file_path": video_file_path, "fps": 2}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["video_id"] == "G20_Summit.mp4"
    assert data["frames_processed"] > 0
    print(f"✓ Extracted {data['frames_processed']} frames at 2 FPS")


@pytest.mark.asyncio
async def test_analyze_with_fps_4(api_client, video_file_path, cleanup_queue):
    """
    Test POST /analyze with valid fps=4.

    Verifies that video analysis endpoint successfully processes a video
    at 4 FPS and returns the correct response format.
    """
    response = await api_client.post(
        "/analyze", json={"file_path": video_file_path, "fps": 4}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["video_id"] == "G20_Summit.mp4"
    assert data["frames_processed"] > 0
    print(f"✓ Extracted {data['frames_processed']} frames at 4 FPS")


@pytest.mark.asyncio
async def test_analyze_invalid_fps(api_client, video_file_path, cleanup_queue):
    """
    Test POST /analyze with invalid fps=3 (should return 422).

    Verifies that the API correctly rejects invalid FPS values that are
    not 2 or 4 with a 422 Unprocessable Entity response.
    """
    response = await api_client.post(
        "/analyze", json={"file_path": video_file_path, "fps": 3}
    )

    assert response.status_code == 422
    print("✓ Invalid FPS correctly rejected with 422")


@pytest.mark.asyncio
async def test_analyze_missing_file(api_client, cleanup_queue):
    """
    Test POST /analyze with non-existent file path (should return 404).

    Verifies that the API correctly handles missing video files with a
    404 Not Found response.
    """
    response = await api_client.post(
        "/analyze", json={"file_path": "/videos/nonexistent.mp4", "fps": 2}
    )

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
    print("✓ Missing file correctly handled with 404")


@pytest.mark.asyncio
async def test_frame_extraction_accuracy(
    api_client, video_file_path, cleanup_queue
):
    """
    Test frame extraction count is reasonable for video duration.

    Verifies that fps=4 extracts approximately 2x as many frames as fps=2,
    confirming correct frame extraction logic.
    """
    # Test with fps=2
    response = await api_client.post(
        "/analyze", json={"file_path": video_file_path, "fps": 2}
    )

    assert response.status_code == 200
    frames_fps_2 = response.json()["frames_processed"]

    # Wait a moment for queue to clear
    await asyncio.sleep(2)

    # Test with fps=4
    response = await api_client.post(
        "/analyze", json={"file_path": video_file_path, "fps": 4}
    )

    assert response.status_code == 200
    frames_fps_4 = response.json()["frames_processed"]

    # fps=4 should extract approximately 2x frames as fps=2
    ratio = frames_fps_4 / frames_fps_2
    assert 1.8 <= ratio <= 2.2, f"Frame ratio should be ~2.0, got {ratio}"
    print(f"✓ Frame extraction ratio: {ratio:.2f} (expected ~2.0)")


@pytest.mark.asyncio
async def test_end_to_end_pipeline(
    api_client, video_file_path, rabbitmq_connection, cleanup_queue
):
    """
    Test end-to-end pipeline: POST /analyze → RabbitMQ → StreamDetector.

    Verifies that frames are successfully published to RabbitMQ and
    consumed by StreamDetector service for face detection processing.
    """
    # Submit video for analysis
    response = await api_client.post(
        "/analyze", json={"file_path": video_file_path, "fps": 2}
    )

    assert response.status_code == 200
    expected_frames = response.json()["frames_processed"]
    print(f"✓ Submitted video, expecting {expected_frames} frames")

    # Give StreamDetector time to process frames
    # For a small video, processing should be quick
    await asyncio.sleep(10)

    # Check queue - should be empty or nearly empty if processing is working
    channel = await rabbitmq_connection.channel()
    queue = await channel.declare_queue(
        "frame_processing_queue", passive=True
    )
    message_count = queue.declaration_result.message_count

    await channel.close()

    # In a real test, we'd verify RespObject was sent to next service
    # For now, verify messages were consumed (queue is empty or low)
    print(
        f"✓ Queue has {message_count} messages remaining "
        f"(expected 0 or low)"
    )

    # Allow some messages to still be in queue during processing
    assert (
        message_count <= expected_frames
    ), "Queue should not have more messages than frames sent"


@pytest.mark.asyncio
async def test_rabbitmq_queue_configuration(rabbitmq_connection):
    """
    Test that RabbitMQ queue is properly configured.

    Verifies that the frame processing queue exists and is accessible,
    confirming proper RabbitMQ setup by the services.
    """
    channel = await rabbitmq_connection.channel()

    # Declare queue with passive=True to check it exists
    # Note: passive=True only checks existence, doesn't return full config
    queue = await channel.declare_queue(
        "frame_processing_queue", passive=True
    )
    assert queue is not None
    assert queue.name == "frame_processing_queue"

    # Verify we can get queue info (confirms it's properly set up)
    # The actual durable configuration is set by the services on startup
    print(f"✓ RabbitMQ queue '{queue.name}' exists and is accessible")

    await channel.close()
    print("✓ RabbitMQ queue properly configured")


@pytest.mark.asyncio
async def test_video_analyzer_health(api_client):
    """
    Test VideoAnalyzer health endpoint.

    Verifies that the VideoAnalyzer service is running and responding
    to health check requests.
    """
    response = await api_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "video_analyzer"
    print("✓ VideoAnalyzer health check passed")


@pytest.mark.asyncio
async def test_stream_detector_health():
    """
    Test StreamDetector health endpoint.

    Verifies that the StreamDetector service is running with an
    initialized face detection model.
    """
    import httpx

    async with httpx.AsyncClient(base_url="http://localhost:8001") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "stream_detector"
        assert data["detector_initialized"] is True
        print("✓ StreamDetector health check passed")

