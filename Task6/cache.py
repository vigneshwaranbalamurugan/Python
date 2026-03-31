import redis.asyncio as redis
from config import CACHE_TTL

redis_client = None

async def connect_redis():
    global redis_client
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=False
    )

async def get_cache(key):
    return await redis_client.get(key)

async def set_cache(key, value):
    await redis_client.set(key, value, ex=CACHE_TTL)