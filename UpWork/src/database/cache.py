import redis

from Intuit.UpWork.src.config.config import REDIS_CONFIG

redis_cache = redis.Redis(**REDIS_CONFIG)

async def get_redis_client():
    return redis_cache