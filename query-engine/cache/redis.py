import os
import redis
from datetime import datetime

from codec import encode_data, decode_data

cache_host = os.environ.get("CACHE_HOST", "redis")
cache_port = int(os.environ.get("CACHE_PORT", 6379))

redis_client = redis.Redis(host=cache_host, port=cache_port)


def get_cache_connection():
    return redis_client


def invalidate_cache(cache_key):
    redis_client.delete(cache_key)


def read_from_cache(key):
    encoded_data = redis_client.get(key)
    if encoded_data:
        decoded_data = decode_data(encoded_data)
        return decoded_data
    return None


def load_lua_script(script_path):
    with open(script_path, "r") as file:
        return file.read()


lua_script = load_lua_script("deduplication_script.lua")


def write_to_cache(key, data, timestamp):
    """
    This function implements a cache invalidation strategy to deduplicate writes
    between the query engine and CDC. It ensures that only the newest value
    retrieved from the database is written to the cache.

    The function encodes the user data and timestamp into a single value and
    executes a Lua script in Redis to perform the deduplication logic. If a newer
    or equal timestamp value is already present in the cache, the write operation
    is skipped. Otherwise, the new value is written to the cache.

    The Lua script executed in Redis performs the deduplication logic atomically,
    ensuring consistency and avoiding race conditions.
    """
    encoded_data = encode_data(data, timestamp)
    redis_client.eval(
        lua_script,
        1,
        key,
        encoded_data,
        timestamp,
    )
