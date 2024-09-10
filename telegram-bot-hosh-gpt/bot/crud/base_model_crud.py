from abc import ABC, abstractmethod


class BaseRedisCRUD(ABC):
    model = None

    @classmethod
    @abstractmethod
    def get(cls, key: str):
        ...

    @classmethod
    @abstractmethod
    def create(cls, instance):
        ...

    @classmethod
    @abstractmethod
    def update(cls, instance):
        ...

    @classmethod
    @abstractmethod
    def delete(cls, key: str):
        ...
