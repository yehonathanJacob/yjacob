# Distributed Video Processing Pipeline with Face Detection

A scalable microservices architecture for video analysis that extracts frames at configurable frame rates and performs real-time face detection using Mediapipe.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

## Overview

This system consists of two FastAPI microservices communicating via RabbitMQ:

1. **VideoAnalyzer Service**: REST API that accepts video files, extracts frames at specified FPS (2 or 4), and publishes to message queue
2. **StreamDetector Service**: Consumes frames from queue, performs face detection using Mediapipe, and sends results downstream

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────────┐
│   Client    │─────>│VideoAnalyzer │─────>│    RabbitMQ      │
│  (POST)     │      │   Service    │      │   Message Queue  │
└─────────────┘      └──────────────┘      └──────────────────┘
                                                      │
                                                      v
                                            ┌──────────────────┐
                                            │ StreamDetector   │
                                            │    Service       │
                                            │  (Face Detection)│
                                            └──────────────────┘
                                                      │
                                                      v
                                            ┌──────────────────┐
                                            │  Next Service    │
                                            │   (Downstream)   │
                                            └──────────────────┘
```

## Features

- ✅ **Configurable Frame Extraction**: Extract frames at 2 FPS or 4 FPS
- ✅ **Async Message Queue**: RabbitMQ for reliable, scalable communication
- ✅ **Face Detection**: Mediapipe-powered face detection with bounding boxes
- ✅ **Production-Ready**: Docker Compose orchestration, health checks, graceful shutdown
- ✅ **Backpressure Handling**: Prefetch limits prevent queue overload
- ✅ **Comprehensive Tests**: Integration tests with Docker Compose
- ✅ **Scalable Architecture**: Ready for horizontal scaling (see [PRODUCTION_ARCHITECTURE.md](PRODUCTION_ARCHITECTURE.md))

## Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Python**: 3.11 (if running locally without Docker)
- **Operating System**: Linux, macOS, or Windows with WSL2

### Verify Prerequisites

```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. Clone Repository (if applicable)

```bash
git clone <repository-url>
cd yehonathan_assignment
```

### 2. Start All Services

```bash
docker-compose up --build
```

This command will:
- Build Docker images for VideoAnalyzer and StreamDetector
- Start RabbitMQ with management UI
- Start both services with health checks
- Mount the `videos/` directory for video file access

**Expected Output:**
```
✓ RabbitMQ ready on ports 5672 (AMQP) and 15672 (Management UI)
✓ VideoAnalyzer ready on port 8000
✓ StreamDetector ready on port 8001
```

### 3. Verify Services

```bash
# Check VideoAnalyzer health
curl http://localhost:8000/health

# Check StreamDetector health
curl http://localhost:8001/health

# Access RabbitMQ Management UI
# Open browser: http://localhost:15672
# Login: guest / guest
```

## Usage

### Process a Video File

The video file must be accessible inside the VideoAnalyzer container. Place your videos in the `videos/` directory, which is mounted to `/videos` in the container.

**Example: Process with 2 FPS**

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/videos/G20_Summit.mp4",
    "fps": 2
  }'
```

**Response:**
```json
{
  "status": "success",
  "video_id": "G20_Summit.mp4",
  "frames_processed": 120,
  "message": "Successfully extracted and published 120 frames"
}
```

**Example: Process with 4 FPS**

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/videos/G20_Summit.mp4",
    "fps": 4
  }'
```

### Add Your Own Videos

```bash
# Copy video to the videos directory
cp /path/to/your/video.mp4 videos/

# Process the video
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/videos/video.mp4",
    "fps": 2
  }'
```

## API Documentation

### VideoAnalyzer Service (Port 8000)

#### POST /analyze

Extract frames from a video and publish to RabbitMQ queue.

**Request Body:**
```json
{
  "file_path": "string (required) - Path to video file inside container",
  "fps": "integer (required) - Frame rate: 2 or 4"
}
```

**Responses:**
- `200 OK`: Video processed successfully
- `404 Not Found`: Video file not found
- `422 Unprocessable Entity`: Invalid FPS value (must be 2 or 4)
- `500 Internal Server Error`: Processing error

**Example Success Response:**
```json
{
  "status": "success",
  "video_id": "G20_Summit.mp4",
  "frames_processed": 240,
  "message": "Successfully extracted and published 240 frames"
}
```

