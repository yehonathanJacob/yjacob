---
title: 'Distributed Video Processing Pipeline with Face Detection'
slug: 'distributed-video-processing-pipeline-face-detection'
created: '2026-01-19'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['FastAPI', 'Mediapipe', 'RabbitMQ', 'aio-pika', 'OpenCV', 'Docker', 'pytest', 'Pydantic', 'numpy']
files_to_modify: ['stream_detector/main.py', 'stream_detector/detector.py', 'stream_detector/requirements.txt', 'stream_detector/DockerFile', 'video_analyzer/main.py', 'video_analyzer/requirements.txt', 'video_analyzer/DockerFile', 'docker-compose.yml']
code_patterns: ['Clean slate implementation', 'Microservices with message queue', 'Async/await throughout', 'Pydantic models for validation', 'FastAPI lifespan events for initialization', 'RabbitMQ durable queues with prefetch']
test_patterns: ['pytest with Docker Compose', 'Integration tests end-to-end', 'Fixtures for RabbitMQ and video files', 'Test containers for services']
---

# Tech-Spec: Distributed Video Processing Pipeline with Face Detection

**Created:** 2026-01-19

## Overview

### Problem Statement

Build a scalable microservices architecture for video analysis that extracts frames at configurable frame rates (2fps or 4fps) and performs face detection on each frame. The system must handle backpressure, support parallel processing, and be production-ready for scaling to hundreds of concurrent videos.

### Solution

Two FastAPI microservices communicating via RabbitMQ message broker:

1. **VideoAnalyzer Service**: Exposes REST API endpoint `POST /analyze` that accepts video file path and fps parameter. Validates fps (must be 2 or 4), extracts frames using OpenCV based on source video fps, and publishes each frame to RabbitMQ queue.

2. **StreamDetector Service**: Consumes frames from RabbitMQ queue asynchronously, runs Mediapipe face detection on each frame, constructs RespObject with video_id, frame_number, and detected face bounding boxes, then passes to downstream service placeholder.

### Scope

**In Scope:**
- VideoAnalyzer POST /analyze endpoint with strict fps validation (2 or 4 only)
- Frame extraction logic that calculates correct frame intervals based on source video fps
- RabbitMQ message broker integration using aio-pika for async communication
- StreamDetector consumer service with Mediapipe face detection
- Face detection model initialization at application startup
- RespObject construction with video_id, frame_number, and bounding boxes
- Dockerfiles for both services
- Docker Compose orchestration including RabbitMQ
- Integration tests using Docker Compose environment
- Production scaling architecture document (Stage 2 interview prep)

**Out of Scope:**
- Actual external service integration (using provided placeholder function)
- Video file upload functionality (accepts local file paths only)
- Database persistence (unless required for state management)
- Authentication/authorization
- Frontend/UI
- Real-time streaming (batch processing model)

## Context for Development

### Codebase Patterns

**Project Structure:**
- **Clean Slate Implementation**: Boilerplate structure exists but no implementation
- **Microservices Architecture**: Two independent services with separate Dockerfiles
- **Message Queue Pattern**: Async producer-consumer model via RabbitMQ
- **Existing Boilerplate**:
  - `stream_detector/detector.py`: `StreamFaceDetector` class with `detect_faces(frame: np.ndarray) -> List[BoundingBox]`
  - `stream_detector/detector_response_handling.py`: `RespObject` and `send_results_next_service()` placeholder
  - Pydantic models: `BoundingBox(x, y, w, h)` and `RespObject(faces, video_id, frame_id)`

**Code Conventions to Follow:**
- Use async/await throughout (FastAPI + aio-pika)
- Pydantic models for request/response validation
- Keep existing `detect_faces()` signature but implement Mediapipe inside
- Initialize heavy resources (Mediapipe model) at app startup using FastAPI lifespan events
- Type hints throughout (already present in boilerplate)
- No shared filesystem - pass frame data via message queue (serialize as base64 or msgpack)

