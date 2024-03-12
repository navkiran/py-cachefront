import os
import redis

cache_host = os.environ.get("CACHE_HOST", "redis")
cache_port = int(os.environ.get("CACHE_PORT", 6379))

redis_client = redis.Redis(host=cache_host, port=cache_port)


def get_cache_connection():
    return redis_client
