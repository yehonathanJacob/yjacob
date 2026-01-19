import asyncio
import pytest
import httpx
from aio_pika import connect_robust
from typing import AsyncGenerator


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def wait_for_services():
    """Wait for all services to be ready before running tests."""
    async def check_service(url: str, max_retries: int = 30, delay: int = 2):
        """Check if a service is ready by polling its health endpoint."""
        for i in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        print(f"✓ Service at {url} is ready")
                        return True
            except Exception as e:
                if i == max_retries - 1:
                    print(f"✗ Service at {url} failed to start: {e}")
                    raise
                print(f"  Waiting for service at {url}... ({i+1}/{max_retries})")
                await asyncio.sleep(delay)
        return False
    
    # Wait for VideoAnalyzer
    await check_service("http://localhost:8000/health")
    
    # Wait for StreamDetector
    await check_service("http://localhost:8001/health")
    
    # Give RabbitMQ a moment to fully initialize
    await asyncio.sleep(2)
    
    print("✓ All services are ready")


@pytest.fixture
async def rabbitmq_connection(wait_for_services):
    """Provide RabbitMQ connection for tests."""
    connection = await connect_robust(
        host="localhost",
        port=5672,
        login="guest",
        password="guest",
    )
    
    yield connection
    
    await connection.close()


@pytest.fixture
def video_file_path() -> str:
    """Provide path to test video file."""
    return "/videos/G20_Summit.mp4"


@pytest.fixture
async def api_client(wait_for_services) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide HTTP client for VideoAnalyzer API."""
    async with httpx.AsyncClient(
        base_url="http://localhost:8000",
        timeout=60.0  # Longer timeout for video processing
    ) as client:
        yield client


@pytest.fixture
async def cleanup_queue(rabbitmq_connection):
    """Clean up RabbitMQ queue after each test."""
    yield
    
    # Purge the queue after test
    try:
        channel = await rabbitmq_connection.channel()
        queue = await channel.get_queue("frame_processing_queue", ensure=False)
        await queue.purge()
        await channel.close()
    except Exception as e:
        print(f"Warning: Could not purge queue: {e}")

