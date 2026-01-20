# Production Architecture for Distributed Video Processing Pipeline

## Overview

This document outlines the production-ready architecture for scaling the distributed video processing pipeline to handle hundreds of concurrent videos with high availability, fault tolerance, and optimal performance.

## 1. Horizontal Scaling Strategy

### Kubernetes Deployment

**Architecture:**
- Deploy all services to Kubernetes (K8s) cluster for orchestration
- Separate deployments for VideoAnalyzer, StreamDetector, and RabbitMQ
- Use Kubernetes namespaces for environment isolation (dev, staging, prod)

**VideoAnalyzer Service Scaling:**
```yaml
# VideoAnalyzer Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: video-analyzer
spec:
  replicas: 5  # Start with 5, auto-scale based on load
  selector:
    matchLabels:
      app: video-analyzer
  template:
    spec:
      containers:
      - name: video-analyzer
        image: video-analyzer:latest
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
```

**StreamDetector Service Scaling:**
```yaml
# StreamDetector Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stream-detector
spec:
  replicas: 10  # More workers for CPU-intensive face detection
  selector:
    matchLabels:
      app: stream-detector
  template:
    spec:
      containers:
      - name: stream-detector
        image: stream-detector:latest
        resources:
          requests:
            cpu: 2000m      # Face detection is CPU-intensive
            memory: 4Gi
          limits:
            cpu: 4000m
            memory: 8Gi
```

**Horizontal Pod Autoscaler (HPA):**
```yaml
# VideoAnalyzer HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: video-analyzer-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: video-analyzer
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"

# StreamDetector HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: stream-detector-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: stream-detector
  minReplicas: 10
  maxReplicas: 100
  metrics:
  - type: External
    external:
      metric:
        name: rabbitmq_queue_depth
      target:
        type: AverageValue
        averageValue: "1000"  # Scale when queue depth > 1000 per pod
```

**Load Balancing:**
- Kubernetes Service with LoadBalancer type for VideoAnalyzer
- Ingress controller (NGINX or Traefik) for external API access
- Internal ClusterIP services for inter-service communication
- Session affinity: None (stateless services)

**RabbitMQ Cluster:**
- Deploy RabbitMQ as StatefulSet with 3-5 nodes
- Use RabbitMQ Cluster Operator for automated management
- Enable mirrored queues across all nodes for HA
- Configure quorum queues for critical workloads

## 2. High Availability & Fault Tolerance

### Multi-Region Deployment

**Active-Active Configuration:**
- Deploy to multiple availability zones within a region (minimum 3 AZs)
- For disaster recovery, deploy to secondary region with active-passive setup
- Use global load balancer (AWS Route53, Google Cloud Load Balancing) for DNS failover
- Cross-region data replication for RabbitMQ and object storage

**Failure Scenarios & Recovery:**

**Service Pod Failure:**
- Kubernetes automatically restarts failed pods
- Readiness/liveness probes detect unhealthy containers
- Rolling updates with zero downtime (maxUnavailable: 0)

**RabbitMQ Node Failure:**
- Quorum queues ensure message durability across nodes
- Automatic failover to healthy nodes
- Client reconnection with exponential backoff

**Network Partition:**
- RabbitMQ partition handling: `pause_minority` mode
- Service mesh (Istio) for circuit breaking and retry policies

### Circuit Breakers & Retry Policies

**Exponential Backoff for RabbitMQ:**
```python
# In both services
connection = await connect_robust(
    host=rabbitmq_host,
    reconnect_interval=1,      # Start with 1 second
    fail_fast=False,
    connection_attempts=10,
)
```

**Circuit Breaker Pattern:**
- Implement using service mesh (Istio) or application-level (pybreaker library)
- Configuration: 5 failures in 10 seconds → open circuit for 30 seconds
- Half-open state: allow 1 request to test recovery

**Dead-Letter Queue (DLQ):**
```python
# Configure DLQ for failed messages
queue = await channel.declare_queue(
    "frame_processing_queue",
    durable=True,
    arguments={
        "x-message-ttl": 3600000,           # 1 hour TTL
        "x-dead-letter-exchange": "dlx",    # Dead-letter exchange
        "x-dead-letter-routing-key": "failed_frames",
        "x-max-retries": 3,                 # Retry 3 times before DLQ
    }
)
```

