import asyncio

import httpx
import pytest
import pytest_asyncio
from aio_pika import connect_robust

# Track if services have been checked
_services_ready = False

# Constants
MAX_RETRIES = 30
RETRY_DELAY = 2
HEALTH_CHECK_TIMEOUT = 5.0
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
VIDEO_FILE_PATH = "/videos/G20_Summit.mp4"
API_TIMEOUT = 60.0

async def check_service(url: str, max_retries: int = 30, delay: int = 2) -> bool:
    """Check if a service is ready by polling its health endpoint."""
    for i in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=HEALTH_CHECK_TIMEOUT) as client:
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
def ensure_services_ready() -> None:
    """
    Ensure services are ready before any tests run.

    This fixture runs once per test session and verifies that both
    VideoAnalyzer and StreamDetector services are healthy before
    proceeding with tests.
    """
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
    """
    Provide RabbitMQ connection for tests.

    Yields:
        RabbitMQ connection object

    Cleanup:
        Closes connection after test
    """
    connection = await connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
    )

    yield connection

    await connection.close()


@pytest.fixture
def video_file_path() -> str:
    """
    Provide path to test video file.

    Returns:
        Path to G20_Summit.mp4 video file
    """
    return VIDEO_FILE_PATH


@pytest_asyncio.fixture
async def api_client():
    """
    Provide HTTP client for VideoAnalyzer API.

    Yields:
        Async HTTP client configured for VideoAnalyzer service
    """
    async with httpx.AsyncClient(
        base_url="http://localhost:8000", timeout=API_TIMEOUT
    ) as client:
        yield client


@pytest_asyncio.fixture
async def cleanup_queue(rabbitmq_connection):
    """
    Clean up RabbitMQ queue after each test.

    Purges the frame processing queue to prevent message accumulation
    between test runs.

    Args:
        rabbitmq_connection: RabbitMQ connection fixture
    """
    yield

    # Purge the queue after test
    try:
        channel = await rabbitmq_connection.channel()
        queue = await channel.get_queue("frame_processing_queue", ensure=False)
        await queue.purge()
        await channel.close()
    except Exception as e:
        print(f"Warning: Could not purge queue: {e}")


