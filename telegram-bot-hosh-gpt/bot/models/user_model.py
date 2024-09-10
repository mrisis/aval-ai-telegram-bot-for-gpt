from .base_model import CoreModel


class User(CoreModel):
    username: str
    chat_id: int