**Graceful Shutdown:**
- Handle SIGTERM for graceful pod termination
- Drain in-flight requests before shutdown (30-second grace period)
- Finish processing current RabbitMQ message before acknowledging

### Health Checks

**Kubernetes Probes:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2
```

## 3. Storage & State Management

### Object Storage (S3/GCS)

**Video File Storage:**
- Store videos in Amazon S3 or Google Cloud Storage
- Lifecycle policies: Transition to cold storage after 30 days
- Versioning enabled for data integrity
- Cross-region replication for disaster recovery

**Access Pattern:**
- VideoAnalyzer pulls videos directly from S3 using pre-signed URLs
- Use S3 Transfer Acceleration for faster uploads
- Enable CloudFront CDN for frequently accessed videos

### Caching Layer (Redis)

**Use Cases:**
- Cache video metadata (fps, duration, frame count)
- Cache face detection results for duplicate frame detection
- Session management for long-running processing jobs

**Redis Cluster Configuration:**
```yaml
# Redis cluster with 3 masters, 3 replicas
Master 1 (AZ-1) → Replica 1 (AZ-2)
Master 2 (AZ-2) → Replica 2 (AZ-3)
Master 3 (AZ-3) → Replica 3 (AZ-1)
```

**TTL Strategy:**
- Video metadata: 1 hour TTL
- Face detection cache: 24 hours TTL
- Eviction policy: `volatile-lru`

### Database (PostgreSQL)

**Job Tracking & Audit Logs:**
```sql
-- Jobs table
CREATE TABLE video_processing_jobs (
    job_id UUID PRIMARY KEY,
    video_id VARCHAR(255),
    status VARCHAR(50),  -- pending, processing, completed, failed
    fps INT,
    frames_total INT,
    frames_processed INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Audit log table
CREATE TABLE processing_audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    job_id UUID REFERENCES video_processing_jobs(job_id),
    event_type VARCHAR(50),  -- frame_extracted, face_detected, error
    frame_index INT,
    details JSONB,
    timestamp TIMESTAMP
);
```

**PostgreSQL HA:**
- Primary-replica setup with streaming replication
- Automatic failover using Patroni or Stolon
- Connection pooling with PgBouncer (1000 connections)

### Video Preprocessing

**Chunking for Parallel Processing:**
- Split large videos into 5-minute chunks
- Process chunks in parallel across multiple VideoAnalyzer instances
- Use FFmpeg for fast video segmentation
- Merge results after processing

## 4. Monitoring & Observability

### Metrics (Prometheus)

**VideoAnalyzer Metrics:**
- `video_analyzer_requests_total` (counter)
- `video_analyzer_request_duration_seconds` (histogram)
- `video_analyzer_frames_extracted_total` (counter)
- `video_analyzer_errors_total` (counter by error type)

**StreamDetector Metrics:**
- `stream_detector_frames_processed_total` (counter)
- `stream_detector_faces_detected_total` (counter)
- `stream_detector_processing_duration_seconds` (histogram)
- `stream_detector_queue_lag_seconds` (gauge)

**RabbitMQ Metrics:**
- `rabbitmq_queue_depth` (gauge)
- `rabbitmq_message_publish_rate` (gauge)
- `rabbitmq_message_consume_rate` (gauge)
- `rabbitmq_queue_consumers` (gauge)

### Dashboards (Grafana)

**Operational Dashboard:**
- Real-time queue depth graph
- Processing rate: frames/second
- Latency percentiles (p50, p95, p99)
- Error rate by service
- Resource utilization: CPU, memory, network

**Business Metrics Dashboard:**
- Videos processed per hour
- Average processing time per video
- Face detection accuracy metrics
- Cost per video processed

### Distributed Tracing (OpenTelemetry)

**Trace Spans:**
1. `POST /analyze` request → VideoAnalyzer
2. Frame extraction → OpenCV processing
3. RabbitMQ publish → Message delivery
4. StreamDetector consume → Face detection
5. Send to next service → External API call

**Trace Context Propagation:**
- Inject trace ID in RabbitMQ message headers
- Correlate logs across services using trace ID
- Identify bottlenecks in processing pipeline

### Logging (ELK/Loki Stack)

**Structured Logging:**
```python
logger.info(
    "Frame processed",
    extra={
        "video_id": video_id,
        "frame_index": frame_index,
        "faces_detected": len(faces),
        "processing_time_ms": duration_ms,
        "trace_id": trace_id
    }
)
```

**Log Aggregation:**
- Elasticsearch for log storage and search
- Logstash/Fluentd for log collection
- Kibana for log visualization
- Retention: 30 days for production logs

### Alerting

**Critical Alerts (PagerDuty):**
- RabbitMQ queue depth > 50,000 (backpressure)
- StreamDetector processing lag > 5 minutes
- Error rate > 5% for 5 minutes
- Service pod crash loop

**Warning Alerts (Slack):**
- CPU utilization > 80% for 10 minutes
- Memory utilization > 85%
- Disk space < 20%
- Failed message rate increasing

## 5. Performance Optimizations

### GPU Acceleration

**TensorRT for Face Detection:**
- Convert Mediapipe model to TensorRT format
- Deploy StreamDetector pods to GPU-enabled nodes (NVIDIA T4 or A100)
- Batch multiple frames per inference (batch size: 16-32)
- Expected speedup: 5-10x over CPU

**Kubernetes GPU Scheduling:**
```yaml
resources:
  requests:
    nvidia.com/gpu: 1
  limits:
    nvidia.com/gpu: 1