**Architecture Patterns:**
- **VideoAnalyzer**: REST API → Frame Extraction → RabbitMQ Publisher
- **StreamDetector**: RabbitMQ Consumer → Face Detection → Results Handler
- **Message Format**: `{video_id: str, frame_index: int, frame_data: bytes, fps: int}`
- **Queue Strategy**: Single durable queue with prefetch limit for backpressure control
- **Error Handling**: Retry logic for transient failures, dead-letter queue for permanent failures

### Files to Reference

| File | Purpose | Status |
| ---- | ------- | ------ |
| `stream_detector/detector.py` | `StreamFaceDetector` class - implement Mediapipe inside `detect_faces()` | Modify |
| `stream_detector/detector_response_handling.py` | `RespObject` model and `send_results_next_service()` placeholder | Use as-is |
| `stream_detector/main.py` | FastAPI app for StreamDetector consumer service | Create |
| `stream_detector/requirements.txt` | Python dependencies for StreamDetector | Create |
| `stream_detector/DockerFile` | Container definition for StreamDetector | Create |
| `video_analyzer/main.py` | FastAPI app with POST /analyze endpoint | Create |
| `video_analyzer/requirements.txt` | Python dependencies for VideoAnalyzer | Create |
| `video_analyzer/DockerFile` | Container definition for VideoAnalyzer | Create |
| `docker-compose.yml` | Orchestration: RabbitMQ + both services + volume mounts | Create |
| `tests/` | Integration tests using pytest + Docker Compose | Create |
| `videos/G20_Summit.mp4` | Sample video file for testing | Use |
| `PRODUCTION_ARCHITECTURE.md` | Stage 2 interview prep document | Create |

### Technical Decisions

**1. Message Queue Design:**
- **Choice**: RabbitMQ with aio-pika (async Python client)
- **Rationale**: Native async support for FastAPI, proven reliability, simple setup for interview scope
- **Queue Configuration**: 
  - Durable queue named `frame_processing_queue`
  - Prefetch count of 1 per consumer for backpressure
  - Message TTL: 1 hour (prevent queue buildup if consumer dies)
  - Dead-letter exchange for failed messages

**2. Frame Serialization:**
- **Choice**: Serialize frames as JPEG bytes + base64 encoding in JSON
- **Rationale**: Balance between size and simplicity; RabbitMQ handles binary well
- **Alternative Considered**: msgpack (more efficient but adds complexity)

**3. Face Detection Model:**
- **Choice**: Mediapipe Face Detection (short-range model)
- **Rationale**: Lightweight, production-ready, good accuracy for general use
- **Initialization**: Load model once at FastAPI app startup using `@asynccontextmanager` lifespan

**4. Video ID Generation:**
- **Choice**: Use filename as video_id (per assignment suggestion)
- **Rationale**: Simple, deterministic, sufficient for interview scope
- **Production Note**: Would use UUID or hash for real deployment

**5. Error Handling Strategy:**
- VideoAnalyzer: Return 422 for validation errors, 404 for missing files, 500 for processing errors
- StreamDetector: Log failed frames, send to dead-letter queue after 3 retries
- Both: Structured logging with correlation IDs

**6. Testing Approach:**
- Integration tests using pytest with Docker Compose
- Fixtures for RabbitMQ connection and test video files
- End-to-end validation: POST /analyze → verify messages in queue → verify detector processing
- Test cases: valid fps (2, 4), invalid fps, missing file, frame count validation

## Implementation Plan

### Tasks

**Phase 1: Infrastructure Setup**

- [ ] **Task 1: Create RabbitMQ configuration in docker-compose.yml**
  - File: `docker-compose.yml`
  - Action: Define RabbitMQ service with management plugin, expose ports 5672 (AMQP) and 15672 (management UI)
  - Configuration: Set default user/password, configure health check, define shared network
  - Notes: Use `rabbitmq:3.12-management` image

- [ ] **Task 2: Create VideoAnalyzer requirements.txt**
  - File: `video_analyzer/requirements.txt`
  - Action: List all dependencies with pinned versions (FastAPI, uvicorn, opencv-python, aio-pika, pydantic, python-multipart)
  - Notes: Use versions specified in Dependencies section

