import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
import sys
import os
import redis

# Add the parent directory to the path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock Redis before importing main
mock_redis = Mock()
mock_redis.ping.return_value = True
mock_redis.lpush.return_value = 1
mock_redis.hset.return_value = 1
mock_redis.hget.return_value = "queued"
mock_redis.decode_responses = True

with patch('redis.Redis', return_value=mock_redis):
    from main import app

client = TestClient(app)


class TestHealthCheck:
    def test_health_check_healthy(self):
        """Test health check endpoint when Redis is healthy"""
        mock_redis.ping.return_value = True
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_check_unhealthy(self):
        """Test health check endpoint when Redis is unhealthy"""
        mock_redis.ping.side_effect = redis.ConnectionError("Connection failed")
        response = client.get("/health")
        assert response.status_code == 503
        assert "Redis connection failed" in response.json()["detail"]


class TestCreateJob:
    def test_create_job_success(self):
        """Test successful job creation"""
        mock_redis.lpush.return_value = 1
        mock_redis.hset.return_value = 1

        response = client.post("/jobs")

        assert response.status_code == 200
        assert "job_id" in response.json()
        assert len(response.json()["job_id"]) == 36  # UUID format

        # Verify Redis operations were called
        mock_redis.lpush.assert_called_once()
        mock_redis.hset.assert_called_once()

    def test_create_job_redis_error(self):
        """Test job creation when Redis fails"""
        mock_redis.lpush.side_effect = redis.RedisError("Redis error")

        response = client.post("/jobs")

        assert response.status_code == 500
        assert "Failed to create job" in response.json()["detail"]


class TestGetJob:
    def test_get_job_success(self):
        """Test successful job status retrieval"""
        mock_redis.hget.return_value = "completed"

        response = client.get("/jobs/test-job-id")

        assert response.status_code == 200
        assert response.json() == {"job_id": "test-job-id", "status": "completed"}
        mock_redis.hget.assert_called_once_with("job:test-job-id", "status")

    def test_get_job_not_found(self):
        """Test job status retrieval when job doesn't exist"""
        mock_redis.hget.return_value = None

        response = client.get("/jobs/nonexistent-job")

        assert response.status_code == 404
        assert "Job not found" in response.json()["detail"]

    def test_get_job_redis_error(self):
        """Test job status retrieval when Redis fails"""
        mock_redis.hget.side_effect = redis.RedisError("Redis error")

        response = client.get("/jobs/test-job-id")

        assert response.status_code == 500
        assert "Failed to get job" in response.json()["detail"]
