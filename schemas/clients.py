from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    id: Optional[int]
    name: str