from fastapi import FastAPI, HTTPException
import redis
import uuid
import os
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    r.ping()
    logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    sys.exit(1)

@app.get("/health")
def health_check():
    try:
        r.ping()
        return {"status": "healthy"}
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis connection failed")


@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush(QUEUE_NAME, job_id)
        r.hset(f"job:{job_id}", "status", "queued")
        logger.info(f"Created job {job_id}")
        return {"job_id": job_id}
    except redis.RedisError as e:
        logger.error(f"Failed to create job: {e}")
        raise HTTPException(status_code=500, detail="Failed to create job")


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
        if not status:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job_id": job_id, "status": status}
    except redis.RedisError as e:
        logger.error(f"Failed to get job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get job")


def signal_handler(sig, frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