- [ ] **Task 3: Create StreamDetector requirements.txt**
  - File: `stream_detector/requirements.txt`
  - Action: List all dependencies with pinned versions (FastAPI, uvicorn, mediapipe, aio-pika, pydantic, numpy, opencv-python)
  - Notes: Use versions specified in Dependencies section

**Phase 2: VideoAnalyzer Service Implementation**

- [ ] **Task 4: Implement VideoAnalyzer FastAPI application**
  - File: `video_analyzer/main.py`
  - Action: Create FastAPI app with:
    - Pydantic request model `AnalyzeRequest(file_path: str, fps: Literal[2, 4])`
    - POST /analyze endpoint
    - Lifespan context manager for RabbitMQ connection setup/teardown
    - RabbitMQ publisher using aio-pika
  - Notes: Initialize connection to RabbitMQ at `rabbitmq:5672`, declare durable queue `frame_processing_queue`

- [ ] **Task 5: Implement frame extraction logic**
  - File: `video_analyzer/main.py`
  - Action: In POST /analyze handler:
    - Validate file exists (404 if not)
    - Open video with cv2.VideoCapture
    - Get source fps from video metadata
    - Calculate frame interval: `interval = source_fps / requested_fps`
    - Extract frames at calculated intervals
    - Serialize each frame as JPEG, encode as base64
    - Publish to RabbitMQ with message: `{video_id, frame_index, frame_data, fps}`
    - Return 200 OK only after all frames published
  - Notes: Use os.path.basename(file_path) as video_id, handle cv2 errors gracefully

- [ ] **Task 6: Create VideoAnalyzer Dockerfile**
  - File: `video_analyzer/DockerFile`
  - Action: Multi-stage build with:
    - Base: `python:3.11-slim`
    - Install system dependencies for OpenCV (libgl1-mesa-glx, libglib2.0-0)
    - COPY requirements.txt and pip install
    - COPY main.py
    - Expose port 8000
    - CMD: `uvicorn main:app --host 0.0.0.0 --port 8000`
  - Notes: Optimize layer caching, use --no-cache-dir for pip

- [ ] **Task 7: Add VideoAnalyzer to docker-compose.yml**
  - File: `docker-compose.yml`
  - Action: Define video_analyzer service:
    - Build from `./video_analyzer`
    - Expose port 8000
    - Mount `./videos` volume to `/videos` in container
    - Environment variables: RABBITMQ_HOST=rabbitmq
    - depends_on: rabbitmq (with health check condition)
  - Notes: Use shared network for service communication

**Phase 3: StreamDetector Service Implementation**

- [ ] **Task 8: Implement Mediapipe face detection in StreamFaceDetector**
  - File: `stream_detector/detector.py`
  - Action: Modify `StreamFaceDetector.__init__()`:
    - Import mediapipe as mp
    - Initialize `self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)`
  - Action: Modify `detect_faces(frame)`:
    - Convert frame from BGR to RGB
    - Process with `self.face_detection.process()`
    - Extract bounding boxes from detections
    - Convert to BoundingBox models (x, y, w, h in pixel coordinates)
    - Return List[BoundingBox]
  - Notes: Handle case when no faces detected (return empty list), ensure proper resource cleanup

- [ ] **Task 9: Implement StreamDetector FastAPI consumer application**
  - File: `stream_detector/main.py`
  - Action: Create FastAPI app with:
    - Lifespan context manager for RabbitMQ connection and Mediapipe initialization
    - Initialize `StreamFaceDetector` in lifespan startup
    - Background task or startup event that starts RabbitMQ consumer
    - Consumer callback that:
      - Deserializes message (video_id, frame_index, frame_data)
      - Decodes base64 frame_data to numpy array
      - Calls `detector.detect_faces(frame)`
      - Constructs `RespObject(video_id, frame_id=frame_index, faces=detected_faces)`
      - Calls `send_results_next_service([resp_object])`
      - Acknowledges message
  - Notes: Use prefetch_count=1 for backpressure, log processing progress