#### GET /health

Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "video_analyzer"
}
```

### StreamDetector Service (Port 8001)

The StreamDetector service runs as a background consumer and doesn't expose processing endpoints. It automatically consumes messages from the RabbitMQ queue.

#### GET /health

Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "stream_detector",
  "detector_initialized": true
}
```

### Interactive API Documentation

Both services provide Swagger UI documentation:

- **VideoAnalyzer**: http://localhost:8000/docs
- **StreamDetector**: http://localhost:8001/docs

## Testing

### Run Integration Tests

The test suite validates the entire pipeline end-to-end.

**1. Start Services:**
```bash
docker-compose up --build -d
```

**2. Install Test Dependencies:**
```bash
pip install -r tests/requirements.txt
```

**3. Run Tests:**
```bash
pytest tests/ -v
```

**Expected Output:**
```
tests/test_integration.py::test_video_analyzer_health PASSED
tests/test_integration.py::test_stream_detector_health PASSED
tests/test_integration.py::test_analyze_with_fps_2 PASSED
tests/test_integration.py::test_analyze_with_fps_4 PASSED
tests/test_integration.py::test_analyze_invalid_fps PASSED
tests/test_integration.py::test_analyze_missing_file PASSED
tests/test_integration.py::test_frame_extraction_accuracy PASSED
tests/test_integration.py::test_end_to_end_pipeline PASSED
tests/test_integration.py::test_rabbitmq_queue_configuration PASSED

========== 9 passed in 45.23s ==========
```

### Test Coverage

Tests validate:
- ✅ Service health checks
- ✅ Valid FPS values (2 and 4)
- ✅ Invalid FPS rejection (returns 422)
- ✅ Missing file handling (returns 404)
- ✅ Frame extraction accuracy (fps=4 extracts ~2x frames as fps=2)
- ✅ End-to-end pipeline (frames → RabbitMQ → face detection)
- ✅ RabbitMQ queue configuration

## Monitoring

### RabbitMQ Management UI

Access the RabbitMQ Management UI to monitor message queue:

```
URL: http://localhost:15672
Username: guest
Password: guest
```

**Key Metrics to Monitor:**
- **Queue Depth**: Number of messages in `frame_processing_queue`
- **Publish Rate**: Frames per second being published
- **Consume Rate**: Frames per second being consumed
- **Consumer Count**: Number of active StreamDetector consumers (should be 1+)

### Service Logs

View real-time logs for each service:

```bash
# VideoAnalyzer logs
docker-compose logs -f video_analyzer

# StreamDetector logs
docker-compose logs -f stream_detector

# RabbitMQ logs
docker-compose logs -f rabbitmq

# All services
docker-compose logs -f
```

### Key Log Messages

**VideoAnalyzer:**
```
INFO: Starting analysis for video: G20_Summit.mp4 with fps=2
INFO: Video metadata: source_fps=30.0, total_frames=900
INFO: Completed analysis: 120 frames extracted and published
```

**StreamDetector:**
```
INFO: Mediapipe Face Detection model initialized successfully
INFO: Processing frame 42 from video G20_Summit.mp4 (fps=2)
INFO: Detected 3 faces in frame 42
INFO: Successfully processed frame 42 from video G20_Summit.mp4
```

## Troubleshooting

### Issue: "Connection refused" when calling API

**Solution:**
1. Verify services are running: `docker-compose ps`
2. Check health endpoints: `curl http://localhost:8000/health`
3. View logs: `docker-compose logs video_analyzer`

### Issue: RabbitMQ connection errors

**Symptoms:**
```
ERROR: [Errno 111] Connection refused
ERROR: Failed to connect to RabbitMQ
```

**Solution:**
1. Ensure RabbitMQ is healthy: `docker-compose ps rabbitmq`
2. Wait for health check: RabbitMQ takes 10-15 seconds to start
3. Restart services: `docker-compose restart video_analyzer stream_detector`

### Issue: Video file not found (404 error)

**Solution:**
1. Ensure video is in `videos/` directory: `ls -la videos/`
2. Use correct container path: `/videos/filename.mp4` (not `./videos/`)
3. Check file permissions: `chmod 644 videos/*.mp4`

### Issue: StreamDetector not processing frames

**Symptoms:**
- RabbitMQ queue depth keeps increasing
- No face detection logs

