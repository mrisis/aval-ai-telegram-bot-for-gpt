from ..redis_client import redis_client
from ..models.user_model import User
from .base_model_crud import BaseRedisCRUD
import json


class UserCRUD(BaseRedisCRUD):
    model = User

    @classmethod
    def get(cls, key: str):
        data = redis_client.hget(name="users", key=key)
        if data:
            return cls.model(**json.loads(data))
        else:
            return None

    @classmethod
    def create(cls, instance: User):
        key = instance.id
        redis_client.hset(name='users', key=key, value=json.dumps(instance.dict(by_alias=True)))
        return instance

    @classmethod
    def update(cls, instance: User):
        key = instance.id
        if redis_client.exists(key):
            redis_client.hset(name='users', key=key, value=json.dumps(instance.dict(by_alias=True)))
            return instance
        else:
            return None

    @classmethod
    def delete(cls, key: str):
        if redis_client.exists(key):
            redis_client.delete(key)
            return True
        else:
            return False