- [ ] **Task 10: Create StreamDetector Dockerfile**
  - File: `stream_detector/DockerFile`
  - Action: Multi-stage build with:
    - Base: `python:3.11-slim`
    - Install system dependencies for OpenCV and Mediapipe
    - COPY requirements.txt and pip install
    - COPY detector.py, detector_response_handling.py, main.py
    - Expose port 8001 (for health checks)
    - CMD: `uvicorn main:app --host 0.0.0.0 --port 8001`
  - Notes: Mediapipe downloads models on first use, consider caching

- [ ] **Task 11: Add StreamDetector to docker-compose.yml**
  - File: `docker-compose.yml`
  - Action: Define stream_detector service:
    - Build from `./stream_detector`
    - Expose port 8001
    - Environment variables: RABBITMQ_HOST=rabbitmq
    - depends_on: rabbitmq (with health check condition)
  - Notes: Use shared network, can scale with `docker-compose up --scale stream_detector=3`

**Phase 4: Testing Infrastructure**

- [ ] **Task 12: Create integration test structure**
  - File: `tests/conftest.py`
  - Action: Create pytest fixtures:
    - `rabbitmq_connection`: Async fixture that connects to RabbitMQ, yields connection, closes on teardown
    - `video_file_path`: Fixture returning path to test video (`/videos/G20_Summit.mp4`)
    - `api_client`: httpx.AsyncClient fixture pointing to VideoAnalyzer at `http://localhost:8000`
    - `wait_for_services`: Fixture that waits for both services to be ready before tests run
  - Notes: Use pytest-asyncio, add timeouts for service readiness

- [ ] **Task 13: Implement integration tests**
  - File: `tests/test_integration.py`
  - Action: Implement test cases:
    - `test_analyze_with_fps_2_and_4`: POST with valid fps, verify 200 response
    - `test_analyze_invalid_fps`: POST with fps=3, verify 422 response
    - `test_analyze_missing_file`: POST with non-existent path, verify 404 response
    - `test_frame_extraction_accuracy`: Verify frame count matches expected calculation
    - `test_end_to_end_pipeline`: POST /analyze, consume queue messages, verify RespObject structure with face detections
  - Notes: Use async test functions, add proper cleanup between tests

- [ ] **Task 14: Create test requirements and Docker Compose override**
  - File: `tests/requirements.txt`
  - Action: List test dependencies (pytest, pytest-asyncio, httpx, aio-pika)
  - File: `docker-compose.test.yml`
  - Action: Create override file that adds pytest container with network access to services
  - Notes: Mount test code and videos into test container

**Phase 5: Documentation**

- [ ] **Task 15: Create production architecture document**
  - File: `PRODUCTION_ARCHITECTURE.md`
  - Action: Document production scaling approach with sections:
    - Horizontal Scaling Strategy (K8s, HPA, load balancing)
    - High Availability & Fault Tolerance (multi-region, circuit breakers, DLQ)
    - Storage & State Management (S3, Redis, PostgreSQL)
    - Monitoring & Observability (Prometheus, Grafana, OpenTelemetry, logging)
    - Performance Optimizations (GPU, batching, connection pooling)
    - Security Considerations (mTLS, encryption, auth, secrets)
    - Cost Optimization (spot instances, auto-scaling, archival)
  - Notes: Include architecture diagrams (textual descriptions acceptable), reference scaling to hundreds of concurrent videos

