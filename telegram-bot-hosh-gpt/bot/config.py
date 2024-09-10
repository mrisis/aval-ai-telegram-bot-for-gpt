from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    telegram_token: str
    aval_ai_token: str
    aval_ai_url: str
    redis_host: str
    redis_port: int
    redis_db: int
    channel_id: str
    channel_id_member_ship: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Setting()
