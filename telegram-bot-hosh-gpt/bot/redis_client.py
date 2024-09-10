import redis
from .config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db
        )

    def get_client(self):
        return self.client


redis_client = RedisClient().get_client()