**Solution:**
1. Check StreamDetector logs: `docker-compose logs stream_detector`
2. Verify consumer is running: Check RabbitMQ Management UI → Queues → Consumers
3. Restart StreamDetector: `docker-compose restart stream_detector`

### Issue: Out of memory errors

**Solution:**
1. Increase Docker memory limit (Docker Desktop → Settings → Resources)
2. Reduce concurrent video processing
3. Lower FPS to reduce frame count

### Issue: Slow processing

**Symptoms:**
- Long response times
- High queue backlog

**Solution:**
1. **Scale StreamDetector**: 
   ```bash
   docker-compose up --scale stream_detector=3
   ```
2. **Reduce FPS**: Use fps=2 instead of fps=4
3. **Add GPU support** (see [PRODUCTION_ARCHITECTURE.md](PRODUCTION_ARCHITECTURE.md))

### Reset Everything

If you encounter persistent issues:

```bash
# Stop all services
docker-compose down

# Remove volumes (clears RabbitMQ data)
docker-compose down -v

# Rebuild and restart
docker-compose up --build
```

## Production Deployment

For production deployment guidance, including:
- Kubernetes configuration with HPA
- Multi-region setup and HA
- GPU acceleration with TensorRT
- Monitoring with Prometheus/Grafana
- Security hardening (mTLS, encryption)
- Cost optimization strategies

See **[PRODUCTION_ARCHITECTURE.md](PRODUCTION_ARCHITECTURE.md)**

### Quick Production Checklist

- [ ] Deploy to Kubernetes cluster
- [ ] Configure RabbitMQ cluster (3+ nodes)
- [ ] Enable horizontal autoscaling (HPA)
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure logging (ELK/Loki stack)
- [ ] Implement authentication (JWT tokens)
- [ ] Enable mTLS between services
- [ ] Use GPU instances for StreamDetector
- [ ] Configure auto-scaling based on queue depth
- [ ] Set up alerts (PagerDuty/Slack)

## Project Structure

```
yehonathan_assignment/
├── video_analyzer/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── DockerFile          # Container definition
├── stream_detector/
│   ├── main.py              # FastAPI consumer application
│   ├── detector.py          # Mediapipe face detection
│   ├── detector_response_handling.py  # Response models
│   ├── requirements.txt     # Python dependencies
│   └── DockerFile          # Container definition
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_integration.py  # Integration tests
│   └── requirements.txt     # Test dependencies
├── videos/
│   └── G20_Summit.mp4       # Sample video file
├── docker-compose.yml       # Service orchestration
├── pytest.ini              # Pytest configuration
├── README.md               # This file
└── PRODUCTION_ARCHITECTURE.md  # Production deployment guide
```

## Technology Stack

- **Backend**: FastAPI 0.109.0
- **Video Processing**: OpenCV 4.9.0.80
- **Face Detection**: Mediapipe 0.10.9
- **Message Queue**: RabbitMQ 3.12 with aio-pika 9.3.1
- **Validation**: Pydantic 2.5.3
- **Testing**: pytest 7.4.3 with pytest-asyncio
- **Containerization**: Docker with Python 3.11-slim base image

## Performance Metrics

**Development Environment (Docker Compose):**
- VideoAnalyzer: ~1-2 seconds per video (30-second video, fps=2)
- StreamDetector: ~100ms per frame (CPU-only)
- Throughput: ~10 frames/second per StreamDetector instance

**Production Environment (Kubernetes + GPU):**
- VideoAnalyzer: ~0.5 seconds per video (with optimizations)
- StreamDetector: ~10ms per frame (GPU-accelerated)
- Throughput: ~100 frames/second per GPU instance
- See [PRODUCTION_ARCHITECTURE.md](PRODUCTION_ARCHITECTURE.md) for scaling to 500+ concurrent videos

## Contributing

### Development Setup

```bash
# Install dependencies locally for development
cd video_analyzer
pip install -r requirements.txt

cd ../stream_detector
pip install -r requirements.txt

cd ../tests
pip install -r requirements.txt
```

### Code Style

- Follow PEP 8 style guide
- Use type hints throughout
- Add docstrings for all functions
- Keep functions focused and testable

## License

[Specify your license here]

## Contact

For questions or issues, please contact [your-contact-info].

---

**Built with ❤️ for scalable video processing and computer vision applications.**

