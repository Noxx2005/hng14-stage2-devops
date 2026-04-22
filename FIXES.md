# FIXES.md

This document lists all bugs found and fixed in the application.

## api/main.py

| Line | Problem | Fix |
|------|---------|-----|
| 8 | Hardcoded Redis host "localhost" - will fail in containerized environment | Changed to use environment variable `REDIS_HOST` with fallback to "localhost" |
| 8 | Hardcoded Redis port 6379 - not configurable | Changed to use environment variable `REDIS_PORT` with fallback to 6379 |
| 8 | Missing `decode_responses=True` - causes bytes/string handling issues | Added `decode_responses=True` to Redis connection |
| 13 | Hardcoded queue name "job" - not configurable | Changed to use environment variable `QUEUE_NAME` with fallback to "job" |
| 21 | Returns error response without proper HTTP status code | Changed to raise HTTPException with 404 status |
| 22 | Status decoding was inconsistent (line 22 decoded, line 21 didn't) | Fixed by using `decode_responses=True` on Redis connection |
| Entire file | Missing healthcheck endpoint for container orchestration | Added `/health` endpoint that checks Redis connectivity |
| Entire file | No error handling for Redis connection failures | Added try-except blocks with proper error logging and HTTP status codes |
| Entire file | No graceful shutdown handling | Added signal handlers for SIGTERM and SIGINT |
| Entire file | No logging for debugging and monitoring | Added comprehensive logging with timestamps and log levels |

## api/requirements.txt

| Line | Problem | Fix |
|------|---------|-----|
| 1-3 | Missing version pinning - causes unreproducible builds | Pinned all dependencies to specific versions |
| Entire file | Missing pydantic dependency (required by FastAPI) | Added `pydantic==2.5.0` |

## frontend/app.js

| Line | Problem | Fix |
|------|---------|-----|
| 6 | Hardcoded API URL "http://localhost:8000" - will fail in containerized environment | Changed to use environment variable `API_URL` with fallback |
| 29 | Hardcoded port 3000 - not configurable | Changed to use environment variable `PORT` with fallback to 3000 |
| Entire file | No healthcheck endpoint for container orchestration | Added `/health` endpoint |
| 16-17 | Generic error message without propagating actual error details | Enhanced error handling to propagate API error responses |
| 20-26 | Generic error message without propagating actual error details | Enhanced error handling to propagate API error responses |
| 29 | Server not stored in variable for graceful shutdown | Stored server in variable for graceful shutdown |
| Entire file | No graceful shutdown handling | Added graceful shutdown with SIGTERM/SIGINT handlers and 10s timeout |

## frontend/package.json

| Line | Problem | Fix |
|------|---------|-----|
| 9-10 | Using caret (^) for versions - causes unpredictable updates | Pinned exact versions for reproducibility |

## frontend/views/index.html

| Line | Problem | Fix |
|------|---------|-----|
| 24-28 | No error handling for failed job submission | Added try-except with error display |
| 31-37 | No error handling for failed status polling | Added try-except with error display |
| 35 | Will poll indefinitely on "not found" errors | Added check to stop polling on 404/not found errors |
| 35-37 | No timeout on polling - could run forever | Added 5-minute timeout to prevent infinite polling |
| 35 | Polling doesn't track start time for timeout | Added startTime parameter to track polling duration |
| 57 | No check for undefined status before polling | Added check `if (data.status)` before polling |

## worker/worker.py

| Line | Problem | Fix |
|------|---------|-----|
| 6 | Hardcoded Redis host "localhost" - will fail in containerized environment | Changed to use environment variable `REDIS_HOST` with fallback to "localhost" |
| 6 | Hardcoded Redis port 6379 - not configurable | Changed to use environment variable `REDIS_PORT` with fallback to 6379 |
| 6 | Missing `decode_responses=True` - causes bytes/string handling issues | Added `decode_responses=True` to Redis connection |
| 15 | Hardcoded queue name "job" - not configurable | Changed to use environment variable `QUEUE_NAME` with fallback to "job" |
| 18 | Job ID decode() call needed due to bytes from Redis | Fixed by using `decode_responses=True` on Redis connection |
| 4 | Signal module imported but never used | Implemented actual signal handlers for SIGTERM and SIGINT |
| 14-18 | No error handling for job processing | Added try-except around process_job with error logging |
| 14-18 | Infinite loop without graceful shutdown mechanism | Added `running` flag controlled by signal handlers |
| Entire file | No Redis connection error handling | Added try-except around brpop with retry logic |
| Entire file | No logging for debugging and monitoring | Added comprehensive logging with timestamps and log levels |

## worker/requirements.txt

| Line | Problem | Fix |
|------|---------|-----|
| 1 | Missing version pinning - causes unreproducible builds | Pinned redis to specific version `5.0.1` |
