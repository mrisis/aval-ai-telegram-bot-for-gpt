from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class CoreModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")

    class Config:
        allow_population_by_field_name = True
