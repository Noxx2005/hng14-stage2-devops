import redis
import time
import os
import signal
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

running = True

def process_job(job_id):
    try:
        logger.info(f"Processing job {job_id}")
        time.sleep(2)  # simulate work
        r.hset(f"job:{job_id}", "status", "completed")
        logger.info(f"Done: {job_id}")
    except redis.RedisError as e:
        logger.error(f"Failed to process job {job_id}: {e}")


def signal_handler(sig, frame):
    global running
    logger.info(f"Received signal {sig}, shutting down gracefully...")
    running = False


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)
        if job:
            _, job_id = job
            process_job(job_id)
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        time.sleep(5)  # Wait before retrying

logger.info("Worker shutdown complete")