nodeSelector:
  accelerator: nvidia-tesla-t4
```

### Batch Processing

**Frame Batching in RabbitMQ:**
- Instead of 1 message per frame, batch 10 frames per message
- Reduces RabbitMQ overhead by 90%
- StreamDetector processes batches in parallel

**Inference Batching:**
- Accumulate frames for 100ms before inference
- Process batch of 32 frames simultaneously on GPU
- Trade latency for throughput

### Connection Pooling

**RabbitMQ Connection Pool:**
```python
# Shared connection pool for VideoAnalyzer
connection_pool = ConnectionPool(
    max_connections=10,
    host=rabbitmq_host
)
```

**Database Connection Pool (PgBouncer):**
- Pool mode: transaction pooling
- Max connections per worker: 5
- Total pool size: 1000 connections

### Frame Preprocessing Pipeline

**Optimization Steps:**
1. Resize frames to 640x480 before sending (reduce message size by 60%)
2. Convert to grayscale for face detection (reduce processing by 30%)
3. Use JPEG compression quality 75 (balance size vs accuracy)
4. Implement frame deduplication for static video segments

### Async I/O Throughout

**Current Implementation:**
- Already using `asyncio` and `aio-pika`
- All I/O operations are non-blocking
- Efficient use of event loop

**Further Optimization:**
- Use `asyncio.gather()` for parallel operations
- Implement connection pooling for HTTP clients
- Use uvloop for faster event loop (2x speedup)

## 6. Security Considerations

### mTLS Between Services

**Service Mesh (Istio):**
- Automatic mTLS encryption for all service-to-service communication
- Certificate rotation every 24 hours
- Zero-trust network model

**Manual Implementation:**
```python
# RabbitMQ with TLS
connection = await connect_robust(
    host=rabbitmq_host,
    ssl=True,
    ssl_options={
        "cert_reqs": ssl.CERT_REQUIRED,
        "ca_certs": "/etc/certs/ca.crt",
        "certfile": "/etc/certs/client.crt",
        "keyfile": "/etc/certs/client.key"
    }
)
```

### Encryption at Rest

**Video Files:**
- S3 server-side encryption (SSE-KMS)
- Customer-managed keys in AWS KMS
- Rotate encryption keys annually

**Database:**
- PostgreSQL transparent data encryption (TDE)
- Encrypt backups with separate keys
- Encrypted EBS volumes for RabbitMQ data

### API Authentication (JWT Tokens)

**FastAPI JWT Authentication:**
```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    # Verify JWT with public key
    if not verify_jwt(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.post("/analyze", dependencies=[Depends(verify_token)])
async def analyze_video(request: AnalyzeRequest):
    # Protected endpoint
    pass
```

**API Gateway:**
- Use Kong or AWS API Gateway
- Rate limiting: 100 requests/minute per user
- IP whitelisting for internal services
- OAuth2/OIDC integration for user authentication

### Network Policies

**Kubernetes NetworkPolicies:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: video-analyzer-policy
spec:
  podSelector:
    matchLabels:
      app: video-analyzer
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: rabbitmq
    ports:
    - protocol: TCP
      port: 5672
```

### Secrets Management

**HashiCorp Vault:**
- Store RabbitMQ credentials, database passwords, API keys
- Dynamic secrets with short TTL (1 hour)
- Audit logging for secret access

**Kubernetes Secrets (Alternative):**
- Encrypt secrets at rest with KMS
- Use external-secrets operator to sync with Vault
- Inject secrets as environment variables or volume mounts

### Input Validation & Sanitization

**File Path Validation:**
```python
# Prevent path traversal attacks
def validate_file_path(file_path: str) -> str:
    # Ensure path is within allowed directory
    allowed_dir = "/videos"
    abs_path = os.path.abspath(file_path)
    if not abs_path.startswith(allowed_dir):
        raise HTTPException(status_code=400, detail="Invalid file path")
    return abs_path
```

**Message Validation:**
- Validate all RabbitMQ message schemas with Pydantic
- Reject malformed messages to DLQ
- Implement message size limits (10MB max)

## 7. Cost Optimization

### Spot Instances for Batch Workloads

**AWS Spot Instances:**
- Use Spot instances for StreamDetector workers (70% cost savings)
- Configure K8s cluster autoscaler with mixed instance types
- Implement graceful handling of Spot interruptions (2-minute warning)

**GCP Preemptible VMs:**
- Similar to Spot instances, 80% discount
- Max 24-hour runtime, plan for interruptions

### Auto-Scaling Based on Queue Depth

**KEDA (Kubernetes Event-Driven Autoscaling):**
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: stream-detector-scaler
spec:
  scaleTargetRef:
    name: stream-detector
  minReplicaCount: 5
  maxReplicaCount: 100
  triggers:
  - type: rabbitmq
    metadata:
      queueName: frame_processing_queue
      queueLength: "100"  # Scale up when queue length > 100 per pod
```

**Benefits:**
- Scale to zero during low traffic (VideoAnalyzer can scale to 1 replica)
- Scale up rapidly during peak hours
- Reduce costs by 60% during off-peak hours

### Video Archival Policies

**S3 Lifecycle Rules:**
- Standard storage: 7 days (frequent access)
- Infrequent Access (IA): 8-30 days (occasional access)
- Glacier: 31-90 days (archive)
- Glacier Deep Archive: >90 days (long-term retention)

**Cost Impact:**
- Glacier: 90% cheaper than Standard
- Delete processed videos after retention period
- Compress videos before archival (H.265 codec)

### Model Optimization

**Model Quantization:**
- Convert Mediapipe model from FP32 to INT8 (4x smaller)
- Minimal accuracy loss (<2%)
- 2-3x faster inference

**Model Pruning:**
- Remove redundant neurons from neural network
- Reduce model size by 40%
- Maintain 95%+ accuracy

**Edge Deployment (Future):**
- Deploy lightweight models to edge devices
- Reduce cloud processing costs by 80%
- Process videos locally, send only detection results

### Resource Right-Sizing

**Regular Analysis:**
- Use Kubernetes Vertical Pod Autoscaler (VPA) for recommendations
- Analyze Prometheus metrics for actual resource usage
- Adjust resource requests/limits quarterly

**Example Findings:**
- VideoAnalyzer: Reduce memory request from 2Gi to 1.5Gi (25% savings)
- StreamDetector: Increase CPU but reduce memory (optimize for workload)

### Reserved Capacity

**Reserved Instances/Committed Use Discounts:**
- Reserve baseline capacity for 1-3 years (40-60% discount)
- Use Spot/Preemptible for burst capacity
- Example: Reserve 20 nodes, burst to 100 with Spot

**RabbitMQ:**
- Use managed service (AWS MQ, Google Cloud Pub/Sub) for predictable pricing
- Alternatively, self-managed RabbitMQ on reserved capacity

## Architecture Diagrams (Textual)

### Kubernetes Production Architecture

```
                            [Global Load Balancer]
                                     |
                                     v
                    [Ingress Controller (NGINX)]
                                     |
              +----------------------+----------------------+
              |                                             |
              v                                             v
    [VideoAnalyzer Service]                       [API Gateway (Kong)]
    - HPA: 5-50 replicas                          - Authentication
    - CPU: 1-2 cores                              - Rate limiting
    - Memory: 2-4Gi                               - Logging
              |                                             |
              v                                             v
    [RabbitMQ Cluster]                            [VideoAnalyzer Service]
    - 3-5 nodes (StatefulSet)                            |
    - Quorum queues                                      v
    - Mirrored across AZs                    [RabbitMQ Cluster]
              |                                             |
              v                                             v
    [StreamDetector Service]                  [StreamDetector Service]
    - HPA: 10-100 replicas                    - GPU-enabled nodes (optional)
    - CPU: 2-4 cores                          - Batch processing
    - Memory: 4-8Gi                           - TensorRT inference
    - GPU: 1x T4 (optional)
              |
              v
    [Next Service / Results Storage]

    Supporting Infrastructure:
    - [PostgreSQL Primary + Replica]  (Job tracking, audit logs)
    - [Redis Cluster]                 (Caching, session management)
    - [S3/GCS]                        (Video storage)
    - [Prometheus + Grafana]          (Monitoring)
    - [ELK/Loki Stack]                (Logging)
    - [HashiCorp Vault]               (Secrets management)
```

### Data Flow with Scaling

```
1. Client → API Gateway → VideoAnalyzer (Load Balanced)
   - 50 concurrent VideoAnalyzer replicas handle 1000 videos simultaneously

2. VideoAnalyzer → RabbitMQ Cluster
   - Extract frames: 2 fps = 120 frames/min, 4 fps = 240 frames/min
   - 1000 videos × 240 frames/min = 240,000 frames/min to queue

3. RabbitMQ → StreamDetector (Horizontally Scaled)
   - 100 StreamDetector workers consume from queue
   - Each worker: 10 frames/sec = 100 workers × 10 = 1000 frames/sec
   - Process 60,000 frames/min (can handle 250 concurrent 4fps videos)

4. StreamDetector → Next Service
   - Send face detection results (RespObject) downstream
   - Async, non-blocking
```

### Failure Recovery Flow

```
Scenario: RabbitMQ Node Failure

1. Node 2 (of 3) crashes
2. Kubernetes detects pod failure (liveness probe)
3. Quorum queue automatically fails over to Node 1 & 3
4. Messages remain durable (not lost)
5. Kubernetes schedules new pod for Node 2
6. New pod joins cluster and syncs data
7. Recovery time: < 30 seconds
8. Alert sent to operations team

Scenario: StreamDetector Pod Crash During Processing

1. Pod crashes mid-frame processing
2. RabbitMQ detects connection loss
3. Unacknowledged messages requeued automatically
4. Another StreamDetector worker picks up message
5. Frame is reprocessed (idempotent operation)
6. No data loss, slight latency increase
```

## Scaling to Hundreds of Concurrent Videos

### Capacity Planning

**Target: 500 Concurrent Videos**

**VideoAnalyzer:**
- Assume 30-second video processing time per video
- 500 concurrent = 500 videos every 30 seconds = 1000 videos/minute
- Require 50 VideoAnalyzer replicas (10 videos per replica)

**RabbitMQ:**
- 500 videos × 4 fps × 30 sec avg duration = 60,000 frames in flight
- RabbitMQ can handle 1M+ messages, no issue

**StreamDetector:**
- Assume 100ms per frame processing (with GPU)
- 60,000 frames / 100 workers = 600 frames per worker = 60 seconds backlog
- Add 50% buffer → 150 StreamDetector replicas with GPU

**Cost Estimate (AWS):**
- VideoAnalyzer: 50 × c5.xlarge = 50 × $0.17/hr = $8.50/hr
- StreamDetector: 150 × g4dn.xlarge (GPU) = 150 × $0.526/hr = $78.90/hr
- RabbitMQ: 3 × m5.large = 3 × $0.096/hr = $0.29/hr
- Total: ~$88/hr = $2,112/day for 500 concurrent videos

**With Spot Instances (70% discount on StreamDetector):**
- StreamDetector: 150 × $0.158/hr (Spot) = $23.70/hr
- Total: ~$33/hr = $792/day (63% cost reduction)

## Conclusion

This production architecture provides:
- **Scalability:** Handle 500+ concurrent videos with auto-scaling
- **High Availability:** Multi-AZ deployment, automatic failover, 99.99% uptime
- **Performance:** GPU acceleration, batch processing, <100ms latency per frame
- **Security:** mTLS, encryption at rest/in transit, JWT authentication, network policies
- **Observability:** Comprehensive metrics, distributed tracing, structured logging, alerting
- **Cost Efficiency:** Spot instances, auto-scaling, archival policies, 63% cost reduction

The system is production-ready for the Stage 2 interview discussion and can be deployed to AWS, GCP, or Azure with minimal modifications.

