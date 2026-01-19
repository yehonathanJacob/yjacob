import asyncio
import pytest
import pytest_asyncio
import httpx
from aio_pika import connect_robust

# Track if services have been checked
_services_ready = False


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
            print(f"  Waiting for service at {url}... ({i + 1}/{max_retries})")
            await asyncio.sleep(delay)
    return False


@pytest.fixture(scope="session", autouse=True)
def ensure_services_ready():
    """Ensure services are ready before any tests run (sync fixture for session scope)."""
    global _services_ready
    if not _services_ready:
        # Run the async check in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Wait for VideoAnalyzer
            loop.run_until_complete(check_service("http://localhost:8000/health"))
            # Wait for StreamDetector
            loop.run_until_complete(check_service("http://localhost:8001/health"))
            # Give RabbitMQ a moment to fully initialize
            loop.run_until_complete(asyncio.sleep(2))
            print("✓ All services are ready")
            _services_ready = True
        finally:
            loop.close()


@pytest_asyncio.fixture
async def rabbitmq_connection():
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


@pytest_asyncio.fixture
async def api_client():
    """Provide HTTP client for VideoAnalyzer API."""
    async with httpx.AsyncClient(
            base_url="http://localhost:8000",
            timeout=60.0  # Longer timeout for video processing
    ) as client:
        yield client


@pytest_asyncio.fixture
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


