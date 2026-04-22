# HNG Stage 2 DevOps - Job Processing Microservices

A containerized job processing system with three services: a frontend (Node.js), an API (Python/FastAPI), and a worker (Python), all communicating through Redis.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Git

## Quick Start

1. Clone the repository:
```bash
git clone <your-fork-url>
cd hng14-stage2-devops
```

2. Copy the example environment file (optional for local testing with defaults):
```bash
cp .env.example .env
```

3. Build and start all services:
```bash
docker-compose up -d
```

4. Verify all services are healthy:
```bash
docker-compose ps
```

Expected output should show all services as "healthy":
```
NAME                             STATUS
hng14-stage2-devops-redis-1      Up X minutes (healthy)
hng14-stage2-devops-api-1        Up X minutes (healthy)
hng14-stage2-devops-worker-1     Up X minutes (healthy)
hng14-stage2-devops-frontend-1   Up X minutes (healthy)
```

5. Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Health Check: http://localhost:8000/health

## Testing the Application

### Submit a Job
```bash
curl -X POST http://localhost:3000/submit
```

Response:
```json
{"job_id": "<uuid>"}
```

### Check Job Status
```bash
curl http://localhost:3000/status/<job_id>
```

Response:
```json
{"job_id": "<uuid>", "status": "completed"}
```

## Stopping the Application

```bash
docker-compose down
```

To also remove volumes:
```bash
docker-compose down -v
```

## Architecture

- **Frontend**: Node.js/Express server serving static HTML and proxying API requests
- **API**: Python/FastAPI service for job creation and status retrieval
- **Worker**: Python service that processes jobs from Redis queue
- **Redis**: In-memory data store for job queue and status

## Configuration

All configuration is done via environment variables. See `.env.example` for available options:

- `REDIS_HOST`: Redis server hostname (default: redis)
- `REDIS_PORT`: Redis server port (default: 6379)
- `QUEUE_NAME`: Name of the job queue (default: job)
- `API_URL`: API endpoint URL for frontend (default: http://api:8000)
- `PORT`: Frontend server port (default: 3000)

## Development

### Running Individual Services

API:
```bash
cd api
docker build -t my-api .
docker run -p 8000:8000 -e REDIS_HOST=host.docker.internal my-api
```

Worker:
```bash
cd worker
docker build -t my-worker .
docker run -e REDIS_HOST=host.docker.internal my-worker
```

Frontend:
```bash
cd frontend
docker build -t my-frontend .
docker run -p 3000:3000 -e API_URL=http://host.docker.internal:8000 my-frontend
```

## Health Checks

Each service includes a healthcheck endpoint:
- API: `GET /health`
- Frontend: `GET /health`
- Worker: Checks Redis connectivity
- Redis: `redis-cli ping`

## Resource Limits

Each service has the following resource limits in docker-compose:
- CPU: 0.5 cores
- Memory: 256MB

## Security

- All services run as non-root users
- No secrets or credentials are copied into images
- Redis is not exposed on the host machine (internal network only)
- Environment variables are used for all configuration