- [ ] **Task 16: Create README with setup and run instructions**
  - File: `README.md`
  - Action: Document:
    - Project overview and architecture
    - Prerequisites (Docker, Docker Compose)
    - Setup instructions: `docker-compose up --build`
    - Usage: How to call POST /analyze endpoint with curl examples
    - Testing: How to run integration tests
    - RabbitMQ management UI access (http://localhost:15672)
    - Troubleshooting common issues
  - Notes: Include example API calls with fps=2 and fps=4

### Acceptance Criteria

**VideoAnalyzer Service:**

- [ ] **AC1**: Given a valid video file path and fps=2, when POST /analyze is called, then the endpoint returns 200 OK after all frames are extracted and published to RabbitMQ

- [ ] **AC2**: Given a valid video file path and fps=4, when POST /analyze is called, then the endpoint returns 200 OK after all frames are extracted and published to RabbitMQ

- [ ] **AC3**: Given a valid video file with source fps=30 and requested fps=2, when POST /analyze is called, then exactly every 15th frame is extracted (source_fps/requested_fps = 30/2 = 15)

- [ ] **AC4**: Given a valid video file with source fps=30 and requested fps=4, when POST /analyze is called, then frame extraction interval is calculated correctly (every 7-8th frame)

- [ ] **AC5**: Given fps parameter of 3 (invalid), when POST /analyze is called, then the endpoint returns 422 Unprocessable Entity with validation error message

- [ ] **AC6**: Given a non-existent video file path, when POST /analyze is called, then the endpoint returns 404 Not Found with clear error message

- [ ] **AC7**: Given successful frame extraction, when frames are published to RabbitMQ, then each message contains video_id (filename), frame_index, frame_data (base64), and fps

**StreamDetector Service:**

- [ ] **AC8**: Given the StreamDetector service starts, when initialization completes, then the Mediapipe face detection model is loaded and ready

- [ ] **AC9**: Given a frame message in the RabbitMQ queue, when StreamDetector consumes it, then face detection is performed and results are logged

- [ ] **AC10**: Given a frame with detected faces, when detection completes, then RespObject contains video_id, frame_id (frame_index), and List[BoundingBox] with correct x, y, w, h coordinates

- [ ] **AC11**: Given a frame with no faces detected, when detection completes, then RespObject contains video_id, frame_id, and empty faces list

- [ ] **AC12**: Given RespObject is constructed, when processing completes, then send_results_next_service() is called with the RespObject

- [ ] **AC13**: Given successful processing, when StreamDetector finishes with a message, then the RabbitMQ message is acknowledged (removed from queue)

**Infrastructure & Integration:**

- [ ] **AC14**: Given docker-compose up is executed, when all services start, then RabbitMQ, VideoAnalyzer, and StreamDetector are all healthy and reachable

- [ ] **AC15**: Given RabbitMQ management UI, when accessed at http://localhost:15672, then the frame_processing_queue is visible with correct configuration (durable, TTL)

- [ ] **AC16**: Given VideoAnalyzer publishes frames, when StreamDetector is not running, then messages accumulate in RabbitMQ queue without loss (backpressure handling)

- [ ] **AC17**: Given end-to-end pipeline execution, when POST /analyze completes and StreamDetector processes all frames, then total frames processed matches frames extracted

**Testing:**

- [ ] **AC18**: Given integration tests are executed, when test suite runs with docker-compose up, then all tests pass without manual intervention

- [ ] **AC19**: Given test_analyze_with_fps_2_and_4, when executed, then both fps=2 and fps=4 requests return 200 OK

- [ ] **AC20**: Given test_analyze_invalid_fps, when executed, then fps=3 request returns 422 error

- [ ] **AC21**: Given test_end_to_end_pipeline, when executed, then frames flow from VideoAnalyzer → RabbitMQ → StreamDetector with face detection results produced

**Documentation:**

- [ ] **AC22**: Given PRODUCTION_ARCHITECTURE.md exists, when reviewed, then all 7 sections are documented with specific technology choices and scaling strategies

- [ ] **AC23**: Given README.md exists, when followed by a new developer, then they can successfully run the system and execute test API calls without external help

## Additional Context

### Dependencies

**VideoAnalyzer Service (`video_analyzer/requirements.txt`):**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
opencv-python==4.9.0.80
aio-pika==9.3.1
pydantic==2.5.3
python-multipart==0.0.6
```

**StreamDetector Service (`stream_detector/requirements.txt`):**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
mediapipe==0.10.9
aio-pika==9.3.1
pydantic==2.5.3
numpy==1.24.3
opencv-python==4.9.0.80
```

**Test Dependencies (`tests/requirements.txt`):**
```
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.26.0
aio-pika==9.3.1
```

**Docker Base Images:**
- Both services: `python:3.11-slim` (balance size and compatibility)
- RabbitMQ: `rabbitmq:3.12-management` (includes web UI for debugging)

**Key Library Choices:**
- **aio-pika 9.3.1**: Latest stable async RabbitMQ client with excellent FastAPI integration
- **Mediapipe 0.10.9**: Latest stable release with face detection models
- **opencv-python**: Headless version sufficient for server-side processing
- **FastAPI 0.109.0**: Latest with native lifespan context manager support

### Testing Strategy

**Integration Tests using Docker Compose:**

**Test Environment:**
- Spin up all services via `docker-compose up` in test mode
- Wait for RabbitMQ health check and service readiness
- Use `httpx.AsyncClient` for API calls
- Connect to RabbitMQ to verify message flow

**Test Cases:**

1. **Happy Path - Valid FPS (2 and 4)**
   - Given: G20_Summit.mp4 video file exists
   - When: POST /analyze with fps=2 and fps=4
   - Then: 200 OK response, correct number of frames extracted and published to queue

2. **FPS Validation**
   - Given: Valid video file
   - When: POST /analyze with fps=3 (invalid)
   - Then: 422 Unprocessable Entity with validation error

3. **Missing File Handling**
   - Given: Non-existent video path
   - When: POST /analyze with valid fps
   - Then: 404 Not Found with clear error message

4. **Frame Extraction Accuracy**
   - Given: Video with known fps (e.g., 30fps)
   - When: POST /analyze with fps=2
   - Then: Verify correct frame interval calculation (every 15th frame)

5. **End-to-End Pipeline**
   - Given: Valid video and fps
   - When: POST /analyze completes
   - Then: StreamDetector consumes messages, detects faces, calls send_results_next_service()
   - Verify: RespObject contains video_id, frame_number, and bounding boxes

6. **Backpressure Handling** (Stretch Goal)
   - Given: StreamDetector processing delay
   - When: Multiple concurrent POST /analyze requests
   - Then: Messages queue up, no data loss, VideoAnalyzer completes successfully

**Test Fixtures:**
- `rabbitmq_connection`: Async fixture for RabbitMQ connection
- `video_file_path`: Fixture providing path to test video
- `api_client`: httpx.AsyncClient pointing to VideoAnalyzer service
- `detector_service`: Reference to StreamDetector for verification

**Test Utilities:**
- `wait_for_service(url, timeout=30)`: Wait for service health check
- `consume_queue_messages(queue_name, count)`: Helper to read messages for verification
- `mock_send_results()`: Capture calls to send_results_next_service() for assertions

### Notes

**Stage 2 Interview Prep - Production Architecture Document:**

Create `PRODUCTION_ARCHITECTURE.md` covering:

1. **Horizontal Scaling Strategy**
   - Kubernetes deployment with HPA (Horizontal Pod Autoscaler)
   - Multiple VideoAnalyzer replicas behind load balancer
   - Multiple StreamDetector consumer replicas (queue workers)
   - RabbitMQ cluster with mirrored queues

2. **High Availability & Fault Tolerance**
   - Multi-region deployment for disaster recovery
   - Circuit breakers and retry policies
   - Dead-letter queues with alerting
   - Health checks and readiness probes
   - Graceful shutdown handling

3. **Storage & State Management**
   - Object storage (S3/GCS) for video files
   - Redis for caching video metadata
   - PostgreSQL for job tracking and audit logs
   - Video preprocessing: chunking for parallel processing

4. **Monitoring & Observability**
   - Prometheus metrics: processing rate, queue depth, latency
   - Grafana dashboards for operational visibility
   - OpenTelemetry for distributed tracing
   - Structured logging with ELK/Loki stack
   - Alerts: queue buildup, service failures, high latency

5. **Performance Optimizations**
   - GPU acceleration for face detection (TensorRT)
   - Batch processing multiple frames per message
   - Connection pooling for RabbitMQ
   - Async I/O throughout
   - Frame preprocessing pipeline (resize, normalize)

6. **Security Considerations**
   - mTLS between services
   - Video file encryption at rest
   - API authentication (JWT tokens)
   - Network policies and service mesh
   - Secrets management (Vault/K8s secrets)

7. **Cost Optimization**
   - Spot instances for batch workloads
   - Auto-scaling based on queue depth
   - Video archival policies
   - Model optimization (quantization, pruning)

**Diagram Ideas:**
- Architecture diagram showing K8s deployment
- Data flow diagram with scaling dimensions
- Failure scenario diagrams with recovery paths

